# Pre-registration: Stage C (frontier tier)

**Status:** draft. It becomes registered when committed, **after the pilot and before the
main run**. Scenario or adapter defects the pilot reveals may be fixed before then (record
them under *Pilot findings*). After the commit, change nothing listed here.

| | |
|---|---|
| Spec | [`experiments/stage_c.json`](../../experiments/stage_c.json) |
| Pilot spec | [`experiments/stage_c_pilot.json`](../../experiments/stage_c_pilot.json): seed 900, frontier models only, not analysed |
| Analysis | [`analysis/stage_c.py`](../../analysis/stage_c.py) `<run> runs/compound-confirm-20261012-112744`, run unchanged |
| Origin of hypotheses | G1, G2, G3 and G5 come from the prospectus (H1, H5, H2). G4 replicates the confirmed keys hazard (C3). |
| Definitions | [DEFINITIONS.md](../DEFINITIONS.md) |

## Question

Do the confirmed results hold at the frontier tier? Two answers would decide the paper's
H5 framing:

- If scale **removes** the need for the runtime, the paper's argument weakens.
- If scale only **improves recovery**, the argument strengthens: the runtime is still needed
  at the frontier.

## Design

- **Frontier models:** `claude-fable-5-1` and `gpt-6-astra`, at effort `high`.
- **Same cells and seeds as the earlier runs.** The fault conditions match the
  [confirmation run](compound-confirm.md): *hidden write* and *hidden partial commit*. The
  semantic faults and the workflow controller match [Stage A](stage-a.md).

| Block | Controllers | Cells | Policies | Seeds |
|---|---|---|---|---|
| H1/H5 | frontier | hidden write, 4 base scenarios | `P1[expose_keys=False]` | 100–129 |
| keys hazard | frontier | hidden partial commit, 3 base scenarios | `P1`, `P1[expose_keys=False]` | 100–129 |
| P6 reference | frontier | both | `P6[threshold=0.7]` | 100–109 |
| H2 | frontier | semantic faults, 5 base scenarios incl. `platform` | `P1[runtime=semantic]` | 100–109 |
| workflow baseline | `scripted:workflow` | semantic faults, 5 scenarios | `P1[runtime=semantic]` | 100–109 |
| drift anchor | Opus 5.5, `gpt-6.1-sol` | hidden write / hidden partial commit | `P1[expose_keys=False]` / `P1` | 100–109 |

- **Size:** 1,300 episodes (1,160 LLM). The cost will be re-estimated from the pilot.

## Drift gate (decided now, applied before G3)

G3 compares the frontier with the *strong* tier. The comparator is the confirmation run's
Opus 5.5 and `gpt-6.1-sol` episodes in identical cells, which is valid only if those models
haven't changed since.

**Rule:** for each anchor model, compare its Stage C episodes (seeds 100–109) with its
confirmation-run episodes at the same seeds, using Fisher's exact test, on three cells:

- hidden write, harm
- hidden write, end-state harm
- hidden partial commit with keys, harm

If **any** comparison has p < 0.05, or an anchor cell is missing, drift is declared. G3
then uses the concurrent anchor (seeds 100–109) as its comparator. Otherwise G3 uses the
confirmation run's strong models (seeds 100–129).

## Confirmatory hypotheses

All five are tested together, with Holm correction at α = 0.05. G2 is a one-sided exact
binomial test against a 10% floor; the others are two-sided Mantel–Haenszel tests. A
hypothesis is confirmed only if its Holm-adjusted p < 0.05 **and** the effect points the
predicted way.

| ID | Claim | Arm A (predicted higher) | Arm B | Outcome | Strata |
|---|---|---|---|---|---|
| G1 | H1 at the frontier: the runtime still prevents what reasoning can't | frontier, hidden write, no keys | frontier, hidden write, P6 | harm | model × scenario |
| G2 | H5: scale doesn't eliminate execution ambiguity | frontier, hidden write, no keys | floor of 10% | harm | n/a |
| G3 | H5: recovery improves with scale | strong (per the drift gate) | frontier | end-state harm | provider × scenario |
| G4 | The keys hazard persists at the frontier | frontier, hidden partial commit, `P1` | frontier, hidden partial commit, no keys | harm | model × scenario |
| G5 | H2 at the frontier | frontier, semantic faults | workflow, semantic faults | success | scenario × fault |

**How the H5 results would read:**

- **G2 and G3 both confirmed:** scale improves recovery but doesn't remove the need for the
  runtime.
- **G2 not confirmed:** scale eliminates the execution-ambiguity harm. That would be a
  substantive negative result for the paper's framing, and it must be reported.

## Secondary (pre-registered)

- Harm, end-state harm, self-corrected harm and success for every model × cell.
- Mechanism M1 (checking state before retrying) under the hidden partial commit, for the
  frontier and anchor models.
- Mean cost and model latency per episode (RQ5). Frontier turns can be long.

## Exploratory (to be labelled as such)

- Comparisons with the weak tier (Haiku, Luna).
- Anything not listed above.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations):

- Episodes ending in a harness error, or in an agent error other than a refusal, are re-run
  from the registered commit.
- Refusals stay in the data as recorded outcomes. Fable 5.1 runs safety classifiers, and
  server-side fallbacks are off, so a refusal is not swapped for another model.
- **API access:** Fable 5.1 requires 30-day data retention, and requests from a
  zero-data-retention org fail with a 400. If the pilot shows that, Stage C can't run as
  designed. Record it and stop.

## Pilot findings

The pilot (`runs/stage-c-pilot-20261013-104810`) ran 48 episodes: seed 900, frontier models only,
no errors. Both models are reachable; Fable 5.1 returned no data-retention 400s.

- **No scenario or adapter defects.** Outcomes were inspected only for defects. Fable was
  harmed in all 4 hidden-write, no-keys episodes; that is the designed hazard, which every
  model hits (54–77% in the confirmation run), not a defect pattern.
- **Measured costs:** $0.102 per episode for Fable 5.1 and $0.064 for `gpt-6-astra`, with
  mean model latency of 16 s and 23 s. The full run is re-estimated at **$91** ($56
  Anthropic, $36 OpenAI), up from the $75 list-price estimate.

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
  confirmation-run episodes with the fix reproduced every one exactly. Stage C shares the code (it includes `platform/base` semantic-fault cells), so the same plan applies.

### Outcome (recorded after analysis, 2026-10-13)

The run completed with 1,300 valid episodes and no exclusions. The drift gate found no drift.

- **G1 confirmed:** the runtime still prevents all harm at the frontier (78% harm vs 0%).
- **G2 confirmed:** the frontier is harmed in 78% of hidden-write episodes without keys, far
  above the 10% floor.
- **G4 confirmed:** the keys hazard persists at the frontier (9% vs 0%).
- **G5 confirmed:** H2 holds at the frontier (100% success on semantic faults vs 7% for the
  workflow).
- **G3 not confirmed, and significant in the opposite direction.** Frontier end-state harm
  was 64% vs 32% for the strong tier, driven by Fable 5.1 (115/120). So "recovery improves
  with scale" is refuted for this design.

The exploratory trace analysis is in the run's `NOTES.md`.

