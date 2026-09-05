"""File-based conversation persistence."""

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path
from threading import RLock
from uuid import uuid4


DEFAULT_SYSTEM_PROMPT = "You are a careful research assistant."


@dataclass
class Conversation:
    id: str
    title: str
    model: str
    temperature: float
    max_turns: int
    system_prompt: str
    messages: list[dict[str, str]] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ConversationStore:
    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._lock = RLock()
        self._data_dir.mkdir(parents=True, exist_ok=True)

    def create(
        self,
        model: str,
        max_turns: int,
        temperature: float = 0.2,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> Conversation:
        now = _timestamp()
        conversation = Conversation(
            id=uuid4().hex,
            title="New conversation",
            model=model,
            temperature=temperature,
            max_turns=max_turns,
            system_prompt=system_prompt,
            created_at=now,
            updated_at=now,
        )
        self.save(conversation)
        return conversation

    def get(self, conversation_id: str) -> Conversation:
        path = self._path_for(conversation_id)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return Conversation(**payload)
        except FileNotFoundError as error:
            raise KeyError(conversation_id) from error
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            raise ValueError(f"Conversation file is invalid: {conversation_id}") from error

    def list(self) -> list[Conversation]:
        conversations = []
        for path in self._data_dir.glob("*.json"):
            try:
                conversations.append(self.get(path.stem))
            except ValueError:
                continue
        return sorted(conversations, key=lambda item: item.updated_at, reverse=True)

    def save(self, conversation: Conversation) -> None:
        with self._lock:
            conversation.updated_at = _timestamp()
            path = self._path_for(conversation.id)
            temporary_path = path.with_suffix(".tmp")
            temporary_path.write_text(
                json.dumps(conversation.to_dict(), indent=2), encoding="utf-8"
            )
            temporary_path.replace(path)

    def append_user_message(self, conversation: Conversation, content: str) -> None:
        if not content.strip():
            raise ValueError("Prompt must not be empty.")
        if conversation.title == "New conversation":
            conversation.title = content.strip().replace("\n", " ")[:60]
        conversation.messages.append({"role": "user", "content": content})
        self.save(conversation)

    def append_assistant_message(self, conversation: Conversation, content: str) -> None:
        conversation.messages.append({"role": "assistant", "content": content})
        self.save(conversation)

    def update_settings(
        self,
        conversation: Conversation,
        model: str,
        temperature: float,
        max_turns: int,
        system_prompt: str,
    ) -> None:
        if not model.strip() or not 0 <= temperature <= 1 or max_turns < 1:
            raise ValueError("Conversation settings are invalid.")
        conversation.model = model.strip()
        conversation.temperature = temperature
        conversation.max_turns = max_turns
        conversation.system_prompt = system_prompt.strip()
        self.save(conversation)

    def _path_for(self, conversation_id: str) -> Path:
        if not conversation_id.isalnum():
            raise KeyError(conversation_id)
        return self._data_dir / f"{conversation_id}.json"


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()