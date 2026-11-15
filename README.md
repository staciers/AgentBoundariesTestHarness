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

## Paper

The first paper from this harness is **Execution Boundaries for Agentic Systems** (Stacie
Riddle, 2026). arXiv link to follow.

- [`paper/full.md`](paper/full.md) and [`paper/supplements.md`](paper/supplements.md): the
  paper and its supplement (S1–S5).
- [`paper/latex/`](paper/latex/): the LaTeX build. `md2tex.py --supplement` produces the paper and
  supplement as one PDF; see [its README](paper/latex/README.md).
- [`paper/figures/make_figures.py`](paper/figures/make_figures.py): regenerates every figure from
  the committed runs.
- [`docs/preregistration/`](docs/preregistration/) and [`docs/RESULTS.md`](docs/RESULTS.md): the
  registered hypotheses and the results.
- `runs/`: the committed runs behind the paper (episodes and traces). `python3 -m abh rescore
  runs/<dir>` replays any of them with no model calls.

## Quick start

The core needs only Python ≥ 3.9 and has no dependencies.

```bash
python3 -m abh list
```

```bash
python3 -m abh episode travel/base --policy P1 --agent scripted:naive --fault timeout_after_execution
```

For a failure *rate* instead of a scheduled fault, give `rate` in a spec, e.g.
`{"type": "transient_failure", "target": "@writes", "rate": 0.1}`; see
[`experiments/rate_sweep_scripted.json`](experiments/rate_sweep_scripted.json).

To inject a compound fault, repeat `--fault`. Faults that hit the same call compose; see
[Compound faults](docs/ARCHITECTURE.md#compound-faults).

```bash
python3 -m abh episode devops/base --policy P1 --agent scripted:strong --fault timeout_after_execution --fault delayed_visibility
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
resumed with `--resume runs/<dir>` (add `--rerun-errors` to re-run errored episodes, keeping the
originals), and `python3 -m abh report runs/<dir>` rebuilds the report. Every launch is recorded
in `manifest.json` (git commit, clean tree, versions), and `python3 -m abh status runs/<dir>`
shows progress, errors and cost from the run's own `status.json`.
`python3 -m abh rescore runs/<dir>` replays saved traces under the current evaluator, with no
model calls. Use it after changing metrics.

### LLM agents (Claude and OpenAI)

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

For OpenAI models, install the adapter dependency and set `OPENAI_API_KEY`:

```bash
python3.11 -m pip install '.[openai]'
python3.11 -m abh episode devops/base --policy P6 --agent openai:gpt-5.4:high --fault timeout_after_execution -v
python3.11 -m abh run experiments/pilot_openai.json --dry-run
```

Known OpenAI models have dated pricing defaults for cost reporting. You can override
`input_price`, `output_price`, and `cache_read_price` (USD per million tokens) in the agent spec;
retain those assumptions with the run. Unknown models report measured usage but zero cost until
prices are supplied.

## Concepts

| Concept | Where | Notes |
|---|---|---|
| Action semantics | `abh/semantics.py` | side_effect, idempotent, reversible, compensable, consequence, authority_requirement, idempotency-key support, multipart |
| Execution states | `abh/semantics.py` | NOT_EXECUTED, EXECUTED, EXECUTION_UNKNOWN, PARTIALLY_EXECUTED, VERIFIED, SEMANTIC_FAILURE |
| World | `abh/world.py` | versioned records with truth and visible views (delayed visibility), effects ledger, simulated clock |
| Faults (12) | `abh/faults.py` | the full fault taxonomy, listed in [Fault types](docs/DEFINITIONS.md#fault-types); each injection records whether it committed and who resolved it; faults can be combined ([compound faults](docs/ARCHITECTURE.md#compound-faults)) |
| Runtime | `abh/runtime.py` | `none` (raw errors), `naive_retry` (conventional infra retry), `semantic` (keys, reconcile, verify, compensate, classify) |
| Authority | `abh/authority.py` | principals, delegation, rules; kept independent of uncertainty |
| Human | `abh/human.py`, `abh/human_model.py` | in-episode decisions: simulated (error rate, vigilance decrement, attention budget) or interactive. After the run: an empirical time-and-cost model by organization profile (coverage, after-hours, runbooks, approval chains) with Monte Carlo intervals; `abh human-cost runs/<dir>`, see [docs/HUMAN_MODEL.md](docs/HUMAN_MODEL.md) |
| Policies | `abh/policies.py` | P1–P6 and ORACLE; the runtime mode can be overridden per experiment |
| Control plane | `abh/controlplane.py` | authority → gate → runtime → route; does the ground-truth bookkeeping |
| Scenarios | `abh/domains/` | travel, commerce, devops, scheduling, platform (repo / CI / PR, the Paper 2 seed) × {base, ambiguous, authority} |
| Agents | `abh/agents/` | `scripted` baseline (incl. the deterministic `workflow`), plus `anthropic`, `openai`, and `compat` (open-weight models via OpenAI-compatible Chat Completions: Together, Fireworks, DeepInfra, OpenRouter, DeepSeek, Z.ai) manual tool loops; `replay` re-scores traces |

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

Every term in a report, from column names to outcomes, policies, faults and execution states,
is defined in [docs/DEFINITIONS.md](docs/DEFINITIONS.md), and report column headers link
there. Caveats appear in each report as footnotes, and only when they apply to that run's
data. The full catalogue is in [Report notes](docs/DEFINITIONS.md#report-notes). The ones
that most often change how a result reads:

- [Scripted-agent results check the harness; they aren't evidence](docs/DEFINITIONS.md#note-scripted_not_evidence)
- [Autonomous coverage is capped by the share of `base` scenarios](docs/DEFINITIONS.md#note-coverage_ceiling)
- [Gate reliance under approval-gated policies](docs/DEFINITIONS.md#note-gate_reliance)
- [End-state vs. self-corrected harm](docs/DEFINITIONS.md#note-harm_split) (rationale in
  [ARCHITECTURE.md](docs/ARCHITECTURE.md#harm-end-state-vs-self-corrected))
- [Failure ownership is heuristic](docs/DEFINITIONS.md#note-ownership_heuristic)
- [Small groups](docs/DEFINITIONS.md#note-small_samples)

Definitions and notes are maintained in `abh/definitions.py`. After editing it, run
`python3 -m abh definitions` to regenerate the doc; a test fails if you forget.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the harness maps to the RQs and
hypotheses, and [docs/OPENAI_MODELS.md](docs/OPENAI_MODELS.md) for the OpenAI integration and
class, component, sequence, and deployment diagrams.

## License

MIT. See [LICENSE](LICENSE).
