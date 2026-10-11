# Autonomy Boundary Harness (ABH)

The experimental testbed for **Autonomy Boundaries for Agentic Systems: Allocating Control Across
Runtimes, Agents, and Humans**. Its interfaces are also meant to become the execution and control
layer for the follow-on platform paper.

ABH runs tool-using agents against **stateful, deterministic environments**. It injects
**controlled faults** between the agent and the services, and it routes every proposed action
through a **control plane** that splits control three ways:

```
            HUMAN       judgment / authority        <- escalation (approval, clarification, execution state)
              ▲
            AGENT       reasoning / replanning      <- semantic failures, structured errors
              ▲
     RELIABILITY RUNTIME  execution / verification / recovery   (none | naive_retry | semantic)
              │
     TOOLS ─► FAULT INJECTOR ─► SERVICES ─► WORLD STATE (truth vs. visible, effects ledger)
```

Success is scored by **world-state invariants** checked against ground truth, not by an LLM
judge. Every episode records duplicate side effects, authority violations, escalations (each
labelled necessary or not), the human needs that were met, how many failures reached the model,
tokens, and simulated latency.

## Quick start

The core needs only Python ≥ 3.9 and has no dependencies.

```bash
python3 -m abh list
```

```bash
python3 -m abh episode travel/base --policy P1 --agent scripted:naive --fault timeout_after_execution
```

```bash
python3 -m abh run experiments/pilot_scripted.json
```

```bash
python3 -m unittest discover -s tests -v
```

`run` writes `runs/<name>-<timestamp>/` containing `episodes.jsonl`, `report.md`, and the CSVs
`by_policy`, `by_policy_runtime`, `by_fault`, `by_variant`, `failure_ownership` and
`risk_coverage`. If matplotlib is installed, it also writes `risk_coverage.png`. Runs can be
resumed with `--resume runs/<dir>`, and `python3 -m abh report runs/<dir>` rebuilds the report.

### LLM agents (Claude)

```bash
python3.11 -m pip install anthropic
```

```bash
python3.11 -m abh episode devops/base --policy P6 --agent anthropic:claude-opus-5-5:high --fault timeout_after_execution -v
```

```bash
python3.11 -m abh run experiments/pilot_claude.json --dry-run
```

The current `anthropic` SDK requires Python ≥ 3.10. Credentials come from `ANTHROPIC_API_KEY` or
an `ant auth login` profile. Always run with `--dry-run` first to see how many episodes a spec
expands to, because every LLM episode costs money. Each episode records measured tokens and
cost, and `keep_traces: true` saves the full transcripts.

## Concepts

| Concept | Where | Notes |
|---|---|---|
| Action semantics | `abh/semantics.py` | side_effect, idempotent, reversible, compensable, consequence, authority_requirement, idempotency-key support, multipart |
| Execution states | `abh/semantics.py` | NOT_EXECUTED, EXECUTED, EXECUTION_UNKNOWN, PARTIALLY_EXECUTED, VERIFIED, SEMANTIC_FAILURE |
| World | `abh/world.py` | versioned records with truth and visible views (delayed visibility), effects ledger, simulated clock |
| Faults (12) | `abh/faults.py` | the full prospectus §6 taxonomy; each injection records whether it committed and who resolved it (link: https://docs.google.com/document/d/1Uwq2EzlwCvjG2rwmyl9x1YVzFJiwK02g9VYpPjhgEBE/edit?tab=t.h35zl5z98uqb)|
| Runtime | `abh/runtime.py` | `none` (raw errors), `naive_retry` (conventional infra retry), `semantic` (keys, reconcile, verify, compensate, classify) |
| Authority | `abh/authority.py` | principals, delegation, rules; kept independent of uncertainty |
| Human | `abh/human.py` | simulated (log-normal latency, error rate, vigilance decrement, attention budget) or interactive |
| Policies | `abh/policies.py` | P1–P6 and ORACLE; the runtime mode can be overridden per experiment |
| Control plane | `abh/controlplane.py` | authority → gate → runtime → route; does the ground-truth bookkeeping |
| Scenarios | `abh/domains/` | travel, commerce, devops, scheduling × {base, ambiguous, authority} |
| Agents | `abh/agents/` | `scripted` (reference plan with competence knobs) and `anthropic` (manual tool loop) |

### Policies

| | Gate (before execution) | Route (unresolved after execution) | Default runtime |
|---|---|---|---|
| P1 | never | agent | none |
| P2 | every side-effecting action | agent | none |
| P3 | stated confidence < threshold (any call) | agent | none |
| P4 | consequence ≥ class (default HIGH) | agent | none |
| P5 | never; the agent gets an `ask_human` tool | agent | none |
| P6 | authority violation; or a consequential action with confidence < threshold | execution-unresolved and consequential → human, otherwise agent | semantic |
| ORACLE | ground truth: authority, or the action would be wrong | as P6 | semantic |

Parameterise a policy as a dict, e.g. `{"name": "P6", "threshold": 0.8, "min_consequence": "HIGH"}`.
Any policy also accepts `"runtime"`, and `"ask_human": true` exposes the ask tool.

## Read this before interpreting results

1. **Scripted-agent results check the harness. They are not evidence for the hypotheses.** The
   scripted agent's competence knobs and the ORACLE's labels encode the paper's assumptions.
   Patterns like "P6 beats P1 on execution faults" are partly built in. The evidence has to come
   from LLM agents, across model families and capability levels. Use scripted runs to debug
   scenarios, size experiments, and run sensitivity analyses (for example, sweep `replan_skill`).
2. **Ceilings on autonomous coverage.** Two-thirds of the scenarios (`ambiguous`, `authority`)
   cannot be completed correctly without a human, so with the full scenario set coverage tops out
   near 0.33. Compare policies at matched task mixes, and also report results by `variant`.
3. **Gate reliance.** Under gated policies (P2/P3/P4/P6/ORACLE), agents are told that some actions
   may be sent to an approver. A scripted agent that is aware of an authority rule then goes
   ahead, trusting the gate. That is why P3 can show *more* authority violations than P1: P1
   agents more often refuse. LLMs may do the same, so this is a real effect, but report it as
   one.
4. **Failure ownership is heuristic.** A fault counts as runtime-resolved when the call ended
   resolved after a runtime action. It counts as human-resolved when it was escalated. Otherwise
   it counts as passed to the agent, whatever the agent then did with it.
5. **Refusal fallbacks are off by default** in the Claude adapter. Silently switching models
   would confound the model-capability factor. Refusals end the episode as `agent_error`.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the harness maps to the RQs and
hypotheses, the metric definitions, and the extension points for Paper 2.
