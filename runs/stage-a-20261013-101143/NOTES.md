# stage-a: execution notes

- **Pre-registration:** `docs/preregistration/stage-a.md`, committed in `eda3331` (2026-10-13 10:10).
  The run started at 10:11.
- **Episodes:** 4,690, all valid.
- **Re-run under the exclusion rule:** one harness crash, `9e3cedef96cf4c9c` (`platform/base`,
  malformed `files` argument; see the deviation note). It was re-run from a worktree at
  `eda3331` and succeeded, since the model formed its arguments correctly the second time. The
  original row is kept in `episodes_rerun_originals.jsonl`. Nothing was excluded, so the
  sensitivity analysis registered in `52148b2` was not needed.
- **Analysis:** `analysis/stage_a.py`, unchanged from `eda3331` and run from that worktree.
  Output: `stage_a.md`.
- **Cost:** $38.24 ($28.20 Anthropic, $10.04 OpenAI).

## Exploratory (not pre-registered)

- **Naive retry vs no runtime, execution faults:** 40/880 harm (each model exactly 10/220)
  vs 4/880. Blind infrastructure retries cause duplicates regardless of the model. The
  scripted runs predicted this, by construction.
- **E2:** the verdict is "equivalent" within ±10 points, but the difference test is also
  significant (97% vs 91%). The semantic runtime helps on semantic faults by a few points,
  mostly on `persistent_unavailable`, where it backs off and then reports clearly that the
  tool is unavailable.
