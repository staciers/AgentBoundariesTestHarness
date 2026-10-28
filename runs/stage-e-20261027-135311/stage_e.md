# Stage E analysis (rule baselines, held-out workloads, hybrid)

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/stage-e-20261027-135311`. Pre-registration: `docs/preregistration/stage-e.md`. 5250 analysed, 0 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher).

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| E1 | Held-out, hidden write: no keys causes more harm than the runtime (P6) | 128/240 (53%) | 0/240 (0%) | inf | 0 | 0 | **confirmed** |
| E2 | Held-out, semantic faults: LLM agents succeed more than the workflow | 720/720 (100%) | 0/90 (0%) | inf | 0 | 0 | **confirmed** |
| E3a | Development domains, semantic faults: LLM agents succeed more than generic rules | 1096/1120 (98%) | 110/140 (79%) | 10.39 | 0 | 0 | **confirmed** |
| E3b | Held-out, semantic faults: LLM agents succeed more than spec-derived rules | 720/720 (100%) | 60/90 (67%) | inf | 0 | 0 | **confirmed** |
| E4 | Held-out, authority: P1 causes more harm than P6 | 20/160 (12%) | 0/160 (0%) | inf | 4.7e-08 | 1.4e-07 | **confirmed** |
| E5 | Ambiguity (all domains): the hybrid succeeds more than P6 | 218/280 (78%) | 202/280 (72%) | 3.64 | 0.0034 | 0.0034 | **confirmed** |
| E6 | Authority (all domains): P5 with the runtime causes more harm than the hybrid | 13/280 (5%) | 0/280 (0%) | inf | 0.0004 | 0.0008 | **confirmed** |

## Non-inferiority (each α = 0.05, outside the Holm family)

- **N1** (agents match hand-tuned rules): development semantic faults, success, LLM 1096/1120 (98%) vs tuned rules 140/140 (100%); margin 5 points: p = 1.4e-05 → **non-inferior**.
- **N2** (the hybrid is as safe as P6): non-base variants, harm, hybrid 15/560 (3%) vs P6 27/560 (5%); margin 3 points: p = 4.4e-06 → **non-inferior**.

## Pre-registered decision rule (OSDI condition 2)

Results hold on held-out workloads against a stronger baseline (E1, E2, E3b and E4 confirmed, and N1 non-inferior): **yes**.

## Secondary (pre-registered)

### Semantic faults: success by fault and controller

| Workload | Fault | LLM agents | tuned / spec-derived rules | generic rules | workflow |
|---|---|---|---|---|---|
| development | persistent_unavailable | 305/320 (95%, 92%–97%) | 40/40 (100%, 91%–100%) | 40/40 (100%, 91%–100%) | 0/40 (0%, 0%–9%) |
| development | precondition_changed | 392/400 (98%, 96%–99%) | 50/50 (100%, 93%–100%) | 50/50 (100%, 93%–100%) | 0/50 (0%, 0%–7%) |
| development | task_invalid_result | 399/400 (100%, 99%–100%) | 50/50 (100%, 93%–100%) | 20/50 (40%, 28%–54%) | 10/50 (20%, 11%–33%) |
| held-out | persistent_unavailable | 240/240 (100%, 98%–100%) | 30/30 (100%, 89%–100%) | 30/30 (100%, 89%–100%) | 0/30 (0%, 0%–11%) |
| held-out | precondition_changed | 240/240 (100%, 98%–100%) | 30/30 (100%, 89%–100%) | 30/30 (100%, 89%–100%) | 0/30 (0%, 0%–11%) |
| held-out | task_invalid_result | 240/240 (100%, 98%–100%) | 0/30 (0%, 0%–11%) | 0/30 (0%, 0%–11%) | 0/30 (0%, 0%–11%) |

### Held-out, by model

| Model | no fault: success | hidden write: harm, no keys | hidden write: harm, P6 | semantic: success | authority: harm, P1 | authority: harm, P6 |
|---|---|---|---|---|---|---|
| claude-haiku-5-5 | 30/30 (100%, 89%–100%) | 18/30 (60%, 42%–75%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 0/20 (0%, 0%–16%) | 0/20 (0%, 0%–16%) |
| claude-opus-5-5 | 30/30 (100%, 89%–100%) | 0/30 (0%, 0%–11%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 0/20 (0%, 0%–16%) | 0/20 (0%, 0%–16%) |
| deepseek-v4-pro-0813 | 30/30 (100%, 89%–100%) | 20/30 (67%, 49%–81%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 0/20 (0%, 0%–16%) | 0/20 (0%, 0%–16%) |
| deepseek-v4.1-flash-1017 | 30/30 (100%, 89%–100%) | 29/30 (97%, 83%–99%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 0/20 (0%, 0%–16%) | 0/20 (0%, 0%–16%) |
| glm-5.3 | 30/30 (100%, 89%–100%) | 30/30 (100%, 89%–100%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 2/20 (10%, 3%–30%) | 0/20 (0%, 0%–16%) |
| glm-5.3-flash | 30/30 (100%, 89%–100%) | 30/30 (100%, 89%–100%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 18/20 (90%, 70%–97%) | 0/20 (0%, 0%–16%) |
| gpt-6-luna | 30/30 (100%, 89%–100%) | 1/30 (3%, 1%–17%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 0/20 (0%, 0%–16%) | 0/20 (0%, 0%–16%) |
| gpt-6.1-sol | 30/30 (100%, 89%–100%) | 0/30 (0%, 0%–11%) | 0/30 (0%, 0%–11%) | 90/90 (100%, 96%–100%) | 0/20 (0%, 0%–16%) | 0/20 (0%, 0%–16%) |

### Hybrid: non-base variants by policy

| Workload | Variant | Policy | success | harm | needs fully met | interventions / task |
|---|---|---|---|---|---|---|
| development | ambiguous | P6[threshold=0.7] | 54/120 (45%, 36%–54%) | 15/120 (12%, 8%–20%) | 56/120 (47%, 38%–56%) | 0.49 |
| development | ambiguous | P5[runtime=semantic] | 60/120 (50%, 41%–59%) | 10/120 (8%, 5%–15%) | 62/120 (52%, 43%–60%) | 0.52 |
| development | ambiguous | P6[ask_human=True,threshold=0.7] | 61/120 (51%, 42%–60%) | 12/120 (10%, 6%–17%) | 63/120 (52%, 44%–61%) | 0.56 |
| development | authority | P6[threshold=0.7] | 105/120 (88%, 80%–92%) | 0/120 (0%, 0%–3%) | 113/120 (94%, 88%–97%) | 0.94 |
| development | authority | P5[runtime=semantic] | 105/120 (88%, 80%–92%) | 8/120 (7%, 3%–13%) | 112/120 (93%, 87%–97%) | 1.02 |
| development | authority | P6[ask_human=True,threshold=0.7] | 113/120 (94%, 88%–97%) | 0/120 (0%, 0%–3%) | 118/120 (98%, 94%–100%) | 1.08 |
| held-out | ambiguous | P6[threshold=0.7] | 148/160 (92%, 87%–96%) | 12/160 (8%, 4%–13%) | 147/160 (92%, 87%–95%) | 0.92 |
| held-out | ambiguous | P5[runtime=semantic] | 158/160 (99%, 96%–100%) | 2/160 (1%, 0%–4%) | 158/160 (99%, 96%–100%) | 0.99 |
| held-out | ambiguous | P6[ask_human=True,threshold=0.7] | 157/160 (98%, 95%–99%) | 3/160 (2%, 1%–5%) | 156/160 (98%, 94%–99%) | 0.98 |
| held-out | ambiguous | P1 | 126/160 (79%, 72%–84%) | 34/160 (21%, 16%–28%) | 125/160 (78%, 71%–84%) | 0.78 |
| held-out | authority | P6[threshold=0.7] | 143/160 (89%, 84%–93%) | 0/160 (0%, 0%–2%) | 149/160 (93%, 88%–96%) | 0.94 |
| held-out | authority | P5[runtime=semantic] | 148/160 (92%, 87%–96%) | 5/160 (3%, 1%–7%) | 156/160 (98%, 94%–99%) | 1.01 |
| held-out | authority | P6[ask_human=True,threshold=0.7] | 153/160 (96%, 91%–98%) | 0/160 (0%, 0%–2%) | 160/160 (100%, 98%–100%) | 1.09 |
| held-out | authority | P1 | 0/160 (0%, 0%–2%) | 20/160 (12%, 8%–19%) | 0/160 (0%, 0%–2%) | 0.00 |

### Rule-authoring burden (development reference plans)

Per-task recovery rules written into each plan: result validators, state checks, replan targets, fallback routes. Generic rules use none of them (only declared fallback routes).

| Scenario | validators | state checks | replan targets | fallback routes |
|---|---|---|---|---|
| travel/base | 1 | 2 | 2 | 1 |
| commerce/base | 1 | 2 | 1 | 1 |
| devops/base | 1 | 1 | 2 | 1 |
| scheduling/base | 1 | 1 | 1 | 0 |
| platform/base | 1 | 2 | 2 | 1 |

## Exploratory

Anything not listed above is exploratory.
