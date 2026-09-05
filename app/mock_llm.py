"""Deterministic offline provider used for local development."""

from collections.abc import Iterator

from .llm_client import Message


class MockLLMClient:
    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
    ) -> Iterator[str]:
        del model, temperature
        prompt = messages[-1]["content"] if messages else ""
        response = (
            '{"type":"thought","content":"Mock provider is considering the request."}\n'
            f'{{"type":"final","content":"Mock response for: {prompt}"}}\n'
        )
        for chunk_start in range(0, len(response), 24):
            yield response[chunk_start : chunk_start + 24]