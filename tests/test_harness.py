"""Behavioural tests for the mechanisms the experiments depend on.

Run with:  python3 -m unittest discover -s tests -v
"""
import json
import os
import tempfile
import unittest

from abh.controlplane import ToolCall
from abh.agents.openai_agent import OpenAIAgent, _conf as openai_conf, _openai_tool
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


class TestOpenAIAdapter(unittest.TestCase):
    def test_translates_tool_schema_to_function(self):
        schema = {"name": "book", "description": "Book it", "input_schema": {
            "type": "object", "properties": {"confidence": {"type": "number"}},
            "required": ["confidence"], "additionalProperties": False,
        }}
        tool = _openai_tool(schema)
        self.assertEqual(tool["type"], "function")
        self.assertEqual(tool["parameters"], schema["input_schema"])
        self.assertNotIn("strict", tool)

    def test_extracts_confidence(self):
        self.assertEqual(openai_conf({"confidence": 0.75}), 0.75)
        self.assertIsNone(openai_conf({"confidence": "unknown"}))

    def test_known_model_uses_pricing_defaults(self):
        agent = OpenAIAgent(model="gpt-5.4")
        self.assertEqual((agent.input_price, agent.cache_read_price, agent.output_price),
                         (2.50, 0.25, 15.00))


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


class TestCompoundFaults(unittest.TestCase):
    INCIDENT = dict(title="x", severity="SEV2", service="checkout-api", summary="s")
    NO_KEYS = {"type": "scripted", "profile": "strong", "use_idempotency_keys": 0.0}

    def tool(self, sc, name):
        return next(t for t in sc.tools if t.name == name)

    def run_cfg(self, scenario, policy, agent, faults):
        fs = [FaultSpec.parse(f) for f in faults]
        return run_episode(EpisodeConfig(scenario, policy, agent, [f.to_dict() for f in fs],
                                         "+".join(f.type.value for f in fs)))

    def test_both_faults_recorded_on_one_call(self):
        sc, w, rt, inj = runtime_for("devops/base", "none", ["timeout_after_execution", "delayed_visibility"])
        out = rt.execute(self.tool(sc, "create_incident"), self.INCIDENT, "c1")
        self.assertEqual(out.state, ExecutionState.EXECUTION_UNKNOWN)
        self.assertEqual(sorted(f.type.value for f in inj.injected),
                         ["delayed_visibility", "timeout_after_execution"])
        self.assertTrue(all(f.committed for f in inj.injected))
        self.assertEqual(w.scan("incidents"), [])                    # committed but not yet visible
        self.assertEqual(len(w.scan("incidents", visible=False)), 1)

    def test_check_then_retry_defeated_without_keys(self):
        # The agent checks state after the timeout, sees nothing (not visible yet), and retries.
        r = self.run_cfg("devops/base", "P1", self.NO_KEYS, ["timeout_after_execution", "delayed_visibility"])
        self.assertEqual(r["outcome"], "harm")
        self.assertFalse(r["invariants"]["no_duplicate_pages"])

    def test_semantic_runtime_prevents_duplicate(self):
        r = self.run_cfg("devops/base", "P6", self.NO_KEYS, ["timeout_after_execution", "delayed_visibility"])
        self.assertTrue(r["success"])
        self.assertEqual(r["duplicate_effects"], 0)
        self.assertEqual(r["failures_exposed_to_agent"], 0)

    def test_timeout_masks_partial_commit(self):
        sc, w, rt, _ = runtime_for("travel/base", "none", ["partial_mutation", "timeout_after_execution"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertEqual(out.error_kind, "timeout")                    # the partial failure is hidden
        kinds = [r["kind"] for r in w.scan("reservations", visible=False)]
        self.assertEqual(kinds, ["flight"])

    def test_semantic_runtime_compensates_hidden_partial(self):
        sc, w, rt, _ = runtime_for("travel/base", "semantic", ["partial_mutation", "timeout_after_execution"])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertTrue(out.resolved)
        self.assertIn("compensate_unknown_partial", out.runtime_actions)
        self.assertEqual(w.duplicate_effects(), 0)
        active = w.scan("reservations", visible=False, where=lambda r: r["status"] != "cancelled")
        self.assertEqual(sorted(r["kind"] for r in active), ["flight", "hotel"])

    def test_compensation_spares_completed_but_invisible_work(self):
        # Full commit hidden by delayed visibility + timeout: compensation must not cancel it.
        sc, w, rt, _ = runtime_for("travel/base", "semantic", [
            "timeout_after_execution", {"type": "delayed_visibility", "params": {"delay_ms": 600000}}])
        out = rt.execute(self.tool(sc, "book_trip"), TRIP, "c1")
        self.assertTrue(out.resolved)
        self.assertEqual(w.compensated_effects(), 0)
        self.assertEqual(w.duplicate_effects(), 0)

    def test_invalid_compounds_rejected(self):
        for bad in (["timeout_after_execution", "malformed_response"],
                    ["transient_failure", "rate_limited"],
                    ["timeout_before_execution", "duplicate_execution"],
                    ["timeout_after_execution", "timeout_after_execution"]):
            with self.assertRaises(ValueError, msg=bad):
                self.run_cfg("travel/base", "P1", "scripted", bad)

    def test_non_overlapping_same_type_allowed(self):
        r = self.run_cfg("devops/base", "P6", "scripted", [
            "transient_failure", {"type": "transient_failure", "target": "@write", "on_call": 3}])
        self.assertEqual(len(r["faults_injected"]), 1)  # the second never triggers: the call succeeds on retry 2

    def test_experiment_expansion_rejects_bad_compound(self):
        spec = {"scenarios": ["travel/base"], "policies": ["P1"], "seeds": 1,
                "fault_conditions": [["timeout_after_execution", "partial_response"]]}
        with self.assertRaises(ValueError):
            list(expand(spec))


class TestScenarioInputTolerance(unittest.TestCase):
    """Reasonable spellings an LLM uses must behave like the canonical ones (found in live runs)."""

    def setup(self, sid):
        sc = make_scenario(sid)
        w = World(SimClock())
        sc.build_world(w)
        return sc, w, {t.name: t for t in sc.tools}

    def test_internal_email_addresses_are_directory_ids(self):
        sc, w, tools = self.setup("scheduling/base")
        full = ["alice@corp.example", "bob@corp.example", "carol@corp.example"]
        ctx = __import__("abh.tools", fromlist=["InvocationContext"]).InvocationContext("c1")
        slots = tools["find_free_slots"].execute(w, {"attendees": full, "duration_min": 30}, ctx)["slots"]
        self.assertEqual(slots[0], "2026-11-12T12:00")
        args = {"title": "Platform leads sync", "attendees": full, "start": slots[0], "duration_min": 30}
        self.assertTrue(sc.delegation.check("create_meeting", args, w).permitted)
        self.assertTrue(sc.oracle.action_correct("create_meeting", args, w)[0])

    def test_external_address_still_needs_approval(self):
        sc, w, _ = self.setup("scheduling/authority")
        args = {"attendees": ["alice@corp.example", "pat@vendorco.com"]}
        self.assertFalse(sc.delegation.check("create_meeting", args, w).permitted)

    def test_city_aliases(self):
        sc, w, tools = self.setup("travel/base")
        ctx = __import__("abh.tools", fromlist=["InvocationContext"]).InvocationContext("c1")
        for city in ("NYC", "New York", "new york city", "Manhattan"):
            r = tools["search_hotels"].execute(w, {"city": city, "checkin": "2026-11-12", "nights": 2}, ctx)
            self.assertEqual(len(r["hotels"]), 3, city)


class TestHiddenKeys(unittest.TestCase):
    HIDE = {"name": "P1", "expose_keys": False}

    def schemas(self, policy):
        from abh.controlplane import ControlPlane
        from abh.policies import make_policy
        sc = make_scenario("devops/base")
        cp = ControlPlane(sc, make_policy(policy), None, None, None, None, None)
        return {t["name"]: t["input_schema"]["properties"] for t in cp.tool_schemas()}

    def test_schema_hides_key(self):
        self.assertIn("idempotency_key", self.schemas("P1")["create_incident"])
        self.assertNotIn("idempotency_key", self.schemas(self.HIDE)["create_incident"])

    def test_label_distinguishes_condition(self):
        from abh.policies import make_policy
        self.assertEqual(make_policy(self.HIDE).label, "P1[expose_keys=False]")

    def run_cfg(self, policy, agent, faults):
        fs = [FaultSpec.parse(f) for f in faults]
        return run_episode(EpisodeConfig("devops/base", policy, agent, [f.to_dict() for f in fs],
                                         "+".join(f.type.value for f in fs)))

    def test_agent_supplied_key_ignored_when_hidden(self):
        # A key-happy agent can't protect itself when the platform doesn't offer keys.
        agent = {"type": "scripted", "profile": "strong", "use_idempotency_keys": 1.0}
        faults = ["timeout_after_execution", "delayed_visibility"]
        self.assertTrue(self.run_cfg("P1", agent, faults)["success"])
        r = self.run_cfg(self.HIDE, agent, faults)
        self.assertGreater(r["duplicate_effects"], 0)

    def test_semantic_runtime_keys_unaffected(self):
        r = self.run_cfg({"name": "P6", "expose_keys": False}, "scripted",
                         ["timeout_after_execution", "delayed_visibility"])
        self.assertTrue(r["success"])
        self.assertEqual(r["duplicate_effects"], 0)


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
