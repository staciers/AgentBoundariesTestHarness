"""Command-line interface.

    python -m abh list                              # scenarios, policies, faults
    python -m abh run experiments/smoke.json        # run an experiment spec
    python -m abh run spec.json --resume runs/x     # continue an interrupted run
    python -m abh report runs/x                     # rebuild report from episodes.jsonl
    python -m abh rescore runs/x                    # replay traces under the current evaluator
    python -m abh definitions                       # regenerate docs/DEFINITIONS.md
    python -m abh episode travel/base --policy P6 --fault timeout_after_execution --agent scripted:naive -v
"""
from __future__ import annotations

import argparse
import json
import sys

from .domains.base import list_scenarios, make_scenario
from .episode import EpisodeConfig, fault_label, run_episode
from .experiment import run_experiment
from .faults import FaultSpec, FaultType
from .metrics import load_episodes, write_report
from .policies import POLICIES


def _agent(s: str):
    if s.startswith("{"):  # full JSON agent spec, e.g. with prices
        return json.loads(s)
    if s.startswith("compat:"):  # compat:<provider>:<model>[:effort]
        parts = s.split(":")
        d = {"type": "compat", "provider": parts[1], "model": parts[2]}
        if len(parts) > 3:
            d["effort"] = parts[3]
        return d
    if s.startswith("scripted"):
        return {"type": "scripted", "profile": s.split(":", 1)[1] if ":" in s else "careful"}
    if s.startswith("anthropic"):
        parts = s.split(":")
        d = {"type": "anthropic"}
        if len(parts) > 1:
            d["model"] = parts[1]
        if len(parts) > 2:
            d["effort"] = parts[2]
        return d
    if s.startswith("openai"):
        parts = s.split(":")
        d = {"type": "openai"}
        if len(parts) > 1:
            d["model"] = parts[1]
        if len(parts) > 2:
            d["effort"] = parts[2]
        return d
    raise SystemExit(f"unknown agent {s!r} (use scripted[:profile], anthropic[:model[:effort]], "
                     "openai[:model[:effort]], compat:<provider>:<model>[:effort], or a JSON spec)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="abh", description="Autonomy Boundary Harness")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    r = sub.add_parser("run")
    r.add_argument("spec")
    r.add_argument("--out", default="runs")
    r.add_argument("--resume")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--rerun-errors", action="store_true",
                   help="with --resume: set errored episodes aside and run them again (exclusion rule)")
    st = sub.add_parser("status", help="progress, errors and cost of a run, from its status.json")
    st.add_argument("run_dir", nargs="+")
    rp = sub.add_parser("report")
    rp.add_argument("run_dir")
    mp = sub.add_parser("models", help="list model IDs an OpenAI-compatible provider serves")
    mp.add_argument("provider")
    hc = sub.add_parser("human-cost", help="empirical human time/cost for a run's escalations (no API calls)")
    hc.add_argument("run_dir")
    hc.add_argument("--draws", type=int, default=200)
    sub.add_parser("human-model-doc", help="regenerate docs/HUMAN_MODEL.md")
    sub.add_parser("definitions", help="regenerate docs/DEFINITIONS.md from abh/definitions.py")
    rs = sub.add_parser("rescore", help="re-score a run's traces under the current evaluator (no model calls)")
    rs.add_argument("run_dir")
    rs.add_argument("--check", action="store_true",
                    help="replay under the current code and report differences; write nothing")
    e = sub.add_parser("episode")
    e.add_argument("scenario")
    e.add_argument("--policy", default="P1", help="P1..P6, ORACLE, or JSON e.g. '{\"name\":\"P3\",\"threshold\":0.6}'")
    e.add_argument("--agent", default="scripted:careful")
    e.add_argument("--fault", action="append", default=[])
    e.add_argument("--runtime", choices=["none", "naive_retry", "semantic"])
    e.add_argument("--seed", type=int, default=0)
    e.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "list":
        print("Scenarios:")
        for s in list_scenarios():
            sc = make_scenario(s)
            sup = [ft.value for ft in FaultType if sc.supports(ft)]
            print(f"  {s:24s} {sc.title}  [{len(sup)}/{len(FaultType)} faults]")
        print("\nPolicies:")
        for name, cls in POLICIES.items():
            print(f"  {name:7s} {cls.description}")
        print("\nFaults:")
        for ft in FaultType:
            print(f"  {ft.value:26s} ({ft.failure_class.value})")
        return 0
    if a.cmd == "run":
        with open(a.spec) as f:
            spec = json.load(f)
        out = run_experiment(spec, a.out, a.resume, a.dry_run, a.rerun_errors)
        print(out)
        return 0
    if a.cmd == "status":
        from .runlog import read_status
        print("\n".join(read_status(d) for d in a.run_dir))
        return 0
    if a.cmd == "report":
        eps = [x for x in load_episodes(f"{a.run_dir}/episodes.jsonl") if "error" not in x]
        print(write_report(eps, a.run_dir))
        return 0
    if a.cmd == "models":
        from .agents.compat_agent import list_models
        print("\n".join(list_models(a.provider)))
        return 0
    if a.cmd == "human-cost":
        from .human_model import analyze, to_markdown
        eps = [x for x in load_episodes(f"{a.run_dir}/episodes.jsonl") if "error" not in x]
        text = ("# Human time and cost (empirical model)\n\nGenerated by `abh human-cost` from the recorded escalations; "
                f"{a.draws} Monte Carlo draws over the parameter ranges in docs/HUMAN_MODEL.md. Cells: central estimate "
                "(5th–95th percentile across draws).\n\n" + to_markdown(analyze(eps, draws=a.draws)))
        with open(f"{a.run_dir}/human_cost.md", "w") as f:
            f.write(text)
        print(text)
        return 0
    if a.cmd == "human-model-doc":
        import os
        from .definitions import DEFINITIONS_PATH
        from .human_model import render_doc
        path = os.path.join(os.path.dirname(DEFINITIONS_PATH), "HUMAN_MODEL.md")
        with open(path, "w") as f:
            f.write(render_doc())
        print(path)
        return 0
    if a.cmd == "definitions":
        from .definitions import write_definitions_md
        print(write_definitions_md())
        return 0
    if a.cmd == "rescore":
        from .rescore import check_run, rescore_run
        if a.check:
            res = check_run(a.run_dir)
            print(json.dumps(res, indent=2))
            return 1 if res["stats"]["changed"] else 0
        stats = rescore_run(a.run_dir)
        print(json.dumps(stats, indent=2))
        eps = [x for x in load_episodes(f"{a.run_dir}/episodes.jsonl") if "error" not in x]
        print(write_report(eps, a.run_dir))
        return 1 if stats["mismatch"] else 0
    if a.cmd == "episode":
        pol = json.loads(a.policy) if a.policy.startswith("{") else a.policy
        faults = [FaultSpec.parse(x) for x in a.fault]
        res = run_episode(EpisodeConfig(a.scenario, pol, _agent(a.agent), [f.to_dict() for f in faults],
                                        fault_label(faults), a.runtime, None, a.seed))
        if a.verbose:
            for ev in res["trace"]:
                print(json.dumps(ev, default=str))
        keys = ["scenario", "policy", "runtime", "agent", "faults", "outcome", "invariants", "authority_violations",
                "duplicate_effects", "interventions", "interventions_necessary", "needs_total", "needs_met",
                "failures_exposed_to_agent", "model_calls", "input_tokens", "output_tokens",
                "cache_read_tokens", "model_cost_usd", "model_latency_ms", "agent_tool_calls", "service_invocations",
                "sim_duration_ms", "faults_injected", "termination", "agent_error", "final_message"]
        print(json.dumps({k: res[k] for k in keys}, indent=2, default=str))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
