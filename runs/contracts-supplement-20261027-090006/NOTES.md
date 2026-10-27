# Contract study supplement: DeepSeek-V4.1-Flash-1017 (exploratory)

- **Why it exists:** Together withdrew `DeepSeek-V4-Flash-0731` during the contract study, so
  all 560 of its episodes were excluded under the registered rule (see Deviations in
  [contracts.md](../../docs/preregistration/contracts.md)).
- **When it was decided:** on 2026-10-27, before the main analysis was run, the same design was
  run with this substitute.
- **Status: exploratory, never pooled with the confirmatory tests.**
  - [contracts.md](contracts.md) in this folder was produced by the same script. Its
    "confirmatory" and "pre-registered" headings **don't apply here**.
  - With one model and 90 episodes per arm, it has little power.
- **Spec:** [`experiments/contracts_supplement.json`](../../experiments/contracts_supplement.json).
  The manifest marks the tree as not clean because that new spec file was uncommitted; all code
  was at `45b0e78`.
- **Execution:** 560 episodes, $1.41, no errors. Every response came from
  `deepseek-ai/DeepSeek-V4.1-Flash-1017`.

**Results** (harm under a hidden partial commit, 90 episodes per arm):

| A | B | C | D | N |
|---|---|---|---|---|
| 1% | 2% | 1% | 2% | 0% |

- Hidden write: 2/40 vs 0/40.
- The model barely shows the keys hazard, so it says little about scope or wording.
- It's not a stand-in for V4 Flash, whose earlier key discipline was poor (first write keyed in
  39% of episodes, open-confirm).
