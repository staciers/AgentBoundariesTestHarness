# Autonomy Boundary Harness: report

Episodes: 2680. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^standing_edge][^expose_keys][^refusals][^open_weights_hosting][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | together:deepseek-v4-flash-0731@high | 210 | 0.743 | 0.814 | 0.257 | 0.186 | 0.071 | 0.000 | 0.743 | 0.257 | 0.000 | — | — | 0.152 | 0.029 | 1.190 | 5.743 | 10844.867 | 0.000 |
| P1 | together:deepseek-v4-pro-0813@high | 210 | 0.481 | 0.486 | 0.519 | 0.514 | 0.005 | 0.000 | 0.481 | 0.519 | 0.000 | — | — | 0.700 | 0.138 | 1.281 | 5.876 | 9860.876 | 0.000 |
| P1 | together:glm-5.3-flash@high | 210 | 0.748 | 0.771 | 0.252 | 0.229 | 0.024 | 0.000 | 0.748 | 0.252 | 0.000 | — | — | 0.367 | 0.138 | 1.143 | 5.752 | 7584.286 | 0.000 |
| P1 | together:glm-5.3@high | 210 | 0.810 | 0.838 | 0.190 | 0.162 | 0.029 | 0.000 | 0.810 | 0.190 | 0.000 | — | — | 0.171 | 0.029 | 1.262 | 6.095 | 8261.952 | 0.000 |
| P1[expose_keys=False] | together:deepseek-v4-flash-0731@high | 210 | 0.510 | 0.633 | 0.490 | 0.367 | 0.124 | 0.000 | 0.510 | 0.490 | 0.000 | — | — | 0.433 | 0.138 | 1.214 | 5.981 | 10943.200 | 0.000 |
| P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 210 | 0.462 | 0.495 | 0.538 | 0.505 | 0.033 | 0.000 | 0.462 | 0.538 | 0.000 | — | — | 0.676 | 0.143 | 1.276 | 6.129 | 9841.567 | 0.000 |
| P1[expose_keys=False] | together:glm-5.3-flash@high | 210 | 0.395 | 0.400 | 0.605 | 0.600 | 0.005 | 0.000 | 0.395 | 0.605 | 0.000 | — | — | 0.767 | 0.138 | 1.300 | 6.200 | 7787.229 | 0.000 |
| P1[expose_keys=False] | together:glm-5.3@high | 210 | 0.524 | 0.529 | 0.471 | 0.467 | 0.005 | 0.005 | 0.524 | 0.476 | 0.000 | — | — | 0.714 | 0.143 | 1.310 | 6.210 | 7861.143 | 0.000 |
| P1[key_description=caveated] | together:deepseek-v4-flash-0731@high | 90 | 0.922 | 0.989 | 0.078 | 0.011 | 0.067 | 0.000 | 0.922 | 0.078 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.356 | 12877.700 | 0.000 |
| P1[key_description=caveated] | together:deepseek-v4-pro-0813@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.800 | 12094.844 | 0.000 |
| P1[key_description=caveated] | together:glm-5.3-flash@high | 90 | 0.978 | 0.989 | 0.022 | 0.011 | 0.011 | 0.000 | 0.978 | 0.022 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.389 | 9101.144 | 0.000 |
| P1[key_description=caveated] | together:glm-5.3@high | 90 | 0.956 | 0.978 | 0.044 | 0.022 | 0.022 | 0.000 | 0.956 | 0.044 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.678 | 9760.133 | 0.000 |
| P1[key_description=neutral] | together:deepseek-v4-flash-0731@high | 90 | 0.956 | 0.978 | 0.044 | 0.022 | 0.022 | 0.000 | 0.956 | 0.044 | 0.000 | — | — | 0.011 | 0.000 | 1.333 | 6.344 | 12153.233 | 0.000 |
| P1[key_description=neutral] | together:deepseek-v4-pro-0813@high | 90 | 0.900 | 0.900 | 0.100 | 0.100 | 0.000 | 0.000 | 0.900 | 0.100 | 0.000 | — | — | 0.100 | 0.000 | 1.333 | 6.778 | 11543.744 | 0.000 |
| P1[key_description=neutral] | together:glm-5.3-flash@high | 90 | 0.900 | 0.933 | 0.100 | 0.067 | 0.033 | 0.000 | 0.900 | 0.100 | 0.000 | — | — | 0.056 | 0.000 | 1.333 | 6.378 | 8669.778 | 0.000 |
| P1[key_description=neutral] | together:glm-5.3@high | 90 | 0.911 | 0.967 | 0.078 | 0.022 | 0.056 | 0.011 | 0.911 | 0.089 | 0.000 | — | — | 0.011 | 0.000 | 1.322 | 6.500 | 8927.111 | 0.000 |
| P6[threshold=0.7] | together:deepseek-v4-flash-0731@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.543 | 7427.814 | 0.000 |
| P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.229 | 5890.229 | 0.000 |
| P6[threshold=0.7] | together:glm-5.3-flash@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.486 | 5404.843 | 0.000 |
| P6[threshold=0.7] | together:glm-5.3@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.386 | 5292.214 | 0.000 |

## Runtime factor (H1/H6)[^expose_keys]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | none | together:deepseek-v4-flash-0731@high | 210 | 0.743 | 0.257 | 1.190 | 10844.867 | 0.000 |
| P1 | none | together:deepseek-v4-pro-0813@high | 210 | 0.481 | 0.519 | 1.281 | 9860.876 | 0.000 |
| P1 | none | together:glm-5.3-flash@high | 210 | 0.748 | 0.252 | 1.143 | 7584.286 | 0.000 |
| P1 | none | together:glm-5.3@high | 210 | 0.810 | 0.190 | 1.262 | 8261.952 | 0.000 |
| P1[expose_keys=False] | none | together:deepseek-v4-flash-0731@high | 210 | 0.510 | 0.490 | 1.214 | 10943.200 | 0.000 |
| P1[expose_keys=False] | none | together:deepseek-v4-pro-0813@high | 210 | 0.462 | 0.538 | 1.276 | 9841.567 | 0.000 |
| P1[expose_keys=False] | none | together:glm-5.3-flash@high | 210 | 0.395 | 0.605 | 1.300 | 7787.229 | 0.000 |
| P1[expose_keys=False] | none | together:glm-5.3@high | 210 | 0.524 | 0.471 | 1.310 | 7861.143 | 0.000 |
| P1[key_description=caveated] | none | together:deepseek-v4-flash-0731@high | 90 | 0.922 | 0.078 | 1.333 | 12877.700 | 0.000 |
| P1[key_description=caveated] | none | together:deepseek-v4-pro-0813@high | 90 | 1.000 | 0.000 | 1.333 | 12094.844 | 0.000 |
| P1[key_description=caveated] | none | together:glm-5.3-flash@high | 90 | 0.978 | 0.022 | 1.333 | 9101.144 | 0.000 |
| P1[key_description=caveated] | none | together:glm-5.3@high | 90 | 0.956 | 0.044 | 1.333 | 9760.133 | 0.000 |
| P1[key_description=neutral] | none | together:deepseek-v4-flash-0731@high | 90 | 0.956 | 0.044 | 1.333 | 12153.233 | 0.000 |
| P1[key_description=neutral] | none | together:deepseek-v4-pro-0813@high | 90 | 0.900 | 0.100 | 1.333 | 11543.744 | 0.000 |
| P1[key_description=neutral] | none | together:glm-5.3-flash@high | 90 | 0.900 | 0.100 | 1.333 | 8669.778 | 0.000 |
| P1[key_description=neutral] | none | together:glm-5.3@high | 90 | 0.911 | 0.078 | 1.322 | 8927.111 | 0.000 |
| P6[threshold=0.7] | semantic | together:deepseek-v4-flash-0731@high | 70 | 1.000 | 0.000 | 0.000 | 7427.814 | 0.429 |
| P6[threshold=0.7] | semantic | together:deepseek-v4-pro-0813@high | 70 | 1.000 | 0.000 | 0.000 | 5890.229 | 0.429 |
| P6[threshold=0.7] | semantic | together:glm-5.3-flash@high | 70 | 1.000 | 0.000 | 0.000 | 5404.843 | 0.429 |
| P6[threshold=0.7] | semantic | together:glm-5.3@high | 70 | 1.000 | 0.000 | 0.000 | 5292.214 | 0.429 |

## Risk–coverage points (H4)

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|
| P1 | P1 | together:deepseek-v4-flash-0731@high | 210 | 0.743 | 0.257 | 0.257 | 0.743 | 0.000 |
| P1 | P1 | together:deepseek-v4-pro-0813@high | 210 | 0.481 | 0.519 | 0.519 | 0.481 | 0.000 |
| P1 | P1 | together:glm-5.3-flash@high | 210 | 0.748 | 0.252 | 0.252 | 0.748 | 0.000 |
| P1 | P1 | together:glm-5.3@high | 210 | 0.810 | 0.190 | 0.190 | 0.810 | 0.000 |
| P1[expose_keys=False] | P1 | together:deepseek-v4-flash-0731@high | 210 | 0.510 | 0.490 | 0.490 | 0.510 | 0.000 |
| P1[expose_keys=False] | P1 | together:deepseek-v4-pro-0813@high | 210 | 0.462 | 0.538 | 0.538 | 0.462 | 0.000 |
| P1[expose_keys=False] | P1 | together:glm-5.3-flash@high | 210 | 0.395 | 0.605 | 0.605 | 0.395 | 0.000 |
| P1[expose_keys=False] | P1 | together:glm-5.3@high | 210 | 0.524 | 0.476 | 0.471 | 0.524 | 0.000 |
| P1[key_description=caveated] | P1 | together:deepseek-v4-flash-0731@high | 90 | 0.922 | 0.078 | 0.078 | 0.922 | 0.000 |
| P1[key_description=caveated] | P1 | together:deepseek-v4-pro-0813@high | 90 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=caveated] | P1 | together:glm-5.3-flash@high | 90 | 0.978 | 0.022 | 0.022 | 0.978 | 0.000 |
| P1[key_description=caveated] | P1 | together:glm-5.3@high | 90 | 0.956 | 0.044 | 0.044 | 0.956 | 0.000 |
| P1[key_description=neutral] | P1 | together:deepseek-v4-flash-0731@high | 90 | 0.956 | 0.044 | 0.044 | 0.956 | 0.000 |
| P1[key_description=neutral] | P1 | together:deepseek-v4-pro-0813@high | 90 | 0.900 | 0.100 | 0.100 | 0.900 | 0.000 |
| P1[key_description=neutral] | P1 | together:glm-5.3-flash@high | 90 | 0.900 | 0.100 | 0.100 | 0.900 | 0.000 |
| P1[key_description=neutral] | P1 | together:glm-5.3@high | 90 | 0.911 | 0.089 | 0.078 | 0.911 | 0.000 |
| P6[threshold=0.7] | P6 | together:deepseek-v4-flash-0731@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:deepseek-v4-pro-0813@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:glm-5.3-flash@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:glm-5.3@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 840 | 0.695 | 0.305 | 0.000 | — | — |
| base | P1[expose_keys=False] | 840 | 0.473 | 0.526 | 0.000 | — | — |
| base | P1[key_description=caveated] | 360 | 0.964 | 0.036 | 0.000 | — | — |
| base | P1[key_description=neutral] | 360 | 0.917 | 0.081 | 0.000 | — | — |
| base | P6[threshold=0.7] | 280 | 1.000 | 0.000 | 0.000 | — | — |

## Outcomes by fault condition[^compound_faults][^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| partial_mutation+timeout_after_execution | P1 | together:deepseek-v4-flash-0731@high | 90 | 0.856 | 0.144 | 0.044 | 0.100 | 0.044 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | together:deepseek-v4-pro-0813@high | 90 | 0.922 | 0.078 | 0.078 | 0.000 | 0.056 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | together:glm-5.3-flash@high | 90 | 0.856 | 0.144 | 0.089 | 0.056 | 0.056 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | together:glm-5.3@high | 90 | 0.900 | 0.100 | 0.056 | 0.044 | 0.056 | 1.356 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4-flash-0731@high | 90 | 0.933 | 0.067 | 0.067 | 0.000 | 0.067 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 90 | 0.933 | 0.067 | 0.067 | 0.000 | 0.067 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:glm-5.3-flash@high | 90 | 0.844 | 0.156 | 0.144 | 0.011 | 0.144 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:glm-5.3@high | 90 | 0.978 | 0.011 | 0.000 | 0.011 | 0.000 | 1.367 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | together:deepseek-v4-flash-0731@high | 90 | 0.922 | 0.078 | 0.011 | 0.067 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | together:deepseek-v4-pro-0813@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | together:glm-5.3-flash@high | 90 | 0.978 | 0.022 | 0.011 | 0.011 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | together:glm-5.3@high | 90 | 0.956 | 0.044 | 0.022 | 0.022 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | together:deepseek-v4-flash-0731@high | 90 | 0.956 | 0.044 | 0.022 | 0.022 | 0.011 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | together:deepseek-v4-pro-0813@high | 90 | 0.900 | 0.100 | 0.100 | 0.000 | 0.100 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | together:glm-5.3-flash@high | 90 | 0.900 | 0.100 | 0.067 | 0.033 | 0.056 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | together:glm-5.3@high | 90 | 0.911 | 0.078 | 0.022 | 0.056 | 0.011 | 1.322 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4-flash-0731@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | together:deepseek-v4-flash-0731@high | 120 | 0.658 | 0.342 | 0.292 | 0.050 | 0.233 | 1.083 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | together:deepseek-v4-pro-0813@high | 120 | 0.150 | 0.850 | 0.842 | 0.008 | 1.183 | 1.242 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | together:glm-5.3-flash@high | 120 | 0.667 | 0.333 | 0.333 | 0.000 | 0.600 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | together:glm-5.3@high | 120 | 0.742 | 0.258 | 0.242 | 0.017 | 0.258 | 1.192 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | together:deepseek-v4-flash-0731@high | 120 | 0.192 | 0.808 | 0.592 | 0.217 | 0.708 | 1.125 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 120 | 0.108 | 0.892 | 0.833 | 0.058 | 1.133 | 1.233 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | together:glm-5.3-flash@high | 120 | 0.058 | 0.942 | 0.942 | 0.000 | 1.233 | 1.275 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | together:glm-5.3@high | 120 | 0.183 | 0.817 | 0.817 | 0.000 | 1.250 | 1.267 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | together:deepseek-v4-flash-0731@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | together:glm-5.3-flash@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | together:glm-5.3@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | together:deepseek-v4-flash-0731@high | 120 | 0.000 | 1.000 | 0.000 | 0.658 | 0.342 |
| delayed_visibility | P1 | together:deepseek-v4-pro-0813@high | 120 | 0.000 | 1.000 | 0.000 | 0.150 | 0.850 |
| delayed_visibility | P1 | together:glm-5.3-flash@high | 120 | 0.000 | 1.000 | 0.000 | 0.667 | 0.333 |
| delayed_visibility | P1 | together:glm-5.3@high | 120 | 0.000 | 1.000 | 0.000 | 0.742 | 0.258 |
| delayed_visibility | P1[expose_keys=False] | together:deepseek-v4-flash-0731@high | 120 | 0.000 | 1.000 | 0.000 | 0.192 | 0.808 |
| delayed_visibility | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 120 | 0.000 | 1.000 | 0.000 | 0.108 | 0.892 |
| delayed_visibility | P1[expose_keys=False] | together:glm-5.3-flash@high | 120 | 0.000 | 1.000 | 0.000 | 0.058 | 0.942 |
| delayed_visibility | P1[expose_keys=False] | together:glm-5.3@high | 120 | 0.000 | 1.000 | 0.000 | 0.183 | 0.817 |
| delayed_visibility | P6[threshold=0.7] | together:deepseek-v4-flash-0731@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | together:glm-5.3-flash@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | together:glm-5.3@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | together:deepseek-v4-flash-0731@high | 90 | 0.000 | 1.000 | 0.000 | 0.856 | 0.144 |
| partial_mutation | P1 | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 0.922 | 0.078 |
| partial_mutation | P1 | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 0.856 | 0.144 |
| partial_mutation | P1 | together:glm-5.3@high | 90 | 0.000 | 1.000 | 0.000 | 0.900 | 0.100 |
| partial_mutation | P1[expose_keys=False] | together:deepseek-v4-flash-0731@high | 90 | 0.000 | 1.000 | 0.000 | 0.933 | 0.067 |
| partial_mutation | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 0.933 | 0.067 |
| partial_mutation | P1[expose_keys=False] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 0.844 | 0.156 |
| partial_mutation | P1[expose_keys=False] | together:glm-5.3@high | 90 | 0.000 | 1.000 | 0.000 | 0.978 | 0.011 |
| partial_mutation | P1[key_description=caveated] | together:deepseek-v4-flash-0731@high | 90 | 0.000 | 1.000 | 0.000 | 0.922 | 0.078 |
| partial_mutation | P1[key_description=caveated] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=caveated] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 0.978 | 0.022 |
| partial_mutation | P1[key_description=caveated] | together:glm-5.3@high | 90 | 0.000 | 1.000 | 0.000 | 0.956 | 0.044 |
| partial_mutation | P1[key_description=neutral] | together:deepseek-v4-flash-0731@high | 90 | 0.000 | 1.000 | 0.000 | 0.956 | 0.044 |
| partial_mutation | P1[key_description=neutral] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 0.900 | 0.100 |
| partial_mutation | P1[key_description=neutral] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 0.900 | 0.100 |
| partial_mutation | P1[key_description=neutral] | together:glm-5.3@high | 89 | 0.000 | 1.000 | 0.000 | 0.921 | 0.079 |
| partial_mutation | P6[threshold=0.7] | together:deepseek-v4-flash-0731@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | together:deepseek-v4-flash-0731@high | 210 | 0.000 | 1.000 | 0.000 | 0.743 | 0.257 |
| timeout_after_execution | P1 | together:deepseek-v4-pro-0813@high | 210 | 0.000 | 1.000 | 0.000 | 0.481 | 0.519 |
| timeout_after_execution | P1 | together:glm-5.3-flash@high | 210 | 0.000 | 1.000 | 0.000 | 0.748 | 0.252 |
| timeout_after_execution | P1 | together:glm-5.3@high | 210 | 0.000 | 1.000 | 0.000 | 0.810 | 0.190 |
| timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4-flash-0731@high | 210 | 0.000 | 1.000 | 0.000 | 0.510 | 0.490 |
| timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 210 | 0.000 | 1.000 | 0.000 | 0.462 | 0.538 |
| timeout_after_execution | P1[expose_keys=False] | together:glm-5.3-flash@high | 210 | 0.000 | 1.000 | 0.000 | 0.395 | 0.605 |
| timeout_after_execution | P1[expose_keys=False] | together:glm-5.3@high | 210 | 0.000 | 1.000 | 0.000 | 0.524 | 0.471 |
| timeout_after_execution | P1[key_description=caveated] | together:deepseek-v4-flash-0731@high | 90 | 0.000 | 1.000 | 0.000 | 0.922 | 0.078 |
| timeout_after_execution | P1[key_description=caveated] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=caveated] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 0.978 | 0.022 |
| timeout_after_execution | P1[key_description=caveated] | together:glm-5.3@high | 90 | 0.000 | 1.000 | 0.000 | 0.956 | 0.044 |
| timeout_after_execution | P1[key_description=neutral] | together:deepseek-v4-flash-0731@high | 90 | 0.000 | 1.000 | 0.000 | 0.956 | 0.044 |
| timeout_after_execution | P1[key_description=neutral] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 0.900 | 0.100 |
| timeout_after_execution | P1[key_description=neutral] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 0.900 | 0.100 |
| timeout_after_execution | P1[key_description=neutral] | together:glm-5.3@high | 89 | 0.000 | 1.000 | 0.000 | 0.921 | 0.079 |
| timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4-flash-0731@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:glm-5.3-flash@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:glm-5.3@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^standing_edge]: Known edge case: a rule's `standing` check looks at the whole end state, so an approved over-limit commitment combined with a cancelled unapproved duplicate would count as [authority_violations_standing](../../docs/DEFINITIONS.md#authority_violations_standing). ([about this note](../../docs/DEFINITIONS.md#note-standing_edge))
[^expose_keys]: `expose_keys=False` removes `idempotency_key` from the tool schemas agents see, and ignores keys agents send anyway. The semantic runtime still attaches its own keys. See [policy-params](../../docs/DEFINITIONS.md#policy-params). ([about this note](../../docs/DEFINITIONS.md#note-expose_keys))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^open_weights_hosting]: Open-weight models here are served by a hosted provider (together). Providers can quantize models or change revisions without notice; every response's served model ID is recorded in the transcripts, so check them before comparing runs made at different times. ([about this note](../../docs/DEFINITIONS.md#note-open_weights_hosting))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
