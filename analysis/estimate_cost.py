"""Estimate the API cost of an experiment spec from a previous run's observed costs.

    .venv/bin/python analysis/estimate_cost.py experiments/compound_confirm.json runs/<previous-run>

Each planned episode is priced at the mean observed cost for the most specific matching
cell: (model, fault condition, policy) first, then (model, fault condition), then the
model's overall mean. Policies with ablation parameters (key_description) borrow the
cost of their parent policy (same label without that parameter).
"""
import json
import re
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, ".")
from abh.agents.base import make_agent  # noqa: E402
from abh.experiment import expand  # noqa: E402
from abh.metrics import load_episodes  # noqa: E402
from abh.policies import make_policy  # noqa: E402


def parent(label: str) -> str:
    return re.sub(r"\[key_description=[a-z_]+\]", "", label)


def price_ratio_fallback(agent: str, cells) -> float:
    """Unseen model: scale the observed mean of a same-provider model by list-price ratio
    (blended 1:4 input:output, roughly an agentic workload). Returns cost or raises."""
    from abh.agents.anthropic_agent import PRICES as AP
    from abh.agents.openai_agent import PRICES as OP
    provider, rest = agent.split(":", 1)
    model = rest.split("@")[0]
    prices = AP if provider == "anthropic" else OP
    blend = lambda m: (prices[m][0] + 4 * prices[m][1]) / 5
    seen = [(a, v) for (a, *_), v in cells.items() if len(_) == 0 and a.startswith(provider + ":")]
    if model not in prices or not seen:
        raise SystemExit(f"no observed cost for {agent} and no same-provider model to scale from")
    ref, vals = max(seen, key=lambda kv: blend(kv[0].split(":", 1)[1].split("@")[0]))
    ref_model = ref.split(":", 1)[1].split("@")[0]
    ratio = blend(model) / blend(ref_model)
    print(f"  (estimating {agent} as {ref} x {ratio:.1f} by list price)")
    return float(np.mean(vals)) * ratio


def main(spec_path: str, run_dir: str, headroom: float = 0.3) -> None:
    spec = json.load(open(spec_path))
    eps = []
    for rd in run_dir.split(","):  # several runs may be pooled: "runs/a,runs/b"
        eps += [e for e in load_episodes(f"{rd}/episodes.jsonl") if "error" not in e]
    cells = defaultdict(list)
    for e in eps:
        for key in ((e["agent"], e["faults"], e["policy"]), (e["agent"], e["faults"]), (e["agent"],)):
            cells[key].append(e["model_cost_usd"])
    plan = Counter()
    cost = Counter()
    scaled = {}
    for c in expand(spec):
        agent, pol = make_agent(c.agent).label, parent(make_policy(c.policy).label)
        if agent.startswith("scripted"):  # no API calls
            plan[agent] += 1
            continue
        for key in ((agent, c.fault_label, pol), (agent, c.fault_label), (agent,)):
            if cells.get(key):
                unit = float(np.mean(cells[key]))
                break
        else:
            if agent not in scaled:
                scaled[agent] = price_ratio_fallback(agent, cells)
            unit = scaled[agent]
        provider = agent.split(":")[0]
        plan[agent] += 1
        cost[provider] += unit
    print(f"{sum(plan.values())} episodes")
    for a, n in sorted(plan.items()):
        print(f"  {a}: {n}")
    total = sum(cost.values())
    for p, v in sorted(cost.items()):
        print(f"  {p}: ${v:.2f} expected, fund ${v * (1 + headroom):.2f} with {headroom:.0%} headroom")
    print(f"  total: ${total:.2f} expected, ${total * (1 + headroom):.2f} with headroom")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
