# Contract study analysis (key scope × key description)

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/contracts-supplement-20261027-090006`. Pre-registration: `docs/preregistration/contracts.md`. 560 analysed, 0 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher). Outcome: harm.

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| K1 | Scope: an atomic key scope removes the hazard ('at most once' wording): A > C | 1/90 (1%) | 1/90 (1%) | 1.00 | 0.48 | 1 | not confirmed |
| K2 | Wording: contract-generated descriptions reduce harm (completed scope): A > B | 1/90 (1%) | 2/90 (2%) | 0.49 | 1 | 1 | not confirmed |
| K3 | Replication of C3 on fresh seeds, all 8 models: A > N | 1/90 (1%) | 0/90 (0%) | inf | 1 | 1 | not confirmed |

## Non-inferiority and equivalence (each α = 0.05, outside the Holm family)

- **N1**: harm, atomic scope, 'at most once' wording (C) 1/90 (1%) vs no keys 0/90 (0%); non-inferiority margin 3 points: p = 0.15 → not shown.
- **N2**: harm, atomic scope, contract wording (D) 2/90 (2%) vs no keys 0/90 (0%); non-inferiority margin 3 points: p = 0.35 → not shown.
- **E1** (sanity: scope doesn't matter when the commit is complete): harm under hidden write, completed 2/40 (5%, 1%–17%) vs atomic 0/40 (0%, 0%–9%); ±3 points: TOST p = 0.65, difference p = 0.3. Verdict: inconclusive.

## Pre-registered reading

- Scope claim (K1 confirmed and N1 non-inferior): no.
- Interface claim (K2 confirmed): no.

## Secondary (pre-registered)

### Harm by arm and model (hidden partial commit)

| Arm | Model | harm (Wilson 95%) | end-state | self-corrected |
|---|---|---|---|---|
| A | deepseek-v4.1-flash-1017 | 1/90 (1%, 0%–6%) | 1 | 0 |
| B | deepseek-v4.1-flash-1017 | 2/90 (2%, 1%–8%) | 2 | 0 |
| C | deepseek-v4.1-flash-1017 | 1/90 (1%, 0%–6%) | 1 | 0 |
| D | deepseek-v4.1-flash-1017 | 2/90 (2%, 1%–8%) | 1 | 1 |
| N | deepseek-v4.1-flash-1017 | 0/90 (0%, 0%–4%) | 0 | 0 |

### By family

| Arm | closed | open |
|---|---|---|
| A: completed scope, 'at most once' wording | — | 1/90 (1%, 0%–6%) |
| B: completed scope, contract wording | — | 2/90 (2%, 1%–8%) |
| C: atomic scope, 'at most once' wording | — | 1/90 (1%, 0%–6%) |
| D: atomic scope, contract wording | — | 2/90 (2%, 1%–8%) |
| N: no keys | — | 0/90 (0%, 0%–4%) |

### Mechanism: checked state before retrying (M1 definition)

| Arm | checked before retry |
|---|---|
| A: completed scope, 'at most once' wording | 88/90 (98%) |
| B: completed scope, contract wording | 86/90 (96%) |
| C: atomic scope, 'at most once' wording | 89/90 (99%) |
| D: atomic scope, contract wording | 53/90 (59%) |
| N: no keys | 89/90 (99%) |

### Reference: contract-driven runtime (P6) under an atomic scope

Harm 0/30 (0%, 0%–11%); end-state harm 0.

## Exploratory

Anything not listed above (key discipline, per-scenario effects, wording effects under the atomic scope, comparisons with the confirmation run) is exploratory.
