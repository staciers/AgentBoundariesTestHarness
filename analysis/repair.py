"""Pre-registered analysis for the repair study (contract-declared repair of partial commits).

    .venv/bin/python analysis/repair.py runs/<repair-run>

Implements exactly the tests in docs/preregistration/repair.md. Freeze with the
pre-registration commit; add new analyses only to the exploratory section.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

from statsmodels.stats.multitest import multipletests

sys.path.insert(0, ".")
from abh.metrics import load_episodes  # noqa: E402
from analysis.confirmatory import stratified, wilson  # noqa: E402  (frozen helpers)
from analysis.stage_b import noninferior  # noqa: E402  (frozen helper)

PARTIAL = "partial_mutation+timeout_after_execution"
GENERATED, NO_KEYS, P6 = "P1[key_description=contract]", "P1[expose_keys=False]", "P6[threshold=0.7]"
NONE_ = "key_scope=atomic"
PROSE = "key_scope=atomic,repair=prose"
PRIMITIVE = "key_scope=atomic,partial_report=True,repair=cancel_partial"
ALPHA = 0.05
OPEN_PROVIDERS = {"together", "fireworks", "deepinfra", "openrouter", "deepseek", "zai"}
REPLAYED = "already failed partway"


def model(e):
    return e["agent"].split(":", 1)[1].split("@")[0]


def family(e):
    return "open" if e["agent"].split(":")[0] in OPEN_PROVIDERS else "closed"


harm = lambda e: bool(e["harm"])
ms = lambda e: (model(e), e["scenario"])
dup = lambda e: e["duplicate_effects"] > 0 or e.get("transient_duplicate_effects", 0) > 0


def arm(policy, contract):
    return lambda e: e["policy"] == policy and e["contract"] == contract and e["faults"] == PARTIAL


ARMS = {"D: no repair guidance": arm(GENERATED, NONE_),
        "D1: repair-aware wording": arm(GENERATED, PROSE),
        "D2: partial report + cancel_partial": arm(GENERATED, PRIMITIVE),
        "N: no keys": arm(NO_KEYS, "default")}


def rate(es, f=harm):
    k, n = sum(map(f, es)), len(es)
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({k / n:.0%}, {lo:.0%}–{hi:.0%})" if n else "—"


def trace_facts(run_dir: str, e: dict) -> dict:
    """From the saved trace: did a keyed request get its partial outcome replayed, did the agent
    then resend that tool with a different (or no) key, and did it call cancel_partial?"""
    path = os.path.join(run_dir, "traces", f"{e['key']}.json")
    out = {"replayed": False, "new_key_resend": False, "used_cancel": False}
    if not os.path.exists(path):
        return out
    with open(path) as f:
        evs = json.load(f)["trace"]
    replayed = {}  # tool -> key whose partial outcome was replayed
    for ev in evs:
        if ev.get("event") == "runtime_outcome" and REPLAYED in str(ev.get("error_message") or ""):
            replayed[ev.get("tool")] = ev.get("idempotency_key")
            out["replayed"] = True
        elif ev.get("event") == "agent_call":
            tool, args = ev.get("tool"), ev.get("args") or {}
            if tool == "cancel_partial":
                out["used_cancel"] = True
            elif tool in replayed and args.get("idempotency_key") != replayed[tool]:
                out["new_key_resend"] = True
    return out


def main(run_dir: str) -> None:
    rows = load_episodes(os.path.join(run_dir, "episodes.jsonl"))
    eps = [e for e in rows if "error" not in e and not (e.get("agent_error") and
                                                         not str(e["agent_error"]).startswith("refusal"))]
    D, D1, D2, N = ARMS.values()
    fam = [
        ("R1", "Repair primitives reduce harm vs no repair guidance: D > D2", stratified(eps, D, D2, harm, ms)),
        ("R2", "Repair-aware wording reduces harm vs no repair guidance: D > D1", stratified(eps, D, D1, harm, ms)),
        ("R3", "Primitives beat wording: D1 > D2", stratified(eps, D1, D2, harm, ms)),
    ]
    holm = multipletests([r["p"] for _, _, r in fam], alpha=ALPHA, method="holm")[1]
    out = ["# Repair study analysis (contract-declared repair of partial commits)", "",
           f"Run: `{run_dir}`. Pre-registration: `docs/preregistration/repair.md`. {len(eps)} analysed, "
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

    sel = lambda f: [e for e in eps if f(e)]
    ka, na, kb, nb, p = noninferior(sel(D2), sel(N), harm, 0.03, higher_is_better=False)
    ni = p < ALPHA
    out += ["", "## Non-inferiority (α = 0.05, outside the Holm family)", "",
            f"- **N4**: harm, D2 {ka}/{na} ({ka / na:.0%}) vs no keys {kb}/{nb} ({kb / nb:.0%}); non-inferiority "
            f"margin 3 points: p = {p:.2g} → {'**non-inferior**' if ni else 'not shown'}."]
    out += ["", "## Pre-registered reading", "",
            f"- Primitive claim (R1 confirmed and N4 non-inferior): {'**yes**' if verdict['R1'] and ni else 'no'}.",
            f"- Wording claim (R2 confirmed): {'**yes**' if verdict['R2'] else 'no'}."]

    # Secondary ---------------------------------------------------------------------------
    facts = {e["key"]: trace_facts(run_dir, e) for e in eps if any(f(e) for f in ARMS.values())}
    out += ["", "## Secondary (pre-registered)", "", "### By arm and family", "",
            "| Arm | harm, closed | harm, open | duplicate-effect episodes | partial outcome replayed | "
            "resent with a new key after a replay | used cancel_partial |", "|---|---|---|---|---|---|---|"]
    for name, f in ARMS.items():
        es = sel(f)
        fr = lambda k: sum(facts[e["key"]][k] for e in es)
        out.append(f"| {name} | {rate([e for e in es if family(e) == 'closed'])} | "
                   f"{rate([e for e in es if family(e) == 'open'])} | {sum(map(dup, es))} | {fr('replayed')} | "
                   f"{fr('new_key_resend')} | {fr('used_cancel')} |")
    out += ["", "### Harm by arm, model and scenario", "", "| Arm | Model | travel | commerce | platform |",
            "|---|---|---|---|---|"]
    for name, f in ARMS.items():
        by = defaultdict(lambda: defaultdict(list))
        for e in sel(f):
            by[model(e)][e["scenario"].split("/")[0]].append(e)
        for m in sorted(by):
            out.append(f"| {name[:2].rstrip(':')} | {m} | " +
                       " | ".join(rate(by[m][d]) for d in ("travel", "commerce", "platform")) + " |")
    ref = sel(arm(P6, PRIMITIVE))
    out += ["", "### Reference: runtime (P6) with the repair contract", "", f"Harm {rate(ref)}."]
    out += ["", "## Exploratory", "", "Anything not listed above is exploratory."]
    text = "\n".join(out) + "\n"
    with open(os.path.join(run_dir, "repair.md"), "w") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
