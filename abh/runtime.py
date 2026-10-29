"""The reliability runtime: deterministic control of execution semantics.

Three modes are provided so that runtime capability is an independent experimental
factor (RQ2):

* ``none``        - passthrough; every failure is surfaced raw to the agent.
* ``naive_retry`` - conventional infrastructure retry: retries timeouts/5xx/429 with
                    backoff but without semantics (can duplicate side effects).
* ``semantic``    - semantics-aware: idempotency keys, reconciliation of ambiguous
                    outcomes via lookup, postcondition verification with visibility
                    waits, compensation of partial mutations, and *classification*
                    of what it cannot resolve (execution vs semantic).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .faults import FaultInjector, MalformedPayload
from .semantics import ExecutionState, FailureClass
from .contract import Contracts
from .tools import (BusinessError, InvalidRequest, InvocationContext, PartialFailure,
                    RateLimited, ServiceUnavailable, ToolError, ToolSpec, ToolTimeout)
from .trace import Trace
from .world import World


class RuntimeMode(str, Enum):
    NONE = "none"
    NAIVE_RETRY = "naive_retry"
    SEMANTIC = "semantic"


@dataclass
class RuntimeConfig:
    mode: RuntimeMode = RuntimeMode.NONE
    max_retries: int = 3
    backoff_ms: int = 500
    reconcile_polls: int = 4
    reconcile_wait_ms: int = 2500
    verify_postconditions: bool = True
    compensate_partial: bool = True
    # Fast path: after a timeout on a keyed write whose contract offers ``inspect``, ask how far
    # the attempt got instead of polling. Off by default, so registered studies are unchanged.
    inspect_partial: bool = False

    @classmethod
    def parse(cls, d) -> "RuntimeConfig":
        if isinstance(d, RuntimeConfig):
            return d
        if isinstance(d, str):
            return cls(mode=RuntimeMode(d))
        d = dict(d)
        d["mode"] = RuntimeMode(d.get("mode", "none"))
        return cls(**d)


@dataclass
class Outcome:
    call_id: str
    tool: str
    state: ExecutionState
    response: Optional[dict] = None
    error_kind: Optional[str] = None
    error_message: Optional[str] = None
    attempts: int = 0
    runtime_actions: List[str] = field(default_factory=list)
    failure_class: Optional[FailureClass] = None
    idempotency_key: Optional[str] = None
    malformed: bool = False

    @property
    def resolved(self) -> bool:
        return self.state in (ExecutionState.EXECUTED, ExecutionState.VERIFIED)

    def to_dict(self) -> dict:
        return {"call_id": self.call_id, "tool": self.tool, "state": self.state.value,
                "error_kind": self.error_kind, "error_message": self.error_message,
                "attempts": self.attempts, "runtime_actions": self.runtime_actions,
                "failure_class": self.failure_class.value if self.failure_class else None,
                "idempotency_key": self.idempotency_key, "malformed": self.malformed}


def _well_formed(tool: ToolSpec, resp: Any) -> bool:
    if isinstance(resp, MalformedPayload) or not isinstance(resp, dict):
        return False
    return all(f in resp for f in tool.response_fields)


class ReliabilityRuntime:
    def __init__(self, cfg: RuntimeConfig, world: World, injector: FaultInjector, trace: Trace,
                 contracts: Optional[Contracts] = None):
        self.cfg = cfg
        self.contracts = contracts or Contracts()
        self.world = world
        self.injector = injector
        self.trace = trace

    # ------------------------------------------------------------- public
    def execute(self, tool: ToolSpec, args: dict, call_id: str) -> Outcome:
        mode = self.cfg.mode
        if mode == RuntimeMode.SEMANTIC:
            out = self._semantic(tool, args, call_id)
        else:
            out = self._simple(tool, args, call_id, retry=(mode == RuntimeMode.NAIVE_RETRY))
        self.trace.emit("runtime_outcome", "runtime", **out.to_dict())
        return out

    # ------------------------------------------------- none / naive_retry
    def _simple(self, tool: ToolSpec, args: dict, call_id: str, retry: bool) -> Outcome:
        key = args.get("idempotency_key")
        out = Outcome(call_id, tool.name, ExecutionState.NOT_EXECUTED, idempotency_key=key)
        max_attempts = 1 + (self.cfg.max_retries if retry else 0)
        for attempt in range(1, max_attempts + 1):
            out.attempts = attempt
            ctx = InvocationContext(call_id, key, attempt, contract=self.contracts.of(tool))
            try:
                resp = self.injector.invoke(tool, args, self.world, ctx)
            except (BusinessError, InvalidRequest) as e:
                return self._fail(out, ExecutionState.SEMANTIC_FAILURE, e, FailureClass.SEMANTIC)
            except RateLimited as e:
                self._fail(out, ExecutionState.NOT_EXECUTED, e, FailureClass.EXECUTION)
                if retry:
                    out.runtime_actions.append("retry_after_429")
                    self.world.clock.wait(e.info.get("retry_after_ms", self.cfg.backoff_ms))
                    continue
                return out
            except ServiceUnavailable as e:
                self._fail(out, ExecutionState.NOT_EXECUTED, e, FailureClass.EXECUTION)
                if retry:
                    out.runtime_actions.append("blind_retry_5xx")
                    self.world.clock.wait(self.cfg.backoff_ms * 2 ** (attempt - 1))
                    continue
                return out
            except ToolTimeout as e:
                state = (ExecutionState.NOT_EXECUTED if tool.semantics.read_only
                         else ExecutionState.EXECUTION_UNKNOWN)
                self._fail(out, state, e, FailureClass.EXECUTION)
                if retry:
                    out.runtime_actions.append("blind_retry_timeout")
                    continue
                return out
            except PartialFailure as e:
                self._fail(out, ExecutionState.PARTIALLY_EXECUTED, e, FailureClass.EXECUTION)
                if retry:
                    out.runtime_actions.append("blind_retry_partial")
                    continue
                return out
            out.response = dict(resp)
            out.error_kind = out.error_message = out.failure_class = None
            if not _well_formed(tool, resp):
                out.malformed = True
                out.state = (ExecutionState.EXECUTED if tool.semantics.read_only
                             else ExecutionState.EXECUTION_UNKNOWN)
                out.failure_class = FailureClass.EXECUTION
                if retry and isinstance(resp, MalformedPayload):
                    out.runtime_actions.append("blind_retry_malformed")
                    continue
                return out
            out.state = ExecutionState.EXECUTED
            return out
        return out

    # ------------------------------------------------------------ semantic
    def _semantic(self, tool: ToolSpec, args: dict, call_id: str) -> Outcome:
        sem = tool.semantics
        c = self.contracts.of(tool)
        key = args.get("idempotency_key") or (f"rt-{call_id}" if c.keyed else None)
        out = Outcome(call_id, tool.name, ExecutionState.NOT_EXECUTED, idempotency_key=key)
        if key and c.keyed and "idempotency_key" not in args:
            out.runtime_actions.append("attach_idempotency_key")
        last_err: Optional[ToolError] = None
        for attempt in range(1, self.cfg.max_retries + 2):
            out.attempts = attempt
            ctx = InvocationContext(call_id, key, attempt, contract=self.contracts.of(tool))
            try:
                resp = self.injector.invoke(tool, args, self.world, ctx)
            except (BusinessError, InvalidRequest) as e:
                # The service understood and rejected the request: not a systems problem.
                return self._fail(out, ExecutionState.SEMANTIC_FAILURE, e, FailureClass.SEMANTIC)
            except RateLimited as e:
                last_err = e
                out.runtime_actions.append("honor_retry_after")
                self.world.clock.wait(e.info.get("retry_after_ms", self.cfg.backoff_ms))
                continue
            except ServiceUnavailable as e:
                last_err = e
                out.runtime_actions.append("backoff_retry")
                self.world.clock.wait(self.cfg.backoff_ms * 2 ** (attempt - 1))
                continue
            except ToolTimeout as e:
                last_err = e
                if sem.read_only:
                    out.runtime_actions.append("retry_read")
                    continue
                if self.cfg.inspect_partial and c.inspect and key and self._inspect_fast(tool, args, key, c, out):
                    continue
                found = self._reconcile(tool, args, key, out)
                if found is not None:
                    return self._success(tool, args, found, out)
                if key or sem.idempotent:
                    if (c.retry_may_duplicate_partial and self.cfg.compensate_partial
                            and tool.compensate and sem.compensable):
                        # A timeout can hide a partial commit that the key store never
                        # recorded (key scope "completed"); undo any incomplete attempt
                        # before replaying. Under an atomic key scope the replay returns the
                        # original outcome instead, so this isn't needed.
                        tool.compensate(self.world, args, key or call_id)
                        out.runtime_actions.append("compensate_unknown_partial")
                    out.runtime_actions.append("safe_retry_with_key" if key else "retry_idempotent")
                    continue
                out.runtime_actions.append("cannot_disambiguate")
                return self._fail(out, ExecutionState.EXECUTION_UNKNOWN, e, FailureClass.EXECUTION)
            except PartialFailure as e:
                last_err = e
                if self.cfg.compensate_partial and tool.compensate and sem.compensable:
                    tool.compensate(self.world, args, key or call_id)
                    out.runtime_actions.append("compensate_partial")
                    key = f"{key}-r{attempt}" if key else None
                    continue
                return self._fail(out, ExecutionState.PARTIALLY_EXECUTED, e, FailureClass.EXECUTION)

            if not _well_formed(tool, resp):
                out.malformed = True
                if sem.read_only:
                    out.runtime_actions.append("reread_malformed")
                    continue
                found = self._reconcile(tool, args, key, out)
                if found is not None:
                    return self._success(tool, args, found, out)
                if key:
                    out.runtime_actions.append("replay_with_key")
                    continue
                out.runtime_actions.append("cannot_parse_outcome")
                out.state = ExecutionState.EXECUTION_UNKNOWN
                out.failure_class = FailureClass.EXECUTION
                out.error_kind, out.error_message = "malformed_response", "unparseable response"
                return out
            return self._success(tool, args, resp, out)

        # Retries exhausted.
        if isinstance(last_err, (ServiceUnavailable, RateLimited)):
            # Persistent unavailability is a *semantic* problem: pick another route.
            return self._fail(out, ExecutionState.NOT_EXECUTED, last_err, FailureClass.SEMANTIC)
        state = (ExecutionState.EXECUTION_UNKNOWN if not sem.read_only else ExecutionState.NOT_EXECUTED)
        return self._fail(out, state, last_err or ToolError("retries exhausted"), FailureClass.EXECUTION)

    def _inspect_fast(self, tool: ToolSpec, args: dict, key: str, c, out: Outcome) -> bool:
        """Resolve a timeout from current state, without polling. True = retry now with the key.

        ``partial``: undo the committed part, then retry (only where a keyed retry would otherwise
        repeat it, i.e. key scope "completed"). ``absent``: nothing committed; retry. ``complete``
        or unknown: fall back to reconciling against visible state, which also waits until the
        write is visible, so the agent never reads state older than its own success.
        """
        status = tool.inspect(self.world, args, key)
        out.runtime_actions.append(f"inspect_{status or 'unknown'}")
        if status == "absent":
            out.runtime_actions.append("safe_retry_with_key")
            return True
        if (status == "partial" and c.retry_may_duplicate_partial and self.cfg.compensate_partial
                and tool.compensate and tool.semantics.compensable):
            tool.compensate(self.world, args, key)
            out.runtime_actions += ["compensate_partial_fast", "safe_retry_with_key"]
            return True
        return False

    def _reconcile(self, tool: ToolSpec, args: dict, key: Optional[str], out: Outcome) -> Optional[dict]:
        if tool.reconcile is None or key is None:
            return None
        for i in range(self.cfg.reconcile_polls):
            found = tool.reconcile(self.world, args, key)
            out.runtime_actions.append("reconcile_lookup")
            if found is not None:
                out.runtime_actions.append("reconciled_executed")
                return found
            self.world.clock.wait(self.cfg.reconcile_wait_ms)
        out.runtime_actions.append("reconcile_not_found")
        return None

    def _success(self, tool: ToolSpec, args: dict, resp: dict, out: Outcome) -> Outcome:
        out.response = dict(resp)
        out.error_kind = out.error_message = out.failure_class = None
        out.state = ExecutionState.EXECUTED
        if self.cfg.verify_postconditions and tool.postcondition is not None:
            for i in range(self.cfg.reconcile_polls):
                if tool.postcondition(self.world, args, out.response):
                    out.state = ExecutionState.VERIFIED
                    out.runtime_actions.append("postcondition_verified")
                    break
                out.runtime_actions.append("await_visibility")
                self.world.clock.wait(self.cfg.reconcile_wait_ms)
        return out

    @staticmethod
    def _fail(out: Outcome, state: ExecutionState, e: ToolError, fc: FailureClass) -> Outcome:
        out.state = state
        out.error_kind = e.kind
        out.error_message = e.message
        out.failure_class = fc
        return out


# ------------------------------------------------------------ agent view
def agent_view(out: Outcome, mode: RuntimeMode) -> Dict[str, Any]:
    """Render an outcome as the agent will see it.

    Without a semantic runtime the agent sees what a typical HTTP client returns.
    With it, unresolved outcomes are surfaced with structured execution semantics so
    the agent can tell *what it does not know* from *what went wrong*.
    """
    if mode != RuntimeMode.SEMANTIC:
        if out.resolved and not out.malformed:
            return {"content": out.response, "is_error": False}
        if out.malformed and out.response is not None:
            raw = out.response.get("_raw") if "_raw" in out.response else out.response
            return {"content": raw, "is_error": False}
        return {"content": f"Error ({out.error_kind}): {out.error_message}", "is_error": True}
    if out.resolved:
        body = dict(out.response or {})
        body["execution_state"] = out.state.value
        return {"content": body, "is_error": False}
    return {"content": {
        "execution_state": out.state.value,
        "failure_class": out.failure_class.value if out.failure_class else None,
        "error_type": out.error_kind,
        "message": out.error_message,
        "runtime_actions_taken": out.runtime_actions,
        "guidance": _guidance(out),
    }, "is_error": True}


def _guidance(out: Outcome) -> str:
    if out.failure_class == FailureClass.SEMANTIC:
        if out.state == ExecutionState.NOT_EXECUTED:
            return ("The action was NOT executed and the tool appears persistently unavailable. "
                    "Consider an alternative tool or approach.")
        return ("The service rejected the request; it was NOT executed. Retrying the same "
                "request will not help. Re-examine current state and revise the plan.")
    if out.state == ExecutionState.EXECUTION_UNKNOWN:
        return ("The runtime could not determine whether this action executed. Do not repeat "
                "it blindly; verify state or escalate.")
    if out.state == ExecutionState.PARTIALLY_EXECUTED:
        return "Part of this operation committed and could not be compensated automatically."
    return ""
