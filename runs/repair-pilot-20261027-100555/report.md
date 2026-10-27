# Autonomy Boundary Harness: report

Episodes: 90. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^refusals][^cross_provider_tokens][^open_weights_hosting][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 45 | 0.889 | 0.889 | 0.111 | 0.111 | 0.000 | 0.000 | 0.889 | 0.111 | 0.111 | 0.000 | — | — | 0.000 | 0.000 | 1.244 | 7.244 | 26587.578 | 0.000 |
| P1[key_description=contract] | together:glm-5.3-flash@high | 45 | 0.889 | 0.911 | 0.111 | 0.089 | 0.022 | 0.000 | 0.889 | 0.111 | 0.111 | 0.000 | — | — | 0.067 | 0.000 | 1.178 | 6.889 | 13744.978 | 0.000 |

## Runtime factor (H1/H6)[^cross_provider_tokens]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1[key_description=contract] | none | anthropic:claude-haiku-5-5@high | 45 | 0.889 | 0.111 | 1.244 | 26587.578 | 0.000 |
| P1[key_description=contract] | none | together:glm-5.3-flash@high | 45 | 0.889 | 0.111 | 1.178 | 13744.978 | 0.000 |

## Risk–coverage points (H4)

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|
| P1[key_description=contract] | P1 | anthropic:claude-haiku-5-5@high | 45 | 0.889 | 0.111 | 0.111 | 0.111 | 0.889 | 0.000 |
| P1[key_description=contract] | P1 | together:glm-5.3-flash@high | 45 | 0.889 | 0.111 | 0.111 | 0.111 | 0.889 | 0.000 |

## Where autonomous episodes end (all agents)

| [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [autonomy_rate](../../docs/DEFINITIONS.md#autonomy_rate) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_no_harm](../../docs/DEFINITIONS.md#autonomous_failure_no_harm) | [autonomous_harmful](../../docs/DEFINITIONS.md#autonomous_harmful) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| P1[key_description=contract] | 90 | 1.000 | 0.889 | 0.000 | 0.111 | 0.111 | 0.111 | 0.111 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1[key_description=contract] | 90 | 0.889 | 0.111 | 0.000 | — | — |

## Outcomes by fault condition[^compound_faults][^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| partial_mutation+timeout_after_execution | P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 45 | 0.889 | 0.111 | 0.111 | 0.000 | 0.000 | 1.244 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | together:glm-5.3-flash@high | 45 | 0.889 | 0.111 | 0.089 | 0.022 | 0.067 | 1.178 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| partial_mutation | P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 45 | 0.000 | 1.000 | 0.000 | 0.889 | 0.111 |
| partial_mutation | P1[key_description=contract] | together:glm-5.3-flash@high | 45 | 0.000 | 1.000 | 0.000 | 0.889 | 0.111 |
| timeout_after_execution | P1[key_description=contract] | anthropic:claude-haiku-5-5@high | 45 | 0.000 | 1.000 | 0.000 | 0.889 | 0.111 |
| timeout_after_execution | P1[key_description=contract] | together:glm-5.3-flash@high | 45 | 0.000 | 1.000 | 0.000 | 0.889 | 0.111 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^cross_provider_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) are counted by each provider's own tokenizer, so they are comparable within a provider but not across providers (anthropic, together here). Compare [model_calls](../../docs/DEFINITIONS.md#model_calls) or [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) across providers. ([about this note](../../docs/DEFINITIONS.md#note-cross_provider_tokens))
[^open_weights_hosting]: Open-weight models here are served by a hosted provider (together). Providers can quantize models or change revisions without notice; every response's served model ID is recorded in the transcripts, so check them before comparing runs made at different times. ([about this note](../../docs/DEFINITIONS.md#note-open_weights_hosting))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
