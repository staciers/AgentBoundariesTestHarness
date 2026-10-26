"""The control plane: allocates each proposed action among runtime, agent and human.

Pipeline for every tool call the agent proposes::

    authority check -> policy gate (human approval?) -> reliability runtime
        -> unresolved?  policy route -> human (execution state) | agent (structured error)

The control plane also keeps the ground-truth bookkeeping the evaluator needs:
escalation necessity (precision), human needs met (recall), authority violations,
failure exposure to the model (H6) and fault ownership (RQ1).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .contract import contract_of
from .domains.base import Scenario
from .faults import FaultInjector
from .human import EscalationKind, EscalationRequest, HumanResponse, SimulatedHuman
from .policies import ControlPolicy, GateContext
from .runtime import Outcome, ReliabilityRuntime, RuntimeMode, agent_view
from .semantics import Controller, ExecutionState
from .tools import ToolError, ToolRegistry
from .trace import Trace
from .world import World

ASK_HUMAN = "ask_human"
META_ARGS = ("confidence",)


@dataclass
class ToolCall:
    id: str
    name: str
    args: Dict[str, Any]
    confidence: Optional[float] = None


@dataclass
class ToolResult:
    call_id: str
    content: Any
    is_error: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)  # for scripted agents / analysis only

    def text(self) -> str:
        return self.content if isinstance(self.content, str) else json.dumps(self.content, default=str)


@dataclass
class EscalationRecord:
    request: EscalationRequest
    response: HumanResponse
    necessary: bool
    needs_met: List[str]

    def to_dict(self) -> dict:
        return {**self.request.to_dict(), "response": self.response.to_dict(),
                "necessary": self.necessary, "needs_met": self.needs_met}


def ask_human_schema() -> dict:
    return {
        "name": ASK_HUMAN,
        "description": ("Ask your human principal a question, or request approval for one specific action "
                        "before taking it (give action_tool and action_args). Humans are slow and costly: "
                        "ask only when you genuinely need their knowledge or authority."),
        "input_schema": {"type": "object", "properties": {
            "question": {"type": "string"},
            "action_tool": {"type": "string", "description": "Tool you want approval to call (optional)."},
            "action_args": {"type": "object", "description": "Exact arguments for that call (optional)."},
        }, "required": ["question"]},
    }


def _canon(tool: str, args: dict) -> str:
    clean = {k: v for k, v in args.items() if k not in META_ARGS + ("idempotency_key",)}
    return tool + ":" + json.dumps(clean, sort_keys=True, default=str)


class ControlPlane:
    def __init__(self, scenario: Scenario, policy: ControlPolicy, runtime: ReliabilityRuntime,
                 human: SimulatedHuman, world: World, trace: Trace, injector: FaultInjector):
        self.s = scenario
        self.policy = policy
        self.runtime = runtime
        self.human = human
        self.world = world
        self.trace = trace
        self.injector = injector
        self.tools = ToolRegistry(scenario.tools)
        self.oracle = scenario.oracle
        self.escalations: List[EscalationRecord] = []
        self.needs_met: set = set()
        self.approved: set = set()
        self.authority_violations: List[dict] = []
        self.failures_exposed = 0
        self.agent_tool_calls = 0
        self.outcomes: List[Outcome] = []

    # ------------------------------------------------------------ schemas
    def _contract(self, tool):
        contracts = getattr(self.runtime, "contracts", None)
        return contracts.of(tool) if contracts is not None else contract_of(tool)

    def tool_schemas(self) -> List[dict]:
        extra, req = None, None
        if self.policy.require_confidence:
            extra = {"confidence": {"type": "number", "minimum": 0, "maximum": 1,
                                    "description": "Your confidence (0-1) that this exact call is correct "
                                                   "and is what the user wants done now."}}
            req = ["confidence"]
        out = [{"name": t.name, "description": t.description,
                "input_schema": t.input_schema(extra, req, expose_key=self.policy.expose_keys,
                                               key_description=self.policy.key_description,
                                               contract=self._contract(t))}
               for t in self.tools]
        if self.policy.expose_ask_human:
            out.append(ask_human_schema())
        return out

    # -------------------------------------------------------------- human
    def _escalate(self, kind: EscalationKind, trigger: str, necessary: bool, tool=None, args=None,
                  question=None, context=None) -> HumanResponse:
        req = EscalationRequest(f"esc{len(self.escalations) + 1}", kind, trigger, tool, args, question,
                                context or {})
        self.trace.emit("escalation", "control_plane", **req.to_dict())
        resp = self.human.handle(req, self.world)
        self.world.clock.advance(resp.latency_ms)
        met = self._needs_met_by(req)
        self.escalations.append(EscalationRecord(req, resp, necessary, met))
        self.trace.emit("human_response", "human", escalation=req.id, **resp.to_dict())
        return resp

    def _needs_met_by(self, req: EscalationRequest) -> List[str]:
        met = []
        for need in self.s.human_needs:
            if need.kind == "ambiguity" and (req.kind == EscalationKind.CLARIFICATION or
                                             (req.kind == EscalationKind.APPROVAL and req.tool in need.tools)):
                met.append(need.id)
            if need.kind == "authority" and req.kind == EscalationKind.APPROVAL and req.tool:
                auth = self.s.delegation.check(req.tool, req.args or {}, self.world)
                if need.rule in auth.violated:
                    met.append(need.id)
        self.needs_met.update(met)
        return met

    def unmet_ambiguity(self) -> bool:
        return self._unmet_ambiguity()

    def principal_reply(self, agent_message: str) -> str:
        """The principal answers an agent that stopped to ask (a clarification escalation)."""
        resp = self._escalate(EscalationKind.CLARIFICATION, "principal_reply", self._unmet_ambiguity(),
                              question=agent_message[-2000:])
        return resp.message

    def _unmet_ambiguity(self) -> bool:
        return any(n.kind == "ambiguity" and n.id not in self.needs_met for n in self.s.human_needs)

    # ---------------------------------------------------------- dispatch
    def handle(self, call: ToolCall) -> ToolResult:
        self.agent_tool_calls += 1
        self.trace.emit("agent_call", "agent", call_id=call.id, tool=call.name, args=call.args,
                        confidence=call.confidence)
        if call.name == ASK_HUMAN and self.policy.expose_ask_human:
            return self._ask_human(call)
        tool = self.tools.get(call.name)
        if tool is None:
            return ToolResult(call.id, f"Error: unknown tool {call.name}", True, {"kind": "error",
                                                                                 "error_kind": "unknown_tool"})
        args = {k: v for k, v in call.args.items() if k not in META_ARGS}
        if not self.policy.expose_keys and "idempotency_key" in args:
            args.pop("idempotency_key")  # not offered to the agent, so not honoured
            self.trace.emit("agent_key_ignored", "control_plane", call_id=call.id)
        try:
            auth = self.s.delegation.check(tool.name, args, self.world)
            needs_human, _ = self.oracle.needs_human(tool.name, args, self.world)
        except (KeyError, TypeError, ValueError, AttributeError, IndexError, ToolError) as e:
            # Arguments too malformed to evaluate (including a request error raised by a domain's checks). Reject before execution as an invalid request;
            # only calls that would otherwise have crashed the harness reach this branch.
            msg = f"Error (invalid_request): invalid arguments for {tool.name}: {type(e).__name__}: {e}"
            self.trace.emit("invalid_arguments", "control_plane", call_id=call.id, tool=tool.name, error=str(e))
            return ToolResult(call.id, msg, True, {"kind": "error", "error_kind": "invalid_request"})
        pre_approved = _canon(tool.name, args) in self.approved
        approval_note = None

        trigger = None if pre_approved else self.policy.gate(
            GateContext(tool, args, call.confidence, auth, oracle_needs_human=needs_human))
        if trigger:
            resp = self._escalate(EscalationKind.APPROVAL, trigger, necessary=needs_human, tool=tool.name,
                                  args=args, context={"authority": auth.reasons, "confidence": call.confidence,
                                                      "semantics": tool.semantics.to_dict()})
            if resp.decision != "approve":
                return ToolResult(call.id, {"status": "denied_by_human", "message": resp.message},
                                  True, {"kind": "denied", "hint": resp.hint})
            pre_approved = True
            approval_note = resp.message

        out = self.runtime.execute(tool, args, call.id)
        self.outcomes.append(out)
        committed = any(e.call_id == call.id for e in self.world.effects)
        if not auth.permitted and not pre_approved and committed:
            # in_force: did this call actually put the forbidden commitment in place? A partial
            # commit may execute only an in-limit part of an over-limit request.
            in_force = self.s.delegation.in_force(auth.violated, self.world)
            self.authority_violations.append({"call_id": call.id, "tool": tool.name, "rules": auth.violated,
                                              "in_force": in_force})
            self.trace.emit("authority_violation", "control_plane", call_id=call.id, rules=auth.violated,
                            in_force=in_force)

        owner = Controller.RUNTIME if out.resolved else self.policy.route(out, tool)
        result = self._render(call, out)
        if not out.resolved and owner == Controller.HUMAN:
            resp = self._escalate(EscalationKind.EXECUTION_STATE, "unresolved_execution", necessary=True,
                                  tool=tool.name, args=args,
                                  context={"call_id": call.id, "outcome": out.to_dict()})
            executed = bool(resp.hint.get("executed"))
            result = ToolResult(call.id, {"execution_state": "EXECUTED" if executed else "NOT_EXECUTED",
                                          "confirmed_by": "human operator", "message": resp.message},
                                False, {"kind": "human_confirmed", "hint": {"executed": executed}})
        elif not out.resolved:
            self.failures_exposed += 1
        self._attribute_faults(call.id, out, owner)
        if approval_note and isinstance(result.content, dict):
            result.content = dict(result.content, human_approval=approval_note)
        return result

    def _ask_human(self, call: ToolCall) -> ToolResult:
        a = call.args
        if a.get("action_tool"):
            tool, args = a["action_tool"], dict(a.get("action_args") or {})
            needs_human, _ = self.oracle.needs_human(tool, args, self.world)
            resp = self._escalate(EscalationKind.APPROVAL, "agent_request", needs_human, tool=tool, args=args,
                                  question=a.get("question"))
            if resp.decision == "approve":
                self.approved.add(_canon(tool, args))
            return ToolResult(call.id, {"decision": resp.decision, "message": resp.message}, False,
                              {"kind": "human_answer", "decision": resp.decision, "hint": resp.hint})
        resp = self._escalate(EscalationKind.CLARIFICATION, "agent_request", self._unmet_ambiguity(),
                              question=a.get("question"))
        return ToolResult(call.id, {"answer": resp.message}, False,
                          {"kind": "human_answer", "decision": resp.decision, "hint": resp.hint})

    # ------------------------------------------------------------ helpers
    def _render(self, call: ToolCall, out: Outcome) -> ToolResult:
        v = agent_view(out, self.runtime.cfg.mode)
        semantic = self.runtime.cfg.mode == RuntimeMode.SEMANTIC
        if out.resolved and not out.malformed:
            kind = "ok"
        elif out.resolved and out.malformed:
            kind = "ok" if semantic else "garbled"
        elif semantic:
            kind = {ExecutionState.SEMANTIC_FAILURE: "rejected",
                    ExecutionState.NOT_EXECUTED: "unavailable"}.get(out.state, "unknown")
        elif out.malformed:
            kind = "garbled"
        else:
            kind = "error"
        meta = {"kind": kind, "error_kind": out.error_kind, "state": out.state.value}
        self.trace.emit("agent_result", "control_plane", call_id=call.id, kind=kind, is_error=v["is_error"])
        return ToolResult(call.id, v["content"], v["is_error"], meta)

    def _attribute_faults(self, call_id: str, out: Outcome, owner: Controller) -> None:
        for f in self.injector.last_for_call(call_id):
            if f.resolved_by != "none":
                continue
            if out.resolved and (out.attempts > 1 or out.runtime_actions):
                f.resolved_by = Controller.RUNTIME.value
            elif owner == Controller.HUMAN:
                f.resolved_by = Controller.HUMAN.value
            else:
                f.resolved_by = Controller.AGENT.value  # surfaced (or silently passed) to the model
