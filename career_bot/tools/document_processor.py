"""Document processor – loads personal career documents and stores them in a
ChromaDB vector store for retrieval by the career-bot agents.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from career_bot.config import settings

# Supported file extensions and their loaders
_LOADERS = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
}


def _file_hash(path: Path) -> str:
    """Return an MD5 hex-digest of a file's contents."""
    md5 = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def load_documents(docs_dir: Path | None = None) -> List[Document]:
    """Load all supported documents from *docs_dir* and return them as a flat
    list of LangChain :class:`~langchain_core.documents.Document` objects.

    Each document is annotated with ``source`` and ``file_hash`` metadata so
    that the vector store can skip files that have not changed on re-ingestion.
    """
    directory = docs_dir or settings.docs_dir
    docs: List[Document] = []

    if not directory.exists():
        return docs

    for path in sorted(directory.iterdir()):
        suffix = path.suffix.lower()
        loader_cls = _LOADERS.get(suffix)
        if loader_cls is None:
            continue  # unsupported extension – skip silently

        try:
            loader = loader_cls(str(path))
            raw = loader.load()
            file_hash = _file_hash(path)
            for doc in raw:
                doc.metadata["source"] = str(path)
                doc.metadata["file_hash"] = file_hash
            docs.extend(raw)
        except (OSError, IOError, UnicodeDecodeError, ValueError) as exc:
            # Log but do not crash the whole ingestion pipeline
            print(f"[document_processor] WARNING: could not load {path}: {exc}")

    return docs


def build_vector_store(
    docs_dir: Path | None = None,
    persist_dir: str | None = None,
    collection_name: str | None = None,
) -> Chroma:
    """Ingest documents from *docs_dir* into a persistent ChromaDB collection
    and return the :class:`~langchain_chroma.Chroma` instance.

    Documents whose ``file_hash`` metadata already exists in the collection are
    skipped to avoid duplicate embeddings.
    """
    persist_dir = persist_dir or settings.chroma_persist_dir
    collection_name = collection_name or settings.chroma_collection

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.openai_api_key,
    )

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )

    documents = load_documents(docs_dir)
    if not documents:
        return vector_store

    # Determine which hashes are already stored so we only embed new/changed files.
    existing_hashes: set[str] = set()
    try:
        existing = vector_store.get(include=["metadatas"])
        for meta in existing.get("metadatas") or []:
            if meta and meta.get("file_hash"):
                existing_hashes.add(meta["file_hash"])
    except (RuntimeError, ValueError, AttributeError):
        pass  # empty store – ingest everything

    new_docs = [
        doc
        for doc in documents
        if doc.metadata.get("file_hash") not in existing_hashes
    ]

    if not new_docs:
        return vector_store

    # Split into smaller chunks for better retrieval granularity
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(new_docs)

    vector_store.add_documents(chunks)

    return vector_store


def get_vector_store(
    persist_dir: str | None = None,
    collection_name: str | None = None,
) -> Chroma:
    """Return a :class:`~langchain_chroma.Chroma` instance connected to an
    already-built vector store (no ingestion step).
    """
    persist_dir = persist_dir or settings.chroma_persist_dir
    collection_name = collection_name or settings.chroma_collection

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.openai_api_key,
    )

    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )


def retrieve_context(query: str, k: int = 6) -> str:
    """Perform a similarity search against the personal documents vector store
    and return the top-*k* chunks concatenated as a single string.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return "\n\n---\n\n".join(doc.page_content for doc in results)
