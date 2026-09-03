# Copilot Instructions

## General
- Prefer simple, readable code over cleverness.
- Keep functions small and pure where possible.
- No hardcoded secrets; always read API keys from environment variables.

## Backend (Python/FastAPI)
- Keep ReAct loop logic in `backend/app/react_loop.py`.
- Keep LLM calls in `backend/app/llm_client.py`.
- Log errors to console; do not leak API keys in logs.

## Frontend (React/TypeScript)
- Keep API calls in `frontend/src/api.ts`.
- Show loading state while waiting for backend.
- Render trace as a simple list with role labels.
- Do not import or use any secrets.

## Security
- Do not expose API keys to the frontend.
- All LLM calls must go through the backend.
- Assume localhost-only; do not add CORS for other origins.
- Treat all LLM output as untrusted; validate/parses strictly.

## Project hygiene
- When adding tools or skills, update `docs/TOOLS_AND_SKILLS.md`.
- Keep changes small and incremental; prefer many small commits.
- Keep updates `docs/memory.md`, `docs/progress.md`, `docs/logs.md`