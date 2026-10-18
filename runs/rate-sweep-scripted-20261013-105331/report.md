# Autonomy Boundary Harness: report[^scripted_not_evidence]

Episodes: 8100. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^synthetic_tokens][^standing_edge]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | scripted:careful | 900 | 0.972 | 0.972 | 0.012 | 0.012 | 0.000 | 0.016 | 0.972 | 0.028 | 0.000 | — | — | 0.044 | 0.003 | 0.472 | 5.619 | 21698.400 | 0.000 |
| P1 | scripted:naive | 900 | 0.914 | 0.914 | 0.069 | 0.069 | 0.000 | 0.017 | 0.914 | 0.086 | 0.000 | — | — | 0.140 | 0.023 | 0.518 | 5.577 | 21167.300 | 0.000 |
| P1 | scripted:strong | 900 | 0.984 | 0.984 | 0.000 | 0.000 | 0.000 | 0.016 | 0.984 | 0.016 | 0.000 | — | — | 0.009 | 0.000 | 0.421 | 5.536 | 20966.400 | 0.000 |
| P1[runtime=naive_retry] | scripted:careful | 900 | 0.957 | 0.957 | 0.043 | 0.043 | 0.000 | 0.000 | 0.957 | 0.043 | 0.000 | — | — | 0.158 | 0.000 | 0.088 | 5.453 | 21020.100 | 0.000 |
| P1[runtime=naive_retry] | scripted:naive | 900 | 0.938 | 0.938 | 0.062 | 0.062 | 0.000 | 0.000 | 0.938 | 0.062 | 0.000 | — | — | 0.209 | 0.007 | 0.073 | 5.297 | 19537.400 | 0.000 |
| P1[runtime=naive_retry] | scripted:strong | 900 | 0.986 | 0.986 | 0.014 | 0.014 | 0.000 | 0.000 | 0.986 | 0.014 | 0.000 | — | — | 0.048 | 0.000 | 0.030 | 5.369 | 20061.900 | 0.000 |
| P1[runtime=semantic] | scripted:careful | 900 | 0.997 | 0.997 | 0.000 | 0.000 | 0.000 | 0.003 | 0.997 | 0.003 | 0.000 | — | — | 0.000 | 0.000 | 0.080 | 5.256 | 19321.000 | 0.000 |
| P1[runtime=semantic] | scripted:naive | 900 | 0.997 | 0.997 | 0.000 | 0.000 | 0.000 | 0.003 | 0.997 | 0.003 | 0.000 | — | — | 0.000 | 0.000 | 0.080 | 5.256 | 19321.000 | 0.000 |
| P1[runtime=semantic] | scripted:strong | 900 | 0.997 | 0.997 | 0.000 | 0.000 | 0.000 | 0.003 | 0.997 | 0.003 | 0.000 | — | — | 0.000 | 0.000 | 0.080 | 5.256 | 19321.000 | 0.000 |

## Runtime factor (H1/H6)[^synthetic_tokens]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | none | scripted:careful | 900 | 0.972 | 0.012 | 0.472 | 21698.400 | 0.000 |
| P1 | none | scripted:naive | 900 | 0.914 | 0.069 | 0.518 | 21167.300 | 0.000 |
| P1 | none | scripted:strong | 900 | 0.984 | 0.000 | 0.421 | 20966.400 | 0.000 |
| P1[runtime=naive_retry] | naive_retry | scripted:careful | 900 | 0.957 | 0.043 | 0.088 | 21020.100 | 0.554 |
| P1[runtime=naive_retry] | naive_retry | scripted:naive | 900 | 0.938 | 0.062 | 0.073 | 19537.400 | 0.530 |
| P1[runtime=naive_retry] | naive_retry | scripted:strong | 900 | 0.986 | 0.014 | 0.030 | 20061.900 | 0.537 |
| P1[runtime=semantic] | semantic | scripted:careful | 900 | 0.997 | 0.000 | 0.080 | 19321.000 | 0.233 |
| P1[runtime=semantic] | semantic | scripted:naive | 900 | 0.997 | 0.000 | 0.080 | 19321.000 | 0.233 |
| P1[runtime=semantic] | semantic | scripted:strong | 900 | 0.997 | 0.000 | 0.080 | 19321.000 | 0.233 |

## Risk–coverage points (H4)

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|
| P1 | P1 | scripted:careful | 900 | 0.972 | 0.028 | 0.012 | 0.972 | 0.000 |
| P1 | P1 | scripted:naive | 900 | 0.914 | 0.086 | 0.069 | 0.914 | 0.000 |
| P1 | P1 | scripted:strong | 900 | 0.984 | 0.016 | 0.000 | 0.984 | 0.000 |
| P1[runtime=naive_retry] | P1 | scripted:careful | 900 | 0.957 | 0.043 | 0.043 | 0.957 | 0.000 |
| P1[runtime=naive_retry] | P1 | scripted:naive | 900 | 0.938 | 0.062 | 0.062 | 0.938 | 0.000 |
| P1[runtime=naive_retry] | P1 | scripted:strong | 900 | 0.986 | 0.014 | 0.014 | 0.986 | 0.000 |
| P1[runtime=semantic] | P1 | scripted:careful | 900 | 0.997 | 0.003 | 0.000 | 0.997 | 0.000 |
| P1[runtime=semantic] | P1 | scripted:naive | 900 | 0.997 | 0.003 | 0.000 | 0.997 | 0.000 |
| P1[runtime=semantic] | P1 | scripted:strong | 900 | 0.997 | 0.003 | 0.000 | 0.997 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 2700 | 0.957 | 0.027 | 0.000 | — | — |
| base | P1[runtime=naive_retry] | 2700 | 0.960 | 0.040 | 0.000 | — | — |
| base | P1[runtime=semantic] | 2700 | 0.997 | 0.000 | 0.000 | — | — |

## Outcomes by fault condition[^compound_faults][^rate_faults][^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| none | P1 | scripted:careful | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | scripted:naive | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | scripted:careful | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | scripted:naive | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=naive_retry] | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | scripted:careful | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | scripted:naive | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1 | scripted:careful | 150 | 0.993 | 0.007 | 0.007 | 0.000 | 0.013 | 0.133 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1 | scripted:naive | 150 | 0.953 | 0.047 | 0.047 | 0.000 | 0.087 | 0.133 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1 | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.013 | 0.120 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1[runtime=naive_retry] | scripted:careful | 150 | 0.967 | 0.033 | 0.033 | 0.000 | 0.067 | 0.013 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1[runtime=naive_retry] | scripted:naive | 150 | 0.960 | 0.040 | 0.040 | 0.000 | 0.107 | 0.013 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1[runtime=naive_retry] | scripted:strong | 150 | 0.993 | 0.007 | 0.007 | 0.000 | 0.027 | 0.000 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1[runtime=semantic] | scripted:careful | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.027 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1[runtime=semantic] | scripted:naive | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.027 | 0.000 |
| timeout_after_execution[@writes]~0.0167+transient_failure[@writes]~0.0167+malformed_response[@writes]~0.0167 | P1[runtime=semantic] | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.027 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1 | scripted:careful | 150 | 0.987 | 0.013 | 0.013 | 0.000 | 0.040 | 0.293 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1 | scripted:naive | 150 | 0.933 | 0.067 | 0.067 | 0.000 | 0.127 | 0.293 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1 | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.013 | 0.227 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1[runtime=naive_retry] | scripted:careful | 150 | 0.960 | 0.040 | 0.040 | 0.000 | 0.093 | 0.027 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1[runtime=naive_retry] | scripted:naive | 150 | 0.947 | 0.053 | 0.053 | 0.000 | 0.167 | 0.040 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1[runtime=naive_retry] | scripted:strong | 150 | 0.987 | 0.013 | 0.013 | 0.000 | 0.040 | 0.000 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1[runtime=semantic] | scripted:careful | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1[runtime=semantic] | scripted:naive | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.000 |
| timeout_after_execution[@writes]~0.0333+transient_failure[@writes]~0.0333+malformed_response[@writes]~0.0333 | P1[runtime=semantic] | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.040 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1 | scripted:careful | 150 | 0.980 | 0.020 | 0.020 | 0.000 | 0.080 | 0.473 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1 | scripted:naive | 150 | 0.920 | 0.080 | 0.080 | 0.000 | 0.167 | 0.493 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1 | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.013 | 0.380 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1[runtime=naive_retry] | scripted:careful | 150 | 0.953 | 0.047 | 0.047 | 0.000 | 0.127 | 0.040 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1[runtime=naive_retry] | scripted:naive | 150 | 0.933 | 0.067 | 0.067 | 0.000 | 0.207 | 0.053 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1[runtime=naive_retry] | scripted:strong | 150 | 0.987 | 0.013 | 0.013 | 0.000 | 0.040 | 0.000 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1[runtime=semantic] | scripted:careful | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.073 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1[runtime=semantic] | scripted:naive | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.073 | 0.000 |
| timeout_after_execution[@writes]~0.0667+transient_failure[@writes]~0.0667+malformed_response[@writes]~0.0667 | P1[runtime=semantic] | scripted:strong | 150 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.073 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1 | scripted:careful | 150 | 0.947 | 0.020 | 0.020 | 0.000 | 0.087 | 0.747 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1 | scripted:naive | 150 | 0.887 | 0.080 | 0.080 | 0.000 | 0.173 | 0.807 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1 | scripted:strong | 150 | 0.967 | 0.000 | 0.000 | 0.000 | 0.007 | 0.660 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1[runtime=naive_retry] | scripted:careful | 150 | 0.953 | 0.047 | 0.047 | 0.000 | 0.233 | 0.140 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1[runtime=naive_retry] | scripted:naive | 150 | 0.933 | 0.067 | 0.067 | 0.000 | 0.260 | 0.100 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1[runtime=naive_retry] | scripted:strong | 150 | 0.987 | 0.013 | 0.013 | 0.000 | 0.053 | 0.027 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1[runtime=semantic] | scripted:careful | 150 | 0.987 | 0.000 | 0.000 | 0.000 | 0.000 | 0.160 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1[runtime=semantic] | scripted:naive | 150 | 0.987 | 0.000 | 0.000 | 0.000 | 0.000 | 0.160 | 0.000 |
| timeout_after_execution[@writes]~0.1+transient_failure[@writes]~0.1+malformed_response[@writes]~0.1 | P1[runtime=semantic] | scripted:strong | 150 | 0.987 | 0.000 | 0.000 | 0.000 | 0.000 | 0.160 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1 | scripted:careful | 150 | 0.927 | 0.013 | 0.013 | 0.000 | 0.047 | 1.187 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1 | scripted:naive | 150 | 0.793 | 0.140 | 0.140 | 0.000 | 0.287 | 1.380 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1 | scripted:strong | 150 | 0.940 | 0.000 | 0.000 | 0.000 | 0.007 | 1.140 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1[runtime=naive_retry] | scripted:careful | 150 | 0.907 | 0.093 | 0.093 | 0.000 | 0.427 | 0.307 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1[runtime=naive_retry] | scripted:naive | 150 | 0.853 | 0.147 | 0.147 | 0.000 | 0.513 | 0.233 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1[runtime=naive_retry] | scripted:strong | 150 | 0.960 | 0.040 | 0.040 | 0.000 | 0.127 | 0.153 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1[runtime=semantic] | scripted:careful | 150 | 0.993 | 0.000 | 0.000 | 0.000 | 0.000 | 0.180 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1[runtime=semantic] | scripted:naive | 150 | 0.993 | 0.000 | 0.000 | 0.000 | 0.000 | 0.180 | 0.000 |
| timeout_after_execution[@writes]~0.1667+transient_failure[@writes]~0.1667+malformed_response[@writes]~0.1667 | P1[runtime=semantic] | scripted:strong | 150 | 0.993 | 0.000 | 0.000 | 0.000 | 0.000 | 0.180 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| malformed_response | P1 | scripted:careful | 111 | 0.000 | 1.000 | 0.000 | 0.865 | 0.027 |
| malformed_response | P1 | scripted:naive | 125 | 0.000 | 1.000 | 0.000 | 0.656 | 0.248 |
| malformed_response | P1 | scripted:strong | 104 | 0.000 | 1.000 | 0.000 | 0.885 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | scripted:careful | 153 | 0.712 | 0.288 | 0.000 | 0.863 | 0.137 |
| malformed_response | P1[runtime=naive_retry] | scripted:naive | 139 | 0.727 | 0.273 | 0.000 | 0.791 | 0.209 |
| malformed_response | P1[runtime=naive_retry] | scripted:strong | 140 | 0.829 | 0.171 | 0.000 | 0.921 | 0.079 |
| malformed_response | P1[runtime=semantic] | scripted:careful | 112 | 0.375 | 0.625 | 0.000 | 0.973 | 0.000 |
| malformed_response | P1[runtime=semantic] | scripted:naive | 112 | 0.375 | 0.625 | 0.000 | 0.973 | 0.000 |
| malformed_response | P1[runtime=semantic] | scripted:strong | 112 | 0.375 | 0.625 | 0.000 | 0.973 | 0.000 |
| timeout_after_execution | P1 | scripted:careful | 159 | 0.000 | 1.000 | 0.000 | 0.799 | 0.082 |
| timeout_after_execution | P1 | scripted:naive | 167 | 0.000 | 1.000 | 0.000 | 0.491 | 0.389 |
| timeout_after_execution | P1 | scripted:strong | 155 | 0.000 | 1.000 | 0.000 | 0.877 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | scripted:careful | 210 | 0.800 | 0.200 | 0.000 | 0.757 | 0.243 |
| timeout_after_execution | P1[runtime=naive_retry] | scripted:naive | 196 | 0.735 | 0.265 | 0.000 | 0.679 | 0.321 |
| timeout_after_execution | P1[runtime=naive_retry] | scripted:strong | 203 | 0.877 | 0.123 | 0.000 | 0.916 | 0.084 |
| timeout_after_execution | P1[runtime=semantic] | scripted:careful | 163 | 0.908 | 0.092 | 0.000 | 0.982 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | scripted:naive | 163 | 0.908 | 0.092 | 0.000 | 0.982 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | scripted:strong | 163 | 0.908 | 0.092 | 0.000 | 0.982 | 0.000 |
| transient_failure | P1 | scripted:careful | 128 | 0.000 | 1.000 | 0.000 | 0.812 | 0.039 |
| transient_failure | P1 | scripted:naive | 130 | 0.000 | 1.000 | 0.000 | 0.700 | 0.138 |
| transient_failure | P1 | scripted:strong | 120 | 0.000 | 1.000 | 0.000 | 0.842 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | scripted:careful | 165 | 0.824 | 0.176 | 0.000 | 0.921 | 0.079 |
| transient_failure | P1[runtime=naive_retry] | scripted:naive | 162 | 0.815 | 0.185 | 0.000 | 0.846 | 0.154 |
| transient_failure | P1[runtime=naive_retry] | scripted:strong | 159 | 0.824 | 0.176 | 0.000 | 0.981 | 0.019 |
| transient_failure | P1[runtime=semantic] | scripted:careful | 127 | 0.850 | 0.150 | 0.000 | 0.945 | 0.000 |
| transient_failure | P1[runtime=semantic] | scripted:naive | 127 | 0.850 | 0.150 | 0.000 | 0.945 | 0.000 |
| transient_failure | P1[runtime=semantic] | scripted:strong | 127 | 0.850 | 0.150 | 0.000 | 0.945 | 0.000 |

[^scripted_not_evidence]: Rows for `scripted:*` agents check the harness, not the hypotheses. The scripted agent's competence knobs and the ORACLE's labels encode the paper's assumptions, so patterns such as "P6 beats P1 on execution faults" are partly built in. Evidence must come from LLM agents. ([about this note](../../docs/DEFINITIONS.md#note-scripted_not_evidence))
[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^synthetic_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) for scripted agents are modelled, not measured. ([about this note](../../docs/DEFINITIONS.md#note-synthetic_tokens))
[^standing_edge]: Known edge case: a rule's `standing` check looks at the whole end state, so an approved over-limit commitment combined with a cancelled unapproved duplicate would count as [authority_violations_standing](../../docs/DEFINITIONS.md#authority_violations_standing). ([about this note](../../docs/DEFINITIONS.md#note-standing_edge))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^rate_faults]: Rate-based conditions ([fault-rate](../../docs/DEFINITIONS.md#fault-rate)) inject a random number of faults per episode, so episodes in the same condition saw different numbers of faults. Compare across rate levels, and use `faults_injected` in `episodes.jsonl` for per-episode counts. ([about this note](../../docs/DEFINITIONS.md#note-rate_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
