# FYP Agent Loop

A small local browser application for experimenting with a ReAct-style agent loop.
The first development stage uses OpenRouter and a Qwen model under 8B parameters.
It supports multi-turn conversations, live thought streaming, and locally persisted
conversation history. Tools are intentionally deferred until the core loop is stable.

## Development status

The repository is currently in the planning-to-development transition. See
[docs/spec.md](docs/spec.md), [docs/architecture.md](docs/architecture.md), and
[docs/progress.md](docs/progress.md) for the current scope and next slice.

## Local setup

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```

Then open the local URL printed by the application.

The `.env` file is local-only and must never be committed. The browser UI does not
receive the OpenRouter API key.