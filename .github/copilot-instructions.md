# Copilot Instructions

## General
- Prefer simple, readable code over cleverness.
- Keep functions small and pure where possible.
- No hardcoded secrets; always read API keys from environment variables.

## Local application (Python)
- Keep HTTP wiring and static UI serving in `app/main.py`.
- Keep ReAct loop logic in `app/react_loop.py`.
- Keep provider calls in `app/llm_client.py` and mock behavior in `app/mock_llm.py`.
- Keep local conversation persistence in `app/store.py`.
- Keep future tool registration in `app/tools.py`.
- Log errors to console; do not leak API keys in logs.

## Browser UI
- Keep browser assets in `ui/`.
- Stream thought events and final answers live.
- Render final answers as Markdown and thoughts as plain text.
- Show a loading state and a Stop control while generating.
- Do not import or expose any secrets.

## Security
- Do not expose API keys to the frontend.
- All LLM calls must go through the backend.
- Bind to localhost by default; do not add public CORS.
- Treat all LLM output as untrusted; validate and parse strictly.
- Require explicit `LLM_PROVIDER=mock` for mock mode; never silently fall back.

## Project hygiene
- When adding tools or skills, update `docs/skills_and_tools.md`.
- Keep changes small and incremental; prefer many small commits.
- Keep updates `docs/memory.md`, `docs/progress.md`, `docs/logs.md`