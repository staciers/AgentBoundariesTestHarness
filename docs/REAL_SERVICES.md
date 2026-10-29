# Real services (Tier A): the ledger on Postgres

Every other domain in the harness runs against simulated services: Python dictionaries in an
in-memory `World`, with faults applied inside it. This replication runs the held-out ledger
domain against real infrastructure, to answer the reviewer objection *"the runtime only works
because you wrote the services"*. Tier A is local. Network latency across data centers is
Tier B (not built yet).

## What runs where

```
 harness (abh)                         services/ledger/                 Docker (postgres:16)
 ─────────────                         ────────────────                 ────────────────────
 agent ⇄ control plane ⇄ runtime
            │ RemoteToolSpec (httpx, 3 s client timeout)
            ▼
       proxy.py :8700  ── X-Fault ──▶  service.py :8701  ── writes ──▶  primary :55432
       (withholds responses,           (business rules,                   │ streaming replication
        forwards partial flag)          idempotency keys,                 ├──▶ fast replica    :55434 (no apply delay)
                                         two-transaction payments)        └──▶ lagging replica :55433 (apply delay 9 s)
                                         reads ─▶ fast replica, or lagging after a delayed_visibility fault
 evaluator ◀── sync(): payments, invoices, balance, read from the primary after every call
```

## What is real and what is injected

| | Simulated ledger | Real ledger (`ledger_real/base`) |
|---|---|---|
| State | dicts in `World` | Postgres, one database per episode |
| A payment | two writes to the world | two Postgres transactions: debit and record the payment, then mark the invoice paid |
| Partial commit | `ctx.partial` skips the second write | the service fails between its two transactions (told to by the proxy) |
| Inspecting an attempt | `inspect` reads ground truth | `GET /payments/attempts`: takes the key's lock (waiting for any attempt in flight), then reads the primary |
| Idempotency key | a world table | a row in `idempotency_keys`, written in the invoice transaction (completed scope); same-key requests serialized by an advisory lock |
| Visibility lag | per-write, only under the `delayed_visibility` fault | reads go through a streaming replica with no apply delay (1.6 ms median lag); from the call carrying `delayed_visibility` on, through a second replica that applies WAL 9 s after commit |
| Timeout | the injector raises `ToolTimeout` | the proxy withholds the response and holds the connection for 6 s, so the client's 3 s read timeout fires |
| Which call is faulted | the fault injector | the same fault injector; it names the faults in `X-Fault`, and the proxy makes them happen |
| Clock | `SimClock` (simulated) | `RealClock` (wall clock): model and service latency take real time, and the runtime's waits really sleep |
| Evaluation | invariants on the world | the same invariants, on the world after `sync()` mirrors the primary into it |

**Timing alignment.** In the simulator a hidden write stays invisible for 6 s after the client
gets its timeout. Here the client times out 3 s after the commit and the replica applies 9 s
after it, which gives the same 6 s. The runtime's poll budget is unchanged (4 lookups, 2.5 s
apart). In both substrates it finds a hidden write on its 4th lookup, about 1.5 s after the
write becomes visible. In scripted checks, 24 concurrent P6 episodes all found it. Under heavy
load, real replication can outrun that margin; the study reports any misses.

**Why two replicas.** The first pilot read everything through the 9 s replica. That made every
condition a hidden write, including the partial commit, which in the simulator has no
visibility lag. With a fast replica as the normal read path, each condition matches the
simulator's, and every lag is still real replication lag. The study's lag-only arm (a
successful payment hidden for 9 s, no timeout) measures the hazard that constant lag creates.

## Running it

```bash
services/ledger/stack.sh up
services/ledger/stack.sh fresh-log
caffeinate -i -s .venv/bin/python -m abh run experiments/real_ledger_pilot.json
services/ledger/stack.sh collect runs/<run_dir>
.venv/bin/python analysis/real_services.py runs/<run_dir>
services/ledger/stack.sh down
```

- `stack.sh up` starts the Postgres primary and both replicas (`infra.sh`), the service and the
  proxy. It records the stack (image digest, Postgres version, both replicas' delays, hold,
  client timeout, git commit) in `services/ledger/.run/stack.json`.
- `fresh-log` restarts the proxy with a new request log, so a run's fault audit counts only that
  run.
- `collect` copies `stack.json` and the proxy log into the run folder. The analysis checks
  that the faults the proxy produced equal the faults the injector requested.

**Tests.** `TestRealServices` in `tests/test_harness.py` runs without the stack. With the stack
up, `ABH_LEDGER_LIVE=1 .venv/bin/python -m unittest tests.test_harness.TestRealServices` also
runs scripted agents through every fault arm and checks that the outcomes match the simulator.

## Limits

- **Local only.** Round trips are sub-millisecond, so latency and overhead numbers from this
  setup understate a deployed system. Tier B (cross-region) addresses that.
- **Faults are still chosen by the harness.** The proxy and the service make them happen on
  real infrastructure, but how often they occur is set by the study, not observed.
- **One domain, one key scope.** Only the default (completed) key scope is implemented. The
  contract variants (atomic scope, repair primitives) raise an error rather than run.
- **No trace replay.** Real services aren't deterministic, so `abh rescore` doesn't apply to
  these runs; the analysis uses the recorded outcomes.
- **Real-services scenarios are opt-in.** `ledger_real/*` is never listed by
  `list_scenarios()` and never matched by a glob in a spec; name it exactly.
