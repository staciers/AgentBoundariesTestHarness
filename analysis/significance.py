"""Significance, direction consistency and power for the compound-fault contrasts.

    .venv/bin/python analysis/significance.py runs/compound-live-20261011-123250

For each contrast, it reports:

* the counts in each arm
* an exact test: Fisher, plus Mantel-Haenszel stratified by model x scenario, because
  episodes within a scenario are not independent
* Holm-adjusted p-values across the confirmatory family
* direction consistency across strata (sign test)
* episodes per arm needed for 80% power, and what they would cost at observed per-episode costs

Needs scipy and statsmodels (analysis-only; not harness dependencies).
"""
from __future__ import annotations

import math
import sys
from collections import defaultdict
from typing import Callable, Dict, List, Tuple

import numpy as np
from scipy.stats import binomtest, fisher_exact, mannwhitneyu
from statsmodels.stats.contingency_tables import StratifiedTable
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import confint_proportions_2indep, proportion_effectsize

sys.path.insert(0, ".")
from abh.metrics import load_episodes  # noqa: E402

TD = "timeout_after_execution+delayed_visibility"
PT = "partial_mutation+timeout_after_execution"
NOKEY = "P1[expose_keys=False]"
P6 = "P6[threshold=0.7]"
STRONG = {"claude-opus-5-5", "gpt-6.1-sol"}
PROVIDER = {"claude-opus-5-5": "anthropic", "claude-haiku-5-5": "anthropic", "gpt-6.1-sol": "openai",
            "gpt-6-luna": "openai"}
POWER, ALPHA = 0.80, 0.05


def model(e) -> str:
    return e["agent"].split(":")[1].split("@")[0]


def contrast(eps, a_sel, b_sel, outcome, strata=lambda e: (model(e), e["scenario"])):
    a = [e for e in eps if a_sel(e)]
    b = [e for e in eps if b_sel(e)]
    ka, kb = sum(outcome(e) for e in a), sum(outcome(e) for e in b)
    _, p_fisher = fisher_exact([[ka, len(a) - ka], [kb, len(b) - kb]])
    # Mantel-Haenszel across strata (skip strata missing an arm or without variation)
    tables, signs = [], []
    by: Dict[tuple, Tuple[list, list]] = defaultdict(lambda: ([], []))
    for e in a:
        by[strata(e)][0].append(e)
    for e in b:
        by[strata(e)][1].append(e)
    for key, (sa, sb) in sorted(by.items()):
        if not sa or not sb:
            continue
        xa, xb = sum(outcome(e) for e in sa), sum(outcome(e) for e in sb)
        tables.append(np.array([[xa, len(sa) - xa], [xb, len(sb) - xb]], dtype=float) + 0.0)
        ra, rb = xa / len(sa), xb / len(sb)
        signs.append(0 if ra == rb else (1 if ra > rb else -1))
    p_mh = float("nan")
    informative = [t for t in tables if t[:, 0].sum() > 0 and t[:, 1].sum() > 0]
    if len(informative) >= 1:
        try:
            p_mh = StratifiedTable(informative).test_null_odds(correction=True).pvalue
        except Exception:
            pass
    pos, neg = signs.count(1), signs.count(-1)
    p_sign = binomtest(pos, pos + neg, 0.5).pvalue if pos + neg else float("nan")
    return dict(na=len(a), ka=ka, nb=len(b), kb=kb, pa=ka / len(a), pb=kb / len(b), p_fisher=p_fisher,
                p_mh=p_mh, strata_same_dir=pos, strata_opposite=neg, strata_tied=signs.count(0), p_sign=p_sign)


def n_conservative(r: dict, alpha: float) -> float:
    """Episodes per arm, planning for the low end of the 95% CI of the difference.

    Observed effects in small samples tend to be inflated, so planning on them under-sizes
    the confirmation run.
    """
    lo, hi = confint_proportions_2indep(r["ka"], r["na"], r["kb"], r["nb"], method="newcomb")
    toward_null = lo if r["pa"] >= r["pb"] else -hi
    if toward_null <= 0:
        return float("inf")
    return n_per_arm(r["pb"] + toward_null, r["pb"], alpha)


def n_per_arm(pa: float, pb: float, alpha: float) -> float:
    """Episodes per arm for 80% power (two-sided), from Cohen's h. Zero cells nudged to 0.5/n-style floor."""
    pa, pb = min(max(pa, 0.02), 0.98), min(max(pb, 0.02), 0.98)
    h = abs(proportion_effectsize(pa, pb))
    if h < 1e-9:
        return float("inf")
    return NormalIndPower().solve_power(effect_size=h, alpha=alpha, power=POWER, ratio=1.0)


def main(run_dir: str) -> None:
    eps = [e for e in load_episodes(f"{run_dir}/episodes.jsonl") if "error" not in e]
    cost = defaultdict(list)
    for e in eps:
        cost[model(e)].append(e["model_cost_usd"])
    unit = {m: float(np.mean(v)) for m, v in cost.items()}
    harm = lambda e: bool(e["harm"])
    end = lambda e: bool(e["end_state_harm"])
    f = lambda e, faults, pol: e["faults"] == faults and e["policy"] == pol
    rows: List[Tuple[str, str, dict, List[str]]] = []

    def add(name, hyp, r, models):
        rows.append((name, hyp, r, models))

    all_m = sorted(PROVIDER)
    # Confirmatory family -------------------------------------------------------------
    add("No keys vs keys, timeout+hidden write (harm)", "H1",
        contrast(eps, lambda e: f(e, TD, NOKEY), lambda e: f(e, TD, "P1"), harm), all_m)
    add("No keys vs P6 runtime, timeout+hidden write (harm)", "H1",
        contrast(eps, lambda e: f(e, TD, NOKEY), lambda e: f(e, TD, P6), harm), all_m)
    add("Weak vs strong model, no keys, timeout+hidden write (end-state harm)", "H5",
        contrast(eps, lambda e: f(e, TD, NOKEY) and model(e) not in STRONG,
                 lambda e: f(e, TD, NOKEY) and model(e) in STRONG, end,
                 strata=lambda e: (PROVIDER[model(e)], e["scenario"])), all_m)
    add("Keys vs no keys, hidden partial commit, all models (harm)", "keys",
        contrast(eps, lambda e: f(e, PT, "P1"), lambda e: f(e, PT, NOKEY), harm), all_m)
    # Exploratory ------------------------------------------------------------------
    add("Keys vs no keys, hidden partial commit, OpenAI only (harm)", "keys (exploratory)",
        contrast(eps, lambda e: f(e, PT, "P1") and PROVIDER[model(e)] == "openai",
                 lambda e: f(e, PT, NOKEY) and PROVIDER[model(e)] == "openai", harm), ["gpt-6.1-sol", "gpt-6-luna"])
    add("Weak vs strong model, no keys (any harm incl. self-corrected)", "H5 (exploratory)",
        contrast(eps, lambda e: f(e, TD, NOKEY) and model(e) not in STRONG,
                 lambda e: f(e, TD, NOKEY) and model(e) in STRONG, harm,
                 strata=lambda e: (PROVIDER[model(e)], e["scenario"])), all_m)
    add("OpenAI vs Claude with keys, hidden partial commit (harm)", "provider (exploratory)",
        contrast(eps, lambda e: f(e, PT, "P1") and PROVIDER[model(e)] == "openai",
                 lambda e: f(e, PT, "P1") and PROVIDER[model(e)] == "anthropic", harm,
                 strata=lambda e: e["scenario"]), all_m)
    for m in all_m:
        add(f"No keys vs keys, timeout+hidden write: {m}", "H1 per model",
            contrast(eps, lambda e, m=m: f(e, TD, NOKEY) and model(e) == m,
                     lambda e, m=m: f(e, TD, "P1") and model(e) == m, harm), [m])

    confirm = [i for i, r in enumerate(rows) if "exploratory" not in r[1] and "per model" not in r[1]]
    pvals = [rows[i][2]["p_mh"] if not math.isnan(rows[i][2]["p_mh"]) else rows[i][2]["p_fisher"] for i in confirm]
    holm = multipletests(pvals, method="holm")[1]
    adj = {i: h for i, h in zip(confirm, holm)}
    alpha_planned = ALPHA / max(1, len(confirm))  # conservative planning alpha (Bonferroni)

    out = ["# Significance and power: compound-fault contrasts", "",
           f"Run: `{run_dir}`. {len(eps)} episodes. Generated by `analysis/significance.py`.", "",
           "Arms are compared on the outcome named in each row. `p (MH)` is Mantel–Haenszel stratified by "
           "model × scenario (provider × scenario for model comparisons); `Holm` adjusts the confirmatory "
           "family. Direction: strata where arm A is higher / lower / tied, and a sign-test p.", "",
           "| Contrast | Hyp | A k/n | B k/n | p (Fisher) | p (MH) | Holm | Direction (A>B / A<B / tie), p | "
           "n/arm for 80% power (conservative) | extra episodes | est. cost |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, (name, hyp, r, models) in enumerate(rows):
        a_ = alpha_planned if i in adj else ALPHA
        need = n_conservative(r, a_)
        have = min(r["na"], r["nb"])
        if math.isinf(need):
            extra, c = 0, 0.0
        else:
            extra = max(0, math.ceil(need - r["na"])) + max(0, math.ceil(need - r["nb"]))
            c = extra * float(np.mean([unit[m] for m in models]))
        need_s = "∞ (no effect seen)" if math.isinf(need) else f"{math.ceil(need)}"
        out.append(f"| {name} | {hyp} | {r['ka']}/{r['na']} ({r['pa']:.0%}) | {r['kb']}/{r['nb']} ({r['pb']:.0%}) | "
                   f"{r['p_fisher']:.2g} | {r['p_mh']:.2g} | {adj[i]:.2g} | " if i in adj else
                   f"| {name} | {hyp} | {r['ka']}/{r['na']} ({r['pa']:.0%}) | {r['kb']}/{r['nb']} ({r['pb']:.0%}) | "
                   f"{r['p_fisher']:.2g} | {r['p_mh']:.2g} | — | ")
        out[-1] += (f"{r['strata_same_dir']}/{r['strata_opposite']}/{r['strata_tied']}, {r['p_sign']:.2g} | "
                    f"{need_s} | {extra if not math.isinf(need) else '—'} | "
                    f"{'$%.2f' % c if not math.isinf(need) else '—'} |")

    # H6: efficiency (continuous) ---------------------------------------------------
    out += ["", "## H6: model calls, P1 (keys) vs P6, all fault conditions", "",
            "| Model | P1 mean | P6 mean | Mann–Whitney p |", "|---|---|---|---|"]
    for m in all_m:
        a = [e["model_calls"] for e in eps if model(e) == m and e["policy"] == "P1"]
        b = [e["model_calls"] for e in eps if model(e) == m and e["policy"] == P6]
        out.append(f"| {m} | {np.mean(a):.2f} | {np.mean(b):.2f} | {mannwhitneyu(a, b).pvalue:.2g} |")
    out += ["", f"Per-episode cost used for estimates: " +
            ", ".join(f"{m} ${unit[m]:.4f}" for m in all_m) + ".",
            f"Power planning targets the low end of each difference's 95% CI (Newcombe), not the observed "
            f"effect, because small-sample effects tend to be inflated. It uses α={alpha_planned:.4f} for "
            f"confirmatory rows (Bonferroni over {len(confirm)}) and α={ALPHA} otherwise; rates of 0% or 100% "
            f"are floored at 2%/98%. `∞` means the CI includes no effect, so no sample size is implied. "
            f"Extra episodes assume the same arms are extended; a confirmation run should use fresh seeds."]
    text = "\n".join(out) + "\n"
    with open(f"{run_dir}/significance.md", "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
