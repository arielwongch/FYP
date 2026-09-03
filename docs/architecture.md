# docs/architecture.md
# Architecture

## Components

### Frontend (React)
- ChatInput: text box + send button.
- TraceView: renders the ReAct trace as a timeline.
- Calls backend at /chat.

### Backend (FastAPI)
- POST /chat:
  - Receives user prompt.
  - Calls ReAct loop.
  - Returns final answer + trace.

### ReAct loop
- System prompt defines:
  - Agent role
  - Available tools (even if just "think" and "final_answer" initially)
  - Output format (thought/action/observation/final).
- Loop:
  1. Call LLM with conversation + allowed format.
  2. Parse response:
     - If thought/action: execute / record observation.
     - If final: break and return.
  3. Append to conversation and repeat until max turns.

### LLM client
- Wraps provider API (e.g., OpenAI).
- Reads API key from env.
- Exposes `call_llm(messages, model_config) -> text`.

## Data flow
User → React → POST /chat → ReAct loop → LLM API → trace → React UI

## Module boundaries
- `frontend/` – UI only, no secrets, no direct LLM calls.
- `backend/app/main.py` – HTTP wiring only.
- `backend/app/react_loop.py` – ReAct algorithm only.
- `backend/app/llm_client.py` – LLM API calls only.
