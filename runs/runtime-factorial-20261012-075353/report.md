# Autonomy Boundary Harness: report[^scripted_not_evidence]

Episodes: 9000. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^synthetic_tokens][^standing_edge]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | scripted:careful | 3000 | 0.832 | 0.832 | 0.130 | 0.130 | 0.000 | 0.038 | 0.832 | 0.168 | 0.000 | — | — | 0.148 | 0.007 | 0.458 | 4.677 | 15531.900 | 0.000 |
| P1 | scripted:naive | 3000 | 0.634 | 0.634 | 0.255 | 0.255 | 0.000 | 0.111 | 0.634 | 0.366 | 0.000 | — | — | 0.327 | 0.048 | 0.496 | 4.461 | 14547.240 | 0.000 |
| P1 | scripted:strong | 3000 | 0.936 | 0.936 | 0.046 | 0.046 | 0.000 | 0.018 | 0.936 | 0.064 | 0.000 | — | — | 0.047 | 0.001 | 0.434 | 4.728 | 15773.190 | 0.000 |

## Runtime factor (H1/H6)[^synthetic_tokens]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | naive_retry | scripted:careful | 1000 | 0.732 | 0.237 | 0.395 | 15414.750 | 1.000 |
| P1 | naive_retry | scripted:naive | 1000 | 0.540 | 0.353 | 0.436 | 14435.100 | 1.000 |
| P1 | naive_retry | scripted:strong | 1000 | 0.896 | 0.093 | 0.354 | 15553.710 | 1.000 |
| P1 | none | scripted:careful | 1000 | 0.818 | 0.136 | 0.833 | 17303.400 | 0.000 |
| P1 | none | scripted:naive | 1000 | 0.528 | 0.365 | 0.896 | 16243.020 | 0.000 |
| P1 | none | scripted:strong | 1000 | 0.928 | 0.041 | 0.806 | 17589.150 | 0.000 |
| P1 | semantic | scripted:careful | 1000 | 0.947 | 0.016 | 0.146 | 13877.550 | 0.480 |
| P1 | semantic | scripted:naive | 1000 | 0.834 | 0.047 | 0.156 | 12963.600 | 0.480 |
| P1 | semantic | scripted:strong | 1000 | 0.984 | 0.005 | 0.142 | 14176.710 | 0.480 |

## Risk–coverage points (H4)

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|
| P1 | P1 | scripted:careful | 3000 | 0.832 | 0.168 | 0.130 | 0.832 | 0.000 |
| P1 | P1 | scripted:naive | 3000 | 0.634 | 0.366 | 0.255 | 0.634 | 0.000 |
| P1 | P1 | scripted:strong | 3000 | 0.936 | 0.064 | 0.046 | 0.936 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 9000 | 0.801 | 0.144 | 0.000 | — | — |

## Outcomes by fault condition[^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | scripted:careful | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1 | scripted:naive | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1 | scripted:strong | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1 | scripted:careful | 240 | 0.533 | 0.467 | 0.467 | 0.000 | 0.625 | 0.125 | 0.000 |
| duplicate_execution | P1 | scripted:naive | 240 | 0.458 | 0.542 | 0.542 | 0.000 | 0.833 | 0.167 | 0.000 |
| duplicate_execution | P1 | scripted:strong | 240 | 0.867 | 0.133 | 0.133 | 0.000 | 0.167 | 0.033 | 0.000 |
| malformed_response | P1 | scripted:careful | 240 | 0.713 | 0.287 | 0.287 | 0.000 | 0.446 | 0.412 | 0.000 |
| malformed_response | P1 | scripted:naive | 240 | 0.433 | 0.567 | 0.567 | 0.000 | 1.250 | 0.500 | 0.000 |
| malformed_response | P1 | scripted:strong | 240 | 0.933 | 0.067 | 0.067 | 0.000 | 0.083 | 0.350 | 0.000 |
| none | P1 | scripted:careful | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | scripted:naive | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | scripted:strong | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1 | scripted:careful | 180 | 0.556 | 0.361 | 0.361 | 0.000 | 0.361 | 0.333 | 0.000 |
| partial_mutation | P1 | scripted:naive | 180 | 0.556 | 0.444 | 0.444 | 0.000 | 0.444 | 0.333 | 0.000 |
| partial_mutation | P1 | scripted:strong | 180 | 0.556 | 0.333 | 0.333 | 0.000 | 0.333 | 0.333 | 0.000 |
| partial_response | P1 | scripted:careful | 240 | 0.892 | 0.108 | 0.108 | 0.000 | 0.133 | 0.700 | 0.000 |
| partial_response | P1 | scripted:naive | 240 | 0.408 | 0.592 | 0.592 | 0.000 | 0.833 | 0.833 | 0.000 |
| partial_response | P1 | scripted:strong | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.667 | 0.000 |
| persistent_unavailable | P1 | scripted:careful | 180 | 0.833 | 0.000 | 0.000 | 0.000 | 0.000 | 2.333 | 0.000 |
| persistent_unavailable | P1 | scripted:naive | 180 | 0.383 | 0.000 | 0.000 | 0.000 | 0.000 | 2.333 | 0.000 |
| persistent_unavailable | P1 | scripted:strong | 180 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 2.333 | 0.000 |
| precondition_changed | P1 | scripted:careful | 240 | 0.762 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | scripted:naive | 240 | 0.250 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | scripted:strong | 240 | 0.925 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | scripted:careful | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| rate_limited | P1 | scripted:naive | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| rate_limited | P1 | scripted:strong | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| task_invalid_result | P1 | scripted:careful | 240 | 0.750 | 0.200 | 0.200 | 0.000 | 0.000 | 0.075 | 0.000 |
| task_invalid_result | P1 | scripted:naive | 240 | 0.237 | 0.588 | 0.588 | 0.000 | 0.000 | 0.200 | 0.000 |
| task_invalid_result | P1 | scripted:strong | 240 | 0.925 | 0.062 | 0.062 | 0.000 | 0.000 | 0.025 | 0.000 |
| timeout_after_execution | P1 | scripted:careful | 240 | 0.713 | 0.287 | 0.287 | 0.000 | 0.379 | 0.412 | 0.000 |
| timeout_after_execution | P1 | scripted:naive | 240 | 0.433 | 0.567 | 0.567 | 0.000 | 0.833 | 0.500 | 0.000 |
| timeout_after_execution | P1 | scripted:strong | 240 | 0.933 | 0.067 | 0.067 | 0.000 | 0.083 | 0.350 | 0.000 |
| timeout_before_execution | P1 | scripted:careful | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| timeout_before_execution | P1 | scripted:naive | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| timeout_before_execution | P1 | scripted:strong | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| transient_failure | P1 | scripted:careful | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| transient_failure | P1 | scripted:naive | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |
| transient_failure | P1 | scripted:strong | 240 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.333 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | scripted:careful | 240 | 0.333 | 0.667 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | scripted:naive | 240 | 0.333 | 0.667 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | scripted:strong | 240 | 0.333 | 0.667 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1 | scripted:careful | 240 | 0.333 | 0.667 | 0.000 | 0.533 | 0.467 |
| duplicate_execution | P1 | scripted:naive | 240 | 0.333 | 0.667 | 0.000 | 0.458 | 0.542 |
| duplicate_execution | P1 | scripted:strong | 240 | 0.333 | 0.667 | 0.000 | 0.867 | 0.133 |
| malformed_response | P1 | scripted:careful | 240 | 0.604 | 0.396 | 0.000 | 0.713 | 0.287 |
| malformed_response | P1 | scripted:naive | 240 | 0.583 | 0.417 | 0.000 | 0.433 | 0.567 |
| malformed_response | P1 | scripted:strong | 240 | 0.650 | 0.350 | 0.000 | 0.933 | 0.067 |
| partial_mutation | P1 | scripted:careful | 180 | 0.667 | 0.333 | 0.000 | 0.556 | 0.361 |
| partial_mutation | P1 | scripted:naive | 180 | 0.667 | 0.333 | 0.000 | 0.556 | 0.444 |
| partial_mutation | P1 | scripted:strong | 180 | 0.667 | 0.333 | 0.000 | 0.556 | 0.333 |
| partial_response | P1 | scripted:careful | 240 | 0.333 | 0.667 | 0.000 | 0.892 | 0.108 |
| partial_response | P1 | scripted:naive | 240 | 0.333 | 0.667 | 0.000 | 0.408 | 0.592 |
| partial_response | P1 | scripted:strong | 240 | 0.333 | 0.667 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1 | scripted:careful | 1140 | 0.000 | 1.000 | 0.000 | 0.846 | 0.000 |
| persistent_unavailable | P1 | scripted:naive | 1140 | 0.000 | 1.000 | 0.000 | 0.408 | 0.000 |
| persistent_unavailable | P1 | scripted:strong | 1140 | 0.000 | 1.000 | 0.000 | 0.933 | 0.000 |
| precondition_changed | P1 | scripted:careful | 240 | 0.000 | 1.000 | 0.000 | 0.762 | 0.000 |
| precondition_changed | P1 | scripted:naive | 240 | 0.000 | 1.000 | 0.000 | 0.250 | 0.000 |
| precondition_changed | P1 | scripted:strong | 240 | 0.000 | 1.000 | 0.000 | 0.925 | 0.000 |
| rate_limited | P1 | scripted:careful | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | scripted:naive | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | scripted:strong | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | scripted:careful | 240 | 0.000 | 1.000 | 0.000 | 0.750 | 0.200 |
| task_invalid_result | P1 | scripted:naive | 240 | 0.000 | 1.000 | 0.000 | 0.237 | 0.588 |
| task_invalid_result | P1 | scripted:strong | 240 | 0.000 | 1.000 | 0.000 | 0.925 | 0.062 |
| timeout_after_execution | P1 | scripted:careful | 240 | 0.604 | 0.396 | 0.000 | 0.713 | 0.287 |
| timeout_after_execution | P1 | scripted:naive | 240 | 0.583 | 0.417 | 0.000 | 0.433 | 0.567 |
| timeout_after_execution | P1 | scripted:strong | 240 | 0.650 | 0.350 | 0.000 | 0.933 | 0.067 |
| timeout_before_execution | P1 | scripted:careful | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | scripted:naive | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | scripted:strong | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | scripted:careful | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | scripted:naive | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | scripted:strong | 240 | 0.667 | 0.333 | 0.000 | 1.000 | 0.000 |

[^scripted_not_evidence]: Rows for `scripted:*` agents check the harness, not the hypotheses. The scripted agent's competence knobs and the ORACLE's labels encode the paper's assumptions, so patterns such as "P6 beats P1 on execution faults" are partly built in. Evidence must come from LLM agents. ([about this note](../../docs/DEFINITIONS.md#note-scripted_not_evidence))
[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^synthetic_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) for scripted agents are modelled, not measured. ([about this note](../../docs/DEFINITIONS.md#note-synthetic_tokens))
[^standing_edge]: Known edge case: a rule's `standing` check looks at the whole end state, so an approved over-limit commitment combined with a cancelled unapproved duplicate would count as [authority_violations_standing](../../docs/DEFINITIONS.md#authority_violations_standing). ([about this note](../../docs/DEFINITIONS.md#note-standing_edge))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
