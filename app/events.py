"""Validated events emitted by the agent loop and streamed over SSE."""

from dataclasses import dataclass
import json
from typing import Any, Literal


EventKind = Literal["thought", "final", "status", "error"]
_EVENT_KINDS = {"thought", "final", "status", "error"}


class EventValidationError(ValueError):
    """Raised when an event payload is not safe to expose to the browser."""


@dataclass(frozen=True)
class StreamEvent:
    kind: EventKind
    content: str

    def __post_init__(self) -> None:
        if self.kind not in _EVENT_KINDS:
            raise EventValidationError(f"Unsupported event kind: {self.kind}")
        if not isinstance(self.content, str):
            raise EventValidationError("Event content must be text.")

    def to_dict(self) -> dict[str, str]:
        return {"type": self.kind, "content": self.content}

    def to_sse(self) -> str:
        return f"event: {self.kind}\ndata: {json.dumps(self.to_dict())}\n\n"

    @classmethod
    def from_dict(cls, payload: Any) -> "StreamEvent":
        if not isinstance(payload, dict):
            raise EventValidationError("Event payload must be an object.")
        kind = payload.get("type")
        content = payload.get("content")
        if kind not in _EVENT_KINDS:
            raise EventValidationError("Event type is invalid.")
        if not isinstance(content, str):
            raise EventValidationError("Event content must be text.")
        return cls(kind=kind, content=content)