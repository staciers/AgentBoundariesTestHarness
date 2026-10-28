# Pre-registration: real-services replication (Tier A: the ledger on Postgres)

**Status:** draft. It becomes registered when committed, **after the pilot and before the
main run**. Defects the pilot reveals may be fixed before then (record them under *Pilot
findings*). After the commit, change nothing listed here.

| | |
|---|---|
| Spec | [`experiments/real_ledger.json`](../../experiments/real_ledger.json): 2,520 LLM episodes |
| Pilot specs | [`experiments/real_ledger_pilot.json`](../../experiments/real_ledger_pilot.json) (36 episodes, seeds 900–902) and, after the design fix, [`experiments/real_ledger_pilot_recheck.json`](../../experiments/real_ledger_pilot_recheck.json) (42 episodes, seeds 903–905); real ledger only, Haiku and GLM-5.3-Flash; not analysed |
| Analysis | [`analysis/real_services.py`](../../analysis/real_services.py), run unchanged |
| System | [`docs/REAL_SERVICES.md`](../REAL_SERVICES.md); [`services/ledger/`](../../services/ledger/); [`abh/domains/ledger_real.py`](../../abh/domains/ledger_real.py) |
| Origin of hypotheses | the reviewer objection "services are simulated" in the [paper outline](../PAPER_OUTLINE.md#likely-reviewer-objections); C1, G1, OC1 and E1 (the runtime result), C3 (the keys hazard) |

## Question

Every result so far comes from simulated services. Does the paper's central execution result
(Q1) hold when the ledger runs on real infrastructure? Here, *real* means Postgres
transactions, a real two-transaction partial commit, idempotency keys as database rows, a
streaming read replica with real replication lag, client-side timeouts and wall-clock time.

Three parts:
1. Does the runtime still prevent the harm that agents cause on their own?
2. Does the keys hazard still appear?
3. Does the simulator predict real-service behaviour closely enough to stand in for it?

## Design

**Substrates:** `ledger_real/base` (the real stack) and `ledger/base` (the simulator). They are
run **side by side in the same run**, on the same models, seeds and arms, so the comparison
isn't confounded by model drift between runs. Both use the same parameterized instances (the
seed picks vendor, invoices and amounts).

**Models (6, all at effort `high`).** They span the per-model range seen on the simulated
ledger in Stage E (hidden-write harm without keys, 0–100%):
- closed: `claude-opus-5-5` (0%), `claude-haiku-5-5` (60%), `gpt-6.1-sol` (0%), `gpt-6-luna` (3%)
- open (Together): `GLM-5.3-Flash` (100%), `DeepSeek-V4.1-Flash-1017` (97%)

**Seeds:** 600–629 (fresh), so 30 per model per arm per substrate.

| Arm | Fault | Policy |
|---|---|---|
| no fault | none | P1 (keys offered) |
| visibility lag only | delayed visibility, 9 s (a successful payment stays hidden) | P1 |
| hidden write, no keys | timeout after execution (+ visibility lag) | `P1[expose_keys=false]` |
| hidden write, runtime | same | P6 (threshold 0.7) |
| partial commit, keys | partial mutation + timeout after execution | P1 |
| partial commit, no keys | same | `P1[expose_keys=false]` |
| partial commit, runtime | same | P6 |

7 arms × 2 substrates × 6 models × 30 seeds = **2,520 episodes**.

**The real stack:**
- **Software:** Postgres 16.15 (`postgres:16`, digest recorded in each run's `stack.json`).
- **Replicas:** reads normally go through a streaming replica that applies WAL as it arrives
  (measured lag 1.6 ms median). From the call that carries `delayed_visibility` on, reads go
  through a second streaming replica that applies WAL 9 s after each commit.
- **Timing:** the client timeout is 3 s and the proxy holds withheld responses for 6 s. A hidden
  write therefore stays invisible for 6 s after the client's timeout, as in the simulator. In
  the lag-only arm the simulator's delay is set to 9 s to match.
- **Runtime:** the poll budget is unchanged.
- **Key scope:** default (completed).

All of this is described in [REAL_SERVICES.md](../REAL_SERVICES.md).

**Execution:**
- per-provider pools (Anthropic 8, OpenAI 8, Together 12), a 180 s request timeout
- `caffeinate -i -s`
- `stack.sh fresh-log` before the run, and `stack.sh collect` after it

**Fixed sample.** No interim looks at outcomes.

## Confirmatory hypotheses

Outcome: [harm](../DEFINITIONS.md#harm) on the **real** substrate. These are two-sided
Mantel–Haenszel tests stratified by model, Holm-corrected across T1–T3 at α = 0.05. A
hypothesis is confirmed only if its Holm p < 0.05 **and** the pooled odds ratio is > 1 (arm A
higher).

| ID | Claim | Arm A (predicted higher harm) | Arm B |
|---|---|---|---|
| T1 | The runtime prevents hidden-write harm on real services | hidden write, no keys | hidden write, runtime |
| T2 | The runtime prevents partial-commit harm on real services | partial commit, keys | partial commit, runtime |
| T3 | The keys hazard appears on real services | partial commit, keys | partial commit, no keys |

**Separate test, α = 0.05:**
- **N1 (non-inferiority):** P6 harm under both faults, real vs simulated, margin +3 points. The
  runtime is as safe on real services as in the simulator.

**Pre-registered decision rule:** Q1 holds on real services **if T1 and T2 are confirmed and N1
is non-inferior**. T3 and the substrate comparison inform the paper but don't decide this.

**Substrate comparison (pre-registered, each TOST at α = 0.05, margin ±10 points):** real vs
simulated harm, pooled over models, in each of the five arms where the agent recovers on its
own (no fault; visibility lag only; hidden write without keys; partial commit with and without
keys). "Equivalent"
supports using the simulator as a stand-in for real services in those conditions. "Different"
is a finding about what the simulator misses.

**Expectations, stated so they aren't mistaken for findings:**
- **Visibility lag only.** A successful payment hidden by lag can lead an agent that re-reads
  within 9 s to pay again, with no timeout at all. Both substrates model this arm.
- **Opus and GPT-6.1-Sol** had no hidden-write harm on the simulated ledger. They may contribute
  no events to T1's strata.

## Secondary (pre-registered)

- Harm and success by arm and substrate, with Wilson intervals.
- Harm by model, by arm and substrate.
- The runtime against real lag: for P6 on the real substrate, reconcile lookups on the faulted
  payment and whether it was found (by fault).
- Episode duration by arm and substrate (wall clock for real, simulated clock for the simulator;
  descriptive only, since the clocks differ).
- Fault audit: responses the proxy withheld and partial commits it forwarded, against the
  faults the injector requested. A mismatch is a deviation.

## Exploratory (to be labelled as such)

- How agents behaved when replication lag hid a *successful* payment.
- Per-instance differences.
- Comparisons with Stage E.
- Anything not listed above.

## Exclusions

Same rules as the [confirmation run](compound-confirm.md#exclusions-and-deviations), via
`--rerun-errors`:
- Errored episodes (harness errors, including stack failures such as a replica that never
  catches up, and non-refusal agent errors including `timeout`) are re-run from the registered
  commit with the stack unchanged. Originals and traces are kept.
- Episodes that still fail are excluded and counted.
- A model withdrawn by its provider is excluded and counted, with no substitute.
- Every response's served model ID is checked.
- The stack's `stack.json` must match the values above; a difference is a deviation.

## Cost

Using each model's measured cost per simulated-ledger episode in Stage E, plus 30% headroom
(real episodes may take more turns):

| Provider | Estimate |
|---|---|
| Anthropic | ≈ $12.80 |
| OpenAI | ≈ $5.25 |
| Together | ≈ $1.40 |
| **Total** | **≈ $19.50** |

The pilot and its re-check cost $0.06.

## Pilot findings

**Pilot** (`runs/real-ledger-pilot-20261028-110218`): 36 episodes, $0.03, on the uncommitted
study code (recorded in `manifest.json` and `stack.json`).
- **Execution:** two harness errors, from a race in the harness, not the stack. Two worker
  threads imported `httpx` lazily at the same moment ("partially initialized module"). Fixed by
  importing it, and `psycopg`, when `ledger_real` loads, which happens in the main thread. Both
  episodes succeeded on re-run. Every GLM response came from the requested model.
- **Mechanics:** the proxy withheld exactly the responses the injector requested. P6 found every
  hidden write on its 4th lookup and compensated every partial commit. The no-fault task was
  solvable (6/6).

**One design defect found and fixed before registration: the real partial-commit condition
didn't match the simulator's.**
- **The problem:** every read went through the 9 s replica, so on the real stack a partial
  commit was *also* a hidden write. In the simulator a partial commit has no visibility lag, so
  an agent that checks after the timeout sees the stray payment. On the real stack it didn't,
  and agents without keys paid again (5 of 6 harmed, 1 self-corrected). T3 and the substrate
  comparison would have compared different conditions.
- **The fix:**
  - A second streaming replica with no apply delay is the normal read path.
  - Reads move to the 9 s replica only from the call that carries `delayed_visibility`, as in
    the simulator, where that fault alone hides writes.
  - All lag remains real replication lag.
  - The hazard of a successful payment hidden by lag became its own arm, on both substrates
    (lag only, no timeout; the simulator's delay set to 9 s to match). That adds 360 episodes.
- **Re-check** (`runs/real-ledger-pilot-recheck-20261028-110737`): 42 episodes on every arm,
  fresh seeds 903–905, $0.03.
  - No errors, and the fault audit matched (30 timeouts, 18 partial commits).
  - P6 found every hidden write on its 4th lookup and compensated every partial commit.
  - Outcomes were inspected only to confirm that the partial-commit arms now leave the stray
    payment visible, as in the simulator.

Analysis: `analysis/real_services.py` guards against a missing substrate (the pilots are
real-only) and includes the lag-only arm in the substrate comparison. No change to
hypotheses or tests.

### Deviations

*(None yet.)*
