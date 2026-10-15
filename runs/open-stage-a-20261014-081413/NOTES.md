# open-stage-a: execution notes

- **Pre-registration:** `docs/preregistration/open-replications.md`, committed in `53d1fc8`
  (2026-10-14 08:13). The run started at 08:14. A deviation note for the crash defect was
  committed in `79a217d` (11:42), before the affected outcome was seen.
- **Episodes:** 4,690. 52 ended in errors and were re-run from a worktree at `53d1fc8`, per the
  exclusion rule:
  - 45 × Together `409 No deployments are ready to serve` (a DeepSeek V4 Flash capacity
    outage; it also slowed the run mid-way)
  - 6 × `max_tokens` (runaway DeepSeek output)
  - 1 × harness crash: empty meeting start time (`8cd9eda0daf106a6`)

  All 52 re-runs succeeded. The originals are in `episodes_rerun_originals.jsonl`. Nothing
  was excluded, so the sensitivity analysis was not needed.
- **Served models:** every response came from exactly the requested model ID.
- **Analysis:** `analysis/replication.py stage-a`, unchanged from `53d1fc8` and run from that
  worktree. Output: `replication_stage_a.md`.
- **Cost:** $15.13 for the main run plus the re-runs, on Together.

## Results: all five replicated

| ID | Original | Result | Verdict |
|---|---|---|---|
| OA1 | A1 | LLM 98% vs workflow 7% success on semantic faults | replicated |
| OA2 | A2 | workflow 21% vs LLM 0% harm on semantic faults | replicated |
| OA3 | A3 (**not** confirmed for the closed models) | 8% harm on single execution faults without a runtime vs 0% with the semantic runtime | replicated |
| OE1 | E1 | LLM 880/880 vs workflow 440/440, execution faults | equivalent |
| OE2 | E2 | semantic runtime 98% vs none 98% on semantic faults | equivalent |

## Exploratory

- **A3 is model-dependent.** The closed models recovered from single, observable execution
  faults on their own (0.5% harm); the open models didn't (8%; DeepSeek V4 Pro 15%). That
  fits the key-discipline finding in `open-confirm`.
- **Naive retry vs no runtime, execution faults:** 162/880 harm vs 74/880. Blind retries
  more than double the harm.
