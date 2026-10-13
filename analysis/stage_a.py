"""Pre-registered analysis for Stage A (H2, RQ1, RQ2).

    .venv/bin/python analysis/stage_a.py runs/<stage-a-run>

Implements exactly the tests in docs/preregistration/stage-a.md. Freeze with the
pre-registration commit; add new analyses only to the exploratory section.
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import test_proportions_2indep

sys.path.insert(0, ".")
from abh.faults import FaultType  # noqa: E402
from abh.metrics import failure_ownership, load_episodes, to_markdown  # noqa: E402
from analysis.confirmatory import stratified, wilson  # noqa: E402  (frozen helpers)

SEMANTIC = {f.value for f in FaultType if f.failure_class.value == "semantic"}
EXECUTION = {f.value for f in FaultType if f.failure_class.value == "execution"}
SEMRT = "P1[runtime=semantic]"
NONE_RT = "P1"
NAIVE = "P1[runtime=naive_retry]"
WORKFLOW = "scripted:workflow"
ALPHA = 0.05


def is_llm(e) -> bool:
    return not e["agent"].startswith("scripted")


def model(e) -> str:
    return e["agent"].split(":")[1].split("@")[0] if is_llm(e) else "workflow"


def success(e) -> bool:
    return bool(e["success"])


def harm(e) -> bool:
    return bool(e["harm"])


def tost(ka, na, kb, nb, margin):
    lo = test_proportions_2indep(ka, na, kb, nb, value=-margin, compare="diff", alternative="larger").pvalue
    hi = test_proportions_2indep(ka, na, kb, nb, value=margin, compare="diff", alternative="smaller").pvalue
    diff = test_proportions_2indep(ka, na, kb, nb).pvalue
    p = max(lo, hi)
    verdict = ("**equivalent**" if p < ALPHA else "**different**" if diff < ALPHA else "inconclusive")
    return p, diff, verdict


def main(run_dir: str) -> None:
    rows = load_episodes(os.path.join(run_dir, "episodes.jsonl"))
    excluded = [e for e in rows if "error" in e or (e.get("agent_error") and
                                                    not str(e["agent_error"]).startswith("refusal"))]
    eps = [e for e in rows if e not in excluded]
    sem = lambda e: e["faults"] in SEMANTIC
    exe = lambda e: e["faults"] in EXECUTION
    sf = lambda e: (e["scenario"], e["faults"])
    msf = lambda e: (model(e), e["scenario"], e["faults"])

    fam = [
        ("A1", "H2: LLM agents succeed more than the deterministic workflow on semantic faults (semantic runtime)",
         stratified(eps, lambda e: sem(e) and is_llm(e) and e["policy"] == SEMRT,
                    lambda e: sem(e) and e["agent"] == WORKFLOW, success, sf)),
        ("A2", "H2: the workflow causes more harm than LLM agents on semantic faults (semantic runtime)",
         stratified(eps, lambda e: sem(e) and e["agent"] == WORKFLOW,
                    lambda e: sem(e) and is_llm(e) and e["policy"] == SEMRT, harm, sf)),
        ("A3", "RQ2/H1: LLM agents cause more harm without a runtime than with the semantic runtime (execution faults)",
         stratified(eps, lambda e: exe(e) and is_llm(e) and e["policy"] == NONE_RT,
                    lambda e: exe(e) and is_llm(e) and e["policy"] == SEMRT, harm, msf)),
    ]
    holm = multipletests([r["p"] for _, _, r in fam], alpha=ALPHA, method="holm")[1]
    out = ["# Stage A analysis (H2, RQ1, RQ2)", "",
           f"Run: `{run_dir}`. Pre-registration: `docs/preregistration/stage-a.md`. {len(eps)} analysed; "
           f"{len(excluded)} excluded.", "",
           "## Confirmatory family (Holm, α = 0.05)", "",
           "Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher).", "",
           "| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |", "|---|---|---|---|---|---|---|---|"]
    for (cid, name, r), h in zip(fam, holm):
        ok = h < ALPHA and r["or"] > 1
        out.append(f"| {cid} | {name} | {r['ka']}/{r['na']} ({r['pa']:.0%}) | {r['kb']}/{r['nb']} ({r['pb']:.0%}) | "
                   f"{r['or']:.2f} | {r['p']:.2g} | {h:.2g} | {'**confirmed**' if ok else 'not confirmed'} |")

    out += ["", "## Equivalence tests (TOST, α = 0.05 each)", ""]
    a = [e for e in eps if exe(e) and is_llm(e) and e["policy"] == SEMRT]
    b = [e for e in eps if exe(e) and e["agent"] == WORKFLOW]
    p, d, v = tost(sum(map(success, a)), len(a), sum(map(success, b)), len(b), 0.05)
    out.append(f"- **E1** (the runtime suffices for execution faults): success on execution faults under the "
               f"semantic runtime, LLM agents {sum(map(success, a))}/{len(a)} vs workflow "
               f"{sum(map(success, b))}/{len(b)}; margin ±5 points. TOST p = {p:.2g}, difference p = {d:.2g}. "
               f"Verdict: {v}.")
    a = [e for e in eps if sem(e) and is_llm(e) and e["policy"] == SEMRT]
    b = [e for e in eps if sem(e) and is_llm(e) and e["policy"] == NONE_RT]
    p, d, v = tost(sum(map(success, a)), len(a), sum(map(success, b)), len(b), 0.10)
    out.append(f"- **E2** (semantic faults are the agent's: the runtime doesn't change LLM success): semantic "
               f"runtime {sum(map(success, a))}/{len(a)} vs none {sum(map(success, b))}/{len(b)}; margin ±10 "
               f"points. TOST p = {p:.2g}, difference p = {d:.2g}. Verdict: {v}.")

    out += ["", "## Secondary (pre-registered, outside the family)", "",
            "### Success and harm by controller × fault class (semantic runtime)", "",
            "| Fault class | Controller | success | harm |", "|---|---|---|---|"]
    cells = defaultdict(list)
    for e in eps:
        if e["policy"] != SEMRT or e["faults"] == "none":
            continue
        cells[("semantic" if sem(e) else "execution", model(e))].append(e)
    for (fc, m), es in sorted(cells.items()):
        n, ks, kh = len(es), sum(map(success, es)), sum(map(harm, es))
        (sl, sh), (hl, hh) = wilson(ks, n), wilson(kh, n)
        out.append(f"| {fc} | {m} | {ks}/{n} ({ks / n:.0%}, {sl:.0%}–{sh:.0%}) | {kh}/{n} ({kh / n:.0%}, {hl:.0%}–{hh:.0%}) |")
    out += ["", "### Runtime factor on execution faults (LLM agents)", "",
            "| Runtime | Model | success | harm | failures exposed | model calls |", "|---|---|---|---|---|---|"]
    cells = defaultdict(list)
    for e in eps:
        if is_llm(e) and exe(e):
            cells[(e["runtime"], model(e))].append(e)
    for (rt, m), es in sorted(cells.items()):
        n = len(es)
        out.append(f"| {rt} | {m} | {sum(map(success, es))}/{n} | {sum(map(harm, es))}/{n} | "
                   f"{sum(e['failures_exposed_to_agent'] for e in es) / n:.2f} | {sum(e['model_calls'] for e in es) / n:.2f} |")
    out += ["", "### Semantic faults by type (semantic runtime)", "", "| Fault | Controller | success | harm |",
            "|---|---|---|---|"]
    cells = defaultdict(list)
    for e in eps:
        if sem(e) and e["policy"] == SEMRT:
            cells[(e["faults"], model(e))].append(e)
    for (ft, m), es in sorted(cells.items()):
        n = len(es)
        out.append(f"| {ft} | {m} | {sum(map(success, es))}/{n} | {sum(map(harm, es))}/{n} |")
    out += ["", "### Failure ownership (RQ1)", "", to_markdown(failure_ownership([e for e in eps if e["faults"] != "none"]))]
    out += ["", "## Exploratory", ""]
    r = stratified(eps, lambda e: exe(e) and is_llm(e) and e["policy"] == NAIVE,
                   lambda e: exe(e) and is_llm(e) and e["policy"] == NONE_RT, harm, msf)
    out.append(f"- naive retry vs no runtime, harm on execution faults: {r['ka']}/{r['na']} vs {r['kb']}/{r['nb']}, "
               f"MH OR {r['or']:.2f}, p {r['p']:.2g}")
    text = "\n".join(out) + "\n"
    with open(os.path.join(run_dir, "stage_a.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
