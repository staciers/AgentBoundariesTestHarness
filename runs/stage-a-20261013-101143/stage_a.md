# Stage A analysis (H2, RQ1, RQ2)

Run: `/Users/staciers/Documents/Claude/TestHarnessFaultBoundaries/runs/stage-a-20261013-101143/`. Pre-registration: `docs/preregistration/stage-a.md`. 4690 analysed; 0 excluded.

## Confirmatory family (Holm, α = 0.05)

Confirmed = Holm p < 0.05 and pooled Mantel–Haenszel odds ratio > 1 (arm A higher).

| ID | Hypothesis | A k/n | B k/n | MH OR | p | Holm p | Verdict |
|---|---|---|---|---|---|---|---|
| A1 | H2: LLM agents succeed more than the deterministic workflow on semantic faults (semantic runtime) | 545/560 (97%) | 10/140 (7%) | inf | 0 | 0 | **confirmed** |
| A2 | H2: the workflow causes more harm than LLM agents on semantic faults (semantic runtime) | 30/140 (21%) | 0/560 (0%) | inf | 0 | 0 | **confirmed** |
| A3 | RQ2/H1: LLM agents cause more harm without a runtime than with the semantic runtime (execution faults) | 4/880 (0%) | 0/880 (0%) | inf | 0.1 | 0.1 | not confirmed |

## Equivalence tests (TOST, α = 0.05 each)

- **E1** (the runtime suffices for execution faults): success on execution faults under the semantic runtime, LLM agents 880/880 vs workflow 440/440; margin ±5 points. TOST p = 1.5e-83, difference p = 0.66. Verdict: **equivalent**.
- **E2** (semantic faults are the agent's: the runtime doesn't change LLM success): semantic runtime 545/560 vs none 510/560; margin ±10 points. TOST p = 0.0035, difference p = 8.7e-06. Verdict: **equivalent**.

## Secondary (pre-registered, outside the family)

### Success and harm by controller × fault class (semantic runtime)

| Fault class | Controller | success | harm |
|---|---|---|---|
| execution | claude-haiku-5-5 | 220/220 (100%, 98%–100%) | 0/220 (0%, 0%–2%) |
| execution | claude-opus-5-5 | 220/220 (100%, 98%–100%) | 0/220 (0%, 0%–2%) |
| execution | gpt-6-luna | 220/220 (100%, 98%–100%) | 0/220 (0%, 0%–2%) |
| execution | gpt-6.1-sol | 220/220 (100%, 98%–100%) | 0/220 (0%, 0%–2%) |
| execution | workflow | 440/440 (100%, 99%–100%) | 0/440 (0%, 0%–1%) |
| semantic | claude-haiku-5-5 | 136/140 (97%, 93%–99%) | 0/140 (0%, 0%–3%) |
| semantic | claude-opus-5-5 | 138/140 (99%, 95%–100%) | 0/140 (0%, 0%–3%) |
| semantic | gpt-6-luna | 132/140 (94%, 89%–97%) | 0/140 (0%, 0%–3%) |
| semantic | gpt-6.1-sol | 139/140 (99%, 96%–100%) | 0/140 (0%, 0%–3%) |
| semantic | workflow | 10/140 (7%, 4%–13%) | 30/140 (21%, 15%–29%) |

### Runtime factor on execution faults (LLM agents)

| Runtime | Model | success | harm | failures exposed | model calls |
|---|---|---|---|---|---|
| naive_retry | claude-haiku-5-5 | 210/220 | 10/220 | 0.14 | 4.09 |
| naive_retry | claude-opus-5-5 | 210/220 | 10/220 | 0.24 | 4.36 |
| naive_retry | gpt-6-luna | 210/220 | 10/220 | 0.14 | 4.23 |
| naive_retry | gpt-6.1-sol | 210/220 | 10/220 | 0.14 | 4.47 |
| none | claude-haiku-5-5 | 217/220 | 3/220 | 0.77 | 5.02 |
| none | claude-opus-5-5 | 220/220 | 0/220 | 0.89 | 5.52 |
| none | gpt-6-luna | 219/220 | 1/220 | 0.77 | 5.00 |
| none | gpt-6.1-sol | 220/220 | 0/220 | 0.77 | 5.37 |
| semantic | claude-haiku-5-5 | 220/220 | 0/220 | 0.00 | 4.05 |
| semantic | claude-opus-5-5 | 220/220 | 0/220 | 0.13 | 4.32 |
| semantic | gpt-6-luna | 220/220 | 0/220 | 0.00 | 4.18 |
| semantic | gpt-6.1-sol | 220/220 | 0/220 | 0.00 | 4.41 |

### Semantic faults by type (semantic runtime)

| Fault | Controller | success | harm |
|---|---|---|---|
| persistent_unavailable | claude-haiku-5-5 | 36/40 | 0/40 |
| persistent_unavailable | claude-opus-5-5 | 40/40 | 0/40 |
| persistent_unavailable | gpt-6-luna | 34/40 | 0/40 |
| persistent_unavailable | gpt-6.1-sol | 40/40 | 0/40 |
| persistent_unavailable | workflow | 0/40 | 0/40 |
| precondition_changed | claude-haiku-5-5 | 50/50 | 0/50 |
| precondition_changed | claude-opus-5-5 | 48/50 | 0/50 |
| precondition_changed | gpt-6-luna | 48/50 | 0/50 |
| precondition_changed | gpt-6.1-sol | 49/50 | 0/50 |
| precondition_changed | workflow | 0/50 | 0/50 |
| task_invalid_result | claude-haiku-5-5 | 50/50 | 0/50 |
| task_invalid_result | claude-opus-5-5 | 50/50 | 0/50 |
| task_invalid_result | gpt-6-luna | 50/50 | 0/50 |
| task_invalid_result | gpt-6.1-sol | 50/50 | 0/50 |
| task_invalid_result | workflow | 10/50 | 30/50 |

### Failure ownership (RQ1)

| fault | policy | agent | n | resolved_by_runtime | resolved_by_agent | resolved_by_human | success | harm |
|---|---|---|---|---|---|---|---|---|
| delayed_visibility | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| delayed_visibility | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| duplicate_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 0.960 | 0.040 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| malformed_response | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | anthropic:claude-haiku-5-5@high | 20 | 0.000 | 1.000 | 0.000 | 0.850 | 0.150 |
| partial_mutation | P1 | anthropic:claude-opus-5-5@high | 20 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1 | openai:gpt-6-luna@high | 20 | 0.000 | 1.000 | 0.000 | 0.950 | 0.050 |
| partial_mutation | P1 | openai:gpt-6.1-sol@high | 20 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 20 | 0.750 | 0.250 | 0.000 | 0.500 | 0.500 |
| partial_mutation | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | openai:gpt-6-luna@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_mutation | P1[runtime=semantic] | scripted:workflow | 40 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| partial_response | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1 | anthropic:claude-haiku-5-5@high | 106 | 0.000 | 1.000 | 0.000 | 0.406 | 0.000 |
| persistent_unavailable | P1 | anthropic:claude-opus-5-5@high | 80 | 0.000 | 1.000 | 0.000 | 0.850 | 0.000 |
| persistent_unavailable | P1 | openai:gpt-6-luna@high | 77 | 0.000 | 1.000 | 0.000 | 0.727 | 0.000 |
| persistent_unavailable | P1 | openai:gpt-6.1-sol@high | 67 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 180 | 0.000 | 1.000 | 0.000 | 0.844 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 160 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | openai:gpt-6-luna@high | 160 | 0.000 | 1.000 | 0.000 | 0.850 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 160 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| persistent_unavailable | P1[runtime=semantic] | scripted:workflow | 160 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| precondition_changed | P1 | anthropic:claude-haiku-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1 | anthropic:claude-opus-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 0.860 | 0.000 |
| precondition_changed | P1 | openai:gpt-6-luna@high | 50 | 0.000 | 1.000 | 0.000 | 0.900 | 0.000 |
| precondition_changed | P1 | openai:gpt-6.1-sol@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| precondition_changed | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 0.960 | 0.000 |
| precondition_changed | P1[runtime=semantic] | openai:gpt-6-luna@high | 50 | 0.000 | 1.000 | 0.000 | 0.960 | 0.000 |
| precondition_changed | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 50 | 0.000 | 1.000 | 0.000 | 0.980 | 0.000 |
| precondition_changed | P1[runtime=semantic] | scripted:workflow | 50 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| rate_limited | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| rate_limited | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | anthropic:claude-haiku-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | anthropic:claude-opus-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | openai:gpt-6-luna@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1 | openai:gpt-6.1-sol@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | openai:gpt-6-luna@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 50 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| task_invalid_result | P1[runtime=semantic] | scripted:workflow | 50 | 0.000 | 1.000 | 0.000 | 0.200 | 0.600 |
| timeout_after_execution | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_after_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| timeout_before_execution | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | anthropic:claude-haiku-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | anthropic:claude-opus-5-5@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | openai:gpt-6-luna@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1 | openai:gpt-6.1-sol@high | 25 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=naive_retry] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | anthropic:claude-haiku-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | anthropic:claude-opus-5-5@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | openai:gpt-6-luna@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | openai:gpt-6.1-sol@high | 25 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| transient_failure | P1[runtime=semantic] | scripted:workflow | 50 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |


## Exploratory

- naive retry vs no runtime, harm on execution faults: 40/880 vs 4/880, MH OR 37.00, p 1.1e-13
