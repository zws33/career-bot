"""Tests for career_bot.tools.document_processor."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from career_bot.tools.document_processor import load_documents, _file_hash


# ── Helpers ───────────────────────────────────────────────────────────────────


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


# ── Tests ──────────────────────────────────────────────────────────────────────


def test_load_documents_empty_dir(tmp_path):
    """load_documents should return an empty list for an empty directory."""
    docs = load_documents(tmp_path)
    assert docs == []


def test_load_documents_txt(tmp_path):
    """load_documents should load .txt files."""
    _write(tmp_path, "skills.txt", "Android, Kotlin, Jetpack Compose, MVVM")
    docs = load_documents(tmp_path)
    assert len(docs) >= 1
    combined = " ".join(d.page_content for d in docs)
    assert "Kotlin" in combined


def test_load_documents_md(tmp_path):
    """load_documents should load .md files."""
    _write(tmp_path, "accomplishments.md", "# Wins\n- Reduced app crash rate by 40%")
    docs = load_documents(tmp_path)
    assert len(docs) >= 1


def test_load_documents_skips_unsupported(tmp_path):
    """load_documents should silently skip unsupported file types."""
    _write(tmp_path, "notes.csv", "col1,col2\nval1,val2")
    _write(tmp_path, "skills.txt", "Kotlin")
    docs = load_documents(tmp_path)
    # Only the .txt file should be loaded
    assert all(".csv" not in d.metadata.get("source", "") for d in docs)


def test_load_documents_metadata(tmp_path):
    """Each document should carry source and file_hash metadata."""
    _write(tmp_path, "experience.txt", "5 years Android development")
    docs = load_documents(tmp_path)
    for doc in docs:
        assert "source" in doc.metadata
        assert "file_hash" in doc.metadata
        assert doc.metadata["file_hash"]  # non-empty


def test_load_documents_nonexistent_dir(tmp_path):
    """load_documents should return empty list for a non-existent directory."""
    missing = tmp_path / "does_not_exist"
    docs = load_documents(missing)
    assert docs == []


def test_file_hash_consistency(tmp_path):
    """_file_hash should return the same hash for identical file contents."""
    path = _write(tmp_path, "file.txt", "constant content")
    h1 = _file_hash(path)
    h2 = _file_hash(path)
    assert h1 == h2
    assert len(h1) == 32  # MD5 hex digest


def test_file_hash_different_content(tmp_path):
    """_file_hash should return different hashes for different content."""
    p1 = _write(tmp_path, "a.txt", "content A")
    p2 = _write(tmp_path, "b.txt", "content B")
    assert _file_hash(p1) != _file_hash(p2)
