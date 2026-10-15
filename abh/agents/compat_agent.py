"""Open-weight models through OpenAI-compatible Chat Completions endpoints.

Hosted inference providers (Together, Fireworks, DeepInfra, OpenRouter) and first-party
open-model APIs (DeepSeek, Z.ai) expose ``/v1/chat/completions`` with OpenAI-style
function calling. This adapter speaks that protocol with the ``openai`` SDK and a
provider ``base_url``. As with the other adapters, the harness owns the loop so the
control plane mediates every tool call.

Reproducibility notes:

* Hosted models can be quantized or swapped between revisions without notice. Every
  response's ``model`` and ``system_fingerprint`` are recorded in the transcript, and
  the served model is kept on the agent so runs can be checked for silent changes.
* Prices are configuration, not defaults, because they differ by provider and change
  often. A model with no configured price is reported at $0 with a warning in its label.
* Thinking models may return ``reasoning_content``. Whether it must be sent back on
  later turns differs by provider; ``replay_reasoning`` controls it (default off).
"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional

from ..controlplane import ToolCall, ToolResult
from .base import Agent, AgentTurn, TaskBrief, Usage
from .openai_agent import ASK_NOTE, CONF_NOTE, GATED_NOTE, SYSTEM

# base_url and the environment variable holding the key. Verify base URLs against the
# provider's docs; model IDs are provider-specific and set per agent.
PROVIDERS: Dict[str, Dict[str, str]] = {
    "together": {"base_url": "https://api.together.xyz/v1", "key_env": "TOGETHER_API_KEY"},
    "fireworks": {"base_url": "https://api.fireworks.ai/inference/v1", "key_env": "FIREWORKS_API_KEY"},
    "deepinfra": {"base_url": "https://api.deepinfra.com/v1/openai", "key_env": "DEEPINFRA_API_KEY"},
    "openrouter": {"base_url": "https://openrouter.ai/api/v1", "key_env": "OPENROUTER_API_KEY"},
    "deepseek": {"base_url": "https://api.deepseek.com", "key_env": "DEEPSEEK_API_KEY"},
    "zai": {"base_url": "https://api.z.ai/api/paas/v4", "key_env": "ZAI_API_KEY"},
}


class CompatAgent(Agent):
    def __init__(self, provider: str, model: str, effort: Optional[str] = None, base_url: Optional[str] = None,
                 key_env: Optional[str] = None, input_price: float = 0.0, output_price: float = 0.0,
                 cache_read_price: Optional[float] = None, max_tokens: int = 16000,
                 temperature: Optional[float] = None, extra_body: Optional[dict] = None,
                 replay_reasoning: bool = False, max_retries: int = 4, timeout_s: float = 600.0,
                 alias: Optional[str] = None):
        preset = PROVIDERS.get(provider, {})
        self.provider = provider
        self.model = model
        self.effort = effort
        self.base_url = base_url or preset.get("base_url")
        self.key_env = key_env or preset.get("key_env")
        if not self.base_url or not self.key_env:
            raise ValueError(f"unknown provider {provider!r}: give base_url and key_env")
        self.input_price, self.output_price = input_price, output_price
        self.cache_read_price = input_price if cache_read_price is None else cache_read_price
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.extra_body = dict(extra_body or {})
        self.replay_reasoning = replay_reasoning
        self.max_retries, self.timeout_s = max_retries, timeout_s
        name = alias or model.split("/")[-1]
        self.label = f"{provider}:{name}" + (f"@{effort}" if effort else "")
        self.served_models: set = set()

    def start(self, brief: TaskBrief, seed: int) -> None:
        from openai import OpenAI
        self.client = OpenAI(base_url=self.base_url, api_key=os.environ.get(self.key_env, ""),
                             max_retries=self.max_retries, timeout=self.timeout_s)
        notes = [brief.system_notes]
        if brief.expose_ask_human:
            notes.append(ASK_NOTE)
        if brief.approval_gated:
            notes.append(GATED_NOTE)
        if brief.require_confidence:
            notes.append(CONF_NOTE)
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM.format(notes="\n\n".join(n for n in notes if n))},
            {"role": "user", "content": brief.prompt}]
        self.tools = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                        "parameters": t["input_schema"]}}
                      for t in brief.tool_schemas]
        self._log: List[dict] = []

    def _request(self) -> Any:
        kwargs: Dict[str, Any] = dict(model=self.model, messages=self.messages, tools=self.tools,
                                      max_tokens=self.max_tokens)
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        body = dict(self.extra_body)
        if self.effort:
            body.setdefault("reasoning_effort", self.effort)
        if body:
            kwargs["extra_body"] = body
        return self.client.chat.completions.create(**kwargs)

    def act(self, results: Optional[List[ToolResult]]) -> AgentTurn:
        import openai
        for r in results or []:
            self.messages.append({"role": "tool", "tool_call_id": r.call_id, "content": r.text()})
        t0 = time.time()
        try:
            resp = self._request()
        except openai.BadRequestError as e:
            return self._error("bad_request", e, t0)
        except openai.APIStatusError as e:
            return self._error(f"api_error {e.status_code}", e, t0)
        except openai.APIConnectionError as e:
            return self._error("connection_error", e, t0)
        usage = self._usage(resp, int((time.time() - t0) * 1000))
        if not resp.choices:
            return AgentTurn(error="empty_response", usage=usage)
        choice = resp.choices[0]
        msg = choice.message
        self.served_models.add(getattr(resp, "model", None))
        reasoning = getattr(msg, "reasoning_content", None)
        self._log.append({"served_model": getattr(resp, "model", None),
                          "system_fingerprint": getattr(resp, "system_fingerprint", None),
                          "finish_reason": choice.finish_reason, "content": msg.content,
                          "reasoning_content": reasoning,
                          "tool_calls": [tc.model_dump() for tc in (msg.tool_calls or [])]})
        assistant: Dict[str, Any] = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            assistant["tool_calls"] = [{"id": tc.id, "type": "function",
                                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                                       for tc in msg.tool_calls]
        if self.replay_reasoning and reasoning:
            assistant["reasoning_content"] = reasoning
        self.messages.append(assistant)

        calls = []
        for tc in msg.tool_calls or []:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except (TypeError, ValueError) as e:
                return AgentTurn(error=f"invalid_tool_arguments: {e}", usage=usage)
            calls.append(ToolCall(tc.id, tc.function.name, args, _conf(args)))
        if calls:
            return AgentTurn(calls=calls, usage=usage)
        if choice.finish_reason == "length":
            return AgentTurn(error="max_tokens", usage=usage)
        if choice.finish_reason == "content_filter":
            return AgentTurn(error="refusal: content_filter", usage=usage)
        return AgentTurn(final=msg.content or "(no text)", usage=usage)

    def _error(self, kind: str, exc: Exception, t0: float) -> AgentTurn:
        return AgentTurn(error=f"{kind}: {exc}", usage=Usage(latency_ms=int((time.time() - t0) * 1000)))

    def _usage(self, resp: Any, latency_ms: int) -> Usage:
        u = getattr(resp, "usage", None)
        if u is None:
            return Usage(model_calls=1, latency_ms=latency_ms)
        inp = int(getattr(u, "prompt_tokens", 0) or 0)
        out = int(getattr(u, "completion_tokens", 0) or 0)
        details = getattr(u, "prompt_tokens_details", None)
        cached = int(getattr(details, "cached_tokens", 0) or 0) or int(getattr(u, "prompt_cache_hit_tokens", 0) or 0)
        cost = ((inp - cached) * self.input_price + cached * self.cache_read_price + out * self.output_price) / 1e6
        return Usage(input_tokens=inp, output_tokens=out, cache_read_tokens=cached, model_calls=1,
                     latency_ms=latency_ms, cost_usd=cost)

    def user_reply(self, text: str) -> bool:
        self.messages.append({"role": "user", "content": text})
        return True

    def transcript(self) -> Optional[list]:
        return self._log


def _conf(args: dict) -> Optional[float]:
    try:
        return float(args["confidence"]) if "confidence" in args else None
    except (TypeError, ValueError):
        return None


def list_models(provider: str, key_env: Optional[str] = None) -> List[str]:
    """Model IDs a provider currently serves; use to verify IDs before a run."""
    from openai import OpenAI
    p = PROVIDERS[provider]
    client = OpenAI(base_url=p["base_url"], api_key=os.environ.get(key_env or p["key_env"], ""))
    # Some providers (e.g. Together) return a bare JSON list rather than {"data": [...]},
    # which the SDK's paginated parser rejects; read the raw body and accept either shape.
    body = client.models.with_raw_response.list().http_response.json()
    items = body if isinstance(body, list) else body.get("data", [])
    return sorted(m["id"] for m in items)
