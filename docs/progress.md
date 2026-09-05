# Progress

## Current focus
- Review and validate the complete local research console.

## Done
- [x] Added per-conversation JSON persistence under `.data/`.
- [x] Added a bounded tool-free ReAct loop with validated SSE events.
- [x] Added conversation and streaming chat HTTP endpoints.
- [x] Added a responsive vanilla browser UI with sidebar, chat, thought trace,
  settings, Markdown answers, and a Stop-ready busy state.
- [x] Served the UI directly from the Python application.
- [x] Persisted settings edits through the conversation API.
- [x] Verified the backend with 8 focused tests and an HTTP mock smoke test.
- [x] Added typed environment configuration with explicit provider validation.
- [x] Added focused configuration tests for mock mode and credential errors.
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
- [ ] Add browser automation coverage when a browser test runner is available.

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
- SSE is the browser streaming transport; the UI uses plain HTML, CSS, and
	JavaScript with no frontend build step.