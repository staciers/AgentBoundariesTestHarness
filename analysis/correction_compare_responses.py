"""Fingerprint every agent-visible response in every traced episode, for comparing two code versions.

    .venv/bin/python analysis/correction_compare_responses.py OUT.json        (run once per code version)
    python3 analysis/correction_compare_responses.py --compare A.json B.json [report.json]

Saved traces record each result's kind and error flag but not its content, so a replay can't
compare full responses against the original records. Instead, this replays every traced episode
(recorded agent decisions, no model calls) and records, per episode, the full sequence of tool
results the agent receives (content and error flag, serialized). Running it under the code before
and after a change, and comparing the two files, shows whether the change alters anything an agent
would see. Episodes on real services (domain ledger_real) need the live stack and are skipped.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, ".")


def _run(run: str) -> dict:
    from abh import controlplane
    from abh.agents.replay import ReplayAgent
    from abh.episode import run_episode
    from abh.experiment import episode_key, expand
    from abh.metrics import load_episodes

    seen: list = []
    original = controlplane.ControlPlane.handle

    def handle(self, call):
        r = original(self, call)
        seen.append(json.dumps([r.content, r.is_error], sort_keys=True, default=str))
        return r

    controlplane.ControlPlane.handle = handle
    d = os.path.join("runs", run)
    with open(os.path.join(d, "spec.json")) as f:
        cfgs = {episode_key(c): c for c in expand(json.load(f))}
    out = {}
    for e in load_episodes(os.path.join(d, "episodes.jsonl")):
        tpath = os.path.join(d, "traces", f"{e['key']}.json")
        if "error" in e or e.get("domain") == "ledger_real" or not os.path.exists(tpath) or e["key"] not in cfgs:
            continue
        with open(tpath) as f:
            trace = json.load(f)["trace"]
        seen.clear()
        run_episode(cfgs[e["key"]], keep_trace=False, agent=ReplayAgent(trace, label=e["agent"]))
        out[e["key"]] = {"n": len(seen), "sha256": hashlib.sha256("\n".join(seen).encode()).hexdigest()}
    controlplane.ControlPlane.handle = original
    return {"run": run, "episodes": out}


def fingerprint(out_path: str) -> None:
    files = subprocess.run(["git", "ls-files", "runs"], capture_output=True, text=True, check=True).stdout.split()
    runs = sorted({f.split("/")[1] for f in files if f.endswith("spec.json")})
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(_run, runs))
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    with open(out_path, "w") as f:
        json.dump({"code": commit, "runs": res}, f)
    print(f"{sum(len(r['episodes']) for r in res)} episodes, "
          f"{sum(v['n'] for r in res for v in r['episodes'].values())} responses -> {out_path}")


def compare(a_path: str, b_path: str, report: str | None = None) -> None:
    a, b = (json.load(open(p)) for p in (a_path, b_path))
    ea = {(r["run"], k): v for r in a["runs"] for k, v in r["episodes"].items()}
    eb = {(r["run"], k): v for r in b["runs"] for k, v in r["episodes"].items()}
    differ = sorted(k for k in ea.keys() & eb.keys() if ea[k] != eb[k])
    res = {"episodes_compared": len(ea.keys() & eb.keys()),
           "responses_compared": sum(ea[k]["n"] for k in ea.keys() & eb.keys()),
           "only_in_first": len(ea.keys() - eb.keys()), "only_in_second": len(eb.keys() - ea.keys()),
           "differing_episodes": [list(k) for k in differ]}
    print(json.dumps({k: (v if k != "differing_episodes" else len(v)) for k, v in res.items()}))
    if report:
        with open(report, "w") as f:
            json.dump(res, f, indent=2)


if __name__ == "__main__":
    if sys.argv[1] == "--compare":
        compare(*sys.argv[2:])
    else:
        fingerprint(sys.argv[1])
