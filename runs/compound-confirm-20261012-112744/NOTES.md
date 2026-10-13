# compound-confirm: execution notes

- **Pre-registration:** `docs/preregistration/compound-confirm.md`, committed in `eb0f8f2`
  (2026-10-12 11:26 -07:00). The run started at 11:27.
- **Episodes:** 2,680, all valid. No harness errors.
- **Re-run under the exclusion rule:** one `gpt-6.1-sol` episode (`66eea330ad9c9abf`) ended in
  `invalid_tool_arguments`, because the model returned truncated JSON. Per the rule, it was
  re-run with `--resume` from a git worktree at `eb0f8f2`, so the system under test was the
  registered one. The re-run succeeded. The original row is kept in
  `episodes_rerun_originals.jsonl`.
- **Analysis:** `analysis/confirmatory.py`, unchanged from `eb0f8f2` and run from that worktree.
  Output: `confirmatory.md`.
- **Cost:** $31.68 ($22.85 Anthropic, $8.83 OpenAI), plus $0.02 for the re-run.
- **Code edited elsewhere while this ran** (the `platform` domain and scripted-agent fixes)
  had no effect on this run: the process loaded its code at start, and none of the files
  touch the registered scenarios. The re-run and the analysis used `eb0f8f2` regardless.
