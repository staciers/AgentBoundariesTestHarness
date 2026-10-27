"""Tool specifications and service-side execution (including idempotency keys).

A ``ToolSpec`` is the contract between a stateful service and its callers. Beyond
the JSON schema an LLM sees, it carries the action semantics and optional hooks the
reliability runtime may exploit: response validation, postcondition checks,
reconciliation (lookup-by-client-reference) and compensation.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .contract import describe_key
from .semantics import ActionSemantics, Consequence, READ_ONLY, SideEffect
from .world import World


# ----------------------------------------------------------------- errors
class ToolError(Exception):
    kind = "error"
    http_status = 500

    def __init__(self, message: str = "", **info):
        super().__init__(message or self.kind)
        self.message = message or self.kind
        self.info = info


class ToolTimeout(ToolError):
    kind = "timeout"
    http_status = 504


class ServiceUnavailable(ToolError):
    kind = "unavailable"
    http_status = 503


class RateLimited(ToolError):
    kind = "rate_limited"
    http_status = 429


class BusinessError(ToolError):
    """Request understood and rejected by the service (sold out, conflict, quarantined...).

    These are *semantic* failures: retrying the same request will not help.
    """

    kind = "business_error"
    http_status = 409


class PartialFailure(ToolError):
    """Multi-part operation committed some, not all, of its parts."""

    kind = "partial_failure"
    http_status = 500


class InvalidRequest(ToolError):
    kind = "invalid_request"
    http_status = 400


# ---------------------------------------------------------------- context
@dataclass
class InvocationContext:
    call_id: str
    idempotency_key: Optional[str] = None
    attempt: int = 1
    partial: bool = False  # set by fault injector: commit only the first part
    contract: Any = None   # the tool's ExecutionContract for this episode (abh.contract)


Handler = Callable[[World, dict, InvocationContext], dict]


@dataclass
class ToolSpec:
    name: str
    description: str
    params: Dict[str, dict]
    handler: Handler
    required: List[str] = field(default_factory=list)
    semantics: ActionSemantics = READ_ONLY
    latency_ms: int = 300
    # Fields a well-formed success response must contain (runtime validation).
    response_fields: List[str] = field(default_factory=list)
    # postcondition(world, args, response) -> bool using *visible* state.
    postcondition: Optional[Callable[[World, dict, dict], bool]] = None
    # reconcile(world, args, idempotency_key) -> response if the action is
    # observable as executed, else None. Uses visible state only.
    reconcile: Optional[Callable[[World, dict, str], Optional[dict]]] = None
    # compensate(world, args, idempotency_key) -> undo the effects of an *incomplete*
    # attempt made with this key. Must be a no-op if that attempt completed, because the
    # runtime may call it when it cannot tell whether a request finished.
    compensate: Optional[Callable[[World, dict, str], None]] = None
    tags: List[str] = field(default_factory=list)

    def input_schema(self, extra: Optional[Dict[str, dict]] = None,
                     extra_required: Optional[List[str]] = None, expose_key: bool = True,
                     key_description: str = "at_most_once", contract: Any = None) -> dict:
        props = dict(self.params)
        req = list(self.required)
        if self.semantics.supports_idempotency_key and expose_key:
            props["idempotency_key"] = {
                "type": "string",
                "description": (describe_key(contract) if key_description == "contract"
                                else KEY_DESCRIPTIONS[key_description]),
            }
        if extra:
            props.update(extra)
            req.extend(extra_required or [])
        return {"type": "object", "properties": props, "required": req,
                "additionalProperties": False}

    def execute(self, world: World, args: dict, ctx: InvocationContext) -> dict:
        """Service-side execution with server-enforced idempotency keys."""
        key = ctx.idempotency_key if self.semantics.supports_idempotency_key else None
        atomic = key and ctx.contract is not None and ctx.contract.key_scope.value == "atomic"
        report = ctx.contract is not None and ctx.contract.partial_report
        if key:
            prior = world.get(f"_idem:{self.name}", key, visible=False)
            if prior is not None:
                if "partial_error" in prior:  # atomic scope: replay the original partial outcome
                    raise PartialFailure(f"A request with this idempotency key already failed partway and was not "
                                         f"executed again. Original error: {prior['partial_error']}"
                                         + (_committed_text(prior.get("committed", [])) if report else ""))
                return dict(prior["response"])
        clean = {k: v for k, v in args.items() if k != "idempotency_key"}
        n_effects = len(world.effects)
        try:
            resp = self.handler(world, clean, ctx)
        except PartialFailure as e:
            committed = [_effect_summary(x) for x in world.effects[n_effects:]]
            if atomic:  # the key is recorded with the committed part
                rec = {"partial_error": str(e)}
                if report or (ctx.contract is not None and ctx.contract.repair.value == "cancel_partial"):
                    rec.update(committed=committed, args=clean)
                world.put(f"_idem:{self.name}", key, rec)
            if report:
                raise PartialFailure(str(e) + _committed_text(committed), **e.info) from e
            raise
        except ToolError:
            raise
        except (KeyError, TypeError, ValueError, AttributeError, IndexError) as e:
            # A malformed call (wrong argument shape) is the caller's error, as a 400 from a real API,
            # not a harness crash. Only calls that would otherwise have crashed reach this branch.
            raise InvalidRequest(f"Invalid arguments for {self.name}: {type(e).__name__}: {e}")
        if key:
            world.put(f"_idem:{self.name}", key, {"response": resp})
        return resp


# How the idempotency_key parameter is described to agents (key-wording ablation).
# "at_most_once" is the original wording; the others test whether the promise it makes
# drives over-trust. The service behaves identically under all three: it records a key
# only when a request completes.
KEY_DESCRIPTIONS = {
    "contract": None,  # generated from the tool's execution contract (abh.contract.describe_key)
    "at_most_once": "Optional client-supplied key. Requests repeated with the same key are executed at most once.",
    "neutral": "Optional client-supplied request identifier.",
    "caveated": ("Optional client-supplied key. A request repeated with the same key is not executed again if the "
                 "first one completed. If the first request failed partway, part of it may already have taken "
                 "effect; check current state before retrying."),
}


def _effect_summary(e) -> dict:
    return {"kind": e.kind, **{k: v for k, v in e.data.items() if not str(k).startswith("_")}}


def _committed_text(committed: list) -> str:
    return " Committed before the failure: " + json.dumps(committed, default=str, sort_keys=True)


def make_cancel_partial_tool(tools: List["ToolSpec"]) -> "ToolSpec":
    """``cancel_partial(tool, key)``: the repair operation an execution contract can declare.

    It undoes exactly what a partially failed keyed request committed (via the tool's own
    compensation hook) and clears the key's record, so the full request can be sent again with
    the same key. Only requests recorded under an atomic key scope can be cancelled.
    """
    by_name = {t.name: t for t in tools}

    def handler(world: World, a: dict, ctx: "InvocationContext") -> dict:
        name, key = a.get("tool"), a.get("key")
        tool = by_name.get(name)
        if tool is None or not key:
            raise InvalidRequest(f"cancel_partial needs a tool (one of {sorted(by_name)}) and the key it used")
        rec = world.get(f"_idem:{name}", key, visible=False)
        if rec is None or "partial_error" not in rec:
            raise BusinessError(f"No request to {name} with that key failed partway; nothing to cancel")
        tool.compensate(world, rec.get("args", {}), key)
        world.delete(f"_idem:{name}", key)
        return {"cancelled": True, "tool": name, "key": key, "undone": rec.get("committed", [])}

    return ToolSpec(
        name="cancel_partial",
        description=("Undo exactly what a request committed before it failed partway, identified by the tool it "
                     "called and the idempotency key it used. Afterwards the same key can be used to send the full "
                     "request again."),
        params={"tool": {"type": "string", "enum": sorted(by_name),
                         "description": "Name of the tool whose request failed partway."},
                "key": {"type": "string", "description": "The idempotency key that request used."}},
        required=["tool", "key"], handler=handler,
        semantics=ActionSemantics(SideEffect.EXTERNAL, idempotent=True, reversible=False, compensable=False,
                                  consequence=Consequence.MEDIUM),
        response_fields=["cancelled"], tags=["contract"])


class ToolRegistry:
    def __init__(self, tools: List[ToolSpec]):
        self._tools = {t.name: t for t in tools}

    def get(self, name: str) -> Optional[ToolSpec]:
        return self._tools.get(name)

    def __iter__(self):
        return iter(self._tools.values())

    def names(self) -> List[str]:
        return list(self._tools)
