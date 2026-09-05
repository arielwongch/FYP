import pytest

from app.config import ConfigurationError, Settings


def test_mock_provider_does_not_require_api_key() -> None:
    settings = Settings.from_env({"LLM_PROVIDER": "mock"})

    assert settings.provider == "mock"
    assert settings.openrouter_api_key is None


def test_openrouter_provider_requires_api_key() -> None:
    with pytest.raises(ConfigurationError, match="OPENROUTER_API_KEY"):
        Settings.from_env({"LLM_PROVIDER": "openrouter"})


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(ConfigurationError, match="LLM_PROVIDER"):
        Settings.from_env({"LLM_PROVIDER": "other"})