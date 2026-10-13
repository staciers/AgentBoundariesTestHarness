# Pre-registration: Stage A (H2, RQ1, RQ2)

**Status:** draft. It becomes registered when committed, **after the pilot and before the
main run**. Between the pilot and that commit, scenario bugs the pilot reveals may be fixed
(record them under *Pilot findings*). After the commit, change nothing listed here; record
deviations at the end instead.

| | |
|---|---|
| Spec | [`experiments/stage_a.json`](../../experiments/stage_a.json) |
| Pilot spec | [`experiments/stage_a_pilot.json`](../../experiments/stage_a_pilot.json): seed 900, main arm only, not analysed |
| Analysis | [`analysis/stage_a.py`](../../analysis/stage_a.py), run unchanged on the finished run |
| Origin of hypotheses | the research prospectus (H2, RQ1, RQ2), stated before any data |
| Definitions | [DEFINITIONS.md](../DEFINITIONS.md) |

## Question

The confirmation run showed the *runtime's* share of the three-way split. Stage A tests the
*agent's* share:

- **H2:** agent reasoning beats deterministic recovery when success needs replanning, choosing
  another tool, or interpreting changed circumstances.
- **The crossover:** that advantage should disappear on execution faults, which the runtime
  handles for any controller.

## Design

- **Scenarios:** `travel/base`, `commerce/base`, `devops/base`, `scheduling/base`,
  `platform/base`. Scheduling lacks `persistent_unavailable` and `partial_mutation`.
- **Faults**, one per episode:
  - semantic: `precondition_changed`, `task_invalid_result`, `persistent_unavailable`
  - execution: the nine execution faults
  - plus no fault
- **Controllers:**
  - **LLM agents:** `claude-opus-5-5`, `claude-haiku-5-5`, `gpt-6.1-sol`, `gpt-6-luna`, all
    at effort `high`.
  - **Deterministic workflow:** `scripted:workflow`. It follows the reference plan exactly,
    retries transient errors, and never verifies, replans, switches tools, notices bad
    results, asks, or attaches keys.
- **Runtime:** `P1[runtime=semantic]` (the semantic runtime with no human gate), `P1` (no
  runtime), `P1[runtime=naive_retry]`.

| Block | Controllers | Faults | Policies | Seeds |
|---|---|---|---|---|
| H2 semantic faults | LLM ×4 | semantic | `P1[runtime=semantic]`, `P1` | 100–109 |
| execution × runtime | LLM ×4 | execution | `P1[runtime=semantic]`, `P1`, `P1[runtime=naive_retry]` | 100–104 |
| no-fault baseline | LLM ×4 | none | same three | 100–104 |
| workflow baseline | workflow | none, semantic, execution | `P1[runtime=semantic]` | 100–109 |

- **Size:** 4,060 LLM episodes plus 630 workflow episodes.
- **Cost:** the estimate will be re-made from the pilot's measured per-cell costs.
- **Fixed sample.** No interim looks at outcomes.

## Confirmatory hypotheses

These are two-sided Mantel–Haenszel tests with Holm correction across A1–A3 at α = 0.05. A
hypothesis is **confirmed** only if its Holm-adjusted p < 0.05 **and** the pooled odds ratio
is > 1 (arm A higher, as predicted). The outcomes are [success](../DEFINITIONS.md#success)
(strict) and [harm](../DEFINITIONS.md#harm).

| ID | Claim | Arm A (predicted higher) | Arm B | Outcome | Strata |
|---|---|---|---|---|---|
| A1 | H2: agents recover from semantic faults; a workflow can't | LLM, semantic faults, `P1[runtime=semantic]` | workflow, semantic faults | success | scenario × fault |
| A2 | H2: without reasoning, semantic faults cause harm (e.g. acting on an invalid result) | workflow, semantic faults | LLM, semantic faults, `P1[runtime=semantic]` | harm | scenario × fault |
| A3 | RQ2/H1 at the single-fault level: no runtime causes more harm than the semantic runtime | LLM, execution faults, `P1` | LLM, execution faults, `P1[runtime=semantic]` | harm | model × scenario × fault |

The equivalence tests are TOST, each at α = 0.05 and outside the Holm family. Each verdict is
**equivalent** (TOST p < 0.05), **different** (difference test p < 0.05), or
**inconclusive**.

- **E1, the runtime suffices for execution faults.** Under `P1[runtime=semantic]`, compare
  success of LLM agents vs the workflow on execution faults. Margin: ±5 points.
- **E2, semantic faults belong to the agent.** Compare LLM success on semantic faults under
  `P1[runtime=semantic]` vs `P1`. Margin: ±10 points.

A1 + A2 + E1 together are the crossover. If all three hold, *where* recovery should live
depends on the fault class, which is the paper's thesis.

## Secondary (pre-registered, outside the family)

- Success and harm by controller × fault class, with Wilson intervals.
- **Runtime factor on execution faults, per model:** success, harm, failures exposed to the
  agent, and model calls (RQ2, H6).
- Semantic faults by type and controller.
- [Failure ownership](../DEFINITIONS.md#resolved_by_runtime) (RQ1).

## Exploratory (to be labelled as such)

- Naive retry vs no runtime on execution faults. The scripted runs suggest naive retry can be
  *worse* than no runtime, but that is by construction, so it isn't a pre-registered
  hypothesis.
- Anything not listed above.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations):

- Episodes ending in a harness error, or in an agent error other than a refusal, are re-run
  from the registered commit before analysis.
- Any that still fail are excluded and counted.
- Refusals stay in the data as recorded outcomes.

## Pilot findings

The pilot (`runs/stage-a-pilot-20261013-093242`) ran 252 episodes: seed 900, main arm, $2.22,
no errors. Outcomes were inspected only to find scenario defects. One was found and fixed
before registration:

- **`devops/base` + `task_invalid_result` harmed all four models**, for the same reason in
  each case. The corrupted release list marked `v2.3.1-rc` healthy, and the prompt asked for
  "the most recent healthy release". An RC is a release, so nothing in the data or the
  instruction contradicted the corruption, which violates the rule that task-invalid results
  must be detectable by careful reading.
  - **Fix:** listings now show each release's `environment` (the RC ran only in staging), and
    the prompt asks for "the most recent release that was healthy in production".
  - **Effect on the baselines:** the deterministic workflow is still fooled, while careful
    agents can now catch it.
  - **Re-check:** 8 episodes at seeds 900–901 (4 models × 2); all 8 rolled back correctly.
  - **Regression test:** `TestPilotFixes`.
  - The prompt change also applies to `devops/ambiguous`, for consistency.

Measured pilot costs put the full run at about $40–43.

No change to hypotheses, tests or design.

### Deviations

**2026-10-13 — harness defect found during the run (recorded before any affected outcome was seen).**
Malformed tool arguments crashed the harness instead of returning an error to the model. In
the `platform` domain, a `files` argument sent as a JSON string or a list of strings crashed
the approver check. Stage A had one such episode (`9e3cedef96cf4c9c`) after about 1,100
episodes.

- **Primary analysis:** unchanged, per the exclusion rule. Crashed episodes are re-run from
  the registered commit, and any that crash again are excluded and counted.
- **Added sensitivity analysis** (decided before seeing the affected outcomes): excluded
  episodes are re-run with the fix, commit to be recorded here. Results are reported with
  and without them.
- **The fix** turns would-be crashes into "invalid arguments" errors, the way a real API
  returns a 400. It leaves every other episode unchanged: re-scoring all 2,680
  confirmation-run episodes with the fix reproduced every one exactly.

### Outcome (recorded after analysis, 2026-10-13)

The run completed with 4,690 valid episodes. The one crashed episode was re-run from
`eda3331` and succeeded, so nothing was excluded.

- **A1 confirmed:** LLM agents 97% vs workflow 7% success on semantic faults.
- **A2 confirmed:** the workflow caused harm in 21% of semantic-fault episodes; the LLM agents
  in 0%.
- **A3 not confirmed:** on *single* execution faults, LLM agents without a runtime caused
  harm in only 4/880 episodes, vs 0/880 with the semantic runtime (p = 0.10). With a single,
  observable execution fault, current models check state and recover on their own.
- **E1 equivalent:** with the semantic runtime, the LLMs and the workflow both succeeded on
  every execution-fault episode (880/880 and 440/440).
- **E2 equivalent within ±10 points,** but also significantly different (97% vs 91%). The
  runtime adds a few points on semantic faults.

**Reading the results together:** the runtime is *necessary* when the outcome of a failure
can't be observed (the hidden write and hidden partial commit in the confirmation run and
Stage C). It is *helpful but not necessary* for single, observable faults: no harm, about 20%
fewer model calls, and failures no longer reach the agent. The agent is necessary for
semantic faults.
