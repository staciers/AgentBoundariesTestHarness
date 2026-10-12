"""Aggregate episode results into the prospectus metrics (§8) and write reports.

Metric definitions and report caveats live in ``abh/definitions.py`` (rendered to
``docs/DEFINITIONS.md``). Report column headers link there, and applicable caveats become
footnotes.
"""
from __future__ import annotations

import csv
import json
import math
import os
from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

from .definitions import DEFINITIONS_PATH, defs_href, note, render_note, term


def load_episodes(path: str) -> List[dict]:
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def _mean_field(eps: Sequence[dict], key: str) -> float:
    """Mean over episodes that have the field (older runs predate some fields)."""
    return _mean([float(e[key]) for e in eps if key in e])


def summarize(eps: List[dict]) -> Dict[str, Any]:
    n = len(eps)
    succ = sum(e["success"] for e in eps)
    auto = [e for e in eps if e["autonomous"]]
    esc = sum(e["interventions"] for e in eps)
    nec = sum(e["interventions_necessary"] for e in eps)
    needs = sum(e["needs_total"] for e in eps)
    met = sum(e["needs_met"] for e in eps)
    lo, hi = wilson(succ, n)
    return {
        "n": n,
        "success": succ / n if n else float("nan"), "success_ci_lo": lo, "success_ci_hi": hi,
        "harm": _mean([e["harm"] for e in eps]),
        "end_state_success": _mean_field(eps, "end_state_success"),
        "end_state_harm": _mean_field(eps, "end_state_harm"),
        "self_corrected_harm": _mean_field(eps, "self_corrected_harm"),
        "transient_duplicates": _mean_field(eps, "transient_duplicate_effects"),
        "fail_safe": _mean([e["outcome"] == "fail_safe" for e in eps]),
        "autonomy_rate": len(auto) / n if n else float("nan"),
        "autonomous_coverage": _mean([e["autonomous_success"] for e in eps]),
        "autonomous_risk": _mean([not e["success"] for e in auto]),
        "autonomous_harm_risk": _mean([e["harm"] for e in auto]),
        "interventions_per_task": esc / n if n else float("nan"),
        "intervention_precision": nec / esc if esc else float("nan"),
        "intervention_recall": met / needs if needs else float("nan"),
        "duplicate_effects": _mean([e["duplicate_effects"] for e in eps]),
        "authority_violations": _mean([e["authority_violations"] for e in eps]),
        "human_errors": _mean([e["human_errors"] for e in eps]),
        "model_calls": _mean([e["model_calls"] for e in eps]),
        "tokens": _mean([e["input_tokens"] + e["output_tokens"] for e in eps]),
        "agent_tool_calls": _mean([e["agent_tool_calls"] for e in eps]),
        "service_invocations": _mean([e["service_invocations"] for e in eps]),
        "runtime_retries": _mean([e["runtime_retries"] for e in eps]),
        "failures_exposed": _mean([e["failures_exposed_to_agent"] for e in eps]),
        "sim_minutes": _mean([e["sim_duration_ms"] / 60000 for e in eps]),
        "human_wait_minutes": _mean([e["human_wait_ms"] / 60000 for e in eps]),
        "model_cost_usd": _mean([e["model_cost_usd"] for e in eps]),
        "human_cost_usd": _mean([e["human_cost_usd"] for e in eps]),
    }


def group(eps: Iterable[dict], keys: Sequence[str]) -> Dict[tuple, List[dict]]:
    g: Dict[tuple, List[dict]] = defaultdict(list)
    for e in eps:
        g[tuple(e[k] for k in keys)].append(e)
    return dict(sorted(g.items(), key=lambda kv: tuple(str(x) for x in kv[0])))


def table(eps: List[dict], keys: Sequence[str], cols: Optional[Sequence[str]] = None) -> List[dict]:
    rows = []
    for k, grp in group(eps, keys).items():
        row = dict(zip(keys, k))
        s = summarize(grp)
        row.update({c: s[c] for c in (cols or s)})
        rows.append(row)
    return rows


def failure_ownership(eps: List[dict]) -> List[dict]:
    """RQ1: for each fault type x policy, who handled the fault and how did it end?"""
    acc: Dict[tuple, Dict[str, Any]] = defaultdict(lambda: defaultdict(int))
    for e in eps:
        for f in e["faults_injected"]:
            a = acc[(f["type"], e["policy"], e["agent"])]
            a["n"] += 1
            a["by_" + f["resolved_by"]] += 1
            a["success"] += int(e["success"])
            a["harm"] += int(e["harm"])
    rows = []
    for (ft, pol, agent), a in sorted(acc.items()):
        n = a["n"]
        rows.append({"fault": ft, "policy": pol, "agent": agent, "n": n,
                     "resolved_by_runtime": a["by_runtime"] / n, "resolved_by_agent": a["by_agent"] / n,
                     "resolved_by_human": a["by_human"] / n, "success": a["success"] / n, "harm": a["harm"] / n})
    return rows


def risk_coverage(eps: List[dict]) -> List[dict]:
    """One point per (policy label, agent). Threshold sweeps of P3/P6 trace a curve."""
    rows = []
    for (pol, name, agent), grp in group(eps, ["policy", "policy_name", "agent"]).items():
        s = summarize(grp)
        rows.append({"policy": pol, "policy_name": name, "agent": agent, "n": s["n"],
                     "autonomous_coverage": s["autonomous_coverage"], "autonomous_risk": s["autonomous_risk"],
                     "harm": s["harm"], "success": s["success"], "interventions_per_task": s["interventions_per_task"]})
    return rows


# ------------------------------------------------------------------ output
def _fmt(v: Any) -> str:
    if isinstance(v, float):
        return "—" if math.isnan(v) else f"{v:.3f}"
    return str(v)


def to_markdown(rows: List[dict], cols: Optional[Sequence[str]] = None,
                href: Optional[Callable[[str], str]] = None) -> str:
    """Markdown table. With ``href``, each header links to its definition (unknown columns raise)."""
    if not rows:
        return "_no data_\n"
    cols = list(cols or rows[0].keys())
    if href is not None:
        heads = [f"[{c}]({href(term(c).key)})" for c in cols]
    else:
        heads = cols
    out = ["| " + " | ".join(heads) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(_fmt(r.get(c)) for c in cols) + " |")
    return "\n".join(out) + "\n"


def to_csv(rows: List[dict], path: str) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


HEADLINE = ["n", "success", "end_state_success", "harm", "end_state_harm", "self_corrected_harm", "fail_safe", "autonomous_coverage", "autonomous_risk", "interventions_per_task",
            "intervention_precision", "intervention_recall", "duplicate_effects", "authority_violations",
            "failures_exposed", "model_calls", "tokens", "human_wait_minutes"]


# Report sections and the notes (footnotes) that qualify each one.
SECTION_NOTES = {
    "top": ["scripted_not_evidence", "run_notes", "errored", "rescored"],
    "headline": ["harm_split", "unsplit", "coverage_ceiling", "gate_reliance", "small_samples", "synthetic_tokens",
                 "never_in_force", "standing_edge", "expose_keys", "refusals", "costs"],
    "runtime": ["synthetic_tokens", "expose_keys"],
    "risk_coverage": ["coverage_ceiling", "small_samples"],
    "variant": ["ground_truth_oversight", "coverage_ceiling"],
    "fault": ["compound_faults", "harm_split", "unsplit", "small_samples"],
    "ownership": ["ownership_heuristic", "compound_faults"],
}


def report_context(eps: List[dict], out_dir: str, groups: Sequence[List[dict]] = ()) -> Dict[str, Any]:
    """Facts about a set of episodes that decide which notes apply."""
    ep_path = os.path.join(out_dir, "episodes.jsonl")
    errored = sum(1 for e in load_episodes(ep_path) if "error" in e) if os.path.exists(ep_path) else 0
    sizes = [len(g) for g in groups if g] or [len(eps) or 1]
    min_n = min(sizes)
    base = sum(1 for e in eps if e.get("variant") == "base")
    arch = os.path.relpath(os.path.join(os.path.dirname(DEFINITIONS_PATH), "ARCHITECTURE.md"),
                           os.path.abspath(out_dir))
    return {
        "has_scripted": any(str(e["agent"]).startswith("scripted") for e in eps),
        "has_llm": any(not str(e["agent"]).startswith("scripted") for e in eps),
        "policy_names": {e["policy_name"] for e in eps},
        "non_base": len(eps) - base, "base_share": base / len(eps) if eps else 0.0,
        "has_authority_variant": any(e.get("variant") == "authority" for e in eps),
        "unsplit": sum(1 for e in eps if "end_state_harm" not in e),
        "never_in_force": sum(e.get("authority_violations_never_in_force", 0) for e in eps),
        "authority_violations": sum(e["authority_violations"] for e in eps),
        "has_hidden_keys": any("expose_keys=False" in e["policy"] for e in eps),
        "has_compound": any("+" in e["faults"] for e in eps),
        "faults_injected": sum(len(e["faults_injected"]) for e in eps),
        "interventions": sum(e["interventions"] for e in eps),
        "min_n": min_n, "half_width": 1.96 * math.sqrt(0.25 / min_n),
        "refusals": sum(1 for e in eps if str(e.get("agent_error") or "").startswith("refusal")),
        "rescored": sum(1 for e in eps if e.get("rescored")),
        "errored": errored,
        "has_run_notes": os.path.exists(os.path.join(out_dir, "NOTES.md")),
        "arch_href": arch,
    }


def write_report(eps: List[dict], out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    href = defs_href(out_dir)
    by_policy = table(eps, ["policy", "agent"], HEADLINE)
    by_policy_runtime = table(eps, ["policy", "runtime", "agent"], ["n", "success", "harm", "failures_exposed",
                                                                    "tokens", "runtime_retries"])
    by_fault = table(eps, ["faults", "policy"], ["n", "success", "harm", "end_state_harm", "self_corrected_harm",
                                                 "duplicate_effects", "failures_exposed", "interventions_per_task"])
    by_variant = table(eps, ["variant", "policy"], ["n", "success", "harm", "interventions_per_task",
                                                    "intervention_precision", "intervention_recall"])
    own = failure_ownership(eps)
    rc = risk_coverage(eps)
    for name, rows in [("by_policy", by_policy), ("by_policy_runtime", by_policy_runtime), ("by_fault", by_fault),
                       ("by_variant", by_variant), ("failure_ownership", own), ("risk_coverage", rc)]:
        to_csv(rows, os.path.join(out_dir, f"{name}.csv"))

    groupings = (["policy", "agent"], ["policy", "runtime", "agent"], ["faults", "policy"], ["variant", "policy"],
                 ["policy", "policy_name", "agent"])
    ctx = report_context(eps, out_dir, [g for keys in groupings for g in group(eps, keys).values()])
    used: List[str] = []

    def marks(section: str) -> str:
        keys = [k for k in SECTION_NOTES[section] if note(k).applies(ctx)]
        used.extend(k for k in keys if k not in used)
        return "".join(f"[^{k}]" for k in keys)

    def sec(title: str, section: str, rows: List[dict], cols=None) -> List[str]:
        return [f"## {title}{marks(section)}", "", to_markdown(rows, cols, href)]

    defs_link = os.path.relpath(DEFINITIONS_PATH, os.path.abspath(out_dir))
    md = [f"# Autonomy Boundary Harness: report{marks('top')}", "",
          f"Episodes: {len(eps)}. Column headers link to their definitions in "
          f"[DEFINITIONS.md]({defs_link}); footnotes qualify the sections they're attached to.", ""]
    md += sec("Headline metrics by policy", "headline", by_policy)
    md += sec("Runtime factor (H1/H6)", "runtime", by_policy_runtime)
    md += sec("Risk–coverage points (H4)", "risk_coverage", rc)
    md += sec("Escalation quality by task variant (H3/H7)", "variant", by_variant)
    md += sec("Outcomes by fault condition", "fault", by_fault)
    md += sec("Failure ownership (RQ1)", "ownership", own)
    md += [f"[^{k}]: {render_note(note(k), ctx, href)} ([about this note]({defs_link}#note-{k}))" for k in used]
    path = os.path.join(out_dir, "report.md")
    with open(path, "w") as f:
        f.write("\n".join(md) + "\n")
    _maybe_plot(rc, out_dir)
    return path


def _maybe_plot(rc: List[dict], out_dir: str) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    fig, ax = plt.subplots(figsize=(6, 4.5))
    for (name, agent), pts in group(rc, ["policy_name", "agent"]).items():
        pts = sorted(pts, key=lambda r: r["autonomous_coverage"])
        ax.plot([p["autonomous_coverage"] for p in pts], [p["autonomous_risk"] for p in pts], marker="o",
                label=f"{name} · {agent}")
    ax.set_xlabel("Autonomous coverage (tasks completed with no human)")
    ax.set_ylabel("Autonomous risk  P(not success | autonomous)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "risk_coverage.png"), dpi=160)
