from pathlib import Path

from app.mock_llm import MockLLMClient
from app.react_loop import run_loop
from app.store import ConversationStore


def test_conversations_are_persisted_individually(tmp_path: Path) -> None:
    store = ConversationStore(tmp_path)
    conversation = store.create("qwen/test", 4)
    store.append_user_message(conversation, "What is persistence?")

    restored = ConversationStore(tmp_path).get(conversation.id)

    assert restored.title == "What is persistence?"
    assert restored.messages[0]["role"] == "user"
    assert (tmp_path / f"{conversation.id}.json").is_file()


def test_mock_react_loop_emits_final_event() -> None:
    events = list(
        run_loop(
            MockLLMClient(),
            [{"role": "user", "content": "hello"}],
            "qwen/test",
            0.2,
            4,
        )
    )

    assert [event.kind for event in events] == ["status", "thought", "final", "status"]


def test_conversation_settings_are_persisted(tmp_path: Path) -> None:
    store = ConversationStore(tmp_path)
    conversation = store.create("qwen/test", 4)
    store.update_settings(conversation, "qwen/updated", 0.7, 9, "Be concise.")

    restored = ConversationStore(tmp_path).get(conversation.id)

    assert restored.model == "qwen/updated"
    assert restored.temperature == 0.7
    assert restored.max_turns == 9
    assert restored.system_prompt == "Be concise."