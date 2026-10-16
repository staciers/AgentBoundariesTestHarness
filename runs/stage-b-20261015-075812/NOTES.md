# stage-b: execution notes

- **Pre-registration:** `docs/preregistration/stage-b.md`, committed in `a39b53c`
  (2026-10-15 07:51). The run started at 07:58.
- **Stall:** the Mac slept overnight (repeated deep-idle/maintenance sleep), which hung in-flight
  requests at 6,552/7,920. The run was stopped on 2026-10-16 and resumed from the unchanged
  registered tree under `caffeinate -i -s`. Completed episodes were kept. Logged as a procedural
  deviation before any outcome was seen.
- **Errors (3), re-run from a worktree at `a39b53c`:**
  - `78a0ed3aa0ba3e79` (`max_tokens`): succeeded on re-run.
  - `d3d983895bf08a45` (harness crash: `merge_pr` sent for approval without a PR number):
    succeeded on re-run.
  - `dba2866062b17895` (harness crash: meeting start time "TBD…" in the approval path): crashed
    again, so it is **excluded** (1 of 7,920).
- **Sensitivity analysis:** the excluded episode was re-run with the fix (`c2a6fae`) in
  `runs/stage-b-20261015-075812-sensitivity/` and succeeded. **Every confirmatory verdict is
  identical with or without it.**
- **Fixes after the run:** the approver path now also covers `approver_accepts`. Both fixes
  leave every other episode unchanged.
- **Served models:** every response came from exactly the requested model ID.
- **Analysis:** `analysis/stage_b.py` and `abh human-cost`, unchanged from `a39b53c` and run from
  that worktree. Outputs: `stage_b.md` and `human_cost.md`.
- **Cost:** $69.12 ($38.40 Anthropic, $10.97 OpenAI, $19.75 Together), above the $57 estimate
  (escalation-heavy episodes ran longer than the pilot suggested).

## Results

| ID | Claim | Result | Verdict |
|---|---|---|---|
| B1 | H3: escalation adds value where a human is needed | P6 65% vs P1 18% success (ambiguous/authority) | confirmed |
| B2 | H7: universal approval wastes attention | episodes with an unnecessary escalation: P2 79% vs P6 1% | confirmed |
| B4 | H4: more autonomy than static risk rules | autonomous success: P6 34% vs P4 13% | confirmed |
| B5 | Confidence alone misses authority | harm: P3 39% vs P6 4% | confirmed |
| B6 | P6 meets needs that P5 misses | needs fully met: P6 67% vs P5 72% (the opposite direction) | not confirmed |
| N1 | H7: recall kept vs P2 | P6 67% vs P2 93% | not shown |
| N2 | H4: no added risk vs P4 | harm: P6 4% vs P4 16% | non-inferior (better) |
| E1 | H3: no value where none is needed | `base`: P6 100% vs P1 91% | different (P6 better; its runtime handles the hidden write) |

**Human time and cost** (empirical model, weighted organization mix):

- **P2:** median wait[^wait] 3.9 h per task; 82% of tasks wait over 1 h; $38 of human effort per task.[^cost]
- **P6:** median wait[^wait] 0; 24% of tasks wait over 1 h; $5.90 per task.[^cost]

[^wait]: Time to decision from the empirical human model, defined in [DEFINITIONS.md](../../docs/DEFINITIONS.md#human_time_to_decision): the minutes an agent waits on humans in one task, summed over its escalations, with organization coverage, after-hours arrival, runbooks and approval chains applied. "Median" is across tasks, then the median across 200 Monte Carlo draws; see `human_cost.md` for the 5th–95th percentile intervals.
[^cost]: Human effort cost per task, defined in [DEFINITIONS.md](../../docs/DEFINITIONS.md#human_effort_cost_per_task) and computed as described in [HUMAN_MODEL.md → How the outputs are computed](../../docs/HUMAN_MODEL.md#how-the-outputs-are-computed). Cost = active human minutes ÷ 60 × the organization's hourly rate, averaged over tasks, then the median across 200 Monte Carlo draws. Waiting time is not costed. For P2: 2.68 escalations per task → 17.6 effort-minutes per task × $127.50/h (the weighted mix's average rate) ÷ 60 ≈ $37.40, reported as **$38.22** (interval $13.01–65.07; a median of per-draw means, so not exactly the product). For P6: 0.45 escalations per task → 2.7 effort-minutes → **$5.86** ($2.07–9.23). This is the empirical model's cost, not the episode field `human_cost_usd` (simulated wait × rate).
