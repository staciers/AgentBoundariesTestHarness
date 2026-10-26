# Pre-registration: Stage D (runtime × policy factorial, P6 component ablation)

**Status:** draft. It becomes registered when committed, **after the pilot and before the
main run**. Scenario or harness defects the pilot reveals may be fixed before then (record
them under *Pilot findings*). After the commit, change nothing listed here.

| | |
|---|---|
| Spec | [`experiments/stage_d.json`](../../experiments/stage_d.json): 10,800 episodes |
| Pilot spec | [`experiments/stage_d_pilot.json`](../../experiments/stage_d_pilot.json): 300 episodes, seed 900, 2 models, the new arms only; not analysed |
| Analysis | [`analysis/stage_d.py`](../../analysis/stage_d.py), run unchanged |
| Origin of hypotheses | the Stage B confound (below), a review of the Stage B results, and an exploratory look at Stage B's no-fault cells |
| Definitions | [DEFINITIONS.md](../DEFINITIONS.md) |

## Question

In [Stage B](stage-b.md), each policy ran with its default runtime: P1–P5 with none, P6 and
ORACLE with the semantic runtime. B1, B4, B5 and E1 therefore measured P6's **delegation
rules and its runtime together**. A reviewer would rightly say the result may show only that a
better runtime helps.

Stage D asks two questions:

1. **Is there a delegation effect when the runtime is held fixed?** Every policy is run at
   both runtime levels.
2. **Which part of P6 produces it?** P6 has three parts, and each can be switched off:
   - a deterministic **authority gate**
   - a **confidence gate** on consequential actions
   - **routing** of unresolved consequential execution outcomes to a human

**What is already known (exploratory, from Stage B; stated here so it is not mistaken for a
result):**
- In the no-fault cells, where the runtime has nothing to recover, P6 still beat P1 (76% vs 47%
  success, 5% vs 10% harm) and P4 (71%, 9%).
- In P6's 720 episodes, the authority gate fired 227 times, the confidence gate 6 times, and
  routing to a human never, because the semantic runtime resolved every hidden write.

The component predictions below follow from those counts.

## Design

- **Scenarios, fault conditions, models, seeds, simulated human, principal replies:**
  identical to [Stage B](stage-b.md#design).
  - all 15 scenarios
  - no fault, and *hidden write* (`timeout_after_execution` + `delayed_visibility`)
  - 8 models (4 closed, 4 open-weight via Together), all at effort `high`
  - seeds 100–102
  - `principal_replies: 1`
- **Factorial block:** `P1`, `P3` (threshold 0.7), `P4`, `P5`, `P6` (threshold 0.7) and `ORACLE`,
  each at runtime `none` **and** `semantic`. 12 arms.
  - P2 is omitted: it gates every write, so its runtime level doesn't bear on the delegation
    question.
- **Component block:**
  - `P6[authority_gate=false]`, semantic runtime
  - `P6[confidence_gate=false]`, semantic runtime
  - `P6[route=agent]`, runtime **none**: the only level at which routing can fire
- Each arm has 720 episodes; 15 arms make 10,800 in total.
- **All arms run concurrently in one run,** so no comparison crosses runs or dates. Stage B data
  is not reused.
- **Fixed sample.** No interim looks at outcomes.

## Confirmatory hypotheses

These are two-sided Mantel–Haenszel tests, stratified by model × scenario, with Holm
correction within each family at α = 0.05. A hypothesis is confirmed only if its Holm p < 0.05
**and** the pooled odds ratio is > 1 (arm A higher). "Non-base" means the `ambiguous` and
`authority` variants. Outcomes:
- [success](../DEFINITIONS.md#success)
- [harm](../DEFINITIONS.md#harm)
- [autonomous success](../DEFINITIONS.md#autonomous_coverage)

### Primary family: delegation and runtime effects

| ID | Claim | Arm A (predicted higher) | Arm B | Outcome | Episodes |
|---|---|---|---|---|---|
| D1 | Delegation helps where a human is needed, runtime held at semantic | P6 / semantic | P1 / semantic | success | non-base |
| D2 | The same, runtime held at none | P6 / none | P1 / none | success | non-base |
| D3 | Without delegation, more harm, runtime held at semantic | P1 / semantic | P6 / semantic | harm | all |
| D4 | Confidence-only gating misses authority, runtime held at semantic (deconfounded B5) | P3 / semantic | P6 / semantic | harm | all |
| D5 | P6 completes more autonomously than static risk rules, runtime held at semantic (deconfounded B4) | P6 / semantic | P4 / semantic | autonomous success | all |
| D6 | The runtime prevents harm, policy held at P6 | P6 / none | P6 / semantic | harm | hidden write |

### Component family: which part of P6 earns the effect

| ID | Claim | Arm A (predicted higher) | Arm B | Outcome | Episodes |
|---|---|---|---|---|---|
| K1 | The authority gate prevents harm | P6[authority_gate=false] / semantic | P6 / semantic | harm | `authority` |
| K3 | Routing unresolved outcomes to a human prevents harm when there is no runtime | P6[route=agent] / none | P6 / none | harm | hidden write |

**Separate test, α = 0.05:**
- **K2: the confidence gate contributes little (TOST):** success, P6 vs
  P6[confidence_gate=false], semantic runtime, all episodes. Margin ±5 points.

### Decision rule (pre-registered)

**A distinct delegation effect is established if D1, D2 and D3 are all confirmed:** P6's
delegation rules improve outcomes at both runtime levels, independently of the runtime. This
is the first of the two conditions for pursuing an OSDI framing. The second (a stronger
baseline and held-out workloads) is a separate, later study.

If D1–D3 are not all confirmed, the paper is framed as an empirical study of execution
boundaries, and P6 is presented as a combination of known mechanisms.

## Secondary (pre-registered)

- **Policy × runtime grid:** success, harm, end-state harm, autonomous success, autonomous
  harmful share, and interventions per task, for every arm.
- **Delegation effect by fault condition:** P6 − P1 success on non-base tasks, at each runtime
  level, separately for no fault and hidden write.
- **Interaction:** a logistic regression of success and of harm on P6 × semantic runtime, with
  model and scenario fixed effects (P1 and P6 arms). This is reported descriptively; if it does
  not fit, that is reported.
- **Which component fired:** authority-gate, confidence-gate, routed-to-human and
  principal-reply escalations per 100 episodes, for each P6 arm.

## Exploratory (to be labelled as such)

- Per-model and per-family effects.
- Comparisons with Stage B.
- The other policy × runtime contrasts (P3, P4, P5 and ORACLE at each runtime level).
- Anything not listed above.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations):
- Episodes ending in a harness error, or in an agent error other than a refusal (including
  provider capacity errors), are re-run from the registered commit.
- If any still fail, they are excluded and counted, and the sensitivity analysis registered in
  `52148b2` applies.
- Every response's served model ID is checked; a mismatch is a deviation.
- The run uses `caffeinate -i -s` from the start.

## Cost

Stage B averaged $0.0087 per episode on the same models and scenarios, so the main run is
estimated at **about $94**. The pilot is estimated at **about $2** (300 episodes, on the two
cheapest models). The pilot's measured cost replaces this estimate before registration.

## Pilot findings

The pilot (`runs/stage-d-pilot-20261018-104306`) ran 300 episodes (Haiku and GLM-5.3-Flash,
seed 900) for **$0.38**: $0.16 Anthropic, $0.23 Together.
- **No defects found:** no harness or agent errors, and every GLM response was served by
  `zai-org/GLM-5.3-Flash`.
- Outcomes were inspected only to check that each new switch does what it says, by counting
  escalation triggers per arm:
  - `authority_gate=false`: no authority escalations.
  - `confidence_gate=false`: no confidence escalations; the authority gate still fired.
  - `route=agent` at runtime `none`: no execution-state escalations, vs 22 in the 60 P6 episodes
    at runtime `none`.
  - With the gate on, the confidence gate fired once in 120 P6 episodes, consistent with Stage B.
- **No change to the design, hypotheses or tests.**

**Cost re-estimate:** Stage B's measured per-model costs × 1,350 episodes per model give
**$94**: $52 Anthropic, $15 OpenAI, $27 Together.

### Deviations

*(None yet.)*

### Outcome (recorded after analysis, 2026-10-18)

Run `runs/stage-d-20261018-111143`: 10,800 episodes, $86.25. 5 `max_tokens` episodes were
re-run from `32cb181` and all succeeded; nothing was excluded. Every response came from the
requested model.

- **Decision rule met:** D1, D2 and D3 confirmed. P6's delegation effect holds with the runtime
  held fixed, at both runtime levels.
- **D4 and D5 confirmed:** B5 and B4, deconfounded.
- **D6 not confirmed:** with no runtime, P6 routes unresolved outcomes to a human, and harm stays
  low (4% vs 3%). The cost moves to human attention (0.84 vs 0.45 interventions per task).
- **K1 and K3 confirmed;** K2 equivalent. The effect comes from the authority gate and from
  routing; the confidence gate is inert.

Details, and the exploratory P5 comparison, are in the run's `NOTES.md`.
