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
      "max_turns": 30, "workers": 4, "keep_traces": false,
      "keep_world": false              # with keep_traces: also save the final World and effects ledger
    }

Every launch is recorded in ``manifest.json`` (git commit, clean tree, versions) and progress
in ``status.json``; see ``abh.runlog``.

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
from . import runlog


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
            if any(not sc.resolve_targets(f.target, f.type) for f in cond):
                continue  # scenario lacks a tool for this fault
            resolved = [FaultSpec(f.type, tool, f.on_call, f.times, f.params, f.rate)
                        for f in cond for tool in sc.resolve_targets(f.target, f.type)]
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
                                                seed=seed, max_turns=spec.get("max_turns", 30),
                                                principal_replies=int(spec.get("principal_replies", 0)))


def episode_key(c: EpisodeConfig) -> str:
    parts = [c.scenario, make_policy(c.policy).label, make_agent(c.agent).label, c.fault_label,
             c.faults, c.runtime, c.human, c.seed]
    if c.principal_replies:  # only when used, so earlier episode keys are unchanged
        parts.append({"principal_replies": c.principal_replies})
    blob = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def run_experiment(spec: Dict[str, Any], out_root: str = "runs", resume: Optional[str] = None,
                   dry_run: bool = False, rerun_errors: bool = False) -> str:
    """Run (or resume) a spec. ``rerun_errors`` (with ``resume``) first moves errored episodes to
    ``episodes_rerun_originals.jsonl`` so they run again, per the pre-registered exclusion rule."""
    if rerun_errors and not resume:
        raise ValueError("rerun_errors needs resume=<run dir>")
    out_dir = resume or os.path.join(out_root, f"{spec.get('name', 'exp')}-{time.strftime('%Y%m%d-%H%M%S')}")
    ep_path = os.path.join(out_dir, "episodes.jsonl")
    if dry_run:  # count only; write nothing
        done = {e.get("key") for e in load_episodes(ep_path)} if os.path.exists(ep_path) else set()
        n = sum(1 for c in expand(spec) if episode_key(c) not in done)
        print(f"[abh] {n} episodes to run ({len(done)} already done) -> {out_dir}", file=sys.stderr)
        return out_dir
    os.makedirs(out_dir, exist_ok=True)
    set_aside: List[str] = []
    if rerun_errors and os.path.exists(ep_path):
        set_aside = runlog.set_aside_errors(out_dir)
    with open(os.path.join(out_dir, "spec.json"), "w") as f:
        json.dump(spec, f, indent=2)
    existing = load_episodes(ep_path) if os.path.exists(ep_path) else []
    done = {e.get("key") for e in existing}

    all_keys: List[Tuple[str, EpisodeConfig]] = [(episode_key(c), c) for c in expand(spec)]
    todo = [(k, c) for k, c in all_keys if k not in done]
    print(f"[abh] {len(todo)} episodes to run ({len(done)} already done) -> {out_dir}", file=sys.stderr)

    workers = int(spec.get("workers", 1))
    mode = "rerun_errors" if rerun_errors else "resume" if resume else "new"
    launch = runlog.record_launch(out_dir, mode, workers, len(all_keys), len(todo),
                                  **({"rerun_keys": set_aside} if rerun_errors else {}))
    if launch["clean"] is False:
        print(f"[abh] WARNING: code tree not clean ({', '.join(launch['dirty_paths'])}); recorded in manifest.json",
              file=sys.stderr)
    status = runlog.Status(out_dir, len(all_keys), existing, launch)
    status.write("running")

    keep = bool(spec.get("keep_traces", False))
    keep_world = keep and bool(spec.get("keep_world", False))
    trace_dir = os.path.join(out_dir, "traces")
    if keep:
        os.makedirs(trace_dir, exist_ok=True)
    lock = threading.Lock()
    t0 = time.time()

    def one(item):
        key, cfg = item
        try:
            res = run_episode(cfg, keep_trace=keep, keep_world=keep_world)
        except Exception as e:  # never lose a long run to one bad episode
            res = {"error": f"{type(e).__name__}: {e}", "scenario": cfg.scenario}
        res["key"] = key
        payload = {"trace": res.pop("trace", None), "transcript": res.pop("transcript", None)}
        if "world" in res:
            payload["world"] = res.pop("world")
        with lock:
            if keep and "error" not in res:
                runlog.save_trace(trace_dir, key, payload)
            with open(ep_path, "a") as f:
                f.write(json.dumps(res, default=str) + "\n")
            status.add(res)
        return res

    n_done = 0
    try:
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
    except KeyboardInterrupt:
        status.write("interrupted")
        raise
    except BaseException:
        status.write("failed")
        raise
    status.write("finished")
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
