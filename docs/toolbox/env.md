# Environment

## Runtime
- Python 3.11+

## Application
- Install: `pip install -r requirements.txt`
- Run: `python -m app`
- Test: `pytest`

## Common workflow

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```

## Env vars
- `OPENROUTER_API_KEY=...`
- `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`
- `QWEN_MODEL=qwen/qwen3-4b`
- `LLM_PROVIDER=openrouter` or `mock`
- `HOST=127.0.0.1`
- `PORT=8000`
- `MAX_AGENT_TURNS=8`
- The browser receives no secrets.