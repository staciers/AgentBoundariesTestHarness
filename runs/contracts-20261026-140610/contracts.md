# Contract study analysis (key scope × key description)

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/contracts-20261026-140610`. Pre-registration: `docs/preregistration/contracts.md`. 3920 analysed, 560 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher). Outcome: harm.

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| K1 | Scope: an atomic key scope removes the hazard ('at most once' wording): A > C | 116/630 (18%) | 45/630 (7%) | 3.09 | 5.8e-11 | 5.8e-11 | **confirmed** |
| K2 | Wording: contract-generated descriptions reduce harm (completed scope): A > B | 116/630 (18%) | 31/630 (5%) | 4.65 | 1.1e-16 | 2.2e-16 | **confirmed** |
| K3 | Replication of C3 on fresh seeds, all 8 models: A > N | 116/630 (18%) | 24/630 (4%) | 5.57 | 0 | 0 | **confirmed** |

## Non-inferiority and equivalence (each α = 0.05, outside the Holm family)

- **N1**: harm, atomic scope, 'at most once' wording (C) 45/630 (7%) vs no keys 24/630 (4%); non-inferiority margin 3 points: p = 0.6 → not shown.
- **N2**: harm, atomic scope, contract wording (D) 119/630 (19%) vs no keys 24/630 (4%); non-inferiority margin 3 points: p = 1 → not shown.
- **E1** (sanity: scope doesn't matter when the commit is complete): harm under hidden write, completed 87/280 (31%, 26%–37%) vs atomic 86/280 (31%, 26%–36%); ±3 points: TOST p = 0.25, difference p = 0.93. Verdict: inconclusive.

## Pre-registered reading

- Scope claim (K1 confirmed and N1 non-inferior): no.
- Interface claim (K2 confirmed): **yes**.

## Secondary (pre-registered)

### Harm by arm and model (hidden partial commit)

| Arm | Model | harm (Wilson 95%) | end-state | self-corrected |
|---|---|---|---|---|
| A | claude-haiku-5-5 | 24/90 (27%, 19%–37%) | 14 | 10 |
| A | claude-opus-5-5 | 3/90 (3%, 1%–9%) | 0 | 3 |
| A | deepseek-v4-pro-0813 | 9/90 (10%, 5%–18%) | 9 | 0 |
| A | glm-5.3 | 9/90 (10%, 5%–18%) | 1 | 8 |
| A | glm-5.3-flash | 6/90 (7%, 3%–14%) | 3 | 3 |
| A | gpt-6-luna | 47/90 (52%, 42%–62%) | 37 | 10 |
| A | gpt-6.1-sol | 18/90 (20%, 13%–29%) | 0 | 18 |
| B | claude-haiku-5-5 | 3/90 (3%, 1%–9%) | 3 | 0 |
| B | claude-opus-5-5 | 0/90 (0%, 0%–4%) | 0 | 0 |
| B | deepseek-v4-pro-0813 | 21/90 (23%, 16%–33%) | 21 | 0 |
| B | glm-5.3 | 2/90 (2%, 1%–8%) | 2 | 0 |
| B | glm-5.3-flash | 5/90 (6%, 2%–12%) | 4 | 1 |
| B | gpt-6-luna | 0/90 (0%, 0%–4%) | 0 | 0 |
| B | gpt-6.1-sol | 0/90 (0%, 0%–4%) | 0 | 0 |
| C | claude-haiku-5-5 | 16/90 (18%, 11%–27%) | 16 | 0 |
| C | claude-opus-5-5 | 0/90 (0%, 0%–4%) | 0 | 0 |
| C | deepseek-v4-pro-0813 | 12/90 (13%, 8%–22%) | 12 | 0 |
| C | glm-5.3 | 12/90 (13%, 8%–22%) | 8 | 4 |
| C | glm-5.3-flash | 4/90 (4%, 2%–11%) | 4 | 0 |
| C | gpt-6-luna | 1/90 (1%, 0%–6%) | 1 | 0 |
| C | gpt-6.1-sol | 0/90 (0%, 0%–4%) | 0 | 0 |
| D | claude-haiku-5-5 | 30/90 (33%, 24%–44%) | 30 | 0 |
| D | claude-opus-5-5 | 0/90 (0%, 0%–4%) | 0 | 0 |
| D | deepseek-v4-pro-0813 | 28/90 (31%, 22%–41%) | 28 | 0 |
| D | glm-5.3 | 27/90 (30%, 22%–40%) | 13 | 14 |
| D | glm-5.3-flash | 34/90 (38%, 28%–48%) | 18 | 16 |
| D | gpt-6-luna | 0/90 (0%, 0%–4%) | 0 | 0 |
| D | gpt-6.1-sol | 0/90 (0%, 0%–4%) | 0 | 0 |
| N | claude-haiku-5-5 | 1/90 (1%, 0%–6%) | 1 | 0 |
| N | claude-opus-5-5 | 0/90 (0%, 0%–4%) | 0 | 0 |
| N | deepseek-v4-pro-0813 | 9/90 (10%, 5%–18%) | 9 | 0 |
| N | glm-5.3 | 1/90 (1%, 0%–6%) | 1 | 0 |
| N | glm-5.3-flash | 12/90 (13%, 8%–22%) | 12 | 0 |
| N | gpt-6-luna | 1/90 (1%, 0%–6%) | 1 | 0 |
| N | gpt-6.1-sol | 0/90 (0%, 0%–4%) | 0 | 0 |

### By family

| Arm | closed | open |
|---|---|---|
| A: completed scope, 'at most once' wording | 92/360 (26%, 21%–30%) | 24/270 (9%, 6%–13%) |
| B: completed scope, contract wording | 3/360 (1%, 0%–2%) | 28/270 (10%, 7%–15%) |
| C: atomic scope, 'at most once' wording | 17/360 (5%, 3%–7%) | 28/270 (10%, 7%–15%) |
| D: atomic scope, contract wording | 30/360 (8%, 6%–12%) | 89/270 (33%, 28%–39%) |
| N: no keys | 2/360 (1%, 0%–2%) | 22/270 (8%, 5%–12%) |

### Mechanism: checked state before retrying (M1 definition)

| Arm | checked before retry |
|---|---|
| A: completed scope, 'at most once' wording | 555/630 (88%) |
| B: completed scope, contract wording | 624/630 (99%) |
| C: atomic scope, 'at most once' wording | 570/630 (90%) |
| D: atomic scope, contract wording | 326/630 (52%) |
| N: no keys | 617/630 (98%) |

### Reference: contract-driven runtime (P6) under an atomic scope

Harm 0/210 (0%, 0%–2%); end-state harm 0.

## Exploratory

Anything not listed above (key discipline, per-scenario effects, wording effects under the atomic scope, comparisons with the confirmation run) is exploratory.
