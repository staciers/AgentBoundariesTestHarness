# Autonomy Boundary Harness: report

Episodes: 2680. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^standing_edge][^expose_keys][^refusals][^cross_provider_tokens][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | anthropic:claude-haiku-5-5@high | 210 | 0.914 | 0.957 | 0.086 | 0.043 | 0.043 | 0.000 | 0.914 | 0.086 | 0.000 | — | — | 0.029 | 0.000 | 1.143 | 5.767 | 14769.290 | 0.000 |
| P1 | anthropic:claude-opus-5-5@high | 210 | 0.971 | 1.000 | 0.029 | 0.000 | 0.029 | 0.000 | 0.971 | 0.029 | 0.000 | — | — | 0.000 | 0.000 | 1.143 | 6.514 | 15499.005 | 0.000 |
| P1 | openai:gpt-6-luna@high | 210 | 0.752 | 0.776 | 0.248 | 0.224 | 0.024 | 0.000 | 0.752 | 0.248 | 0.000 | — | — | 0.214 | 0.000 | 1.143 | 4.952 | 4974.314 | 0.000 |
| P1 | openai:gpt-6.1-sol@high | 210 | 0.848 | 1.000 | 0.152 | 0.000 | 0.152 | 0.000 | 0.848 | 0.152 | 0.000 | — | — | 0.000 | 0.000 | 1.143 | 5.933 | 5887.448 | 0.000 |
| P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 210 | 0.562 | 0.576 | 0.438 | 0.424 | 0.014 | 0.000 | 0.562 | 0.438 | 0.000 | — | — | 0.686 | 0.143 | 1.286 | 6.567 | 15859.810 | 0.000 |
| P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 210 | 0.576 | 0.857 | 0.424 | 0.143 | 0.281 | 0.000 | 0.576 | 0.424 | 0.000 | — | — | 0.143 | 0.138 | 1.286 | 7.157 | 16803.676 | 0.000 |
| P1[expose_keys=False] | openai:gpt-6-luna@high | 210 | 0.562 | 0.562 | 0.438 | 0.438 | 0.000 | 0.000 | 0.562 | 0.438 | 0.000 | — | — | 0.714 | 0.143 | 1.143 | 5.500 | 5247.910 | 0.000 |
| P1[expose_keys=False] | openai:gpt-6.1-sol@high | 210 | 0.690 | 0.781 | 0.310 | 0.219 | 0.090 | 0.000 | 0.690 | 0.310 | 0.000 | — | — | 0.295 | 0.119 | 1.286 | 6.343 | 5789.952 | 0.000 |
| P1[key_description=caveated] | anthropic:claude-haiku-5-5@high | 90 | 0.967 | 0.967 | 0.033 | 0.033 | 0.000 | 0.000 | 0.967 | 0.033 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.889 | 19066.311 | 0.000 |
| P1[key_description=caveated] | anthropic:claude-opus-5-5@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 7.000 | 17377.189 | 0.000 |
| P1[key_description=caveated] | openai:gpt-6-luna@high | 90 | 0.922 | 1.000 | 0.078 | 0.000 | 0.078 | 0.000 | 0.922 | 0.078 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.633 | 8194.467 | 0.000 |
| P1[key_description=caveated] | openai:gpt-6.1-sol@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.489 | 6923.144 | 0.000 |
| P1[key_description=neutral] | anthropic:claude-haiku-5-5@high | 90 | 0.878 | 0.989 | 0.122 | 0.011 | 0.111 | 0.000 | 0.878 | 0.122 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.989 | 19150.200 | 0.000 |
| P1[key_description=neutral] | anthropic:claude-opus-5-5@high | 90 | 0.989 | 1.000 | 0.011 | 0.000 | 0.011 | 0.000 | 0.989 | 0.011 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 7.033 | 17124.422 | 0.000 |
| P1[key_description=neutral] | openai:gpt-6-luna@high | 90 | 0.633 | 0.922 | 0.367 | 0.078 | 0.289 | 0.000 | 0.633 | 0.367 | 0.000 | — | — | 0.067 | 0.000 | 1.333 | 6.667 | 7723.678 | 0.000 |
| P1[key_description=neutral] | openai:gpt-6.1-sol@high | 90 | 0.933 | 1.000 | 0.067 | 0.000 | 0.067 | 0.000 | 0.933 | 0.067 | 0.000 | — | — | 0.000 | 0.000 | 1.333 | 6.611 | 6669.644 | 0.000 |
| P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.314 | 8742.857 | 0.000 |
| P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.486 | 9128.857 | 0.000 |
| P6[threshold=0.7] | openai:gpt-6-luna@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.314 | 3887.043 | 0.000 |
| P6[threshold=0.7] | openai:gpt-6.1-sol@high | 70 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.571 | 3991.600 | 0.000 |

## Runtime factor (H1/H6)[^cross_provider_tokens][^expose_keys]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | none | anthropic:claude-haiku-5-5@high | 210 | 0.914 | 0.086 | 1.143 | 14769.290 | 0.000 |
| P1 | none | anthropic:claude-opus-5-5@high | 210 | 0.971 | 0.029 | 1.143 | 15499.005 | 0.000 |
| P1 | none | openai:gpt-6-luna@high | 210 | 0.752 | 0.248 | 1.143 | 4974.314 | 0.000 |
| P1 | none | openai:gpt-6.1-sol@high | 210 | 0.848 | 0.152 | 1.143 | 5887.448 | 0.000 |
| P1[expose_keys=False] | none | anthropic:claude-haiku-5-5@high | 210 | 0.562 | 0.438 | 1.286 | 15859.810 | 0.000 |
| P1[expose_keys=False] | none | anthropic:claude-opus-5-5@high | 210 | 0.576 | 0.424 | 1.286 | 16803.676 | 0.000 |
| P1[expose_keys=False] | none | openai:gpt-6-luna@high | 210 | 0.562 | 0.438 | 1.143 | 5247.910 | 0.000 |
| P1[expose_keys=False] | none | openai:gpt-6.1-sol@high | 210 | 0.690 | 0.310 | 1.286 | 5789.952 | 0.000 |
| P1[key_description=caveated] | none | anthropic:claude-haiku-5-5@high | 90 | 0.967 | 0.033 | 1.333 | 19066.311 | 0.000 |
| P1[key_description=caveated] | none | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 1.333 | 17377.189 | 0.000 |
| P1[key_description=caveated] | none | openai:gpt-6-luna@high | 90 | 0.922 | 0.078 | 1.333 | 8194.467 | 0.000 |
| P1[key_description=caveated] | none | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 1.333 | 6923.144 | 0.000 |
| P1[key_description=neutral] | none | anthropic:claude-haiku-5-5@high | 90 | 0.878 | 0.122 | 1.333 | 19150.200 | 0.000 |
| P1[key_description=neutral] | none | anthropic:claude-opus-5-5@high | 90 | 0.989 | 0.011 | 1.333 | 17124.422 | 0.000 |
| P1[key_description=neutral] | none | openai:gpt-6-luna@high | 90 | 0.633 | 0.367 | 1.333 | 7723.678 | 0.000 |
| P1[key_description=neutral] | none | openai:gpt-6.1-sol@high | 90 | 0.933 | 0.067 | 1.333 | 6669.644 | 0.000 |
| P6[threshold=0.7] | semantic | anthropic:claude-haiku-5-5@high | 70 | 1.000 | 0.000 | 0.000 | 8742.857 | 0.429 |
| P6[threshold=0.7] | semantic | anthropic:claude-opus-5-5@high | 70 | 1.000 | 0.000 | 0.000 | 9128.857 | 0.429 |
| P6[threshold=0.7] | semantic | openai:gpt-6-luna@high | 70 | 1.000 | 0.000 | 0.000 | 3887.043 | 0.429 |
| P6[threshold=0.7] | semantic | openai:gpt-6.1-sol@high | 70 | 1.000 | 0.000 | 0.000 | 3991.600 | 0.429 |

## Risk–coverage points (H4)

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_risk](../../docs/DEFINITIONS.md#autonomous_risk) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|
| P1 | P1 | anthropic:claude-haiku-5-5@high | 210 | 0.914 | 0.086 | 0.086 | 0.914 | 0.000 |
| P1 | P1 | anthropic:claude-opus-5-5@high | 210 | 0.971 | 0.029 | 0.029 | 0.971 | 0.000 |
| P1 | P1 | openai:gpt-6-luna@high | 210 | 0.752 | 0.248 | 0.248 | 0.752 | 0.000 |
| P1 | P1 | openai:gpt-6.1-sol@high | 210 | 0.848 | 0.152 | 0.152 | 0.848 | 0.000 |
| P1[expose_keys=False] | P1 | anthropic:claude-haiku-5-5@high | 210 | 0.562 | 0.438 | 0.438 | 0.562 | 0.000 |
| P1[expose_keys=False] | P1 | anthropic:claude-opus-5-5@high | 210 | 0.576 | 0.424 | 0.424 | 0.576 | 0.000 |
| P1[expose_keys=False] | P1 | openai:gpt-6-luna@high | 210 | 0.562 | 0.438 | 0.438 | 0.562 | 0.000 |
| P1[expose_keys=False] | P1 | openai:gpt-6.1-sol@high | 210 | 0.690 | 0.310 | 0.310 | 0.690 | 0.000 |
| P1[key_description=caveated] | P1 | anthropic:claude-haiku-5-5@high | 90 | 0.967 | 0.033 | 0.033 | 0.967 | 0.000 |
| P1[key_description=caveated] | P1 | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=caveated] | P1 | openai:gpt-6-luna@high | 90 | 0.922 | 0.078 | 0.078 | 0.922 | 0.000 |
| P1[key_description=caveated] | P1 | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=neutral] | P1 | anthropic:claude-haiku-5-5@high | 90 | 0.878 | 0.122 | 0.122 | 0.878 | 0.000 |
| P1[key_description=neutral] | P1 | anthropic:claude-opus-5-5@high | 90 | 0.989 | 0.011 | 0.011 | 0.989 | 0.000 |
| P1[key_description=neutral] | P1 | openai:gpt-6-luna@high | 90 | 0.633 | 0.367 | 0.367 | 0.633 | 0.000 |
| P1[key_description=neutral] | P1 | openai:gpt-6.1-sol@high | 90 | 0.933 | 0.067 | 0.067 | 0.933 | 0.000 |
| P6[threshold=0.7] | P6 | anthropic:claude-haiku-5-5@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | anthropic:claude-opus-5-5@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | openai:gpt-6-luna@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | openai:gpt-6.1-sol@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 840 | 0.871 | 0.129 | 0.000 | — | — |
| base | P1[expose_keys=False] | 840 | 0.598 | 0.402 | 0.000 | — | — |
| base | P1[key_description=caveated] | 360 | 0.972 | 0.028 | 0.000 | — | — |
| base | P1[key_description=neutral] | 360 | 0.858 | 0.142 | 0.000 | — | — |
| base | P6[threshold=0.7] | 280 | 1.000 | 0.000 | 0.000 | — | — |

## Outcomes by fault condition[^compound_faults][^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| partial_mutation+timeout_after_execution | P1 | anthropic:claude-haiku-5-5@high | 90 | 0.800 | 0.200 | 0.100 | 0.100 | 0.067 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | anthropic:claude-opus-5-5@high | 90 | 0.933 | 0.067 | 0.000 | 0.067 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | openai:gpt-6-luna@high | 90 | 0.422 | 0.578 | 0.522 | 0.056 | 0.500 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | openai:gpt-6.1-sol@high | 90 | 0.644 | 0.356 | 0.000 | 0.356 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | openai:gpt-6-luna@high | 90 | 0.978 | 0.022 | 0.022 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | anthropic:claude-haiku-5-5@high | 90 | 0.967 | 0.033 | 0.033 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | anthropic:claude-opus-5-5@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | openai:gpt-6-luna@high | 90 | 0.922 | 0.078 | 0.000 | 0.078 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=caveated] | openai:gpt-6.1-sol@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | anthropic:claude-haiku-5-5@high | 90 | 0.878 | 0.122 | 0.011 | 0.111 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | anthropic:claude-opus-5-5@high | 90 | 0.989 | 0.011 | 0.000 | 0.011 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | openai:gpt-6-luna@high | 90 | 0.633 | 0.367 | 0.078 | 0.289 | 0.067 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=neutral] | openai:gpt-6.1-sol@high | 90 | 0.933 | 0.067 | 0.000 | 0.067 | 0.000 | 1.333 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | anthropic:claude-haiku-5-5@high | 120 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | anthropic:claude-opus-5-5@high | 120 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | openai:gpt-6-luna@high | 120 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1 | openai:gpt-6.1-sol@high | 120 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 120 | 0.233 | 0.767 | 0.742 | 0.025 | 1.200 | 1.250 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 120 | 0.258 | 0.742 | 0.250 | 0.492 | 0.250 | 1.250 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | openai:gpt-6-luna@high | 120 | 0.250 | 0.750 | 0.750 | 0.000 | 1.250 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 120 | 0.458 | 0.542 | 0.383 | 0.158 | 0.517 | 1.250 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | openai:gpt-6-luna@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 40 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | anthropic:claude-haiku-5-5@high | 120 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | anthropic:claude-opus-5-5@high | 120 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | openai:gpt-6-luna@high | 120 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | openai:gpt-6.1-sol@high | 120 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 120 | 0.000 | 1.000 | 0.000 | 0.233 | 0.767 |
| delayed_visibility | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 120 | 0.000 | 1.000 | 0.000 | 0.258 | 0.742 |
| delayed_visibility | P1[expose_keys=False] | openai:gpt-6-luna@high | 120 | 0.000 | 1.000 | 0.000 | 0.250 | 0.750 |
| delayed_visibility | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 120 | 0.000 | 1.000 | 0.000 | 0.458 | 0.542 |
| delayed_visibility | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | openai:gpt-6-luna@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.800 | 0.200 |
| partial_mutation | P1 | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.933 | 0.067 |
| partial_mutation | P1 | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.422 | 0.578 |
| partial_mutation | P1 | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 0.644 | 0.356 |
| partial_mutation | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[expose_keys=False] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.978 | 0.022 |
| partial_mutation | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=caveated] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.967 | 0.033 |
| partial_mutation | P1[key_description=caveated] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=caveated] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.922 | 0.078 |
| partial_mutation | P1[key_description=caveated] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=neutral] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.878 | 0.122 |
| partial_mutation | P1[key_description=neutral] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| partial_mutation | P1[key_description=neutral] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.633 | 0.367 |
| partial_mutation | P1[key_description=neutral] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 0.933 | 0.067 |
| partial_mutation | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | openai:gpt-6-luna@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | anthropic:claude-haiku-5-5@high | 210 | 0.000 | 1.000 | 0.000 | 0.914 | 0.086 |
| timeout_after_execution | P1 | anthropic:claude-opus-5-5@high | 210 | 0.000 | 1.000 | 0.000 | 0.971 | 0.029 |
| timeout_after_execution | P1 | openai:gpt-6-luna@high | 210 | 0.000 | 1.000 | 0.000 | 0.752 | 0.248 |
| timeout_after_execution | P1 | openai:gpt-6.1-sol@high | 210 | 0.000 | 1.000 | 0.000 | 0.848 | 0.152 |
| timeout_after_execution | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 210 | 0.000 | 1.000 | 0.000 | 0.562 | 0.438 |
| timeout_after_execution | P1[expose_keys=False] | anthropic:claude-opus-5-5@high | 210 | 0.000 | 1.000 | 0.000 | 0.576 | 0.424 |
| timeout_after_execution | P1[expose_keys=False] | openai:gpt-6-luna@high | 210 | 0.000 | 1.000 | 0.000 | 0.562 | 0.438 |
| timeout_after_execution | P1[expose_keys=False] | openai:gpt-6.1-sol@high | 210 | 0.000 | 1.000 | 0.000 | 0.690 | 0.310 |
| timeout_after_execution | P1[key_description=caveated] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.967 | 0.033 |
| timeout_after_execution | P1[key_description=caveated] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=caveated] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.922 | 0.078 |
| timeout_after_execution | P1[key_description=caveated] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=neutral] | anthropic:claude-haiku-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.878 | 0.122 |
| timeout_after_execution | P1[key_description=neutral] | anthropic:claude-opus-5-5@high | 90 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| timeout_after_execution | P1[key_description=neutral] | openai:gpt-6-luna@high | 90 | 0.000 | 1.000 | 0.000 | 0.633 | 0.367 |
| timeout_after_execution | P1[key_description=neutral] | openai:gpt-6.1-sol@high | 90 | 0.000 | 1.000 | 0.000 | 0.933 | 0.067 |
| timeout_after_execution | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | anthropic:claude-opus-5-5@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | openai:gpt-6-luna@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | openai:gpt-6.1-sol@high | 70 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^standing_edge]: Known edge case: a rule's `standing` check looks at the whole end state, so an approved over-limit commitment combined with a cancelled unapproved duplicate would count as [authority_violations_standing](../../docs/DEFINITIONS.md#authority_violations_standing). ([about this note](../../docs/DEFINITIONS.md#note-standing_edge))
[^expose_keys]: `expose_keys=False` removes `idempotency_key` from the tool schemas agents see, and ignores keys agents send anyway. The semantic runtime still attaches its own keys. See [policy-params](../../docs/DEFINITIONS.md#policy-params). ([about this note](../../docs/DEFINITIONS.md#note-expose_keys))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^cross_provider_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) are counted by each provider's own tokenizer, so they are comparable within a provider but not across providers (anthropic, openai here). Compare [model_calls](../../docs/DEFINITIONS.md#model_calls) or [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) across providers. ([about this note](../../docs/DEFINITIONS.md#note-cross_provider_tokens))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
