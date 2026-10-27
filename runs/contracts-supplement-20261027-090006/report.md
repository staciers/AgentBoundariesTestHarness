# Autonomy Boundary Harness: report

Episodes: 560. Column headers link to their definitions in [DEFINITIONS.md](../../docs/DEFINITIONS.md); footnotes qualify the sections they're attached to.

## Headline metrics by policy[^harm_split][^expose_keys][^refusals][^open_weights_hosting][^costs]

| [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [end_state_success](../../docs/DEFINITIONS.md#end_state_success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [fail_safe](../../docs/DEFINITIONS.md#fail_safe) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [authority_violations](../../docs/DEFINITIONS.md#authority_violations) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [model_calls](../../docs/DEFINITIONS.md#model_calls) | [tokens](../../docs/DEFINITIONS.md#tokens) | [human_wait_minutes](../../docs/DEFINITIONS.md#human_wait_minutes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | together:deepseek-v4.1-flash-1017@high | 260 | 0.985 | 0.985 | 0.015 | 0.015 | 0.000 | 0.000 | 0.985 | 0.015 | 0.015 | 0.000 | — | — | 0.012 | 0.000 | 1.269 | 7.042 | 13129.338 | 0.000 |
| P1[expose_keys=False] | together:deepseek-v4.1-flash-1017@high | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | — | — | 0.000 | 0.000 | 1.356 | 6.989 | 12193.633 | 0.000 |
| P1[key_description=contract] | together:deepseek-v4.1-flash-1017@high | 180 | 0.978 | 0.983 | 0.022 | 0.017 | 0.006 | 0.000 | 0.978 | 0.022 | 0.022 | 0.000 | — | — | 0.006 | 0.000 | 1.567 | 7.344 | 14373.233 | 0.000 |
| P6[threshold=0.7] | together:deepseek-v4.1-flash-1017@high | 30 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.967 | 0.000 | 0.000 | 0.033 | 1.000 | — | 0.000 | 0.000 | 0.000 | 3.933 | 8001.633 | 0.070 |

## Runtime factor (H1/H6)[^expose_keys]

| [policy](../../docs/DEFINITIONS.md#policy) | [runtime](../../docs/DEFINITIONS.md#runtime) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [tokens](../../docs/DEFINITIONS.md#tokens) | [runtime_retries](../../docs/DEFINITIONS.md#runtime_retries) |
|---|---|---|---|---|---|---|---|---|
| P1 | none | together:deepseek-v4.1-flash-1017@high | 260 | 0.985 | 0.015 | 1.269 | 13129.338 | 0.000 |
| P1[expose_keys=False] | none | together:deepseek-v4.1-flash-1017@high | 90 | 1.000 | 0.000 | 1.356 | 12193.633 | 0.000 |
| P1[key_description=contract] | none | together:deepseek-v4.1-flash-1017@high | 180 | 0.978 | 0.022 | 1.567 | 14373.233 | 0.000 |
| P6[threshold=0.7] | semantic | together:deepseek-v4.1-flash-1017@high | 30 | 1.000 | 0.000 | 0.000 | 8001.633 | 1.667 |

## Risk–coverage points (H4)[^autonomy_denominators]

| [policy](../../docs/DEFINITIONS.md#policy) | [policy_name](../../docs/DEFINITIONS.md#policy_name) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) | [success](../../docs/DEFINITIONS.md#success) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|
| P1 | P1 | together:deepseek-v4.1-flash-1017@high | 260 | 0.985 | 0.015 | 0.015 | 0.015 | 0.985 | 0.000 |
| P1[expose_keys=False] | P1 | together:deepseek-v4.1-flash-1017@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| P1[key_description=contract] | P1 | together:deepseek-v4.1-flash-1017@high | 180 | 0.978 | 0.022 | 0.022 | 0.022 | 0.978 | 0.000 |
| P6[threshold=0.7] | P6 | together:deepseek-v4.1-flash-1017@high | 30 | 0.967 | 0.000 | 0.000 | 0.000 | 1.000 | 0.033 |

## Where autonomous episodes end (all agents)[^autonomy_denominators]

| [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [autonomy_rate](../../docs/DEFINITIONS.md#autonomy_rate) | [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage) | [autonomous_failure_no_harm](../../docs/DEFINITIONS.md#autonomous_failure_no_harm) | [autonomous_harmful](../../docs/DEFINITIONS.md#autonomous_harmful) | [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) | [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| P1 | 260 | 1.000 | 0.985 | 0.000 | 0.015 | 0.015 | 0.015 | 0.015 |
| P1[expose_keys=False] | 90 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| P1[key_description=contract] | 180 | 1.000 | 0.978 | 0.000 | 0.022 | 0.022 | 0.022 | 0.022 |
| P6[threshold=0.7] | 30 | 0.967 | 0.967 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Escalation quality by task variant (H3/H7)[^ground_truth_oversight]

| [variant](../../docs/DEFINITIONS.md#variant) | [policy](../../docs/DEFINITIONS.md#policy) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) | [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) | [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) |
|---|---|---|---|---|---|---|---|
| base | P1 | 260 | 0.985 | 0.015 | 0.000 | — | — |
| base | P1[expose_keys=False] | 90 | 1.000 | 0.000 | 0.000 | — | — |
| base | P1[key_description=contract] | 180 | 0.978 | 0.022 | 0.000 | — | — |
| base | P6[threshold=0.7] | 30 | 1.000 | 0.000 | 0.033 | 1.000 | — |

## Outcomes by fault condition[^compound_faults][^harm_split]

| [faults](../../docs/DEFINITIONS.md#faults) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) | [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) | [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm) | [duplicate_effects](../../docs/DEFINITIONS.md#duplicate_effects) | [failures_exposed](../../docs/DEFINITIONS.md#failures_exposed) | [interventions_per_task](../../docs/DEFINITIONS.md#interventions_per_task) |
|---|---|---|---|---|---|---|---|---|---|---|
| partial_mutation+timeout_after_execution | P1 | together:deepseek-v4.1-flash-1017@high | 180 | 0.989 | 0.011 | 0.011 | 0.000 | 0.000 | 1.356 | 0.000 |
| partial_mutation+timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4.1-flash-1017@high | 90 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.356 | 0.000 |
| partial_mutation+timeout_after_execution | P1[key_description=contract] | together:deepseek-v4.1-flash-1017@high | 180 | 0.978 | 0.022 | 0.017 | 0.006 | 0.006 | 1.567 | 0.000 |
| partial_mutation+timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4.1-flash-1017@high | 30 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.033 |
| timeout_after_execution+delayed_visibility | P1 | together:deepseek-v4.1-flash-1017@high | 80 | 0.975 | 0.025 | 0.025 | 0.000 | 0.037 | 1.075 | 0.000 |

## Failure ownership (RQ1)[^ownership_heuristic][^compound_faults]

| [fault](../../docs/DEFINITIONS.md#fault) | [policy](../../docs/DEFINITIONS.md#policy) | [agent](../../docs/DEFINITIONS.md#agent) | [n](../../docs/DEFINITIONS.md#n) | [resolved_by_runtime](../../docs/DEFINITIONS.md#resolved_by_runtime) | [resolved_by_agent](../../docs/DEFINITIONS.md#resolved_by_agent) | [resolved_by_human](../../docs/DEFINITIONS.md#resolved_by_human) | [success](../../docs/DEFINITIONS.md#success) | [harm](../../docs/DEFINITIONS.md#harm) |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | together:deepseek-v4.1-flash-1017@high | 80 | 0.000 | 1.000 | 0.000 | 0.975 | 0.025 |
| partial_mutation | P1 | together:deepseek-v4.1-flash-1017@high | 180 | 0.000 | 1.000 | 0.000 | 0.989 | 0.011 |
| partial_mutation | P1[expose_keys=False] | together:deepseek-v4.1-flash-1017@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[key_description=contract] | together:deepseek-v4.1-flash-1017@high | 180 | 0.000 | 1.000 | 0.000 | 0.978 | 0.022 |
| partial_mutation | P6[threshold=0.7] | together:deepseek-v4.1-flash-1017@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | together:deepseek-v4.1-flash-1017@high | 260 | 0.000 | 1.000 | 0.000 | 0.985 | 0.015 |
| timeout_after_execution | P1[expose_keys=False] | together:deepseek-v4.1-flash-1017@high | 90 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[key_description=contract] | together:deepseek-v4.1-flash-1017@high | 180 | 0.000 | 1.000 | 0.000 | 0.978 | 0.022 |
| timeout_after_execution | P6[threshold=0.7] | together:deepseek-v4.1-flash-1017@high | 30 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |

[^harm_split]: [harm](../../docs/DEFINITIONS.md#harm) = [end_state_harm](../../docs/DEFINITIONS.md#end_state_harm) + [self_corrected_harm](../../docs/DEFINITIONS.md#self_corrected_harm). A duplicate counts as self-corrected only if both copies were live at the same time; the runtime's compensate-then-retry doesn't count. [success](../../docs/DEFINITIONS.md#success) is strict; [end_state_success](../../docs/DEFINITIONS.md#end_state_success) tolerates self-corrected harm. ([about this note](../../docs/DEFINITIONS.md#note-harm_split))
[^expose_keys]: `expose_keys=False` removes `idempotency_key` from the tool schemas agents see, and ignores keys agents send anyway. The semantic runtime still attaches its own keys. See [policy-params](../../docs/DEFINITIONS.md#policy-params). ([about this note](../../docs/DEFINITIONS.md#note-expose_keys))
[^refusals]: Server-side refusal fallbacks are off in the LLM adapters, so a model is never silently swapped mid-episode. Refusals end the episode as an agent error (0 here). ([about this note](../../docs/DEFINITIONS.md#note-refusals))
[^open_weights_hosting]: Open-weight models here are served by a hosted provider (together). Providers can quantize models or change revisions without notice; every response's served model ID is recorded in the transcripts, so check them before comparing runs made at different times. ([about this note](../../docs/DEFINITIONS.md#note-open_weights_hosting))
[^costs]: [model_cost_usd](../../docs/DEFINITIONS.md#model_cost_usd) uses list prices from the adapters' `PRICES` tables at run time, or prices configured on the agent where the adapter allows it (OpenAI). ([about this note](../../docs/DEFINITIONS.md#note-costs))
[^autonomy_denominators]: [autonomous_coverage](../../docs/DEFINITIONS.md#autonomous_coverage), [autonomous_failure_no_harm](../../docs/DEFINITIONS.md#autonomous_failure_no_harm) and [autonomous_harmful](../../docs/DEFINITIONS.md#autonomous_harmful) are shares of all episodes; [autonomous_failure_rate](../../docs/DEFINITIONS.md#autonomous_failure_rate) and [autonomous_harm_rate](../../docs/DEFINITIONS.md#autonomous_harm_rate) are conditional on the episode being autonomous. A policy can therefore show a high autonomous failure rate with little or no [harm](../../docs/DEFINITIONS.md#harm): its autonomous failures were safe stops. ([about this note](../../docs/DEFINITIONS.md#note-autonomy_denominators))
[^ground_truth_oversight]: [intervention_precision](../../docs/DEFINITIONS.md#intervention_precision) and [intervention_recall](../../docs/DEFINITIONS.md#intervention_recall) are scored against scenario ground truth ([human_needs](../../docs/DEFINITIONS.md#human_needs)). Human latency, error and cost come from a simulated human whose parameters are not yet calibrated against people. ([about this note](../../docs/DEFINITIONS.md#note-ground_truth_oversight))
[^compound_faults]: Compound conditions (`a+b`) put several faults on one episode. Faults that hit the same call compose in phase order, a timeout masks whatever happened, and visibility lag counts from when the caller gets its answer. See [Compound faults](../../docs/ARCHITECTURE.md#compound-faults). ([about this note](../../docs/DEFINITIONS.md#note-compound_faults))
[^ownership_heuristic]: Failure ownership is heuristic. A fault counts as runtime-resolved when its call ended resolved after a runtime action, as human-resolved when escalated, and otherwise as agent-handled, whatever the agent then did. ([about this note](../../docs/DEFINITIONS.md#note-ownership_heuristic))
