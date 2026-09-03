# docs/toolbox/env.md
# Environment

## Runtimes
- Python 3.11+
- Node 20+

## Backend
- Install: `pip install -r backend/requirements.txt`
- Run: `cd backend && uvicorn app.main:app --reload`
- Test: `cd backend && pytest`

## Frontend
- Install: `cd frontend && npm install`
- Run: `cd frontend && npm start`
- Lint: `npm run lint`

## Common workflows

### Start both services
- Terminal 1:
  ```bash
  cd backend
  uvicorn app.main:app --reload
  ```
- Terminal 2:
  ```bash
  cd frontend
  npm start
  ```

## VS Code setup
- Extensions:
  - Python, Pylance, Black Formatter, ruff
  - ESLint, Prettier
  - GitHub Copilot, Copilot Chat
- Recommended settings:
  - Format on save
  - Run tests on save (optional)

## Env vars
- Backend `.env`:
  - `LLM_API_KEY=...`
  - `LLM_BASE_URL=https://api.openai.com/v1` (or your provider)
- Frontend:
  - No secrets; all calls go through backend.