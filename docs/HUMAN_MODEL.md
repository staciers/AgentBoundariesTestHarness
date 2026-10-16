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

## How the outputs are computed

For each Monte Carlo draw (default 200, seed 0), every parameter above is sampled uniformly within its range. Then, for each task (episode) in the run:

1. **Organization.** A profile is chosen (by weight, for the weighted mix), and the task's arrival period is drawn: business hours with probability 1 − `offhours_share`; otherwise night with probability `night_share_of_offhours`, else evening/weekend.
2. **Each recorded escalation, in order:**
   - *decision time* = log-normal(median for its kind, `lognormal_sigma`) × `runbook_multiplier` if a runbook exists (probability = the profile's runbook coverage for that kind)
   - plus the coverage effect outside business hours: `handoff_delay_min` (follow-the-sun); × `offhours_multiplier`, or × `sleep_multiplier` + `sleep_wake_delay_min` at night (regional on-call); or the wait until 09:00 the next business day (business hours only, ~40% of off-hours arrivals fall on a weekend)
   - approvals with a chain of *n* add *n − 1* further decision times
   - *effort* = the effort parameter for its kind × log-normal(0, 0.4), × *n* for approval chains
3. **Per task:** time to decision = Σ decision times; effort = Σ efforts; **cost = effort ÷ 60 × the profile's $/hour**. A task with no escalations costs 0.
4. **Per draw and policy:** the median and p90 of time to decision across tasks, the share of tasks waiting over 60 minutes, and the **mean** effort and cost per task.

Each reported cell is the **median across draws**, with the 5th–95th percentile across draws in parentheses. Because the cost is a median of per-draw means, it is close to, but not exactly, (effort per task ÷ 60) × the mix's average hourly rate.

*Worked example (Stage B, P2, weighted mix):* 17.6 effort-minutes per task × $127.50/h (the weights' average rate: 0.25×110 + 0.35×120 + 0.30×140 + 0.10×160) ÷ 60 ≈ $37.40, against the reported $38.22 ($13.01–65.07).

## Calibrating it

The ranges should be narrowed with real data: a team's own PagerDuty or incident-tool exports (time to acknowledge, by hour and by whether a runbook was linked), approval-tool logs, or the planned interactive pilot with real reviewers. Edit `PARAMS` and `PROFILES` in `abh/human_model.py`, then regenerate this file.
