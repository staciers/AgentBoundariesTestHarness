"""Core vocabulary: action semantics, execution states, controllers, failure classes.

These types are the shared language between tools, the reliability runtime, control
policies, the simulated human, and the evaluator. They are deliberately small and
serialisable so that traces can be analysed outside the harness.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum, IntEnum
from typing import Optional


class SideEffect(str, Enum):
    NONE = "none"          # read-only
    INTERNAL = "internal"  # mutates org-internal state (calendar, deploy, ticket)
    EXTERNAL = "external"  # leaves the org boundary (payment, email, vendor order)


class Consequence(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def parse(cls, v) -> "Consequence":
        if isinstance(v, Consequence):
            return v
        if isinstance(v, int):
            return cls(v)
        return cls[str(v).upper()]


class ExecutionState(str, Enum):
    NOT_EXECUTED = "NOT_EXECUTED"
    EXECUTED = "EXECUTED"
    EXECUTION_UNKNOWN = "EXECUTION_UNKNOWN"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    VERIFIED = "VERIFIED"
    SEMANTIC_FAILURE = "SEMANTIC_FAILURE"


class Controller(str, Enum):
    RUNTIME = "runtime"
    AGENT = "agent"
    HUMAN = "human"
    NONE = "none"  # nobody handled it


class FailureClass(str, Enum):
    EXECUTION = "execution"  # what happened? (distributed-systems uncertainty)
    SEMANTIC = "semantic"    # what should be done now? (reasoning / replanning)
    AUTHORITY = "authority"  # is the system permitted to decide?
    EPISTEMIC = "epistemic"  # does the agent know the principal's intent?


@dataclass(frozen=True)
class ActionSemantics:
    """Machine-readable semantics every tool declares (prospectus §4)."""

    side_effect: SideEffect = SideEffect.NONE
    idempotent: bool = True
    reversible: bool = True
    compensable: bool = True
    consequence: Consequence = Consequence.LOW
    authority_requirement: Optional[str] = None  # role whose approval may be required
    supports_idempotency_key: bool = False       # service dedupes on a client-supplied key
    multipart: bool = False                      # can commit partially

    @property
    def read_only(self) -> bool:
        return self.side_effect == SideEffect.NONE

    @property
    def safe_to_blind_retry(self) -> bool:
        return self.read_only or self.idempotent

    def to_dict(self) -> dict:
        d = asdict(self)
        d["side_effect"] = self.side_effect.value
        d["consequence"] = self.consequence.name
        return d


READ_ONLY = ActionSemantics()
