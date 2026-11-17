"""Re-score a finished run under the current evaluator, without calling any model.

Each episode with a saved trace is replayed (``ReplayAgent``) against a fresh, identical
environment. The replay is accepted only if it reproduces the recorded run: the same
invariant results, duplicates, authority violations, interventions, injected faults and
simulated duration. Accepted episodes get the current evaluator's outcome fields. The
previous outcome is kept under ``pre_rescore``. Anything that doesn't reproduce is left
unchanged and reported.

    python -m abh rescore runs/<dir>
    python -m abh rescore --check runs/<dir>   # replay and report differences; writes nothing
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


def _agent_visible(trace: List[dict]) -> List[tuple]:
    """What the runtime did and what the agent was shown, call by call."""
    sig = []
    for ev in trace:
        if ev.get("event") == "runtime_outcome":
            sig.append(("outcome", ev.get("tool"), ev.get("state"), tuple(ev.get("runtime_actions") or ())))
        elif ev.get("event") == "agent_result":
            sig.append(("result", ev.get("kind"), ev.get("is_error")))
    return sig


def check_run(run_dir: str, skip_domains=("ledger_real",)) -> Dict[str, object]:
    """Replay a run under the current code and report differences, writing nothing.

    For each episode, compares the recorded run with the replay on the faithfulness fields
    (VERIFY), the injected faults, the outcome fields (outcome, success, harm), each runtime outcome
    in the trace (state and actions), and each result's kind and error flag. Traces don't record
    response content, so content can't be compared with the record; to compare it between two code
    versions, see analysis/correction_compare_responses.py. Episodes on real services
    (ledger_real) need the live stack and are counted as skipped.
    """
    with open(os.path.join(run_dir, "spec.json")) as f:
        spec = json.load(f)
    cfgs = {episode_key(c): c for c in expand(spec)}
    episodes = load_episodes(os.path.join(run_dir, "episodes.jsonl"))
    stats = {"episodes": len(episodes), "identical": 0, "changed": 0, "errored": 0, "no_trace": 0,
             "no_config": 0, "skipped_real_services": 0}
    changed = []
    for e in episodes:
        if "error" in e:
            stats["errored"] += 1
            continue
        if e.get("domain") in skip_domains:
            stats["skipped_real_services"] += 1
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
        r = run_episode(cfg, keep_trace=True, agent=ReplayAgent(trace, label=e["agent"]))
        diffs = [k for k in VERIFY + ("outcome", "success", "harm") if r[k] != e[k]]
        if _faults_sig(r["faults_injected"]) != _faults_sig(e["faults_injected"]):
            diffs.append("faults_injected")
        if _agent_visible(r["trace"]) != _agent_visible(trace):
            diffs.append("agent_visible_results")
        if diffs:
            stats["changed"] += 1
            changed.append({"key": e["key"], "fields": diffs,
                            "before": {k: e.get(k) for k in ("outcome", "success", "harm")},
                            "after": {k: r.get(k) for k in ("outcome", "success", "harm")}})
        else:
            stats["identical"] += 1
    return {"run": os.path.basename(run_dir.rstrip("/")), "stats": stats, "changed": changed}


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
