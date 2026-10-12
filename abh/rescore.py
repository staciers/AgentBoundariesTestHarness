"""Re-score a finished run under the current evaluator, without calling any model.

Each episode with a saved trace is replayed (``ReplayAgent``) against a fresh, identical
environment. The replay is accepted only if it reproduces the recorded run: the same
invariant results, duplicates, authority violations, interventions, injected faults and
simulated duration. Accepted episodes get the current evaluator's outcome fields. The
previous outcome is kept under ``pre_rescore``. Anything that doesn't reproduce is left
unchanged and reported.

    python -m abh rescore runs/<dir>
"""
from __future__ import annotations

import json
import os
import shutil
import time
from typing import Dict, List

from .agents.replay import ReplayAgent
from .episode import run_episode
from .experiment import episode_key, expand
from .metrics import load_episodes

# Fields that must match for a replay to count as faithful.
VERIFY = ("invariants", "duplicate_effects", "authority_violations", "interventions", "sim_duration_ms",
          "agent_tool_calls")
# Fields the current evaluator recomputes.
RESCORED = ("outcome", "success", "task_ok", "harm", "end_state_success", "end_state_harm", "self_corrected_harm",
            "harm_invariants_failed", "authority_violations_standing", "authority_violations_transient",
            "authority_violations_never_in_force",
            "transient_duplicate_effects", "duplicate_effects_incl_compensated", "compensated_effects")


def _faults_sig(faults: List[dict]) -> List[tuple]:
    return sorted((f["type"], f["tool"], f["committed"]) for f in faults)


def rescore_run(run_dir: str) -> Dict[str, int]:
    with open(os.path.join(run_dir, "spec.json")) as f:
        spec = json.load(f)
    cfgs = {episode_key(c): c for c in expand(spec)}
    path = os.path.join(run_dir, "episodes.jsonl")
    episodes = load_episodes(path)
    stats = {"rescored": 0, "unchanged_outcome": 0, "changed_outcome": 0, "no_trace": 0, "no_config": 0,
             "mismatch": 0, "errored": 0}
    mismatches = []
    for e in episodes:
        if "error" in e:
            stats["errored"] += 1
            continue
        tpath = os.path.join(run_dir, "traces", f"{e['key']}.json")
        if not os.path.exists(tpath):
            stats["no_trace"] += 1
            continue
        cfg = cfgs.get(e["key"])
        if cfg is None:
            stats["no_config"] += 1
            continue
        with open(tpath) as f:
            trace = json.load(f)["trace"]
        r = run_episode(cfg, keep_trace=False, agent=ReplayAgent(trace, label=e["agent"]))
        diffs = [k for k in VERIFY if r[k] != e[k]]
        if _faults_sig(r["faults_injected"]) != _faults_sig(e["faults_injected"]):
            diffs.append("faults_injected")
        if diffs:
            stats["mismatch"] += 1
            mismatches.append({"key": e["key"], "fields": diffs})
            continue
        before = {k: e.get(k) for k in ("outcome", "success", "harm")}
        e.setdefault("pre_rescore", before)
        e.update({k: r[k] for k in RESCORED})
        e["rescored"] = {"method": "trace_replay", "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        stats["rescored"] += 1
        stats["changed_outcome" if before["outcome"] != r["outcome"] else "unchanged_outcome"] += 1
    if stats["rescored"]:
        backup = os.path.join(run_dir, f"episodes.pre_rescore-{time.strftime('%Y%m%d-%H%M%S')}.jsonl")
        shutil.copyfile(path, backup)
        with open(path, "w") as f:
            for e in episodes:
                f.write(json.dumps(e, default=str) + "\n")
    if mismatches:
        with open(os.path.join(run_dir, "rescore_mismatches.json"), "w") as f:
            json.dump(mismatches, f, indent=2)
    return stats
