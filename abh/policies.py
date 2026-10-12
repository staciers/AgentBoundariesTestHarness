"""Control-allocation policies P1-P6 and the oracle (prospectus §5).

A policy decides two things:

* ``gate``  - before execution: must a human approve this proposed action?
* ``route`` - after execution: who owns an outcome the runtime did not resolve?

The runtime mode is part of each policy's default configuration but may be
overridden in an experiment, making runtime capability and escalation policy
independently variable (e.g. P1 + semantic runtime isolates H1/H6).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .authority import AuthorityDecision
from .runtime import Outcome, RuntimeMode
from .semantics import Consequence, Controller, ExecutionState, FailureClass, SideEffect
from .tools import ToolSpec


@dataclass
class GateContext:
    tool: ToolSpec
    args: dict
    confidence: Optional[float]
    authority: AuthorityDecision
    oracle_needs_human: bool = False  # ground truth; only the ORACLE policy may read it


class ControlPolicy:
    name = "base"
    description = ""
    runtime_mode = RuntimeMode.NONE
    expose_ask_human = False
    require_confidence = False

    def __init__(self, **params):
        self.params = params
        if "runtime" in params:
            self.runtime_mode = RuntimeMode(params["runtime"])
        if "ask_human" in params:
            self.expose_ask_human = bool(params["ask_human"])
        # Whether agents may supply idempotency keys. Hiding them isolates "the platform
        # provides keys" from "the agent uses keys the platform offers" (H1 ablation).
        # The semantic runtime attaches its own keys either way.
        self.expose_keys = bool(params.get("expose_keys", True))
        # Wording of the idempotency_key description (see tools.KEY_DESCRIPTIONS); ablation only.
        self.key_description = str(params.get("key_description", "at_most_once"))
        from .tools import KEY_DESCRIPTIONS
        if self.key_description not in KEY_DESCRIPTIONS:
            raise ValueError(f"key_description must be one of {sorted(KEY_DESCRIPTIONS)}")

    @property
    def label(self) -> str:
        extras = {k: v for k, v in self.params.items()}
        return self.name if not extras else self.name + "[" + ",".join(f"{k}={v}" for k, v in sorted(extras.items())) + "]"

    def gate(self, g: GateContext) -> Optional[str]:
        return None

    def route(self, out: Outcome, tool: ToolSpec) -> Controller:
        return Controller.AGENT


class FullAutonomy(ControlPolicy):
    name = "P1"
    description = "Full agent autonomy: failures go to the model, no human."


class UniversalApproval(ControlPolicy):
    name = "P2"
    description = "Every side-effecting action requires human approval."

    def gate(self, g):
        return None if g.tool.semantics.read_only else "side_effecting_action"


class ConfidenceHITL(ControlPolicy):
    name = "P3"
    description = "Escalate when the agent's stated confidence is below a threshold."
    require_confidence = True

    def gate(self, g):
        thr = float(self.params.get("threshold", 0.7))
        conf = g.confidence if g.confidence is not None else float(self.params.get("missing", 0.5))
        return "low_confidence" if conf < thr else None


class StaticRiskHITL(ControlPolicy):
    name = "P4"
    description = "Actions at or above a consequence class always require approval."

    def gate(self, g):
        floor = Consequence.parse(self.params.get("min_consequence", "HIGH"))
        if not g.tool.semantics.read_only and g.tool.semantics.consequence >= floor:
            return "high_risk_action"
        return None


class AgentSelectedHITL(ControlPolicy):
    name = "P5"
    description = "The agent decides when to ask a human (ask_human tool)."
    expose_ask_human = True


def _consequential_unresolved(out: Outcome, tool: ToolSpec) -> bool:
    sem = tool.semantics
    if out.failure_class != FailureClass.EXECUTION:
        return False
    if out.state not in (ExecutionState.EXECUTION_UNKNOWN, ExecutionState.PARTIALLY_EXECUTED):
        return False
    return sem.consequence >= Consequence.HIGH or (not sem.reversible and sem.side_effect == SideEffect.EXTERNAL)


class SemanticRuntimeAware(ControlPolicy):
    name = "P6"
    description = ("Execution failures -> runtime; semantic failures -> agent; authority and "
                   "unresolved consequential uncertainty -> human.")
    runtime_mode = RuntimeMode.SEMANTIC
    require_confidence = True

    def gate(self, g):
        if not g.authority.permitted:
            return "authority:" + ",".join(g.authority.violated)
        sem = g.tool.semantics
        floor = Consequence.parse(self.params.get("min_consequence", "MEDIUM"))
        thr = float(self.params.get("threshold", 0.7))
        if not sem.read_only and sem.consequence >= floor and not (sem.reversible and sem.consequence < Consequence.HIGH):
            conf = g.confidence if g.confidence is not None else float(self.params.get("missing", 0.5))
            if conf < thr:
                return "consequential_epistemic_uncertainty"
        return None

    def route(self, out, tool):
        return Controller.HUMAN if _consequential_unresolved(out, tool) else Controller.AGENT


class OraclePolicy(ControlPolicy):
    name = "ORACLE"
    description = "Escalates exactly when ground truth says a human is needed (upper bound)."
    runtime_mode = RuntimeMode.SEMANTIC

    def gate(self, g):
        return "oracle" if g.oracle_needs_human else None

    def route(self, out, tool):
        return Controller.HUMAN if _consequential_unresolved(out, tool) else Controller.AGENT


POLICIES: Dict[str, type] = {c.name: c for c in (FullAutonomy, UniversalApproval, ConfidenceHITL,
                                                 StaticRiskHITL, AgentSelectedHITL, SemanticRuntimeAware,
                                                 OraclePolicy)}


def make_policy(spec: Any) -> ControlPolicy:
    if isinstance(spec, ControlPolicy):
        return spec
    if isinstance(spec, str):
        spec = {"name": spec}
    spec = dict(spec)
    cls = POLICIES[spec.pop("name").upper()]
    return cls(**spec)
