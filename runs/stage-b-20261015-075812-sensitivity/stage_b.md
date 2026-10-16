# Stage B analysis (human escalation)

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/stage-b-20261015-075812-sensitivity/`. Pre-registration: `docs/preregistration/stage-b.md`. 7920 analysed, 0 excluded. Policy shorthand: P3 and P6 at threshold 0.7.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher).

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| B1 | H3: P6 succeeds more than P1 where a human is needed (ambiguous/authority) | 310/480 (65%) | 88/480 (18%) | 17.65 | 0 | 0 | **confirmed** |
| B2 | H7: P2 escalates unnecessarily more often than P6 | 567/720 (79%) | 4/720 (1%) | inf | 0 | 0 | **confirmed** |
| B4 | H4: P6 completes more tasks autonomously than P4 (static risk HITL) | 243/720 (34%) | 91/720 (13%) | inf | 0 | 0 | **confirmed** |
| B5 | H3/H4: confidence-only HITL (P3) causes more harm than P6 at the same threshold | 280/720 (39%) | 31/720 (4%) | 34.20 | 0 | 0 | **confirmed** |
| B6 | RQ3: P6 meets the human needs that agent-selected HITL (P5) misses | 322/480 (67%) | 347/480 (72%) | 0.44 | 0.0011 | 0.0011 | not confirmed |

## Non-inferiority and equivalence (each α = 0.05, outside the Holm family)

- **N1** (H7, recall kept): human needs fully met, P6 322/480 (67%) vs P2 448/480 (93%); non-inferiority margin 10 points: p = 1 → not shown.
- **N2** (H4, no added risk): harm, P6 31/720 (4%) vs P4 118/720 (16%); non-inferiority margin 5 points: p = 1.8e-27 → **non-inferior**.
- **E1** (H3, no value where no human is needed): success in `base` variants, P6 240/240 vs P1 218/240; ±5 points: TOST p = 0.98, difference p = 2.5e-06. Verdict: **different**.

## Secondary (pre-registered)

### Per policy (all models, both fault conditions)

| Policy | success | harm | autonomous coverage | autonomous risk | interventions / task | precision | needs fully met (non-base) | human wait min / task |
|---|---|---|---|---|---|---|---|---|
| ORACLE | 94% | 0% | 34% | 9% | 0.67 | 100% | 95% | 1.4 |
| P1 | 42% | 15% | 31% | 65% | 0.13 | 100% | 19% | 0.2 |
| P2 | 82% | 9% | 0% | 100% | 2.68 | 33% | 93% | 5.9 |
| P3[threshold=0.5] | 43% | 40% | 31% | 63% | 0.20 | 63% | 19% | 0.4 |
| P3[threshold=0.7] | 44% | 39% | 31% | 62% | 0.41 | 34% | 21% | 0.8 |
| P3[threshold=0.9] | 55% | 30% | 28% | 54% | 0.97 | 32% | 43% | 1.8 |
| P4 | 64% | 16% | 13% | 65% | 1.01 | 54% | 66% | 1.9 |
| P5 | 71% | 13% | 30% | 41% | 0.49 | 98% | 72% | 0.9 |
| P6[threshold=0.5] | 76% | 4% | 34% | 39% | 0.44 | 100% | 66% | 0.8 |
| P6[threshold=0.7] | 76% | 4% | 34% | 39% | 0.45 | 99% | 67% | 0.8 |
| P6[threshold=0.9] | 80% | 3% | 32% | 36% | 0.55 | 90% | 73% | 1.0 |

### Risk–coverage points (H4): P3 and P6 threshold sweeps, P4, ORACLE

| Policy | autonomous coverage | autonomous risk | success |
|---|---|---|---|
| ORACLE | 34% | 9% | 94% |
| P3[threshold=0.5] | 31% | 63% | 43% |
| P3[threshold=0.7] | 31% | 62% | 44% |
| P3[threshold=0.9] | 28% | 54% | 55% |
| P4 | 13% | 65% | 64% |
| P6[threshold=0.5] | 34% | 39% | 76% |
| P6[threshold=0.7] | 34% | 39% | 76% |
| P6[threshold=0.9] | 32% | 36% | 80% |

### Execution-aware escalation (H7): interventions per task, hidden write vs no fault

| Policy | no fault | hidden write |
|---|---|---|
| ORACLE | 0.67 | 0.67 |
| P1 | 0.13 | 0.12 |
| P2 | 2.22 | 3.15 |
| P3[threshold=0.5] | 0.17 | 0.24 |
| P3[threshold=0.7] | 0.46 | 0.35 |
| P3[threshold=0.9] | 0.81 | 1.12 |
| P4 | 0.83 | 1.18 |
| P5 | 0.49 | 0.50 |
| P6[threshold=0.5] | 0.44 | 0.44 |
| P6[threshold=0.7] | 0.46 | 0.44 |
| P6[threshold=0.9] | 0.55 | 0.54 |

### By model family (P6 at 0.7)

| Family | success | harm | needs fully met (non-base) |
|---|---|---|---|
| closed | 78% | 3% | 70% |
| open | 75% | 5% | 65% |

## Exploratory

Anything not listed above (per-model comparisons, confidence calibration, gate reliance) is exploratory.
