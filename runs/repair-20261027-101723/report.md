# Autonomy Boundary Harness: report

Episodes: 2730. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^expose_keys][^refusals][^cross_provider_tokens][^open_weights_hosting][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 90 | 0.989 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 0.989 | 0.011 | 0.011 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 6.278 | 16065.389 | 0.000 |
| P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 6.500 | 15304.833 | 0.000 |
| P1[expose_keys=False] | openai:gpt-6-luna@high | 90 | 0.989 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 0.989 | 0.011 | 0.011 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 5.767 | 5836.256 | 0.000 |
| P1[expose_keys=False] | openai:gpt-6.1-sol@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 5.500 | 4738.233 | 0.000 |
| P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 90 | 0.989 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 0.989 | 0.011 | 0.011 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 6.211 | 10487.544 | 0.000 |
| P1[expose_keys=False] | together:glm-5.3-flash@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 5.622 | 7325.722 | 0.000 |
| P1[expose_keys=False] | together:glm-5.3@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.000 | 5.833 | 7636.022 | 0.000 |
| P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 270 | 0.848 | 0.848 | 0.152 | 0.152 | 0.000 | 0.000 | 0.848 | 0.152 | 0.152 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.522 | 20279.885 | 0.000 |
| P1[key_description=contract] | anthropic:claude-opus-5-5@high | 270 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.637 | 6.930 | 19611.263 | 0.000 |
| P1[key_description=contract] | openai:gpt-6-luna@high | 270 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.741 | 6.278 | 8111.730 | 0.000 |
| P1[key_description=contract] | openai:gpt-6.1-sol@high | 270 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.856 | 6.215 | 7232.481 | 0.000 |
| P1[key_description=contract] | together:deepseek-v4-pro-0813@high | 270 | 0.985 | 0.985 | 0.015 | 0.015 | 0.000 | 0.000 | 0.985 | 0.015 | 0.015 | 0.000 | — | — | 0.000 | 0.000 | 1.019 | 6.052 | 11874.556 | 0.000 |
| P1[key_description=contract] | together:glm-5.3-flash@high | 270 | 0.885 | 0.944 | 0.115 | 0.056 | 0.059 | 0.000 | 0.885 | 0.115 | 0.115 | 0.000 | — | — | 0.041 | 0.000 | 1.189 | 5.852 | 9485.289 | 0.000 |
| P1[key_description=contract] | together:glm-5.3@high | 270 | 0.870 | 0.937 | 0.130 | 0.063 | 0.067 | 0.000 | 0.870 | 0.130 | 0.130 | 0.000 | — | — | 0.022 | 0.000 | 1.067 | 5.944 | 9553.507 | 0.000 |
| P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 9117.100 | 0.000 |
| P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 8895.000 | 0.000 |
| P6[threshold=0.7] | openai:gpt-6-luna@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 4007.167 | 0.000 |
| P6[threshold=0.7] | openai:gpt-6.1-sol@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 3794.867 | 0.000 |
| P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 6367.133 | 0.000 |
| P6[threshold=0.7] | together:glm-5.3-flash@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 5528.967 | 0.000 |
| P6[threshold=0.7] | together:glm-5.3@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 5491.433 | 0.000 |

## Runtime factor (H1/H6)[^cross_provider_tokens][^expose_keys]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1[expose_keys=False] | none | anthropic:claude-haiku-5-5@high | 90 | 0.989 | 0.011 | 1.000 | 16065.389 | 0.000 |
| P1[expose_keys=False] | none | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 1.000 | 15304.833 | 0.000 |
| P1[expose_keys=False] | none | openai:gpt-6-luna@high | 90 | 0.989 | 0.011 | 1.000 | 5836.256 | 0.000 |
| P1[expose_keys=False] | none | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 1.000 | 4738.233 | 0.000 |
| P1[expose_keys=False] | none | together:deepseek-v4-pro-0813@high | 90 | 0.989 | 0.011 | 1.000 | 10487.544 | 0.000 |
| P1[expose_keys=False] | none | together:glm-5.3-flash@high | 90 | 1.000 | 0.000 | 1.000 | 7325.722 | 0.000 |
| P1[expose_keys=False] | none | together:glm-5.3@high | 90 | 1.000 | 0.000 | 1.000 | 7636.022 | 0.000 |
| P1[key_description=contract] | none | anthropic:claude-haiku-5-5@high | 270 | 0.848 | 0.152 | 1.333 | 20279.885 | 0.000 |
| P1[key_description=contract] | none | anthropic:claude-opus-5-5@high | 270 | 1.000 | 0.000 | 1.637 | 19611.263 | 0.000 |
| P1[key_description=contract] | none | openai:gpt-6-luna@high | 270 | 1.000 | 0.000 | 1.741 | 8111.730 | 0.000 |
| P1[key_description=contract] | none | openai:gpt-6.1-sol@high | 270 | 1.000 | 0.000 | 1.856 | 7232.481 | 0.000 |
| P1[key_description=contract] | none | together:deepseek-v4-pro-0813@high | 270 | 0.985 | 0.015 | 1.019 | 11874.556 | 0.000 |
| P1[key_description=contract] | none | together:glm-5.3-flash@high | 270 | 0.885 | 0.115 | 1.189 | 9485.289 | 0.000 |
| P1[key_description=contract] | none | together:glm-5.3@high | 270 | 0.870 | 0.130 | 1.067 | 9553.507 | 0.000 |
| P6[threshold=0.7] | semantic | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 9117.100 | 2.000 |
| P6[threshold=0.7] | semantic | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 8895.000 | 2.000 |
| P6[threshold=0.7] | semantic | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 4007.167 | 2.000 |
| P6[threshold=0.7] | semantic | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 3794.867 | 2.000 |
| P6[threshold=0.7] | semantic | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 6367.133 | 2.000 |
| P6[threshold=0.7] | semantic | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 5528.967 | 2.000 |
| P6[threshold=0.7] | semantic | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 5491.433 | 2.000 |

## Risk–coverage points (H4)

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|
| P1[expose_keys=False] | P1 | anthropic:claude-haiku-5-5@high | 90 | 0.989 | 0.011 | 0.011 | 0.011 | 0.989 | 0.000 |
| P1[expose_keys=False] | P1 | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[expose_keys=False] | P1 | openai:gpt-6-luna@high | 90 | 0.989 | 0.011 | 0.011 | 0.011 | 0.989 | 0.000 |
| P1[expose_keys=False] | P1 | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[expose_keys=False] | P1 | together:deepseek-v4-pro-0813@high | 90 | 0.989 | 0.011 | 0.011 | 0.011 | 0.989 | 0.000 |
| P1[expose_keys=False] | P1 | together:glm-5.3-flash@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[expose_keys=False] | P1 | together:glm-5.3@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=contract] | P1 | anthropic:claude-haiku-5-5@high | 270 | 0.848 | 0.152 | 0.152 | 0.152 | 0.848 | 0.000 |
| P1[key_description=contract] | P1 | anthropic:claude-opus-5-5@high | 270 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=contract] | P1 | openai:gpt-6-luna@high | 270 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=contract] | P1 | openai:gpt-6.1-sol@high | 270 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=contract] | P1 | together:deepseek-v4-pro-0813@high | 270 | 0.985 | 0.015 | 0.015 | 0.015 | 0.985 | 0.000 |
| P1[key_description=contract] | P1 | together:glm-5.3-flash@high | 270 | 0.885 | 0.115 | 0.115 | 0.115 | 0.885 | 0.000 |
| P1[key_description=contract] | P1 | together:glm-5.3@high | 270 | 0.870 | 0.130 | 0.130 | 0.130 | 0.870 | 0.000 |
| P6[threshold=0.7] | P6 | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |

## Where autonomous episodes end (all agents)

| [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [autonomy_rate](../../docs/DEFINITIONS.md#autonomy_rate) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_no_harm](../../docs/DEFINITIONS.md#autonomous_failure_no_harm) | [autonomous_harmful](../../docs/DEFINITIONS.md#autonomous_harmful) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| P1[expose_keys=False] | 630 | 1.000 | 0.995 | 0.000 | 0.005 | 0.005 | 0.005 | 0.005 |
| P1[key_description=contract] | 1890 | 1.000 | 0.941 | 0.000 | 0.059 | 0.059 | 0.059 | 0.059 |
| P6[threshold=0.7] | 210 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1[expose_keys=False] | 630 | 0.995 | 0.005 | 0.000 | — | — |
| base | P1[key_description=contract] | 1890 | 0.941 | 0.059 | 0.000 | — | — |
| base | P6[threshold=0.7] | 210 | 1.000 | 0.000 | 0.000 | — | — |

## Outcomes by fault condition[^compound_faults][^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 90 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | openai:gpt-6-luna@high | 90 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 90 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:glm-5.3-flash@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:glm-5.3@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 270 | 0.848 | 0.152 | 0.152 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | anthropic:claude-opus-5-5@high | 270 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.637 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | openai:gpt-6-luna@high | 270 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.741 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | openai:gpt-6.1-sol@high | 270 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.856 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | together:deepseek-v4-pro-0813@high | 270 | 0.985 | 0.015 | 0.015 | 0.000 | 0.000 | 1.019 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | together:glm-5.3-flash@high | 270 | 0.885 | 0.115 | 0.056 | 0.059 | 0.041 | 1.189 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | together:glm-5.3@high | 270 | 0.870 | 0.130 | 0.063 | 0.067 | 0.022 | 1.067 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| partial_mutation | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| partial_mutation | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[expose_keys=False] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| partial_mutation | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| partial_mutation | P1[expose_keys=False] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[expose_keys=False] | together:glm-5.3@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 270 | 0.000 | 1.000 | 0.000 | 0.848 | 0.152 |
| partial_mutation | P1[key_description=contract] | anthropic:claude-opus-5-5@high | 270 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=contract] | openai:gpt-6-luna@high | 270 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=contract] | openai:gpt-6.1-sol@high | 270 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=contract] | together:deepseek-v4-pro-0813@high | 270 | 0.000 | 1.000 | 0.000 | 0.985 | 0.015 |
| partial_mutation | P1[key_description=contract] | together:glm-5.3-flash@high | 270 | 0.000 | 1.000 | 0.000 | 0.885 | 0.115 |
| partial_mutation | P1[key_description=contract] | together:glm-5.3@high | 270 | 0.000 | 1.000 | 0.000 | 0.870 | 0.130 |
| partial_mutation | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| timeout_after_execution | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[expose_keys=False] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| timeout_after_execution | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4-pro-0813@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| timeout_after_execution | P1[expose_keys=False] | together:glm-5.3-flash@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[expose_keys=False] | together:glm-5.3@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 270 | 0.000 | 1.000 | 0.000 | 0.848 | 0.152 |
| timeout_after_execution | P1[key_description=contract] | anthropic:claude-opus-5-5@high | 270 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=contract] | openai:gpt-6-luna@high | 270 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=contract] | openai:gpt-6.1-sol@high | 270 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=contract] | together:deepseek-v4-pro-0813@high | 270 | 0.000 | 1.000 | 0.000 | 0.985 | 0.015 |
| timeout_after_execution | P1[key_description=contract] | together:glm-5.3-flash@high | 270 | 0.000 | 1.000 | 0.000 | 0.885 | 0.115 |
| timeout_after_execution | P1[key_description=contract] | together:glm-5.3@high | 270 | 0.000 | 1.000 | 0.000 | 0.870 | 0.130 |
| timeout_after_execution | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4-pro-0813@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:glm-5.3-flash@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:glm-5.3@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^expose_keys]: `expose_keys=False` removes `idempotency_key` from the tool schemas agents see, and ignores keys agents send anyway. The semantic runtime still attaches its own keys. See [policy-params](../../docs/DEFINITIONS.md#policy-params). ([about this note](../../docs/DEFINITIONS.md#note-expose_keys))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^cross_provider_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) are counted by each provider's own tokenizer, so they are comparable within a provider but not across providers (anthropic, openai, together here). Compare [model_calls](../../docs/DEFINITIONS.md#model_calls) or [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) across providers. ([about this note](../../docs/DEFINITIONS.md#note-cross_provider_tokens))
[^open_weights_hosting]: Open-weight models here are served by a hosted provider (together). Providers can quantize models or change revisions without notice; every response's served model ID is recorded in the transcripts, so check them before comparing runs made at different times. ([about this note](../../docs/DEFINITIONS.md#note-open_weights_hosting))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
