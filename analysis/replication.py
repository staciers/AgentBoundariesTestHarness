"""Pre-registered analysis for the open-weight replications.

    .venv/bin/python analysis/replication.py confirm runs/<open-confirm-run>
    .venv/bin/python analysis/replication.py stage-a runs/<open-stage-a-run>

Implements exactly the tests in docs/preregistration/open-replications.md: the original
confirmatory tests (analysis/confirmatory.py, analysis/stage_a.py) re-stated for the
open-weight models' strong/weak tiers and families. The statistical helpers are imported
from those frozen scripts so they can't drift. Freeze with the registration commit.
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

from statsmodels.stats.multitest import multipletests

sys.path.insert(0, ".")
from abh.faults import FaultType  # noqa: E402
from abh.metrics import failure_ownership, load_episodes, to_markdown  # noqa: E402
from analysis.confirmatory import checked_before_retry, stratified, wilson  # noqa: E402  (frozen helpers)
from analysis.stage_a import tost  # noqa: E402  (frozen helper)

STRONG = {"deepseek-v4-pro-0813", "glm-5.3"}
WEAK = {"deepseek-v4-flash-0731", "glm-5.3-flash"}
FAMILY = {"deepseek-v4-pro-0813": "deepseek", "deepseek-v4-flash-0731": "deepseek",
          "glm-5.3": "glm", "glm-5.3-flash": "glm"}
TD = "timeout_after_execution+delayed_visibility"
PT = "partial_mutation+timeout_after_execution"
KEYED, NOKEY, CAVEATED, NEUTRAL = "P1", "P1[expose_keys=False]", "P1[key_description=caveated]", "P1[key_description=neutral]"
P6 = "P6[threshold=0.7]"
SEMRT, NAIVE = "P1[runtime=semantic]", "P1[runtime=naive_retry]"
WORKFLOW = "scripted:workflow"
SEMANTIC = {f.value for f in FaultType if f.failure_class.value == "semantic"}
EXECUTION = {f.value for f in FaultType if f.failure_class.value == "execution"}
ALPHA = 0.05


def model(e):
    return e["agent"].split(":", 1)[1].split("@")[0] if not e["agent"].startswith("scripted") else "workflow"


def is_open(e):
    return model(e) in FAMILY


def load(run_dir):
    rows = load_episodes(os.path.join(run_dir, "episodes.jsonl"))
    keep = [e for e in rows if "error" not in e and not (e.get("agent_error") and
                                                         not str(e["agent_error"]).startswith("refusal"))]
    return rows, keep


def family_table(fam, title):
    holm = multipletests([r["p"] for _, _, r in fam], alpha=ALPHA, method="holm")[1]
    out = [f"## {title} (Holm, α = 0.05)", "",
           "Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher).", "",
           "| ID | Hypothesis (original) | A k/n | B k/n | MH OR | p | Holm p | Verdict |", "|---|---|---|---|---|---|---|---|"]
    for (cid, name, r), h in zip(fam, holm):
        ok = h < ALPHA and r["or"] > 1
        out.append(f"| {cid} | {name} | {r['ka']}/{r['na']} ({r['pa']:.0%}) | {r['kb']}/{r['nb']} ({r['pb']:.0%}) | "
                   f"{r['or']:.2f} | {r['p']:.2g} | {h:.2g} | {'**replicated**' if ok else 'not replicated'} |")
    return out


def confirm(run_dir):
    rows, eps = load(run_dir)
    harm, end = (lambda e: bool(e["harm"])), (lambda e: bool(e["end_state_harm"]))
    f = lambda e, faults, pol: e["faults"] == faults and e["policy"] == pol
    ms = lambda e: (model(e), e["scenario"])
    fs = lambda e: (FAMILY[model(e)], e["scenario"])
    fam = [
        ("OC1", "C1: no keys > P6 runtime (hidden write, harm)",
         stratified(eps, lambda e: f(e, TD, NOKEY), lambda e: f(e, TD, P6), harm, ms)),
        ("OC2", "C2: weak > strong (hidden write, no keys, end-state harm)",
         stratified(eps, lambda e: f(e, TD, NOKEY) and model(e) in WEAK,
                    lambda e: f(e, TD, NOKEY) and model(e) in STRONG, end, fs)),
        ("OC3", "C3: keys > no keys (hidden partial commit, harm)",
         stratified(eps, lambda e: f(e, PT, KEYED), lambda e: f(e, PT, NOKEY), harm, ms)),
        ("OC5", "C5: 'at most once' > caveated wording (hidden partial commit, harm)",
         stratified(eps, lambda e: f(e, PT, KEYED), lambda e: f(e, PT, CAVEATED), harm, ms)),
    ]
    out = ["# Open-weight replication: confirmation design", "",
           f"Run: `{run_dir}`. Pre-registration: `docs/preregistration/open-replications.md`. {len(eps)} analysed, "
           f"{len(rows) - len(eps)} excluded.", ""] + family_table(fam, "Confirmatory family")
    a = [e for e in eps if f(e, TD, NOKEY) and model(e) in STRONG]
    b = [e for e in eps if f(e, TD, NOKEY) and model(e) in WEAK]
    p, d, v = tost(sum(map(harm, a)), len(a), sum(map(harm, b)), len(b), 0.10)
    out += ["", "## OE1 (= E1), equivalence, α = 0.05", "",
            f"Any harm, hidden write, no keys: strong {sum(map(harm, a))}/{len(a)} vs weak {sum(map(harm, b))}/{len(b)}; "
            f"margin ±10 points. TOST p = {p:.2g}, difference p = {d:.2g}. Verdict: {v}."]
    out += ["", "## Secondary (pre-registered)", "", "### Per-model rates (harm, Wilson 95% CI)", "",
            "| Cell | Policy | Model | harm | end-state | self-corrected |", "|---|---|---|---|---|---|"]
    cells = defaultdict(list)
    for e in eps:
        cells[(e["faults"], e["policy"], model(e))].append(e)
    for (c, pol, m), es in sorted(cells.items()):
        n, k = len(es), sum(map(harm, es))
        lo, hi = wilson(k, n)
        out.append(f"| {c} | {pol} | {m} | {k}/{n} ({k / n:.0%}, {lo:.0%}–{hi:.0%}) | {sum(map(end, es))} | "
                   f"{sum(bool(e.get('self_corrected_harm')) for e in es)} |")
    out += ["", "### Mechanism M1: checked state before retrying", "", "| Condition | Policy | Model | checked / eligible |",
            "|---|---|---|---|"]
    mech = defaultdict(lambda: [0, 0])
    for e in eps:
        if e["faults"] in (TD, PT):
            c = checked_before_retry(run_dir, e)
            if c is not None:
                mech[(e["faults"], e["policy"], model(e))][0] += int(c)
                mech[(e["faults"], e["policy"], model(e))][1] += 1
    for (c, pol, m), (k, n) in sorted(mech.items()):
        out.append(f"| {c} | {pol} | {m} | {k}/{n} ({k / n:.0%}) |")
    r = stratified(eps, lambda e: f(e, PT, KEYED) and FAMILY[model(e)] == "deepseek",
                   lambda e: f(e, PT, KEYED) and FAMILY[model(e)] == "glm", harm, lambda e: e["scenario"])
    out += ["", "## Exploratory", "",
            f"- Family difference in the keys hazard (two-sided, no predicted direction): DeepSeek "
            f"{r['ka']}/{r['na']} vs GLM {r['kb']}/{r['nb']}, MH OR {r['or']:.2f}, p {r['p']:.2g}.",
            "- Open vs closed comparisons with `runs/compound-confirm-20261012-112744` are exploratory."]
    _write(run_dir, "replication_confirm.md", out)


def stage_a(run_dir):
    rows, eps = load(run_dir)
    succ, harm = (lambda e: bool(e["success"])), (lambda e: bool(e["harm"]))
    sem, exe = (lambda e: e["faults"] in SEMANTIC), (lambda e: e["faults"] in EXECUTION)
    sf = lambda e: (e["scenario"], e["faults"])
    msf = lambda e: (model(e), e["scenario"], e["faults"])
    fam = [
        ("OA1", "A1: LLM > workflow success on semantic faults (semantic runtime)",
         stratified(eps, lambda e: sem(e) and is_open(e) and e["policy"] == SEMRT,
                    lambda e: sem(e) and e["agent"] == WORKFLOW, succ, sf)),
        ("OA2", "A2: workflow > LLM harm on semantic faults (semantic runtime)",
         stratified(eps, lambda e: sem(e) and e["agent"] == WORKFLOW,
                    lambda e: sem(e) and is_open(e) and e["policy"] == SEMRT, harm, sf)),
        ("OA3", "A3: no runtime > semantic runtime harm on execution faults",
         stratified(eps, lambda e: exe(e) and is_open(e) and e["policy"] == "P1",
                    lambda e: exe(e) and is_open(e) and e["policy"] == SEMRT, harm, msf)),
    ]
    out = ["# Open-weight replication: Stage A design", "",
           f"Run: `{run_dir}`. Pre-registration: `docs/preregistration/open-replications.md`. {len(eps)} analysed, "
           f"{len(rows) - len(eps)} excluded.", ""] + family_table(fam, "Confirmatory family")
    out += ["", "## Equivalence (TOST, α = 0.05 each)", ""]
    a = [e for e in eps if exe(e) and is_open(e) and e["policy"] == SEMRT]
    b = [e for e in eps if exe(e) and e["agent"] == WORKFLOW]
    p, d, v = tost(sum(map(succ, a)), len(a), sum(map(succ, b)), len(b), 0.05)
    out.append(f"- **OE1** (= E1): execution faults, semantic runtime, LLM {sum(map(succ, a))}/{len(a)} vs workflow "
               f"{sum(map(succ, b))}/{len(b)}, ±5 points: TOST p = {p:.2g}, difference p = {d:.2g}. Verdict: {v}.")
    a = [e for e in eps if sem(e) and is_open(e) and e["policy"] == SEMRT]
    b = [e for e in eps if sem(e) and is_open(e) and e["policy"] == "P1"]
    p, d, v = tost(sum(map(succ, a)), len(a), sum(map(succ, b)), len(b), 0.10)
    out.append(f"- **OE2** (= E2): semantic faults, LLM, semantic runtime {sum(map(succ, a))}/{len(a)} vs none "
               f"{sum(map(succ, b))}/{len(b)}, ±10 points: TOST p = {p:.2g}, difference p = {d:.2g}. Verdict: {v}.")
    out += ["", "## Secondary (pre-registered)", "", "### Controller × fault class (semantic runtime)", "",
            "| Fault class | Controller | success | harm |", "|---|---|---|---|"]
    cells = defaultdict(list)
    for e in eps:
        if e["policy"] == SEMRT and e["faults"] != "none":
            cells[("semantic" if sem(e) else "execution", model(e))].append(e)
    for (fc, m), es in sorted(cells.items()):
        n, ks, kh = len(es), sum(map(succ, es)), sum(map(harm, es))
        out.append(f"| {fc} | {m} | {ks}/{n} ({ks / n:.0%}) | {kh}/{n} ({kh / n:.0%}) |")
    out += ["", "### Runtime factor on execution faults", "", "| Runtime | Model | success | harm | failures exposed | model calls |",
            "|---|---|---|---|---|---|"]
    cells = defaultdict(list)
    for e in eps:
        if is_open(e) and exe(e):
            cells[(e["runtime"], model(e))].append(e)
    for (rt, m), es in sorted(cells.items()):
        n = len(es)
        out.append(f"| {rt} | {m} | {sum(map(succ, es))}/{n} | {sum(map(harm, es))}/{n} | "
                   f"{sum(e['failures_exposed_to_agent'] for e in es) / n:.2f} | {sum(e['model_calls'] for e in es) / n:.2f} |")
    out += ["", "### Failure ownership (RQ1)", "", to_markdown(failure_ownership([e for e in eps if e["faults"] != "none"]))]
    r = stratified(eps, lambda e: exe(e) and is_open(e) and e["policy"] == NAIVE,
                   lambda e: exe(e) and is_open(e) and e["policy"] == "P1", harm, msf)
    out += ["", "## Exploratory", "",
            f"- Naive retry vs no runtime, harm on execution faults: {r['ka']}/{r['na']} vs {r['kb']}/{r['nb']}, "
            f"MH OR {r['or']:.2f}, p {r['p']:.2g}.",
            "- Open vs closed comparisons with `runs/stage-a-20261013-101143` are exploratory."]
    _write(run_dir, "replication_stage_a.md", out)


def _write(run_dir, name, out):
    text = "\n".join(out) + "\n"
    with open(os.path.join(run_dir, name), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    {"confirm": confirm, "stage-a": stage_a}[sys.argv[1]](sys.argv[2])
