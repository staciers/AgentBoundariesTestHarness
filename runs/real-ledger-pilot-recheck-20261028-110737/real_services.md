# Real-services study analysis (Tier A: the ledger on Postgres)

Run: `runs/real-ledger-pilot-recheck-20261028-110737`. Pre-registration: `docs/preregistration/real-services.md`. 42 analysed, 0 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher). Strata: model.

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| T1 | Real, hidden write: no keys causes more harm than the runtime (P6) | 6/6 (100%) | 0/6 (0%) | inf | 0.0084 | 0.025 | **confirmed** |
| T2 | Real, hidden partial commit: P1 with keys causes more harm than the runtime (P6) | 3/6 (50%) | 0/6 (0%) | inf | 0.14 | 0.27 | not confirmed |
| T3 | Real, hidden partial commit: offering keys causes more harm than not (keys hazard) | 3/6 (50%) | 1/6 (17%) | inf | 0.43 | 0.43 | not confirmed |

## Non-inferiority (α = 0.05, outside the Holm family)

- **N1** (the runtime is as safe on real services as in the simulator): P6 harm under both faults, real 0/12 (0%) vs simulated 0/0 (0%); margin 3 points: p = nan → not shown.

## Pre-registered decision rule

Q1 holds on real services (T1 and T2 confirmed, and N1 non-inferior): **no**.

## Simulator vs real services (pre-registered TOST, each α = 0.05)

Harm with the agent recovering on its own, pooled over models (same models, seeds and arms on both substrates). Equivalent = within ±10%.

| Arm | Real | Simulated | Real − simulated | TOST p | Difference p | Verdict |
|---|---|---|---|---|---|---|

## Secondary (pre-registered)

### Harm and success by arm and substrate

| Arm | Real: harm | Simulated: harm | Real: success | Simulated: success |
|---|---|---|---|---|
| no fault, P1 | 0/6 (0%, 0%–39%) | — | 6/6 (100%, 61%–100%) | — |
| visibility lag only, P1 | 0/6 (0%, 0%–39%) | — | 6/6 (100%, 61%–100%) | — |
| hidden write, no keys | 6/6 (100%, 61%–100%) | — | 0/6 (0%, 0%–39%) | — |
| partial commit, keys | 3/6 (50%, 19%–81%) | — | 3/6 (50%, 19%–81%) | — |
| partial commit, no keys | 1/6 (17%, 3%–56%) | — | 5/6 (83%, 44%–97%) | — |
| hidden write, P6 | 0/6 (0%, 0%–39%) | — | 6/6 (100%, 61%–100%) | — |
| partial commit, P6 | 0/6 (0%, 0%–39%) | — | 6/6 (100%, 61%–100%) | — |

### Harm by model (real / simulated)

| Model | no fault, P1 | visibility lag only, P1 | hidden write, no keys | partial commit, keys | partial commit, no keys | hidden write, P6 | partial commit, P6 |
|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 0/3 / 0/0 | 0/3 / 0/0 | 3/3 / 0/0 | 0/3 / 0/0 | 0/3 / 0/0 | 0/3 / 0/0 | 0/3 / 0/0 |
| glm-5.3-flash | 0/3 / 0/0 | 0/3 / 0/0 | 3/3 / 0/0 | 3/3 / 0/0 | 1/3 / 0/0 | 0/3 / 0/0 | 0/3 / 0/0 |

### The runtime against real replication lag (P6, real)

Reconcile lookups on the faulted payment, and whether a completed payment was found. Hidden write: the simulator finds it on the 4th of 4 lookups; not found means replication outran the poll budget. Partial commit: there is no completed payment to find, so the runtime compensates instead.

| Fault | Lookups | Found | Episodes |
|---|---|---|---|
| partial commit | 4 | False | 6 |
| hidden write | 4 | True | 6 |

### Episode duration (s): wall clock for real, simulated clock for the simulator

| Substrate | Arm | median | p90 |
|---|---|---|---|
| ledger_real | no fault, P1 | 8.1 | 9.1 |
| ledger_real | visibility lag only, P1 | 6.2 | 6.5 |
| ledger_real | hidden write, no keys | 16.9 | 26.0 |
| ledger_real | partial commit, keys | 12.6 | 15.1 |
| ledger_real | partial commit, no keys | 12.4 | 13.1 |
| ledger_real | hidden write, P6 | 17.1 | 22.7 |
| ledger_real | partial commit, P6 | 17.7 | 20.2 |

### Fault audit (proxy log for this run)

Responses the proxy withheld: 30; timeouts the injector requested: 30. Partial commits the proxy forwarded: 18; requested: 18. **Match.**

## Exploratory

Anything not listed above is exploratory.
