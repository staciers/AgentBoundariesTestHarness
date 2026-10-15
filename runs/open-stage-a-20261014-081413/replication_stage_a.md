# Open-weight replication: Stage A design

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/open-stage-a-20261014-081413/`. Pre-registration: `docs/preregistration/open-replications.md`. 4690 analysed, 0 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher).

| ID | Hypothesis (original) | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| OA1 | A1: LLM > workflow success on semantic faults (semantic runtime) | 550/560 (98%) | 10/140 (7%) | inf | 0 | 0 | **replicated** |
| OA2 | A2: workflow > LLM harm on semantic faults (semantic runtime) | 30/140 (21%) | 0/560 (0%) | inf | 0 | 0 | **replicated** |
| OA3 | A3: no runtime > semantic runtime harm on execution faults | 74/880 (8%) | 0/880 (0%) | inf | 0 | 0 | **replicated** |

## Equivalence (TOST, α = 0.05 each)

- **OE1** (= E1): execution faults, semantic runtime, LLM 880/880 vs workflow 440/440, ±5 points: TOST p = 1.5e-83, difference p = 0.66. Verdict: **equivalent**.
- **OE2** (= E2): semantic faults, LLM, semantic runtime 550/560 vs none 548/560, ±10 points: TOST p = 2.4e-29, difference p = 0.68. Verdict: **equivalent**.

## Secondary (pre-registered)

### Controller × fault class (semantic runtime)

| Fault class | Controller | success | harm |
|---|---|---|---|
| execution | deepseek-v4-flash-0731 | 220/220 (100%) | 0/220 (0%) |
| execution | deepseek-v4-pro-0813 | 220/220 (100%) | 0/220 (0%) |
| execution | glm-5.3 | 220/220 (100%) | 0/220 (0%) |
| execution | glm-5.3-flash | 220/220 (100%) | 0/220 (0%) |
| execution | workflow | 440/440 (100%) | 0/440 (0%) |
| semantic | deepseek-v4-flash-0731 | 140/140 (100%) | 0/140 (0%) |
| semantic | deepseek-v4-pro-0813 | 131/140 (94%) | 0/140 (0%) |
| semantic | glm-5.3 | 140/140 (100%) | 0/140 (0%) |
| semantic | glm-5.3-flash | 139/140 (99%) | 0/140 (0%) |
| semantic | workflow | 10/140 (7%) | 30/140 (21%) |

### Runtime factor on execution faults

| Runtime | Model | success | harm | failures exposed | model calls |
|---|---|---|---|---|---|
| naive_retry | deepseek-v4-flash-0731 | 182/220 | 38/220 | 0.27 | 4.49 |
| naive_retry | deepseek-v4-pro-0813 | 154/220 | 65/220 | 0.30 | 4.20 |
| naive_retry | glm-5.3 | 192/220 | 27/220 | 0.26 | 4.38 |
| naive_retry | glm-5.3-flash | 188/220 | 32/220 | 0.25 | 4.38 |
| none | deepseek-v4-flash-0731 | 202/220 | 18/220 | 0.82 | 5.25 |
| none | deepseek-v4-pro-0813 | 188/220 | 32/220 | 0.86 | 5.03 |
| none | glm-5.3 | 211/220 | 7/220 | 0.80 | 5.12 |
| none | glm-5.3-flash | 203/220 | 17/220 | 0.82 | 5.25 |
| semantic | deepseek-v4-flash-0731 | 220/220 | 0/220 | 0.00 | 4.26 |
| semantic | deepseek-v4-pro-0813 | 220/220 | 0/220 | 0.00 | 4.00 |
| semantic | glm-5.3 | 220/220 | 0/220 | 0.00 | 4.13 |
| semantic | glm-5.3-flash | 220/220 | 0/220 | 0.01 | 4.21 |

### Failure ownership (RQ1)

| fault | policy | agent | n | resolved_by_runtime | resolved_by_agent | resolved_by_human | success | harm |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 0.400 | 0.600 |
| duplicate_execution | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 0.200 | 0.800 |
| duplicate_execution | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 0.600 | 0.400 |
| duplicate_execution | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 0.720 | 0.280 |
| duplicate_execution | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 0.520 | 0.480 |
| duplicate_execution | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 0.200 | 0.800 |
| duplicate_execution | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 0.640 | 0.360 |
| duplicate_execution | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 0.720 | 0.280 |
| duplicate_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 0.960 | 0.040 |
| malformed_response | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 0.760 | 0.240 |
| malformed_response | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| malformed_response | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.600 | 0.400 | 0.000 | 0.760 | 0.240 |
| malformed_response | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 24 | 0.625 | 0.375 | 0.000 | 0.375 | 0.625 |
| malformed_response | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.720 | 0.280 | 0.000 | 0.800 | 0.200 |
| malformed_response | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.640 | 0.360 | 0.000 | 0.880 | 0.120 |
| malformed_response | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | together:deepseek-v4-flash-0731@high | 20 | 0.000 | 1.000 | 0.000 | 0.950 | 0.050 |
| partial_mutation | P1 | together:deepseek-v4-pro-0813@high | 20 | 0.000 | 1.000 | 0.000 | 0.950 | 0.050 |
| partial_mutation | P1 | together:glm-5.3-flash@high | 20 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | together:glm-5.3@high | 19 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=naive_retry] | together:glm-5.3@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=semantic] | scripted:workflow | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:glm-5.3-flash@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:glm-5.3@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1 | together:deepseek-v4-flash-0731@high | 92 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1 | together:deepseek-v4-pro-0813@high | 154 | 0.000 | 1.000 | 0.000 | 0.351 | 0.000 |
| persistent_unavailable | P1 | together:glm-5.3-flash@high | 74 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1 | together:glm-5.3@high | 69 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | scripted:workflow | 160 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 180 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 232 | 0.000 | 1.000 | 0.000 | 0.586 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:glm-5.3-flash@high | 168 | 0.000 | 1.000 | 0.000 | 0.952 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:glm-5.3@high | 160 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:deepseek-v4-flash-0731@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:deepseek-v4-pro-0813@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:glm-5.3-flash@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:glm-5.3@high | 50 | 0.000 | 1.000 | 0.000 | 0.960 | 0.000 |
| precondition_changed | P1[runtime=semantic] | scripted:workflow | 50 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 50 | 0.000 | 1.000 | 0.000 | 0.980 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:glm-5.3-flash@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:glm-5.3@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | together:deepseek-v4-flash-0731@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | together:deepseek-v4-pro-0813@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | together:glm-5.3-flash@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | together:glm-5.3@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | scripted:workflow | 50 | 0.000 | 1.000 | 0.000 | 0.200 | 0.600 |
| task_invalid_result | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:glm-5.3-flash@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:glm-5.3@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 0.960 | 0.040 |
| timeout_after_execution | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| timeout_after_execution | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 0.920 | 0.080 |
| timeout_after_execution | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.600 | 0.400 | 0.000 | 0.600 | 0.400 |
| timeout_after_execution | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.600 | 0.400 | 0.000 | 0.200 | 0.800 |
| timeout_after_execution | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.760 | 0.240 | 0.000 | 0.680 | 0.320 |
| timeout_after_execution | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.720 | 0.280 | 0.000 | 0.720 | 0.280 |
| timeout_after_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:glm-5.3@high | 24 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:glm-5.3-flash@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:glm-5.3@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.960 | 0.000 |
| transient_failure | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |


## Exploratory

- Naive retry vs no runtime, harm on execution faults: 162/880 vs 74/880, MH OR 6.57, p 0.
- Open vs closed comparisons with `runs/stage-a-20261013-101143` are exploratory.
