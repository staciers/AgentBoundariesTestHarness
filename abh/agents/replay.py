"""Replays the tool calls recorded in an episode trace, at their recorded times.

The environment is deterministic given the call sequence and timing, so replaying a
trace rebuilds the episode's world exactly, without calling a model. That lets runs be
re-scored when the evaluator changes (see ``abh.rescore``).

The recorded turns are rebuilt from the trace. Calls made in one turn are handled back to
back, so each starts at the time the previous event ended; a later call starts a new turn
(the gap is the model's latency). A final reply that the principal answered
(``principal_replies``) shows as a ``principal_reply`` escalation, recorded at the time of
that final turn with the reply as its question, followed by a ``principal_reply`` event;
the replay returns that final, accepts the answer in ``user_reply`` and carries on with the
calls recorded after it.
"""
from __future__ import annotations

from typing import List, Optional

from ..controlplane import ToolCall, ToolResult
from .base import Agent, AgentTurn, TaskBrief, Usage


class ReplayAgent(Agent):
    def __init__(self, trace: List[dict], label: str = "replay"):
        end = [e for e in trace if e.get("event") == "episode_end"]
        self.end = end[-1] if end else {}
        self.label = label
        # Each turn: {"t_ms", "calls"} or {"t_ms", "final", "replied"}.
        self.turns: List[dict] = []
        prev_t, open_calls = None, None
        for e in trace:
            kind = e.get("event")
            if kind == "agent_call":
                if open_calls is None or e["t_ms"] > prev_t:
                    open_calls = {"t_ms": e["t_ms"], "calls": []}
                    self.turns.append(open_calls)
                open_calls["calls"].append(e)
            elif kind == "escalation" and e.get("trigger") == "principal_reply":
                self.turns.append({"t_ms": e["t_ms"], "final": e.get("question") or "", "replied": False})
                open_calls = None
            elif kind == "principal_reply" and self.turns and "final" in self.turns[-1]:
                self.turns[-1]["replied"] = True
            prev_t = e.get("t_ms", prev_t)
        if self.turns and "final" in self.turns[-1] and not self.turns[-1]["replied"]:
            # The episode's last final was offered a reply the agent declined: it ends the episode.
            self.final_t = self.turns.pop()["t_ms"]
        else:
            self.final_t = None

    def start(self, brief: TaskBrief, seed: int) -> None:
        if brief.clock is None:
            raise ValueError("ReplayAgent needs the simulation clock in its brief")
        self.clock = brief.clock
        self.i = 0
        self.awaiting_reply = False

    def _wait_until(self, t_ms: int) -> Usage:
        # The harness advances the clock by the turn's latency before handling its calls.
        return Usage(latency_ms=max(0, int(t_ms) - self.clock.now_ms))

    def act(self, results: Optional[List[ToolResult]]) -> AgentTurn:
        self.awaiting_reply = False
        if self.i < len(self.turns):
            turn = self.turns[self.i]
            self.i += 1
            usage = self._wait_until(turn["t_ms"])
            if "final" in turn:
                self.awaiting_reply = True
                return AgentTurn(final=turn["final"], usage=usage)
            return AgentTurn(calls=[ToolCall(e["call_id"], e["tool"], dict(e.get("args") or {}), e.get("confidence"))
                                    for e in turn["calls"]], usage=usage)
        termination = self.end.get("termination")
        if termination == "max_turns":
            # Turns without calls (if any) leave no trace; idle until the harness stops the episode.
            return AgentTurn(usage=self._wait_until(self.end.get("t_ms", self.clock.now_ms)))
        t_end = self.final_t if self.final_t is not None else self.end.get("t_ms", self.clock.now_ms)
        usage = self._wait_until(t_end)
        if termination == "agent_error":
            return AgentTurn(error=self.end.get("error") or "agent_error", usage=usage)
        return AgentTurn(final=self.end.get("final") or "", usage=usage)

    def user_reply(self, text: str) -> bool:
        # Only a final that the recorded episode continued past takes the reply.
        accepted, self.awaiting_reply = self.awaiting_reply, False
        return accepted
