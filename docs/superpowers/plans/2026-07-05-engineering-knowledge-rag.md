# Engineering Knowledge RAG Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first CLI version of `engineering-knowledge-rag/`, a production-shaped engineering knowledge base RAG Agent using LangChain, LangGraph, and LangSmith.

**Architecture:** The CLI is only an adapter. Core behavior lives in focused modules for settings, document ingestion, embeddings, local vector index, LangGraph workflow, and eval. The first version indexes only allowlisted repository documents, answers with citations, validates citation sources, exposes low-confidence/refusal behavior, and keeps the graph reusable for a future FastAPI adapter.

**Tech Stack:** Python 3.14, uv, pytest, Typer, Rich, Pydantic Settings, LangChain, LangGraph, LangSmith, Ollama provider, OpenAI-compatible provider.

## Global Constraints

- Create the project under `engineering-knowledge-rag/`.
- Use `uv` for dependency management.
- First version is CLI-only.
- Do not implement FastAPI in this plan.
- First version indexes only: `README.md`, `CLAUDE.md`, `agent-loop/README.md`, `fast-api-demo/README.md`, `learning-resources/resources.md`, `docs/superpowers/specs/*.md`.
- Do not index code files, PDF files, or external websites in the first version.
- Support both Ollama and OpenAI-compatible APIs for chat models and embeddings.
- Keep provider differences out of `graph.py`.
- Use LangChain for document loading/splitting, embeddings, prompt templates, and LLM adapters.
- Use LangGraph for the RAG state machine.
- Use LangSmith tracing through environment configuration.
- CLI commands must include: `uv run rag doctor`, `uv run rag ingest`, `uv run rag ask "这个仓库的 Agent 学习路线是什么？"`, and `uv run rag eval`.
- Test deterministic logic with fake providers; do not require network model calls for unit tests.
- Documentation must include interview-focused project highlights and talking points.

---

## File Structure

- Create `engineering-knowledge-rag/pyproject.toml`: uv project metadata, dependencies, and `rag` console script.
- Create `engineering-knowledge-rag/.gitignore`: ignore local env, venv, caches, and generated JSON indexes.
- Create `engineering-knowledge-rag/.env.example`: documented configuration for Ollama, OpenAI-compatible APIs, and LangSmith.
- Create `engineering-knowledge-rag/README.md`: project positioning, quick start, CLI commands, architecture summary, project highlights, MVP boundary.
- Create `engineering-knowledge-rag/docs/architecture.md`: framework responsibilities, graph flow, provider boundary, CLI-to-FastAPI evolution.
- Create `engineering-knowledge-rag/docs/interview-notes.md`: interview narrative, highlights, follow-up questions, answer outlines.
- Create `engineering-knowledge-rag/docs/eval-strategy.md`: smoke eval design and quality gates.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/__init__.py`: package marker and version.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/config.py`: settings and paths.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/documents.py`: allowlisted discovery, reading, normalization, chunking.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/embeddings.py`: deterministic test embeddings and runtime embedding provider factories.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/llms.py`: chat model provider factories.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/vectorstore.py`: local JSON vector index with cosine search.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/prompts.py`: prompt templates.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py`: graph state, nodes, citation verification, LangGraph builder.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/evals.py`: smoke eval loading, metric checks, runner.
- Create `engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py`: Typer CLI adapter.
- Create `engineering-knowledge-rag/data/evals/smoke.jsonl`: 6 smoke eval cases.
- Create `engineering-knowledge-rag/data/indexes/.gitkeep`: keep index directory without committing generated index files.
- Create `engineering-knowledge-rag/tests/test_config.py`: settings tests.
- Create `engineering-knowledge-rag/tests/test_documents.py`: discovery and chunk metadata tests.
- Create `engineering-knowledge-rag/tests/test_vectorstore.py`: local index persistence and search tests.
- Create `engineering-knowledge-rag/tests/test_citations.py`: citation validation tests.
- Create `engineering-knowledge-rag/tests/test_graph_state.py`: graph state and low-confidence path tests.
- Create `engineering-knowledge-rag/tests/test_evals.py`: eval metric tests.

### Task 1: Project Scaffold And Settings

**Files:**
- Create: `engineering-knowledge-rag/pyproject.toml`
- Create: `engineering-knowledge-rag/.gitignore`
- Create: `engineering-knowledge-rag/.env.example`
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/__init__.py`
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/config.py`
- Create: `engineering-knowledge-rag/tests/test_config.py`

**Interfaces:**
- Consumes: no earlier project code
- Produces:
  - `ProviderName = Literal["ollama", "openai"]`
  - `AppSettings`
  - `load_settings(env_file: str | Path | None = None) -> AppSettings`
  - `apply_langsmith_environment(settings: AppSettings) -> None`
  - `AppSettings.project_root: Path`
  - `AppSettings.repo_root: Path`
  - `AppSettings.index_path: Path`
  - `AppSettings.eval_path: Path`

- [ ] **Step 1: Write the failing settings tests**

Create `engineering-knowledge-rag/tests/test_config.py` with:

```python
import os
from pathlib import Path

from engineering_knowledge_rag.config import AppSettings, apply_langsmith_environment, load_settings


def test_default_settings_point_to_repo_and_project_paths():
    settings = AppSettings()

    assert settings.model_provider == "ollama"
    assert settings.project_root.name == "engineering-knowledge-rag"
    assert settings.repo_root.name == "AiFlowScript"
    assert settings.index_path == settings.project_root / "data" / "indexes" / "knowledge_index.json"
    assert settings.eval_path == settings.project_root / "data" / "evals" / "smoke.jsonl"


def test_openai_settings_can_be_loaded_from_env_file(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "MODEL_PROVIDER=openai",
                "OPENAI_BASE_URL=https://example.test/v1",
                "OPENAI_API_KEY=test-key",
                "OPENAI_CHAT_MODEL=test-chat",
                "OPENAI_EMBEDDING_MODEL=test-embed",
            ]
        ),
        encoding="utf-8",
    )

    settings = load_settings(env_file)

    assert settings.model_provider == "openai"
    assert settings.openai_base_url == "https://example.test/v1"
    assert settings.openai_api_key == "test-key"
    assert settings.openai_chat_model == "test-chat"
    assert settings.openai_embedding_model == "test-embed"


def test_apply_langsmith_environment_sets_process_env(monkeypatch):
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_PROJECT", raising=False)
    settings = AppSettings(langsmith_tracing=True, langsmith_project="test-rag-project")

    apply_langsmith_environment(settings)

    assert os.environ["LANGSMITH_TRACING"] == "true"
    assert os.environ["LANGSMITH_PROJECT"] == "test-rag-project"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_config.py -v
```

Expected: fail because `pyproject.toml` and `engineering_knowledge_rag.config` do not exist yet.

- [ ] **Step 3: Create project metadata**

Create `engineering-knowledge-rag/pyproject.toml` with:

```toml
[project]
name = "engineering-knowledge-rag"
version = "0.1.0"
description = "Engineering knowledge base RAG Agent with LangChain, LangGraph, and LangSmith"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "langchain-core>=1.0.0",
    "langchain-text-splitters>=1.0.0",
    "langchain-ollama>=1.0.0",
    "langchain-openai>=1.0.0",
    "langgraph>=1.0.0",
    "langsmith>=0.4.0",
    "httpx>=0.28.0",
    "pydantic-settings>=2.12.0",
    "rich>=14.0.0",
    "typer>=0.20.0",
]

[dependency-groups]
dev = [
    "pytest>=9.0.0",
]

[project.scripts]
rag = "engineering_knowledge_rag.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Create `engineering-knowledge-rag/.env.example` with:

```env
MODEL_PROVIDER=ollama

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=qwen3:14b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

LANGSMITH_TRACING=true
LANGSMITH_PROJECT=engineering-knowledge-rag
```

Create `engineering-knowledge-rag/.gitignore` with:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
data/indexes/*.json
```

- [ ] **Step 4: Implement package marker and settings**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/__init__.py` with:

```python
"""Engineering knowledge base RAG Agent."""

__version__ = "0.1.0"
```

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/config.py` with:

```python
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ProviderName = Literal["ollama", "openai"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT.parent


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    model_provider: ProviderName = "ollama"

    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "qwen3:14b"
    ollama_embedding_model: str = "nomic-embed-text"

    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    langsmith_tracing: bool = True
    langsmith_project: str = "engineering-knowledge-rag"

    project_root: Path = Field(default=PROJECT_ROOT)
    repo_root: Path = Field(default=REPO_ROOT)
    index_path: Path = Field(default=PROJECT_ROOT / "data" / "indexes" / "knowledge_index.json")
    eval_path: Path = Field(default=PROJECT_ROOT / "data" / "evals" / "smoke.jsonl")

    chunk_size: int = 900
    chunk_overlap: int = 120
    top_k: int = 5
    min_relevance_score: float = 0.15


def load_settings(env_file: str | Path | None = None) -> AppSettings:
    if env_file is None:
        return AppSettings()
    return AppSettings(_env_file=env_file)


def apply_langsmith_environment(settings: AppSettings) -> None:
    os.environ["LANGSMITH_TRACING"] = "true" if settings.langsmith_tracing else "false"
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
```

- [ ] **Step 5: Run settings tests**

Run:

```bash
cd engineering-knowledge-rag
uv sync
uv run pytest tests/test_config.py -v
```

Expected: both tests pass.

- [ ] **Step 6: Commit scaffold and settings**

```bash
git add engineering-knowledge-rag/pyproject.toml \
  engineering-knowledge-rag/uv.lock \
  engineering-knowledge-rag/.gitignore \
  engineering-knowledge-rag/.env.example \
  engineering-knowledge-rag/src/engineering_knowledge_rag/__init__.py \
  engineering-knowledge-rag/src/engineering_knowledge_rag/config.py \
  engineering-knowledge-rag/tests/test_config.py
git commit -m "feat: scaffold engineering knowledge rag project"
```

### Task 2: Document Discovery And Chunking

**Files:**
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/documents.py`
- Create: `engineering-knowledge-rag/tests/test_documents.py`

**Interfaces:**
- Consumes:
  - `AppSettings.repo_root`
  - `AppSettings.chunk_size`
  - `AppSettings.chunk_overlap`
- Produces:
  - `DEFAULT_SOURCE_PATTERNS: tuple[str, ...]`
  - `discover_source_files(repo_root: Path, patterns: Sequence[str] = DEFAULT_SOURCE_PATTERNS) -> list[Path]`
  - `load_source_documents(repo_root: Path, patterns: Sequence[str] = DEFAULT_SOURCE_PATTERNS) -> list[Document]`
  - `chunk_documents(documents: Sequence[Document], chunk_size: int, chunk_overlap: int) -> list[Document]`

- [ ] **Step 1: Write failing document tests**

Create `engineering-knowledge-rag/tests/test_documents.py` with:

```python
from pathlib import Path

from engineering_knowledge_rag.documents import (
    DEFAULT_SOURCE_PATTERNS,
    chunk_documents,
    discover_source_files,
    load_source_documents,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_discover_source_files_uses_allowlist(tmp_path: Path):
    write(tmp_path / "README.md", "# Root")
    write(tmp_path / "CLAUDE.md", "# Agent rules")
    write(tmp_path / "agent-loop" / "README.md", "# Agent Loop")
    write(tmp_path / "notes.py", "print('not indexed')")
    write(tmp_path / "learning-resources" / "paper.pdf", "%PDF")
    write(tmp_path / "docs" / "superpowers" / "specs" / "spec.md", "# Spec")

    files = discover_source_files(tmp_path, DEFAULT_SOURCE_PATTERNS)

    assert files == [
        Path("CLAUDE.md"),
        Path("README.md"),
        Path("agent-loop/README.md"),
        Path("docs/superpowers/specs/spec.md"),
    ]


def test_load_source_documents_adds_source_metadata(tmp_path: Path):
    write(tmp_path / "README.md", "# Root\n\nThis is the root readme.")

    docs = load_source_documents(tmp_path, patterns=("README.md",))

    assert len(docs) == 1
    assert docs[0].page_content == "# Root\n\nThis is the root readme."
    assert docs[0].metadata["source_path"] == "README.md"
    assert docs[0].metadata["source_type"] == ".md"


def test_chunk_documents_preserves_source_and_chunk_id(tmp_path: Path):
    write(tmp_path / "README.md", "# Root\n\n" + "Agent knowledge base. " * 80)
    docs = load_source_documents(tmp_path, patterns=("README.md",))

    chunks = chunk_documents(docs, chunk_size=120, chunk_overlap=20)

    assert len(chunks) > 1
    assert chunks[0].metadata["source_path"] == "README.md"
    assert chunks[0].metadata["chunk_id"] == "README.md#0000"
    assert chunks[1].metadata["chunk_id"] == "README.md#0001"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_documents.py -v
```

Expected: fail because `engineering_knowledge_rag.documents` does not exist.

- [ ] **Step 3: Implement document discovery and chunking**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/documents.py` with:

```python
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_SOURCE_PATTERNS: tuple[str, ...] = (
    "README.md",
    "CLAUDE.md",
    "agent-loop/README.md",
    "fast-api-demo/README.md",
    "learning-resources/resources.md",
    "docs/superpowers/specs/*.md",
)


def discover_source_files(
    repo_root: Path,
    patterns: Sequence[str] = DEFAULT_SOURCE_PATTERNS,
) -> list[Path]:
    repo_root = repo_root.resolve()
    discovered: set[Path] = set()

    for pattern in patterns:
        for path in repo_root.glob(pattern):
            if path.is_file():
                discovered.add(path.resolve().relative_to(repo_root))

    return sorted(discovered, key=lambda item: item.as_posix())


def load_source_documents(
    repo_root: Path,
    patterns: Sequence[str] = DEFAULT_SOURCE_PATTERNS,
) -> list[Document]:
    repo_root = repo_root.resolve()
    documents: list[Document] = []

    for relative_path in discover_source_files(repo_root, patterns):
        absolute_path = repo_root / relative_path
        text = absolute_path.read_text(encoding="utf-8", errors="ignore")
        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source_path": relative_path.as_posix(),
                    "source_type": absolute_path.suffix,
                },
            )
        )

    return documents


def chunk_documents(
    documents: Sequence[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "，", " ", ""],
    )
    chunks: list[Document] = []
    per_source_count: dict[str, int] = {}

    for document in documents:
        source_path = str(document.metadata["source_path"])
        split_docs = splitter.split_documents([document])
        for split_doc in split_docs:
            ordinal = per_source_count.get(source_path, 0)
            per_source_count[source_path] = ordinal + 1
            split_doc.metadata = {
                **split_doc.metadata,
                "source_path": source_path,
                "chunk_id": f"{source_path}#{ordinal:04d}",
            }
            chunks.append(split_doc)

    return chunks
```

- [ ] **Step 4: Run document tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_documents.py -v
```

Expected: all 3 tests pass.

- [ ] **Step 5: Run config and document tests together**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_config.py tests/test_documents.py -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit document ingestion**

```bash
git add engineering-knowledge-rag/src/engineering_knowledge_rag/documents.py \
  engineering-knowledge-rag/tests/test_documents.py
git commit -m "feat: add document discovery and chunking"
```

### Task 3: Embeddings And Local Vector Index

**Files:**
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/embeddings.py`
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/vectorstore.py`
- Create: `engineering-knowledge-rag/tests/test_vectorstore.py`
- Create: `engineering-knowledge-rag/data/indexes/.gitkeep`

**Interfaces:**
- Consumes:
  - LangChain `Document`
  - `AppSettings.model_provider`
  - `AppSettings.index_path`
- Produces:
  - `HashEmbeddings(size: int = 64)`
  - `create_embeddings(settings: AppSettings) -> Embeddings`
  - `IndexedChunk`
  - `SearchResult`
  - `LocalVectorStore.from_documents(documents: Sequence[Document], embeddings: Embeddings) -> LocalVectorStore`
  - `LocalVectorStore.save(path: Path) -> None`
  - `LocalVectorStore.load(path: Path) -> LocalVectorStore`
  - `LocalVectorStore.search(query: str, embeddings: Embeddings, top_k: int) -> list[SearchResult]`

- [ ] **Step 1: Write failing vector store tests**

Create `engineering-knowledge-rag/tests/test_vectorstore.py` with:

```python
from pathlib import Path

from langchain_core.documents import Document

from engineering_knowledge_rag.embeddings import HashEmbeddings
from engineering_knowledge_rag.vectorstore import LocalVectorStore, cosine_similarity


def test_cosine_similarity_handles_same_and_empty_vectors():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert cosine_similarity([], []) == 0.0
    assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_local_vector_store_persists_and_searches(tmp_path: Path):
    docs = [
        Document(
            page_content="Agent Loop uses tool calling and tool result feedback.",
            metadata={"source_path": "agent-loop/README.md", "chunk_id": "agent-loop/README.md#0000"},
        ),
        Document(
            page_content="FastAPI exposes HTTP APIs for production services.",
            metadata={"source_path": "fast-api-demo/README.md", "chunk_id": "fast-api-demo/README.md#0000"},
        ),
    ]
    embeddings = HashEmbeddings(size=32)
    index_path = tmp_path / "index.json"

    store = LocalVectorStore.from_documents(docs, embeddings)
    store.save(index_path)
    loaded = LocalVectorStore.load(index_path)
    results = loaded.search("How does Agent Loop handle tool calling?", embeddings, top_k=1)

    assert len(results) == 1
    assert results[0].source_path == "agent-loop/README.md"
    assert results[0].chunk_id == "agent-loop/README.md#0000"
    assert results[0].score > 0.0
```

- [ ] **Step 2: Run vector store tests to verify they fail**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_vectorstore.py -v
```

Expected: fail because `embeddings.py` and `vectorstore.py` do not exist.

- [ ] **Step 3: Implement embeddings provider factory**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/embeddings.py` with:

```python
from __future__ import annotations

import hashlib
import math

from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

from engineering_knowledge_rag.config import AppSettings


class HashEmbeddings(Embeddings):
    """Deterministic embeddings for unit tests and offline smoke checks."""

    def __init__(self, size: int = 64) -> None:
        self.size = size

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        vector = [0.0] * self.size
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.size
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0.0:
            return vector
        return [value / norm for value in vector]


def create_embeddings(settings: AppSettings) -> Embeddings:
    if settings.model_provider == "ollama":
        return OllamaEmbeddings(
            model=settings.ollama_embedding_model,
            base_url=settings.ollama_base_url,
        )

    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        base_url=settings.openai_base_url,
        api_key=settings.openai_api_key,
    )
```

- [ ] **Step 4: Implement local vector store**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/vectorstore.py` with:

```python
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


@dataclass(frozen=True)
class IndexedChunk:
    chunk_id: str
    source_path: str
    text: str
    vector: list[float]


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    source_path: str
    text: str
    score: float


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


class LocalVectorStore:
    def __init__(self, chunks: list[IndexedChunk]) -> None:
        self.chunks = chunks

    @classmethod
    def from_documents(
        cls,
        documents: Sequence[Document],
        embeddings: Embeddings,
    ) -> "LocalVectorStore":
        texts = [document.page_content for document in documents]
        vectors = embeddings.embed_documents(texts)
        chunks = [
            IndexedChunk(
                chunk_id=str(document.metadata["chunk_id"]),
                source_path=str(document.metadata["source_path"]),
                text=document.page_content,
                vector=vector,
            )
            for document, vector in zip(documents, vectors)
        ]
        return cls(chunks)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"chunks": [asdict(chunk) for chunk in self.chunks]}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "LocalVectorStore":
        payload = json.loads(path.read_text(encoding="utf-8"))
        chunks = [IndexedChunk(**item) for item in payload["chunks"]]
        return cls(chunks)

    def search(
        self,
        query: str,
        embeddings: Embeddings,
        top_k: int,
    ) -> list[SearchResult]:
        query_vector = embeddings.embed_query(query)
        scored = [
            SearchResult(
                chunk_id=chunk.chunk_id,
                source_path=chunk.source_path,
                text=chunk.text,
                score=cosine_similarity(query_vector, chunk.vector),
            )
            for chunk in self.chunks
        ]
        scored.sort(key=lambda result: result.score, reverse=True)
        return scored[:top_k]
```

Create `engineering-knowledge-rag/data/indexes/.gitkeep` as an empty file.

- [ ] **Step 5: Run vector store tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_vectorstore.py -v
```

Expected: both tests pass.

- [ ] **Step 6: Run all current tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_config.py tests/test_documents.py tests/test_vectorstore.py -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit embeddings and vector store**

```bash
git add engineering-knowledge-rag/src/engineering_knowledge_rag/embeddings.py \
  engineering-knowledge-rag/src/engineering_knowledge_rag/vectorstore.py \
  engineering-knowledge-rag/tests/test_vectorstore.py \
  engineering-knowledge-rag/data/indexes/.gitkeep
git commit -m "feat: add local vector index"
```

### Task 4: Graph State And Citation Governance

**Files:**
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py`
- Create: `engineering-knowledge-rag/tests/test_citations.py`
- Create: `engineering-knowledge-rag/tests/test_graph_state.py`

**Interfaces:**
- Consumes:
  - `SearchResult`
- Produces:
  - `KnowledgeRagState`
  - `RetrievedDoc`
  - `create_initial_state(question: str) -> KnowledgeRagState`
  - `extract_citations(answer: str) -> list[str]`
  - `verify_citation_sources(answer: str, docs: Sequence[RetrievedDoc]) -> tuple[list[str], list[str]]`
  - `decide_final_response(state: KnowledgeRagState) -> KnowledgeRagState`

- [ ] **Step 1: Write failing citation tests**

Create `engineering-knowledge-rag/tests/test_citations.py` with:

```python
from engineering_knowledge_rag.graph import RetrievedDoc, extract_citations, verify_citation_sources


def test_extract_citations_from_answer_text():
    answer = "Agent Loop 的核心在于工具调用和结果回灌。[agent-loop/README.md] 也记录了 max_steps 护栏。[CLAUDE.md]"

    assert extract_citations(answer) == ["agent-loop/README.md", "CLAUDE.md"]


def test_verify_citation_sources_accepts_retrieved_sources():
    docs = [
        RetrievedDoc(
            chunk_id="agent-loop/README.md#0000",
            source_path="agent-loop/README.md",
            text="Agent Loop",
            score=0.9,
        )
    ]

    citations, warnings = verify_citation_sources("参考 [agent-loop/README.md]", docs)

    assert citations == ["agent-loop/README.md"]
    assert warnings == []


def test_verify_citation_sources_flags_fabricated_sources():
    docs = [
        RetrievedDoc(
            chunk_id="README.md#0000",
            source_path="README.md",
            text="Root README",
            score=0.8,
        )
    ]

    citations, warnings = verify_citation_sources("参考 [missing.md]", docs)

    assert citations == ["missing.md"]
    assert warnings == ["引用来源不在召回文档中: missing.md"]
```

- [ ] **Step 2: Write failing graph state tests**

Create `engineering-knowledge-rag/tests/test_graph_state.py` with:

```python
from engineering_knowledge_rag.graph import create_initial_state, decide_final_response


def test_create_initial_state_contains_required_fields():
    state = create_initial_state("这个仓库怎么学 Agent？")

    assert state["question"] == "这个仓库怎么学 Agent？"
    assert state["rewritten_query"] == ""
    assert state["retrieved_docs"] == []
    assert state["graded_docs"] == []
    assert state["answer"] == ""
    assert state["citations"] == []
    assert state["confidence"] == 0.0
    assert state["warnings"] == []
    assert state["trace_metadata"] == {}


def test_decide_final_response_refuses_when_no_documents_pass_grading():
    state = create_initial_state("怎么做饭？")

    decided = decide_final_response(state)

    assert decided["confidence"] == 0.0
    assert "无法回答" in decided["answer"]
    assert "没有足够的仓库文档证据" in decided["warnings"]
```

- [ ] **Step 3: Run citation and graph state tests to verify they fail**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_citations.py tests/test_graph_state.py -v
```

Expected: fail because `graph.py` does not exist.

- [ ] **Step 4: Implement graph state and citation helpers**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py` with:

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Sequence, TypedDict


@dataclass(frozen=True)
class RetrievedDoc:
    chunk_id: str
    source_path: str
    text: str
    score: float


class KnowledgeRagState(TypedDict):
    question: str
    rewritten_query: str
    retrieved_docs: list[RetrievedDoc]
    graded_docs: list[RetrievedDoc]
    answer: str
    citations: list[str]
    confidence: float
    warnings: list[str]
    trace_metadata: dict[str, Any]


def create_initial_state(question: str) -> KnowledgeRagState:
    return {
        "question": question,
        "rewritten_query": "",
        "retrieved_docs": [],
        "graded_docs": [],
        "answer": "",
        "citations": [],
        "confidence": 0.0,
        "warnings": [],
        "trace_metadata": {},
    }


def extract_citations(answer: str) -> list[str]:
    return re.findall(r"\[([A-Za-z0-9_./-]+\.(?:md|html))\]", answer)


def verify_citation_sources(
    answer: str,
    docs: Sequence[RetrievedDoc],
) -> tuple[list[str], list[str]]:
    citations = extract_citations(answer)
    valid_sources = {doc.source_path for doc in docs}
    warnings = [
        f"引用来源不在召回文档中: {citation}"
        for citation in citations
        if citation not in valid_sources
    ]
    if answer.strip() and not citations:
        warnings.append("答案缺少引用来源")
    return citations, warnings


def decide_final_response(state: KnowledgeRagState) -> KnowledgeRagState:
    if not state["graded_docs"]:
        return {
            **state,
            "answer": "根据当前知识库资料，无法回答这个问题。请确认问题是否属于仓库文档范围，或重新运行索引。",
            "confidence": 0.0,
            "warnings": [*state["warnings"], "没有足够的仓库文档证据"],
        }

    if state["warnings"]:
        return {
            **state,
            "confidence": min(state["confidence"], 0.4),
        }

    return state
```

- [ ] **Step 5: Run citation and graph state tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_citations.py tests/test_graph_state.py -v
```

Expected: all 5 tests pass.

- [ ] **Step 6: Run all current tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests -v
```

Expected: all current tests pass.

- [ ] **Step 7: Commit graph state and citation governance**

```bash
git add engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py \
  engineering-knowledge-rag/tests/test_citations.py \
  engineering-knowledge-rag/tests/test_graph_state.py
git commit -m "feat: add graph state and citation checks"
```

### Task 5: Provider Factories And LangGraph Workflow

**Files:**
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/llms.py`
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/prompts.py`
- Modify: `engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py`
- Modify: `engineering-knowledge-rag/tests/test_graph_state.py`

**Interfaces:**
- Consumes:
  - `AppSettings`
  - `LocalVectorStore`
  - `SearchResult`
  - `RetrievedDoc`
  - `create_embeddings(settings)`
- Produces:
  - `create_chat_model(settings: AppSettings) -> BaseChatModel`
  - `RagRuntime`
  - `rewrite_query_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState`
  - `retrieve_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState`
  - `grade_documents_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState`
  - `generate_answer_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState`
  - `verify_citations_node(state: KnowledgeRagState) -> KnowledgeRagState`
  - `build_graph(runtime: RagRuntime)`
  - `run_rag(question: str, runtime: RagRuntime) -> KnowledgeRagState`

- [ ] **Step 1: Extend graph tests for runtime workflow with fakes**

Replace `engineering-knowledge-rag/tests/test_graph_state.py` with:

```python
from dataclasses import dataclass

from engineering_knowledge_rag.graph import (
    RagRuntime,
    RetrievedDoc,
    create_initial_state,
    decide_final_response,
    grade_documents_node,
    run_rag,
)


class FakeChatModel:
    def invoke(self, messages):
        content = str(messages[-1].content)
        if "改写" in content or "rewrite" in content.lower():
            return type("Message", (), {"content": "AiFlowScript Agent Loop 学习路线"})()
        return type(
            "Message",
            (),
            {"content": "这个仓库先通过 Agent Loop 理解工具调用和结果回灌。[agent-loop/README.md]"},
        )()


@dataclass
class FakeStore:
    docs: list[RetrievedDoc]

    def search(self, query, embeddings, top_k):
        return self.docs[:top_k]


class FakeEmbeddings:
    def embed_query(self, text):
        return [1.0]

    def embed_documents(self, texts):
        return [[1.0] for _ in texts]


def test_create_initial_state_contains_required_fields():
    state = create_initial_state("这个仓库怎么学 Agent？")

    assert state["question"] == "这个仓库怎么学 Agent？"
    assert state["rewritten_query"] == ""
    assert state["retrieved_docs"] == []
    assert state["graded_docs"] == []
    assert state["answer"] == ""
    assert state["citations"] == []
    assert state["confidence"] == 0.0
    assert state["warnings"] == []
    assert state["trace_metadata"] == {}


def test_decide_final_response_refuses_when_no_documents_pass_grading():
    state = create_initial_state("怎么做饭？")

    decided = decide_final_response(state)

    assert decided["confidence"] == 0.0
    assert "无法回答" in decided["answer"]
    assert "没有足够的仓库文档证据" in decided["warnings"]


def test_grade_documents_node_filters_by_relevance_score():
    runtime = RagRuntime(
        llm=FakeChatModel(),
        embeddings=FakeEmbeddings(),
        vector_store=FakeStore([]),
        top_k=3,
        min_relevance_score=0.5,
    )
    state = {
        **create_initial_state("Agent Loop 是什么？"),
        "retrieved_docs": [
            RetrievedDoc("a#0000", "a.md", "relevant", 0.8),
            RetrievedDoc("b#0000", "b.md", "weak", 0.1),
        ],
    }

    result = grade_documents_node(state, runtime)

    assert [doc.source_path for doc in result["graded_docs"]] == ["a.md"]
    assert result["confidence"] == 0.8


def test_run_rag_returns_answer_with_valid_citation():
    runtime = RagRuntime(
        llm=FakeChatModel(),
        embeddings=FakeEmbeddings(),
        vector_store=FakeStore(
            [
                RetrievedDoc(
                    chunk_id="agent-loop/README.md#0000",
                    source_path="agent-loop/README.md",
                    text="Agent Loop 通过工具调用和结果回灌完成任务。",
                    score=0.9,
                )
            ]
        ),
        top_k=3,
        min_relevance_score=0.2,
    )

    result = run_rag("这个仓库怎么学 Agent？", runtime)

    assert "Agent Loop" in result["answer"]
    assert result["citations"] == ["agent-loop/README.md"]
    assert result["warnings"] == []
    assert result["confidence"] == 0.9
```

- [ ] **Step 2: Run graph tests to verify new failures**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_graph_state.py -v
```

Expected: fail because `RagRuntime`, workflow nodes, and `run_rag` are not implemented yet.

- [ ] **Step 3: Implement chat model factory**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/llms.py` with:

```python
from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from engineering_knowledge_rag.config import AppSettings


def create_chat_model(settings: AppSettings) -> BaseChatModel:
    if settings.model_provider == "ollama":
        return ChatOllama(
            model=settings.ollama_chat_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )

    return ChatOpenAI(
        model=settings.openai_chat_model,
        base_url=settings.openai_base_url,
        api_key=settings.openai_api_key,
        temperature=0,
    )
```

- [ ] **Step 4: Implement prompt templates**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/prompts.py` with:

```python
from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate


REWRITE_QUERY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是工程知识库检索助手。把用户问题改写成适合检索仓库文档的短查询。只输出查询本身。",
        ),
        ("human", "请改写这个问题用于检索: {question}"),
    ]
)


ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是工程知识库 RAG Agent。只能基于给定上下文回答。"
            "每个关键结论都要引用来源，引用格式必须是 [source_path]。"
            "如果上下文证据不足，明确说明无法基于当前知识库回答。",
        ),
        (
            "human",
            "问题: {question}\n\n改写后的检索 query: {rewritten_query}\n\n上下文:\n{context}\n\n请给出中文答案。",
        ),
    ]
)
```

- [ ] **Step 5: Extend `graph.py` with workflow nodes and LangGraph builder**

Replace `engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py` with:

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Protocol, Sequence, TypedDict

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from engineering_knowledge_rag.prompts import ANSWER_PROMPT, REWRITE_QUERY_PROMPT
from engineering_knowledge_rag.vectorstore import LocalVectorStore


@dataclass(frozen=True)
class RetrievedDoc:
    chunk_id: str
    source_path: str
    text: str
    score: float


class SearchableStore(Protocol):
    def search(self, query: str, embeddings: Embeddings, top_k: int):
        raise NotImplementedError


@dataclass(frozen=True)
class RagRuntime:
    llm: BaseChatModel
    embeddings: Embeddings
    vector_store: LocalVectorStore | SearchableStore
    top_k: int
    min_relevance_score: float


class KnowledgeRagState(TypedDict):
    question: str
    rewritten_query: str
    retrieved_docs: list[RetrievedDoc]
    graded_docs: list[RetrievedDoc]
    answer: str
    citations: list[str]
    confidence: float
    warnings: list[str]
    trace_metadata: dict[str, Any]


def create_initial_state(question: str) -> KnowledgeRagState:
    return {
        "question": question,
        "rewritten_query": "",
        "retrieved_docs": [],
        "graded_docs": [],
        "answer": "",
        "citations": [],
        "confidence": 0.0,
        "warnings": [],
        "trace_metadata": {},
    }


def extract_citations(answer: str) -> list[str]:
    return re.findall(r"\[([A-Za-z0-9_./-]+\.(?:md|html))\]", answer)


def verify_citation_sources(
    answer: str,
    docs: Sequence[RetrievedDoc],
) -> tuple[list[str], list[str]]:
    citations = extract_citations(answer)
    valid_sources = {doc.source_path for doc in docs}
    warnings = [
        f"引用来源不在召回文档中: {citation}"
        for citation in citations
        if citation not in valid_sources
    ]
    if answer.strip() and not citations:
        warnings.append("答案缺少引用来源")
    return citations, warnings


def _message_content(message: Any) -> str:
    content = getattr(message, "content", message)
    if isinstance(content, list):
        return "\n".join(str(item) for item in content)
    return str(content).strip()


def rewrite_query_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState:
    prompt_value = REWRITE_QUERY_PROMPT.invoke({"question": state["question"]})
    response = runtime.llm.invoke(prompt_value.messages)
    rewritten_query = _message_content(response) or state["question"]
    return {
        **state,
        "rewritten_query": rewritten_query,
        "trace_metadata": {**state["trace_metadata"], "rewrite_query": rewritten_query},
    }


def retrieve_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState:
    query = state["rewritten_query"] or state["question"]
    results = runtime.vector_store.search(query, runtime.embeddings, runtime.top_k)
    docs = [
        RetrievedDoc(
            chunk_id=result.chunk_id,
            source_path=result.source_path,
            text=result.text,
            score=result.score,
        )
        for result in results
    ]
    return {
        **state,
        "retrieved_docs": docs,
        "trace_metadata": {**state["trace_metadata"], "retrieved_count": len(docs)},
    }


def grade_documents_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState:
    graded_docs = [
        doc
        for doc in state["retrieved_docs"]
        if doc.score >= runtime.min_relevance_score
    ]
    confidence = max((doc.score for doc in graded_docs), default=0.0)
    return {
        **state,
        "graded_docs": graded_docs,
        "confidence": confidence,
        "trace_metadata": {**state["trace_metadata"], "graded_count": len(graded_docs)},
    }


def _format_context(docs: Sequence[RetrievedDoc]) -> str:
    return "\n\n".join(
        f"Source: {doc.source_path}\nChunk: {doc.chunk_id}\nScore: {doc.score:.4f}\nContent:\n{doc.text}"
        for doc in docs
    )


def generate_answer_node(state: KnowledgeRagState, runtime: RagRuntime) -> KnowledgeRagState:
    if not state["graded_docs"]:
        return state

    prompt_value = ANSWER_PROMPT.invoke(
        {
            "question": state["question"],
            "rewritten_query": state["rewritten_query"],
            "context": _format_context(state["graded_docs"]),
        }
    )
    response = runtime.llm.invoke(prompt_value.messages)
    answer = _message_content(response)
    return {
        **state,
        "answer": answer,
        "trace_metadata": {**state["trace_metadata"], "answer_length": len(answer)},
    }


def verify_citations_node(state: KnowledgeRagState) -> KnowledgeRagState:
    citations, citation_warnings = verify_citation_sources(state["answer"], state["graded_docs"])
    return {
        **state,
        "citations": citations,
        "warnings": [*state["warnings"], *citation_warnings],
    }


def decide_final_response(state: KnowledgeRagState) -> KnowledgeRagState:
    if not state["graded_docs"]:
        return {
            **state,
            "answer": "根据当前知识库资料，无法回答这个问题。请确认问题是否属于仓库文档范围，或重新运行索引。",
            "confidence": 0.0,
            "warnings": [*state["warnings"], "没有足够的仓库文档证据"],
        }

    if state["warnings"]:
        return {
            **state,
            "confidence": min(state["confidence"], 0.4),
        }

    return state


def build_graph(runtime: RagRuntime):
    graph = StateGraph(KnowledgeRagState)
    graph.add_node("rewrite_query", lambda state: rewrite_query_node(state, runtime))
    graph.add_node("retrieve", lambda state: retrieve_node(state, runtime))
    graph.add_node("grade_documents", lambda state: grade_documents_node(state, runtime))
    graph.add_node("generate_answer", lambda state: generate_answer_node(state, runtime))
    graph.add_node("verify_citations", verify_citations_node)
    graph.add_node("decide_final_response", decide_final_response)

    graph.add_edge(START, "rewrite_query")
    graph.add_edge("rewrite_query", "retrieve")
    graph.add_edge("retrieve", "grade_documents")
    graph.add_edge("grade_documents", "generate_answer")
    graph.add_edge("generate_answer", "verify_citations")
    graph.add_edge("verify_citations", "decide_final_response")
    graph.add_edge("decide_final_response", END)

    return graph.compile()


def run_rag(question: str, runtime: RagRuntime) -> KnowledgeRagState:
    compiled = build_graph(runtime)
    return compiled.invoke(create_initial_state(question))
```

- [ ] **Step 6: Run graph workflow tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_graph_state.py tests/test_citations.py -v
```

Expected: all graph and citation tests pass.

- [ ] **Step 7: Run all current tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests -v
```

Expected: all current tests pass.

- [ ] **Step 8: Commit providers and workflow**

```bash
git add engineering-knowledge-rag/src/engineering_knowledge_rag/llms.py \
  engineering-knowledge-rag/src/engineering_knowledge_rag/prompts.py \
  engineering-knowledge-rag/src/engineering_knowledge_rag/graph.py \
  engineering-knowledge-rag/tests/test_graph_state.py
git commit -m "feat: add langgraph rag workflow"
```

### Task 6: CLI Adapter For Doctor, Ingest, And Ask

**Files:**
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py`
- Modify: `engineering-knowledge-rag/tests/test_config.py`

**Interfaces:**
- Consumes:
  - `load_settings()`
  - `load_source_documents()`
  - `chunk_documents()`
  - `create_embeddings()`
  - `create_chat_model()`
  - `LocalVectorStore`
  - `RagRuntime`
  - `run_rag()`
- Produces:
  - Typer app object: `app`
  - CLI commands: `doctor`, `ingest`, `ask`

- [ ] **Step 1: Add CLI import smoke test**

Append to `engineering-knowledge-rag/tests/test_config.py`:

```python

def test_cli_app_imports():
    from engineering_knowledge_rag.cli import app

    assert app.info.name == "rag"
```

- [ ] **Step 2: Run CLI import test to verify it fails**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_config.py::test_cli_app_imports -v
```

Expected: fail because `cli.py` does not exist.

- [ ] **Step 3: Implement CLI commands**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py` with:

```python
from __future__ import annotations

import httpx
import typer
from rich.console import Console
from rich.table import Table

from engineering_knowledge_rag.config import AppSettings, apply_langsmith_environment, load_settings
from engineering_knowledge_rag.documents import chunk_documents, load_source_documents
from engineering_knowledge_rag.embeddings import create_embeddings
from engineering_knowledge_rag.graph import RagRuntime, run_rag
from engineering_knowledge_rag.llms import create_chat_model
from engineering_knowledge_rag.vectorstore import LocalVectorStore


app = typer.Typer(name="rag", help="Engineering knowledge base RAG Agent.")
console = Console()


def _provider_status(settings: AppSettings) -> tuple[str, str]:
    try:
        if settings.model_provider == "ollama":
            response = httpx.get(f"{settings.ollama_base_url.rstrip('/')}/api/tags", timeout=2.0)
            return ("ollama_connectivity", "ok" if response.is_success else f"http_{response.status_code}")

        if not settings.openai_api_key:
            return ("openai_connectivity", "missing_api_key")

        response = httpx.get(
            f"{settings.openai_base_url.rstrip('/')}/models",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            timeout=2.0,
        )
        return ("openai_connectivity", "ok" if response.is_success else f"http_{response.status_code}")
    except httpx.HTTPError as exc:
        return ("provider_connectivity", f"error: {exc.__class__.__name__}")


def _load_runtime(settings: AppSettings) -> RagRuntime:
    apply_langsmith_environment(settings)
    embeddings = create_embeddings(settings)
    vector_store = LocalVectorStore.load(settings.index_path)
    llm = create_chat_model(settings)
    return RagRuntime(
        llm=llm,
        embeddings=embeddings,
        vector_store=vector_store,
        top_k=settings.top_k,
        min_relevance_score=settings.min_relevance_score,
    )


@app.command()
def doctor() -> None:
    settings = load_settings()
    apply_langsmith_environment(settings)
    table = Table(title="RAG Doctor")
    table.add_column("Item")
    table.add_column("Value")
    table.add_column("Status")

    table.add_row("provider", settings.model_provider, "ok")
    table.add_row("repo_root", str(settings.repo_root), "ok" if settings.repo_root.exists() else "missing")
    table.add_row("index_path", str(settings.index_path), "ok" if settings.index_path.exists() else "missing")
    table.add_row("eval_path", str(settings.eval_path), "ok" if settings.eval_path.exists() else "missing")
    table.add_row("langsmith_project", settings.langsmith_project, "configured")
    table.add_row("langsmith_tracing", str(settings.langsmith_tracing).lower(), "configured")
    provider_item, provider_status = _provider_status(settings)
    table.add_row(provider_item, settings.model_provider, provider_status)

    if settings.model_provider == "openai" and not settings.openai_api_key:
        table.add_row("openai_api_key", "empty", "missing")

    console.print(table)


@app.command()
def ingest() -> None:
    settings = load_settings()
    apply_langsmith_environment(settings)
    source_documents = load_source_documents(settings.repo_root)
    chunks = chunk_documents(source_documents, settings.chunk_size, settings.chunk_overlap)
    embeddings = create_embeddings(settings)
    store = LocalVectorStore.from_documents(chunks, embeddings)
    store.save(settings.index_path)

    console.print(f"Indexed {len(chunks)} chunks from {len(source_documents)} documents.")
    console.print(f"Index written to {settings.index_path}")


@app.command()
def ask(question: str) -> None:
    settings = load_settings()
    apply_langsmith_environment(settings)
    if not settings.index_path.exists():
        raise typer.BadParameter(f"Index does not exist. Run `uv run rag ingest` first: {settings.index_path}")

    runtime = _load_runtime(settings)
    result = run_rag(question, runtime)

    console.print("\n[bold]Answer[/bold]")
    console.print(result["answer"])

    console.print("\n[bold]Citations[/bold]")
    if result["citations"]:
        for citation in result["citations"]:
            console.print(f"- {citation}")
    else:
        console.print("- none")

    console.print(f"\n[bold]Confidence[/bold] {result['confidence']:.4f}")

    if result["warnings"]:
        console.print("\n[bold yellow]Warnings[/bold yellow]")
        for warning in result["warnings"]:
            console.print(f"- {warning}")

    if result["trace_metadata"]:
        console.print("\n[bold]Trace Metadata[/bold]")
        for key, value in result["trace_metadata"].items():
            console.print(f"- {key}: {value}")
```

- [ ] **Step 4: Run CLI import test**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_config.py::test_cli_app_imports -v
```

Expected: test passes.

- [ ] **Step 5: Run doctor command**

Run:

```bash
cd engineering-knowledge-rag
uv run rag doctor
```

Expected: prints a `RAG Doctor` table. `index_path` can be `missing` before ingestion. Provider connectivity can be `ok`, `missing_api_key`, `http_<status>`, or `error: <ExceptionName>` depending on local setup.

- [ ] **Step 6: Run all current tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests -v
```

Expected: all current tests pass.

- [ ] **Step 7: Commit CLI adapter**

```bash
git add engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py \
  engineering-knowledge-rag/tests/test_config.py
git commit -m "feat: add rag cli adapter"
```

### Task 7: Smoke Eval Runner

**Files:**
- Create: `engineering-knowledge-rag/src/engineering_knowledge_rag/evals.py`
- Create: `engineering-knowledge-rag/tests/test_evals.py`
- Create: `engineering-knowledge-rag/data/evals/smoke.jsonl`
- Modify: `engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py`

**Interfaces:**
- Consumes:
  - `KnowledgeRagState`
  - `load_settings()`
  - `_load_runtime(settings)`
  - `run_rag(question, runtime)`
- Produces:
  - `EvalCase`
  - `EvalResult`
  - `load_eval_cases(path: Path) -> list[EvalCase]`
  - `evaluate_result(case: EvalCase, state: KnowledgeRagState) -> EvalResult`
  - CLI command: `uv run rag eval`

- [ ] **Step 1: Write failing eval tests**

Create `engineering-knowledge-rag/tests/test_evals.py` with:

```python
from pathlib import Path

from engineering_knowledge_rag.evals import EvalCase, evaluate_result, load_eval_cases
from engineering_knowledge_rag.graph import create_initial_state


def test_load_eval_cases_from_jsonl(tmp_path: Path):
    path = tmp_path / "smoke.jsonl"
    path.write_text(
        '{"id":"route","question":"仓库学习路线是什么？","expects_refusal":false}\\n'
        '{"id":"cooking","question":"怎么做饭？","expects_refusal":true}\\n',
        encoding="utf-8",
    )

    cases = load_eval_cases(path)

    assert cases == [
        EvalCase(id="route", question="仓库学习路线是什么？", expects_refusal=False),
        EvalCase(id="cooking", question="怎么做饭？", expects_refusal=True),
    ]


def test_evaluate_result_checks_answer_citation_and_refusal():
    case = EvalCase(id="route", question="仓库学习路线是什么？", expects_refusal=False)
    state = {
        **create_initial_state(case.question),
        "answer": "仓库通过 Agent Loop 入门。[agent-loop/README.md]",
        "citations": ["agent-loop/README.md"],
        "warnings": [],
        "confidence": 0.8,
    }

    result = evaluate_result(case, state)

    assert result.answer_present is True
    assert result.citation_present is True
    assert result.citation_valid is True
    assert result.refusal_correct is True


def test_evaluate_result_accepts_expected_refusal():
    case = EvalCase(id="cooking", question="怎么做饭？", expects_refusal=True)
    state = {
        **create_initial_state(case.question),
        "answer": "根据当前知识库资料，无法回答这个问题。",
        "citations": [],
        "warnings": ["没有足够的仓库文档证据"],
        "confidence": 0.0,
    }

    result = evaluate_result(case, state)

    assert result.refusal_correct is True
```

- [ ] **Step 2: Run eval tests to verify they fail**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_evals.py -v
```

Expected: fail because `evals.py` does not exist.

- [ ] **Step 3: Implement eval logic**

Create `engineering-knowledge-rag/src/engineering_knowledge_rag/evals.py` with:

```python
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from engineering_knowledge_rag.graph import KnowledgeRagState


@dataclass(frozen=True)
class EvalCase:
    id: str
    question: str
    expects_refusal: bool


@dataclass(frozen=True)
class EvalResult:
    id: str
    answer_present: bool
    citation_present: bool
    citation_valid: bool
    refusal_correct: bool

    @property
    def passed(self) -> bool:
        return all(
            [
                self.answer_present,
                self.citation_valid,
                self.refusal_correct,
            ]
        )


def load_eval_cases(path: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        cases.append(
            EvalCase(
                id=payload["id"],
                question=payload["question"],
                expects_refusal=bool(payload["expects_refusal"]),
            )
        )
    return cases


def evaluate_result(case: EvalCase, state: KnowledgeRagState) -> EvalResult:
    answer_present = bool(state["answer"].strip())
    citation_present = bool(state["citations"])
    citation_valid = citation_present or case.expects_refusal
    refused = "无法回答" in state["answer"] or state["confidence"] == 0.0
    refusal_correct = refused if case.expects_refusal else not refused
    return EvalResult(
        id=case.id,
        answer_present=answer_present,
        citation_present=citation_present,
        citation_valid=citation_valid,
        refusal_correct=refusal_correct,
    )
```

- [ ] **Step 4: Add smoke eval dataset**

Create `engineering-knowledge-rag/data/evals/smoke.jsonl` with:

```jsonl
{"id":"learning_route","question":"这个仓库的 Agent 学习路线是什么？","expects_refusal":false}
{"id":"agent_loop_goal","question":"agent-loop 项目解决什么问题？","expects_refusal":false}
{"id":"framework_after_loop","question":"为什么这个仓库强调先理解 Agent Loop，再学习框架？","expects_refusal":false}
{"id":"resources","question":"仓库里有哪些 AI Agent 学习资源？","expects_refusal":false}
{"id":"fastapi_role","question":"fast-api-demo 在学习路线里承担什么角色？","expects_refusal":false}
{"id":"out_of_scope","question":"请给我一份川菜菜谱。","expects_refusal":true}
```

- [ ] **Step 5: Add `eval` command to CLI**

Append this import to `engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py`:

```python
from engineering_knowledge_rag.evals import evaluate_result, load_eval_cases
```

Append this command to `engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py`:

```python

@app.command(name="eval")
def run_eval() -> None:
    settings = load_settings()
    apply_langsmith_environment(settings)
    if not settings.index_path.exists():
        raise typer.BadParameter(f"Index does not exist. Run `uv run rag ingest` first: {settings.index_path}")

    runtime = _load_runtime(settings)
    cases = load_eval_cases(settings.eval_path)
    rows = []
    for case in cases:
        state = run_rag(case.question, runtime)
        rows.append(evaluate_result(case, state))

    table = Table(title="Smoke Eval")
    table.add_column("ID")
    table.add_column("Answer")
    table.add_column("Citation")
    table.add_column("Citation Valid")
    table.add_column("Refusal")
    table.add_column("Passed")

    for row in rows:
        table.add_row(
            row.id,
            str(row.answer_present),
            str(row.citation_present),
            str(row.citation_valid),
            str(row.refusal_correct),
            str(row.passed),
        )

    passed = sum(1 for row in rows if row.passed)
    console.print(table)
    console.print(f"Passed {passed}/{len(rows)} cases.")
```

- [ ] **Step 6: Run eval tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests/test_evals.py -v
```

Expected: all eval tests pass.

- [ ] **Step 7: Run all tests**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests -v
```

Expected: all tests pass.

- [ ] **Step 8: Commit eval runner**

```bash
git add engineering-knowledge-rag/src/engineering_knowledge_rag/evals.py \
  engineering-knowledge-rag/src/engineering_knowledge_rag/cli.py \
  engineering-knowledge-rag/tests/test_evals.py \
  engineering-knowledge-rag/data/evals/smoke.jsonl
git commit -m "feat: add smoke eval runner"
```

### Task 8: Documentation And Final Verification

**Files:**
- Create: `engineering-knowledge-rag/README.md`
- Create: `engineering-knowledge-rag/docs/architecture.md`
- Create: `engineering-knowledge-rag/docs/interview-notes.md`
- Create: `engineering-knowledge-rag/docs/eval-strategy.md`
- Modify: `README.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes:
  - implemented CLI commands
  - architecture from the approved design
- Produces:
  - user-facing project docs
  - interview talking points
  - root project index updates

- [ ] **Step 1: Create subproject README**

Create `engineering-knowledge-rag/README.md` with:

````markdown
# Engineering Knowledge RAG Agent

面向研发知识库的 RAG Agent，用一个可运行 CLI 项目实践 LangChain、LangGraph 和 LangSmith。

这个项目不是普通 RAG Demo。它把 RAG 拆成可观测、可评估、可治理的流程：query rewrite、retrieval、document grading、answer generation、citation verification 和 final response control。

## 快速开始

```bash
cd engineering-knowledge-rag
uv sync
cp .env.example .env
uv run rag doctor
uv run rag ingest
uv run rag ask "这个仓库的 Agent 学习路线是什么？"
uv run rag eval
```

默认使用 Ollama：

```env
MODEL_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=qwen3:14b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

也可以切换到 OpenAI-compatible API：

```env
MODEL_PROVIDER=openai
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-api-key
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## CLI 命令

| 命令 | 作用 |
| --- | --- |
| `uv run rag doctor` | 检查模型 provider、索引、eval 文件和 LangSmith 配置 |
| `uv run rag ingest` | 扫描 allowlist 文档并构建本地向量索引 |
| `uv run rag ask "问题"` | 执行 LangGraph RAG 工作流并输出答案、引用、置信度和 warnings |
| `uv run rag eval` | 运行 smoke eval，检查答案、引用和拒答行为 |

## 架构亮点

- LangChain 负责文档处理、embedding、prompt 和模型适配。
- LangGraph 把 RAG 过程拆成可调试状态机。
- LangSmith 记录每个节点 trace，用于 badcase 归因。
- 引用溯源是一等可靠性要求。
- 系统有低置信度和拒答路径，而不是任何问题都强行回答。
- CLI 是第一版 adapter，后续 FastAPI 可以复用同一套 graph。

## MVP 边界

第一版只索引仓库文档：

```text
README.md
CLAUDE.md
agent-loop/README.md
fast-api-demo/README.md
learning-resources/resources.md
docs/superpowers/specs/*.md
```

第一版不索引代码文件、PDF、网页，也不实现 FastAPI。

## 面试讲法

可以把项目讲成一个「面向研发团队知识库的可观测 RAG Agent」。重点说明：为什么把 RAG 拆成多个 LangGraph 节点，如何做引用校验，如何通过 LangSmith 定位 badcase，以及如何从 CLI adapter 演进到 FastAPI 服务。

更完整的面试材料见 `docs/interview-notes.md`。
````

- [ ] **Step 2: Create architecture doc**

Create `engineering-knowledge-rag/docs/architecture.md` with:

````markdown
# Architecture

## Framework Responsibilities

LangChain 负责组件层：

- 文档加载和文本切分
- embedding provider
- prompt template
- chat model adapter

LangGraph 负责工作流层：

```text
user question
  -> rewrite_query
  -> retrieve
  -> grade_documents
  -> generate_answer
  -> verify_citations
  -> decide_final_response
```

LangSmith 负责观测层：

- 记录每次 `ask` 的节点输入输出
- 支持 eval run 的 trace 对比
- 帮助判断 badcase 来自 query rewrite、retrieval、grading、generation 还是 citation verification

## Provider Boundary

`llms.py` 和 `embeddings.py` 隔离模型 provider 差异。`graph.py` 只依赖抽象后的 chat model、embedding 和 vector store。

本地开发可以用 Ollama 控制成本和保护资料。生产环境可以切到 OpenAI-compatible API 获得更稳定的效果。

## CLI To FastAPI Evolution

第一版 CLI 只是一层 adapter。未来 FastAPI 可以复用：

- `config.py`
- `documents.py`
- `embeddings.py`
- `llms.py`
- `vectorstore.py`
- `graph.py`
- `evals.py`

需要新增的只是 HTTP route、request schema、response schema、鉴权和服务化观测。
````

- [ ] **Step 3: Create interview notes**

Create `engineering-knowledge-rag/docs/interview-notes.md` with:

````markdown
# Interview Notes

## 30 秒版本

我做了一个面向研发知识库的 RAG Agent，用来回答开发者学习仓库里的项目结构、学习路线和技术资料问题。LangChain 负责文档处理和模型适配，LangGraph 把 RAG 拆成可调试状态机，LangSmith 记录每个节点 trace，用于定位 badcase。第一版是 CLI，核心 graph 不依赖入口层，后续可以接 FastAPI。

## 为什么不是普通 RAG Demo

普通 Demo 通常是 `retrieve -> answer`。这个项目增加了生产系统更关心的质量控制：

- query rewrite：降低问题和文档之间的词汇不匹配。
- document grading：减少无关 chunk 进入上下文。
- citation verification：防止模型编造来源。
- final response control：低置信度时拒答或提示重新索引。
- smoke eval：检查答案、引用和拒答行为。

## 面试官可能追问

### 为什么用 LangGraph

RAG 不是单次函数调用，而是多阶段状态流。LangGraph 可以让每个节点独立观测、测试和替换。坏答案出现时，可以定位问题发生在检索、过滤、生成还是引用校验。

### 为什么要引用校验

RAG 的可靠性不只取决于答案是否流畅，还取决于答案是否能追溯到证据。引用校验能发现模型编造来源，避免把无法追责的答案返回给用户。

### 如何处理低置信度

如果没有 chunk 通过 relevance threshold，系统返回拒答。如果答案缺少引用或引用无效，系统降低 confidence 并输出 warning。

### LangSmith 起什么作用

LangSmith 不是只看最终回答，而是看每个节点的输入输出。它可以帮助定位 badcase，并把 eval run 作为可回归记录保存下来。

### 上生产前还缺什么

- FastAPI 服务化和流式响应
- 鉴权、限流和成本控制
- 更完整的 eval 数据集
- LLM-as-judge 和人工标注 badcase
- 代码文件索引和权限控制
- 索引更新任务和版本管理
````

- [ ] **Step 4: Create eval strategy doc**

Create `engineering-knowledge-rag/docs/eval-strategy.md` with:

````markdown
# Eval Strategy

第一版使用 smoke eval，目标是验证 RAG Agent 的关键质量门槛，而不是追求完整 benchmark。

## 数据集

`data/evals/smoke.jsonl` 包含 6 个问题：

- 仓库学习路线
- `agent-loop` 项目目标
- 为什么先理解 Agent Loop
- 学习资源列表
- `fast-api-demo` 的角色
- 超范围问题拒答

## 指标

| 指标 | 含义 |
| --- | --- |
| `answer_present` | 是否生成答案 |
| `citation_present` | 是否有引用 |
| `citation_valid` | 引用是否满足当前规则 |
| `refusal_correct` | 超范围问题是否拒答，范围内问题是否没有误拒答 |

## 后续扩展

- 增加更多真实 badcase。
- 引入 LLM-as-judge 判断答案是否忠于上下文。
- 加入人工标注集作为黄金样本。
- 按 eval run 对比不同 chunk strategy、embedding model 和 relevance threshold。
````

- [ ] **Step 5: Update root README project table**

Modify root `README.md` in the `子项目` table by adding one row:

```markdown
| 🧠 [`engineering-knowledge-rag/`](./engineering-knowledge-rag) | A/B · RAG + Agent 编排 | 面向研发知识库的可观测 RAG Agent，用 LangChain 处理组件、LangGraph 编排状态机、LangSmith 做 trace 和 eval | [README](./engineering-knowledge-rag/README.md) |
```

- [ ] **Step 6: Update `CLAUDE.md` sub-project list**

Modify root `CLAUDE.md` under `## Sub-projects` by adding:

````markdown
### engineering-knowledge-rag/

主线 A/B 交汇项目：**工程知识库 RAG Agent**。第一版用 CLI 索引仓库文档并基于引用回答问题；LangChain 负责文档处理、embedding、prompt 和模型适配，LangGraph 负责编排 `rewrite_query -> retrieve -> grade_documents -> generate_answer -> verify_citations -> decide_final_response` 状态流，LangSmith 用于 trace 和 eval 对比。该项目的 README 与 `docs/interview-notes.md` 需要持续维护面试讲法和项目亮点。

Common commands (run from `engineering-knowledge-rag/`):

```bash
uv sync
uv run rag doctor
uv run rag ingest
uv run rag ask "这个仓库的 Agent 学习路线是什么？"
uv run rag eval
```
````

- [ ] **Step 7: Run final test suite**

Run:

```bash
cd engineering-knowledge-rag
uv run pytest tests -v
```

Expected: all tests pass.

- [ ] **Step 8: Run CLI doctor**

Run:

```bash
cd engineering-knowledge-rag
uv run rag doctor
```

Expected: prints the doctor table. Missing index is acceptable before `ingest`.

- [ ] **Step 9: Optional live ingest check**

Run only when either Ollama is running with `nomic-embed-text` available or OpenAI-compatible credentials are configured:

```bash
cd engineering-knowledge-rag
uv run rag ingest
uv run rag ask "这个仓库的 Agent 学习路线是什么？"
```

Expected: `ingest` writes `data/indexes/knowledge_index.json`; `ask` returns an answer, citations, confidence, warnings if any, and trace metadata.

- [ ] **Step 10: Commit docs and project index**

```bash
git add engineering-knowledge-rag/README.md \
  engineering-knowledge-rag/docs/architecture.md \
  engineering-knowledge-rag/docs/interview-notes.md \
  engineering-knowledge-rag/docs/eval-strategy.md \
  README.md \
  CLAUDE.md
git commit -m "docs: add engineering rag project guide"
```

## Final Verification

After all tasks are complete, run:

```bash
cd engineering-knowledge-rag
uv run pytest tests -v
uv run rag doctor
```

Expected:

- all tests pass
- doctor command prints provider, repo root, index path, eval path, and LangSmith project status

If model credentials or local Ollama are available, also run:

```bash
cd engineering-knowledge-rag
uv run rag ingest
uv run rag ask "这个仓库的 Agent 学习路线是什么？"
uv run rag eval
```

Expected:

- index file is generated under `engineering-knowledge-rag/data/indexes/knowledge_index.json`
- `ask` returns a cited answer
- `eval` prints a smoke eval table
