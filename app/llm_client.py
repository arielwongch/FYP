"""Provider interface and OpenRouter implementation."""

from collections.abc import Iterable, Iterator
import json
from typing import Protocol
from urllib import request

from .config import Settings


Message = dict[str, str]


class LLMClient(Protocol):
    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> Iterable[str]: ...


class OpenRouterClient:
    """Stream text deltas from OpenRouter's OpenAI-compatible endpoint."""

    def __init__(self, settings: Settings) -> None:
        if not settings.openrouter_api_key:
            raise ValueError("OpenRouter client requires an API key.")
        self._api_key = settings.openrouter_api_key
        self._base_url = settings.openrouter_base_url.rstrip("/")

    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> Iterator[str]:
        payload = json.dumps(
            {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": True,
            }
        ).encode("utf-8")
        http_request = request.Request(
            f"{self._base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://127.0.0.1",
            },
            method="POST",
        )
        with request.urlopen(http_request, timeout=120) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line or line == "data: [DONE]":
                    continue
                if not line.startswith("data: "):
                    continue
                chunk = json.loads(line[6:])
                content = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                if isinstance(content, str):
                    yield content


def create_client(settings: Settings) -> LLMClient:
    """Create the explicitly selected provider client."""
    if settings.provider == "openrouter":
        return OpenRouterClient(settings)
    if settings.provider == "mock":
        from .mock_llm import MockLLMClient

        return MockLLMClient()
    raise ValueError(f"Unsupported provider: {settings.provider}")