"""Run bookkeeping written by the harness itself, so a run can be audited and watched
without anyone (or any agent session) polling it.

* ``manifest.json`` - one entry per launch of a run directory (first run, resume, re-run of
  errored episodes): git commit and whether the tree was clean, Python and package
  versions, host, worker count, and what the launch was asked to do. This is the record of
  *which code* produced the episodes, so it doesn't rest on procedure alone.
* ``status.json`` - rewritten atomically while the run progresses: counts, errors and cost
  by provider, rate, ETA, last progress time, pid and state (``running`` / ``finished`` /
  ``failed`` / ``interrupted``). ``abh status <run_dir>`` reads it and flags a stale run.
* Superseded traces - when an episode is re-run, its earlier trace is moved to
  ``traces/superseded/`` instead of being overwritten.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import platform
import subprocess
import sys
import time
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional

# Code paths whose state decides what a run computes; the clean-tree check covers these.
CODE_PATHS = ("abh", "analysis", "experiments")
PACKAGES = ("anthropic", "openai", "numpy", "statsmodels", "pandas")
STALE_AFTER_S = 600


def _now_iso(t: Optional[float] = None) -> str:
    return _dt.datetime.fromtimestamp(t if t is not None else time.time()).astimezone().isoformat(timespec="seconds")


def _git(*args: str) -> Optional[str]:
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        out = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def code_version() -> Dict[str, Any]:
    sha = _git("rev-parse", "HEAD")
    dirty = _git("status", "--porcelain", "--", *CODE_PATHS)
    return {"git_commit": sha, "git_short": sha[:7] if sha else None,
            "clean": (dirty == "") if dirty is not None else None,
            "dirty_paths": [ln[3:] for ln in dirty.splitlines()] if dirty else []}


def _versions() -> Dict[str, Optional[str]]:
    from importlib import metadata
    out: Dict[str, Optional[str]] = {"python": platform.python_version()}
    for p in PACKAGES:
        try:
            out[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            out[p] = None
    return out


def record_launch(out_dir: str, mode: str, workers: Any, total: int, todo: int, **extra: Any) -> Dict[str, Any]:
    """Append this launch to manifest.json and return the entry."""
    path = os.path.join(out_dir, "manifest.json")
    manifest = {"launches": []}
    if os.path.exists(path):
        with open(path) as f:
            manifest = json.load(f)
    entry = {"mode": mode, "started_at": _now_iso(), **code_version(), "versions": _versions(),
             "host": platform.node(), "platform": platform.platform(), "pid": os.getpid(),
             "argv": sys.argv, "workers": workers, "episodes_in_spec": total, "episodes_to_run": todo, **extra}
    manifest["launches"].append(entry)
    _atomic_write(path, manifest)
    return entry


def _atomic_write(path: str, obj: Any) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, default=str)
    os.replace(tmp, path)


def provider(e: dict) -> str:
    a = str(e.get("agent") or "")
    return a.split(":")[0] if a else "unknown"


def is_error(e: dict) -> bool:
    """Episodes the pre-registered exclusion rule re-runs: harness errors and non-refusal agent errors."""
    return "error" in e or (bool(e.get("agent_error")) and not str(e["agent_error"]).startswith("refusal"))


class Status:
    """Progress counters for status.json. Not thread-safe; call under the runner's lock."""

    def __init__(self, out_dir: str, total: int, existing: Iterable[dict], launch: Dict[str, Any]):
        self.path = os.path.join(out_dir, "status.json")
        self.total = total
        self.t0 = time.time()
        self.last_progress = self.t0
        self.launch = {k: launch[k] for k in ("mode", "started_at", "git_short", "clean", "pid", "workers")}
        self.this_launch = 0
        self.by: Dict[str, Dict[str, float]] = defaultdict(lambda: {"episodes": 0, "errors": 0, "cost_usd": 0.0})
        self.done = 0
        for e in existing:
            self._count(e)
        self.done_at_start = self.done
        self._last_write = 0.0

    def _count(self, e: dict) -> None:
        b = self.by[provider(e)]
        b["episodes"] += 1
        b["errors"] += int(is_error(e))
        b["cost_usd"] += float(e.get("model_cost_usd") or 0.0)
        self.done += 1

    def add(self, e: dict) -> None:
        self._count(e)
        self.this_launch += 1
        self.last_progress = time.time()
        if self.last_progress - self._last_write >= 30 or self.this_launch % max(1, self.total // 200) == 0:
            self.write("running")

    def write(self, state: str) -> None:
        now = time.time()
        el = now - self.t0
        rate = self.this_launch / el if el > 0 else 0.0
        remaining = max(0, self.total - self.done)
        _atomic_write(self.path, {
            "state": state, "updated_at": _now_iso(now), "last_progress_at": _now_iso(self.last_progress),
            "done": self.done, "total": self.total, "remaining": remaining,
            "errors": sum(int(b["errors"]) for b in self.by.values()),
            "cost_usd": round(sum(b["cost_usd"] for b in self.by.values()), 4),
            "this_launch": {**self.launch, "episodes_done": self.this_launch, "elapsed_s": round(el),
                            "episodes_per_hour": round(rate * 3600, 1),
                            "eta_s": round(remaining / rate) if rate > 0 and state == "running" else None},
            "by_provider": {p: {"episodes": int(b["episodes"]), "errors": int(b["errors"]),
                                "cost_usd": round(b["cost_usd"], 4)} for p, b in sorted(self.by.items())},
        })
        self._last_write = now


def save_trace(trace_dir: str, key: str, payload: dict) -> None:
    """Write a trace; an existing one for the same key (an earlier attempt) is kept under superseded/."""
    path = os.path.join(trace_dir, f"{key}.json")
    if os.path.exists(path):
        old = os.path.join(trace_dir, "superseded")
        os.makedirs(old, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(os.path.getmtime(path)))
        os.replace(path, os.path.join(old, f"{key}.{stamp}.json"))
    with open(path, "w") as f:
        json.dump(payload, f, default=str)


def set_aside_errors(out_dir: str) -> List[str]:
    """Move errored episodes (per ``is_error``) to episodes_rerun_originals.jsonl so a resume re-runs them."""
    ep = os.path.join(out_dir, "episodes.jsonl")
    keep, bad = [], []
    with open(ep) as f:
        for line in f:
            if line.strip():
                (bad if is_error(json.loads(line)) else keep).append(line)
    if bad:
        with open(os.path.join(out_dir, "episodes_rerun_originals.jsonl"), "a") as f:
            f.writelines(bad)
        tmp = ep + ".tmp"
        with open(tmp, "w") as f:
            f.writelines(keep)
        os.replace(tmp, ep)
    return [json.loads(b).get("key") for b in bad]


def read_status(run_dir: str) -> str:
    """Human-readable summary of status.json, flagging a run that has stopped making progress."""
    path = os.path.join(run_dir, "status.json")
    if not os.path.exists(path):
        return f"{run_dir}: no status.json (run predates status tracking, or hasn't started)"
    with open(path) as f:
        s = json.load(f)
    lines = [f"{run_dir}: {s['state']}, {s['done']}/{s['total']} episodes, {s['errors']} errors, "
             f"${s['cost_usd']:.2f}"]
    tl = s["this_launch"]
    if s["state"] == "running":
        alive = _pid_alive(tl.get("pid"))
        age = time.time() - _dt.datetime.fromisoformat(s["last_progress_at"]).timestamp()
        eta = f", ETA {tl['eta_s'] / 3600:.1f} h" if tl.get("eta_s") else ""
        lines.append(f"  {tl['episodes_per_hour']:.0f} episodes/h{eta}; last progress {age / 60:.0f} min ago")
        if not alive:
            lines.append("  WARNING: the run's process is gone; resume with `abh run <spec> --resume <dir>`")
        elif age > STALE_AFTER_S:
            lines.append(f"  WARNING: no progress for {age / 60:.0f} min (stalled? system sleep?)")
    lines.append(f"  code {tl.get('git_short')} ({'clean' if tl.get('clean') else 'NOT clean'}), "
                 f"launch mode {tl.get('mode')}, {tl.get('workers')} workers")
    for p, b in s["by_provider"].items():
        lines.append(f"  {p:10s} {b['episodes']:6d} episodes  {b['errors']:3d} errors  ${b['cost_usd']:.2f}")
    return "\n".join(lines)


def _pid_alive(pid: Optional[int]) -> bool:
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    return True
