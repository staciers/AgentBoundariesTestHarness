"""Principals, delegation and authority checks.

Authority is modelled independently of uncertainty: an agent may know exactly what
to do, and the runtime may be certain it can execute it, yet the action may still
exceed what the principal delegated. These types are intentionally reusable as the
identity/delegation layer of an agent control plane (Paper 2).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Set

from .world import World


@dataclass(frozen=True)
class Principal:
    id: str
    kind: str = "agent"               # agent | human | service
    on_behalf_of: Optional[str] = None
    roles: tuple = ()


@dataclass
class AuthorityRule:
    """An action pattern that exceeds delegated authority unless approved."""

    name: str
    description: str
    applies: Callable[[str, dict, World], bool]
    approver_role: str = "manager"
    # standing(world) -> True if the end state still holds a commitment this rule forbids
    # without approval. Separates a violation that was undone (self-corrected harm) from
    # one that persists (end-state harm). It is consulted only for episodes that recorded
    # an unapproved violation of this rule. None = assume it persists (conservative).
    standing: Optional[Callable[[World], bool]] = None

    def in_force(self, world: World) -> bool:
        """Does the world currently hold what this rule forbids? Unknown or failing checks say yes."""
        if self.standing is None:
            return True
        try:
            return bool(self.standing(world))
        except Exception:
            return True


@dataclass
class AuthorityDecision:
    permitted: bool
    violated: List[str] = field(default_factory=list)
    approver_role: Optional[str] = None
    reasons: List[str] = field(default_factory=list)


@dataclass
class Delegation:
    principal: Principal
    rules: List[AuthorityRule] = field(default_factory=list)
    allowed_tools: Optional[Set[str]] = None  # None = every registered tool

    def check(self, tool: str, args: dict, world: World) -> AuthorityDecision:
        if self.allowed_tools is not None and tool not in self.allowed_tools:
            return AuthorityDecision(False, [f"tool:{tool}"], "admin",
                                     [f"{tool} is not delegated to {self.principal.id}"])
        violated = [r for r in self.rules if r.applies(tool, args, world)]
        if not violated:
            return AuthorityDecision(True)
        return AuthorityDecision(False, [r.name for r in violated], violated[0].approver_role,
                                 [r.description for r in violated])

    def in_force(self, rule_names: List[str], world: World) -> bool:
        """True if any named rule's forbidden commitment currently holds (unknown names: yes)."""
        rules = {r.name: r for r in self.rules}
        return any(rules[n].in_force(world) if n in rules else True for n in rule_names)

    def policy_text(self) -> str:
        return "\n".join(f"- {r.description} (approver: {r.approver_role})" for r in self.rules)
