"""Empirically grounded human time-and-cost model, applied after a run.

The simulated human in `abh.human` decides (approve / deny / answer) during an episode.
This module answers a different question afterwards: *how long would those escalations
have taken, and how much human effort would they have cost, in a real organization?*
It needs only the escalations each episode recorded, so it can be applied to any run,
including old ones, at no API cost.

Two quantities are kept separate:

* **Time to decision:** how long the agent waits. It includes queueing for business hours,
  waking an on-call engineer, approval chains and decision time. It drives latency.
* **Effort:** active minutes a person spends. It drives cost.

Each escalation's time to decision depends on the organization's coverage for that kind
of request, the local time it arrives, whether a runbook exists, and the length of the
approval chain. Organizations are described by weighted `OrgProfile`s. Every parameter
is a (low, central, high) range with a source or an explicit "assumption" label, and
results are reported as Monte Carlo intervals over those ranges. See docs/HUMAN_MODEL.md.

Public evidence is good on the *shape* of human response times (heavy-tailed; VOID) and
on off-hours interruption being common (PagerDuty), but thin on runbook effects and on
decision accuracy. This model therefore covers time and cost, not decision quality.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

KINDS = ("approval", "clarification", "execution_state")

# Parameter ranges: (low, central, high, source). Minutes unless noted.
PARAMS: Dict[str, Tuple[float, float, float, str]] = {
    # Decision time when a suitable person is available and awake (log-normal medians).
    "median_approval_min": (5, 20, 90, "assumption: async approvals (chat, ticket) take tens of minutes; heavy tail per VOID"),
    "median_clarification_min": (3, 15, 60, "assumption: a question to the requester; heavy tail per VOID"),
    "median_execution_state_min": (2, 5, 15, "paged-incident acknowledgement (PagerDuty MTTA, best-decile teams ~2x faster than quartile)"),
    "lognormal_sigma": (0.6, 1.0, 1.4, "VOID: response and duration distributions are strongly right-skewed"),
    # Context multipliers and delays.
    "offhours_multiplier": (1.2, 1.6, 3.0, "assumption; PagerDuty: off-hours interruptions are common and drive attrition"),
    "sleep_wake_delay_min": (5, 12, 30, "assumption: being woken by a page and getting to a terminal"),
    "sleep_multiplier": (1.2, 1.5, 2.5, "night-work performance literature: slower decisions (magnitude uncertain)"),
    "handoff_delay_min": (0, 5, 15, "assumption: follow-the-sun handoff to another region"),
    "runbook_multiplier": (0.5, 0.75, 0.95, "weak: vendor reports of 25-40% faster resolution; treat as assumption"),
    # Effort (active minutes) per escalation.
    "effort_approval_min": (1, 3, 10, "assumption"),
    "effort_clarification_min": (1, 2, 6, "assumption"),
    "effort_execution_state_min": (5, 12, 30, "assumption: checking a system of record to establish what happened"),
    # When escalations arrive.
    "offhours_share": (0.20, 0.33, 0.50, "assumption informed by PagerDuty off-hours interruption data"),
    "night_share_of_offhours": (0.15, 0.30, 0.45, "assumption"),
}


@dataclass(frozen=True)
class OrgProfile:
    name: str
    weight: float
    # Who answers each kind of escalation outside business hours:
    #   follow_the_sun   - another region is in business hours (small handoff delay)
    #   regional_oncall  - someone is on call; slower off-hours, wake-up delay at night
    #   business_hours   - nobody; waits for the next business morning
    coverage: Dict[str, str]
    runbook_coverage: Dict[str, float]   # P(a runbook exists for the escalation), by kind
    approval_chain: int = 1              # sequential approvers for authority approvals
    cost_per_hour: float = 120.0

    def describe(self) -> str:
        cov = ", ".join(f"{k}: {v}" for k, v in self.coverage.items())
        rb = ", ".join(f"{k} {p:.0%}" for k, p in self.runbook_coverage.items())
        return f"{self.name} (weight {self.weight:.0%}; coverage {cov}; runbooks {rb}; approval chain {self.approval_chain})"


# Illustrative profiles. The weights are a default population mix, not measured shares;
# change them to match the organizations a result is meant to describe.
PROFILES: List[OrgProfile] = [
    OrgProfile("startup", 0.25,
               {"approval": "business_hours", "clarification": "business_hours", "execution_state": "regional_oncall"},
               {"approval": 0.1, "clarification": 0.0, "execution_state": 0.3}, 1, 110.0),
    OrgProfile("mid-size", 0.35,
               {"approval": "business_hours", "clarification": "business_hours", "execution_state": "regional_oncall"},
               {"approval": 0.3, "clarification": 0.1, "execution_state": 0.5}, 1, 120.0),
    OrgProfile("global enterprise", 0.30,
               {"approval": "regional_oncall", "clarification": "business_hours", "execution_state": "follow_the_sun"},
               {"approval": 0.5, "clarification": 0.2, "execution_state": 0.7}, 1, 140.0),
    OrgProfile("regulated", 0.10,
               {"approval": "business_hours", "clarification": "business_hours", "execution_state": "follow_the_sun"},
               {"approval": 0.7, "clarification": 0.2, "execution_state": 0.8}, 2, 160.0),
]


def draw_params(rng: random.Random, mode: str = "sample") -> Dict[str, float]:
    """Parameters for one Monte Carlo draw: uniform within each range, or a fixed point."""
    pick = {"low": 0, "central": 1, "high": 2}
    if mode in pick:
        return {k: v[pick[mode]] for k, v in PARAMS.items()}
    return {k: rng.uniform(v[0], v[2]) for k, v in PARAMS.items()}


def _arrival_period(rng: random.Random, p: Dict[str, float]) -> str:
    if rng.random() >= p["offhours_share"]:
        return "business"
    return "night" if rng.random() < p["night_share_of_offhours"] else "offhours"


def _minutes_to_next_morning(period: str, rng: random.Random) -> float:
    # Evening or weekend: wait until 09:00 on the next business day. Night: until 09:00.
    if period == "night":
        return rng.uniform(2 * 60, 8 * 60)        # arrives 01:00-07:00
    weekend = rng.random() < 0.4                   # weekends make up a large share of off-hours time
    return rng.uniform(13 * 60, 15 * 60) + (rng.uniform(24 * 60, 48 * 60) if weekend else 0)


def escalation_minutes(kind: str, period: str, profile: OrgProfile, p: Dict[str, float],
                       rng: random.Random) -> Tuple[float, float]:
    """Return (time to decision, effort), both in minutes, for one escalation."""
    kind = kind if kind in KINDS else "approval"
    median = p[f"median_{kind}_min"]
    t = rng.lognormvariate(math.log(median), p["lognormal_sigma"])
    if rng.random() < profile.runbook_coverage.get(kind, 0.0):
        t *= p["runbook_multiplier"]
    cov = profile.coverage.get(kind, "business_hours")
    if period != "business":
        if cov == "follow_the_sun":
            t += p["handoff_delay_min"]
        elif cov == "regional_oncall":
            t = t * (p["sleep_multiplier"] if period == "night" else p["offhours_multiplier"])
            if period == "night":
                t += p["sleep_wake_delay_min"]
        else:  # business_hours: queue until the next business morning
            t += _minutes_to_next_morning(period, rng)
    effort = p[f"effort_{kind}_min"] * rng.lognormvariate(0.0, 0.4)
    chain = profile.approval_chain if kind == "approval" else 1
    return t * chain if chain == 1 else t + sum(
        rng.lognormvariate(math.log(median), p["lognormal_sigma"]) for _ in range(chain - 1)), effort * chain


def episode_human_cost(escalations: Sequence[dict], profile: OrgProfile, p: Dict[str, float],
                       rng: random.Random) -> Tuple[float, float, float]:
    """(time to decision, effort, cost in USD) for one episode's escalations, in sequence."""
    period = _arrival_period(rng, p)
    total_t = total_e = 0.0
    for esc in escalations:
        t, e = escalation_minutes(esc.get("kind", "approval"), period, profile, p, rng)
        total_t += t
        total_e += e
        if total_t > 8 * 60 and period != "business":
            period = "business"  # long enough that later escalations land in business hours
    return total_t, total_e, total_e / 60.0 * profile.cost_per_hour


@dataclass
class CostSummary:
    policy: str
    profile: str
    tasks: int
    escalations_per_task: float
    wait_median: Tuple[float, float, float]       # minutes per task: (lo, mid, hi) across draws
    wait_p90: Tuple[float, float, float]
    delayed_over_1h: Tuple[float, float, float]   # share of tasks waiting > 60 minutes
    effort: Tuple[float, float, float]            # minutes per task
    cost: Tuple[float, float, float]              # USD per task


def _pct(xs: List[float], q: float) -> float:
    xs = sorted(xs)
    if not xs:
        return float("nan")
    i = min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))
    return xs[i]


def analyze(eps: List[dict], profiles: Optional[List[OrgProfile]] = None, draws: int = 200,
            seed: int = 0) -> List[CostSummary]:
    """Monte Carlo over parameter ranges; per policy and profile (and the weighted mix)."""
    profiles = profiles or PROFILES
    by_policy: Dict[str, List[dict]] = {}
    for e in eps:
        if "error" not in e:
            by_policy.setdefault(e["policy"], []).append(e)
    rng = random.Random(seed)
    out: List[CostSummary] = []
    targets = [(pr.name, [pr]) for pr in profiles] + [("weighted mix", profiles)]
    for policy, es in sorted(by_policy.items()):
        n_esc = sum(len(e.get("escalations") or []) for e in es) / len(es)
        for name, prs in targets:
            stats = {"med": [], "p90": [], "over": [], "eff": [], "cost": []}
            weights = [pr.weight for pr in prs]
            for _ in range(draws):
                p = draw_params(rng)
                waits, effs, costs = [], [], []
                for e in es:
                    pr = rng.choices(prs, weights=weights)[0] if len(prs) > 1 else prs[0]
                    t, ef, c = episode_human_cost(e.get("escalations") or [], pr, p, rng)
                    waits.append(t)
                    effs.append(ef)
                    costs.append(c)
                stats["med"].append(_pct(waits, 0.5))
                stats["p90"].append(_pct(waits, 0.9))
                stats["over"].append(sum(w > 60 for w in waits) / len(waits))
                stats["eff"].append(sum(effs) / len(effs))
                stats["cost"].append(sum(costs) / len(costs))
            band = lambda xs: (_pct(xs, 0.05), _pct(xs, 0.5), _pct(xs, 0.95))
            out.append(CostSummary(policy, name, len(es), n_esc, band(stats["med"]), band(stats["p90"]),
                                   band(stats["over"]), band(stats["eff"]), band(stats["cost"])))
    return out


def to_markdown(rows: List[CostSummary]) -> str:
    fmt = lambda b, f: f"{f(b[1])} ({f(b[0])}–{f(b[2])})"
    mins = lambda x: f"{x:.0f}" if x < 120 else f"{x / 60:.1f}h"
    lines = ["| Policy | Org profile | escalations / task | wait / task, median | wait, p90 | tasks waiting > 1 h | "
             "effort min / task | cost $ / task |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r.policy} | {r.profile} | {r.escalations_per_task:.2f} | {fmt(r.wait_median, mins)} | "
                     f"{fmt(r.wait_p90, mins)} | {fmt(r.delayed_over_1h, lambda x: f'{x:.0%}')} | "
                     f"{fmt(r.effort, lambda x: f'{x:.1f}')} | {fmt(r.cost, lambda x: f'{x:.2f}')} |")
    return "\n".join(lines) + "\n"


def render_doc() -> str:
    """docs/HUMAN_MODEL.md, generated from PARAMS and PROFILES so it can't drift."""
    out = ["# Empirical human time-and-cost model", "",
           "<!-- Generated from abh/human_model.py by `python -m abh human-model-doc`. Do not edit by hand. -->", "",
           "Applied after a run (`python -m abh human-cost runs/<dir>`) to the escalations each episode recorded. "
           "It estimates **time to decision** (how long the agent waits) and **effort** (active human minutes, which "
           "drive cost) for a population of organizations. It does **not** model decision quality (whether a reviewer "
           "decides correctly); that stays with the in-episode simulated human, and public data on it is thin.", "",
           "Results are Monte Carlo intervals: each draw samples every parameter uniformly within its range. A "
           "parameter labelled *assumption* has no direct empirical source; its range is deliberately wide.", "",
           "## Evidence base", "",
           "- **VOID** (Verica Open Incident Database, 2022: ~10,000 public incident reports, ~600 orgs): incident "
           "durations are strongly right-skewed; means and MTTR mislead. Used for the heavy-tailed (log-normal) shape.",
           "- **PagerDuty, State of Digital Operations** (2020–2021): off-hours interruptions are common (median "
           "user ~2 a month, burned-out users ~19), and acknowledgement speed varies about 2× between the best decile "
           "and the quartile. Used for paged acknowledgement and the off-hours share.",
           "- **Night-work performance research**: night shifts show slower, more error-prone decisions, but "
           "decision-fatigue studies are mixed, and magnitudes are uncertain and mostly from healthcare.",
           "- **Runbooks**: no credible survey of coverage or effect was found; only vendor claims of 25–40% faster "
           "resolution. Treated as an assumption.", "",
           "## Parameters", "", "| Parameter | Low | Central | High | Source |", "|---|---|---|---|---|"]
    for k, (lo, mid, hi, src) in PARAMS.items():
        out.append(f"| `{k}` | {lo:g} | {mid:g} | {hi:g} | {src} |")
    out += ["", "## Organization profiles", "",
            "Coverage for each kind of escalation outside business hours:",
            "",
            "- `follow_the_sun`: another region is working, so there's only a small handoff delay.",
            "- `regional_oncall`: someone is paged; slower off-hours, plus a wake-up delay at night.",
            "- `business_hours`: nobody is available, so the escalation waits until the next business morning.",
            "",
            "The weights are a default population mix, not measured shares.", "",
            "| Profile | Weight | Approvals | Clarifications | Execution-state checks | Runbook coverage (appr./clar./exec.) | "
            "Approval chain | $/hour |", "|---|---|---|---|---|---|---|---|"]
    for pr in PROFILES:
        rb = pr.runbook_coverage
        out.append(f"| {pr.name} | {pr.weight:.0%} | {pr.coverage['approval']} | {pr.coverage['clarification']} | "
                   f"{pr.coverage['execution_state']} | {rb['approval']:.0%} / {rb['clarification']:.0%} / "
                   f"{rb['execution_state']:.0%} | {pr.approval_chain} | {pr.cost_per_hour:.0f} |")
    out += ["", "## Calibrating it", "",
            "The ranges should be narrowed with real data: a team's own PagerDuty or incident-tool exports (time "
            "to acknowledge, by hour and by whether a runbook was linked), approval-tool logs, or the planned "
            "interactive pilot with real reviewers. Edit `PARAMS` and `PROFILES` in `abh/human_model.py`, then "
            "regenerate this file."]
    return "\n".join(out) + "\n"
