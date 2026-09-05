"""Environment-backed application configuration."""

from dataclasses import dataclass
import os
from pathlib import Path


class ConfigurationError(ValueError):
    """Raised when the application configuration cannot be used safely."""


@dataclass(frozen=True)
class Settings:
    """Runtime settings shared by the backend modules."""

    provider: str
    openrouter_api_key: str | None
    openrouter_base_url: str
    qwen_model: str
    host: str
    port: int
    max_agent_turns: int

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> "Settings":
        """Load and validate settings from the process environment and `.env`."""
        _load_dotenv()
        values = os.environ if environ is None else environ
        provider = values.get("LLM_PROVIDER", "openrouter").strip().lower()
        if provider not in {"openrouter", "mock"}:
            raise ConfigurationError(
                "LLM_PROVIDER must be either 'openrouter' or 'mock'."
            )

        api_key = values.get("OPENROUTER_API_KEY", "").strip() or None
        if provider == "openrouter" and api_key is None:
            raise ConfigurationError(
                "OPENROUTER_API_KEY is required when LLM_PROVIDER=openrouter."
            )

        try:
            port = int(values.get("PORT", "8000"))
            max_agent_turns = int(values.get("MAX_AGENT_TURNS", "8"))
        except ValueError as error:
            raise ConfigurationError("PORT and MAX_AGENT_TURNS must be integers.") from error

        if not 1 <= port <= 65535:
            raise ConfigurationError("PORT must be between 1 and 65535.")
        if max_agent_turns < 1:
            raise ConfigurationError("MAX_AGENT_TURNS must be at least 1.")

        return cls(
            provider=provider,
            openrouter_api_key=api_key,
            openrouter_base_url=values.get(
                "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
            ).strip(),
            qwen_model=values.get("QWEN_MODEL", "qwen/qwen3-4b").strip(),
            host=values.get("HOST", "127.0.0.1").strip(),
            port=port,
            max_agent_turns=max_agent_turns,
        )


def _load_dotenv() -> None:
    """Load simple KEY=VALUE entries without overwriting process variables."""
    env_file = Path(".env")
    if not env_file.is_file():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)