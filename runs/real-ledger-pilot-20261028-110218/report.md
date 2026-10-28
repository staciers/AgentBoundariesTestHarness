# Autonomy Boundary Harness: report

Episodes: 36. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^small_samples][^expose_keys][^refusals][^cross_provider_tokens][^open_weights_hosting][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | anthropic:claude-haiku-5-5@high | 6 | 0.500 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 0.000 | — | — | 0.500 | 0.000 | 0.500 | 5.500 | 11876.167 | 0.000 |
| P1 | together:glm-5.3-flash@high | 6 | 0.500 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 | 0.500 | 0.500 | 0.500 | 0.000 | — | — | 0.500 | 0.000 | 0.500 | 4.833 | 5678.833 | 0.000 |
| P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 6 | 0.000 | 0.167 | 1.000 | 0.833 | 0.167 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | — | — | 0.833 | 0.000 | 1.000 | 8.667 | 20480.833 | 0.000 |
| P1[expose_keys=False] | together:glm-5.3-flash@high | 6 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | — | — | 1.000 | 0.000 | 1.000 | 5.167 | 5410.000 | 0.000 |
| P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 6 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.000 | 7182.833 | 0.000 |
| P6[threshold=0.7] | together:glm-5.3-flash@high | 6 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 0.000 | 3.333 | 5030.333 | 0.000 |

## Runtime factor (H1/H6)[^cross_provider_tokens][^expose_keys]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | none | anthropic:claude-haiku-5-5@high | 6 | 0.500 | 0.500 | 0.500 | 11876.167 | 0.000 |
| P1 | none | together:glm-5.3-flash@high | 6 | 0.500 | 0.500 | 0.500 | 5678.833 | 0.000 |
| P1[expose_keys=False] | none | anthropic:claude-haiku-5-5@high | 6 | 0.000 | 1.000 | 1.000 | 20480.833 | 0.000 |
| P1[expose_keys=False] | none | together:glm-5.3-flash@high | 6 | 0.000 | 1.000 | 1.000 | 5410.000 | 0.000 |
| P6[threshold=0.7] | semantic | anthropic:claude-haiku-5-5@high | 6 | 1.000 | 0.000 | 0.000 | 7182.833 | 0.500 |
| P6[threshold=0.7] | semantic | together:glm-5.3-flash@high | 6 | 1.000 | 0.000 | 0.000 | 5030.333 | 0.500 |

## Risk–coverage points (H4)[^small_samples]

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|
| P1 | P1 | anthropic:claude-haiku-5-5@high | 6 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.000 |
| P1 | P1 | together:glm-5.3-flash@high | 6 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 0.000 |
| P1[expose_keys=False] | P1 | anthropic:claude-haiku-5-5@high | 6 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| P1[expose_keys=False] | P1 | together:glm-5.3-flash@high | 6 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| P6[threshold=0.7] | P6 | anthropic:claude-haiku-5-5@high | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P6[threshold=0.7] | P6 | together:glm-5.3-flash@high | 6 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |

## Where autonomous episodes end (all agents)

| [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [autonomy_rate](../../docs/DEFINITIONS.md#autonomy_rate) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_no_harm](../../docs/DEFINITIONS.md#autonomous_failure_no_harm) | [autonomous_harmful](../../docs/DEFINITIONS.md#autonomous_harmful) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| P1 | 12 | 1.000 | 0.500 | 0.000 | 0.500 | 0.500 | 0.500 | 0.500 |
| P1[expose_keys=False] | 12 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| P6[threshold=0.7] | 12 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Escalation quality by task variant (H3/H7)

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 12 | 0.500 | 0.500 | 0.000 | — | — |
| base | P1[expose_keys=False] | 12 | 0.000 | 1.000 | 0.000 | — | — |
| base | P6[threshold=0.7] | 12 | 1.000 | 0.000 | 0.000 | — | — |

## Outcomes by fault condition[^compound_faults][^harm_split][^small_samples]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| none | P1 | anthropic:claude-haiku-5-5@high | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| none | P1 | together:glm-5.3-flash@high | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1 | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 0.667 | 0.333 | 0.667 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:glm-5.3-flash@high | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P1[expose_keys=False] | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| timeout_after_execution+delayed_visibility | P6[threshold=0.7] | together:glm-5.3-flash@high | 3 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| delayed_visibility | P1[expose_keys=False] | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| delayed_visibility | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 3 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P6[threshold=0.7] | together:glm-5.3-flash@high | 3 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| partial_mutation | P1 | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| partial_mutation | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| partial_mutation | P1[expose_keys=False] | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| partial_mutation | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 3 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P6[threshold=0.7] | together:glm-5.3-flash@high | 3 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | anthropic:claude-haiku-5-5@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| timeout_after_execution | P1 | together:glm-5.3-flash@high | 3 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| timeout_after_execution | P1[expose_keys=False] | anthropic:claude-haiku-5-5@high | 6 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| timeout_after_execution | P1[expose_keys=False] | together:glm-5.3-flash@high | 6 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| timeout_after_execution | P6[threshold=0.7] | anthropic:claude-haiku-5-5@high | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P6[threshold=0.7] | together:glm-5.3-flash@high | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^small_samples]: Small groups: the smallest group in these tables has n=3. At that size a 95% interval for a rate near 50% is about ±57%. Wilson intervals for [success](../../docs/DEFINITIONS.md#success) are in the CSVs ([success_ci](../../docs/DEFINITIONS.md#success_ci)). ([about this note](../../docs/DEFINITIONS.md#note-small_samples))
[^expose_keys]: `expose_keys=False` removes `idempotency_key` from the tool schemas agents see, and ignores keys agents send anyway. The semantic runtime still attaches its own keys. See [policy-params](../../docs/DEFINITIONS.md#policy-params). ([about this note](../../docs/DEFINITIONS.md#note-expose_keys))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^cross_provider_tokens]: [tokens](../../docs/DEFINITIONS.md#tokens) are counted by each provider's own tokenizer, so they are comparable within a provider but not across providers (anthropic, together here). Compare [model_calls](../../docs/DEFINITIONS.md#model_calls) or [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) across providers. ([about this note](../../docs/DEFINITIONS.md#note-cross_provider_tokens))
[^open_weights_hosting]: Open-weight models here are served by a hosted provider (together). Providers can quantize models or change revisions without notice; every response's served model ID is recorded in the transcripts, so check them before comparing runs made at different times. ([about this note](../../docs/DEFINITIONS.md#note-open_weights_hosting))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
