# Results synthesis: Autonomy Boundaries for Agentic Systems

*Allocating control across runtimes, agents and humans in stateful tool-using AI systems*

**Status:** results through 2026-10-27. Eleven pre-registered studies are complete: 50,162
LLM episodes across 11 models (4 families plus a frontier tier), at $461.34 total API spend,
including pilots, exploratory runs and re-run episodes. (Deterministic workflow-baseline
episodes are additional and cost nothing.)

**How to read this document:**

- Every result is labelled **confirmatory** (pre-registered: a hypothesis, test and decision rule
  committed before the data existed) or **exploratory** (found in the data afterwards; a
  hypothesis for future work, not evidence).
- Each claim links to its pre-registration, its analysis output and the raw episodes
  (`episodes.jsonl`; one JSON record per episode, with traces under `traces/`).
- Terms (success, harm, end-state vs. self-corrected harm, autonomous coverage, intervention
  precision and recall, …) are defined in [DEFINITIONS.md](DEFINITIONS.md).
- Commit hashes link to the registration commits on GitHub.

---

## 1. Summary

The prospectus hypothesized that reliable agents need **three controllers, each owning a
different kind of uncertainty**:

- a deterministic **runtime** for *execution* uncertainty ("what actually happened?")
- the **agent** for *semantic* uncertainty ("what should be done now?")
- **humans** for *authority* and *unresolved consequential ambiguity*

The evidence supports that allocation, and sharpens it in four ways.

1. **The runtime is necessary when the outcome of an action can't be observed, for every model
   tested.**
   - Under a hidden write (a timeout plus delayed visibility), models without a platform-honoured
     idempotency key were harmed in 70% (closed), 78% (frontier) and 86% (open-weight) of
     episodes. Under the semantic runtime, harm was **0% in every cell for every model**.
   - For single, *observable* faults, capable closed models recover on their own (0.5% harm), but
     open-weight models don't (8%). The runtime is *helpful* there, and necessary only for some
     model families.
2. **Model capability does not buy prevention.**
   - The frontier tier left *more* lasting damage than the strong tier: 64% vs 32% end-state harm.
     This refutes the pre-registered prediction that recovery improves with scale.
   - Among open-weight models, strong and weak tiers were statistically equivalent.
   - Exploratory traces show the most capable model, Fable 5.1, constructing fluent, confident and
     wrong accounts of what happened.
3. **The agent is necessary for semantic faults.** LLM agents succeeded on 97–100% of
   replanning, tool-switching and invalid-data faults; a deterministic workflow succeeded on 7%
   and caused harm on 21%.
4. **Execution-aware escalation (P6) is the best non-oracle policy, but it has a blind spot.**
   - It gives the most autonomy at the least harm, about **1/6 the human cost of universal
     approval** ($5.86 vs $38.22 per task) and almost no unnecessary escalations (1% vs 79%).
   - But it meets only 67% of genuine human needs, vs 93% for universal approval. It misses
     *unrecognized* ambiguity, where agents are confidently wrong, because it gates on
     self-reported confidence.

**Two further confirmatory findings concern a safety mechanism itself:**

- **Offering idempotency keys can *increase* harm** when a failure leaves a partial commit
  hidden behind a timeout (30% vs 1%).
- **That effect is driven by how the key is described:** an accurate description cut harm from
  30% to 3%.

---

## 2. The evidence base

| Study | Question | Pre-registration (commit) | Spec | Data | Analysis output | Episodes | Cost |
|---|---|---|---|---|---|---|---|
| Confirmation | H1, H5, keys hazard (closed models) | [compound-confirm](preregistration/compound-confirm.md) ([`eb0f8f2`](https://github.com/staciers/AgentBoundariesTestHarness/commit/eb0f8f2)) | [spec](../experiments/compound_confirm.json) | [episodes](../runs/compound-confirm-20261012-112744/episodes.jsonl) | [confirmatory.md](../runs/compound-confirm-20261012-112744/confirmatory.md) · [notes](../runs/compound-confirm-20261012-112744/NOTES.md) | 2,680 | $31.69 |
| Stage A | H2, RQ1, RQ2 (closed) | [stage-a](preregistration/stage-a.md) ([`eda3331`](https://github.com/staciers/AgentBoundariesTestHarness/commit/eda3331)) | [spec](../experiments/stage_a.json) | [episodes](../runs/stage-a-20261013-101143/episodes.jsonl) | [stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) · [notes](../runs/stage-a-20261013-101143/NOTES.md) | 4,690 | $38.24 |
| Stage C | Frontier tier: H1, H5, keys, H2 | [stage-c](preregistration/stage-c.md) ([`d5c4cb3`](https://github.com/staciers/AgentBoundariesTestHarness/commit/d5c4cb3)) | [spec](../experiments/stage_c.json) | [episodes](../runs/stage-c-20261013-112552/episodes.jsonl) | [stage_c.md](../runs/stage-c-20261013-112552/stage_c.md) · [notes](../runs/stage-c-20261013-112552/NOTES.md) | 1,300 | $80.12 |
| Open replication 1 | Confirmation design, open weights | [open-replications](preregistration/open-replications.md) ([`53d1fc8`](https://github.com/staciers/AgentBoundariesTestHarness/commit/53d1fc8)) | [spec](../experiments/open_confirm.json) | [episodes](../runs/open-confirm-20261014-081413/episodes.jsonl) | [replication_confirm.md](../runs/open-confirm-20261014-081413/replication_confirm.md) · [notes](../runs/open-confirm-20261014-081413/NOTES.md) | 2,680 | $11.70 |
| Open replication 2 | Stage A design, open weights | same ([`53d1fc8`](https://github.com/staciers/AgentBoundariesTestHarness/commit/53d1fc8)) | [spec](../experiments/open_stage_a.json) | [episodes](../runs/open-stage-a-20261014-081413/episodes.jsonl) | [replication_stage_a.md](../runs/open-stage-a-20261014-081413/replication_stage_a.md) · [notes](../runs/open-stage-a-20261014-081413/NOTES.md) | 4,690 | $15.20 |
| Stage B | Humans: H3, H4, H7, RQ3–RQ5 (8 models) | [stage-b](preregistration/stage-b.md) ([`a39b53c`](https://github.com/staciers/AgentBoundariesTestHarness/commit/a39b53c)) | [spec](../experiments/stage_b.json) | [episodes](../runs/stage-b-20261015-075812/episodes.jsonl) | [stage_b.md](../runs/stage-b-20261015-075812/stage_b.md) · [human_cost.md](../runs/stage-b-20261015-075812/human_cost.md) · [notes](../runs/stage-b-20261015-075812/NOTES.md) | 7,920 | $69.16 |
| Stage D | Runtime × policy factorial; P6 components (8 models) | [stage-d](preregistration/stage-d.md) ([`32cb181`](https://github.com/staciers/AgentBoundariesTestHarness/commit/32cb181)) | [spec](../experiments/stage_d.json) | [episodes](../runs/stage-d-20261018-111143/episodes.jsonl) | [stage_d.md](../runs/stage-d-20261018-111143/stage_d.md) · [notes](../runs/stage-d-20261018-111143/NOTES.md) | 10,800 | $86.25 |
| Contracts | Key scope × key description (Q4); 7 models after one was withdrawn | [contracts](preregistration/contracts.md) ([`45b0e78`](https://github.com/staciers/AgentBoundariesTestHarness/commit/45b0e78)) | [spec](../experiments/contracts.json) | [episodes](../runs/contracts-20261026-140610/episodes.jsonl) | [contracts.md](../runs/contracts-20261026-140610/contracts.md) · [notes](../runs/contracts-20261026-140610/NOTES.md) | 4,480 (3,920 analysed) | $37.40 |
| Repair | Contract-declared repair of partial commits (Q4 follow-up; 7 models) | [repair](preregistration/repair.md) ([`45f28a6`](https://github.com/staciers/AgentBoundariesTestHarness/commit/45f28a6)) | [spec](../experiments/repair.json) | [episodes](../runs/repair-20261027-101723/episodes.jsonl) | [repair.md](../runs/repair-20261027-101723/repair.md) · [notes](../runs/repair-20261027-101723/NOTES.md) | 2,730 | $23.95 |
| Stage E | Rule-based baselines, held-out `ledger` workloads, hybrid policy (Q2, Q5; 8 models) | [stage-e](preregistration/stage-e.md) ([`30078c0`](https://github.com/staciers/AgentBoundariesTestHarness/commit/30078c0)) | [spec](../experiments/stage_e.json) | [episodes](../runs/stage-e-20261027-135311/episodes.jsonl) | [stage_e.md](../runs/stage-e-20261027-135311/stage_e.md) · [notes](../runs/stage-e-20261027-135311/NOTES.md) | 5,250 (4,560 LLM) | $32.64 |
| Real services | Q1 and the keys hazard on Postgres with a streaming replica, side by side with the simulator (6 models) | [real-services](preregistration/real-services.md) ([`3bb3250`](https://github.com/staciers/AgentBoundariesTestHarness/commit/3bb3250)) | [spec](../experiments/real_ledger.json) | [episodes](../runs/real-ledger-20261028-111807/episodes.jsonl) | [real_services.md](../runs/real-ledger-20261028-111807/real_services.md) · [notes](../runs/real-ledger-20261028-111807/NOTES.md) | 2,520 | $15.09 |

**Supporting runs:**

- **Exploratory run** that generated the confirmation run's hypotheses:
  [compound-live](../runs/compound-live-20261011-123250/NOTES.md). 396 episodes, $3.98. The
  power analysis is in [significance.md](../runs/compound-live-20261011-123250/significance.md).
- **Pilots,** which checked scenarios and measured costs but weren't analysed:
  - [Stage A](../runs/stage-a-pilot-20261013-093242/episodes.jsonl): $2.22
  - [Stage C](../runs/stage-c-pilot-20261013-104810/episodes.jsonl): $3.99
  - [open weights](../runs/open-pilot-20261013-143116/episodes.jsonl): $0.79
  - [Stage B](../runs/stage-b-pilot-20261014-135034/episodes.jsonl) and its
    [re-check](../runs/stage-b-pilot-recheck-20261014-141145/episodes.jsonl): $5.54
- **Stage B sensitivity data:**
  [stage-b-sensitivity](../runs/stage-b-20261015-075812-sensitivity/stage_b.md). The one excluded
  episode was re-run with the fix; verdicts were identical.
- **Scripted harness checks** ($0; *not evidence*; local only, because the files are large and
  regenerate deterministically): `experiments/pilot_scripted.json`,
  `experiments/runtime_factorial.json`, `experiments/rate_sweep_scripted.json`.

**Models** (all at reasoning effort `high`):

| Family | Strong | Weak |
|---|---|---|
| Anthropic | `claude-opus-5-5` | `claude-haiku-5-5` |
| OpenAI | `gpt-6.1-sol` | `gpt-6-luna` |
| DeepSeek (open, via Together) | `DeepSeek-V4-Pro-0813` | `DeepSeek-V4-Flash-0731` |
| GLM (open, via Together) | `GLM-5.3` | `GLM-5.3-Flash` |
| **Frontier tier** | `claude-fable-5-1`, `gpt-6-astra` | — |

The closed pairs are matched by tier and generation, and the open ones by family. The
open-weight runs requested pinned model versions, and every response came from exactly the
requested model.

---

## 3. Methods in brief

- **Harness.** Agents act on deterministic, stateful services through tools. Every proposed call
  passes through a control plane: authority check → policy gate → reliability runtime → routing
  of unresolved outcomes. See [README](../README.md) and [ARCHITECTURE](ARCHITECTURE.md).
- **Scenarios.** 5 domains (travel, procurement, devops, scheduling, and a repo/CI/PR software
  platform) × 3 variants (`base`, `ambiguous`, `authority`) = 15 scenarios. Success and harm are
  judged from world-state invariants on ground truth, not by an LLM judge.
- **Faults.** 12 types: 9 execution faults (timeouts, 5xx, 429, garbled or partial responses,
  delayed visibility, duplicate execution, partial mutation) and 3 semantic ones (precondition
  changed, task-invalid result, persistent unavailability). They can be combined on one call
  ([compound faults](ARCHITECTURE.md#compound-faults)). The two compounds used most:
  - *hidden write*: timeout after execution + delayed visibility
  - *hidden partial commit*: partial mutation + timeout
- **Runtime modes.** `none`, `naive_retry`, and `semantic`: idempotency keys, reconciliation,
  postcondition verification, compensation, and failure classification.
- **Policies.**
  - P1: full autonomy
  - P2: universal approval
  - P3: confidence-based gating
  - P4: static risk-based gating
  - P5: agent-selected escalation
  - P6: semantic/runtime-aware delegation
  - ORACLE: escalates exactly when ground truth says a human is needed

  [Definitions](DEFINITIONS.md#control-policies).
- **Humans.**
  - *In-episode decisions:* a simulated principal and approver answering from ground truth, with a
    3% error rate and fatigue. Uncalibrated.
  - *Time and cost:* an [empirical human model](HUMAN_MODEL.md), applied after the run, over
    weighted organization profiles (coverage, after-hours arrival, runbooks, approval chains),
    with Monte Carlo intervals.
- **Statistics.**
  - Mantel–Haenszel tests stratified by model × scenario, Holm-corrected within each study's
    confirmatory family.
  - A result is "confirmed" only if it is significant **and** in the predicted direction.
  - Equivalence and non-inferiority use TOST against pre-stated margins.
- **Pre-registration discipline.**
  - Hypotheses, specs and analysis scripts were committed before each run.
  - Each analysis was run unchanged from a worktree at the registration commit.
  - Errored episodes were re-run from that commit; any still failing were excluded and counted,
    with a pre-specified sensitivity analysis.
  - Pilots preceded each new study, and scenario defects found in pilots were fixed before
    registration (§7).

---

## 4. Results by hypothesis

### H1: the runtime outperforms model recovery on execution failures

| Test | Models | Result | Verdict | Data |
|---|---|---|---|---|
| C1: hidden write, no keys vs P6 runtime (harm) | closed ×4 | **70%** (336/480) vs **0%** (0/160) | confirmed | [confirmatory.md](../runs/compound-confirm-20261012-112744/confirmatory.md) |
| G1: same, frontier | Fable, Astra | **78%** (188/240) vs **0%** (0/80) | confirmed | [stage_c.md](../runs/stage-c-20261013-112552/stage_c.md) |
| OC1: same, open weights | open ×4 | **86%** (415/480) vs **0%** (0/160) | replicated | [replication_confirm.md](../runs/open-confirm-20261014-081413/replication_confirm.md) |
| A3: *single* execution faults, no runtime vs semantic runtime (harm) | closed ×4 | 0.5% (4/880) vs 0% (0/880) | **not confirmed** (p = 0.10) | [stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) |
| OA3: same, open weights | open ×4 | **8%** (74/880) vs 0% (0/880) | replicated | [replication_stage_a.md](../runs/open-stage-a-20261014-081413/replication_stage_a.md) |
| E1 (Stage A): runtime suffices; LLM vs workflow success, execution faults | closed ×4 | 880/880 vs 440/440 | equivalent | [stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) |

**Reading.** H1 holds strongly where the *outcome* of an action is unobservable by checking
state. When a failure is observable, capable closed models recover by themselves; open-weight
models still don't. So the claim for the paper is narrower than the original H1 and stronger
where it applies: **the runtime is necessary for unobservable execution outcomes, and helpful
(but model-dependent) for observable ones.**

### H2: agent reasoning outperforms deterministic recovery on semantic failures

| Test | Models | Result | Verdict | Data |
|---|---|---|---|---|
| A1: LLM vs workflow success, semantic faults | closed ×4 | **97%** (545/560) vs **7%** (10/140) | confirmed | [stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) |
| A2: workflow vs LLM harm, semantic faults | closed ×4 | **21%** (30/140) vs **0%** (0/560) | confirmed | same |
| G5: frontier vs workflow success | Fable, Astra | **100%** (280/280) vs 7% | confirmed | [stage_c.md](../runs/stage-c-20261013-112552/stage_c.md) |
| OA1 / OA2: open weights | open ×4 | 98% vs 7% success; 21% vs 0% harm | replicated | [replication_stage_a.md](../runs/open-stage-a-20261014-081413/replication_stage_a.md) |
| E2: the runtime doesn't change semantic recovery (±10 pts) | closed ×4 | 97% vs 91% | equivalent (but also significantly different: the runtime adds a few points) | [stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) |

**Reading.** Confirmed across all 10 models. The semantic faults are near the ceiling for every
LLM (94–100%), so they show *that* agents beat workflows but don't separate model tiers.

### H3: humans add most value for authority and consequential ambiguity

| Test | Result | Verdict | Data |
|---|---|---|---|
| B1: P6 vs P1 success where a human is needed | **65%** (310/480) vs **18%** (88/480) | confirmed | [stage_b.md](../runs/stage-b-20261015-075812/stage_b.md) |
| B5: confidence-only gating (P3) vs P6, harm | **39%** (280/720) vs **4%** (31/720) | confirmed | same |
| E1 (Stage B): P6 vs P1 on `base` tasks (no value where none is needed) | 100% vs 91% | **different**: P6 is better, through its runtime (hidden-write cells) | same |

**Reading.** Escalation adds large value exactly where judgment or authority is needed.
Confidence-only gating misses authority entirely, because agents are confident about actions
they aren't permitted to take.

### H4: the hybrid policy dominates on autonomy vs. risk

| Test | Result | Verdict | Data |
|---|---|---|---|
| B4: P6 vs P4 autonomous success | **34%** (243/720) vs **13%** (91/720) | confirmed | [stage_b.md](../runs/stage-b-20261015-075812/stage_b.md) |
| N2: P6 harm no more than P4 (+5 pts) | **4%** vs **16%** | non-inferior (better) | same |

Where each policy's episodes end, across all 8 models (secondary;
[stage_b.md](../runs/stage-b-20261015-075812/stage_b.md); decomposition from
[`episodes.jsonl`](../runs/stage-b-20261015-075812/episodes.jsonl) with `abh report`). The
first four columns are shares of **all** episodes and add up to the
[autonomy rate](DEFINITIONS.md#autonomy_rate). The last two are conditional on the episode being
autonomous ([denominators](DEFINITIONS.md#note-autonomy_denominators)).

| Policy | [Autonomous success](DEFINITIONS.md#autonomous_coverage) | [Autonomous, failed safely](DEFINITIONS.md#autonomous_failure_no_harm) | [Autonomous, harmful](DEFINITIONS.md#autonomous_harmful) | Escalated | [Failure rate when autonomous](DEFINITIONS.md#autonomous_failure_rate) | [Harm rate when autonomous](DEFINITIONS.md#autonomous_harm_rate) | Success | Harm |
|---|---|---|---|---|---|---|---|---|
| ORACLE | 34% | 3% | 0% | 63% | 9% | 0% | 94% | 0% |
| **P6** (0.7) | **34%** | 17% | **4%** | 45% | 39% | **8%** | **76%** | **4%** |
| P5 | 30% | 13% | 8% | 49% | 41% | 15% | 71% | 13% |
| P4 | 13% | 17% | 7% | 64% | 65% | 20% | 64% | 16% |
| P3 (0.7) | 31% | 17% | 33% | 18% | 62% | 41% | 44% | 39% |
| P2 | 0% | 2% | 0% | 98% | 100% | 0% | 82% | 9% |
| P1 | 31% | 43% | 13% | 13% | 65% | 15% | 42% | 15% |

**How the columns relate.** Earlier versions of this table reported "autonomous risk",
P(not success | autonomous). That counts every unsuccessful autonomous episode, harmful or not,
so it is a failure rate, not a harm measure (the field is now named
[`autonomous_failure_rate`](DEFINITIONS.md#autonomous_failure_rate)).
- **ORACLE's 9%:** 23 of its 265 autonomous episodes were `authority` tasks where the agent
  stopped short without acting. None caused harm.
- **P6's 39%:** 155 of 398 autonomous episodes failed, and 31 of those (8% of autonomous
  episodes, 4% of all) caused harm. Most were wrong but harmless guesses on `ambiguous` tasks.

P6 matches the oracle's autonomous coverage, at the lowest harm of any non-oracle policy. Its
thresholds (0.5 / 0.7 / 0.9) barely matter, because models rarely report confidence below 0.9.

**Stage D: delegation separated from the runtime.** In Stage B, P1–P5 ran with no runtime while
P6 and ORACLE ran with the semantic one, so B1, B4, B5 and E1 measured both together. Stage D
([pre-registration](preregistration/stage-d.md),
[analysis](../runs/stage-d-20261018-111143/stage_d.md),
[notes](../runs/stage-d-20261018-111143/NOTES.md)) ran every policy at both runtime levels.

| Test | Result | Verdict |
|---|---|---|
| D1: P6 vs P1 success where a human is needed, semantic runtime | **65%** vs **19%** | confirmed |
| D2: the same, no runtime | **65%** vs **16%** | confirmed |
| D3: P1 vs P6 harm, semantic runtime | 9% vs **4%** | confirmed |
| D4: P3 vs P6 harm, semantic runtime (B5 deconfounded) | 34% vs **4%** | confirmed |
| D5: P6 vs P4 autonomous success, semantic runtime (B4 deconfounded) | **34%** vs 13% | confirmed |
| D6: P6 harm under hidden write, no runtime vs semantic | 4% vs 3% | not confirmed |
| K1: P6 without vs with the authority gate, harm on `authority` tasks | 90% vs **0%** | confirmed |
| K3: P6 routing unresolved outcomes to the agent vs a human, harm, no runtime | 21% vs **4%** | confirmed |
| K2: P6 without vs with the confidence gate, success (±5 points) | 76% vs 77% | equivalent |

**Reading.**
- **The pre-registered decision rule is met** (D1–D3): P6's delegation effect is not an
  artefact of its runtime.
- **Its active parts are the deterministic authority gate and the routing of unresolved
  execution outcomes.** The confidence gate is inert.
- **Routing and the runtime are substitutes for safety, but not for autonomy** (D6, and the
  interaction terms):
  - Without a runtime, P6 stays safe by asking a human about unknown outcomes.
  - That nearly doubles interventions (0.84 vs 0.45 per task), and cuts autonomous success from
    34% to 20%.
- *Exploratory:* with the same runtime, agent-selected escalation (P5) nearly matches P6 (79% /
  6% vs 77% / 4% success / harm).
  - P6 is better on authority (0% vs 9% harm); P5 is better on ambiguity (52% vs 42% success).
  - A P5 + P6 hybrid is the obvious next candidate, and the strongest baseline for the paper.

### H5: scaling improves semantic recovery but not execution ambiguity

| Test | Result | Verdict | Data |
|---|---|---|---|
| C2: weak vs strong end-state harm (closed) | 75% vs **32%** | confirmed | [confirmatory.md](../runs/compound-confirm-20261012-112744/confirmatory.md) |
| E1 (confirmation): strong vs weak *any* harm (±10 pts) | 64% vs 76% | **different, not equivalent:** strong models cause somewhat less harm | same |
| G2: the frontier still harmed above 10% | **78%** (188/240) | confirmed | [stage_c.md](../runs/stage-c-20261013-112552/stage_c.md) |
| G3: recovery improves with scale (strong > frontier end-state harm) | strong **32%** vs frontier **64%** | **refuted:** significant in the *opposite* direction | same |
| OC2: weak vs strong end-state harm (open) | 77% vs 82% | not replicated | [replication_confirm.md](../runs/open-confirm-20261014-081413/replication_confirm.md) |
| OE1: strong vs weak any harm (open, ±10 pts) | 85% vs 88% | equivalent | same |

**Reading.** Scale does not remove execution ambiguity (G2). Across the closed models, the
strong tier recovers better than the weak tier (C2), but that does **not** extend to the
frontier (G3), nor to open-weight tiers (OC2, OE1). The defensible revision of H5:
**recovery is a behavioural trait that doesn't track capability; prevention requires the
runtime.**

### H6: handling failures below the model saves tokens, calls and latency

*Cost model (exploratory, 2026-10-28;* [cost_model.md](cost/cost_model.md)*):* on the real
ledger, the runtime adds one read per payment with no fault (one RTT). Under a fault it adds
6–12 requests and 7.5–10 s of polling. With LLM agents it cut model calls 7.5 → 3.6 under a
hidden write (tokens −51%, similar wall time) and 5.9 → 3.6 under a partial commit (tokens −28%,
6 s slower, almost all polling). The partial-effects fast path (`inspect_partial`, added
afterwards) removes that polling: a scripted partial commit recovers in 3.2 s instead of 13.3 s,
with no harm.

On single execution faults, the semantic runtime **cut model calls by about 20%** for every
model (closed: 5.0–5.5 → 4.05–4.41 calls per episode; open: 5.0–5.25 → 4.0–4.26), and
reduced failures exposed to the agent from about 0.8 per episode to 0–0.13. Sources:
[stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) and
[replication_stage_a.md](../runs/open-stage-a-20261014-081413/replication_stage_a.md),
secondary tables. In the exploratory compound run, P6 used about 40% fewer calls than P1, with
p < 10⁻⁷ for every model ([significance.md](../runs/compound-live-20261011-123250/significance.md)).

### H7: execution-aware escalation saves human attention without losing recall

| Test | Result | Verdict | Data |
|---|---|---|---|
| B2: episodes with an unnecessary escalation, P2 vs P6 | **79%** (567/720) vs **1%** (4/720) | confirmed | [stage_b.md](../runs/stage-b-20261015-075812/stage_b.md) |
| N1: P6 meets as many human needs as P2 (−10 pts) | **67%** vs **93%** | **not shown** | same |
| B6: P6 meets needs that agent-selected escalation (P5) misses | 67% vs 72% | **not confirmed** (opposite direction) | same |

**Human time and cost** (pre-registered secondary; the
[empirical model](HUMAN_MODEL.md#how-the-outputs-are-computed), weighted organization mix,
median across Monte Carlo draws with 5–95% intervals;
[human_cost.md](../runs/stage-b-20261015-075812/human_cost.md)):

| Policy | Escalations / task | [Wait](DEFINITIONS.md#human_time_to_decision) / task (median) | Tasks waiting > 1 h | [Human cost](DEFINITIONS.md#human_effort_cost_per_task) / task |
|---|---|---|---|---|
| P2 | 2.68 | 3.9 h | 82% | **$38.22** ($13.01–65.07) |
| P4 | 1.01 | 51 min | 48% | $13.85 ($4.87–23.05) |
| ORACLE | 0.67 | 26 min | 37% | $8.09 ($2.96–14.64) |
| P5 | 0.49 | 0 | 26% | $6.16 ($2.53–9.48) |
| **P6** (0.7) | 0.45 | **0** | **24%** | **$5.86** ($2.07–9.23) |

The per-profile breakdown shows the after-hours effect. For P2, the p90 wait is 29 h at a
startup with single-region coverage vs. 10 h at a global enterprise with follow-the-sun
operations.

**Reading.** P6 saves most of the human attention and cost. But it **does not keep recall**:
it misses *unrecognized* ambiguity, where agents are confidently wrong (the scheduling and
platform `ambiguous` variants), because it gates on self-reported confidence. That is the
paper's clearest pointer to future work: delegation signals better than self-report
(learned deferral, a KnowNo-style baseline).

### RQ1: failure ownership

Fault-by-fault ownership tables (runtime-, agent- or human-resolved, with outcomes) for all 12
fault types are in [stage_a.md](../runs/stage-a-20261013-101143/stage_a.md) and
[replication_stage_a.md](../runs/open-stage-a-20261014-081413/replication_stage_a.md).
Ownership is assigned heuristically ([definition](DEFINITIONS.md#note-ownership_heuristic)).

### The keys hazard (a new result)

| Test | Models | Result | Verdict | Data |
|---|---|---|---|---|
| C3: keys vs no keys, hidden partial commit (harm) | closed | **30%** (108/360) vs **1%** (2/360) | confirmed | [confirmatory.md](../runs/compound-confirm-20261012-112744/confirmatory.md) |
| C4: OpenAI vs Anthropic, with keys | closed | 47% vs 13% | confirmed | same |
| C5: "at most once" vs caveated wording | closed | **30%** vs **3%** | confirmed | same |
| G4: keys hazard at the frontier | Fable, Astra | 9% vs 0% | confirmed | [stage_c.md](../runs/stage-c-20261013-112552/stage_c.md) |
| OC3: keys hazard, open weights | open | 12% vs 8% | not replicated | [replication_confirm.md](../runs/open-confirm-20261014-081413/replication_confirm.md) |
| OC5: wording, open weights | open | **12%** vs **4%** | replicated | same |

**Reading.** When a partial commit is hidden behind a timeout, the service never records the
key, so a "safe" keyed retry duplicates the committed part. The promise in the key's
description ("executed at most once") drives much of the effect, and an accurate description
largely removes it. This is a direct design lesson for tool and MCP schema authors. Neutral
wording falls in between (exploratory: 14%).

**The contract study bounds this** ([pre-registration](preregistration/contracts.md),
[analysis](../runs/contracts-20261026-140610/contracts.md),
[notes](../runs/contracts-20261026-140610/NOTES.md)). It crossed what the key covers (`completed`,
as above, vs `atomic`: recorded with any committed part, so a retry returns the original
outcome) with how the key is described ("at most once" vs generated from the
[execution contract](ARCHITECTURE.md#execution-contracts)). Harm with 7 models (one was withdrawn
by the provider):

| Arm | Harm | Closed | Open | Verdict |
|---|---|---|---|---|
| A: completed scope, "at most once" | 18% | 26% | 9% | — |
| B: completed scope, contract wording | **5%** | **1%** | 10% | K2 (A > B) confirmed |
| C: atomic scope, "at most once" | 7% | 5% | 10% | K1 (A > C) confirmed |
| D: atomic scope, contract wording | 19% | 8% | **33%** | exploratory: backfired |
| N: no keys | 4% | 1% | 8% | K3 (A > N) confirmed |

- **What it shows:**
  - The hazard is a scope mismatch.
  - For closed models, either an atomic scope or an accurate description removes duplication
    entirely (91 → 0 episodes).
  - The atomic scope still left more harm than no keys (N1 not shown). That residual is partial
    work left in place, not duplication.
- **The wording result needs care.** The generated atomic-scope wording said retries are safe.
  Agents checked less, and many (mostly open models) then re-sent the whole request with a new
  key after the replayed partial failure.
- **The P6 runtime had 0% harm under every contract.**

**The repair study then tested contract-declared repair** under the atomic scope
([pre-registration](preregistration/repair.md),
[analysis](../runs/repair-20261027-101723/repair.md),
[notes](../runs/repair-20261027-101723/NOTES.md); travel and commerce, 7 models). D2 adds two things
to the contract:
- a structured partial report, listing what committed
- a `cancel_partial(tool, key)` operation that undoes exactly what that key committed, after which
  the full request can go again with the same key

| Arm | Harm | Closed | Open | Re-sent with a new key after a replay |
|---|---|---|---|---|
| D: no repair guidance | 14% | 11% | 18% | 75 |
| D1: repair-aware wording | 2% | 0% | 6% | 11 |
| D2: partial report + `cancel_partial` | **1%** | **0%** | **3%** | **0** |
| N: no keys | 0.5% | 1% | 0% | — |

- **R1** (D > D2) and **R2** (D > D1) confirmed; **R3** (D1 > D2) not confirmed.
- **N4: D2 is non-inferior to no keys.** With contract-declared repair primitives, agent-side
  recovery from a hidden partial commit is as safe as not using keys.
- *Exploratory:* every remaining D2 harm episode began with an unkeyed first write (GLM models),
  so there was nothing to cancel.

**So the allocation is:**
- The **contract** defines the execution semantics and the repair operations.
- The **runtime** guarantees keys are attached and recovers on its own (0% harm under every
  contract tested).
- An **agent** that recovers itself is safe through the contract's primitives, provided it keys
  its writes.
### Stage E: stronger baselines, held-out workloads and the hybrid policy

Confirmatory ([pre-registration](preregistration/stage-e.md),
[analysis](../runs/stage-e-20261027-135311/stage_e.md),
[notes](../runs/stage-e-20261027-135311/NOTES.md); 8 models). The held-out `ledger`
(accounts-payable) domain was written after the system was frozen, and its instances are
parameterized by seed.

| ID | Claim | Result | Verdict |
|---|---|---|---|
| E1 | Held-out, hidden write: the runtime prevents what agents can't | harm, no keys 53% vs P6 0% | **confirmed** |
| E2 | Held-out, semantic faults: agents beat a workflow | success 100% vs 0% | **confirmed** |
| E3a | Development: agents beat a domain-independent rule library | 98% vs 79% | **confirmed** |
| E3b | Held-out: agents beat rules derived from the task spec | 100% vs 67% | **confirmed** |
| E4 | Held-out: the authority gate prevents harm | harm, P1 12% vs P6 0% | **confirmed** |
| E5 | Hybrid (P6 + `ask_human`) handles ambiguity better than P6 | 78% vs 72% | **confirmed** |
| E6 | Hybrid is safer on authority than P5 + runtime | harm 0% vs 5% | **confirmed** |
| N1 | Agents are within 5 points of hand-tuned rules | 98% vs 100% | **non-inferior** |
| N2 | Hybrid is no less safe than P6 | harm 3% vs 5% | **non-inferior** |

- **The OSDI decision rule (condition 2) is met.**
- **Read per fault:** rules matched agents on changed preconditions and unavailable tools; the
  agents' advantage is on task-invalid results the rules don't anticipate (generic rules 40% on
  development, 0% held-out; agents 98–100%). Hand-tuned rules remain the ceiling on development
  domains, at the cost of 3–6 hand-written recovery rules per task.
- **Held-out semantic faults were at the ceiling** for every model, so they show agents don't
  degrade on an unseen domain rather than measuring its difficulty.
- The hybrid's remaining harm (15 episodes) is all unrecognized ambiguity.

### Real services: the ledger on Postgres

Confirmatory ([pre-registration](preregistration/real-services.md),
[analysis](../runs/real-ledger-20261028-111807/real_services.md),
[notes](../runs/real-ledger-20261028-111807/NOTES.md); 6 models; [system](REAL_SERVICES.md)).
The ledger ran on Postgres:
- real transactions, and a real two-transaction partial commit
- idempotency keys as database rows
- reads through streaming replicas, so lag is real replication lag
- client-side timeouts and wall-clock time

It ran side by side with the simulated ledger, on the same models, seeds and arms.

| ID | Claim (real services) | Result | Verdict |
|---|---|---|---|
| T1 | The runtime prevents hidden-write harm | harm 69% without keys vs 0% | **confirmed** |
| T2 | The runtime prevents partial-commit harm | 27% with keys vs 0% | **confirmed** |
| T3 | The keys hazard appears | 27% with keys vs 19% without | **confirmed** |
| N1 | The runtime is as safe as in the simulator | 0/360 vs 0/360 | **non-inferior** |

- **Decision rule met:** Q1 holds on real services.
- **The simulator matched real services in four of five agent-only arms** (TOST, ±10 points),
  including both partial-commit arms (27% vs 27%, 19% vs 18%).
- **It underestimated hidden-write harm without keys** (46% vs 69%). *Exploratory:* the
  simulated payment's 1.8 s latency is charged before the call executes. That shortens the
  window in which a retry can duplicate the hidden write from 6 s to about 4.2 s. Every retry
  4.2–6 s after the timeout was harmless in the simulator (0/39) and harmful on real services
  (36/36). Opus went from 0% to 50%, and GPT-6-Luna from 13% to 67%, with no change in what
  they did.
- **So agent-side recovery is a timing race, and per-model rates near the boundary depend on
  service latency.** The runtime's guarantee doesn't.
- *Exploratory sensitivity curve* ([latency_sensitivity.md](latency/latency_sensitivity.md)):
  real-stack retry timing predicts every real outcome (180/180). Evaluated at the simulator's
  4.2 s window, it predicts 49% harm against the simulator's observed 46%. Across windows of
  1–8 s, pooled harm without a runtime rises from 8% to at least 80%, while the runtime stays
  at 0%.

---

## 5. Exploratory findings

*Not pre-registered. These are hypotheses for future confirmatory work.*

0. **Every main effect except one varies strongly by model**
   ([heterogeneity.md](heterogeneity/heterogeneity.md), [forest plot](heterogeneity/forest.png),
   `analysis/heterogeneity.py`). The confirmatory tests pooled models. Per model, on the
   risk-difference scale:
   - **Uniform in direction, varying in size** (every model's interval above 0):
     - the runtime on development domains (Q1): +54 to +99 points, 10/10 models
     - agents vs the workflow (Q2): +86 to +93
     - agents vs generic rules (E3a): +15 to +21
     - P6 vs P1 on human-needed variants (D1): +27 to +55. This is the only effect with low
       heterogeneity (I² = 17%).
   - **Concentrated in some models**, with the others at or near 0 in both arms:
     - the runtime on the held-out ledger (E1): GLM-5.3 and GLM-5.3-Flash +100, DeepSeek
       V4.1-Flash +97, DeepSeek V4-Pro +67, Haiku +60, but Opus, GPT-6.1-Sol and GPT-6-Luna
       0 to +3
     - the authority gate on the ledger (E4): GLM-5.3-Flash +90, GLM-5.3 +10, six models 0
     - repair primitives (R1): Haiku +46, the GLMs +20 and +22, four models 0 to +3
     - the keys hazard (C3, G4, OC3): GPT-6-Luna +56, Fable +2, GLM-5.3-Flash −1
   - **One reversal:** contract-generated wording (K2) *raised* harm for DeepSeek V4-Pro, from
     10% to 23% (−13 points, interval −24 to −2). Every other model was neutral or helped.
   - **Which models need a mechanism doesn't follow family or tier, and isn't stable across
     domains.** GPT-6-Luna was harmed in 75% of development hidden-write episodes but 3% on the
     ledger. Haiku needed repair primitives; Opus didn't.
     Part of this is timing, not the model: on real services (Postgres), GPT-6-Luna's ledger
     harm was 67% and Opus's 50%, because the simulator's service latency had given them extra
     time ([real-services notes](../runs/real-ledger-20261028-111807/NOTES.md)).
   - **The mechanisms never made a model worse,** apart from that one wording reversal. So the
     defensible claim is "never worse, and decisive for the models that need it", not a uniform
     effect size.

1. **Key discipline varies by model family.**
   [open-confirm notes](../runs/open-confirm-20261014-081413/NOTES.md).
   - The closed models attached an idempotency key to the *first* attempt 100% of the time, and
     reused it on the retry, so they were never harmed with keys.
   - The open models often added a key only on the retry, which protects nothing. DeepSeek V4
     Pro never keyed a first attempt, and was harmed in 85% of hidden-write episodes *with keys
     offered*.
   - This likely explains OC3's non-replication.
2. **The frontier model's confident misreading.**
   [Stage C notes](../runs/stage-c-20261013-112552/NOTES.md).
   - Fable 5.1 always retried after an empty check, and verified afterwards in only 28% of
     episodes.
   - When it did verify, the duplicate was visible in 34 of 34 cases, but it repaired only 4.
   - Its final messages repeatedly asserted that a single charge, order or meeting existed,
     including reinterpreting a conflict caused by its own first booking as someone else's.
3. **Verifying after the retry predicts repair.** Across models, end-state harm tracks
   post-retry verification: Opus verified 88% (25% lasting harm); Luna 0% (100%).
   [Stage C notes](../runs/stage-c-20261013-112552/NOTES.md).
4. **Two mechanisms behind the keys hazard** (pre-registered as secondary M1/M2,
   [confirmatory.md](../runs/compound-confirm-20261012-112744/confirmatory.md)).
   - *Over-trust:* Luna checked state before retrying only 48% of the time with keys, vs 100%
     without.
   - *Repair order:* Sol checked state every time, but created replacements before undoing
     partial commits (32/90 self-corrected harm).
5. **Naive infrastructure retry adds harm.**
   - Closed: 40/880 vs 4/880 ([Stage A notes](../runs/stage-a-20261013-101143/NOTES.md)).
   - Open: 162/880 vs 74/880 ([open-stage-a notes](../runs/open-stage-a-20261014-081413/NOTES.md)).
6. **Recognized vs. unrecognized ambiguity.**
   [Stage B pilot findings](preregistration/stage-b.md#pilot-findings).
   - Capable agents *stop and ask* when they notice ambiguity (travel, procurement, devops).
   - When ambiguity isn't visible (scheduling, platform), every model is confidently wrong.
   - Escalation policies differ sharply between the two cases.

---

## 6. Synthesis: who should own what

| Kind of uncertainty | Owner | Strength of evidence |
|---|---|---|
| **Unobservable execution outcome** (hidden write, hidden partial commit) | **Runtime: necessary for safe autonomy.** 0% harm under P6 vs 54–99% per model without keys, for all 10 models. Without a runtime, routing the unknown outcome to a human is also safe, but costs human attention and autonomy | Confirmatory: C1, G1, OC1; D6 and K3 |
| **Observable execution fault** | **Runtime: helpful**; necessary for some model families | Confirmatory: A3 (closed: no), OA3 (open: yes), H6 |
| **Semantic** (replan, switch tools, detect bad data) | **Agent: necessary** | Confirmatory: A1, A2, G5, OA1, OA2 |
| **Authority** | **Human,** routed deterministically by policy, not by agent confidence | Confirmatory: B1, B5, D4, K1 |
| **Recognized ambiguity** | **Human,** via the agent asking | Confirmatory: B1; pilot evidence |
| **Unrecognized ambiguity** | **Human,** but current confidence-based routing misses it | Confirmatory: N1 (not met), B6 |
| **Execution-safety mechanisms** (idempotency keys) | **Runtime, not agent.** Agents misuse them (keys hazard; key discipline); contracts that declare the key's scope, a partial report and a repair operation make agent recovery safe (R1, N4), provided the agent keys its writes | Confirmatory: C3, C5, G4, K1–K3, R1–R2, N4; exploratory: key discipline, contract wording |

---

## 7. Threats to validity and deviations

- **Simulated humans.**
  - *Decision quality* (3% error, fatigue) is uncalibrated against people.
  - *Time and cost* use an [empirical model](HUMAN_MODEL.md) with sourced ranges where public
    data exists and labelled assumptions elsewhere.
  - A small interactive pilot is needed before claims about human decision accuracy.
- **Breadth.** 5 domains and 15 scenarios. Results generalize to these tasks; per-scenario
  heterogeneity is reported in the per-model tables.
- **Scenario fixes from pilots,** all made before registration and recorded:
  - travel: the city name "New York" wasn't recognized
  - scheduling: attendee email addresses weren't recognized
    ([compound-live notes](../runs/compound-live-20261011-123250/NOTES.md))
  - devops: the release-candidate corruption wasn't detectable
    ([Stage A pilot findings](preregistration/stage-a.md#pilot-findings))
  - no channel for agents to ask their principal, and `platform/ambiguous` was not genuinely
    ambiguous ([Stage B pilot findings](preregistration/stage-b.md#pilot-findings))
- **Harness defects found during runs.** Malformed tool arguments crashed three code paths. Each
  was fixed in a behaviour-preserving way (all 2,680 confirmation-run episodes replay
  identically), logged before outcomes were seen, and handled under the exclusion rule.
  **Across six studies, one episode was excluded** (Stage B), and its sensitivity analysis left
  every verdict unchanged. Deviation logs:
  - [Stage A](preregistration/stage-a.md#deviations)
  - [Stage C](preregistration/stage-c.md#deviations)
  - [open replications](preregistration/open-replications.md#deviations)
  - [Stage B](preregistration/stage-b.md#deviations)
- **Operational issues.**
  - A provider capacity outage (45 episodes) and runaway outputs (6) were re-run under the rule
    ([open-stage-a notes](../runs/open-stage-a-20261014-081413/NOTES.md)).
  - System sleep stalled Stage B, which was resumed under `caffeinate` with no design change
    ([Stage B notes](../runs/stage-b-20261015-075812/NOTES.md)).
- **Policy and runtime confounded in Stage B.** Each policy ran with its default runtime (P1–P5
  none, P6 and ORACLE semantic). Stage D resolved this: the delegation effects hold with the
  runtime held fixed ([stage_d.md](../runs/stage-d-20261018-111143/stage_d.md)).
- **Cross-run comparisons.** G3 compares the frontier against the confirmation run's
  strong-tier data. A concurrent drift anchor found no change in those models (every anchor
  comparison p ≥ 0.41; [stage_c.md](../runs/stage-c-20261013-112552/stage_c.md)).
  Comparisons between open and closed models are exploratory throughout.
- **Seeds and sampling.** Seeds fix the environment, faults and simulated human, but not LLM
  sampling. Replication across seeds therefore samples model behaviour.
- **Hosting.** Open models were served by one provider (Together), at pinned versions; every
  response's served model ID was verified.
- **Scripted runs** validate the harness and are not evidence
  ([note](DEFINITIONS.md#note-scripted_not_evidence)).
- **Ceiling effects.** The semantic faults are near the ceiling for every LLM, so they can't
  separate model tiers.

---

## 8. Reproducing the analyses

Each analysis can be re-run exactly as registered, without API calls, from the committed data.
For example, for Stage B:

```bash
git worktree add --detach /tmp/prereg a39b53c
cd /tmp/prereg && PYTHONPATH=$PWD /path/to/repo/.venv/bin/python analysis/stage_b.py /path/to/repo/runs/stage-b-20261015-075812/
```

| Study | Registration commit | Command |
|---|---|---|
| Confirmation | `eb0f8f2` | `analysis/confirmatory.py runs/compound-confirm-20261012-112744/` |
| Stage A | `eda3331` | `analysis/stage_a.py runs/stage-a-20261013-101143/` |
| Stage C | `d5c4cb3` | `analysis/stage_c.py runs/stage-c-20261013-112552/ runs/compound-confirm-20261012-112744/` |
| Open replications | `53d1fc8` | `analysis/replication.py confirm runs/open-confirm-20261014-081413/` · `... stage-a runs/open-stage-a-20261014-081413/` |
| Stage B | `a39b53c` | `analysis/stage_b.py runs/stage-b-20261015-075812/` and `python -m abh human-cost runs/stage-b-20261015-075812/` |
| Stage D | `32cb181` | `analysis/stage_d.py runs/stage-d-20261018-111143/` |
| Contracts | `45b0e78` | `analysis/contracts.py runs/contracts-20261026-140610/` |
| Repair | `45f28a6` | `analysis/repair.py runs/repair-20261027-101723/` |
| Stage E | `30078c0` | `analysis/stage_e.py runs/stage-e-20261027-135311/` |
| Real services | `3bb3250` | `analysis/real_services.py runs/real-ledger-20261028-111807/` |

Episodes with saved traces can also be re-scored under a changed evaluator, with no model calls:
`python -m abh rescore runs/<dir>` ([how it works](ARCHITECTURE.md#re-scoring-old-runs)).
Every analysed episode of the ten studies (47,219) replays exactly, including those where the
agent asked the principal a question.
