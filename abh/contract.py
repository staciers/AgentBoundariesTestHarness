"""Agent execution contracts: what a tool guarantees about executing a request.

A tool's JSON Schema says what arguments it takes; its description says, in prose, what it
does. Neither says precisely what happens when a request fails partway, times out, or is
retried. That is what an agent (or a runtime) needs to know to recover safely, and the
evidence of the confirmation run (C3/C5) is that agents fill the gap with the broadest
reading of whatever the prose promises.

An ``ExecutionContract`` declares it:

* **key_scope** - what a client-supplied idempotency key covers:
  ``none`` (no key support), ``completed`` (the key is recorded only when a request completes:
  a request that commits partly and then fails is *not* covered, so a retry with the same key
  runs again), or ``atomic`` (the key is recorded together with any committed part, so a retry
  with the same key returns the original outcome, partial or not, and never re-executes).
* **partial_effects** - whether a request can commit only part of its work and, if so, what
  happens to that part: ``impossible`` (single-step), ``persist`` (it stays until compensated).
* **visibility_lag_ms** - how long a committed write may stay invisible to reads (0 =
  read-your-writes; None = no bound promised).
* **reconcile / postcondition / compensation** - whether the tool offers a lookup by key, a
  checkable postcondition, and an undo for an incomplete attempt.
* **inspect** - whether the tool offers a consistent lookup of how far a keyed attempt got
  (``complete``, ``partial`` or ``absent``), answered from current state once any in-flight
  attempt with that key has finished. With it, a runtime can resolve a timeout at once instead
  of polling visible state (``RuntimeConfig.inspect_partial``).
* **partial_report** - whether a partial failure reports, in machine-readable form, what
  committed before the failure (with an atomic scope, the replayed outcome carries it too).
* **repair** - what the contract offers for repairing a partial outcome: ``none``; ``prose``
  (the description explains how to repair, with no new operation); or ``cancel_partial`` (a
  ``cancel_partial(tool, key)`` operation undoes exactly what that key committed,
  after which the full request can be sent again with the same key). ``cancel_partial`` needs
  an atomic key scope and a compensation hook.

The runtime reads contracts to decide what is safe (``abh.runtime``); services enforce
``key_scope`` (``abh.tools.ToolSpec.execute``); tool descriptions can be generated from them
(``describe_key``). ``mcp_annotations`` shows how much survives translation to MCP's tool
annotations, which have no way to say any of the above except "idempotent".

By default every tool's contract is derived from its ``ActionSemantics`` and hooks, and
matches how the services behaved in all studies so far (key scope ``completed``). An episode
can override fields for all tools (``EpisodeConfig.contract``), which is how the contract
study varies key scope.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
from typing import Any, Dict, Optional

from .semantics import Consequence, SideEffect


class KeyScope(str, Enum):
    NONE = "none"
    COMPLETED = "completed"
    ATOMIC = "atomic"


class PartialEffects(str, Enum):
    IMPOSSIBLE = "impossible"
    PERSIST = "persist"


class Repair(str, Enum):
    NONE = "none"
    PROSE = "prose"
    CANCEL_PARTIAL = "cancel_partial"


@dataclass(frozen=True)
class ExecutionContract:
    tool: str
    side_effect: SideEffect
    consequence: Consequence
    reversible: bool
    idempotent: bool                       # repeating the request has no further effect, key or not
    key_scope: KeyScope
    partial_effects: PartialEffects
    visibility_lag_ms: Optional[int]       # None = no bound promised
    reconcile: bool                        # lookup by key: "did this request execute?"
    postcondition: bool                    # a checkable condition on visible state after success
    compensation: bool                     # undo of an incomplete attempt, by key
    partial_report: bool = False           # partial failures report what committed (structured)
    repair: Repair = Repair.NONE           # repair offered for a partial outcome
    inspect: bool = False                  # consistent lookup of a keyed attempt's progress

    @property
    def read_only(self) -> bool:
        return self.side_effect == SideEffect.NONE

    @property
    def keyed(self) -> bool:
        return self.key_scope is not KeyScope.NONE

    @property
    def retry_may_duplicate_partial(self) -> bool:
        """A keyed retry after a hidden partial commit can repeat the committed part."""
        return (self.key_scope is KeyScope.COMPLETED and self.partial_effects is PartialEffects.PERSIST
                and not self.idempotent)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.update(side_effect=self.side_effect.value, consequence=self.consequence.name,
                 key_scope=self.key_scope.value, partial_effects=self.partial_effects.value,
                 repair=self.repair.value)
        return d


OVERRIDABLE = {"key_scope": KeyScope, "partial_effects": PartialEffects, "visibility_lag_ms": None,
               "partial_report": bool, "repair": Repair}


def contract_of(tool, overrides: Optional[Dict[str, Any]] = None) -> ExecutionContract:
    """Derive a tool's contract from its semantics and hooks, then apply episode overrides.

    Overrides apply only where they make sense: key scope only to tools that support keys,
    partial-effects behaviour only to tools that can commit partly.
    """
    sem = tool.semantics
    c = ExecutionContract(
        tool=tool.name, side_effect=sem.side_effect, consequence=sem.consequence, reversible=sem.reversible,
        idempotent=sem.idempotent,
        key_scope=KeyScope.COMPLETED if sem.supports_idempotency_key else KeyScope.NONE,
        partial_effects=PartialEffects.PERSIST if sem.multipart else PartialEffects.IMPOSSIBLE,
        visibility_lag_ms=None if not sem.read_only else 0,
        reconcile=tool.reconcile is not None, postcondition=tool.postcondition is not None,
        compensation=tool.compensate is not None and sem.compensable,
        inspect=getattr(tool, "inspect", None) is not None)
    for k, v in (overrides or {}).items():
        if k not in OVERRIDABLE:
            raise ValueError(f"contract field {k!r} can't be overridden; allowed: {sorted(OVERRIDABLE)}")
        enum = OVERRIDABLE[k]
        v = enum(v) if enum else v
        if k == "key_scope" and not c.keyed:
            continue
        if k == "partial_effects" and c.partial_effects is PartialEffects.IMPOSSIBLE:
            continue
        if k in ("partial_report", "repair") and not (c.keyed and c.partial_effects is PartialEffects.PERSIST):
            continue  # only tools that take a key and can commit partly
        c = replace(c, **{k: v})
    if c.repair is Repair.CANCEL_PARTIAL and not (c.key_scope is KeyScope.ATOMIC and c.compensation):
        raise ValueError(f"{c.tool}: repair=cancel_partial needs key_scope=atomic and a compensation hook")
    return c


def override_label(overrides: Optional[Dict[str, Any]]) -> str:
    return ",".join(f"{k}={v}" for k, v in sorted((overrides or {}).items())) or "default"


class Contracts:
    """Per-episode contract table (tool name -> contract), with the episode's overrides."""

    def __init__(self, overrides: Optional[Dict[str, Any]] = None):
        self.overrides = dict(overrides or {})
        for k in self.overrides:
            if k not in OVERRIDABLE:
                raise ValueError(f"contract field {k!r} can't be overridden; allowed: {sorted(OVERRIDABLE)}")
        self._cache: Dict[str, ExecutionContract] = {}

    def of(self, tool) -> ExecutionContract:
        c = self._cache.get(tool.name)
        if c is None:
            c = self._cache[tool.name] = contract_of(tool, self.overrides)
        return c


def describe_key(c: ExecutionContract) -> Optional[str]:
    """The idempotency_key description generated from the contract (None: the tool takes no key).

    It states exactly what the key covers, including the partial-commit case, instead of a
    blanket promise. Used when a policy sets ``key_description="contract"``.
    """
    if c.key_scope is KeyScope.NONE:
        return None
    base = "Optional client-supplied key."
    if c.key_scope is KeyScope.ATOMIC:
        if c.partial_effects is PartialEffects.PERSIST:
            text = (f"{base} A request repeated with the same key is never executed again: the service returns the "
                    "original outcome, including when the original failed partway (the retry then reports what "
                    "committed).")
            if c.repair is Repair.CANCEL_PARTIAL:
                return (f"{text} If the request failed partway, repair it this way: call cancel_partial with this "
                        "tool's name and the same key, which undoes exactly the part that committed; then send the "
                        "full request again with the same key. Never resend it with a new key, which would repeat "
                        "the committed part.")
            if c.repair is Repair.PROSE:
                return (f"{text} If the service reports that the original request failed partway, part of it has "
                        "taken effect. Don't send the whole request again, with this key or a new one: first check "
                        "what was committed, then either cancel that part and send the full request again, or "
                        "complete only the missing part if the task allows separate requests.")
            return f"{text} Reuse the key when retrying the same request."
        return (f"{base} A request repeated with the same key is never executed again: the service returns the "
                "original outcome. Reuse the key when retrying the same request.")
    if c.partial_effects is PartialEffects.PERSIST:
        return (f"{base} The key is recorded only when a request completes. A request that failed partway is not "
                "recorded: part of it may have taken effect, and repeating it with the same key runs it again. "
                "After a failure or timeout, check current state before retrying.")
    return (f"{base} The key is recorded when a request completes; a repeated request with the same key is not "
            "executed again.")


def mcp_annotations(c: ExecutionContract) -> Dict[str, Any]:
    """What survives translating the contract to MCP tool annotations (hints, not guarantees).

    MCP annotations are readOnlyHint, destructiveHint, idempotentHint and openWorldHint. None of
    key scope, partial-commit behaviour, visibility, reconciliation or compensation can be
    expressed; they are listed under ``lost``.
    """
    return {
        "annotations": {"readOnlyHint": c.read_only,
                        "destructiveHint": (not c.read_only) and not c.reversible,
                        "idempotentHint": c.idempotent,
                        "openWorldHint": c.side_effect == SideEffect.EXTERNAL},
        "lost": [k for k, keep in (("key_scope", not c.keyed), ("partial_effects",
                                                             c.partial_effects is PartialEffects.IMPOSSIBLE),
                                   ("visibility_lag_ms", c.visibility_lag_ms == 0), ("reconcile", not c.reconcile),
                                   ("postcondition", not c.postcondition), ("compensation", not c.compensation),
                                   ("partial_report", not c.partial_report),
                                   ("repair", c.repair is Repair.NONE))
                 if not keep],
    }
