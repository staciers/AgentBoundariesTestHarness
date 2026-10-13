"""Controlled fault injection (prospectus §6).

Faults are injected *between* the caller and the service, so the same fault can be
observed by any control configuration. Each injected fault is recorded with its
ground-truth effect (did the side effect commit?) so the evaluator can attribute
who ultimately resolved it (RQ1: failure ownership).

Rate-based faults: a spec with ``rate`` set fails each invocation of its target with that
probability instead of at scheduled calls (Phase IV: failure frequencies). Sampling is a
hash of (episode seed, spec, tool, call number), so it's reproducible and independent of
how other tools' calls interleave. Targets ``@writes``, ``@reads`` and ``@any`` expand to
every matching tool. Only execution faults can be rate-based.

Compound faults: several specs may be active on the same invocation. They compose in
the order a real request experiences them (see ``FaultInjector.invoke``). At most one
*pre-execution* fault and at most one *response* fault may overlap on a call;
``validate_compound`` rejects other combinations when the episode is set up.
"""
from __future__ import annotations

import copy
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .semantics import FailureClass
from .tools import (InvocationContext, ServiceUnavailable, RateLimited, ToolError, ToolSpec,
                    ToolTimeout)
from .world import World


class FaultType(str, Enum):
    TIMEOUT_BEFORE_EXECUTION = "timeout_before_execution"
    TIMEOUT_AFTER_EXECUTION = "timeout_after_execution"
    TRANSIENT_FAILURE = "transient_failure"
    RATE_LIMITED = "rate_limited"
    MALFORMED_RESPONSE = "malformed_response"
    PARTIAL_RESPONSE = "partial_response"
    DELAYED_VISIBILITY = "delayed_visibility"
    DUPLICATE_EXECUTION = "duplicate_execution"
    PARTIAL_MUTATION = "partial_mutation"
    PERSISTENT_UNAVAILABLE = "persistent_unavailable"
    PRECONDITION_CHANGED = "precondition_changed"
    TASK_INVALID_RESULT = "task_invalid_result"

    @property
    def failure_class(self) -> FailureClass:
        return (FailureClass.SEMANTIC if self in _SEMANTIC_FAULTS
                else FailureClass.EXECUTION)

    @property
    def default_target(self) -> str:
        return _DEFAULT_TARGET.get(self, "@write")


_SEMANTIC_FAULTS = {FaultType.PERSISTENT_UNAVAILABLE, FaultType.PRECONDITION_CHANGED,
                    FaultType.TASK_INVALID_RESULT}
_DEFAULT_TARGET = {
    FaultType.PARTIAL_MUTATION: "@multi",
    FaultType.PERSISTENT_UNAVAILABLE: "@unavailable",
    FaultType.PRECONDITION_CHANGED: "@semantic",
    FaultType.TASK_INVALID_RESULT: "@semantic",
}

# Phases a request passes through. Pre-execution faults stop the request before the
# service runs; execution modifiers change what the service commits; response faults
# change what the caller receives.
PRE_EXECUTION = {FaultType.TIMEOUT_BEFORE_EXECUTION, FaultType.TRANSIENT_FAILURE,
                 FaultType.PERSISTENT_UNAVAILABLE, FaultType.RATE_LIMITED}
RESPONSE = {FaultType.TIMEOUT_AFTER_EXECUTION, FaultType.MALFORMED_RESPONSE, FaultType.PARTIAL_RESPONSE}


@dataclass
class FaultSpec:
    type: FaultType
    target: str = ""        # tool name or role (@write, @read, @multi, @semantic)
    on_call: int = 1        # trigger on the nth invocation of the target tool
    times: int = 1          # number of consecutive invocations affected
    params: Dict[str, Any] = field(default_factory=dict)
    rate: Optional[float] = None  # if set: fail each invocation with this probability instead

    @property
    def label(self) -> str:
        if self.rate is None:
            return self.type.value
        tgt = "" if self.target == self.type.default_target else f"[{self.target}]"
        return f"{self.type.value}{tgt}~{self.rate:g}"

    @classmethod
    def parse(cls, d) -> "FaultSpec":
        if isinstance(d, FaultSpec):
            return d
        if isinstance(d, str):
            d = {"type": d}
        ft = FaultType(d["type"])
        rate = d.get("rate")
        if rate is not None:
            rate = float(rate)
            if not 0.0 <= rate <= 1.0:
                raise ValueError(f"rate must be in [0, 1], got {rate}")
            if ft.failure_class != FailureClass.EXECUTION:
                raise ValueError(f"{ft.value} is a semantic fault; only execution faults can be rate-based")
        return cls(type=ft, target=d.get("target") or ft.default_target,
                   on_call=int(d.get("on_call", 1)),
                   times=int(d.get("times", 10 ** 6 if ft == FaultType.PERSISTENT_UNAVAILABLE else 1)),
                   params=dict(d.get("params", {})), rate=rate)

    def to_dict(self) -> dict:
        d = {"type": self.type.value, "target": self.target, "on_call": self.on_call,
             "times": self.times, "params": self.params}
        if self.rate is not None:  # only rate specs carry it, so existing episode keys are unchanged
            d["rate"] = self.rate
        return d


@dataclass
class SemanticFaultDef:
    """Domain-provided realisation of a semantic fault on a specific tool."""

    tool: str
    before: Optional[Callable[[World], None]] = None          # mutate world first
    mutate_response: Optional[Callable[[dict], dict]] = None  # corrupt a valid result
    description: str = ""


@dataclass
class InjectedFault:
    id: str
    type: FaultType
    tool: str
    call_id: str
    t_ms: int
    committed: Optional[bool] = None   # ground truth: did a side effect commit?
    resolved_by: str = "none"          # runtime | agent | human | none
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.type.value, "tool": self.tool,
                "call_id": self.call_id, "t_ms": self.t_ms, "committed": self.committed,
                "resolved_by": self.resolved_by, "notes": self.notes}


def _overlap(a: "FaultSpec", b: "FaultSpec") -> bool:
    if a.rate is not None or b.rate is not None:
        return False  # rate specs are reconciled per call at injection time (see FaultInjector._active)
    return a.target == b.target and a.on_call < b.on_call + b.times and b.on_call < a.on_call + a.times


def conflicts(a: FaultType, b: FaultType) -> bool:
    """Can these two faults not both apply to one request?"""
    if a == b:
        return True
    if (a in PRE_EXECUTION and b in PRE_EXECUTION) or (a in RESPONSE and b in RESPONSE):
        return True
    pre, other = (a, b) if a in PRE_EXECUTION else (b, a) if b in PRE_EXECUTION else (None, None)
    return pre is not None and other != FaultType.PRECONDITION_CHANGED


def validate_compound(specs: List["FaultSpec"]) -> None:
    """Reject fault combinations that cannot both apply to one request."""
    for i, a in enumerate(specs):
        for b in specs[i + 1:]:
            if not _overlap(a, b):
                continue
            if a.type == b.type:
                raise ValueError(f"{a.type.value} specified twice for the same call of {a.target}")
            for phase, name in ((PRE_EXECUTION, "pre-execution"), (RESPONSE, "response")):
                if a.type in phase and b.type in phase:
                    raise ValueError(f"{a.type.value} and {b.type.value} are both {name} faults on "
                                     f"{a.target}; at most one can apply to a call")
            pre = a if a.type in PRE_EXECUTION else b if b.type in PRE_EXECUTION else None
            if pre is not None:
                other = b if pre is a else a
                if other.type != FaultType.PRECONDITION_CHANGED:
                    raise ValueError(f"{pre.type.value} prevents execution, so {other.type.value} on the "
                                     f"same call of {a.target} would never apply")


class MalformedPayload(dict):
    """Marker for a garbled response body."""


class FaultInjector:
    def __init__(self, specs: List[FaultSpec], semantic_defs: Dict[FaultType, SemanticFaultDef],
                 defaults: Optional[Dict[str, Any]] = None, seed: int = 0):
        self.specs = specs
        self.seed = seed
        self.semantic_defs = semantic_defs
        self.defaults = {"delay_ms": 6000, "retry_after_ms": 2000, "timeout_ms": 30000}
        self.defaults.update(defaults or {})
        self._counts: Dict[str, int] = {}
        self.injected: List[InjectedFault] = []

    def _draw(self, i: int, tool: str, n: int) -> float:
        h = hashlib.sha256(f"{self.seed}:{i}:{tool}:{n}".encode()).digest()
        return int.from_bytes(h[:8], "big") / 2 ** 64

    def _active(self, tool: str, n: int) -> List[FaultSpec]:
        active = [s for s in self.specs if s.rate is None and s.target == tool and s.on_call <= n < s.on_call + s.times]
        for i, s in enumerate(self.specs):
            if s.rate is None or s.target != tool or self._draw(i, tool, n) >= s.rate:
                continue
            # Several rate specs can fire on one call; keep the earlier ones when they conflict.
            if not any(conflicts(s.type, a.type) for a in active):
                active.append(s)
        return active

    def _record(self, spec: FaultSpec, tool: str, ctx: InvocationContext, world: World) -> InjectedFault:
        f = InjectedFault(f"fault{len(self.injected) + 1}", spec.type, tool, ctx.call_id,
                          world.clock.now_ms)
        self.injected.append(f)
        return f

    def last_for_call(self, call_id: str) -> List[InjectedFault]:
        return [f for f in self.injected if f.call_id == call_id]

    def invoke(self, tool: ToolSpec, args: dict, world: World, ctx: InvocationContext) -> dict:
        """Run one service invocation with every fault active on it, composed in phase order:

        1. world-changing hooks (precondition changed, task-invalid ``before``)
        2. a pre-execution fault, if any, raises and nothing executes
        3. execution with modifiers (partial mutation, duplicate execution); writes are
           captured so delayed visibility can hide them, even if execution raised
        4. a response fault, if any: a timeout masks whatever happened (success or error);
           otherwise a malformed/partial body or a task-invalid mutation replaces the response.
           Delayed visibility counts from this moment (when the caller gets its answer).
        """
        n = self._counts[tool.name] = self._counts.get(tool.name, 0) + 1
        specs = self._active(tool.name, n)
        world.current_call_id = ctx.call_id
        world.clock.advance(tool.latency_ms)
        if not specs:
            return tool.execute(world, args, ctx)

        p = dict(self.defaults)
        for spec in specs:
            p.update(spec.params)
        recs = {spec.type: self._record(spec, tool.name, ctx, world) for spec in specs}
        active = set(recs)
        n_effects = len(world.effects)

        def settle() -> None:
            done = len(world.effects) > n_effects
            for r in recs.values():
                r.committed = done

        # 1. world-changing hooks
        for ft in (FaultType.PRECONDITION_CHANGED, FaultType.TASK_INVALID_RESULT):
            sdef = self.semantic_defs.get(ft)
            if ft in active and sdef and sdef.before:
                sdef.before(world)
                recs[ft].notes.append(sdef.description)

        # 2. pre-execution failure
        if FaultType.TIMEOUT_BEFORE_EXECUTION in active:
            world.clock.advance(p["timeout_ms"])
            settle()
            raise ToolTimeout(f"Request to {tool.name} timed out after {p['timeout_ms']}ms")
        if active & {FaultType.TRANSIENT_FAILURE, FaultType.PERSISTENT_UNAVAILABLE}:
            settle()
            raise ServiceUnavailable(f"503 Service Unavailable: {tool.name}")
        if FaultType.RATE_LIMITED in active:
            settle()
            raise RateLimited(f"429 Too Many Requests: retry after {p['retry_after_ms']}ms",
                              retry_after_ms=p["retry_after_ms"])

        # 3. execution with modifiers
        resp: Optional[dict] = None
        error: Optional[ToolError] = None
        ctx.partial = FaultType.PARTIAL_MUTATION in active
        world.begin_capture()
        try:
            resp = tool.execute(world, args, ctx)
            if FaultType.DUPLICATE_EXECUTION in active:
                # e.g. a load balancer replays the request; server dedupes only with a key
                resp = tool.execute(world, args, ctx)
        except ToolError as e:
            error = e
        finally:
            ctx.partial = False
            writes = world.end_capture()
            settle()

        # 4. response faults. Visibility lag is measured from when the caller gets its answer
        # (response or timeout), so a lag shorter than the timeout still matters.
        if FaultType.TIMEOUT_AFTER_EXECUTION in active:
            world.clock.advance(p["timeout_ms"])
        if FaultType.DELAYED_VISIBILITY in active:
            world.delay_visibility(writes, int(p["delay_ms"]))
        if FaultType.TIMEOUT_AFTER_EXECUTION in active:
            raise ToolTimeout(f"Request to {tool.name} timed out after {p['timeout_ms']}ms")
        if error is not None:
            raise error
        if FaultType.MALFORMED_RESPONSE in active:
            return MalformedPayload({"_raw": "<html><body>502 Bad Gateway</body></html>"
                                             "\x00{\"stat"})
        if FaultType.PARTIAL_RESPONSE in active:
            # Body truncated: the fields a caller needs to know what happened are lost.
            trimmed = {k: v for k, v in resp.items() if k not in tool.response_fields}
            return trimmed or {"status": "accepted"}
        sdef = self.semantic_defs.get(FaultType.TASK_INVALID_RESULT)
        if FaultType.TASK_INVALID_RESULT in active and sdef and sdef.mutate_response:
            recs[FaultType.TASK_INVALID_RESULT].notes.append(sdef.description)
            return sdef.mutate_response(copy.deepcopy(resp))
        return resp
