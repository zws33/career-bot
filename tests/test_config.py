"""Tests for career_bot.config."""

import pytest

from career_bot.config import Settings


def test_defaults():
    """Settings should expose sensible defaults."""
    s = Settings()
    assert s.openai_model == "gpt-4o"
    assert s.chroma_collection == "career_docs"
    assert str(s.docs_dir) == "docs"
    assert str(s.output_dir) == "output"


def test_env_override(monkeypatch):
    """Environment variables should override defaults."""
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4-turbo")
    monkeypatch.setenv("CHROMA_COLLECTION", "my_docs")

    s = Settings()
    assert s.openai_model == "gpt-4-turbo"
    assert s.chroma_collection == "my_docs"


def test_validate_raises_without_api_key(monkeypatch):
    """validate() should raise ValueError when OPENAI_API_KEY is missing."""
    monkeypatch.setenv("OPENAI_API_KEY", "")
    s = Settings()
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        s.validate()


def test_validate_passes_with_api_key(monkeypatch):
    """validate() should not raise when OPENAI_API_KEY is set."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    s = Settings()
    # validate() should complete without raising
    s.validate()
