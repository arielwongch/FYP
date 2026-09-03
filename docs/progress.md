# docs/progress.md
# Progress

## Current focus
- Implement basic ReAct loop with THOUGHT/ACTION/OBSERVATION/FINAL.
- Wire React frontend to call `/chat` and display trace.

## Done
- [ ] Project scaffolding (backend + frontend)
- [ ] Basic `/chat` endpoint (echo)
- [ ] ReAct loop skeleton
- [ ] LLM client skeleton
- [ ] React ChatInput + TraceView

## Next
- [ ] Implement real LLM calls in `llm_client.py`
- [ ] Implement parsing for THOUGHT/ACTION/OBSERVATION/FINAL

## Locked decisions
- Backend: FastAPI + Python 3.11+
- Frontend: React + TypeScript
- LLM: OpenAI-compatible API (swappable via `LLM_BASE_URL`)
- All secrets in backend `.env` only.