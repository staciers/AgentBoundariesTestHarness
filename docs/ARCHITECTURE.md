# Architecture and research mapping

## Episode pipeline

```
agent.act(results) ──► ToolCall(name, args, confidence)
        │
        ▼
ControlPlane.handle
  1. ask_human?            → EscalationKind.CLARIFICATION / APPROVAL (P5, or "ask_human": true)
  2. authority check       → Delegation.check(tool, args, world)                 [authority]
  3. policy.gate(...)      → human APPROVAL before execution (deny returns a hint) [epistemic × consequence]
  4. runtime.execute(...)  → FaultInjector.invoke → ToolSpec.execute (idempotency store)
                              none | naive_retry | semantic(keys, reconcile, verify, compensate) [execution]
  5. unresolved? policy.route → HUMAN (EXECUTION_STATE) | AGENT (raw or structured error)
  6. bookkeeping           → authority violations, escalation necessity, needs met, fault ownership
        │
        ▼
ToolResult(content for the model, meta for scripted agents and analysis)
```

The harness owns the loop. Agents only propose calls. This is what makes it possible to compare
policies on identical agents, faults and seeds.

## Ground truth

| Label | Source | Used for |
|---|---|---|
| Task success | `Invariant(kind="task")` evaluated on `World.truth()` | success, coverage |
| Harm | `Invariant(kind="harm")` plus authority violations | harm, autonomous harm risk |
| Duplicate effects | effects ledger (`dedupe_key`), active effects only | H1, H6 |
| Escalation necessary | `Oracle.needs_human`: authority violated, or the action is wrong w.r.t. hidden intent; clarification while an ambiguity need is unmet; unresolved execution state | intervention precision (H7) |
| Human needs | `Scenario.human_needs` (authority, ambiguity) | intervention recall (H3, H7) |
| Fault committed | `InjectedFault.committed` | RQ1 analysis |

## Mapping to research questions and hypotheses

| | Experiment | Primary metrics |
|---|---|---|
| RQ1 / H1 / H2 | `runtime_factorial.json`: runtime {none, naive_retry, semantic} × agent competence × each single fault | success and harm by fault class; `failure_ownership.csv` |
| RQ2 / H5 | same, with LLM agents of several capability levels in place of scripted profiles | interaction runtime × model on execution faults vs. semantic faults |
| RQ3 / H3 / H7 | `pilot_*.json`, `by_variant` table | intervention precision and recall per variant |
| RQ4 / H4 | P3 and P6 threshold sweeps (+ P4 `min_consequence` sweep) | `risk_coverage.csv` / `.png` at matched task mix |
| RQ5 / H6 | any spec | failures_exposed, tokens, model calls, sim minutes, human wait, cost |

## Adding a scenario

Write a module in `abh/domains/` that builds a `Scenario` and registers it with
`@register("domain/variant")`, then import it in `_ensure_loaded`. A scenario needs:

- **tools**: `ToolSpec` with honest `ActionSemantics`. Add `reconcile` (lookup by client
  reference), `postcondition`, and `compensate` wherever the real system would allow them. The
  semantic runtime can only use hooks that exist, and that limit is deliberate.
- **fault_targets**: tool names for the `write`, `multi`, `read` and `unavailable` roles.
- **semantic_faults**: domain realisations of `PRECONDITION_CHANGED` and `TASK_INVALID_RESULT`.
  Make the invalid result *detectable by reading carefully* (wrong date, "Renewed" in the title,
  an `attendees_checked` field), so that semantic recovery is possible in principle.
- **invariants**, **judge** (correct with respect to hidden intent), **delegation** rules,
  **human_needs**, **hidden** / **guesses** / **clarification**.
- **plan**: reference steps for the scripted agent. The LLM agent never sees this.

## Extension points for Paper 2 (agent-native developer platform)

The control plane is set up to become the agent control plane in the Paper 2 architecture:

| Paper 2 concern | Hook today | Likely extension |
|---|---|---|
| Agent identity and delegated authority | `Principal`, `Delegation`, `AuthorityRule` | task-scoped credentials, delegation chains (human → agent → sub-agent), expiry |
| Policy | `ControlPolicy.gate/route` | policy-as-code (OPA/Cedar-style) evaluated by the control plane |
| Execution services | `ToolSpec` + `ReliabilityRuntime` | sandboxes, CI/CD, infrastructure provisioning as tool families with declared semantics |
| Verification services | `postcondition`, invariants | tests, deploy health, behavioural evaluation as first-class verifiers |
| Context services | `Scenario.system_notes`, read tools | service catalogue / ownership graph / docs as structured context tools |
| Human attention (Paper 5) | `SimulatedHuman`, `HumanConfig.budget`, fatigue | shared reviewer pool across concurrent episodes, queueing, priority scheduling |
| Provenance (Paper 4) | `Trace`, `EscalationRequest.context`, `InteractiveHuman` | vary the information shown in escalations; measure decision time and accuracy |

The `devops` domain is the natural seed for Paper 2. Extend it with repositories, PRs, CI runs,
a service catalogue and multi-step migrations, and keep the same control plane.

## Known limitations / next steps

- Each fault injection hits one tool call. Compound faults on the *same* call (for example a
  timeout after execution *plus* delayed visibility) need `FaultInjector._active` to return
  several specs.
- Only Claude has an adapter. Adding another model family means implementing
  `Agent.start/act` (see `agents/anthropic_agent.py`).
- The simulated human answers from ground truth with fixed noise. Calibrate the latency and
  error parameters against a small interactive pilot (`human.mode = "interactive"`) before
  making claims about human cost.
- Confidence for P3/P6 is self-reported through a tool argument. Consider adding sampled
  consistency, or logprob-based estimates where available, as alternative uncertainty signals
  (the KnowNo-style baseline for the follow-on delegation paper).
