"""Deterministic, versioned world state with a simulated clock.

The world keeps two views of every record:

* **truth** - the latest committed version (what actually happened), used by the
  evaluator, the oracle, and service-internal business logic;
* **visible** - what read APIs can currently observe. Writes become visible at
  ``visible_at``; the ``DELAYED_VISIBILITY`` fault pushes that into the future.

Every externally meaningful side effect is also appended to an immutable effects
ledger, which is the ground truth for duplicate detection and harm accounting.
"""
from __future__ import annotations

import copy
import itertools
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


class SimClock:
    def __init__(self, start_ms: int = 0):
        self.now_ms = start_ms

    def advance(self, ms: float) -> None:
        self.now_ms += int(max(0, ms))

    def wait(self, ms: float) -> None:
        """A deliberate wait (runtime backoff, polling for visibility). Simulated: time just advances."""
        self.advance(ms)


class RealClock(SimClock):
    """Wall-clock time, for episodes against real services (``abh.domains.ledger_real``).

    Model and service latency already take real time, so ``advance`` adds nothing; the
    runtime's deliberate waits really sleep, so its polls race real replication lag.
    """

    def __init__(self):
        self.restart()

    def restart(self) -> None:
        """Start timing from now (after the services are set up for the episode)."""
        self._t0 = time.monotonic()

    @property
    def now_ms(self) -> int:
        return int((time.monotonic() - self._t0) * 1000)

    def advance(self, ms: float) -> None:
        pass

    def wait(self, ms: float) -> None:
        time.sleep(max(0.0, ms) / 1000)


@dataclass
class _Version:
    visible_at: int
    value: Optional[dict]  # None = tombstone


@dataclass
class Effect:
    """A ground-truth external side effect (charge, invite, page, deploy...)."""

    seq: int
    t_ms: int
    kind: str
    tool: str
    call_id: str
    dedupe_key: str  # business identity used for duplicate detection
    data: dict = field(default_factory=dict)
    compensated: bool = False
    compensated_seq: Optional[int] = None  # ledger position at which it was undone


class World:
    def __init__(self, clock: Optional[SimClock] = None):
        self.clock = clock or SimClock()
        self._tables: Dict[str, Dict[str, List[_Version]]] = {}
        self.effects: List[Effect] = []
        self._seq = itertools.count(1)
        self._ids = itertools.count(1)
        self._capture: Optional[List[Tuple[str, str]]] = None
        self.current_call_id: str = "-"

    # ------------------------------------------------------------------ ids
    def new_id(self, prefix: str) -> str:
        return f"{prefix}{next(self._ids):04d}"

    # ---------------------------------------------------------------- reads
    def get(self, table: str, key: str, visible: bool = True) -> Optional[dict]:
        versions = self._tables.get(table, {}).get(key)
        if not versions:
            return None
        if not visible:
            v = versions[-1].value
            return copy.deepcopy(v) if v is not None else None
        for ver in reversed(versions):
            if ver.visible_at <= self.clock.now_ms:
                return copy.deepcopy(ver.value) if ver.value is not None else None
        return None

    def scan(self, table: str, visible: bool = True,
             where: Optional[Callable[[dict], bool]] = None) -> List[dict]:
        out = []
        for key in sorted(self._tables.get(table, {})):
            rec = self.get(table, key, visible=visible)
            if rec is not None and (where is None or where(rec)):
                out.append(rec)
        return out

    # --------------------------------------------------------------- writes
    def put(self, table: str, key: str, value: Optional[dict]) -> None:
        self._tables.setdefault(table, {}).setdefault(key, []).append(
            _Version(self.clock.now_ms, copy.deepcopy(value)))
        if self._capture is not None:
            self._capture.append((table, key))

    def update(self, table: str, key: str, **fields) -> dict:
        rec = self.get(table, key, visible=False)
        if rec is None:
            raise KeyError(f"{table}/{key}")
        rec.update(fields)
        self.put(table, key, rec)
        return rec

    def delete(self, table: str, key: str) -> None:
        self.put(table, key, None)

    def record_effect(self, kind: str, tool: str, dedupe_key: str, **data) -> Effect:
        e = Effect(next(self._seq), self.clock.now_ms, kind, tool,
                   self.current_call_id, dedupe_key, data)
        self.effects.append(e)
        return e

    def compensate_effects(self, predicate: Callable[[Effect], bool]) -> None:
        for e in self.effects:
            if predicate(e) and not e.compensated:
                e.compensated = True
                e.compensated_seq = next(self._seq)

    # ------------------------------------------------ fault-injection hooks
    def begin_capture(self) -> None:
        self._capture = []

    def end_capture(self) -> List[Tuple[str, str]]:
        cap, self._capture = self._capture or [], None
        return cap

    def delay_visibility(self, writes: List[Tuple[str, str]], delay_ms: int) -> None:
        for table, key in writes:
            versions = self._tables[table][key]
            versions[-1].visible_at = self.clock.now_ms + delay_ms

    # ------------------------------------------------------------ snapshot
    def truth(self) -> Dict[str, Dict[str, dict]]:
        snap: Dict[str, Dict[str, dict]] = {}
        for t, rows in self._tables.items():
            for k in rows:
                v = self.get(t, k, visible=False)
                if v is not None:
                    snap.setdefault(t, {})[k] = v
        return snap

    def snapshot(self) -> Dict[str, Any]:
        """Final committed state (including hidden tables) and the full effects ledger."""
        from dataclasses import asdict
        return {"sim_time_ms": self.clock.now_ms, "truth": copy.deepcopy(self.truth()),
                "effects": [asdict(e) for e in self.effects]}

    def active_effects(self, kind: Optional[str] = None) -> List[Effect]:
        return [e for e in self.effects
                if not e.compensated and (kind is None or e.kind == kind)]

    def duplicate_effects(self, include_compensated: bool = False) -> int:
        """Number of (active) effects whose business identity was already executed."""
        seen: Dict[Tuple[str, str], int] = {}
        dups = 0
        for e in self.effects:
            if e.compensated and not include_compensated:
                continue
            k = (e.kind, e.dedupe_key)
            if k in seen:
                dups += 1
            seen[k] = seen.get(k, 0) + 1
        return dups

    def transient_duplicate_effects(self) -> int:
        """Duplicates that were live at the same time but undone by the end of the episode.

        A copy undone *before* its replacement executed (compensate-then-retry) never
        coexisted with it, so it doesn't count.
        """
        events: Dict[Tuple[str, str], List[Tuple[int, int]]] = {}
        for e in self.effects:
            k = (e.kind, e.dedupe_key)
            events.setdefault(k, []).append((e.seq, 1))
            if e.compensated_seq is not None:
                events[k].append((e.compensated_seq, -1))
        total = 0
        for evs in events.values():
            live = peak = 0
            for _, d in sorted(evs):
                live += d
                peak = max(peak, live)
            total += max(0, peak - 1) - max(0, live - 1)
        return total

    def compensated_effects(self) -> int:
        return sum(1 for e in self.effects if e.compensated)
