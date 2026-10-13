# Coverage: prospectus vs. harness vs. evidence

Status as of 2026-10-12, after the confirmation run. "Harness" means the code can run the condition. "Scripted" means it
has run with scripted agents, which validates the harness but is not evidence (see
[note](DEFINITIONS.md#note-scripted_not_evidence)). "LLM" means it has run with real models.
Update this file when runs land.

Legend: ✅ covered · 🟡 partial · ❌ not yet

## Research questions

| | Question | Harness | Scripted | LLM | Gap |
|---|---|---|---|---|---|
| RQ1 | Failure ownership by failure class | ✅ | ✅ all 12 faults | 🟡 3 of 12 faults, compound only | single-fault matrix with LLMs (Stage A) |
| RQ2 | Recovery composition as models improve | ✅ runtime is an independent factor | ✅ `runtime_factorial` | 🟡 P1 vs P6; keys ablation; 2 tiers × 2 families | runtime factorial with LLMs (`naive_retry`, P1+`semantic`); top tier (Stage A, C) |
| RQ3 | When is human intervention necessary? | ✅ | ✅ | ❌ no `ambiguous`/`authority` variants run with LLMs | Stage B |
| RQ4 | Autonomy vs. risk at fixed risk | ✅ P3/P6 threshold sweeps | ✅ | ❌ | Stage B |
| RQ5 | Cost of oversight | 🟡 simulated human, uncalibrated | ✅ | 🟡 model cost/latency only; no human cost | Stage B, plus a human calibration pilot |

## Hypotheses

| | Hypothesis | LLM evidence | Next |
|---|---|---|---|
| H1 | Runtime beats model recovery on execution failures | ✅ **confirmed** (C1: 70% harm without keys vs 0% under P6; 4 models, 30 seeds), for 3 execution faults | extend to all execution faults (Stage A) |
| H2 | Agent beats deterministic recovery on semantic failures | ❌ no semantic faults run with LLMs | **Stage A ready**: `experiments/stage_a.json`, pre-registration draft `docs/preregistration/stage-a.md`; pilot first |
| H3 | Humans add most value for authority / consequential ambiguity | ❌ | Stage B |
| H4 | Hybrid (P6) dominates P1–P5 on risk–coverage | ❌ only P1 vs P6 | Stage B |
| H5 | Scaling helps semantic recovery, not execution ambiguity | 🟡 **C2 confirmed**: stronger models leave less end-state harm (32% vs 75%). **E1 not equivalent**: stronger models also cause somewhat less harm (64% vs 76%), so "doesn't prevent" holds only in the weaker form "doesn't come close to preventing". No top tier yet | Stage C (frontier tier) |
| H6 | Handling failures below the model saves tokens/calls | ✅ strong for all 4 models (p<10⁻⁷) | none needed |
| H7 | Execution-aware escalation saves human attention without losing recall | ❌ | Stage B |
| new | Offering idempotency keys can *increase* harm under a hidden partial commit | ✅ **confirmed** (C3: 30% vs 1%), larger for the OpenAI models (C4: 47% vs 13%), and driven by the "at most once" wording (C5: 30% vs 3% with caveated wording) | key-reuse with different parameters (harness item 6); `platform` domain |

## Experimental conditions (prospectus §5–§7)

| Condition | Harness | Scripted | LLM |
|---|---|---|---|
| P1 Full autonomy | ✅ | ✅ | ✅ |
| P2 Universal approval | ✅ | ✅ | ❌ |
| P3 Confidence HITL (+ threshold sweep) | ✅ | ✅ | ❌ |
| P4 Static risk HITL | ✅ | ✅ | ❌ |
| P5 Agent-selected HITL | ✅ | ✅ | ❌ |
| P6 Semantic/runtime-aware | ✅ | ✅ | ✅ |
| ORACLE | ✅ | ✅ | ❌ |
| Fault taxonomy (12 types) | ✅ | ✅ | 🟡 timeout-after, delayed visibility, partial mutation |
| Compound faults | ✅ | ✅ | ✅ |
| Action types (read-only → irreversible) | ✅ present in all base scenarios | ✅ | 🟡 present, not yet analysed by action type |
| Domains (5; `platform` added 2026-10-12) | ✅ | 🟡 `platform` swept with scripted agents only | 🟡 `base` variants of the original 4 only |
| Variants (`ambiguous`, `authority`) | ✅ | ✅ | ❌ |
| Model families and capability levels | ✅ Anthropic, OpenAI | n/a | 🟡 2 families × 2 tiers; no top tier, no third family |
| Failure *frequencies* (Phase IV) | ❌ faults are scheduled at a call, not injected at a rate | ❌ | ❌ |
| Human attention as a constrained resource | 🟡 per-episode budget and fatigue; no shared reviewer pool | 🟡 | ❌ |
| Human parameters calibrated to people | 🟡 interactive mode exists | ❌ | ❌ |

## Proposed stages

Costs are estimates at the per-episode costs observed in `compound-live`, for 4 models at 5
seeds. Gated policies run longer episodes, so Stage B includes +30%. Price exact numbers with
`analysis/estimate_cost.py` once each stage has a spec.

| Stage | Covers | Design | Episodes | Est. cost |
|---|---|---|---|---|
| Confirmation (ready) | H1, H5, keys hazard | `experiments/compound_confirm.json` | 2,680 | ~$32 ($42 with headroom) |
| A | H2, RQ1, RQ2 | 4 `base` scenarios × no fault + each supported single fault × {P1, P1+`naive_retry`, P1+`semantic`, P6} | ~4,000 | ~$40 |
| B | H3, H4, H7, RQ3, RQ4, RQ5 | all 12 scenarios × {no fault, hidden write} × {P1, P2, P3×3 thresholds, P4, P5, P6×3 thresholds, ORACLE} | ~5,300 | ~$70 |
| C | H5 at the frontier | Fable 5.1 + `gpt-6-astra` on the confirmation design's main block | 840 | ~$60 |

Harness work these stages don't cover:

1. **Rate-based fault injection**, for Phase IV's failure frequencies.
2. **A shared reviewer pool** across concurrent episodes. Needed for RQ5 at scale, and the
   seed of Paper 5.
3. **A small interactive pilot with real people**, to calibrate human latency and error rates
   before making claims about human cost.
4. **More scenarios.** LLM results currently generalise to four tasks. `platform` (repo / CI /
   PR) is built and scripted-validated: 3 variants, all 12 faults.
5. **Optionally, a third model family.**
6. **Idempotency keys reused with different parameters.** Our services return the stored result
   for a reused key even when the request differs. Real APIs such as Stripe reject that.
   `platform` showed the hazard: a CI re-run that reused a key got the stale run from the old
   commit. Make this a per-service policy (`return_stored` vs `reject_mismatch`) and study it.
   Deferred until the confirmation run's analysis is done, because the pre-registration freezes
   the system under test.
