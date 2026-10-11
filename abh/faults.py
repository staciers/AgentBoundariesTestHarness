"""Controlled fault injection (prospectus §6).

Faults are injected *between* the caller and the service, so the same fault can be
observed by any control configuration. Each injected fault is recorded with its
ground-truth effect (did the side effect commit?) so the evaluator can attribute
who ultimately resolved it (RQ1: failure ownership).
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .semantics import FailureClass
from .tools import (InvocationContext, ServiceUnavailable, RateLimited, ToolSpec,
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


@dataclass
class FaultSpec:
    type: FaultType
    target: str = ""        # tool name or role (@write, @read, @multi, @semantic)
    on_call: int = 1        # trigger on the nth invocation of the target tool
    times: int = 1          # number of consecutive invocations affected
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def parse(cls, d) -> "FaultSpec":
        if isinstance(d, FaultSpec):
            return d
        if isinstance(d, str):
            d = {"type": d}
        ft = FaultType(d["type"])
        return cls(type=ft, target=d.get("target") or ft.default_target,
                   on_call=int(d.get("on_call", 1)),
                   times=int(d.get("times", 10 ** 6 if ft == FaultType.PERSISTENT_UNAVAILABLE else 1)),
                   params=dict(d.get("params", {})))

    def to_dict(self) -> dict:
        return {"type": self.type.value, "target": self.target, "on_call": self.on_call,
                "times": self.times, "params": self.params}


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


class MalformedPayload(dict):
    """Marker for a garbled response body."""


class FaultInjector:
    def __init__(self, specs: List[FaultSpec], semantic_defs: Dict[FaultType, SemanticFaultDef],
                 defaults: Optional[Dict[str, Any]] = None):
        self.specs = specs
        self.semantic_defs = semantic_defs
        self.defaults = {"delay_ms": 6000, "retry_after_ms": 2000, "timeout_ms": 30000}
        self.defaults.update(defaults or {})
        self._counts: Dict[str, int] = {}
        self.injected: List[InjectedFault] = []

    def _active(self, tool: str, n: int) -> Optional[FaultSpec]:
        for s in self.specs:
            if s.target == tool and s.on_call <= n < s.on_call + s.times:
                return s
        return None

    def _record(self, spec: FaultSpec, tool: str, ctx: InvocationContext, world: World) -> InjectedFault:
        f = InjectedFault(f"fault{len(self.injected) + 1}", spec.type, tool, ctx.call_id,
                          world.clock.now_ms)
        self.injected.append(f)
        return f

    def last_for_call(self, call_id: str) -> List[InjectedFault]:
        return [f for f in self.injected if f.call_id == call_id]

    def invoke(self, tool: ToolSpec, args: dict, world: World, ctx: InvocationContext) -> dict:
        n = self._counts[tool.name] = self._counts.get(tool.name, 0) + 1
        spec = self._active(tool.name, n)
        p = dict(self.defaults)
        if spec:
            p.update(spec.params)
        world.current_call_id = ctx.call_id
        world.clock.advance(tool.latency_ms)
        if spec is None:
            return tool.execute(world, args, ctx)

        ft = spec.type
        rec = self._record(spec, tool.name, ctx, world)
        n_effects = len(world.effects)

        def committed() -> bool:
            return len(world.effects) > n_effects

        if ft == FaultType.TIMEOUT_BEFORE_EXECUTION:
            world.clock.advance(p["timeout_ms"])
            rec.committed = False
            raise ToolTimeout(f"Request to {tool.name} timed out after {p['timeout_ms']}ms")
        if ft == FaultType.TRANSIENT_FAILURE or ft == FaultType.PERSISTENT_UNAVAILABLE:
            rec.committed = False
            raise ServiceUnavailable(f"503 Service Unavailable: {tool.name}")
        if ft == FaultType.RATE_LIMITED:
            rec.committed = False
            raise RateLimited(f"429 Too Many Requests: retry after {p['retry_after_ms']}ms",
                              retry_after_ms=p["retry_after_ms"])
        if ft == FaultType.PARTIAL_MUTATION:
            ctx.partial = True
            try:
                return tool.execute(world, args, ctx)
            finally:
                ctx.partial = False
                rec.committed = committed()

        sdef = self.semantic_defs.get(ft)
        if ft == FaultType.PRECONDITION_CHANGED and sdef and sdef.before:
            sdef.before(world)
            rec.notes.append(sdef.description)
        if ft == FaultType.TASK_INVALID_RESULT and sdef and sdef.before:
            sdef.before(world)

        world.begin_capture()
        try:
            resp = tool.execute(world, args, ctx)
            if ft == FaultType.DUPLICATE_EXECUTION:
                # e.g. a load balancer replays the request; server dedupes only with a key
                resp = tool.execute(world, args, ctx)
        finally:
            writes = world.end_capture()
            rec.committed = committed()

        if ft == FaultType.DELAYED_VISIBILITY:
            world.delay_visibility(writes, int(p["delay_ms"]))
        if ft == FaultType.TIMEOUT_AFTER_EXECUTION:
            world.clock.advance(p["timeout_ms"])
            raise ToolTimeout(f"Request to {tool.name} timed out after {p['timeout_ms']}ms")
        if ft == FaultType.MALFORMED_RESPONSE:
            return MalformedPayload({"_raw": "<html><body>502 Bad Gateway</body></html>"
                                             "\x00{\"stat"})
        if ft == FaultType.PARTIAL_RESPONSE:
            # Body truncated: the fields a caller needs to know what happened are lost.
            trimmed = {k: v for k, v in resp.items() if k not in tool.response_fields}
            return trimmed or {"status": "accepted"}
        if ft == FaultType.TASK_INVALID_RESULT and sdef and sdef.mutate_response:
            rec.notes.append(sdef.description)
            return sdef.mutate_response(copy.deepcopy(resp))
        return resp
