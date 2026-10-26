# open-confirm: execution notes

- **Pre-registration:** `docs/preregistration/open-replications.md`, committed in `53d1fc8`
  (2026-10-14 08:13). The run started at 08:14.
- **Episodes:** 2,680, all valid. No harness or agent errors; nothing re-run or excluded.
- **Served models:** every response came from exactly the requested model ID, so there are
  no served-model deviations.
- **Analysis:** `analysis/replication.py confirm`, unchanged from `53d1fc8` and run from that
  worktree. Output: `replication_confirm.md`.
- **Cost:** $11.70 on Together.

## Results

| ID | Original | Result | Verdict |
|---|---|---|---|
| OC1 | C1 | 86% harm without keys vs 0% under P6 | replicated |
| OC2 | C2 | end-state harm 77% (weak) vs 82% (strong) | not replicated |
| OC3 | C3 | 12% vs 8% (Holm p = 0.13) | not replicated |
| OC5 | C5 | 12% vs 4% (Holm p = 0.0002) | replicated |
| OE1 | E1 | strong and weak harm equivalent within ±10 points | equivalent |

## Exploratory: key discipline

With keys offered, under hidden write (`P1`), the open models were harmed in 26–85% of
episodes; every closed model in 0%. The traces show why:

| Model | First write carries a key | Retry reuses that key | Harm |
|---|---|---|---|
| Closed models (all four) | 100% | ≈100% | 0% |
| GLM-5.3 | 67% | 65% | 26% |
| GLM-5.3-Flash | 66% | 66% | 33% |
| DeepSeek V4 Flash | 39% | 31% | 34% |
| DeepSeek V4 Pro | 0% | 0% | 85% |

- **The open models often attach a key only on the retry.** That protects nothing, because
  the original request carried no key.
- **This likely explains OC3's non-replication:** models that seldom use keys properly have
  little to over-trust.
- **The P6 runtime attaches keys itself,** and had 0% harm for every model tested so far
  (10 models across all studies).
