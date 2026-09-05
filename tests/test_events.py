import json

import pytest

from app.events import EventValidationError, StreamEvent


def test_event_serializes_as_sse() -> None:
    event = StreamEvent("thought", "checking the request")

    assert event.to_dict() == {"type": "thought", "content": "checking the request"}
    assert event.to_sse().startswith("event: thought\ndata: ")
    assert json.loads(event.to_sse().split("data: ", 1)[1]) == event.to_dict()


def test_event_rejects_untrusted_shape() -> None:
    with pytest.raises(EventValidationError):
        StreamEvent.from_dict({"type": "tool", "content": "run"})


def test_mock_provider_streams_structured_text() -> None:
    from app.mock_llm import MockLLMClient

    output = "".join(MockLLMClient().stream([{"role": "user", "content": "hello"}], "model", 0.2))

    assert '"type":"thought"' in output
    assert '"type":"final"' in output