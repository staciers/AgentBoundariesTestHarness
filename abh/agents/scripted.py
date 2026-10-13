"""A parameterised, non-LLM agent that follows a scenario's reference plan.

It is *not* a model of any particular LLM. Its purpose is to (a) validate the
harness end-to-end without API spend, (b) provide controllable agent competence
for sensitivity analyses (e.g. "how good must semantic recovery be before runtime
recovery stops mattering?"), and (c) serve as a reproducible baseline.

Competence knobs (probabilities) govern failure handling that LLM agents are known
to vary on: blind retry vs. verify-then-retry, idempotency-key use, replanning,
noticing task-invalid results, calibration of stated confidence, awareness of
authority rules, and propensity to ask a human.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..controlplane import ASK_HUMAN, ToolCall, ToolResult
from .base import Agent, AgentTurn, TaskBrief, Usage

PROFILES: Dict[str, Dict[str, float]] = {
    "naive": dict(max_retries=2, verify_before_retry=0.0, use_idempotency_keys=0.0, replan_skill=0.3,
                  detect_invalid=0.2, ask_on_ambiguity=0.1, authority_awareness=0.2, comply_without_ask=0.3,
                  calibration=0.2, false_low_confidence=0.10, spurious_ask=0.05),
    "careful": dict(max_retries=2, verify_before_retry=0.8, use_idempotency_keys=0.3, replan_skill=0.8,
                    detect_invalid=0.7, ask_on_ambiguity=0.6, authority_awareness=0.7, comply_without_ask=0.7,
                    calibration=0.6, false_low_confidence=0.05, spurious_ask=0.15),
    # A deterministic workflow engine, not a model of any agent: it follows the reference
    # plan exactly, retries transient errors, and never verifies, replans, switches tools,
    # notices bad results, asks humans or attaches keys. It is the "deterministic recovery"
    # baseline for H2: run it with the semantic runtime so execution recovery is handled.
    "workflow": dict(max_retries=2, verify_before_retry=0.0, use_idempotency_keys=0.0, replan_skill=0.0,
                     detect_invalid=0.0, ask_on_ambiguity=0.0, authority_awareness=0.0, comply_without_ask=0.0,
                     calibration=0.0, false_low_confidence=0.0, spurious_ask=0.0),
    "strong": dict(max_retries=2, verify_before_retry=1.0, use_idempotency_keys=0.8, replan_skill=0.95,
                   detect_invalid=0.9, ask_on_ambiguity=0.8, authority_awareness=0.9, comply_without_ask=0.9,
                   calibration=0.85, false_low_confidence=0.02, spurious_ask=0.10),
}

TRANSIENT = {"timeout", "unavailable", "rate_limited"}


@dataclass
class _Pending:
    kind: str          # main | check | ask_clarify | ask_approve
    step_idx: int
    call: ToolCall


class ScriptedAgent(Agent):
    def __init__(self, profile: str = "careful", turn_latency_ms: int = 1500, **overrides):
        self.profile = profile
        self.p = dict(PROFILES[profile])
        self.p.update(overrides)
        self.turn_latency_ms = turn_latency_ms
        self.label = f"scripted:{profile}" + ("" if not overrides else "+" + ",".join(
            f"{k}={v}" for k, v in sorted(overrides.items())))

    # ------------------------------------------------------------- lifecycle
    def start(self, brief: TaskBrief, seed: int) -> None:
        self.brief = brief
        self.s = brief.scenario
        self.rng = random.Random(seed * 7919 + 17)
        self.plan = list(self.s.plan)
        self.idx = 0
        self.mem: Dict = {}
        self.uncertain: set = set()
        self.asked: set = set()
        self.approved: set = set()
        self.retries: Dict[int, int] = {}
        self.invalid_retries: Dict[int, int] = {}
        self.keys: Dict[int, str] = {}
        self.pending: Optional[_Pending] = None
        self.final: Optional[str] = None
        self.n = 0
        self.turns = 0

    def _usage(self) -> Usage:
        self.turns += 1
        return Usage(input_tokens=1800 + 450 * self.turns, output_tokens=180, model_calls=1,
                     latency_ms=self.turn_latency_ms, synthetic=True)

    def act(self, results: Optional[List[ToolResult]]) -> AgentTurn:
        if results:
            self._absorb(results[0])
        usage = self._usage()
        if self.final is not None:
            return AgentTurn(final=self.final, usage=usage)
        call = self._next_call()
        if call is None:
            return AgentTurn(final=self.final or "Task complete.", usage=usage)
        return AgentTurn(calls=[call], usage=usage)

    # --------------------------------------------------------------- helpers
    def _id(self) -> str:
        self.n += 1
        return f"call{self.n}"

    def _chance(self, k: str) -> bool:
        return self.rng.random() < self.p[k]

    def _give_up(self, why: str) -> None:
        self.final = f"Unable to complete the task: {why}"
        self.pending = None

    def _confidence(self, step) -> Optional[float]:
        if not self.brief.require_confidence:
            return None
        if any(k in self.uncertain for k in step.uses):
            return round(self.rng.uniform(0.3, 0.55), 2) if self._chance("calibration") \
                else round(self.rng.uniform(0.8, 0.95), 2)
        if self._chance("false_low_confidence"):
            return round(self.rng.uniform(0.4, 0.6), 2)
        return round(self.rng.uniform(0.85, 0.98), 2)

    def _ask(self, kind: str, question: str, step_idx: int, tool=None, args=None) -> ToolCall:
        a = {"question": question}
        if tool:
            a.update(action_tool=tool, action_args=args)
        call = ToolCall(self._id(), ASK_HUMAN, a)
        self.pending = _Pending(kind, step_idx, call)
        return call

    # ---------------------------------------------------------- decide next
    def _next_call(self) -> Optional[ToolCall]:
        if self.pending is not None:  # a queued follow-up call
            return self.pending.call
        if self.idx >= len(self.plan):
            self.final = "Task complete."
            return None
        step = self.plan[self.idx]
        can_ask = self.brief.expose_ask_human
        for k in step.uses:
            if k not in self.mem:
                if can_ask and k not in self.asked and self._chance("ask_on_ambiguity"):
                    self.asked.add(k)
                    return self._ask("ask_clarify", f"To be sure: what should I use for '{k}'?", self.idx)
                self.mem[k] = self.s.guesses[k]
                self.uncertain.add(k)
        try:
            args = step.args(self.mem)
        except Exception as e:  # missing / garbled data from an earlier step
            if self.idx > 0 and self.invalid_retries.get(self.idx - 1, 0) < 2:
                self.invalid_retries[self.idx - 1] = self.invalid_retries.get(self.idx - 1, 0) + 1
                self.idx -= 1
                return self._next_call()
            self._give_up(f"missing information for {step.name} ({e})")
            return None

        tool = next((t for t in self.s.tools if t.name == step.tool), None)
        canon = (step.tool, repr(sorted(args.items())))
        if self.brief.policy_check and canon not in self.approved:
            auth = self.brief.policy_check(step.tool, args)
            if not auth.permitted and self._chance("authority_awareness"):
                if can_ask:
                    return self._ask("ask_approve", "This needs approval under policy: " + "; ".join(auth.reasons),
                                     self.idx, step.tool, args)
                if not self.brief.approval_gated and self._chance("comply_without_ask"):
                    self._give_up("this action requires approval I cannot obtain: " + "; ".join(auth.reasons))
                    return None
        if (can_ask and tool and not tool.semantics.read_only and canon not in self.approved
                and ("spurious", self.idx) not in self.asked and self._chance("spurious_ask")):
            self.asked.add(("spurious", self.idx))
            return self._ask("ask_approve", "Before I proceed, is this OK?", self.idx, step.tool, args)

        if tool and tool.semantics.supports_idempotency_key and self.brief.expose_keys:
            if self.idx not in self.keys and self._chance("use_idempotency_keys"):
                self.keys[self.idx] = f"agent-{step.name}-{self.n}"
            if self.idx in self.keys:
                args = dict(args, idempotency_key=self.keys[self.idx])
        call = ToolCall(self._id(), step.tool, args, self._confidence(step))
        self.pending = _Pending("main", self.idx, call)
        return call

    # ------------------------------------------------------------ absorb
    def _absorb(self, r: ToolResult) -> None:
        pend, self.pending = self.pending, None
        if pend is None:
            return
        meta = r.meta or {}
        kind = meta.get("kind", "ok")
        step = self.plan[pend.step_idx]

        if pend.kind in ("ask_clarify", "ask_approve"):
            hint = meta.get("hint") or {}
            self._learn(hint)
            if pend.kind == "ask_approve":
                if meta.get("decision") == "approve":
                    self.approved.add((pend.call.args["action_tool"],
                                       repr(sorted(pend.call.args["action_args"].items()))))
                elif not hint:
                    self._give_up("approval was denied")
            return

        if pend.kind == "check":
            if kind == "ok" and step.check and step.check[2](r.content, self.mem):
                self._advance(step, {"_reconciled": True})
            else:
                self._retry_or_fail(pend.step_idx, "action could not be confirmed")
            return

        # main call
        if kind == "denied":
            hint = meta.get("hint") or {}
            if hint:
                self._learn(hint)
                return  # redo the work that depended on the corrected assumption
            self._give_up("a human denied the action")
            return
        if kind == "human_confirmed":
            if (meta.get("hint") or {}).get("executed"):
                self._advance(step, {"_confirmed": True})
            else:
                self._retry_or_fail(pend.step_idx, "action did not execute")
            return
        if kind == "ok":
            content = r.content if isinstance(r.content, dict) else {}
            if step.valid and not step.valid(content, {**self.mem, step.save or "_": content}) \
                    and self.invalid_retries.get(pend.step_idx, 0) < 2 and self._chance("detect_invalid"):
                self.invalid_retries[pend.step_idx] = self.invalid_retries.get(pend.step_idx, 0) + 1
                return  # re-run the step
            self._advance(step, content)
            return
        if kind == "rejected" or meta.get("error_kind") in ("business_error", "invalid_request"):
            if step.on_reject and self._chance("replan_skill"):
                self.idx = next(i for i, s in enumerate(self.plan) if s.name == step.on_reject)
                self._forget_keys_from(self.idx)
                return
            self._give_up(f"{step.tool} was rejected: {r.text()[:120]}")
            return
        if kind == "unavailable":
            self._fallback_or_fail(pend.step_idx)
            return
        # error / garbled / unknown
        ek = meta.get("error_kind")
        tool = next((t for t in self.s.tools if t.name == step.tool), None)
        read_only = tool is not None and tool.semantics.read_only
        if read_only or (ek in ("unavailable", "rate_limited") and kind == "error"):
            if self.retries.get(pend.step_idx, 0) >= self.p["max_retries"] and ek in TRANSIENT:
                self._fallback_or_fail(pend.step_idx)
            else:
                self._retry_or_fail(pend.step_idx, "repeated errors")
            return
        # Ambiguous outcome of a side-effecting call (timeout, garbled, partial, unknown).
        if step.check and self._chance("verify_before_retry"):
            ctool, cargs_fn, _ = step.check
            self.pending = _Pending("check", pend.step_idx, ToolCall(self._id(), ctool, cargs_fn(self.mem)))
            return
        self._retry_or_fail(pend.step_idx, "repeated errors")

    def _learn(self, hint: Dict) -> None:
        """Adopt corrected information and replan from the first step that relied on it."""
        if not hint:
            return
        stale = set(hint) & self.uncertain
        self.mem.update(hint)
        self.uncertain -= set(hint)
        if stale:
            first = next((i for i, s in enumerate(self.plan) if set(s.uses) & stale), self.idx)
            self.idx = min(self.idx, first)
            self._forget_keys_from(self.idx)

    def _forget_keys_from(self, idx: int) -> None:
        """Steps redone after a replan or correction are new requests: don't reuse their old keys."""
        for i in [k for k in self.keys if k >= idx]:
            del self.keys[i]

    def _advance(self, step, content) -> None:
        if step.save:
            self.mem[step.save] = content
        self.idx += 1

    def _retry_or_fail(self, idx: int, why: str) -> None:
        self.retries[idx] = self.retries.get(idx, 0) + 1
        if self.retries[idx] > self.p["max_retries"]:
            self._give_up(why)

    def _fallback_or_fail(self, idx: int) -> None:
        step = self.plan[idx]
        if step.fallback and self._chance("replan_skill"):
            self.plan[idx:idx + 1] = list(step.fallback)
            self.retries.pop(idx, None)
            self.keys.pop(idx, None)
            return
        self._give_up(f"{step.tool} is unavailable")
