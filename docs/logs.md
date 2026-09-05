## 2026-09-05 - Planning refinement

- Re-scoped the project from a hosted React/FastAPI demo to a local browser
	research console backed by one Python process.
- Confirmed OpenRouter with a configurable sub-8B Qwen model.
- Confirmed live visible thoughts, multi-turn conversations, local persistence,
	sidebar navigation, editable saved settings, Markdown final answers, and plain
	text thought traces.
- Deferred tools to a later stage and added an explicit offline mock-provider path.

## 2026-09-05 - Backend foundation

- Added `app/config.py` with typed settings and explicit `openrouter`/`mock`
	provider validation.
- Added focused tests covering mock mode, missing credentials, and unknown
	providers.

## 2026-09-05 - Backend vertical slice

- Added one-JSON-file-per-conversation persistence under `.data/`.
- Added the bounded tool-free ReAct loop and SSE endpoints for conversation
	listing, creation, selection, and chat streaming.
- Confirmed 8 focused tests pass and the mock HTTP path returns conversation
	creation plus streamed thought/final events.

## 2026-09-05 - Browser console

- Added the vanilla browser UI with a responsive dark research-console layout,
	conversation sidebar, live thought trace, Markdown-style final answers, and
	per-conversation settings.
- Added static asset serving from `/` and `/ui/*`.
- Added settings updates through `PATCH /api/conversations/{id}`.
- Confirmed 9 focused tests pass, Python compilation succeeds, browser script
	syntax is valid, and the mock-mode app serves its UI and API on localhost.
