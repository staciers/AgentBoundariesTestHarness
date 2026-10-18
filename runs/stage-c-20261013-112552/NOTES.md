# stage-c: execution notes

- **Pre-registration:** `docs/preregistration/stage-c.md`, committed in `d5c4cb3` (2026-10-13 11:24).
  The run started at 11:25.
- **Episodes:** 1,300, all valid. No harness or agent errors, so nothing was re-run and
  nothing was excluded. The sensitivity analysis added in `52148b2` was therefore not needed.
- **Analysis:** `analysis/stage_c.py`, unchanged from `d5c4cb3` and run from a worktree at that
  commit. Output: `stage_c.md`.
- **Drift gate:** no drift (every anchor comparison p ≥ 0.41). G3 used the confirmation run's
  strong models, as registered.
- **Cost:** $80.12 ($48.75 Anthropic, $31.37 OpenAI).

## Exploratory analysis (not pre-registered)

Hidden write, no keys. I looked at the traces to rule out an artifact behind G3's reversal
(Fable left more lasting damage than the strong tier).

- **Every model checked state after the timeout** (480/480), and every Fable episode ended
  normally.
- **Two behaviours determine the outcome:** whether the model retries after its check comes
  back empty, which creates the duplicate, and whether it verifies after the retry, which
  lets it repair.

| Model | Retried | Verified after retry | Lasting (end-state) damage |
|---|---|---|---|
| Opus 5.5 | 100% | 88% | 25% |
| Haiku 5.5 | 100% | 50% | 74% |
| gpt-6.1-sol | 68% | 44% | 38% |
| gpt-6-astra | 53% | 39% | 33% |
| Fable 5.1 | 100% | 28% | 96% |
| gpt-6-luna | 75% | 0% | 100% |

- **When Fable did verify after retrying, the duplicate was visible in all 34 cases**
  (delay elapsed), but it repaired only 4.
- **In the traces, Fable misreads the evidence.** For example, a "conflict" error caused by its
  own first meeting was taken to mean someone else had booked the slot. Fable then created a
  third meeting and reported "no duplicates". Its final messages repeatedly assert, wrongly,
  that only one charge, order, page or invite exists.
- **A measurement error was corrected along the way.** A first version of the
  "verified after retry" measure counted reads after *any* second write, which miscounts
  `devops/base`, where the rollback is also a write. It was redone to key on the retry of the
  faulted tool itself.
