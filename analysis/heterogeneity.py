"""Per-model heterogeneity of the paper's main effects (exploratory, post hoc).

    .venv/bin/python analysis/heterogeneity.py [out_dir]     (default: docs/heterogeneity)

The confirmatory tests pool models with Mantel–Haenszel, which reports one odds ratio per
hypothesis. This script asks how much that pooled effect varies by model. For each claim it
reports, per model, both arms' rates and the risk difference (A − B, percentage points) with a
Newcombe hybrid-Wilson 95% interval, then:
- the Mantel–Haenszel pooled risk difference across models
- Cochran's Q and I² on the per-model risk differences (inverse-variance; rates shrunk by
  (k + 0.5) / (n + 1) so a 0/n cell has finite variance)
- the Breslow–Day test (Tarone-adjusted) for equal odds ratios across models, with 0.5 added to
  every cell of a table that has a zero
- how many models show the effect in the predicted direction (and how many tie or reverse), and
  how many have an interval excluding 0

Arms and exclusions follow each study's registered analysis. Where arm B is a deterministic
engine (no model), each model is compared with the pooled engine rate, and heterogeneity is
tested on the agents' rates alone. Not pre-registered; report as exploratory.
"""
from __future__ import annotations

import math
import os
import sys
import textwrap
from collections import defaultdict
from functools import lru_cache

import numpy as np
from scipy.stats import chi2
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.proportion import proportion_confint

sys.path.insert(0, ".")
from abh.metrics import load_episodes  # noqa: E402

RUNS = {
    "confirm": "runs/compound-confirm-20261012-112744",
    "stage-a": "runs/stage-a-20261013-101143",
    "stage-c": "runs/stage-c-20261013-112552",
    "open-confirm": "runs/open-confirm-20261014-081413",
    "open-stage-a": "runs/open-stage-a-20261014-081413",
    "stage-d": "runs/stage-d-20261018-111143",
    "contracts": "runs/contracts-20261026-140610",
    "repair": "runs/repair-20261027-101723",
    "stage-e": "runs/stage-e-20261027-135311",
}
TD = "timeout_after_execution+delayed_visibility"
PT = "partial_mutation+timeout_after_execution"
SEMANTIC = ("persistent_unavailable", "precondition_changed", "task_invalid_result")
FRONTIER = {"claude-fable-5-1", "gpt-6-astra"}
OPEN_PROVIDERS = {"together", "fireworks", "deepinfra", "openrouter", "deepseek", "zai"}
P6, NOKEY = "P6[threshold=0.7]", "P1[expose_keys=False]"

harm = lambda e: bool(e["harm"])
success = lambda e: bool(e["success"])
llm = lambda e: not e["agent"].startswith("scripted")


def model(e):
    return e["agent"].split(":", 1)[1].split("@")[0]


def family(m_or_e) -> str:
    agent = m_or_e["agent"] if isinstance(m_or_e, dict) else m_or_e
    return "open" if agent.split(":")[0] in OPEN_PROVIDERS else "closed"


@lru_cache(maxsize=None)
def episodes(run: str) -> tuple:
    rows = load_episodes(os.path.join(RUNS[run], "episodes.jsonl"))
    return tuple(e for e in rows if "error" not in e and not (
        e.get("agent_error") and not str(e["agent_error"]).startswith("refusal")))


def pol(p, faults=None, extra=lambda e: True):
    return lambda e: e["policy"] == p and (faults is None or e["faults"] == faults) and extra(e)


frontier = lambda e: model(e) in FRONTIER
non_base = lambda e: e["variant"] != "base"
ledger = lambda e: e["domain"] == "ledger"
dev = lambda e: e["domain"] != "ledger"
sem = lambda e: e["faults"] in SEMANTIC


def rt(policy, runtime, where=lambda e: True):
    return lambda e: e["policy"] == policy and e["runtime"] == runtime and where(e)


def contract(policy, c):
    return lambda e: e["policy"] == policy and e["contract"] == c and e["faults"] == PT


# (id, paper question, title, [(run, arm A, arm B)], outcome, registered source)
# Arm A is the arm the registered hypothesis predicts higher.
CLAIMS = [
    ("Q1", "Q1", "Hidden write, development domains: harm without keys − with the runtime (P6)",
     [("confirm", pol(NOKEY, TD), pol(P6, TD)),
      ("stage-c", pol(NOKEY, TD, frontier), pol(P6, TD, frontier)),
      ("open-confirm", pol(NOKEY, TD), pol(P6, TD))], harm, "C1, G1, OC1"),
    ("Q2", "Q2", "Semantic faults: agent success − fixed workflow",
     [("stage-a", pol("P1[runtime=semantic]", extra=lambda e: sem(e) and llm(e)),
       lambda e: sem(e) and e["agent"] == "scripted:workflow"),
      ("open-stage-a", pol("P1[runtime=semantic]", extra=lambda e: sem(e) and llm(e)),
       lambda e: sem(e) and e["agent"] == "scripted:workflow")], success, "A1, OA1"),
    ("Q2-rules", "Q2", "Semantic faults, development domains: agent success − general recovery rules",
     [("stage-e", pol("P1", extra=lambda e: sem(e) and llm(e) and dev(e)),
       lambda e: sem(e) and dev(e) and e["agent"] == "scripted:rules_generic")], success, "E3a"),
    ("Q3-success", "Q3", "Human-needed variants, semantic runtime: success with P6 − P1",
     [("stage-d", rt(P6, "semantic", non_base), rt("P1", "semantic", non_base))], success, "D1"),
    ("Q3-harm", "Q3", "Semantic runtime: harm with P1 − P6",
     [("stage-d", rt("P1", "semantic"), rt(P6, "semantic"))], harm, "D3"),
    ("Q4-keys", "Q4", "Hidden partial commit: harm with keys − without",
     [("confirm", pol("P1", PT), pol(NOKEY, PT)),
      ("stage-c", pol("P1", PT, frontier), pol(NOKEY, PT, frontier)),
      ("open-confirm", pol("P1", PT), pol(NOKEY, PT))], harm, "C3, G4, OC3"),
    ("Q4-wording", "Q4", "Hidden partial commit: harm with 'at most once' − contract-generated wording",
     [("contracts", contract("P1", "default"), contract("P1[key_description=contract]", "default"))],
     harm, "K2"),
    ("Q4-repair", "Q4", "Hidden partial commit, atomic scope: harm without − with repair primitives",
     [("repair", contract("P1[key_description=contract]", "key_scope=atomic"),
       contract("P1[key_description=contract]", "key_scope=atomic,partial_report=True,repair=cancel_partial"))],
     harm, "R1"),
    # Q5 (paper §7.5): the held-out accounts-payable family, written after the design was frozen.
    ("Q5-hidden-write", "Q5", "Hidden write, held-out accounts-payable family: harm without keys − with the runtime (P6)",
     [("stage-e", pol(NOKEY, TD, ledger), pol(P6, TD, ledger))], harm, "E1"),
    ("Q5-authority", "Q5", "Authority tasks, held-out accounts-payable family: harm with P1 − P6",
     [("stage-e", pol("P1", extra=lambda e: ledger(e) and e["variant"] == "authority"),
       pol(P6, extra=lambda e: ledger(e) and e["variant"] == "authority"))], harm, "E4"),
]


def newcombe(ka, na, kb, nb):
    la, ua = proportion_confint(ka, na, method="wilson")
    lb, ub = proportion_confint(kb, nb, method="wilson")
    pa, pb = ka / na, kb / nb
    d = pa - pb
    return d, d - math.sqrt((pa - la) ** 2 + (ub - pb) ** 2), d + math.sqrt((ua - pa) ** 2 + (pb - lb) ** 2)


def rows_for(claim):
    """Per model: (label, family, ka, na, kb, nb, shared_baseline)."""
    _, _, _, parts, outcome, _ = claim
    out = []
    for run, in_a, in_b in parts:
        eps = episodes(run)
        a, b = defaultdict(list), defaultdict(list)
        for e in eps:
            if in_a(e):
                a[model(e)].append(e)
            elif in_b(e):
                b[model(e) if llm(e) else None].append(e)
        for m in sorted(a):
            shared = m not in b
            bs = b[None] if shared else b[m]
            if not bs:
                continue
            fam = family(a[m][0])
            label = m if len(parts) == 1 else f"{m} ({run})"
            out.append((label, fam, sum(map(outcome, a[m])), len(a[m]), sum(map(outcome, bs)), len(bs), shared))
    return out


def heterogeneity(rows):
    """Cochran's Q and I² on risk differences, Breslow–Day on odds ratios, MH pooled RD."""
    shared = all(r[6] for r in rows)
    shrink = lambda k, n: (k + 0.5) / (n + 1)
    ys, ws = [], []
    for _, _, ka, na, kb, nb, _ in rows:
        pa, pb = shrink(ka, na), shrink(kb, nb)
        var = pa * (1 - pa) / na + (0 if shared else pb * (1 - pb) / nb)
        ys.append(ka / na - (0 if shared else kb / nb))
        ws.append(1 / var)
    ys, ws = np.array(ys), np.array(ws)
    mean = float((ws * ys).sum() / ws.sum())
    q = float((ws * (ys - mean) ** 2).sum())
    df = len(rows) - 1
    p_q = float(chi2.sf(q, df)) if df > 0 else float("nan")
    i2 = max(0.0, (q - df) / q) if q > 0 else 0.0
    p_bd = float("nan")
    if not shared and df > 0:
        tables = []
        for _, _, ka, na, kb, nb, _ in rows:
            t = np.array([[ka, na - ka], [kb, nb - kb]], dtype=float)
            tables.append(t + 0.5 if (t == 0).any() else t)
        p_bd = float(StratifiedTable(tables).test_equal_odds(adjust=True).pvalue)
    w = [na * nb / (na + nb) for _, _, _, na, _, nb, _ in rows]
    mh = sum(wi * (ka / na - kb / nb) for wi, (_, _, ka, na, kb, nb, _) in zip(w, rows)) / sum(w)
    return {"q": q, "df": df, "p_q": p_q, "i2": i2, "p_bd": p_bd, "mh_rd": mh, "shared": shared}


def forest(results, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, ink2, muted, grid, surface = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
    colors = {"closed": "#2a78d6", "open": "#eb6834"}  # categorical slots 1–2 (validated adjacent pair)
    markers = {"closed": "o", "open": "s"}  # secondary encoding, so identity isn't colour alone
    n = len(results)
    cols = 2
    nrows = math.ceil(n / cols)
    heights = [max(len(results[i][1]) for i in range(k * cols, min(n, k * cols + cols))) + 3 for k in range(nrows)]
    fig, axes = plt.subplots(nrows, cols, figsize=(13, sum(heights) * 0.27 + 1.2),
                             gridspec_kw={"height_ratios": heights}, facecolor=surface)
    axes = np.atleast_2d(axes)
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    for ax, (claim, rows, h) in zip(axes.flat, results):
        ax.set_facecolor(surface)
        ys = list(range(len(rows)))[::-1]
        for y, (label, fam, ka, na, kb, nb, _) in zip(ys, rows):
            d, lo, hi = newcombe(ka, na, kb, nb)
            ax.plot([lo * 100, hi * 100], [y, y], color=colors[fam], lw=2, solid_capstyle="round", zorder=2)
            ax.scatter([d * 100], [y], s=40, marker=markers[fam], color=colors[fam], edgecolor=surface,
                       linewidth=1.5, zorder=3)
        ax.scatter([h["mh_rd"] * 100], [-1.2], s=70, marker="D", color=ink, zorder=3)
        ax.axvline(0, color=muted, lw=1, zorder=1)
        ax.set_yticks(ys + [-1.2])
        ax.set_yticklabels([r[0] for r in rows] + ["pooled (MH)"], fontsize=8, color=ink2)
        ax.set_xlim(-105, 105)
        ax.set_ylim(-2, len(rows))
        ax.grid(axis="x", color=grid, lw=0.6)
        ax.tick_params(axis="x", labelsize=8, colors=muted)
        ax.tick_params(axis="y", length=0)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(grid)
        title = textwrap.fill(f"{claim[0]} ({claim[5]}): {claim[2]}", 56)
        ax.set_title(f"{title}\nI² = {h['i2']:.0%}, Q p = {h['p_q']:.2g}",
                     fontsize=8.5, color=ink, loc="left")
        ax.set_xlabel("risk difference, A − B (percentage points)", fontsize=8, color=muted)
    handles = [plt.Line2D([], [], marker=markers[f], color=colors[f], lw=2, label=f"{f} models") for f in colors]
    handles.append(plt.Line2D([], [], marker="D", color=ink, lw=0, label="pooled across models"))
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=160, facecolor=surface)
    plt.close(fig)


def main(out_dir: str = "docs/heterogeneity") -> None:
    os.makedirs(out_dir, exist_ok=True)
    results = []
    out = ["# Per-model heterogeneity of the main effects (exploratory)", "",
           "Generated by `analysis/heterogeneity.py` from the committed runs. **Not pre-registered.** The "
           "confirmatory tests pooled models; this asks how much each effect varies by model.", "",
           "Per model: arm A and arm B rates, and the risk difference A − B in percentage points with a "
           "Newcombe 95% interval. Heterogeneity: Cochran's Q and I² on the per-model risk differences, and "
           "the Breslow–Day test for equal odds ratios. *Direction* counts models with A − B above / equal to "
           "/ below zero (above is the registered prediction; equal is usually 0% in both arms); *CI > 0* "
           "counts those whose interval excludes zero.", "",
           "![Forest plot](forest.png)", "",
           "## Summary", "",
           "| Claim | Source | Models | Pooled A − B | Range across models | Direction | CI > 0 | I² | Q p | Breslow–Day p |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    detail = []
    for claim in CLAIMS:
        rows = rows_for(claim)
        h = heterogeneity(rows)
        results.append((claim, rows, h))
        cis = [newcombe(ka, na, kb, nb) for _, _, ka, na, kb, nb, _ in rows]
        rds = [c[0] for c in cis]
        pos, tie, neg = sum(d > 0 for d in rds), sum(d == 0 for d in rds), sum(d < 0 for d in rds)
        sig = sum(lo > 0 for _, lo, _ in cis)
        bd = "n/a (shared baseline)" if h["shared"] else f"{h['p_bd']:.2g}"
        out.append(f"| {claim[0]}: {claim[2]} | {claim[5]} | {len(rows)} | {h['mh_rd'] * 100:+.0f} | "
                   f"{min(rds) * 100:+.0f} to {max(rds) * 100:+.0f} | {pos} / {tie} / {neg} | {sig}/{len(rows)} | "
                   f"{h['i2']:.0%} | {h['p_q']:.2g} | {bd} |")
        detail += ["", f"### {claim[0]}: {claim[2]}", "", f"Registered source: {claim[5]}."
                   + (" Arm B is a deterministic engine; each model is compared with its pooled rate."
                      if h["shared"] else ""), "",
                   "| Model | Family | A | B | A − B (95% CI) |", "|---|---|---|---|---|"]
        for (label, fam, ka, na, kb, nb, _), (d, lo, hi) in zip(rows, cis):
            detail.append(f"| {label} | {fam} | {ka}/{na} ({ka / na:.0%}) | {kb}/{nb} ({kb / nb:.0%}) | "
                          f"{d * 100:+.0f} ({lo * 100:+.0f} to {hi * 100:+.0f}) |")
    out += ["", "## Per model"] + detail
    forest(results, os.path.join(out_dir, "forest.png"))
    text = "\n".join(out) + "\n"
    with open(os.path.join(out_dir, "heterogeneity.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main(*sys.argv[1:])
