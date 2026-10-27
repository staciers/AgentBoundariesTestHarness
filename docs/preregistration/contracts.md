# Pre-registration: contract study (idempotency-key scope × key description)

**Status:** draft. It becomes registered when committed, **after the pilot and before the
main run**. Defects the pilot reveals may be fixed before then (record them under *Pilot
findings*). After the commit, change nothing listed here.

| | |
|---|---|
| Spec | [`experiments/contracts.json`](../../experiments/contracts.json): 4,480 episodes |
| Pilot spec | [`experiments/contracts_pilot.json`](../../experiments/contracts_pilot.json): 90 episodes, seeds 900–904, 2 models, the new arms only; not analysed |
| Analysis | [`analysis/contracts.py`](../../analysis/contracts.py), run unchanged |
| Contract module | [`abh/contract.py`](../../abh/contract.py) |
| Origin of hypotheses | the confirmation run (C3, C5), its open-weight replication (OC3, OC5), and a review asking that the keys finding be bounded |
| Paper role | Q4 in the [paper outline](../PAPER_OUTLINE.md#evaluation-7) |
| Definitions | [DEFINITIONS.md](../DEFINITIONS.md) |

## Question

The confirmation run found that offering idempotency keys **raised** harm under a hidden
partial commit (C3: 30% vs 1%), and that the "at most once" wording drove most of it (C5: 30%
vs 3%). In those services the key was recorded only when a request *completed*. A request that
committed partly, then failed behind a timeout, left no key record, so a retry with the same
key ran again.

That shows agents over-trusting a guarantee whose scope is narrower than its description
suggests. It does **not** show that correctly implemented end-to-end idempotency is unsafe.
This study separates the two, using execution contracts:

1. **Scope.** If the key is recorded *atomically with the committed part*, does the hazard
   disappear? With key scope `atomic`, a retry with the same key returns the original partial
   outcome and never re-executes.
2. **Interface.** If the key's description is generated from the contract, so it states exactly
   what the key covers, does harm fall without changing the service?

## Design

**Scenarios:** `travel/base`, `commerce/base`, `devops/base`, `scheduling/base`, as in the
confirmation run. The partial-mutation fault applies to the three with multi-part writes.

**Models:** the 8 of Stage D, all at effort `high`:
- closed: `claude-opus-5-5`, `claude-haiku-5-5`, `gpt-6.1-sol`, `gpt-6-luna`
- open (Together): `DeepSeek-V4-Pro-0813`, `DeepSeek-V4-Flash-0731`, `GLM-5.3`, `GLM-5.3-Flash`

**Seeds:** 200–229 (fresh), so 90 episodes per model per arm.

**Main block:** fault = *hidden partial commit* (`partial_mutation` + `timeout_after_execution`),
policy `P1` (no runtime), keys offered.

| Arm | Key scope (service) | Key description (interface) |
|---|---|---|
| A | `completed`, as in all earlier studies | "at most once" (the original wording) |
| B | `completed` | generated from the contract: states that a request failed partway is not recorded, and to check state before retrying |
| C | `atomic` | "at most once" (now true, partial case included) |
| D | `atomic` | generated from the contract: states that a retry returns the original outcome, including a partial failure |
| N | — | no keys offered (`expose_keys=false`) |

**Sanity block:** hidden write (`timeout_after_execution` + `delayed_visibility`), arms A and C
only, seeds 200–209.

**Reference block:** `P6` (threshold 0.7, semantic runtime) with key scope `atomic`, seeds
200–209. The runtime reads the contract and skips its pre-retry compensation, because the
service now replays the original outcome.

**Totals:** 4,480 episodes. Episodes, keys and outcomes for every earlier study are unchanged
by the contract layer:
- New contract fields enter the episode key only when set.
- Replaying all 2,680 confirmation-run episodes and all 9,583 replayable Stage D episodes gave
  identical outcomes.

**Execution:** per-provider worker pools (Anthropic 8, OpenAI 8, Together 12), a request
timeout of 180 s with one retry, and every API retry and timeout recorded per episode
(`api_retries`, `api_timeouts`). The run's `manifest.json` records the code commit and
whether the tree was clean.

**Fixed sample.** No interim looks at outcomes.

## Confirmatory hypotheses

Outcome: [harm](../DEFINITIONS.md#harm) (end-state or self-corrected), as in C3 and C5. These
are two-sided Mantel–Haenszel tests stratified by model × scenario, Holm-corrected across K1–K3
at α = 0.05. A hypothesis is confirmed only if its Holm p < 0.05 **and** the pooled odds ratio
is > 1 (arm A higher).

| ID | Claim | Arm A (predicted higher harm) | Arm B |
|---|---|---|---|
| K1 | **Scope:** an atomic key scope removes the hazard, even with "at most once" wording | A | C |
| K2 | **Interface:** contract-generated descriptions reduce harm, with the service unchanged | A | B |
| K3 | **Replication:** the keys hazard (C3) on fresh seeds, across all 8 models | A | N |

**Separate tests, each at α = 0.05:**
- **N1 (non-inferiority):** harm, C vs N. A keyed retry under an atomic scope is no worse than
  having no keys. Margin +3 points.
- **N2 (non-inferiority):** harm, D vs N. Margin +3 points.
- **E1 (equivalence, TOST, sanity):** harm under a hidden write, A vs C. Scope shouldn't matter
  when the commit is complete. Margin ±3 points.

**Pre-registered reading:**
- **Scope claim** (K1 confirmed **and** N1 non-inferior): correctly scoped end-to-end idempotency
  is safe for agents, and the original hazard is a scope mismatch. If K1 holds but N1 fails,
  atomic keys help but don't fully remove the hazard. The likeliest route is an agent answering
  a replayed partial failure with a *new* key, which repeats the committed part; that would be
  reported as such.
- **Interface claim** (K2 confirmed): describing the key from its contract reduces harm without
  changing the service. This would generalize C5's hand-written caveat into a mechanism.

**Expectations, stated so they aren't mistaken for findings:**
- Open models rarely attach a key to the first write (open-confirm, exploratory), so scope
  should help them less.
- K3 may fail to replicate for open models, as OC3 did. K3 is pooled across all 8 models.

## Secondary (pre-registered)

- Harm per arm and model, with Wilson intervals; end-state vs self-corrected.
- Harm per arm by family (closed / open).
- Mechanism M1, as defined in the confirmation run: whether the agent checked state before
  retrying, per arm.
- The reference block: P6 harm under an atomic scope.

## Exploratory (to be labelled as such)

- Key discipline (first write keyed) by arm.
- Per-scenario effects.
- Wording effects under the atomic scope (C vs D).
- Comparisons with the confirmation run.
- Anything not listed above.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations):
- Episodes ending in a harness error, or in an agent error other than a refusal (now including
  `timeout`), are re-run from the registered commit with `abh run --resume <dir> --rerun-errors`.
  The originals and their traces are kept.
- If any still fail, they are excluded and counted, and the sensitivity analysis registered in
  `52148b2` applies.
- Every response's served model ID is checked; a mismatch is a deviation.
- The run uses `caffeinate -i -s` from the start.

## Cost

From the confirmation and open-confirm runs, which used the same scenarios and faults:
- closed models: about $0.0118 per episode × 2,240 ≈ $26
- open models: about $0.0044 per episode × 2,240 ≈ $10
- **total ≈ $36**

The pilot (90 episodes on the two cheapest models) should cost under $0.25. Its measured cost
replaces this estimate before registration.

## Pilot findings

The pilot (`runs/contracts-pilot-20261026-131823`, code `d09d7c3`, clean tree) ran 90 episodes
on Haiku and GLM-5.3-Flash, seeds 900–904, for **$0.13** ($0.06 Anthropic, $0.07 Together).
- **Execution:** no harness or agent errors, and no API retries or timeouts. Every GLM response
  came from `zai-org/GLM-5.3-Flash`.
- **Coverage:** the partial-commit fault reached travel, commerce and devops, as designed.
  Scheduling has no multi-part write, so it contributes only to the sanity block.
- **The new mechanics fire as designed.** Outcomes were inspected only for this:
  - Under the atomic scope, the service replayed the original partial failure in 20 of 60
    episodes. The agent saw it as `PARTIALLY_EXECUTED`: "A request with this idempotency key
    already failed partway and was not executed again…".
  - Under contract wording, the agents read the generated text. GLM's reasoning quotes it ("a
    request that failed partway is not recorded…").

**One defect found and fixed before registration (logging only).** Traces did not record the
tool schemas the agent was shown, so the description manipulation couldn't be audited from the
traces. The `episode_start` trace event now records `tool_schemas` and the contract label
(test: `test_trace_records_tool_schemas_as_shown`). Behaviour, outcomes and episode keys are
unchanged, so the pilot was not re-run.

**Cost:** the estimate stays at **≈ $36**. The pilot's two models are the cheapest, so its cost
per episode isn't representative of the full model set.

No change to the design, hypotheses or tests.

### Deviations

**2026-10-26: one model withdrawn by the provider (recorded before any outcome was seen).**
- **What happened:** all 560 `DeepSeek-V4-Flash-0731` episodes failed before their first model
  call. Together returned HTTP 400 `endpoint_not_configured` ("Endpoint has no deployments
  configured for routing"). The model no longer appears in Together's model list;
  `DeepSeek-V4.1-Flash` and `DeepSeek-V4.1-Flash-1017` now appear instead. It was last served in
  Stage D (2026-10-18).
- **Per the exclusion rule:** all 560 were re-run from `45b0e78` (`--rerun-errors`), and all
  failed the same way. They are **excluded and counted**. The registered analysis therefore runs
  on 7 of the 8 models (3,920 analysed episodes). The originals are in
  `episodes_rerun_originals.jsonl`.
- **No cost:** no model call was made.
- **Nothing else changed:** all other episodes completed with no errors, 2 API retries and no
  timeouts. Every other Together response came from its requested model.
- **The registered sensitivity analysis (`52148b2`) can't apply,** because there is no fix to
  re-run with: the model itself is unavailable.

**Decision (2026-10-27, before the analysis was run and before any outcome was seen):** add
`deepseek-ai/DeepSeek-V4.1-Flash-1017` (Together; dated snapshot; $0.30 / $1.20 per million
input / output tokens) as an **exploratory supplement**.
- **Design:** exactly the main design (all blocks, seeds, arms and settings), with only this
  model ([`experiments/contracts_supplement.json`](../../experiments/contracts_supplement.json)),
  run into its own folder.
- **Primary analysis unchanged:** 7 models, as registered.
- **The supplement is reported separately** and labelled exploratory. It is never pooled into
  K1–K3, N1–N2 or E1, because it is a different model.

### Outcome (recorded after analysis, 2026-10-27)

Run `runs/contracts-20261026-140610`: 4,480 episodes, $37.40. 560 were excluded (the withdrawn
model, above), leaving 3,920 analysed on 7 models.

- **K1 confirmed:** an atomic key scope reduces harm (18% → 7%).
- **K2 confirmed:** contract-generated descriptions reduce harm with the service unchanged
  (18% → 5%; closed models 26% → 1%).
- **K3 confirmed:** the keys hazard replicates on fresh seeds (18% vs 4% without keys).
- **N1 and N2 not shown:**
  - Under an atomic scope, harm stays above the no-keys level (7%, and 19% with contract
    wording).
- **E1 inconclusive.**
- **Scope claim:** not established as registered. **Interface claim:** yes.

**Exploratory findings** (details in the run's `NOTES.md`):
- For closed models, both fixes remove duplicates entirely (91 → 0 episodes). The remaining
  harm under an atomic scope is partial work left in place.
- The generated atomic-scope description lowered checking before retrying (52%). Many agents,
  mostly open models, then re-sent the whole request with a new key after the replayed partial
  failure, the route anticipated above.
- Open models are dominated by poor key discipline.
- The P6 runtime had 0/210 harm.
- The supplement model (V4.1 Flash) barely showed the hazard.
