"""Application-wide configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central settings object populated from environment variables.

    Each attribute is read from ``os.getenv`` at *instance creation time* so
    that environment changes (e.g. ``monkeypatch.setenv`` in tests) are
    reflected correctly.
    """

    def __init__(self) -> None:
        # ── LLM ───────────────────────────────────────────────────────────────
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")

        # ── Vector store ──────────────────────────────────────────────────────
        self.chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", ".chroma")
        self.chroma_collection: str = os.getenv("CHROMA_COLLECTION", "career_docs")

        # ── Paths ─────────────────────────────────────────────────────────────
        self.docs_dir: Path = Path(os.getenv("DOCS_DIR", "docs"))
        self.output_dir: Path = Path(os.getenv("OUTPUT_DIR", "output"))

    def validate(self) -> None:
        """Raise ``ValueError`` when required settings are missing."""
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Copy .env.example to .env and add your key."
            )


settings = Settings()
