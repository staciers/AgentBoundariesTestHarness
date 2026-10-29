"""Measure what the runtime adds per episode on the real ledger (Q6 cost model). No model calls.

    services/ledger/stack.sh up
    .venv/bin/python analysis/overhead_bench.py [seeds] [out]   (defaults: 20, docs/cost/bench.json)

The same scripted agent (``naive``: no checks of its own, no recovery logic) runs each fault
condition with no runtime (``P1[expose_keys=false]``), with it (P6), and with it plus the
partial-effects fast path (``inspect_partial``), so differences are the runtime's own work. Every HTTP request the harness makes to the ledger service is counted per
episode and attributed either to the agent's tool calls (including the runtime's retries of
them) or to the runtime's own hooks (reconcile lookups, postcondition reads, compensation, inspection).
Payment-call latency and the runtime's deliberate waits come from the episode traces.
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")
from abh.domains import ledger_real  # noqa: E402
from abh.episode import EpisodeConfig, run_episode  # noqa: E402
from abh.faults import FaultSpec  # noqa: E402
from abh.runtime import RuntimeConfig  # noqa: E402
from abh.world import RealClock, World  # noqa: E402

CONDITIONS = {"none": [], "hidden write": ["timeout_after_execution", "delayed_visibility"],
              "partial commit": ["partial_mutation", "timeout_after_execution"]}
P6 = {"name": "P6", "threshold": 0.7}
POLICIES = {"no runtime": ({"name": "P1", "expose_keys": False}, None), "runtime (P6)": (P6, None),
            "runtime (P6) + fast path": (P6, {"mode": "semantic", "inspect_partial": True})}
PAYMENTS = ("send_wire", "send_ach")

_counts = defaultdict(lambda: {"agent": 0, "runtime": 0})
_lock = threading.Lock()
_thread = threading.local()  # .db: this thread's episode database; .in_hook: inside a runtime hook


def _instrument() -> None:
    call, make, create = ledger_real._call, ledger_real._remote_tools, ledger_real._create_db

    def counted(w, *a, **k):
        with _lock:
            _counts[w.real_db]["runtime" if getattr(_thread, "in_hook", False) else "agent"] += 1
        return call(w, *a, **k)

    def hooked(fn):
        def wrapper(*a, **k):
            _thread.in_hook = True
            try:
                return fn(*a, **k)
            finally:
                _thread.in_hook = False
        return wrapper

    def remote_tools():
        tools = make()
        for t in tools:
            for h in ("reconcile", "postcondition", "compensate", "inspect"):
                if getattr(t, h):
                    setattr(t, h, hooked(getattr(t, h)))
        return tools

    def create_db(w):
        create(w)
        _thread.db = w.real_db

    ledger_real._call, ledger_real._remote_tools, ledger_real._create_db = counted, remote_tools, create_db


def run(cond: str, pol: str, seed: int) -> dict:
    fs = [FaultSpec.parse(f).to_dict() for f in CONDITIONS[cond]]
    policy, runtime = POLICIES[pol]
    r = run_episode(EpisodeConfig("ledger_real/base", policy, {"type": "scripted", "profile": "naive"}, fs,
                                  "+".join(CONDITIONS[cond]) or "none", runtime, None, seed), keep_trace=True)
    pay_ms, waits, starts = [], 0, {}
    for ev in r["trace"]:
        if ev["event"] == "agent_call":
            starts[ev.get("call_id")] = ev["t_ms"]
        elif ev["event"] == "runtime_outcome" and ev.get("tool") in PAYMENTS:
            if ev.get("call_id") in starts:
                pay_ms.append(ev["t_ms"] - starts[ev["call_id"]])
            acts = ev.get("runtime_actions") or []
            # Each postcondition miss and each unsuccessful reconcile lookup is followed by one wait.
            waits += acts.count("await_visibility")
            waits += max(0, acts.count("reconcile_lookup") - ("reconciled_executed" in acts))
    return {"condition": cond, "policy": pol, "seed": seed, "outcome": r["outcome"], "harm": r["harm"],
            "requests": dict(_counts[_thread.db]), "pay_call_ms": pay_ms, "waits": waits,
            "duration_ms": r["sim_duration_ms"]}


def measure_request_ms(n: int = 200) -> dict:
    """A plain read through the proxy and service to the fast replica, timed at the client."""
    sc = ledger_real._build("base", 0)
    w = World(RealClock())
    sc.build_world(w)
    try:
        xs = []
        for _ in range(n):
            t0 = time.perf_counter()
            ledger_real._call(w, "GET", "/invoices", params={"vendor": ""})
            xs.append((time.perf_counter() - t0) * 1000)
        xs.sort()
        return {"median": round(xs[n // 2], 2), "p90": round(xs[int(n * 0.9)], 2)}
    finally:
        ledger_real._drop_db(w)


def main(seeds: str = "20", out: str = "docs/cost/bench.json") -> None:
    _instrument()
    jobs = [(c, p, s) for c in CONDITIONS for p in POLICIES for s in range(700, 700 + int(seeds))]
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda j: run(*j), jobs))
    med = lambda xs: statistics.median(xs) if xs else None
    groups = defaultdict(list)
    for r in results:
        groups[(r["condition"], r["policy"])].append(r)
    summary = [{"condition": c, "policy": p, "episodes": len(rs), "harm": sum(r["harm"] for r in rs),
                "agent_requests": med([r["requests"]["agent"] for r in rs]),
                "runtime_requests": med([r["requests"]["runtime"] for r in rs]),
                "waits": med([r["waits"] for r in rs]),
                "first_payment_call_ms": med([r["pay_call_ms"][0] for r in rs if r["pay_call_ms"]]),
                "episode_ms": med([r["duration_ms"] for r in rs])}
               for (c, p), rs in groups.items()]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"seeds": int(seeds), "agent": "scripted:naive", "local_request_ms": measure_request_ms(),
                   "wait_ms": RuntimeConfig().reconcile_wait_ms, "summary": summary, "episodes": results}, f,
                  indent=1)
    for s in summary:
        print(s)


if __name__ == "__main__":
    main(*sys.argv[1:])
