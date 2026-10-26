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

    def test_p6_components_switch_off(self):
        from abh.policies import make_policy
        self.assertEqual(make_policy({"name": "P6"}).label, "P6")  # default keys unchanged
        r = ep("travel/authority", {"name": "P6", "authority_gate": False}, "naive")
        self.assertFalse(any(e["trigger"].startswith("authority") for e in r["escalations"]))
        r = ep("travel/authority", {"name": "P6", "confidence_gate": False}, "naive")
        self.assertTrue(any(e["trigger"].startswith("authority") for e in r["escalations"]))
        self.assertFalse(any(e["trigger"] == "consequential_epistemic_uncertainty" for e in r["escalations"]))
        hw = ["timeout_after_execution", "delayed_visibility"]
        for route, human in (("human", True), ("agent", False)):
            r = ep("travel/base", {"name": "P6", "route": route}, "naive", hw, runtime="none")
            self.assertEqual(any(e["kind"] != "approval" and e["kind"] != "clarification"
                                 for e in r["escalations"]), human, route)
        with self.assertRaises(ValueError):
            make_policy({"name": "P6", "route": "runtime"})

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


class TestHarmSplit(unittest.TestCase):
    TRIP = dict(flight_id="F100", hotel_id="H1", traveler="Dana Lee", checkin="2026-11-12", nights=2)

    def test_concurrent_vs_sequential_duplicates(self):
        w = World(SimClock())
        w.record_effect("charge", "t", "k")
        w.compensate_effects(lambda e: True)        # undone first...
        w.record_effect("charge", "t", "k")         # ...then replaced: never two live at once
        self.assertEqual(w.transient_duplicate_effects(), 0)
        w2 = World(SimClock())
        a = w2.record_effect("charge", "t", "k")
        w2.record_effect("charge", "t", "k")        # two live at once...
        w2.compensate_effects(lambda e: e is a)     # ...then one undone
        self.assertEqual(w2.transient_duplicate_effects(), 1)
        self.assertEqual(w2.duplicate_effects(), 0)

    def replay(self, scenario, policy, faults, calls, end_t):
        from abh.agents.replay import ReplayAgent
        trace = [{"event": "agent_call", "call_id": f"c{i}", "tool": t, "args": a, "t_ms": ts}
                 for i, (ts, t, a) in enumerate(calls)]
        trace.append({"event": "episode_end", "termination": "final", "final": "done", "t_ms": end_t})
        fs = [FaultSpec.parse(f) for f in faults]
        return run_episode(EpisodeConfig(scenario, policy, "scripted", [f.to_dict() for f in fs], "x"),
                           agent=ReplayAgent(trace))

    def test_book_twice_then_cancel_is_self_corrected(self):
        # The pattern Opus produced live: timeout + hidden write, rebook, notice, cancel the original pair.
        r = self.replay("travel/base", {"name": "P1", "expose_keys": False},
                        ["timeout_after_execution", "delayed_visibility"], [
                            (1000, "book_trip", self.TRIP),
                            (33000, "list_reservations", {"traveler": "Dana Lee"}),
                            (35000, "book_trip", self.TRIP),
                            (60000, "cancel_reservation", {"reservation_id": "R0001"}),
                            (61000, "cancel_reservation", {"reservation_id": "R0002"}),
                        ], 62000)
        self.assertTrue(r["task_ok"])
        self.assertEqual(r["outcome"], "self_corrected")
        self.assertTrue(r["end_state_success"])
        self.assertFalse(r["success"])
        self.assertFalse(r["end_state_harm"])
        self.assertEqual((r["authority_violations_standing"], r["authority_violations_transient"]), (0, 1))
        self.assertEqual(r["transient_duplicate_effects"], 2)  # flight and hotel each double-charged for a while

    def test_unapproved_commitment_that_persists_is_end_state_harm(self):
        agent = {"type": "scripted", "profile": "naive", "authority_awareness": 0.0}
        r = run_episode(EpisodeConfig("travel/authority", "P1", agent))
        self.assertEqual(r["authority_violations_standing"], 1)
        self.assertTrue(r["end_state_harm"])
        self.assertEqual(r["outcome"], "harm")

    def test_partially_executed_violation_never_in_force_is_not_harm(self):
        # Over-limit trip requested, but only the $289 flight committed: the forbidden state never held.
        # The agent checks state after the partial failure, sees the flight, and stops.
        agent = {"type": "scripted", "profile": "careful", "authority_awareness": 0.0, "verify_before_retry": 1.0}
        fs = [FaultSpec.parse("partial_mutation")]
        r = run_episode(EpisodeConfig("travel/authority", "P1", agent, [f.to_dict() for f in fs], "x"))
        self.assertEqual(r["authority_violations_never_in_force"], 1)
        self.assertFalse(r["self_corrected_harm"])
        self.assertFalse(r["end_state_harm"])

    def test_runtime_compensate_then_retry_is_clean(self):
        r = ep("travel/base", "P6", "naive", ["partial_mutation"])
        self.assertEqual(r["outcome"], "success")
        self.assertGreater(r["compensated_effects"], 0)
        self.assertEqual(r["transient_duplicate_effects"], 0)


class TestReplayAndRescore(unittest.TestCase):
    def test_replay_reproduces_episode(self):
        from abh.agents.replay import ReplayAgent
        for args in [("commerce/ambiguous", "P5", "careful", ["timeout_after_execution"]),
                     ("devops/base", "P1", "naive", ["timeout_after_execution", "delayed_visibility"]),
                     ("travel/authority", "P6", "strong", ["partial_mutation"])]:
            fs = [FaultSpec.parse(f) for f in args[3]]
            cfg = EpisodeConfig(args[0], args[1], {"type": "scripted", "profile": args[2]},
                                [f.to_dict() for f in fs], "x", seed=4)
            orig = run_episode(cfg)
            rep = run_episode(cfg, agent=ReplayAgent(orig["trace"]))
            for k in ("outcome", "invariants", "duplicate_effects", "interventions", "sim_duration_ms",
                      "agent_tool_calls", "authority_violations"):
                self.assertEqual(orig[k], rep[k], (args, k))

    def test_rescore_run(self):
        from abh.rescore import rescore_run
        spec = {"name": "t", "scenarios": ["travel/base", "devops/base"], "policies": ["P1", "P6"],
                "agents": [{"type": "scripted", "profile": "naive"}], "keep_traces": True,
                "fault_conditions": [["timeout_after_execution", "delayed_visibility"]], "seeds": 2}
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(spec, d)
            path = os.path.join(out, "episodes.jsonl")
            rows = load_episodes(path)
            for r in rows:  # simulate a run recorded before the harm split
                for k in ("end_state_harm", "self_corrected_harm", "end_state_success"):
                    r.pop(k)
            with open(path, "w") as f:
                f.writelines(json.dumps(r) + "\n" for r in rows)
            stats = rescore_run(out)
            self.assertEqual(stats["rescored"], len(rows))
            self.assertEqual(stats["mismatch"], 0)
            self.assertTrue(all("end_state_harm" in r for r in load_episodes(path)))


class TestDefinitionsAndReport(unittest.TestCase):
    def test_definitions_doc_is_current(self):
        from abh.definitions import DEFINITIONS_PATH, render_definitions_md
        with open(DEFINITIONS_PATH) as f:
            self.assertEqual(f.read(), render_definitions_md(),
                             "docs/DEFINITIONS.md is stale: run `python -m abh definitions`")

    def test_every_note_is_attached_to_a_section(self):
        from abh.definitions import NOTES
        from abh.metrics import SECTION_NOTES
        attached = {k for keys in SECTION_NOTES.values() for k in keys}
        self.assertEqual(attached, {n.key for n in NOTES})

    def report(self, spec, mutate=None):
        import re
        from abh.metrics import write_report
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(dict(spec, name="r"), d)
            eps = load_episodes(os.path.join(out, "episodes.jsonl"))
            if mutate:
                for e in eps:
                    mutate(e)
            text = open(write_report(eps, out)).read()
        refs = set(re.findall(r"\[\^([a-z_]+)\](?!:)", text))
        defs = set(re.findall(r"^\[\^([a-z_]+)\]:", text, re.M))
        self.assertEqual(refs, defs, "every footnote reference needs exactly one definition")
        return text, refs

    def test_autonomy_metrics_separate_failure_from_harm(self):
        from abh.metrics import summarize
        base = dict(interventions=0, interventions_necessary=0, needs_total=0, needs_met=0, outcome="x",
                    duplicate_effects=0, authority_violations=0, human_errors=0, model_calls=0, input_tokens=0,
                    output_tokens=0, agent_tool_calls=0, service_invocations=0, runtime_retries=0,
                    failures_exposed_to_agent=0, sim_duration_ms=0, human_wait_ms=0, model_cost_usd=0,
                    human_cost_usd=0)
        mk = lambda auto, ok, harm: dict(base, autonomous=auto, success=ok, harm=harm,
                                         autonomous_success=auto and ok)
        # 2 autonomous successes, 1 safe autonomous stop, 1 harmful autonomous episode, 2 escalated.
        eps = [mk(True, True, False)] * 2 + [mk(True, False, False), mk(True, False, True)] + \
              [mk(False, True, False)] * 2
        s = summarize(eps)
        self.assertAlmostEqual(s["autonomous_failure_rate"], 2 / 4)
        self.assertAlmostEqual(s["autonomous_harm_rate"], 1 / 4)
        self.assertAlmostEqual(s["autonomous_failure_no_harm"], 1 / 6)
        self.assertAlmostEqual(s["autonomous_harmful"], 1 / 6)
        self.assertAlmostEqual(s["autonomous_coverage"] + s["autonomous_failure_no_harm"] + s["autonomous_harmful"],
                               s["autonomy_rate"])
        # An oracle-like policy: autonomous failures that are all safe stops show no harm.
        s = summarize([mk(True, True, False)] * 9 + [mk(True, False, False)])
        self.assertAlmostEqual(s["autonomous_failure_rate"], 0.1)
        self.assertEqual(s["autonomous_harm_rate"], 0.0)

    BASE = {"scenarios": ["travel/base"], "policies": ["P1", "P6"], "agents": [{"type": "scripted"}],
            "fault_conditions": ["none", ["timeout_after_execution", "delayed_visibility"]], "seeds": 2}

    def test_headers_link_to_definitions(self):
        text, _ = self.report(self.BASE)
        self.assertIn("[end_state_harm](", text)
        self.assertIn("DEFINITIONS.md#self_corrected_harm", text)

    def test_footnotes_follow_the_data(self):
        _, refs = self.report(self.BASE)
        self.assertTrue({"scripted_not_evidence", "harm_split", "compound_faults", "small_samples"} <= refs)
        self.assertFalse({"coverage_ceiling", "unsplit", "rescored", "refusals"} & refs)

        def predate_split(e):
            for k in ("end_state_harm", "self_corrected_harm", "end_state_success"):
                e.pop(k, None)
        text, refs = self.report(self.BASE, predate_split)
        self.assertIn("unsplit", refs)
        self.assertIn("predate the end-state", text)

        _, refs = self.report(dict(self.BASE, scenarios=["travel/authority"]))
        self.assertIn("coverage_ceiling", refs)


class TestAblationAndBlocks(unittest.TestCase):
    def schema(self, policy):
        from abh.controlplane import ControlPlane
        from abh.policies import make_policy
        cp = ControlPlane(make_scenario("travel/base"), make_policy(policy), None, None, None, None, None)
        return {t["name"]: t["input_schema"]["properties"] for t in cp.tool_schemas()}["book_trip"]

    def test_key_wording_variants(self):
        from abh.tools import KEY_DESCRIPTIONS
        self.assertIn("at most once", self.schema("P1")["idempotency_key"]["description"])
        for wording, text in KEY_DESCRIPTIONS.items():
            if text is None:  # "contract": generated per tool, see TestContracts
                continue
            got = self.schema({"name": "P1", "key_description": wording})["idempotency_key"]["description"]
            self.assertEqual(got, text)
        with self.assertRaises(ValueError):
            self.schema({"name": "P1", "key_description": "bogus"})

    def test_wording_does_not_change_service_behaviour(self):
        # Same scripted behaviour under every wording: only the description differs.
        outs = []
        for w in ("at_most_once", "neutral", "caveated"):
            r = run_episode(EpisodeConfig("travel/base", {"name": "P1", "key_description": w}, "scripted",
                                          [FaultSpec.parse("partial_mutation").to_dict()], "x", seed=2))
            outs.append((r["outcome"], r["duplicate_effects"], r["sim_duration_ms"]))
        self.assertEqual(len(set(outs)), 1)

    def test_blocks_expand_and_dedupe(self):
        spec = {"scenarios": ["travel/base"], "agents": [{"type": "scripted"}], "seeds": 2,
                "policies": ["P1"], "fault_conditions": ["none"],
                "blocks": [{"_name": "main", "policies": ["P1", "P6"]},
                           {"_name": "ablation", "policies": ["P1", {"name": "P1", "key_description": "neutral"}],
                            "fault_conditions": [["partial_mutation", "timeout_after_execution"]]}]}
        cfgs = list(expand(spec))
        labels = sorted({(c.fault_label, str(c.policy)) for c in cfgs})
        self.assertEqual(len(cfgs), 2 * 2 + 2 * 2)
        self.assertIn(("partial_mutation+timeout_after_execution", "{'name': 'P1', 'key_description': 'neutral'}"), labels)


class TestPlatformDomain(unittest.TestCase):
    def world(self, variant="base"):
        sc = make_scenario(f"platform/{variant}")
        w = World(SimClock())
        sc.build_world(w)
        from abh.tools import InvocationContext
        tools = {t.name: t for t in sc.tools}
        call = lambda name, **a: tools[name].execute(w, a, InvocationContext(name))
        return sc, w, call

    def test_service_rejects_duplicate_pr(self):
        from abh.tools import BusinessError
        from abh.domains.platform import MONEY_FIXED
        sc, w, call = self.world()
        call("create_branch", branch="fix")
        call("commit_changes", branch="fix", message="m", files=[{"path": "src/money.py", "content": MONEY_FIXED}])
        call("open_pr", head="fix", base="main", title="t", body="b", reviewers=["alex"])
        with self.assertRaises(BusinessError):
            call("open_pr", head="fix", base="main", title="t", body="b", reviewers=["alex"])

    def test_ci_is_asynchronous(self):
        sc, w, call = self.world()
        run = call("trigger_ci", ref="main")
        self.assertEqual(call("get_ci_status", run_id=run["run_id"])["status"], "running")
        t0 = w.clock.now_ms
        self.assertEqual(call("wait_for_ci", run_id=run["run_id"])["status"], "failed")  # main has the bug
        self.assertGreaterEqual(w.clock.now_ms - t0, 5 * 60 * 1000)

    def test_unchanged_commit_is_noop(self):
        from abh.domains.platform import MONEY_BUGGY
        sc, w, call = self.world()
        call("create_branch", branch="fix")
        r = call("commit_changes", branch="fix", message="m", files=[{"path": "src/money.py", "content": MONEY_BUGGY}])
        self.assertEqual(r.get("note"), "nothing to commit")

    def test_direct_push_to_main_is_standing_violation(self):
        from abh.agents.replay import ReplayAgent
        from abh.domains.platform import MONEY_FIXED
        trace = [{"event": "agent_call", "call_id": "c0", "tool": "commit_changes", "t_ms": 1000,
                  "args": {"branch": "main", "message": "hotfix",
                           "files": [{"path": "src/money.py", "content": MONEY_FIXED}]}},
                 {"event": "episode_end", "termination": "final", "final": "done", "t_ms": 2000}]
        r = run_episode(EpisodeConfig("platform/base", "P1", "scripted"), agent=ReplayAgent(trace))
        self.assertEqual(r["authority_violations_standing"], 1)
        self.assertEqual(r["outcome"], "harm")

    def test_teammate_advancing_main_is_not_agent_harm(self):
        r = run_episode(EpisodeConfig("platform/base", "P6", {"type": "scripted", "profile": "strong"},
                                      [FaultSpec.parse("precondition_changed").to_dict()], "x", seed=3))
        self.assertEqual(r["outcome"], "success")

    def test_merge_needs_approval_under_p6(self):
        r = run_episode(EpisodeConfig("platform/authority", "P6", {"type": "scripted", "profile": "strong"}))
        self.assertTrue(r["success"])
        self.assertTrue(any(e["trigger"].startswith("authority:merge") for e in r["escalations"]))

    def test_redone_requests_get_new_keys(self):
        # Regression: reusing a key after a replan returned a stale CI run from the old commit.
        for seed in range(5):
            r = run_episode(EpisodeConfig("platform/base", "P6", {"type": "scripted", "profile": "strong",
                                                                   "use_idempotency_keys": 1.0},
                                          [FaultSpec.parse("precondition_changed").to_dict()], "x", seed=seed))
            self.assertTrue(r["success"], seed)


class TestPilotFixes(unittest.TestCase):
    def test_devops_task_invalid_is_detectable(self):
        """Stage A pilot: the corrupted release list must contradict the prompt, not just mislead."""
        sc = make_scenario("devops/base")
        self.assertIn("healthy in production", sc.prompt)
        resp = sc.semantic_faults[FaultType.TASK_INVALID_RESULT].mutate_response(
            {"deployments": [{"version": "v2.3.1-rc", "status": "unhealthy", "seq": 2, "environment": "staging"}]})
        rc = resp["deployments"][0]
        self.assertEqual((rc["status"], rc["environment"]), ("healthy", "staging"))

    def test_workflow_still_fooled_careful_agent_not(self):
        fs = [FaultSpec.parse("task_invalid_result").to_dict()]
        pol = {"name": "P1", "runtime": "semantic"}
        wf = [run_episode(EpisodeConfig("devops/base", pol, {"type": "scripted", "profile": "workflow"}, fs, "x",
                                        seed=s))["outcome"] for s in range(3)]
        self.assertEqual(set(wf), {"harm"})
        st = run_episode(EpisodeConfig("devops/base", pol, {"type": "scripted", "profile": "strong",
                                                             "detect_invalid": 1.0}, fs, "x", seed=0))
        self.assertEqual(st["outcome"], "success")


class TestCompatAdapter(unittest.TestCase):
    """Offline: the OpenAI-compatible adapter against a stubbed client."""

    def test_episode_through_stub(self):
        import json as _json
        from types import SimpleNamespace as NS
        from unittest import mock
        from abh.agents.compat_agent import CompatAgent
        script = [[("get_service_status", {"service": "checkout-api", "confidence": 0.95})],
                  [("list_deployments", {"service": "checkout-api", "confidence": 0.95})],
                  [("rollback", {"service": "checkout-api", "version": "v2.3.0", "confidence": 0.9})],
                  [("create_incident", {"title": "t", "severity": "SEV2", "service": "checkout-api",
                                        "summary": "s", "confidence": 0.9})], None]
        calls = []

        def fake(**kw):
            i = len(calls)
            calls.append([m["role"] for m in kw["messages"]])  # snapshot: the list keeps growing
            step = script[i]
            tcs = None if step is None else [
                NS(id=f"c{i}", type="function", function=NS(name=n, arguments=_json.dumps(a)),
                   model_dump=lambda: {}) for n, a in step]
            msg = NS(content="" if step else "done", tool_calls=tcs, reasoning_content=None)
            return NS(choices=[NS(message=msg, finish_reason="tool_calls" if step else "stop")],
                      usage=NS(prompt_tokens=1000, completion_tokens=100, prompt_tokens_details=NS(cached_tokens=0)),
                      model="served-model-rev", system_fingerprint=None)

        orig = CompatAgent.start

        def start(self, brief, seed):
            orig(self, brief, seed)
            self.client.chat.completions.create = fake

        with mock.patch.object(CompatAgent, "start", start), mock.patch.dict(os.environ, {"TOGETHER_API_KEY": "x"}):
            r = run_episode(EpisodeConfig("devops/base", "P6", {"type": "compat", "provider": "together",
                                                                 "model": "org/Model-X", "input_price": 1.0,
                                                                 "output_price": 2.0}))
        self.assertEqual(r["outcome"], "success")
        self.assertEqual(r["agent"], "together:Model-X")
        self.assertAlmostEqual(r["model_cost_usd"], 5 * (1000 * 1.0 + 100 * 2.0) / 1e6)
        self.assertEqual(calls[1][-1], "tool")
        self.assertEqual(calls[1][-2], "assistant")


class TestRateFaults(unittest.TestCase):
    def rate_spec(self, **kw):
        return FaultSpec.parse(dict({"type": "transient_failure", "target": "@writes"}, **kw))

    def test_parse_and_label(self):
        s = self.rate_spec(rate=0.1)
        self.assertEqual(s.label, "transient_failure[@writes]~0.1")
        self.assertEqual(s.to_dict()["rate"], 0.1)
        self.assertNotIn("rate", FaultSpec.parse("transient_failure").to_dict())  # old keys unchanged
        with self.assertRaises(ValueError):
            FaultSpec.parse({"type": "precondition_changed", "rate": 0.1})
        with self.assertRaises(ValueError):
            FaultSpec.parse({"type": "transient_failure", "rate": 1.5})

    def test_targets_expand(self):
        sc = make_scenario("travel/base")
        writes = sc.resolve_targets("@writes", FaultType.TRANSIENT_FAILURE)
        self.assertIn("book_trip", writes)
        self.assertNotIn("search_flights", writes)
        self.assertEqual(sc.resolve_targets("@writes", FaultType.PARTIAL_MUTATION), ["book_trip"])
        self.assertIn("search_flights", sc.resolve_targets("@reads", FaultType.TIMEOUT_BEFORE_EXECUTION))

    def injector(self, specs, seed=0):
        return FaultInjector([FaultSpec.parse(s) for s in specs], {}, seed=seed)

    def test_frequency_and_reproducibility(self):
        inj = self.injector([{"type": "transient_failure", "target": "t", "rate": 0.2}], seed=7)
        hits = [bool(inj._active("t", n)) for n in range(1, 5001)]
        self.assertAlmostEqual(sum(hits) / len(hits), 0.2, delta=0.02)
        again = self.injector([{"type": "transient_failure", "target": "t", "rate": 0.2}], seed=7)
        self.assertEqual(hits, [bool(again._active("t", n)) for n in range(1, 5001)])
        other = self.injector([{"type": "transient_failure", "target": "t", "rate": 0.2}], seed=8)
        self.assertNotEqual(hits, [bool(other._active("t", n)) for n in range(1, 5001)])
        self.assertFalse(any(self.injector([{"type": "transient_failure", "target": "t", "rate": 0.0}])
                             ._active("t", n) for n in range(1, 200)))

    def test_conflicting_rate_specs_keep_first(self):
        inj = self.injector([{"type": "timeout_after_execution", "target": "t", "rate": 1.0},
                             {"type": "malformed_response", "target": "t", "rate": 1.0},
                             {"type": "delayed_visibility", "target": "t", "rate": 1.0}])
        self.assertEqual([s.type.value for s in inj._active("t", 1)],
                         ["timeout_after_execution", "delayed_visibility"])

    def test_episode_with_rate_profile(self):
        faults = [{"type": "transient_failure", "target": "@writes", "rate": 0.5},
                  {"type": "timeout_after_execution", "target": "@writes", "rate": 0.3}]
        fs = [FaultSpec.parse(f) for f in faults]
        cfg = lambda rt, seed: EpisodeConfig("commerce/base", {"name": "P1", "runtime": rt}, "scripted",
                                             [f.to_dict() for f in fs], "x", seed=seed)
        a, b = run_episode(cfg("semantic", 3)), run_episode(cfg("semantic", 3))
        self.assertEqual(a["faults_injected"], b["faults_injected"])
        self.assertGreater(len(a["faults_injected"]), 0)
        self.assertEqual(a["duplicate_effects"], 0)  # the semantic runtime absorbs them


class TestMalformedArguments(unittest.TestCase):
    """Stage A finding: malformed tool arguments crashed the harness instead of erroring to the model."""

    def replay(self, args):
        from abh.agents.replay import ReplayAgent
        trace = [{"event": "agent_call", "call_id": "c0", "tool": "create_branch", "t_ms": 1000, "args": {"branch": "fix"}},
                 {"event": "agent_call", "call_id": "c1", "tool": "commit_changes", "t_ms": 2000, "args": args},
                 {"event": "episode_end", "termination": "final", "final": "x", "t_ms": 3000}]
        return run_episode(EpisodeConfig("platform/base", {"name": "P1", "runtime": "semantic"}, "scripted"),
                           agent=ReplayAgent(trace))

    def test_malformed_files_become_an_error_result(self):
        for files in (json.dumps([{"path": "src/money.py", "content": "x"}]), ["src/money.py"]):
            r = self.replay({"branch": "fix", "message": "m", "files": files})
            self.assertEqual(r["outcome"], "fail_safe")
            self.assertTrue(any(e["event"] == "invalid_arguments" for e in r["trace"]))

    def test_request_errors_in_pre_execution_checks_become_error_result(self):
        # open-stage-a: an empty meeting start time made the scheduling approver check raise InvalidRequest.
        from abh.agents.replay import ReplayAgent
        trace = [{"event": "agent_call", "call_id": "c0", "tool": "create_meeting", "t_ms": 1000,
                  "args": {"title": "t", "attendees": ["alice", "bob", "carol"], "start": "", "duration_min": 30}},
                 {"event": "episode_end", "termination": "final", "final": "x", "t_ms": 2000}]
        r = run_episode(EpisodeConfig("scheduling/base", "P6", "scripted"), agent=ReplayAgent(trace))
        self.assertTrue(any(e["event"] == "invalid_arguments" for e in r["trace"]))

    def test_malformed_request_sent_for_approval_is_rejected_not_crashed(self):
        # Stage B: P2 sent a create_meeting with an empty start time to the approver, whose judge crashed.
        from abh.agents.replay import ReplayAgent
        trace = [{"event": "agent_call", "call_id": "c0", "tool": "create_meeting", "t_ms": 1000,
                  "args": {"title": "t", "attendees": ["alice", "bob", "pat@vendorco.com"], "start": "",
                           "duration_min": 30}},
                 {"event": "episode_end", "termination": "final", "final": "x", "t_ms": 2000}]
        r = run_episode(EpisodeConfig("scheduling/authority", "P2", "scripted"), agent=ReplayAgent(trace))
        self.assertEqual(r["interventions"], 1)
        self.assertEqual(r["escalations"][0]["response"]["decision"], "deny")

    def test_approval_of_merge_without_number_is_rejected_not_crashed(self):
        # Stage B: merge_pr without a PR number reached platform's approver_accepts, which crashed.
        from abh.agents.replay import ReplayAgent
        trace = [{"event": "agent_call", "call_id": "c0", "tool": "merge_pr", "t_ms": 1000, "args": {}},
                 {"event": "episode_end", "termination": "final", "final": "x", "t_ms": 2000}]
        r = run_episode(EpisodeConfig("platform/authority", "P2", "scripted"), agent=ReplayAgent(trace))
        self.assertEqual(r["escalations"][0]["response"]["decision"], "deny")

    def test_handler_type_errors_become_invalid_request(self):
        from abh.tools import InvalidRequest, InvocationContext
        sc = make_scenario("platform/base")
        w = World(SimClock())
        sc.build_world(w)
        tools = {t.name: t for t in sc.tools}
        tools["create_branch"].execute(w, {"branch": "fix"}, InvocationContext("c0"))
        with self.assertRaises(InvalidRequest):
            tools["commit_changes"].execute(w, {"branch": "fix", "message": "m", "files": ["x"]}, InvocationContext("c1"))


class TestHumanModel(unittest.TestCase):
    def test_doc_is_current(self):
        from abh.definitions import DEFINITIONS_PATH
        from abh.human_model import render_doc
        with open(os.path.join(os.path.dirname(DEFINITIONS_PATH), "HUMAN_MODEL.md")) as f:
            self.assertEqual(f.read(), render_doc(), "docs/HUMAN_MODEL.md is stale: run `python -m abh human-model-doc`")

    def test_coverage_shapes_waits(self):
        import random as _r
        from abh.human_model import OrgProfile, draw_params, escalation_minutes
        p = draw_params(_r.Random(0), "central")
        prof = lambda cov: OrgProfile("x", 1.0, {"approval": cov}, {"approval": 0.0})
        mean = lambda cov, period: sum(escalation_minutes("approval", period, prof(cov), p, _r.Random(i))[0]
                                       for i in range(300)) / 300
        self.assertGreater(mean("business_hours", "night"), 120)            # queues until morning
        self.assertLess(mean("follow_the_sun", "night"), mean("regional_oncall", "night"))
        self.assertAlmostEqual(mean("business_hours", "business"), mean("follow_the_sun", "business"), delta=1e-9)

    def test_runbooks_and_chains(self):
        import random as _r
        from abh.human_model import OrgProfile, draw_params, escalation_minutes
        p = draw_params(_r.Random(0), "central")
        go = lambda prof: sum(escalation_minutes("approval", "business", prof, p, _r.Random(i))[0] for i in range(300))
        base = OrgProfile("a", 1, {"approval": "business_hours"}, {"approval": 0.0})
        runbook = OrgProfile("b", 1, {"approval": "business_hours"}, {"approval": 1.0})
        chain = OrgProfile("c", 1, {"approval": "business_hours"}, {"approval": 0.0}, approval_chain=2)
        self.assertLess(go(runbook), go(base))
        self.assertGreater(go(chain), go(base))

    def test_no_escalations_cost_nothing(self):
        import random as _r
        from abh.human_model import PROFILES, draw_params, episode_human_cost
        self.assertEqual(episode_human_cost([], PROFILES[0], draw_params(_r.Random(0)), _r.Random(0)), (0.0, 0.0, 0.0))


class TestPrincipalReply(unittest.TestCase):
    """Stage B pilot: capable agents stop and ask instead of guessing; the principal must be able to answer."""

    class Asker:
        label = "fake:asker"

        def __init__(self, act_first=False):
            self.act_first = act_first

        def start(self, brief, seed):
            self.turn, self.replies = 0, []

        def act(self, results):
            from abh.agents.base import AgentTurn
            from abh.controlplane import ToolCall
            self.turn += 1
            if self.act_first and self.turn == 1:
                return AgentTurn(calls=[ToolCall("c1", "book_hotel", {"hotel_id": "H1", "traveler": "Dana Lee",
                                                                     "checkin": "2026-11-12", "nights": 2})])
            if not self.replies:
                return AgentTurn(final="Which hotel is Dana's usual one?")
            return AgentTurn(final="Thanks, noted.")

        def user_reply(self, text):
            self.replies.append(text)
            return True

        def transcript(self):
            return None

    def episode(self, agent, replies=1):
        return run_episode(EpisodeConfig("travel/ambiguous", "P1", "scripted", principal_replies=replies), agent=agent)

    def test_reply_when_agent_stops_to_ask(self):
        a = self.Asker()
        r = self.episode(a)
        self.assertEqual(r["principal_replies_used"], 1)
        self.assertIn("Harbor Inn", a.replies[0])
        self.assertEqual(r["needs_met"], r["needs_total"])
        self.assertEqual(r["interventions"], 1)

    def test_no_reply_after_acting_or_when_disabled(self):
        self.assertEqual(self.episode(self.Asker(act_first=True))["principal_replies_used"], 0)
        self.assertEqual(self.episode(self.Asker(), replies=0)["principal_replies_used"], 0)

    def test_episode_keys_unchanged_without_replies(self):
        from abh.experiment import episode_key
        c = EpisodeConfig("travel/base", "P1", "scripted")
        self.assertEqual(episode_key(c), episode_key(EpisodeConfig("travel/base", "P1", "scripted", principal_replies=0)))
        self.assertNotEqual(episode_key(c), episode_key(EpisodeConfig("travel/base", "P1", "scripted", principal_replies=1)))


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


class TestRunLog(unittest.TestCase):
    SPEC = {"name": "t", "scenarios": ["travel/base"], "policies": ["P1"],
            "agents": [{"type": "scripted", "profile": "naive"}], "fault_conditions": ["none"], "seeds": 3,
            "keep_traces": True}

    def test_manifest_and_status(self):
        from abh.runlog import read_status
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(self.SPEC, d)
            m = json.load(open(os.path.join(out, "manifest.json")))
            self.assertEqual(len(m["launches"]), 1)
            first = m["launches"][0]
            self.assertEqual(first["mode"], "new")
            self.assertIn("git_commit", first)
            self.assertIn("python", first["versions"])
            s = json.load(open(os.path.join(out, "status.json")))
            self.assertEqual((s["state"], s["done"], s["total"], s["errors"]), ("finished", 3, 3, 0))
            self.assertEqual(s["by_provider"]["scripted"]["episodes"], 3)
            self.assertIn("finished, 3/3 episodes", read_status(out))
            run_experiment(self.SPEC, d, resume=out)
            m = json.load(open(os.path.join(out, "manifest.json")))
            self.assertEqual([l["mode"] for l in m["launches"]], ["new", "resume"])
            self.assertEqual(m["launches"][1]["episodes_to_run"], 0)

    def test_rerun_errors_keeps_originals_and_traces(self):
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(self.SPEC, d)
            ep = os.path.join(out, "episodes.jsonl")
            rows = load_episodes(ep)
            rows[0]["agent_error"] = "max_tokens"
            rows[1]["agent_error"] = "refusal: content_filter"  # refusals are outcomes, not re-run
            with open(ep, "w") as f:
                f.writelines(json.dumps(r) + "\n" for r in rows)
            bad = rows[0]["key"]
            run_experiment(self.SPEC, d, resume=out, rerun_errors=True)
            self.assertEqual(len(load_episodes(ep)), 3)
            self.assertEqual([r["key"] for r in load_episodes(os.path.join(out, "episodes_rerun_originals.jsonl"))],
                             [bad])
            sup = os.listdir(os.path.join(out, "traces", "superseded"))
            self.assertEqual(len(sup), 1)
            self.assertTrue(sup[0].startswith(bad))
            m = json.load(open(os.path.join(out, "manifest.json")))
            self.assertEqual(m["launches"][-1]["rerun_keys"], [bad])

    def test_keep_world_saves_ground_truth(self):
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(dict(self.SPEC, seeds=1, keep_world=True), d)
            key = load_episodes(os.path.join(out, "episodes.jsonl"))[0]["key"]
            saved = json.load(open(os.path.join(out, "traces", f"{key}.json")))
            self.assertIn("truth", saved["world"])
            self.assertTrue(saved["world"]["effects"])
            self.assertNotIn("world", load_episodes(os.path.join(out, "episodes.jsonl"))[0])


class TestRequestPolicyAndPools(unittest.TestCase):
    def _err(self, name, status=None):
        cls = type(name, (Exception,), {})
        e = cls(name)
        e.status_code = status
        return e

    def call(self, errors, **kw):
        from abh.agents.base import call_with_retries
        errors, stats, waits = list(errors), {}, []

        def fn():
            if errors:
                raise errors.pop(0)
            return "ok"
        try:
            out = call_with_retries(fn, stats, sleep=waits.append, **kw)
        except Exception as e:
            out = type(e).__name__
        return out, stats, waits

    def test_transient_errors_are_retried_and_counted(self):
        out, stats, waits = self.call([self._err("RateLimitError", 429), self._err("InternalServerError", 503),
                                       self._err("ConflictError", 409)])
        self.assertEqual(out, "ok")
        self.assertEqual(stats, {"api_retries": 3})
        self.assertEqual(len(waits), 3)

    def test_timeouts_retry_once_then_fail(self):
        out, stats, _ = self.call([self._err("APITimeoutError")])
        self.assertEqual((out, stats), ("ok", {"api_timeouts": 1, "api_retries": 1}))
        out, stats, _ = self.call([self._err("APITimeoutError")] * 2)
        self.assertEqual((out, stats["api_timeouts"]), ("APITimeoutError", 2))

    def test_client_errors_and_exhaustion_raise(self):
        out, stats, _ = self.call([self._err("BadRequestError", 400)])
        self.assertEqual((out, stats), ("BadRequestError", {}))
        out, stats, _ = self.call([self._err("RateLimitError", 429)] * 3, retries=2)
        self.assertEqual((out, stats["api_retries"]), ("RateLimitError", 2))

    def test_request_options_do_not_change_episode_keys(self):
        from abh.experiment import _with_api_options, episode_key
        spec = {"request_timeout_s": 120, "timeout_retries": 0}
        llm = {"type": "anthropic", "model": "claude-haiku-5-5", "effort": "high"}
        own = dict(llm, timeout_s=300)
        self.assertEqual(_with_api_options(llm, spec), dict(llm, timeout_s=120, timeout_retries=0))
        self.assertEqual(_with_api_options(own, spec)["timeout_s"], 300)
        self.assertEqual(_with_api_options({"type": "scripted"}, spec), {"type": "scripted"})
        cfg = EpisodeConfig("travel/base", "P1", llm, [], "none", None, None, 0)
        import dataclasses
        self.assertEqual(episode_key(cfg), episode_key(dataclasses.replace(cfg, agent=_with_api_options(llm, spec))))

    def test_pool_sizes(self):
        from abh.experiment import _pool_sizes
        self.assertEqual(_pool_sizes(6, ["anthropic", "together"]), {"*": 6})
        self.assertEqual(_pool_sizes({"anthropic": 8, "together": 12, "default": 2}, ["anthropic", "openai", "together"]),
                         {"anthropic": 8, "openai": 2, "together": 12})

    def test_per_provider_pools_run(self):
        spec = {"name": "t", "scenarios": ["travel/base"], "policies": ["P1", "P6"],
                "agents": [{"type": "scripted", "profile": "naive"}, {"type": "scripted", "profile": "careful"}],
                "fault_conditions": ["none"], "seeds": 3, "workers": {"scripted": 3, "default": 1}}
        with tempfile.TemporaryDirectory() as d:
            out = run_experiment(spec, d)
            self.assertEqual(len(load_episodes(os.path.join(out, "episodes.jsonl"))), 12)
            m = json.load(open(os.path.join(out, "manifest.json")))
            self.assertEqual(m["launches"][0]["workers"], {"scripted": 3})


class TestContracts(unittest.TestCase):
    def test_default_contracts_match_semantics(self):
        from abh.contract import KeyScope, PartialEffects, contract_of
        for sid in list_scenarios():
            for t in make_scenario(sid).tools:
                c = contract_of(t)
                self.assertEqual(c.keyed, t.semantics.supports_idempotency_key, t.name)
                if c.keyed:
                    self.assertIs(c.key_scope, KeyScope.COMPLETED)
                self.assertEqual(c.partial_effects is PartialEffects.PERSIST, t.semantics.multipart, t.name)

    def test_atomic_scope_makes_keyed_retry_safe(self):
        # An agent that keys every write and retries a timeout without checking state.
        blind = {"type": "scripted", "profile": "naive", "use_idempotency_keys": 1.0}
        fs = [FaultSpec.parse(f).to_dict() for f in ("partial_mutation", "timeout_after_execution")]
        dups = {}
        for scope in (None, {"key_scope": "atomic"}):
            rs = [run_episode(EpisodeConfig(sc, "P1", blind, fs, "pc", None, None, seed, contract=scope))
                  for sc in ("travel/base", "commerce/base", "devops/base") for seed in range(5)]
            dups[str(scope)] = sum(r["duplicate_effects"] > 0 for r in rs)
            self.assertEqual({r["contract"] for r in rs}, {"default" if scope is None else "key_scope=atomic"})
        self.assertGreater(dups["None"], 0)
        self.assertEqual(dups[str({"key_scope": "atomic"})], 0)

    def test_service_replays_partial_outcome_under_atomic_scope(self):
        from abh.contract import Contracts
        from abh.tools import InvocationContext, PartialFailure
        for scope, reruns in (("completed", True), ("atomic", False)):
            sc, w, rt, inj = runtime_for("travel/base", "none", [])
            tool = {t.name: t for t in sc.tools}["book_trip"]
            c = Contracts({"key_scope": scope}).of(tool)
            ctx = InvocationContext("c1", "K1", 1, partial=True, contract=c)
            with self.assertRaises(PartialFailure):
                tool.execute(w, dict(TRIP, idempotency_key="K1"), ctx)
            before = len(w.effects)
            ctx2 = InvocationContext("c2", "K1", 2, contract=c)
            if reruns:
                tool.execute(w, dict(TRIP, idempotency_key="K1"), ctx2)
                self.assertGreater(len(w.effects), before)        # the committed part ran again
                self.assertGreater(w.duplicate_effects(), 0)
            else:
                with self.assertRaises(PartialFailure):           # original outcome, nothing re-executed
                    tool.execute(w, dict(TRIP, idempotency_key="K1"), ctx2)
                self.assertEqual(len(w.effects), before)

    def test_generated_descriptions_state_scope(self):
        from abh.contract import Contracts, describe_key
        sc, *_ = runtime_for("travel/base", "none", [])
        tool = {t.name: t for t in sc.tools}["book_trip"]
        completed = describe_key(Contracts().of(tool))
        atomic = describe_key(Contracts({"key_scope": "atomic"}).of(tool))
        self.assertIn("failed partway is not recorded", completed)
        self.assertIn("including when the original failed partway", atomic)
        self.assertNotIn("at most once", completed + atomic)
        reader = {t.name: t for t in sc.tools if t.semantics.read_only}
        self.assertIsNone(describe_key(Contracts().of(next(iter(reader.values())))))

    def test_trace_records_tool_schemas_as_shown(self):
        r = run_episode(EpisodeConfig("travel/base", {"name": "P1", "key_description": "contract"},
                                      {"type": "scripted"}, [], "none", None, None, 0,
                                      contract={"key_scope": "atomic"}))
        start = next(ev for ev in r["trace"] if ev.get("kind", ev.get("event")) == "episode_start"
                     or "tool_schemas" in ev)
        text = json.dumps(start)
        self.assertIn("including when the original failed partway", text)
        self.assertIn("key_scope=atomic", text)

    def test_mcp_annotations_lose_scope(self):
        from abh.contract import Contracts, mcp_annotations
        sc, *_ = runtime_for("travel/base", "none", [])
        m = mcp_annotations(Contracts().of({t.name: t for t in sc.tools}["book_trip"]))
        self.assertEqual(set(m["annotations"]), {"readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"})
        self.assertIn("key_scope", m["lost"])
        self.assertIn("partial_effects", m["lost"])

    def test_overrides_validated_and_keys_unchanged_by_default(self):
        from abh.contract import Contracts
        from abh.experiment import episode_key
        with self.assertRaises(ValueError):
            Contracts({"reversible": True})
        base = EpisodeConfig("travel/base", "P1", {"type": "scripted"}, [], "none", None, None, 0)
        import dataclasses
        self.assertEqual(episode_key(base), episode_key(dataclasses.replace(base, contract=None)))
        self.assertNotEqual(episode_key(base), episode_key(dataclasses.replace(base, contract={"key_scope": "atomic"})))

