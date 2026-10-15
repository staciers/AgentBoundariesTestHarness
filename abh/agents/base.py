"""Agent interface. The harness owns the loop; agents only propose actions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from ..controlplane import ToolCall, ToolResult


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    model_calls: int = 0
    latency_ms: int = 0
    cost_usd: float = 0.0
    synthetic: bool = False  # True when tokens are modelled, not measured

    def add(self, o: "Usage") -> None:
        for k in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens",
                  "model_calls", "latency_ms"):
            setattr(self, k, getattr(self, k) + getattr(o, k))
        self.cost_usd += o.cost_usd
        self.synthetic = self.synthetic or o.synthetic


@dataclass
class AgentTurn:
    calls: List[ToolCall] = field(default_factory=list)
    final: Optional[str] = None
    usage: Usage = field(default_factory=Usage)
    error: Optional[str] = None


@dataclass
class TaskBrief:
    prompt: str
    system_notes: str
    tool_schemas: List[dict]
    expose_ask_human: bool
    require_confidence: bool
    approval_gated: bool = False               # the policy may route actions to a human approver
    expose_keys: bool = True                   # tool schemas offer an idempotency_key argument
    scenario: Any = None                       # scripted agent only (reference plan)
    policy_check: Optional[Callable] = None    # scripted agent only (reads policy text)
    clock: Any = None                          # replay agent only (re-times recorded calls)


class Agent:
    label = "agent"

    def start(self, brief: TaskBrief, seed: int) -> None:
        raise NotImplementedError

    def act(self, results: Optional[List[ToolResult]]) -> AgentTurn:
        raise NotImplementedError

    def user_reply(self, text: str) -> bool:
        """Continue after a final reply with a new user message. False if unsupported."""
        return False

    def transcript(self) -> Optional[list]:
        return None


def make_agent(spec) -> Agent:
    if isinstance(spec, Agent):
        return spec
    if isinstance(spec, str):
        spec = {"type": spec}
    spec = dict(spec)
    kind = spec.pop("type")
    if kind == "scripted":
        from .scripted import ScriptedAgent
        return ScriptedAgent(**spec)
    if kind == "anthropic":
        from .anthropic_agent import AnthropicAgent
        return AnthropicAgent(**spec)
    if kind == "openai":
        from .openai_agent import OpenAIAgent
        return OpenAIAgent(**spec)
    if kind == "compat":
        from .compat_agent import CompatAgent
        return CompatAgent(**spec)
    raise ValueError(f"unknown agent type {kind!r}")
