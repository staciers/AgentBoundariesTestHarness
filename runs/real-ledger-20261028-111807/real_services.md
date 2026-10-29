# Real-services study analysis (Tier A: the ledger on Postgres)

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/real-ledger-20261028-111807`. Pre-registration: `docs/preregistration/real-services.md`. 2520 analysed, 0 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher). Strata: model.

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| T1 | Real, hidden write: no keys causes more harm than the runtime (P6) | 125/180 (69%) | 0/180 (0%) | inf | 0 | 0 | **confirmed** |
| T2 | Real, hidden partial commit: P1 with keys causes more harm than the runtime (P6) | 49/180 (27%) | 0/180 (0%) | inf | 0 | 0 | **confirmed** |
| T3 | Real, hidden partial commit: offering keys causes more harm than not (keys hazard) | 49/180 (27%) | 35/180 (19%) | 3.04 | 0.01 | 0.01 | **confirmed** |

## Non-inferiority (α = 0.05, outside the Holm family)

- **N1** (the runtime is as safe on real services as in the simulator): P6 harm under both faults, real 0/360 (0%) vs simulated 0/360 (0%); margin 3 points: p = 7.4e-15 → **non-inferior**.

## Pre-registered decision rule

Q1 holds on real services (T1 and T2 confirmed, and N1 non-inferior): **yes**.

## Simulator vs real services (pre-registered TOST, each α = 0.05)

Harm with the agent recovering on its own, pooled over models (same models, seeds and arms on both substrates). Equivalent = within ±10%.

| Arm | Real | Simulated | Real − simulated | TOST p | Difference p | Verdict |
|---|---|---|---|---|---|---|
| no fault, P1 | 0/180 (0%, 0%–2%) | 0/180 (0%, 0%–2%) | +0 pts | 2.1e-38 | 1 | **equivalent** |
| visibility lag only, P1 | 0/180 (0%, 0%–2%) | 0/180 (0%, 0%–2%) | +0 pts | 2.1e-38 | 1 | **equivalent** |
| hidden write, no keys | 125/180 (69%, 62%–76%) | 82/180 (46%, 38%–53%) | +24 pts | 1 | 2.7e-06 | **different** |
| partial commit, keys | 49/180 (27%, 21%–34%) | 48/180 (27%, 21%–34%) | +1 pts | 0.021 | 0.91 | **equivalent** |
| partial commit, no keys | 35/180 (19%, 14%–26%) | 32/180 (18%, 13%–24%) | +2 pts | 0.021 | 0.69 | **equivalent** |

## Secondary (pre-registered)

### Harm and success by arm and substrate

| Arm | Real: harm | Simulated: harm | Real: success | Simulated: success |
|---|---|---|---|---|
| no fault, P1 | 0/180 (0%, 0%–2%) | 0/180 (0%, 0%–2%) | 180/180 (100%, 98%–100%) | 180/180 (100%, 98%–100%) |
| visibility lag only, P1 | 0/180 (0%, 0%–2%) | 0/180 (0%, 0%–2%) | 180/180 (100%, 98%–100%) | 180/180 (100%, 98%–100%) |
| hidden write, no keys | 125/180 (69%, 62%–76%) | 82/180 (46%, 38%–53%) | 55/180 (31%, 24%–38%) | 98/180 (54%, 47%–62%) |
| partial commit, keys | 49/180 (27%, 21%–34%) | 48/180 (27%, 21%–34%) | 131/180 (73%, 66%–79%) | 132/180 (73%, 66%–79%) |
| partial commit, no keys | 35/180 (19%, 14%–26%) | 32/180 (18%, 13%–24%) | 145/180 (81%, 74%–86%) | 148/180 (82%, 76%–87%) |
| hidden write, P6 | 0/180 (0%, 0%–2%) | 0/180 (0%, 0%–2%) | 180/180 (100%, 98%–100%) | 180/180 (100%, 98%–100%) |
| partial commit, P6 | 0/180 (0%, 0%–2%) | 0/180 (0%, 0%–2%) | 180/180 (100%, 98%–100%) | 180/180 (100%, 98%–100%) |

### Harm by model (real / simulated)

| Model | no fault, P1 | visibility lag only, P1 | hidden write, no keys | partial commit, keys | partial commit, no keys | hidden write, P6 | partial commit, P6 |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0/30 / 0/30 | 0/30 / 0/30 | 30/30 / 23/30 | 0/30 / 1/30 | 1/30 / 1/30 | 0/30 / 0/30 | 0/30 / 0/30 |
| claude-opus-5-5 | 0/30 / 0/30 | 0/30 / 0/30 | 15/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 |
| deepseek-v4.1-flash-1017 | 0/30 / 0/30 | 0/30 / 0/30 | 30/30 / 28/30 | 1/30 / 0/30 | 0/30 / 1/30 | 0/30 / 0/30 | 0/30 / 0/30 |
| glm-5.3-flash | 0/30 / 0/30 | 0/30 / 0/30 | 30/30 / 27/30 | 26/30 / 26/30 | 24/30 / 25/30 | 0/30 / 0/30 | 0/30 / 0/30 |
| gpt-6-luna | 0/30 / 0/30 | 0/30 / 0/30 | 20/30 / 4/30 | 22/30 / 21/30 | 10/30 / 5/30 | 0/30 / 0/30 | 0/30 / 0/30 |
| gpt-6.1-sol | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 | 0/30 / 0/30 |

### The runtime against real replication lag (P6, real)

Reconcile lookups on the faulted payment, and whether a completed payment was found. Hidden write: the simulator finds it on the 4th of 4 lookups; not found means replication outran the poll budget. Partial commit: there is no completed payment to find, so the runtime compensates instead.

| Fault | Lookups | Found | Episodes |
|---|---|---|---|
| partial commit | 4 | False | 180 |
| hidden write | 4 | False | 1 |
| hidden write | 4 | True | 179 |

### Episode duration (s): wall clock for real, simulated clock for the simulator

| Substrate | Arm | median | p90 |
|---|---|---|---|
| ledger_real | no fault, P1 | 6.7 | 10.8 |
| ledger | no fault, P1 | 8.5 | 12.2 |
| ledger_real | visibility lag only, P1 | 7.4 | 16.9 |
| ledger | visibility lag only, P1 | 9.5 | 17.4 |
| ledger_real | hidden write, no keys | 15.6 | 24.1 |
| ledger | hidden write, no keys | 47.7 | 52.9 |
| ledger_real | partial commit, keys | 12.8 | 17.6 |
| ledger | partial commit, keys | 42.4 | 47.5 |
| ledger_real | partial commit, no keys | 12.4 | 17.0 |
| ledger | partial commit, no keys | 42.9 | 46.6 |
| ledger_real | hidden write, P6 | 16.3 | 20.3 |
| ledger | hidden write, P6 | 45.4 | 49.2 |
| ledger_real | partial commit, P6 | 19.0 | 23.2 |
| ledger | partial commit, P6 | 50.6 | 54.1 |

### Fault audit (proxy log for this run)

Responses the proxy withheld: 900; timeouts the injector requested: 900. Partial commits the proxy forwarded: 540; requested: 540. **Match.**

## Exploratory

Anything not listed above is exploratory.
