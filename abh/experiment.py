"""Factorial experiment runner with resumable JSONL output.

Specs may also split into ``"blocks"`` (sub-grids that override top-level keys); see ``expand``.

Spec (JSON)::

    {
      "name": "pilot",
      "scenarios": ["travel/*", "devops/base"],          # globs over registered ids, or "all"
      "policies": ["P1", {"name": "P3", "threshold": 0.6}, "P6"],
      "agents": [{"type": "scripted", "profile": "careful"}],
      "fault_conditions": "single",                      # none + each fault type alone
      "runtime_overrides": [null],                       # e.g. [null, "semantic"] crosses runtime x policy
      "seeds": 5,                      # int -> range(n), explicit list, or {"start": 100, "count": 30}
      "human": {"latency_median_s": 90},
      "max_turns": 30, "workers": 4, "keep_traces": false
    }

``fault_conditions`` may also be a list whose items are ``"none"``, a fault type
name, a fault spec dict, or a list of specs. A list is a *compound* condition: all its
faults are injected in the same episode, and those that target the same call compose
(e.g. ``["timeout_after_execution", "delayed_visibility"]``). Invalid compounds are
rejected while the spec is expanded, before any episode runs.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Iterator, List, Optional, Tuple

from .agents.base import make_agent
from .domains.base import list_scenarios, make_scenario
from .episode import EpisodeConfig, fault_label, run_episode
from .faults import FaultSpec, FaultType, validate_compound
from .metrics import load_episodes, write_report
from .policies import make_policy


def _scenarios(sel) -> List[str]:
    all_ids = list_scenarios()
    if sel in (None, "all"):
        return all_ids
    out: List[str] = []
    for pat in sel:
        out.extend(s for s in all_ids if fnmatch.fnmatch(s, pat) and s not in out)
    return out


def _conditions(sel) -> List[List[FaultSpec]]:
    if sel in (None, "none"):
        return [[]]
    if sel == "single":
        return [[]] + [[FaultSpec.parse(ft.value)] for ft in FaultType]
    out = []
    for c in sel:
        if c == "none" or c == []:
            out.append([])
        elif isinstance(c, list):
            out.append([FaultSpec.parse(x) for x in c])
        else:
            out.append([FaultSpec.parse(c)])
    return out


def expand(spec: Dict[str, Any]) -> Iterator[EpisodeConfig]:
    """Expand a spec into episode configs.

    A spec may contain ``"blocks"``: a list of partial specs, each overriding the top-level
    keys for its own sub-grid. This lets one run hold, say, a main design plus an ablation
    that only applies to some conditions. Episodes produced by more than one block are
    yielded once.
    """
    if "blocks" in spec:
        base = {k: v for k, v in spec.items() if k != "blocks"}
        seen = set()
        for block in spec["blocks"]:
            for cfg in expand({**base, **{k: v for k, v in block.items() if not k.startswith("_")}}):
                key = episode_key(cfg)
                if key not in seen:
                    seen.add(key)
                    yield cfg
        return
    seeds = spec.get("seeds", 3)
    if isinstance(seeds, dict):  # {"start": 100, "count": 30}
        seeds = list(range(int(seeds.get("start", 0)), int(seeds.get("start", 0)) + int(seeds["count"])))
    seeds = list(range(seeds)) if isinstance(seeds, int) else list(seeds)
    for sid in _scenarios(spec.get("scenarios")):
        sc = make_scenario(sid)
        for cond in _conditions(spec.get("fault_conditions", "single")):
            resolved = [FaultSpec(f.type, sc.resolve_target(f.target, f.type), f.on_call, f.times, f.params)
                        for f in cond]
            if any(f.target is None for f in resolved):
                continue  # scenario lacks a tool for this fault
            try:
                validate_compound(resolved)
            except ValueError as e:  # a spec error, not a per-episode failure: stop before spending
                raise ValueError(f"fault condition {fault_label(cond)} on {sid}: {e}") from None
            for pol in spec.get("policies", ["P1"]):
                for rt in spec.get("runtime_overrides", [None]):
                    for ag in spec.get("agents", ["scripted"]):
                        for seed in seeds:
                            yield EpisodeConfig(scenario=sid, policy=pol, agent=ag, faults=[f.to_dict() for f in cond],
                                                fault_label=fault_label(cond), runtime=rt, human=spec.get("human"),
                                                seed=seed, max_turns=spec.get("max_turns", 30))


def episode_key(c: EpisodeConfig) -> str:
    blob = json.dumps([c.scenario, make_policy(c.policy).label, make_agent(c.agent).label, c.fault_label,
                       c.faults, c.runtime, c.human, c.seed], sort_keys=True, default=str)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def run_experiment(spec: Dict[str, Any], out_root: str = "runs", resume: Optional[str] = None,
                   dry_run: bool = False) -> str:
    out_dir = resume or os.path.join(out_root, f"{spec.get('name', 'exp')}-{time.strftime('%Y%m%d-%H%M%S')}")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "spec.json"), "w") as f:
        json.dump(spec, f, indent=2)
    ep_path = os.path.join(out_dir, "episodes.jsonl")
    done = set()
    if os.path.exists(ep_path):
        done = {e.get("key") for e in load_episodes(ep_path)}

    todo: List[Tuple[str, EpisodeConfig]] = [(episode_key(c), c) for c in expand(spec)]
    todo = [(k, c) for k, c in todo if k not in done]
    print(f"[abh] {len(todo)} episodes to run ({len(done)} already done) -> {out_dir}", file=sys.stderr)
    if dry_run:
        return out_dir

    keep = bool(spec.get("keep_traces", False))
    trace_dir = os.path.join(out_dir, "traces")
    if keep:
        os.makedirs(trace_dir, exist_ok=True)
    lock = threading.Lock()
    t0 = time.time()

    def one(item):
        key, cfg = item
        try:
            res = run_episode(cfg, keep_trace=keep)
        except Exception as e:  # never lose a long run to one bad episode
            res = {"error": f"{type(e).__name__}: {e}", "scenario": cfg.scenario}
        res["key"] = key
        trace, transcript = res.pop("trace", None), res.pop("transcript", None)
        with lock:
            if keep and "error" not in res:
                with open(os.path.join(trace_dir, f"{key}.json"), "w") as f:
                    json.dump({"trace": trace, "transcript": transcript}, f, default=str)
            with open(ep_path, "a") as f:
                f.write(json.dumps(res, default=str) + "\n")
        return res

    workers = int(spec.get("workers", 1))
    n_done = 0
    if workers <= 1:
        for item in todo:
            one(item)
            n_done += 1
            _progress(n_done, len(todo), t0)
    else:
        with ThreadPoolExecutor(workers) as ex:
            for _ in as_completed([ex.submit(one, it) for it in todo]):
                n_done += 1
                _progress(n_done, len(todo), t0)
    print(file=sys.stderr)
    eps = [e for e in load_episodes(ep_path) if "error" not in e]
    errs = sum(1 for e in load_episodes(ep_path) if "error" in e)
    if errs:
        print(f"[abh] WARNING: {errs} episodes raised errors (see episodes.jsonl)", file=sys.stderr)
    write_report(eps, out_dir)
    return out_dir


def _progress(i: int, n: int, t0: float) -> None:
    if n and (i == n or i % max(1, n // 50) == 0):
        el = time.time() - t0
        print(f"\r[abh] {i}/{n} episodes  {el:.0f}s elapsed", end="", file=sys.stderr)
