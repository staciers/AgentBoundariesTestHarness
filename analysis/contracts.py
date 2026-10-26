"""Pre-registered analysis for the contract study (key scope x key description).

    .venv/bin/python analysis/contracts.py runs/<contracts-run>

Implements exactly the tests in docs/preregistration/contracts.md. Freeze with the
pre-registration commit; add new analyses only to the exploratory section.
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict

from statsmodels.stats.multitest import multipletests

sys.path.insert(0, ".")
from abh.metrics import load_episodes  # noqa: E402
from analysis.confirmatory import checked_before_retry, stratified, wilson  # noqa: E402  (frozen helpers)
from analysis.stage_a import tost  # noqa: E402  (frozen helper)
from analysis.stage_b import noninferior  # noqa: E402  (frozen helper)

PARTIAL = "partial_mutation+timeout_after_execution"
HIDDEN_WRITE = "timeout_after_execution+delayed_visibility"
CONVENTIONAL, GENERATED, NO_KEYS = "P1", "P1[key_description=contract]", "P1[expose_keys=False]"
COMPLETED, ATOMIC = "default", "key_scope=atomic"
P6 = "P6[threshold=0.7]"
ALPHA = 0.05
OPEN_PROVIDERS = {"together", "fireworks", "deepinfra", "openrouter", "deepseek", "zai"}


def model(e):
    return e["agent"].split(":", 1)[1].split("@")[0]


def family(e):
    return "open" if e["agent"].split(":")[0] in OPEN_PROVIDERS else "closed"


harm = lambda e: bool(e["harm"])
end_state = lambda e: bool(e.get("end_state_harm"))
ms = lambda e: (model(e), e["scenario"])


def arm(policy, contract, fault=PARTIAL):
    return lambda e: e["policy"] == policy and e["contract"] == contract and e["faults"] == fault


ARMS = {"A: completed scope, 'at most once' wording": arm(CONVENTIONAL, COMPLETED),
        "B: completed scope, contract wording": arm(GENERATED, COMPLETED),
        "C: atomic scope, 'at most once' wording": arm(CONVENTIONAL, ATOMIC),
        "D: atomic scope, contract wording": arm(GENERATED, ATOMIC),
        "N: no keys": arm(NO_KEYS, COMPLETED)}


def rate(es, f=harm):
    k, n = sum(map(f, es)), len(es)
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({k / n:.0%}, {lo:.0%}–{hi:.0%})" if n else "—"


def main(run_dir: str) -> None:
    rows = load_episodes(os.path.join(run_dir, "episodes.jsonl"))
    eps = [e for e in rows if "error" not in e and not (e.get("agent_error") and
                                                         not str(e["agent_error"]).startswith("refusal"))]
    A, B, C, D, N = ARMS.values()
    fam = [
        ("K1", "Scope: an atomic key scope removes the hazard ('at most once' wording): A > C",
         stratified(eps, A, C, harm, ms)),
        ("K2", "Wording: contract-generated descriptions reduce harm (completed scope): A > B",
         stratified(eps, A, B, harm, ms)),
        ("K3", "Replication of C3 on fresh seeds, all 8 models: A > N",
         stratified(eps, A, N, harm, ms)),
    ]
    holm = multipletests([r["p"] for _, _, r in fam], alpha=ALPHA, method="holm")[1]
    out = ["# Contract study analysis (key scope × key description)", "",
           f"Run: `{run_dir}`. Pre-registration: `docs/preregistration/contracts.md`. {len(eps)} analysed, "
           f"{len(rows) - len(eps)} excluded.", "",
           "## Confirmatory family (Holm, α = 0.05)", "",
           "Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher). Outcome: harm.", "",
           "| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |", "|---|---|---|---|---|---|---|---|"]
    verdict = {}
    for (cid, name, r), h in zip(fam, holm):
        ok = h < ALPHA and r["or"] > 1
        verdict[cid] = ok
        out.append(f"| {cid} | {name} | {r['ka']}/{r['na']} ({r['pa']:.0%}) | {r['kb']}/{r['nb']} ({r['pb']:.0%}) | "
                   f"{r['or']:.2f} | {r['p']:.2g} | {h:.2g} | {'**confirmed**' if ok else 'not confirmed'} |")

    out += ["", "## Non-inferiority and equivalence (each α = 0.05, outside the Holm family)", ""]
    sel = lambda f: [e for e in eps if f(e)]
    ni = {}
    for cid, name, a in (("N1", "atomic scope, 'at most once' wording (C)", C),
                         ("N2", "atomic scope, contract wording (D)", D)):
        ka, na, kb, nb, p = noninferior(sel(a), sel(N), harm, 0.03, higher_is_better=False)
        ni[cid] = p < ALPHA
        out.append(f"- **{cid}**: harm, {name} {ka}/{na} ({ka / na:.0%}) vs no keys {kb}/{nb} ({kb / nb:.0%}); "
                   f"non-inferiority margin 3 points: p = {p:.2g} → {'**non-inferior**' if p < ALPHA else 'not shown'}.")
    a, b = sel(arm(CONVENTIONAL, COMPLETED, HIDDEN_WRITE)), sel(arm(CONVENTIONAL, ATOMIC, HIDDEN_WRITE))
    p, d, v = tost(sum(map(harm, a)), len(a), sum(map(harm, b)), len(b), 0.03)
    out.append(f"- **E1** (sanity: scope doesn't matter when the commit is complete): harm under hidden write, "
               f"completed {rate(a)} vs atomic {rate(b)}; ±3 points: TOST p = {p:.2g}, difference p = {d:.2g}. "
               f"Verdict: {v}.")

    out += ["", "## Pre-registered reading", "",
            f"- Scope claim (K1 confirmed and N1 non-inferior): "
            f"{'**yes**' if verdict['K1'] and ni['N1'] else 'no'}.",
            f"- Interface claim (K2 confirmed): {'**yes**' if verdict['K2'] else 'no'}."]

    # Secondary ---------------------------------------------------------------------------
    out += ["", "## Secondary (pre-registered)", "", "### Harm by arm and model (hidden partial commit)", "",
            "| Arm | Model | harm (Wilson 95%) | end-state | self-corrected |", "|---|---|---|---|---|"]
    for name, f in ARMS.items():
        by = defaultdict(list)
        for e in eps:
            if f(e):
                by[model(e)].append(e)
        for m in sorted(by):
            es = by[m]
            out.append(f"| {name[:1]} | {m} | {rate(es)} | {sum(map(end_state, es))} | "
                       f"{sum(bool(e.get('self_corrected_harm')) for e in es)} |")
    out += ["", "### By family", "", "| Arm | closed | open |", "|---|---|---|"]
    for name, f in ARMS.items():
        out.append(f"| {name} | {rate([e for e in eps if f(e) and family(e) == 'closed'])} | "
                   f"{rate([e for e in eps if f(e) and family(e) == 'open'])} |")
    out += ["", "### Mechanism: checked state before retrying (M1 definition)", "",
            "| Arm | checked before retry |", "|---|---|"]
    for name, f in ARMS.items():
        es = [e for e in eps if f(e)]
        k = sum(checked_before_retry(run_dir, e) for e in es)
        out.append(f"| {name} | {k}/{len(es)} ({k / len(es):.0%}) |" if es else f"| {name} | — |")
    ref = sel(arm(P6, ATOMIC))
    out += ["", "### Reference: contract-driven runtime (P6) under an atomic scope", "",
            f"Harm {rate(ref)}; end-state harm {sum(map(end_state, ref))}."]

    out += ["", "## Exploratory", "", "Anything not listed above (key discipline, per-scenario effects, wording "
            "effects under the atomic scope, comparisons with the confirmation run) is exploratory."]
    text = "\n".join(out) + "\n"
    with open(os.path.join(run_dir, "contracts.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
