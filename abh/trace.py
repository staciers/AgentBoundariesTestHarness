"""Structured, append-only episode trace (provenance for analysis and Paper 3)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .world import SimClock


@dataclass
class Event:
    t_ms: int
    kind: str
    actor: str
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"t_ms": self.t_ms, "event": self.kind, "actor": self.actor, **self.data}


class Trace:
    def __init__(self, clock: SimClock):
        self.clock = clock
        self.events: List[Event] = []

    def emit(self, kind: str, actor: str, /, **data) -> Event:
        e = Event(self.clock.now_ms, kind, actor, _jsonable(data))
        self.events.append(e)
        return e

    def of(self, kind: str) -> List[Event]:
        return [e for e in self.events if e.kind == kind]

    def to_list(self) -> List[dict]:
        return [e.to_dict() for e in self.events]


def _jsonable(x: Any) -> Any:
    try:
        json.dumps(x)
        return x
    except TypeError:
        if isinstance(x, dict):
            return {str(k): _jsonable(v) for k, v in x.items()}
        if isinstance(x, (list, tuple, set)):
            return [_jsonable(v) for v in x]
        if hasattr(x, "value"):
            return x.value
        return repr(x)
