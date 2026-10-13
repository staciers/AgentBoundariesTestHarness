"""Scenario definition: tools + initial world + ground truth + evaluation.

A scenario bundles everything that is *true* about a task, independent of how it is
controlled: the tools and their semantics, the initial world, the principal's hidden
intent and real authority limits (used by the oracle and the simulated human), the
world-state invariants that define success and harm, and the human needs that a
perfect control policy would escalate (ground truth for intervention recall).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from ..authority import Delegation
from ..faults import FaultType, SemanticFaultDef
from ..tools import ToolSpec
from ..world import World


@dataclass
class Invariant:
    name: str
    check: Callable[[World], bool]
    kind: str = "task"  # task = required for success; harm = unintended side effect
    description: str = ""


@dataclass
class HumanNeed:
    """A point where correct completion genuinely requires a human."""

    id: str
    kind: str                               # authority | ambiguity
    description: str
    rule: Optional[str] = None              # authority rule name that triggers it
    tools: Tuple[str, ...] = ()             # approval on these tools resolves ambiguity


@dataclass
class Step:
    """One step of a reference plan, used by the scripted (non-LLM) agent."""

    name: str
    tool: str
    args: Callable[[dict], dict]
    save: Optional[str] = None
    valid: Optional[Callable[[dict, dict], bool]] = None
    # check = (lookup tool, args_fn(memory), found_fn(response, memory) -> bool)
    check: Optional[Tuple[str, Callable[[dict], dict], Callable[[dict, dict], bool]]] = None
    on_reject: Optional[str] = None
    fallback: Optional[List["Step"]] = None
    uses: Tuple[str, ...] = ()


class Oracle:
    """Ground truth used by the simulated human and the oracle policy."""

    def __init__(self, scenario: "Scenario"):
        self.s = scenario

    def action_correct(self, tool: str, args: dict, world: World) -> Tuple[bool, str, dict]:
        if self.s.judge is None:
            return True, "", {}
        return self.s.judge(tool, args, world)

    def approve(self, tool: str, args: dict, world: World) -> Tuple[bool, str, dict]:
        ok, reason, hint = self.action_correct(tool, args, world)
        if not ok:
            return False, reason, hint
        auth = self.s.delegation.check(tool, args, world)
        if not auth.permitted and not self.s.approver_accepts(tool, args, world):
            return False, "This exceeds what I can authorise.", {}
        return True, "Looks right.", {}

    def clarify(self, question: str, world: World) -> Tuple[str, dict]:
        return self.s.clarification or "No further guidance - proceed as instructed.", dict(self.s.hidden)

    def did_execute(self, tool: str, args: dict, context: dict, world: World) -> bool:
        cid = context.get("call_id")
        return any(e.call_id == cid for e in world.effects)

    def needs_human(self, tool: str, args: dict, world: World) -> Tuple[bool, str]:
        auth = self.s.delegation.check(tool, args, world)
        if not auth.permitted:
            return True, "authority"
        ok, _, _ = self.action_correct(tool, args, world)
        if not ok:
            return True, "incorrect_action"
        return False, ""


@dataclass
class Scenario:
    id: str
    domain: str
    variant: str
    title: str
    prompt: str
    tools: List[ToolSpec]
    build_world: Callable[[World], None]
    delegation: Delegation
    invariants: List[Invariant]
    fault_targets: Dict[str, str]
    semantic_faults: Dict[FaultType, SemanticFaultDef] = field(default_factory=dict)
    unsupported_faults: Set[FaultType] = field(default_factory=set)
    human_needs: List[HumanNeed] = field(default_factory=list)
    # judge(tool, args, world) -> (correct?, reason, hint) w.r.t. hidden intent
    judge: Optional[Callable[[str, dict, World], Tuple[bool, str, dict]]] = None
    approver_accepts: Callable[[str, dict, World], bool] = lambda t, a, w: True
    hidden: Dict[str, Any] = field(default_factory=dict)
    guesses: Dict[str, Any] = field(default_factory=dict)
    clarification: str = ""
    plan: List[Step] = field(default_factory=list)
    context_notes: str = ""

    @property
    def oracle(self) -> Oracle:
        return Oracle(self)

    def resolve_target(self, target: str, ft: FaultType) -> Optional[str]:
        if ft in self.unsupported_faults:
            return None
        if target == "@semantic":
            sdef = self.semantic_faults.get(ft)
            return sdef.tool if sdef else None
        if target.startswith("@"):
            return self.fault_targets.get(target[1:])
        return target

    def resolve_targets(self, target: str, ft: FaultType) -> List[str]:
        """Like resolve_target, but @writes / @reads / @any expand to every matching tool."""
        if ft in self.unsupported_faults:
            return []
        groups = {"@writes": lambda t: not t.semantics.read_only, "@reads": lambda t: t.semantics.read_only,
                  "@any": lambda t: True}
        if target in groups:
            tools = [t for t in self.tools if groups[target](t)]
            if ft == FaultType.PARTIAL_MUTATION:
                tools = [t for t in tools if t.semantics.multipart]
            return [t.name for t in tools]
        one = self.resolve_target(target, ft)
        return [one] if one else []

    def supports(self, ft: FaultType) -> bool:
        return self.resolve_target(ft.default_target, ft) is not None

    def system_notes(self) -> str:
        pol = self.delegation.policy_text()
        out = []
        if pol:
            out.append("Organizational policy (actions requiring approval):\n" + pol)
        if self.context_notes:
            out.append(self.context_notes)
        return "\n\n".join(out)


# ------------------------------------------------------------- registry
_REGISTRY: Dict[str, Callable[[], Scenario]] = {}


def register(scenario_id: str):
    def deco(fn: Callable[[], Scenario]):
        _REGISTRY[scenario_id] = fn
        return fn
    return deco


def make_scenario(scenario_id: str) -> Scenario:
    _ensure_loaded()
    return _REGISTRY[scenario_id]()


def list_scenarios(domain: Optional[str] = None) -> List[str]:
    _ensure_loaded()
    return sorted(s for s in _REGISTRY if domain is None or s.split("/")[0] == domain)


def _ensure_loaded():
    from . import travel, commerce, devops, scheduling, platform  # noqa: F401


# --------------------------------------------------------------- helpers
def lookup_by_ref(table: str, ref_field: str = "client_ref",
                  active: Callable[[dict], bool] = lambda r: r.get("status") != "cancelled",
                  render: Optional[Callable[[dict], dict]] = None):
    """Build a reconcile() hook: find a visible record created with this client key."""

    def reconcile(world: World, args: dict, key: str) -> Optional[dict]:
        rows = world.scan(table, visible=True, where=lambda r: r.get(ref_field) == key and active(r))
        if not rows:
            return None
        return render(rows[0]) if render else rows[0]
    return reconcile


def count_active(world: World, table: str, where: Callable[[dict], bool]) -> int:
    return len(world.scan(table, visible=False,
                          where=lambda r: r.get("status") != "cancelled" and where(r)))
