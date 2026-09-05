# ReAct LLM Loop - Local Research Demo

Build a small local browser app for experimenting with an agent loop. It is a
research tool for one developer, not a hosted product.

The first stage should:
- Serve a browser UI from one simple Python application.
- Send prompts to OpenRouter using a configurable Qwen model under 8B parameters.
- Maintain multi-turn conversation context.
- Stream visible thought events and the final answer live to the browser.
- Render final answers as Markdown; keep thought events as plain text.
- Use a dark research-console theme by default.
- Persist multiple conversations locally, with automatically generated titles.
- Save the effective model, temperature, maximum turns, and system prompt with
  each conversation.
- Run without tools. The loop must have a clear extension point for tools later.

- Localhost only; no authentication, public deployment, or hosted database.
- The OpenRouter API key stays in the local process environment.
- The browser must never receive provider credentials.
- Conversation data is stored in a local file-based format under `.data/`.
- LLM output is untrusted and must be parsed/validated before becoming an event.
- Agent execution has a configurable maximum turn count.
- Provide an offline mock provider for testing the UI and loop without an API key.
- Provider selection is explicit: missing OpenRouter credentials must not silently
  switch an experiment to mock mode.

## Acceptance criteria
- [ ] One Python command starts the local app and serves the browser UI.
- [ ] A chat request accepts a conversation id and prompt, then streams events.
- [ ] Events include `thought`, `final`, and lifecycle/error states.
- [ ] The UI renders user messages, live thoughts, and the final answer distinctly.
- [ ] Final answers render Markdown while thought events remain plain text.
- [ ] The browser UI uses a dark theme by default and remains usable on smaller
  screens.
- [ ] Multiple conversations can be created and selected from a sidebar.
- [ ] Conversations survive an application restart.
- [ ] Conversation settings survive an application restart and are restored when
  the conversation is selected.
- [ ] Changing `OPENROUTER_API_KEY` or `QWEN_MODEL` in `.env` changes configuration
  without code changes.
- [ ] A tool registry boundary exists but contains no enabled tools in stage one.
- [ ] Mock mode can exercise streaming and persistence without calling OpenRouter.
- [ ] Missing credentials produce a clear error unless `LLM_PROVIDER=mock` is set.