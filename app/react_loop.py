"""Tool-free ReAct loop with strict model-event parsing."""

import json
from collections.abc import Iterator
from typing import Any

from .events import EventValidationError, StreamEvent
from .llm_client import LLMClient, Message


def run_loop(
    client: LLMClient,
    messages: list[Message],
    model: str,
    temperature: float,
    max_turns: int,
) -> Iterator[StreamEvent]:
    if max_turns < 1:
        yield StreamEvent("error", "Maximum turns must be at least 1.")
        return

    yield StreamEvent("status", "started")
    buffer = ""
    saw_final = False
    try:
        for chunk in client.stream(messages, model, temperature):
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                event = _parse_model_event(line)
                yield event
                saw_final = saw_final or event.kind == "final"
        if buffer.strip():
            event = _parse_model_event(buffer)
            yield event
            saw_final = saw_final or event.kind == "final"
    except (EventValidationError, json.JSONDecodeError, TypeError) as error:
        yield StreamEvent("error", f"Invalid model event: {error}")
        return

    if not saw_final:
        yield StreamEvent("error", "The model stream ended without a final answer.")
        return
    yield StreamEvent("status", "complete")


def _parse_model_event(line: str) -> StreamEvent:
    payload: Any = json.loads(line)
    return StreamEvent.from_dict(payload)