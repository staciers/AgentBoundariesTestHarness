"""Behavioural tests for the mechanisms the experiments depend on.

Run with:  python3 -m unittest discover -s tests -v
"""
import json
import os
import tempfile
import unittest

from abh.controlplane import ToolCall
from abh.domains.base import list_scenarios, make_scenario
from abh.episode import EpisodeConfig, run_episode
from abh.experiment import expand, run_experiment
from abh.metrics import load_episodes
from abh.faults import FaultInjector, FaultSpec, FaultType
from abh.runtime import ReliabilityRuntime, RuntimeConfig, RuntimeMode
from abh.semantics import ExecutionState
from abh.trace import Trace
from abh.world import SimClock, World


def ep(scenario, policy="P1", agent="naive", faults=(), runtime=None, seed=0, human=None):
    fs = [FaultSpec.parse(f) for f in faults]
    return run_episode(EpisodeConfig(scenario, policy, {"type": "scripted", "profile": agent},
                                     [f.to_dict() for f in fs], "+".join(f.type.value for f in fs) or "none",
                                     runtime, human, seed))


def runtime_for(scenario_id, mode, faults):
    sc = make_scenario(scenario_id)
    w = World(SimClock())
    sc.build_world(w)
    specs = []
    for f in faults:
        s = FaultSpec.parse(f)
        specs.append(FaultSpec(s.type, sc.resolve_target(s.target, s.type), s.on_call, s.times, s.params))
    inj = FaultInjector(specs, sc.semantic_faults)
    rt = ReliabilityRuntime(RuntimeConfig(mode=RuntimeMode(mode)), w, inj, Trace(w.clock))
    return sc, w, rt, inj


TRIP = dict(flight_id="F100", hotel_id="H1", traveler="Dana Lee", checkin="2026-11-12", nights=2)


class TestWorld(unittest.TestCase):
    def test_delayed_visibility(self):
        w = World(SimClock())
        w.begin_capture()
        w.put("t", "k", {"v": 1})
        w.delay_visibility(w.end_capture(), 5000)
        self.assertIsNone(w.get("t", "k"))
        self.assertEqual(w.get("t", "k", visible=False), {"v": 1})
        w.clock.advance(5000)
        self.assertEqual(w.get("t", "k"), {"v": 1})


class TestFaultsAndRuntime(unittest.TestCase):
    def tool(self, sc, name):
        return next(t for t in sc.tools if t.name == name)

    def test_timeout_after_execution_commits(self):
        sc, w, rt, inj = runtime_for("travel/base", "none", ["timeout_after_execution"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertEqual(out.state, ExecutionState.EXECUTION_UNKNOWN)
        self.assertTrue(inj.injected[0].committed)
        self.assertEqual(len(w.active_effects("charge")), 2)

    def test_naive_retry_duplicates_but_semantic_does_not(self):
        sc, w, rt, _ = runtime_for("travel/base", "naive_retry", ["timeout_after_execution"])
        rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertGreater(w.duplicate_effects(), 0)
        sc, w, rt, _ = runtime_for("travel/base", "semantic", ["timeout_after_execution"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertTrue(out.resolved)
        self.assertEqual(w.duplicate_effects(), 0)
        self.assertIn("reconciled_executed", out.runtime_actions)

    def test_duplicate_execution_deduped_by_key(self):
        sc, w, rt, _ = runtime_for("devops/base", "none", ["duplicate_execution"])
        rt.execute(self.tool(sc, "create_incident"), dict(title="x", severity="SEV2", service="checkout-api",
                                                          summary="s"), "c1")
        self.assertEqual(len(w.scan("incidents", visible=False)), 2)
        sc, w, rt, _ = runtime_for("devops/base", "semantic", ["duplicate_execution"])
        rt.execute(self.tool(sc, "create_incident"), dict(title="x", severity="SEV2", service="checkout-api",
                                                          summary="s"), "c1")
        self.assertEqual(len(w.scan("incidents", visible=False)), 1)

    def test_delayed_visibility_verified_without_duplicate(self):
        # Writes stay invisible past the verification window: no retry, no duplicate.
        sc, w, rt, _ = runtime_for("travel/base", "semantic", [
            {"type": "delayed_visibility", "params": {"delay_ms": 60000}},
        ])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertTrue(out.resolved)
        self.assertEqual(w.duplicate_effects(), 0)

    def test_partial_mutation_compensated(self):
        sc, w, rt, _ = runtime_for("travel/base", "semantic", ["partial_mutation"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertTrue(out.resolved)
        self.assertIn("compensate_partial", out.runtime_actions)
        self.assertEqual(w.duplicate_effects(), 0)
        active = w.scan("reservations", visible=False, where=lambda r: r["status"] != "cancelled")
        self.assertEqual(sorted(r["kind"] for r in active), ["flight", "hotel"])

    def test_semantic_failure_not_retried(self):
        sc, w, rt, inj = runtime_for("travel/base", "semantic", ["precondition_changed"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertEqual(out.state, ExecutionState.SEMANTIC_FAILURE)
        self.assertEqual(out.attempts, 1)

    def test_persistent_unavailable_classified_semantic(self):
        sc, w, rt, _ = runtime_for("travel/base", "semantic", ["persistent_unavailable"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertEqual(out.failure_class.value, "semantic")
        self.assertEqual(out.state, ExecutionState.NOT_EXECUTED)


class TestPolicies(unittest.TestCase):
    def test_p1_naive_duplicates_on_timeout(self):
        r = ep("travel/base", "P1", "naive", ["timeout_after_execution"])
        self.assertEqual(r["outcome"], "harm")
        self.assertGreater(r["duplicate_effects"], 0)

    def test_p6_absorbs_execution_faults(self):
        for f in ["timeout_after_execution", "duplicate_execution", "malformed_response", "partial_response",
                  "transient_failure", "rate_limited", "timeout_before_execution", "delayed_visibility",
                  "partial_mutation"]:
            r = ep("travel/base", "P6", "naive", [f])
            self.assertTrue(r["success"], f)
            self.assertEqual(r["failures_exposed_to_agent"], 0, f)
            self.assertEqual(r["interventions"], 0, f)

    def test_authority_requires_human_in_p6(self):
        r = ep("travel/authority", "P6", "naive")
        self.assertTrue(r["success"])
        self.assertEqual(r["needs_met"], r["needs_total"])
        self.assertTrue(any(e["trigger"].startswith("authority") for e in r["escalations"]))

    def test_p2_escalates_every_write(self):
        r = ep("travel/base", "P2", "strong")
        self.assertEqual(r["interventions"], 1)
        self.assertEqual(r["interventions_necessary"], 0)

    def test_oracle_precision(self):
        for s in list_scenarios():
            r = ep(s, "ORACLE", "strong")
            for e in r["escalations"]:
                self.assertTrue(e["necessary"], (s, e["trigger"]))

    def test_ask_human_only_when_exposed(self):
        r = ep("travel/base", "P1", "strong")
        self.assertFalse(any(e["kind"] == "clarification" for e in r["escalations"]))


class TestDeterminismAndRunner(unittest.TestCase):
    def test_deterministic(self):
        a = ep("commerce/ambiguous", "P5", "careful", ["timeout_after_execution"], seed=3)
        b = ep("commerce/ambiguous", "P5", "careful", ["timeout_after_execution"], seed=3)
        for k in ("outcome", "interventions", "sim_duration_ms", "duplicate_effects"):
            self.assertEqual(a[k], b[k])

    def test_every_supported_fault_runs(self):
        for s in list_scenarios():
            sc = make_scenario(s)
            for ft in FaultType:
                if sc.supports(ft):
                    r = ep(s, "P6", "careful", [ft.value])
                    self.assertIn(r["outcome"], ("success", "harm", "fail_safe"))

    def test_runner_resume(self):
        spec = {"name": "t", "scenarios": ["travel/base"], "policies": ["P1", "P6"],
                "agents": [{"type": "scripted", "profile": "naive"}], "fault_conditions": ["none"], "seeds": 2}
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(spec, d)
            path = os.path.join(out, "episodes.jsonl")
            self.assertEqual(len(load_episodes(path)), 4)
            run_experiment(spec, d, resume=out)
            self.assertEqual(len(load_episodes(path)), 4)
            self.assertTrue(os.path.exists(os.path.join(out, "report.md")))


if __name__ == "__main__":
    unittest.main()
