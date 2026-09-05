## Project decisions

- Purpose: a local FYP research tool for experimenting with a small agent loop.
- UI: local browser research console with a sidebar, chat panel, and collapsible
	thought trace; dark theme by default.
- Runtime: one maintainable Python application; no public hosting requirement.
- Provider: OpenRouter, using a configurable Qwen model under 8B parameters.
- Provider selection is explicit through `LLM_PROVIDER`; mock mode is not an
	automatic fallback.
- Stage one has no tools, but the loop must expose a future tool-registry boundary.
- Conversations are multi-turn, stored in project-local `.data/`, and titled from
	the first prompt.
- Model, temperature, maximum turns, and system prompt are editable in the UI and
	persisted per conversation for reproducibility.
- Thought events stream live as plain text; final answers stream live and render
	Markdown.
