# Autonomy Boundary Harness: report

Episodes: 252. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^small_samples][^standing_edge][^refusals][^cross_provider_tokens][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 63 | 0.984 | 0.984 | 0.016 | 0.016 | 0.000 | 0.000 | 0.984 | 0.016 | 0.000 | — | — | 0.016 | 0.016 | 0.143 | 4.556 | 13005.667 | 0.000 |
| P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 63 | 0.984 | 0.984 | 0.016 | 0.016 | 0.000 | 0.000 | 0.984 | 0.016 | 0.000 | — | — | 0.000 | 0.016 | 0.254 | 4.587 | 12221.540 | 0.000 |
| P1[runtime=semantic] | openai:gpt-6-luna@high | 63 | 0.984 | 0.984 | 0.016 | 0.016 | 0.000 | 0.000 | 0.984 | 0.016 | 0.000 | — | — | 0.000 | 0.016 | 0.143 | 4.476 | 4901.413 | 0.000 |
| P1[runtime=semantic] | openai:gpt-6.1-sol@high | 63 | 0.984 | 0.984 | 0.016 | 0.016 | 0.000 | 0.000 | 0.984 | 0.016 | 0.000 | — | — | 0.000 | 0.016 | 0.143 | 4.698 | 5007.063 | 0.000 |

## Runtime factor (H1/H6)[^cross_provider_tokens]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1[runtime=semantic] | semantic | anthropic:claude-haiku-5-5@high | 63 | 0.984 | 0.016 | 0.143 | 13005.667 | 0.492 |
| P1[runtime=semantic] | semantic | anthropic:claude-opus-5-5@high | 63 | 0.984 | 0.016 | 0.254 | 12221.540 | 0.492 |
| P1[runtime=semantic] | semantic | openai:gpt-6-luna@high | 63 | 0.984 | 0.016 | 0.143 | 4901.413 | 0.492 |
| P1[runtime=semantic] | semantic | openai:gpt-6.1-sol@high | 63 | 0.984 | 0.016 | 0.143 | 5007.063 | 0.492 |

## Risk–coverage points (H4)[^small_samples]

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|
| P1[runtime=semantic] | P1 | anthropic:claude-haiku-5-5@high | 63 | 0.984 | 0.016 | 0.016 | 0.984 | 0.000 |
| P1[runtime=semantic] | P1 | anthropic:claude-opus-5-5@high | 63 | 0.984 | 0.016 | 0.016 | 0.984 | 0.000 |
| P1[runtime=semantic] | P1 | openai:gpt-6-luna@high | 63 | 0.984 | 0.016 | 0.016 | 0.984 | 0.000 |
| P1[runtime=semantic] | P1 | openai:gpt-6.1-sol@high | 63 | 0.984 | 0.016 | 0.016 | 0.984 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1[runtime=semantic] | 252 | 0.984 | 0.016 | 0.000 | — | — |

## Outcomes by fault condition[^harm_split][^small_samples]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.200 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.200 | 0.000 |
| none | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.250 | 0.000 |
| partial_mutation | P1[runtime=semantic] | openai:gpt-6-luna@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_response | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_response | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.200 | 0.000 |
| partial_response | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_response | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.250 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | openai:gpt-6-luna@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 4 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.200 | 0.000 |
| rate_limited | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 0.800 | 0.200 | 0.200 | 0.000 | 0.200 | 0.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 0.800 | 0.200 | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 0.800 | 0.200 | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 0.800 | 0.200 | 0.200 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.200 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 4 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 4 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | openai:gpt-6-luna@high | 4 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 4 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 16 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 16 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | openai:gpt-6-luna@high | 16 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 16 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| task_invalid_result | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| task_invalid_result | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| task_invalid_result | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| timeout_after_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | openai:gpt-6-luna@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 5 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^small_samples]: Small groups: the smallest group in these tables has n=4. At that size a 95% interval for a rate near 50% is about ±49%. Wilson intervals for [success](../../docs/DEFINITIONS.md#success) are in the CSVs ([success_ci](../../docs/DEFINITIONS.md#success_ci)). ([about this note](../../docs/DEFINITIONS.md#note-small_samples))
[^standing_edge]: Known edge case: a rule's `standing` check looks at the whole end state, so an approved over-limit commitment combined with a cancelled unapproved duplicate would count as [authority_violations_standing](../../docs/DEFINITIONS.md#authority_violations_standing). ([about this note](../../docs/DEFINITIONS.md#note-standing_edge))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^cross_provider_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) are counted by each provider's own tokenizer, so they are comparable within a provider but not across providers (anthropic, openai here). Compare [model_calls](../../docs/DEFINITIONS.md#model_calls) or [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) across providers. ([about this note](../../docs/DEFINITIONS.md#note-cross_provider_tokens))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
