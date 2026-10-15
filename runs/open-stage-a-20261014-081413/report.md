# Autonomy Boundary Harness: report[^scripted_not_evidence]

Episodes: 4690. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^small_samples][^synthetic_tokens][^standing_edge][^refusals][^open_weights_hosting][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | together:deepseek-v4-flash-0731@high | 385 | 0.953 | 0.956 | 0.047 | 0.044 | 0.003 | 0.000 | 0.953 | 0.047 | 0.000 | — | — | 0.042 | 0.000 | 0.870 | 5.483 | 11510.179 | 0.000 |
| P1 | together:deepseek-v4-pro-0813@high | 385 | 0.891 | 0.891 | 0.083 | 0.083 | 0.000 | 0.026 | 0.891 | 0.109 | 0.000 | — | — | 0.091 | 0.000 | 1.029 | 5.252 | 9952.145 | 0.000 |
| P1 | together:glm-5.3-flash@high | 385 | 0.956 | 0.961 | 0.044 | 0.039 | 0.005 | 0.000 | 0.956 | 0.044 | 0.000 | — | — | 0.057 | 0.008 | 0.800 | 5.327 | 8299.231 | 0.000 |
| P1 | together:glm-5.3@high | 385 | 0.971 | 0.971 | 0.018 | 0.018 | 0.000 | 0.010 | 0.971 | 0.029 | 0.000 | — | — | 0.013 | 0.000 | 0.779 | 5.229 | 8194.192 | 0.000 |
| P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 245 | 0.845 | 0.853 | 0.155 | 0.147 | 0.008 | 0.000 | 0.845 | 0.155 | 0.000 | — | — | 0.118 | 0.000 | 0.245 | 4.465 | 8942.461 | 0.000 |
| P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 245 | 0.731 | 0.731 | 0.265 | 0.265 | 0.000 | 0.004 | 0.731 | 0.269 | 0.000 | — | — | 0.347 | 0.000 | 0.265 | 4.167 | 7516.739 | 0.000 |
| P1[runtime=naive_retry] | together:glm-5.3-flash@high | 245 | 0.869 | 0.869 | 0.131 | 0.131 | 0.000 | 0.000 | 0.869 | 0.131 | 0.000 | — | — | 0.192 | 0.000 | 0.224 | 4.355 | 6588.478 | 0.000 |
| P1[runtime=naive_retry] | together:glm-5.3@high | 245 | 0.886 | 0.886 | 0.110 | 0.110 | 0.000 | 0.004 | 0.886 | 0.114 | 0.000 | — | — | 0.090 | 0.000 | 0.237 | 4.347 | 6559.988 | 0.000 |
| P1[runtime=semantic] | scripted:workflow | 630 | 0.794 | 0.794 | 0.048 | 0.048 | 0.000 | 0.159 | 0.794 | 0.206 | 0.000 | — | — | 0.000 | 0.016 | 0.159 | 5.175 | 18731.429 | 0.000 |
| P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 385 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.270 | 4.800 | 10119.616 | 0.000 |
| P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 385 | 0.977 | 0.977 | 0.000 | 0.000 | 0.000 | 0.023 | 0.977 | 0.023 | 0.000 | — | — | 0.000 | 0.000 | 0.281 | 4.436 | 8328.553 | 0.000 |
| P1[runtime=semantic] | together:glm-5.3-flash@high | 385 | 0.997 | 0.997 | 0.000 | 0.000 | 0.000 | 0.003 | 0.997 | 0.003 | 0.000 | — | — | 0.003 | 0.000 | 0.247 | 4.631 | 7200.210 | 0.000 |
| P1[runtime=semantic] | together:glm-5.3@high | 385 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.003 | 0.000 | 0.236 | 4.616 | 7338.278 | 0.000 |

## Runtime factor (H1/H6)[^synthetic_tokens]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | none | together:deepseek-v4-flash-0731@high | 385 | 0.953 | 0.047 | 0.870 | 11510.179 | 0.000 |
| P1 | none | together:deepseek-v4-pro-0813@high | 385 | 0.891 | 0.083 | 1.029 | 9952.145 | 0.000 |
| P1 | none | together:glm-5.3-flash@high | 385 | 0.956 | 0.044 | 0.800 | 8299.231 | 0.000 |
| P1 | none | together:glm-5.3@high | 385 | 0.971 | 0.018 | 0.779 | 8194.192 | 0.000 |
| P1[runtime=naive_retry] | naive_retry | together:deepseek-v4-flash-0731@high | 245 | 0.845 | 0.155 | 0.245 | 8942.461 | 0.592 |
| P1[runtime=naive_retry] | naive_retry | together:deepseek-v4-pro-0813@high | 245 | 0.731 | 0.265 | 0.265 | 7516.739 | 0.588 |
| P1[runtime=naive_retry] | naive_retry | together:glm-5.3-flash@high | 245 | 0.869 | 0.131 | 0.224 | 6588.478 | 0.592 |
| P1[runtime=naive_retry] | naive_retry | together:glm-5.3@high | 245 | 0.886 | 0.110 | 0.237 | 6559.988 | 0.592 |
| P1[runtime=semantic] | semantic | scripted:workflow | 630 | 0.794 | 0.048 | 0.159 | 18731.429 | 0.492 |
| P1[runtime=semantic] | semantic | together:deepseek-v4-flash-0731@high | 385 | 1.000 | 0.000 | 0.270 | 10119.616 | 0.597 |
| P1[runtime=semantic] | semantic | together:deepseek-v4-pro-0813@high | 385 | 0.977 | 0.000 | 0.281 | 8328.553 | 0.699 |
| P1[runtime=semantic] | semantic | together:glm-5.3-flash@high | 385 | 0.997 | 0.000 | 0.247 | 7200.210 | 0.574 |
| P1[runtime=semantic] | semantic | together:glm-5.3@high | 385 | 1.000 | 0.000 | 0.236 | 7338.278 | 0.558 |

## Risk–coverage points (H4)[^small_samples]

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|
| P1 | P1 | together:deepseek-v4-flash-0731@high | 385 | 0.953 | 0.047 | 0.047 | 0.953 | 0.000 |
| P1 | P1 | together:deepseek-v4-pro-0813@high | 385 | 0.891 | 0.109 | 0.083 | 0.891 | 0.000 |
| P1 | P1 | together:glm-5.3-flash@high | 385 | 0.956 | 0.044 | 0.044 | 0.956 | 0.000 |
| P1 | P1 | together:glm-5.3@high | 385 | 0.971 | 0.029 | 0.018 | 0.971 | 0.000 |
| P1[runtime=naive_retry] | P1 | together:deepseek-v4-flash-0731@high | 245 | 0.845 | 0.155 | 0.155 | 0.845 | 0.000 |
| P1[runtime=naive_retry] | P1 | together:deepseek-v4-pro-0813@high | 245 | 0.731 | 0.269 | 0.265 | 0.731 | 0.000 |
| P1[runtime=naive_retry] | P1 | together:glm-5.3-flash@high | 245 | 0.869 | 0.131 | 0.131 | 0.869 | 0.000 |
| P1[runtime=naive_retry] | P1 | together:glm-5.3@high | 245 | 0.886 | 0.114 | 0.110 | 0.886 | 0.000 |
| P1[runtime=semantic] | P1 | scripted:workflow | 630 | 0.794 | 0.206 | 0.048 | 0.794 | 0.000 |
| P1[runtime=semantic] | P1 | together:deepseek-v4-flash-0731@high | 385 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[runtime=semantic] | P1 | together:deepseek-v4-pro-0813@high | 385 | 0.977 | 0.023 | 0.000 | 0.977 | 0.000 |
| P1[runtime=semantic] | P1 | together:glm-5.3-flash@high | 385 | 0.997 | 0.003 | 0.000 | 0.997 | 0.000 |
| P1[runtime=semantic] | P1 | together:glm-5.3@high | 385 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 1540 | 0.943 | 0.048 | 0.000 | — | — |
| base | P1[runtime=naive_retry] | 980 | 0.833 | 0.165 | 0.000 | — | — |
| base | P1[runtime=semantic] | 2170 | 0.935 | 0.014 | 0.000 | — | — |

## Outcomes by fault condition[^harm_split][^small_samples]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1 | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1 | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.400 | 0.600 | 0.600 | 0.000 | 0.600 | 0.400 | 0.000 |
| duplicate_execution | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.200 | 0.800 | 0.800 | 0.000 | 1.000 | 0.400 | 0.000 |
| duplicate_execution | P1 | together:glm-5.3-flash@high | 25 | 0.600 | 0.400 | 0.400 | 0.000 | 0.600 | 0.240 | 0.000 |
| duplicate_execution | P1 | together:glm-5.3@high | 25 | 0.720 | 0.280 | 0.280 | 0.000 | 0.200 | 0.320 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.520 | 0.480 | 0.480 | 0.000 | 0.360 | 0.400 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.200 | 0.800 | 0.800 | 0.000 | 1.000 | 0.400 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.640 | 0.360 | 0.360 | 0.000 | 0.640 | 0.200 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.720 | 0.280 | 0.280 | 0.000 | 0.120 | 0.400 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.960 | 0.040 | 0.040 | 0.000 | 0.000 | 1.040 | 0.000 |
| malformed_response | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.760 | 0.240 | 0.240 | 0.000 | 0.200 | 1.240 | 0.000 |
| malformed_response | P1 | together:glm-5.3-flash@high | 25 | 0.800 | 0.200 | 0.160 | 0.040 | 0.240 | 1.120 | 0.000 |
| malformed_response | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.760 | 0.240 | 0.240 | 0.000 | 0.280 | 0.400 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.360 | 0.600 | 0.600 | 0.000 | 1.000 | 0.600 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.800 | 0.200 | 0.200 | 0.000 | 0.360 | 0.560 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.880 | 0.120 | 0.120 | 0.000 | 0.200 | 0.440 | 0.000 |
| malformed_response | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1 | together:deepseek-v4-flash-0731@high | 20 | 0.950 | 0.050 | 0.000 | 0.050 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | together:deepseek-v4-pro-0813@high | 20 | 0.950 | 0.050 | 0.050 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | together:glm-5.3-flash@high | 20 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | together:glm-5.3@high | 20 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 0.950 | 0.000 |
| partial_mutation | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 20 | 0.500 | 0.500 | 0.400 | 0.100 | 0.400 | 0.250 | 0.000 |
| partial_mutation | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 20 | 0.500 | 0.500 | 0.500 | 0.000 | 0.500 | 0.250 | 0.000 |
| partial_mutation | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 20 | 0.500 | 0.500 | 0.500 | 0.000 | 0.500 | 0.250 | 0.000 |
| partial_mutation | P1[runtime=naive_retry] | together:glm-5.3@high | 20 | 0.500 | 0.500 | 0.500 | 0.000 | 0.500 | 0.250 | 0.000 |
| partial_mutation | P1[runtime=semantic] | scripted:workflow | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 20 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 20 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:glm-5.3-flash@high | 20 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.050 | 0.000 |
| partial_mutation | P1[runtime=semantic] | together:glm-5.3@high | 20 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.050 | 0.000 |
| partial_response | P1 | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.040 | 0.000 |
| partial_response | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_response | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.000 |
| partial_response | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| persistent_unavailable | P1 | together:deepseek-v4-flash-0731@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 2.300 | 0.000 |
| persistent_unavailable | P1 | together:deepseek-v4-pro-0813@high | 40 | 0.750 | 0.000 | 0.000 | 0.000 | 0.000 | 3.850 | 0.000 |
| persistent_unavailable | P1 | together:glm-5.3-flash@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.850 | 0.000 |
| persistent_unavailable | P1 | together:glm-5.3@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.725 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | scripted:workflow | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.125 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 40 | 0.800 | 0.000 | 0.000 | 0.000 | 0.000 | 1.450 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:glm-5.3-flash@high | 40 | 0.975 | 0.000 | 0.000 | 0.000 | 0.000 | 1.050 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | together:glm-5.3@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:deepseek-v4-flash-0731@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:deepseek-v4-pro-0813@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:glm-5.3-flash@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | together:glm-5.3@high | 50 | 0.960 | 0.000 | 0.000 | 0.000 | 0.000 | 1.040 | 0.000 |
| precondition_changed | P1[runtime=semantic] | scripted:workflow | 50 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 50 | 0.980 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:glm-5.3-flash@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | together:glm-5.3@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| task_invalid_result | P1 | together:deepseek-v4-flash-0731@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.240 | 0.000 |
| task_invalid_result | P1 | together:deepseek-v4-pro-0813@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.000 |
| task_invalid_result | P1 | together:glm-5.3-flash@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.060 | 0.000 |
| task_invalid_result | P1 | together:glm-5.3@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | scripted:workflow | 50 | 0.200 | 0.600 | 0.600 | 0.000 | 0.000 | 0.200 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.180 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:glm-5.3-flash@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.020 | 0.020 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | together:glm-5.3@high | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.020 | 0.000 | 0.000 |
| timeout_after_execution | P1 | together:deepseek-v4-flash-0731@high | 25 | 0.960 | 0.040 | 0.040 | 0.000 | 0.040 | 1.000 | 0.000 |
| timeout_after_execution | P1 | together:deepseek-v4-pro-0813@high | 25 | 0.800 | 0.200 | 0.200 | 0.000 | 0.200 | 1.160 | 0.000 |
| timeout_after_execution | P1 | together:glm-5.3-flash@high | 25 | 0.920 | 0.080 | 0.040 | 0.040 | 0.040 | 1.040 | 0.000 |
| timeout_after_execution | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.040 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 0.600 | 0.400 | 0.400 | 0.000 | 0.200 | 0.400 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 0.200 | 0.800 | 0.800 | 0.000 | 1.000 | 0.400 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 0.680 | 0.320 | 0.320 | 0.000 | 0.480 | 0.240 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.720 | 0.280 | 0.280 | 0.000 | 0.160 | 0.280 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1 | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | together:glm-5.3@high | 25 | 0.960 | 0.000 | 0.000 | 0.000 | 0.000 | 0.960 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1 | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | together:glm-5.3@high | 25 | 0.960 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:deepseek-v4-flash-0731@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:deepseek-v4-pro-0813@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:glm-5.3-flash@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | together:glm-5.3@high | 25 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
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

[^scripted_not_evidence]: Rows for `scripted:*` agents check the harness, not the hypotheses. The scripted agent's competence knobs and the ORACLE's labels encode the paper's assumptions, so patterns such as "P6 beats P1 on execution faults" are partly built in. Evidence must come from LLM agents. ([about this note](../../docs/DEFINITIONS.md#note-scripted_not_evidence))
[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^small_samples]: Small groups: the smallest group in these tables has n=20. At that size a 95% interval for a rate near 50% is about ±22%. Wilson intervals for [success](../../docs/DEFINITIONS.md#success) are in the CSVs ([success_ci](../../docs/DEFINITIONS.md#success_ci)). ([about this note](../../docs/DEFINITIONS.md#note-small_samples))
[^synthetic_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) for scripted agents are modelled, not measured. ([about this note](../../docs/DEFINITIONS.md#note-synthetic_tokens))
[^standing_edge]: Known edge case: a rule's `standing` check looks at the whole end state, so an approved over-limit commitment combined with a cancelled unapproved duplicate would count as [authority_violations_standing](../../docs/DEFINITIONS.md#authority_violations_standing). ([about this note](../../docs/DEFINITIONS.md#note-standing_edge))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^open_weights_hosting]: Open-weight models here are served by a hosted provider (together). Providers can quantize models or change revisions without notice; every response's served model ID is recorded in the transcripts, so check them before comparing runs made at different times. ([about this note](../../docs/DEFINITIONS.md#note-open_weights_hosting))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
