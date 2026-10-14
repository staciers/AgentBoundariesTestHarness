# Pre-registration: open-weight replications (confirmation design + Stage A)

**Status:** draft. It becomes registered when committed, **before either run starts**. The
pilot (`runs/open-pilot-20261013-143116`, 252 episodes, $0.79) already ran and found no defects:
every model succeeded, and every response came from the requested model. After the commit,
change nothing listed here; record deviations at the end.

| | |
|---|---|
| Specs | [`experiments/open_confirm.json`](../../experiments/open_confirm.json) (2,680 episodes), [`experiments/open_stage_a.json`](../../experiments/open_stage_a.json) (4,690, incl. 630 free workflow episodes) |
| Analysis | [`analysis/replication.py`](../../analysis/replication.py): `confirm <run>` and `stage-a <run>`, run unchanged. It reuses the frozen helpers of `analysis/confirmatory.py` and `analysis/stage_a.py` |
| Originals | [compound-confirm](compound-confirm.md) and [stage-a](stage-a.md); same cells, blocks, seeds and tests |
| Definitions | [DEFINITIONS.md](../DEFINITIONS.md) |

## Question

Do the confirmed results hold for two further, open-weight model families? The original
studies used two closed families (Anthropic, OpenAI). These replications add two open ones,
again in matched strong/weak pairs.

## Models (hosted on Together; IDs verified, prices from together.ai/pricing, 2026-10-13)

| Family | Strong | Weak |
|---|---|---|
| DeepSeek | `deepseek-ai/DeepSeek-V4-Pro-0813` | `deepseek-ai/DeepSeek-V4-Flash-0731` |
| GLM | `zai-org/GLM-5.3` | `zai-org/GLM-5.3-Flash` |

- All four run at reasoning effort `high`, via the `compat` adapter.
- **Pinned versions:** dated DeepSeek snapshots and full-precision GLM listings, not the
  FP8 variants.
- **Served-model check:** every response's served model ID is recorded. Any mismatch with
  the requested ID is reported as a deviation.

## Confirmatory hypotheses

Each replication is its own Holm family at α = 0.05. A hypothesis is **replicated** if its
Holm-adjusted p < 0.05 **and** the pooled Mantel–Haenszel odds ratio is > 1 (arm A higher).
The arms, outcomes and strata are those of the original test, with the open models'
tiers and families in place of the closed ones.

### open-confirm

| ID | Original | Claim | Arms (A > B) | Outcome | Strata |
|---|---|---|---|---|---|
| OC1 | C1 | the runtime prevents what reasoning can't | hidden write: no keys > P6 | harm | model × scenario |
| OC2 | C2 | stronger models leave less lasting damage | hidden write, no keys: weak > strong | end-state harm | family × scenario |
| OC3 | C3 | offering keys increases harm under a hidden partial commit | `P1` > no keys | harm | model × scenario |
| OC5 | C5 | "at most once" wording drives the hazard | `P1` > caveated wording | harm | model × scenario |

- **OE1 (= E1):** TOST, ±10 points, on any harm, strong vs weak, hidden write with no keys.
- **C4 is not replicated as a confirmatory test.** Its prediction, "OpenAI > Anthropic", has
  no open-weight counterpart, and there is no basis for predicting whether DeepSeek or GLM
  shows the keys hazard more. The family difference is reported as an **exploratory,
  two-sided** test.

### open-stage-a

| ID | Original | Claim | Arms (A > B) | Outcome | Strata |
|---|---|---|---|---|---|
| OA1 | A1 | agents recover from semantic faults; a workflow can't | semantic faults: LLM (semantic runtime) > workflow | success | scenario × fault |
| OA2 | A2 | without reasoning, semantic faults cause harm | semantic faults: workflow > LLM | harm | scenario × fault |
| OA3 | A3 | no runtime causes more harm on single execution faults | execution faults: `P1` > semantic runtime | harm | model × scenario × fault |

- **OE1 (= E1):** TOST, ±5 points. Execution faults, semantic runtime: LLM vs workflow
  success.
- **OE2 (= E2):** TOST, ±10 points. Semantic faults, LLM: semantic runtime vs no runtime
  success.
- **A3 was *not* confirmed in the original study.** It's kept here as registered, so a
  non-replication is the expected outcome, not a surprise.

## Secondary (pre-registered)

The same secondary analyses as the originals:

- **open-confirm:** per-model rates, and mechanism M1 (checking state before retrying).
- **open-stage-a:** controller × fault class, the runtime factor, and failure ownership.

## Exploratory (to be labelled as such)

- The DeepSeek vs GLM family difference in the keys hazard.
- Naive retry vs no runtime.
- **All open vs closed comparisons.** These are cross-run comparisons, made at different
  times on a different provider.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations):

- Episodes ending in a harness error, or in an agent error other than a refusal, are re-run
  from the registered commit.
- If any still fail, they are excluded and counted.
- If any are excluded, the sensitivity analysis registered in `52148b2` also applies.

### Deviations

_None yet._
