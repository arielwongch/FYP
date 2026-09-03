# docs/spec.md
# ReAct LLM Loop – Local Demo

## Goal
Build a localhost web app where:
- User enters a prompt in a React UI.
- Backend runs a ReAct-style loop calling an LLM API.
- Frontend shows:
  - Final answer
  - ReAct trace (thoughts, actions, observations)

## Constraints
- Localhost only (no auth, no public deployment).
- Backend holds LLM API key in environment variable.
- Support swapping LLM provider via config (OpenAI-compatible interface).

## Acceptance criteria
- [ ] React app runs on http://localhost:3000 (or similar).
- [ ] Backend runs on http://localhost:8000 (or similar).
- [ ] POST /chat accepts { "prompt": string } and returns:
  - final_answer: string
  - trace: array of { role: "thought" | "action" | "observation" | "final", content: string }
- [ ] Frontend sends prompt to backend and displays trace + final answer.
- [ ] Changing LLM_API_KEY in backend .env changes the model used without code changes.