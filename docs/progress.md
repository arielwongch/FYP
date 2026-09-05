# Progress

## Current focus
- Scaffold one maintainable Python application with a local browser UI.
- Implement a tool-free, multi-turn ReAct loop with live thought events.
- Persist conversations locally and expose them through a sidebar.

## Done
- [x] Confirmed local browser UI rather than a hosted deployment.
- [x] Selected OpenRouter as the initial provider.
- [x] Selected a configurable Qwen model under 8B parameters.
- [x] Deferred tools until after the first working loop.
- [x] Chosen live thoughts, multi-turn chat, local persistence, and a sidebar.
- [x] Chosen persisted per-conversation overrides for model, temperature, maximum
	turns, and system prompt.
- [x] Chosen Markdown final answers, plain-text thoughts, and an offline mock mode.
- [x] Chosen a dark theme for the research console.
- [x] Chosen explicit provider selection; missing credentials do not trigger a silent
	mock fallback.

## Next
- [ ] Replace stale full-stack scaffolding assumptions with the single-process layout.
- [ ] Add configuration loading and an OpenRouter client.
- [ ] Define validated stream event schemas.
- [ ] Implement the tool-free ReAct loop with a turn limit.
- [ ] Add local conversation storage and streaming chat endpoints.
- [ ] Build the browser UI with sidebar, chat, and live thought trace.

## Locked decisions
- Local-only browser application; no public hosting requirement.
- Prefer one simple Python process over separate UI and service projects.
- Provider: OpenRouter.
- Model family: Qwen, under 8B parameters, configurable by environment variable.
- Stage one has no tools, but the loop includes a future tool registry boundary.
- Thoughts are visible and streamed live.
- Conversations are multi-turn, locally persisted, and selectable in a sidebar.
- Per-conversation model and agent settings are persisted for reproducibility.
- Conversation files live in the project-local, Git-ignored `.data/` directory.
- Final answers use Markdown; thoughts remain plain text for inspection.
- An offline mock provider is required for development without an API key.
- Mock mode must be selected explicitly with `LLM_PROVIDER=mock`.
- All secrets stay in the local process environment.