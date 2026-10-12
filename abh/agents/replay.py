"""Replays the tool calls recorded in an episode trace, at their recorded times.

The environment is deterministic given the call sequence and timing, so replaying a
trace rebuilds the episode's world exactly, without calling a model. That lets runs be
re-scored when the evaluator changes (see ``abh.rescore``).
"""
from __future__ import annotations

from typing import List, Optional

from ..controlplane import ToolCall, ToolResult
from .base import Agent, AgentTurn, TaskBrief, Usage


class ReplayAgent(Agent):
    def __init__(self, trace: List[dict], label: str = "replay"):
        self.calls = [e for e in trace if e.get("event") == "agent_call"]
        end = [e for e in trace if e.get("event") == "episode_end"]
        self.end = end[-1] if end else {}
        self.label = label

    def start(self, brief: TaskBrief, seed: int) -> None:
        if brief.clock is None:
            raise ValueError("ReplayAgent needs the simulation clock in its brief")
        self.clock = brief.clock
        self.i = 0

    def _wait_until(self, t_ms: int) -> Usage:
        # The harness advances the clock by the turn's latency before handling its calls.
        return Usage(latency_ms=max(0, int(t_ms) - self.clock.now_ms))

    def act(self, results: Optional[List[ToolResult]]) -> AgentTurn:
        if self.i < len(self.calls):
            e = self.calls[self.i]
            self.i += 1
            args = dict(e.get("args") or {})
            return AgentTurn(calls=[ToolCall(e["call_id"], e["tool"], args, e.get("confidence"))],
                             usage=self._wait_until(e["t_ms"]))
        usage = self._wait_until(self.end.get("t_ms", self.clock.now_ms))
        if self.end.get("termination") == "agent_error":
            return AgentTurn(error=self.end.get("error") or "agent_error", usage=usage)
        return AgentTurn(final=self.end.get("final") or "", usage=usage)
