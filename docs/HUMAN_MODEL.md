# Empirical human time-and-cost model

<!-- Generated from abh/human_model.py by `python -m abh human-model-doc`. Do not edit by hand. -->

Applied after a run (`python -m abh human-cost runs/<dir>`) to the escalations each episode recorded. It estimates **time to decision** (how long the agent waits) and **effort** (active human minutes, which drive cost) for a population of organizations. It does **not** model decision quality (whether a reviewer decides correctly); that stays with the in-episode simulated human, and public data on it is thin.

Results are Monte Carlo intervals: each draw samples every parameter uniformly within its range. A parameter labelled *assumption* has no direct empirical source; its range is deliberately wide.

## Evidence base

- **VOID** (Verica Open Incident Database, 2022: ~10,000 public incident reports, ~600 orgs): incident durations are strongly right-skewed; means and MTTR mislead. Used for the heavy-tailed (log-normal) shape.
- **PagerDuty, State of Digital Operations** (2020–2021): off-hours interruptions are common (median user ~2 a month, burned-out users ~19), and acknowledgement speed varies about 2× between the best decile and the quartile. Used for paged acknowledgement and the off-hours share.
- **Night-work performance research**: night shifts show slower, more error-prone decisions, but decision-fatigue studies are mixed, and magnitudes are uncertain and mostly from healthcare.
- **Runbooks**: no credible survey of coverage or effect was found; only vendor claims of 25–40% faster resolution. Treated as an assumption.

## Parameters

| Parameter | Low | Central | High | Source |
|---|---|---|---|---|
| `median_approval_min` | 5 | 20 | 90 | assumption: async approvals (chat, ticket) take tens of minutes; heavy tail per VOID |
| `median_clarification_min` | 3 | 15 | 60 | assumption: a question to the requester; heavy tail per VOID |
| `median_execution_state_min` | 2 | 5 | 15 | paged-incident acknowledgement (PagerDuty MTTA, best-decile teams ~2x faster than quartile) |
| `lognormal_sigma` | 0.6 | 1 | 1.4 | VOID: response and duration distributions are strongly right-skewed |
| `offhours_multiplier` | 1.2 | 1.6 | 3 | assumption; PagerDuty: off-hours interruptions are common and drive attrition |
| `sleep_wake_delay_min` | 5 | 12 | 30 | assumption: being woken by a page and getting to a terminal |
| `sleep_multiplier` | 1.2 | 1.5 | 2.5 | night-work performance literature: slower decisions (magnitude uncertain) |
| `handoff_delay_min` | 0 | 5 | 15 | assumption: follow-the-sun handoff to another region |
| `runbook_multiplier` | 0.5 | 0.75 | 0.95 | weak: vendor reports of 25-40% faster resolution; treat as assumption |
| `effort_approval_min` | 1 | 3 | 10 | assumption |
| `effort_clarification_min` | 1 | 2 | 6 | assumption |
| `effort_execution_state_min` | 5 | 12 | 30 | assumption: checking a system of record to establish what happened |
| `offhours_share` | 0.2 | 0.33 | 0.5 | assumption informed by PagerDuty off-hours interruption data |
| `night_share_of_offhours` | 0.15 | 0.3 | 0.45 | assumption |

## Organization profiles

Coverage for each kind of escalation outside business hours:

- `follow_the_sun`: another region is working, so there's only a small handoff delay.
- `regional_oncall`: someone is paged; slower off-hours, plus a wake-up delay at night.
- `business_hours`: nobody is available, so the escalation waits until the next business morning.

The weights are a default population mix, not measured shares.

| Profile | Weight | Approvals | Clarifications | Execution-state checks | Runbook coverage (appr./clar./exec.) | Approval chain | $/hour |
|---|---|---|---|---|---|---|---|
| startup | 25% | business_hours | business_hours | regional_oncall | 10% / 0% / 30% | 1 | 110 |
| mid-size | 35% | business_hours | business_hours | regional_oncall | 30% / 10% / 50% | 1 | 120 |
| global enterprise | 30% | regional_oncall | business_hours | follow_the_sun | 50% / 20% / 70% | 1 | 140 |
| regulated | 10% | business_hours | business_hours | follow_the_sun | 70% / 20% / 80% | 2 | 160 |

## Calibrating it

The ranges should be narrowed with real data: a team's own PagerDuty or incident-tool exports (time to acknowledge, by hour and by whether a runbook was linked), approval-tool logs, or the planned interactive pilot with real reviewers. Edit `PARAMS` and `PROFILES` in `abh/human_model.py`, then regenerate this file.
