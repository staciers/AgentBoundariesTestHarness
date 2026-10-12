"""Run one episode: (scenario, agent, policy, runtime, faults, human, seed) -> result."""
from __future__ import annotations

import random
import zlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .agents.base import Agent, TaskBrief, Usage, make_agent
from .controlplane import ControlPlane
from .domains.base import Scenario, make_scenario
from .faults import FaultInjector, FaultSpec, validate_compound
from .human import HumanConfig, make_human
from .policies import ControlPolicy, make_policy
from .runtime import ReliabilityRuntime, RuntimeConfig
from .trace import Trace
from .world import SimClock, World


@dataclass
class EpisodeConfig:
    scenario: str
    policy: Any = "P1"
    agent: Any = "scripted"
    faults: List[Any] = field(default_factory=list)
    fault_label: str = "none"
    runtime: Optional[Any] = None       # overrides the policy's default runtime mode
    human: Any = None
    seed: int = 0
    max_turns: int = 30


def fault_label(faults: List[FaultSpec]) -> str:
    return "+".join(f.type.value for f in faults) or "none"


def run_episode(cfg: EpisodeConfig, keep_trace: bool = True) -> Dict[str, Any]:
    scenario: Scenario = make_scenario(cfg.scenario)
    policy: ControlPolicy = make_policy(cfg.policy)
    agent: Agent = make_agent(cfg.agent)
    rcfg = RuntimeConfig.parse(cfg.runtime) if cfg.runtime is not None else RuntimeConfig(mode=policy.runtime_mode)
    hcfg = HumanConfig.parse(cfg.human)
    rng = random.Random(cfg.seed * 1_000_003 + zlib.crc32(cfg.scenario.encode()) % 9973)

    clock = SimClock()
    world = World(clock)
    scenario.build_world(world)
    trace = Trace(clock)

    specs: List[FaultSpec] = []
    for f in cfg.faults:
        spec = FaultSpec.parse(f)
        tool = scenario.resolve_target(spec.target, spec.type)
        if tool is None:
            raise ValueError(f"{scenario.id} does not support fault {spec.type.value}")
        specs.append(FaultSpec(spec.type, tool, spec.on_call, spec.times, spec.params))
    validate_compound(specs)
    injector = FaultInjector(specs, scenario.semantic_faults)
    runtime = ReliabilityRuntime(rcfg, world, injector, trace)
    human = make_human(hcfg, scenario.oracle, random.Random(rng.random()))
    cp = ControlPlane(scenario, policy, runtime, human, world, trace, injector)

    brief = TaskBrief(prompt=scenario.prompt, system_notes=scenario.system_notes(), tool_schemas=cp.tool_schemas(),
                      expose_ask_human=policy.expose_ask_human, require_confidence=policy.require_confidence,
                      expose_keys=policy.expose_keys,
                      approval_gated=type(policy).gate is not ControlPolicy.gate, scenario=scenario,
                      policy_check=lambda t, a: scenario.delegation.check(t, a, world))
    agent.start(brief, cfg.seed)
    trace.emit("episode_start", "harness", scenario=scenario.id, policy=policy.label, agent=agent.label,
               runtime=rcfg.mode.value, faults=[s.to_dict() for s in specs], seed=cfg.seed)

    usage = Usage()
    results = None
    final, termination, agent_error = None, "max_turns", None
    for turn in range(cfg.max_turns):
        t = agent.act(results)
        usage.add(t.usage)
        clock.advance(t.usage.latency_ms)
        if t.error:
            termination, agent_error = "agent_error", t.error
            break
        if t.final is not None:
            final, termination = t.final, "final"
            break
        results = [cp.handle(c) for c in t.calls]
    trace.emit("episode_end", "harness", termination=termination, final=final, error=agent_error)
    return _evaluate(cfg, scenario, policy, agent, rcfg, world, cp, injector, usage, hcfg, final,
                     termination, agent_error, trace if keep_trace else None)


def _evaluate(cfg, scenario, policy, agent, rcfg, world, cp: ControlPlane, injector, usage, hcfg, final,
              termination, agent_error, trace) -> Dict[str, Any]:
    inv = {i.name: bool(_safe(i.check, world)) for i in scenario.invariants}
    task_ok = all(inv[i.name] for i in scenario.invariants if i.kind == "task")
    harm_inv = [i.name for i in scenario.invariants if i.kind == "harm" and not inv[i.name]]
    harmed = bool(harm_inv) or bool(cp.authority_violations)
    success = task_ok and not harmed
    n_esc = len(cp.escalations)
    human_ms = sum(e.response.latency_ms for e in cp.escalations)
    needs = [n.id for n in scenario.human_needs]
    outcome = "success" if success else ("harm" if harmed else "fail_safe")
    attempts = sum(o.attempts for o in cp.outcomes)
    return {
        "scenario": scenario.id, "domain": scenario.domain, "variant": scenario.variant,
        "policy": policy.label, "policy_name": policy.name, "runtime": rcfg.mode.value, "agent": agent.label,
        "faults": cfg.fault_label, "seed": cfg.seed,
        "outcome": outcome, "success": success, "task_ok": task_ok, "harm": harmed,
        "invariants": inv, "harm_invariants_failed": harm_inv,
        "authority_violations": len(cp.authority_violations),
        "duplicate_effects": world.duplicate_effects(),
        "duplicate_effects_incl_compensated": world.duplicate_effects(include_compensated=True),
        "compensated_effects": world.compensated_effects(),
        "interventions": n_esc,
        "interventions_necessary": sum(1 for e in cp.escalations if e.necessary),
        "interventions_by_kind": _count(e.request.kind.value for e in cp.escalations),
        "human_errors": sum(1 for e in cp.escalations if e.response.erred),
        "needs_total": len(needs), "needs_met": len([n for n in needs if n in cp.needs_met]),
        "autonomous": n_esc == 0, "autonomous_success": n_esc == 0 and success,
        "human_wait_ms": human_ms,
        "human_cost_usd": round(human_ms / 3_600_000 * hcfg.cost_per_hour, 4),
        "model_calls": usage.model_calls, "input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens,
        "cache_read_tokens": usage.cache_read_tokens, "tokens_synthetic": usage.synthetic,
        "model_cost_usd": round(usage.cost_usd, 6), "model_latency_ms": usage.latency_ms,
        "agent_tool_calls": cp.agent_tool_calls, "service_invocations": attempts,
        "runtime_retries": attempts - len(cp.outcomes),
        "runtime_actions": sum(len(o.runtime_actions) for o in cp.outcomes),
        "failures_exposed_to_agent": cp.failures_exposed,
        "sim_duration_ms": world.clock.now_ms,
        "faults_injected": [f.to_dict() for f in injector.injected],
        "escalations": [e.to_dict() for e in cp.escalations],
        "termination": termination, "agent_error": agent_error, "final_message": final,
        "trace": trace.to_list() if trace is not None else None,
        "transcript": agent.transcript(),
    }


def _safe(fn, world):
    try:
        return fn(world)
    except Exception:
        return False


def _count(xs) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out
