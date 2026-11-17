# Correction: failed verification and unsafe keyed retries (November 2026)

**Summary.** An external review of the runtime, after all studies were complete, found two gaps
in `abh/runtime.py`. Both are fixed, with regression tests. The fix changes no simulated or
scripted episode: replayed or re-run under the corrected runtime, each one either reproduces its
original record or, for 714 early-pilot episodes, differs in exactly the same way under the code
before the fix (explained below). Every response an agent receives is also identical, in full,
under the code before and after the fix. Real-services episodes were not re-run. One of them
reached the first gap; it ended without harm, and under the corrected runtime it would have been
escalated instead (a prediction, not a measurement). The paper's description of verification
overstated what the runtime guaranteed, and has been corrected.

## What was found

**1. Failed verification returned success.** After a write, the semantic runtime checks the
tool's postcondition, waiting for the write to become visible: up to 4 checks, 2.5 s apart (at
0, 2.5, 5 and 7.5 s; the runtime returns after one more wait, about 10 s after the first). If
every check failed, `_success()` left the outcome as `EXECUTED`, which counts as resolved. The
agent received it with `is_error: false`, and P6 never routed it to a human. The agent's view
did say `execution_state: "EXECUTED"` rather than `"VERIFIED"`, but nothing treated that as
unresolved.

*Why it matters:* the paper states that an agent reading after a verified success sees its own
write. That holds, but a write that was never verified was also presented as a success, so the
guarantee silently didn't apply when visibility lag exceeded the verification window.

**2. A keyed retry could repeat a partial commit.** After a timeout, the runtime retried with the
idempotency key whenever it had one, and undid an incomplete attempt first only if the tool had a
compensation hook. For a tool whose key records only completed calls (key scope `completed`),
whose partial effects persist, and which has no compensation, the retry could repeat the part
that had already committed.

*Why it matters:* the runtime's safety after a timeout depends on what the tool's contract
provides. A general runtime should refuse a retry it can't make safe, rather than assume the
contract provides recovery.

## The fix

1. **New execution state, `UNVERIFIED`** (`abh/semantics.py`): the service reported success, but
   the postcondition wasn't observed within the verification window. It is unresolved. The
   runtime doesn't retry (the service said it succeeded); the agent gets an error telling it not
   to repeat the call and to check again later or escalate; and P6 routes consequential cases to
   a human (`abh/policies.py`). Defined in `abh/definitions.py` and `docs/DEFINITIONS.md`.
2. **Unsafe retries are refused** (`abh/runtime.py`): after a timeout, if a keyed retry could
   repeat a partial commit and the tool can't be compensated, the runtime returns
   `EXECUTION_UNKNOWN` with the action `unsafe_retry_refused`, and P6 escalates. The `inspect`
   fast path follows the same rule. `ExecutionContract.unsafe_retry` (`abh/contract.py`) flags the
   combination, and the harness warns when it loads such a tool.

## Tests

Seven regression tests in `tests/test_harness.py` (`TestRuntimeCorrections2026_11`):

- a postcondition that is always false yields `UNVERIFIED`: unresolved, exactly 4 checks, no
  retry, and an error the agent sees;
- P6 routes that outcome to a human;
- a postcondition that holds on the third check still yields `VERIFIED`;
- a tool with the unsafe combination has its retry refused, with no duplicate effects;
- the same fault on a tool with compensation still retries cleanly;
- P6 escalates the refused retry;
- no tool in any study scenario has the unsafe combination.

Two existing tests asserted the old behavior (a write still invisible after the verification
window counted as resolved). They now expect `UNVERIFIED`; what they were written to check, no
repeat and no wrongful compensation, is unchanged. All 125 tests pass.

## Does it change the reported results?

No. The original records in `runs/` were not modified; every check below compares a new
execution against them.

| What | How | Episodes | Changed by the fix |
|---|---|---|---|
| Studies and pilots with saved traces | Replayed from traces under the corrected runtime (recorded agent decisions, no model calls) and compared with the records: outcome, harm, faithfulness fields, injected faults, each runtime outcome (state and actions), and each result's kind and error flag. [Report](replay-2026-11.md) | 51,393 | 0 (72 pilot episodes differ from their records under both versions; below) |
| Full content of every agent-visible response | Traces don't record response content, so it can't be compared with the records. Instead, every traced episode was replayed under the code before and after the fix, and the full sequence of responses each agent receives (content and error flag) was compared between the two. A control that changed only the guidance text changed 501 of 4,690 episodes' responses, so the comparison does see content. [Results](responses-2026-11.json) | 51,393 (274,815 responses) | 0 |
| Scripted-agent runs (no traces) | Re-run from their configurations (deterministic, no model calls) and compared with the records. [Results](rerun-scripted-2026-11.json) | 64,290 | 0 (642 pilot episodes differ from their records under both versions; below) |
| Stage B sensitivity analysis | Same 7,920 episodes as the Stage B run, whose traces replayed identically | 7,920 | 0 |
| Real-services episodes (Postgres) | Not replayed or re-run (needs the live stack). Searched all 97,172 runtime outcomes in the committed traces for the two conditions | 1,338 | 1 reached gap 1 (below; effect predicted, not measured) |
| Overhead benchmark (Table 2) | Verification never ran out in any benchmark episode (at most 3 of the 4 checks used) | 180 | 0 |

**Differences that predate the fix.** Some old pilot records no longer reproduce under the current
harness, with or without this fix: 72 episodes in the Stage B and Stage E pilots, and 642 in
the first scripted pilot (October 12). Each was checked against the code before the fix and
differs in exactly the same way, so they reflect earlier scenario and harness changes recorded in
Supplement Table S1, not this correction. None is part of a registered analysis.

**The affected episode.** Gap 1 occurred 7 times, all on real services: 6 times in the
real-services pilot, during the replica design defect (Table S1, issue 20), and once in the
registered real-services run (`runs/real-ledger-20261028-111807`, DeepSeek-V4.1-Flash, P6, hidden
write, seed 624).

- *Measured (the original run):* the payment stayed invisible past the verification window, the
  runtime returned success, and the episode ended in success with no harm and no escalation. The
  arm (P6, hidden write, real services) recorded 0/180 harm and 180/180 autonomous success.
- *Expected under the corrected runtime (not re-run):* the payment call would be reported as
  `UNVERIFIED`, and P6 would escalate it to the simulated human, since a wire payment is
  consequential. What happens next was not measured: the simulated human can err, and the agent's
  later turns could differ from the recorded ones. If the escalation resolves correctly, the arm
  would show 179/180 autonomous success; its harm can't be stated without re-running the episode.

Gap 2 never occurred: every tool that can commit partly, simulated or real, has a compensation hook.

## What changes in the paper

- §4.3: verification checks for a bounded window and does not wait indefinitely; the pseudocode
  shows the `UNVERIFIED` case.
- §9, new limitations: (1) the verification window is bounded (last check about 7.5 s after the
  first), so "the agent sees its own write" holds only when visibility lag is within it; beyond it
  the runtime reports the call as unresolved instead of as a success. (2) Automatic recovery after a timeout requires the tool's contract to
  provide an atomic key scope, compensation, or inspection; without them the runtime escalates.
- Supplement Table S1: issues 25 and 26.

## Not done here

A systematic test of where the runtime's assumptions fail (exceeding the polling budget, failed
compensation, incorrect reconciliation, a restart during recovery, a delayed original request) is
future work. The affected episode above is a natural instance of the first.

## Reproduce

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/python analysis/correction_replay.py           # replay; writes docs/corrections/replay-2026-11.*
.venv/bin/python analysis/correction_rerun_scripted.py   # scripted re-run; writes rerun-scripted-2026-11.json
# full response content, between two code versions (run the first command under each):
.venv/bin/python analysis/correction_compare_responses.py responses-after.json
python3 analysis/correction_compare_responses.py --compare responses-before.json responses-after.json
.venv/bin/python -m abh rescore --check runs/<dir>       # one run, report only
```
