# Architecture

## Direction

Use one small Python application that serves static browser assets and exposes a
local streaming chat endpoint. Avoid separate frontend and backend projects until
the research workflow proves that they are needed.

### Browser UI
- ChatSidebar: lists saved conversations and creates a new chat.
- ChatView: renders the selected conversation.
- ThoughtTrace: renders live thought events separately from final answers.
- ChatInput: sends a new user message and supports the busy state.

### Local Python application
- Serves the browser UI.
- Exposes conversation and streaming chat endpoints.
- Loads configuration from `.env`.
- Reads and writes the local conversation store.

### ReAct loop
- System prompt defines the agent role and the structured event format.
- Stage one enables only `thought` and `final` events. Tool events remain reserved
  for the later tool registry.

### LLM client
- Wraps the OpenRouter OpenAI-compatible API.
- Reads credentials and model settings from environment variables.
- Exposes a small streaming call interface to the ReAct loop.
- Provides a deterministic mock provider with the same interface for local tests.
- Selects the provider explicitly from `LLM_PROVIDER`; it never falls back silently.

### Conversation store
- Stores conversations in a local JSON file under the project `.data/` directory.
- Owns loading, saving, listing, and selecting conversations.
- Persists the effective model, temperature, maximum turns, and system prompt for
  each conversation so experiments can be reproduced.
- Does not contain provider or browser-specific logic.

### Tool registry (stage two boundary)
- Defines tool metadata, input validation, execution, and result events.
- Has no enabled tools in stage one.

## Data flow
User → browser UI → local streaming endpoint → ReAct loop → OpenRouter → events → browser UI

## Module boundaries
- `app/main.py` - local HTTP wiring and static UI serving only.
- `app/react_loop.py` - ReAct algorithm and event validation only.
- `app/llm_client.py` - OpenRouter API calls only.
- `app/mock_llm.py` - offline provider for UI and loop development.
- `app/store.py` - local conversation persistence only.
- `app/tools.py` - future tool registry boundary; no stage-one tools.
- `ui/` - browser assets only; no secrets or direct LLM calls.
