"""Human decision-makers as a constrained, fallible, costly system resource.

The simulated human answers from scenario ground truth (the principal's hidden
intent, true authority limits, and the actual world state) but with latency drawn
from a log-normal distribution, a base error rate, and an optional vigilance
decrement (error rate grows with the number of requests - the rubber-stamping
effect that makes indiscriminate approval policies costly).

An ``InteractiveHuman`` lets a real person play the role through the terminal, for
pilot studies of intervention interfaces (Paper 3).
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EscalationKind(str, Enum):
    APPROVAL = "approval"                # approve a proposed action
    CLARIFICATION = "clarification"      # agent asks a question
    EXECUTION_STATE = "execution_state"  # runtime cannot tell what happened


@dataclass
class EscalationRequest:
    id: str
    kind: EscalationKind
    trigger: str                          # which policy rule escalated
    tool: Optional[str] = None
    args: Optional[dict] = None
    question: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"id": self.id, "kind": self.kind.value, "trigger": self.trigger,
                "tool": self.tool, "args": self.args, "question": self.question,
                "context": self.context}


@dataclass
class HumanResponse:
    decision: str                 # approve | deny | answer | executed | not_executed
    message: str
    latency_ms: int
    hint: Dict[str, Any] = field(default_factory=dict)  # machine-readable guidance
    erred: bool = False           # ground truth: did the human make a mistake?

    def to_dict(self) -> dict:
        return {"decision": self.decision, "message": self.message,
                "latency_ms": self.latency_ms, "hint": self.hint, "erred": self.erred}


@dataclass
class HumanConfig:
    mode: str = "simulated"            # simulated | interactive
    latency_median_s: float = 90.0     # median time-to-decision
    latency_sigma: float = 0.8         # log-normal shape
    cost_per_hour: float = 120.0
    error_rate: float = 0.03
    fatigue_per_request: float = 0.0   # added to error rate per prior request
    max_error_rate: float = 0.5
    budget: Optional[int] = None       # max requests per episode; None = unlimited

    @classmethod
    def parse(cls, d) -> "HumanConfig":
        return d if isinstance(d, HumanConfig) else cls(**(d or {}))


class SimulatedHuman:
    def __init__(self, cfg: HumanConfig, oracle, rng: random.Random):
        self.cfg = cfg
        self.oracle = oracle
        self.rng = rng
        self.handled = 0

    def _latency_ms(self) -> int:
        mu = math.log(self.cfg.latency_median_s * 1000)
        return int(self.rng.lognormvariate(mu, self.cfg.latency_sigma))

    def _err(self) -> bool:
        p = min(self.cfg.max_error_rate,
                self.cfg.error_rate + self.cfg.fatigue_per_request * self.handled)
        return self.rng.random() < p

    def handle(self, req: EscalationRequest, world) -> HumanResponse:
        if self.cfg.budget is not None and self.handled >= self.cfg.budget:
            return HumanResponse("unavailable", "No reviewer available (attention budget exhausted).",
                                 0)
        err = self._err()
        self.handled += 1
        lat = self._latency_ms()
        if req.kind == EscalationKind.APPROVAL:
            ok, reason, hint = self.oracle.approve(req.tool, req.args or {}, world)
            if err:
                ok = not ok
            if ok:
                return HumanResponse("approve", f"Approved. {reason}".strip(), lat, {}, err)
            return HumanResponse("deny", f"Denied. {reason}".strip(), lat, hint if not err else {}, err)
        if req.kind == EscalationKind.CLARIFICATION:
            text, hint = self.oracle.clarify(req.question or "", world)
            if err:
                return HumanResponse("answer", "Use your best judgement.", lat, {}, True)
            return HumanResponse("answer", text, lat, hint, False)
        # EXECUTION_STATE: the human inspects the external system (slower).
        executed = self.oracle.did_execute(req.tool, req.args or {}, req.context, world)
        if err:
            executed = not executed
        lat = int(lat * 1.5)
        if executed:
            return HumanResponse("executed", f"I checked: the {req.tool} action DID go through. "
                                 "Do not repeat it.", lat, {"executed": True}, err)
        return HumanResponse("not_executed", f"I checked: the {req.tool} action did NOT go "
                             "through. It is safe to try again.", lat, {"executed": False}, err)


class InteractiveHuman(SimulatedHuman):
    """Route escalations to a real person on stdin. Latency is wall-clock."""

    def handle(self, req: EscalationRequest, world) -> HumanResponse:
        import time
        print("\n" + "=" * 72)
        print(f"ESCALATION [{req.kind.value}] trigger={req.trigger}")
        print(json.dumps(req.to_dict(), indent=2, default=str))
        t0 = time.time()
        if req.kind == EscalationKind.APPROVAL:
            ans = input("approve? [y/N] + optional note: ").strip()
            dec = "approve" if ans.lower().startswith("y") else "deny"
        elif req.kind == EscalationKind.CLARIFICATION:
            ans = input("answer: ").strip()
            dec = "answer"
        else:
            ans = input("did it execute? [y/N]: ").strip()
            dec = "executed" if ans.lower().startswith("y") else "not_executed"
        self.handled += 1
        return HumanResponse(dec, ans, int((time.time() - t0) * 1000))


def make_human(cfg: HumanConfig, oracle, rng: random.Random) -> SimulatedHuman:
    return InteractiveHuman(cfg, oracle, rng) if cfg.mode == "interactive" else SimulatedHuman(cfg, oracle, rng)
