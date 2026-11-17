"""Re-run the committed scripted-agent runs under the current code and compare with the records.

    .venv/bin/python analysis/correction_rerun_scripted.py [out_dir]     (default docs/corrections)

The scripted runs kept no traces, so they can't be replayed; but scripted agents are
deterministic and make no model calls, so each episode can be run again from its config and
compared with the original record. Writes nothing to runs/.
"""
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, ".")
from abh.episode import run_episode  # noqa: E402
from abh.experiment import episode_key, expand  # noqa: E402
from abh.metrics import load_episodes  # noqa: E402

RUNS = ["pilot-scripted-20261012-075322", "rate-sweep-scripted-20261013-105331", "runtime-factorial-20261012-075353"]
COMPARE = ("outcome", "success", "harm", "invariants", "duplicate_effects", "authority_violations", "interventions",
           "sim_duration_ms", "agent_tool_calls")


def _one(args):
    cfg, rec = args
    r = run_episode(cfg, keep_trace=False)
    diffs = [k for k in COMPARE if r.get(k) != rec.get(k)]
    return (rec["key"], diffs, {k: rec.get(k) for k in ("outcome", "harm")}, {k: r.get(k) for k in ("outcome", "harm")})


def check(run: str) -> dict:
    d = os.path.join("runs", run)
    with open(os.path.join(d, "spec.json")) as f:
        cfgs = {episode_key(c): c for c in expand(json.load(f))}
    recs = [e for e in load_episodes(os.path.join(d, "episodes.jsonl")) if "error" not in e]
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(_one, [(cfgs[e["key"]], e) for e in recs if e["key"] in cfgs], chunksize=200))
    changed = [{"key": k, "fields": f, "before": b, "after": a} for k, f, b, a in res if f]
    return {"run": run, "episodes": len(recs), "rerun": len(res), "identical": len(res) - len(changed),
            "changed": changed}


def main(out_dir: str = "docs/corrections") -> None:
    results = [check(r) for r in RUNS]
    with open(os.path.join(out_dir, "rerun-scripted-2026-11.json"), "w") as f:
        json.dump(results, f, indent=2)
    for r in results:
        print(f"{r['run']}: {r['rerun']} re-run, {r['identical']} identical, {len(r['changed'])} changed")


if __name__ == "__main__":
    main(*sys.argv[1:])
