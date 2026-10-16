# Pre-registration: Stage B (human escalation: H3, H4, H7, RQ3–RQ5)

**Status:** draft. It becomes registered when committed, **after the pilot and before the
main run**. Scenario defects the pilot reveals may be fixed before then (record them under
*Pilot findings*). After the commit, change nothing listed here.

| | |
|---|---|
| Spec | [`experiments/stage_b.json`](../../experiments/stage_b.json): 7,920 episodes |
| Pilot spec | [`experiments/stage_b_pilot.json`](../../experiments/stage_b_pilot.json): seed 900, P2/P5/P6/ORACLE, no fault; not analysed |
| Analysis | [`analysis/stage_b.py`](../../analysis/stage_b.py) and `python -m abh human-cost` (secondary), run unchanged |
| Human time and cost model | [`docs/HUMAN_MODEL.md`](../HUMAN_MODEL.md) (`abh/human_model.py`), frozen with this commit |
| Origin of hypotheses | the research prospectus (H3, H4, H7, RQ3–RQ5), stated before any data |
| Definitions | [DEFINITIONS.md](../DEFINITIONS.md) |

## Question

Earlier studies tested the runtime's and the agent's shares of the three-way split. Stage B
tests the **human's** share:

- Does escalation add value exactly where judgment or authority is needed (H3)?
- Does the semantic/runtime-aware policy reach more autonomy at no more risk (H4)?
- Does it save human attention without missing what humans are needed for (H7)?

## Design

- **Scenarios:** all 15, i.e. `travel`, `commerce`, `devops`, `scheduling`, `platform` × `base`,
  `ambiguous`, `authority`.
- **Fault conditions:** no fault; *hidden write* (`timeout_after_execution` +
  `delayed_visibility`).
- **Policies:** `P1`, `P2`, `P3` at thresholds 0.5/0.7/0.9, `P4`, `P5`, `P6` at thresholds
  0.5/0.7/0.9, and `ORACLE`.
- **Models:**
  - closed: `claude-opus-5-5`, `claude-haiku-5-5`, `gpt-6.1-sol`, `gpt-6-luna`
  - open, on Together: `DeepSeek-V4-Pro-0813`, `DeepSeek-V4-Flash-0731`, `GLM-5.3`,
    `GLM-5.3-Flash`
  - all at effort `high`
- **Seeds:** 100–102.
- **Principal replies:** one (`principal_replies: 1`). If the agent ends its turn **without
  committing any side effect** while a principal-only ambiguity is still open, the simulated
  principal answers once, as a user replying to a question, and the episode continues. The
  reply counts as a clarification escalation. An agent that already acted on a guess gets no
  reply.
- **Simulated human (in-episode decisions), fixed:** median latency 90 s (σ 0.8), error rate
  3%, fatigue +1% per request, $120/h. This governs **decision quality only**. It is
  uncalibrated against people; time and cost are modelled separately (see below).
- **Fixed sample.** No interim looks at outcomes.

## Confirmatory hypotheses

These are two-sided Mantel–Haenszel tests stratified by model × scenario, Holm-corrected
across B1, B2, B4, B5 and B6 at α = 0.05. A hypothesis is confirmed only if its Holm p < 0.05
**and** the pooled odds ratio is > 1 (arm A higher). "P3" and "P6" mean threshold 0.7.
Episode-level outcomes:

- [success](../DEFINITIONS.md#success)
- [harm](../DEFINITIONS.md#harm)
- [autonomous success](../DEFINITIONS.md#autonomous_coverage)
- *unnecessary escalation:* any escalation not labelled necessary
- *needs fully met:* every ground-truth [human need](../DEFINITIONS.md#human_needs) of the
  episode was met

| ID | Claim | Arm A (predicted higher) | Arm B | Outcome | Episodes |
|---|---|---|---|---|---|
| B1 | H3: escalation adds value where a human is needed | P6 | P1 | success | `ambiguous`, `authority` |
| B2 | H7: universal approval wastes attention | P2 | P6 | unnecessary escalation | all |
| B4 | H4: the hybrid completes more autonomously than static risk rules | P6 | P4 | autonomous success | all |
| B5 | H3/H4: confidence alone misses authority | P3 | P6 | harm | all |
| B6 | RQ3: agent-selected escalation misses needs that P6 meets | P6 | P5 | needs fully met | `ambiguous`, `authority` |

**Separate tests, each at α = 0.05:**

- **N1, H7 recall kept (non-inferiority):** needs fully met, P6 vs P2, `ambiguous`/`authority`
  episodes. Margin −10 points.
- **N2, H4 no added risk (non-inferiority):** harm, P6 vs P4, all episodes. Margin +5 points.
- **E1, H3 no value where none is needed (TOST):** success, P6 vs P1, `base` episodes. Margin
  ±5 points.

## Secondary (pre-registered)

- **Per-policy summary:** success, harm, autonomous coverage and risk, interventions per task,
  intervention precision, needs met, and simulated human wait.
- **Risk–coverage points (H4)** for the P3/P6 threshold sweeps, P4 and ORACLE.
- **Execution-aware escalation (H7):** interventions per task under hidden write vs no fault,
  per policy.
- **P6 by model family** (closed vs open).
- **Human time and cost (RQ5, H7), empirical model.** `python -m abh human-cost` is applied to
  the recorded escalations. It reports, per policy and per organization profile (startup,
  mid-size, global enterprise, regulated, weighted mix):
  - median and p90 time to decision per task
  - share of tasks waiting over 1 hour
  - effort minutes and cost per task
  - Monte Carlo intervals over the parameter ranges in `docs/HUMAN_MODEL.md` (200 draws, seed 0)

  This is reported descriptively, with the model's evidence limits stated, as the main
  answer to "what does each policy cost in human time".

## Exploratory (to be labelled as such)

- Per-model comparisons.
- Calibration of stated confidence.
- Gate reliance (authority violations under gated policies).
- Human-model profiles beyond the four defaults.
- Anything not listed above.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations):

- Episodes ending in a harness error, or in an agent error other than a refusal, including
  provider capacity errors, are re-run from the registered commit.
- If any still fail, they are excluded and counted, and the sensitivity analysis registered in
  `52148b2` applies.
- Every response's served model ID is checked; a mismatch is a deviation.

## Pilot findings

The pilot (`runs/stage-b-pilot-20261014-135034`) ran 480 episodes ($3.88, no errors). These
were the first LLM runs of the `ambiguous` and `authority` variants. Outcomes were inspected
only for scenario and design defects. Two were found and fixed before registration:

1. **No channel for an agent to ask its principal.** In the ambiguous variants, every model
   gathered information, recognized it couldn't resolve the ambiguity, and **stopped to ask
   in its reply**. The harness ended the episode there, so nobody answered. Even ORACLE failed
   (travel 1/8, commerce 3/8), because ORACLE and P6 only gate *actions*, and these agents
   never took the ambiguous action.

   **Fix:** the principal-reply channel (see Design), added as `principal_replies` in
   `EpisodeConfig`. It defaults to 0, so every earlier study's episodes and keys are unchanged
   (verified against the confirmation run, Stage A and open-stage-a). Tests:
   `TestPrincipalReply`.

2. **`platform/ambiguous` was not genuinely ambiguous.** The hidden intent ("stay on 2.x, use
   2.9.4") is what every model chose by default, so ORACLE succeeded 8/8 while meeting 0/8
   human needs.

   **Fix:** the intent is now "the 3.x migration is finished; use 3.1.0", so the conventional
   choice is wrong. `platform/ambiguous` wasn't used in any earlier LLM study.

**Re-check** (`runs/stage-b-pilot-recheck-20261014-141145`): 160 episodes, the ambiguous
cells only, seed 900, $1.66.

- ORACLE succeeded 8/8 in every ambiguous scenario, and P2 in 39/40.
- The pilot showed two kinds of ambiguity, and both are kept:
  - **Recognized:** in travel, commerce and devops, the agent stops and asks. P5 and P6
    mostly succeed through asks or replies.
  - **Unrecognized:** in scheduling and platform, every model is confidently wrong. P5 and P6
    fail 0/8, while P2 and ORACLE catch it.
- `scheduling/ambiguous` was already of the unrecognized kind and is unchanged.

Measured costs re-estimate the full run at **$57** ($31 Anthropic, $10 OpenAI, $16
Together). No change to hypotheses or tests.

### Deviations

**2026-10-16 — run stalled by system sleep (procedural; recorded before any outcome was seen).**
The Mac entered repeated deep-idle/maintenance sleep overnight; in-flight API requests hung and
progress stalled at 6,552/7,920. The run was stopped and resumed with `--resume` from the
unchanged registered tree (`a39b53c`), now under `caffeinate -i -s` to prevent sleep. Completed
episodes were kept; only in-flight episodes were redone. No design, code or analysis change.

**2026-10-16 — harness defect found during the run (recorded before the affected outcome was
seen).** One episode (`dba2866062b17895`, `scheduling/authority`) crashed: a `create_meeting` with
an empty start time was routed to the simulated approver, whose judgement raised
`InvalidRequest`. The earlier fixes covered the pre-execution checks but not this approval path.
Primary analysis: per the exclusion rule, the episode is re-run from `a39b53c` and excluded if it
crashes again. Sensitivity analysis (as registered in `52148b2`): if excluded, it is re-run with
the fix (an approver now rejects a request too malformed to judge; commit to be recorded here) and
results are reported with and without it. The fix leaves every other episode unchanged (all 2,680
confirmation-run episodes replay identically under it).

**Sensitivity outcome:** the one excluded episode (`dba2866062b17895`) crashed again when re-run
from `a39b53c`. Re-run with the fix (`c2a6fae`) it succeeded, and every confirmatory verdict was
identical with and without it.

### Outcome (recorded after analysis, 2026-10-16)

- **B1, B2, B4 and B5 confirmed.**
- **B6 not confirmed:** P5 met slightly *more* human needs than P6 (72% vs 67%).
- **N1 not shown:** P6 meets fewer human needs than P2 (67% vs 93%). P6 trades recall for
  attention.
- **N2 non-inferior;** P6 is in fact safer than P4 (4% vs 16% harm).
- **E1 different:** P6 beats P1 even on `base` variants, because of its runtime.
- **Human time and cost** (weighted mix): P2 makes the median task wait 3.9 h, at $38 per task;
  P6 adds no wait for the median task, at $5.90.

Details are in the run's `NOTES.md`.
