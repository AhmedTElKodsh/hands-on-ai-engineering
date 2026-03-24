

# 🔬 UNIFIED ANALYSIS & DEFINITIVE CURRICULUM

## Based on: Gemini Strategic Framework + BMad Repo Analysis + Repo Structure

---

# PART A: CRITICAL ANALYSIS — RECONCILING YOUR TWO PLANS

After thoroughly analyzing both documents, here's what I found:

## ✅ Where They Agree (Strong Foundation)

| Dimension | Gemini Plan | BMad/Repo Plan | Verdict |
|-----------|-------------|----------------|---------|
| **Focus** | AI Engineering (not ML research) | GenAI Engineer role | ✅ Aligned |
| **Approach** | Project-centric, build-while-learning | Two Flagship projects | ✅ Aligned |
| **Core Stack** | RAG, Agents, LLM APIs, Vector DBs | RAG Platform + AI Agent System | ✅ Aligned |
| **Production Focus** | Hyperscale, observability, fallbacks | Production Engineering weeks 17-22 | ✅ Aligned |
| **Egyptian Context** | Local ecosystem, Arabic NLP | Implicit (Ahmed in Cairo) | ✅ Aligned |

## ⚠️ Where They Conflict (Must Resolve)

| Dimension | Gemini Plan | BMad/Repo Plan | **Resolution** |
|-----------|-------------|----------------|----------------|
| **Daily Time** | 30 min/day | 4 hrs/day (80/120/40) | **Use 4-hr as primary; 30-min for theory-only days** |
| **Duration** | 90 days | 28 weeks (196 days) | **28 weeks is realistic; 90 days was aspirational** |
| **Start Point** | Assumes some coding ability | SQL Week 1, Backend-first | **Follow repo: start with SQL + Python backend** |
| **Classical ML** | Minimal (not the focus) | Not emphasized | **Include as "just enough" — 1 week max** |
| **Deep Learning** | Skip training from scratch | Not in curriculum | **Correct — understand architectures, don't train** |

## 🚨 Critical Insight: What the Gemini Plan Gets RIGHT That My Original Answer Got WRONG

My original 90-day curriculum had you spending **21 days on Python basics and math** and **21 days on classical deep learning (CNNs, RNNs from scratch)**. The Gemini plan correctly argues:

> *"The industry has transitioned from training foundational models from scratch to the era of AI engineering. The focal point of value creation has definitively moved toward the application layer."*

**Translation:** You should NOT spend 3 weeks implementing neural networks from scratch. You should spend that time **building RAG systems, AI agents, and production APIs.** The BMad repo plan agrees — there's no "build a CNN" week.

---

# PART B: THE DEFINITIVE 28-WEEK CURRICULUM

## Aligned with Layer1-Final + Gemini Strategic Framework

### 📐 Daily Time Budget (The 80/120/40 Split)

| Block | Duration | Activity | Gemini Principle |
|-------|----------|----------|-----------------|
| **🧠 Learn** | 80 min | Video + reading (multimodal) | Modality Principle — use audio/visual, not just text |
| **💻 Build** | 120 min | Code on Flagship projects | Interactive/kinesthetic — highest retention |
| **📝 Document** | 40 min | Notes, commit, journal | Spaced repetition — active recall |
| **Total** | **4 hrs/day** | 5 days/week = **20 hrs/week** | |

### 🎯 For 30-Min-Only Days (Busy Days)
Use the Gemini plan's nano-learning approach:
- **10 min**: Watch one concept video (3Blue1Brown, StatQuest, or Fireship)
- **15 min**: Write/modify ONE function in your Flagship project
- **5 min**: Commit with descriptive message + 1-sentence journal entry

---

---

# WEEKS 1–4: ENGINEERING FOUNDATIONS + LLM CLIENT

---

## 📅 WEEK 1: SQL + Python Backend Fundamentals

> **Repo path:** `Layer1-Final/week-01/`
> **Flagship tie-in:** Setting up the data layer for both projects

---

### Day 1 (Mon) — Environment Setup + SQL Fundamentals

**🧠 Learn (80 min):**
- 🎥 [CS50 SQL — Full Course](https://www.youtube.com/watch?v=YzP164YANAU) — Watch first 90 min (1.5x speed = 60 min)
- 📖 [SQLBolt — Interactive SQL Tutorial (Lessons 1-6)](https://sqlbolt.com/) — 20 min

**💻 Build (120 min):**
```sql
-- Set up PostgreSQL locally (or use SQLite for speed)
-- Exercise 1.1: Create your first database schema for the RAG Platform
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    chunk_index INTEGER,
    embedding_id TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    role TEXT CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tokens_used INTEGER,
    model TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Exercise 1.2: Write 10 queries
-- SELECT, WHERE, JOIN, GROUP BY, ORDER BY, HAVING
-- INSERT sample data and query it

-- Exercise 1.3: Write a query to find the most active conversations
-- (most messages) in the last 7 days
```

**📝 Document (40 min):**
- Install tools: Python 3.11+, VS Code, Git, PostgreSQL (or SQLite)
- Clone repo: `git clone https://github.com/AhmedTElKodsh/hands-on-ai-engineering`
- Run: `Layer1-Final/guides/DAY-00-DIAGNOSTIC.py`
- Journal: What did the diagnostic reveal? What are your gaps?

**📎 Setup Checklist:**
```bash
# Required installations
python --version          # 3.11+
git --version             # 2.x
pip install uv            # Fast package manager
uv venv .venv             # Create virtual environment
source .venv/bin/activate
uv pip install pytest httpx sqlalchemy alembic python-dotenv
```

---

### Day 2 (Tue) — Advanced SQL + Python-SQL Integration

**🧠 Learn (80 min):**
- 🎥 [SQLAlchemy Tutorial — Pretty Printed](https://www.youtube.com/watch?v=AKQ3XEDI9Mw) — 40 min
- 📖 [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) — 40 min

**💻 Build (120 min):**
```python
# Exercise 2.1: Build a database module for Flagship #1 (RAG Platform)
# File: src/database/models.py

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    chunks = relationship("Chunk", back_populates="document")

class Chunk(Base):
    __tablename__ = 'chunks'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer)
    embedding_id = Column(String(100))
    
    document = relationship("Document", back_populates="chunks")

# Exercise 2.2: CRUD operations
class DocumentRepository:
    def __init__(self, session):
        self.session = session
    
    def create(self, title: str, content: str, source_url: str = None) -> Document:
        doc = Document(title=title, content=content, source_url=source_url)
        self.session.add(doc)
        self.session.commit()
        return doc
    
    def get_by_id(self, doc_id: int) -> Document | None:
        return self.session.query(Document).filter_by(id=doc_id).first()
    
    def search(self, query: str) -> list[Document]:
        return self.session.query(Document).filter(
            Document.content.ilike(f'%{query}%')
        ).all()
    
    def delete(self, doc_id: int) -> bool:
        doc = self.get_by_id(doc_id)
        if doc:
            self.session.delete(doc)
            self.session.commit()
            return True
        return False

# Exercise 2.3: Database initialization script
def init_db(database_url: str = "sqlite:///rag_platform.db"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
```

**📝 Document (40 min):**
- Write a `README.md` for the database module
- Commit: `git commit -m "Week 1 Day 2: Database models and repository pattern"`

---

### Day 3 (Wed) — Python Backend: HTTP, APIs, async

**🧠 Learn (80 min):**
- 🎥 [FastAPI Full Course — freeCodeCamp](https://www.youtube.com/watch?v=0sOvCWFmrtA) — Watch first 80 min at 1.5x
- 📖 [FastAPI Tutorial — First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

**💻 Build (120 min):**
```python
# Exercise 3.1: Create a basic FastAPI app for your RAG Platform
# File: src/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="RAG Platform API",
    description="Flagship Project #1 — Hands-On AI Engineering",
    version="0.1.0"
)

# --- Pydantic Models (Request/Response schemas) ---
class DocumentCreate(BaseModel):
    title: str
    content: str
    source_url: str | None = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    source_url: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

# --- Endpoints ---
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.utcnow()
    )

@app.post("/documents", response_model=DocumentResponse, status_code=201)
async def create_document(doc: DocumentCreate):
    # TODO: Wire to database repository (Exercise for you!)
    pass

@app.get("/documents/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: int):
    # TODO: Implement
    pass

@app.get("/documents", response_model=list[DocumentResponse])
async def list_documents(skip: int = 0, limit: int = 20):
    # TODO: Implement with pagination
    pass

# Exercise 3.2: Run it
# uvicorn src.api.main:app --reload
# Visit http://localhost:8000/docs for auto-generated Swagger UI

# Exercise 3.3: Write an HTTP client to test your API
import httpx

async def test_api():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Health check
        response = await client.get("/health")
        assert response.status_code == 200
        
        # Create document
        response = await client.post("/documents", json={
            "title": "Test Document",
            "content": "This is a test document for our RAG platform."
        })
        assert response.status_code == 201
```

**📝 Document (40 min):**
- Document the API endpoints in README
- Commit with descriptive message

---

### Day 4 (Thu) — Testing from Day One

**🧠 Learn (80 min):**
- 🎥 [Pytest Tutorial — ArjanCodes](https://www.youtube.com/watch?v=cHYq1MRoyI0) — 40 min
- 📖 [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/) — 20 min
- 📖 [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html) — 20 min

**💻 Build (120 min):**
```python
# File: tests/test_database.py
import pytest
from src.database.models import init_db, DocumentRepository, Document

@pytest.fixture
def db_session():
    """Create a fresh test database for each test."""
    session = init_db("sqlite:///:memory:")
    yield session
    session.close()

@pytest.fixture
def repo(db_session):
    return DocumentRepository(db_session)

class TestDocumentRepository:
    def test_create_document(self, repo):
        doc = repo.create("Test Title", "Test Content")
        assert doc.id is not None
        assert doc.title == "Test Title"
    
    def test_get_by_id(self, repo):
        created = repo.create("Test", "Content")
        found = repo.get_by_id(created.id)
        assert found is not None
        assert found.title == "Test"
    
    def test_get_nonexistent_returns_none(self, repo):
        assert repo.get_by_id(999) is None
    
    def test_search(self, repo):
        repo.create("Python Guide", "Learn Python programming")
        repo.create("SQL Guide", "Learn SQL databases")
        results = repo.search("Python")
        assert len(results) == 1
        assert results[0].title == "Python Guide"
    
    def test_delete(self, repo):
        doc = repo.create("To Delete", "Content")
        assert repo.delete(doc.id) is True
        assert repo.get_by_id(doc.id) is None
    
    def test_delete_nonexistent(self, repo):
        assert repo.delete(999) is False

# File: tests/test_api.py
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

# Run: pytest tests/ -v
```

**📝 Document (40 min):**
- Set up `pytest.ini` or `pyproject.toml` for test configuration
- Create test coverage baseline: `pytest --cov=src tests/`

---

### Day 5 (Fri) — Git Workflow + Project Structure + Week 1 Integration

**🧠 Learn (80 min):**
- 🎥 [Git for Professionals — Fireship](https://www.youtube.com/watch?v=Uszj_k0DGsg) — 12 min
- 📖 [Conventional Commits](https://www.conventionalcommits.org/) — 10 min
- 📖 [Python Project Structure (Real Python)](https://realpython.com/python-application-layouts/) — 30 min
- 🎥 [Poetry/UV for Python Project Management](https://www.youtube.com/watch?v=0f3moPe_bhk) — 28 min

**💻 Build (120 min):**
```
# Exercise 5.1: Establish the canonical project structure
# for BOTH flagship projects

hands-on-ai-engineering/
├── Layer1-Final/
│   ├── week-01/
│   │   ├── exercises/          # Daily exercises
│   │   ├── notes/              # Learning journal
│   │   └── checkpoint.md       # Week 1 self-assessment
│   ├── week-02/
│   ├── ...
│   └── guides/
│       ├── DAY-00-DIAGNOSTIC.py
│       ├── GUIDE-FOR-AI-ASSISTANTS.md
│       └── MIGRATION-GUIDE.md
│
├── flagship-1-rag-platform/    # 🏗️ Flagship #1
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   └── routes/
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── repository.py
│   │   ├── ingestion/          # Document processing (Week 5+)
│   │   ├── retrieval/          # Vector search (Week 6+)
│   │   └── generation/         # LLM integration (Week 7+)
│   ├── tests/
│   │   ├── test_database.py
│   │   ├── test_api.py
│   │   └── test_ingestion.py
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── README.md
│
├── flagship-2-ai-agent/        # 🤖 Flagship #2 (Week 11+)
│   ├── src/
│   ├── tests/
│   └── README.md
│
├── _ARCHIVE_2026-03/           # Archived previous curricula
│   ├── Layer1-original/
│   ├── Layer2/
│   └── Modified/
│
└── README.md                   # Master progress tracker
```

```python
# Exercise 5.2: Create pyproject.toml
"""
[project]
name = "rag-platform"
version = "0.1.0"
description = "Flagship Project #1 — RAG Platform"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109",
    "uvicorn>=0.27",
    "sqlalchemy>=2.0",
    "python-dotenv>=1.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "pytest-asyncio>=0.23",
    "ruff>=0.2",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
"""

# Exercise 5.3: Create .env and config management
# File: src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///rag_platform.db"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # LLM settings (for later weeks)
    openai_api_key: str = ""
    default_model: str = "gpt-3.5-turbo"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**📝 Document (40 min):**
- Write master `README.md` with progress tracker
- Fill out `Layer1-Final/week-01/checkpoint.md`:
  - ✅ Can I create SQL tables and write JOINs?
  - ✅ Can I build SQLAlchemy models with relationships?
  - ✅ Can I create FastAPI endpoints with Pydantic validation?
  - ✅ Can I write pytest tests with fixtures?
  - ✅ Do I understand the repository pattern?
- Commit everything, push to GitHub

---

## 📅 WEEK 2: Python Mastery + First LLM API Call

> **Repo path:** `Layer1-Final/week-02/`
> **Flagship tie-in:** Adding LLM integration to RAG Platform

---

### Day 6 (Mon) — Python Intermediate: Decorators, Generators, Type Hints

**🧠 Learn (80 min):**
- 🎥 [Corey Schafer — Decorators](https://www.youtube.com/watch?v=FsAPt_9Bf3U) — 30 min
- 🎥 [ArjanCodes — Type Hints](https://www.youtube.com/watch?v=dgBCEB2jVU0) — 25 min
- 📖 [Real Python — Generators](https://realpython.com/introduction-to-python-generators/) — 25 min

**💻 Build (120 min):**
```python
# Exercise 6.1: Build utility decorators for the RAG Platform
# File: src/utils/decorators.py

import time
import functools
import logging
from typing import Callable, TypeVar, ParamSpec

logger = logging.getLogger(__name__)
P = ParamSpec('P')
T = TypeVar('T')

def timer(func: Callable[P, T]) -> Callable[P, T]:
    """Log execution time. Critical for LLM API calls."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} completed in {elapsed:.3f}s")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Retry with exponential backoff. Essential for LLM API resilience."""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(
                        f"{func.__name__} attempt {attempt+1}/{max_attempts} "
                        f"failed: {e}. Retrying in {current_delay}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def validate_not_empty(*param_names: str):
    """Validate that specified string parameters are not empty."""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name in param_names:
                value = bound.arguments.get(name)
                if not value or (isinstance(value, str) and not value.strip()):
                    raise ValueError(f"Parameter '{name}' must not be empty")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Exercise 6.2: Generator for batch processing documents
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """Yield overlapping text chunks. Core RAG operation."""
    words = text.split()
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        yield chunk
        start = end - overlap
        if start < 0:
            break

# Test it
sample_text = "word " * 2000
chunks = list(chunk_text(sample_text, chunk_size=100, overlap=20))
print(f"Generated {len(chunks)} chunks from {len(sample_text.split())} words")
for i, chunk in enumerate(chunks[:3]):
    print(f"  Chunk {i}: {len(chunk.split())} words")

# Exercise 6.3: Write tests for ALL decorators and the chunker
```

---

### Day 7 (Tue) — async/await + httpx (Async HTTP)

**🧠 Learn (80 min):**
- 🎥 [ArjanCodes — Async Python](https://www.youtube.com/watch?v=2IW-ZEui4h4) — 30 min
- 📖 [Real Python — Async IO](https://realpython.com/async-io-python/) — 30 min
- 📖 [httpx Documentation](https://www.python-httpx.org/) — 20 min

**💻 Build (120 min):**
```python
# Exercise 7.1: Build an async HTTP client wrapper
# File: src/utils/http_client.py

import httpx
from typing import Any
from src.utils.decorators import retry, timer

class AsyncHTTPClient:
    """Reusable async HTTP client with retry logic."""
    
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
    
    async def _request(
        self, method: str, path: str, 
        headers: dict | None = None, **kwargs
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(
            base_url=self.base_url, 
            timeout=self.timeout
        ) as client:
            response = await client.request(method, path, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
    
    async def get(self, path: str, **kwargs) -> dict:
        return await self._request("GET", path, **kwargs)
    
    async def post(self, path: str, **kwargs) -> dict:
        return await self._request("POST", path, **kwargs)

# Exercise 7.2: Build a basic LLM client (prepare for Day 8)
# File: src/llm/base_client.py

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LLMResponse:
    content: str
    model: str
    tokens_used: int
    latency_ms: float

class BaseLLMClient(ABC):
    """Abstract base for all LLM clients (OpenAI, Ollama, etc.)."""
    
    @abstractmethod
    async def chat(
        self, 
        messages: list[dict[str, str]], 
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> LLMResponse:
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass
```

---

### Day 8 (Wed) — 🎯 MILESTONE: First LLM API Call

**🧠 Learn (80 min):**
- 📖 [OpenAI API Quickstart](https://platform.openai.com/docs/quickstart) — 30 min
- 📖 [OpenAI Chat Completions Guide](https://platform.openai.com/docs/guides/text-generation) — 30 min
- 🎥 [Fireship — OpenAI API in 100 Seconds](https://www.youtube.com/watch?v=_j7JEDWuqLE) — 5 min
- 📖 [Anthropic Claude Quickstart](https://docs.anthropic.com/en/docs/quickstart) — 15 min

**💻 Build (120 min):**
```python
# Exercise 8.1: Implement OpenAI LLM Client
# File: src/llm/openai_client.py

import time
from openai import AsyncOpenAI
from src.llm.base_client import BaseLLMClient, LLMResponse
from src.config import settings

class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str | None = None):
        self.client = AsyncOpenAI(api_key=api_key or settings.openai_api_key)
        self.default_model = settings.default_model
    
    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> LLMResponse:
        start = time.perf_counter()
        
        response = await self.client.chat.completions.create(
            model=model or self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            tokens_used=response.usage.total_tokens,
            latency_ms=elapsed_ms
        )
    
    async def embed(self, text: str, model: str = "text-embedding-3-small") -> list[float]:
        response = await self.client.embeddings.create(
            model=model,
            input=[text]
        )
        return response.data[0].embedding

# Exercise 8.2: Your FIRST LLM call!
import asyncio

async def main():
    client = OpenAIClient()
    
    # Simple chat
    response = await client.chat(
        messages=[
            {"role": "system", "content": "You are a helpful AI engineering tutor."},
            {"role": "user", "content": "Explain RAG in 3 sentences for a software engineer."}
        ],
        temperature=0.3
    )
    
    print(f"Response: {response.content}")
    print(f"Model: {response.model}")
    print(f"Tokens: {response.tokens_used}")
    print(f"Latency: {response.latency_ms:.0f}ms")
    
    # First embedding
    embedding = await client.embed("What is retrieval-augmented generation?")
    print(f"\nEmbedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

asyncio.run(main())

# Exercise 8.3: Implement Ollama client as alternative
# File: src/llm/ollama_client.py (for local, free inference)
class OllamaClient(BaseLLMClient):
    """Local LLM via Ollama — zero cost, full privacy."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    async def chat(self, messages, model="llama3.1", **kwargs) -> LLMResponse:
        start = time.perf_counter()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={"model": model, "messages": messages, "stream": False}
            )
            data = response.json()
        elapsed_ms = (time.perf_counter() - start) * 1000
        return LLMResponse(
            content=data["message"]["content"],
            model=model,
            tokens_used=data.get("eval_count", 0),
            latency_ms=elapsed_ms
        )
    
    async def embed(self, text: str) -> list[float]:
        # TODO: Implement using Ollama embeddings endpoint
        pass

# Exercise 8.4: Build an LLM Factory (Strategy Pattern)
class LLMFactory:
    """Create the right LLM client based on config."""
    
    @staticmethod
    def create(provider: str = "openai") -> BaseLLMClient:
        match provider:
            case "openai":
                return OpenAIClient()
            case "ollama":
                return OllamaClient()
            case _:
                raise ValueError(f"Unknown provider: {provider}")
```

**📝 Document (40 min):**
- Record your first LLM response in your learning journal
- Note: latency, token usage, response quality
- Commit: `feat: implement LLM client abstraction with OpenAI and Ollama`

---

### Day 9 (Thu) — Prompt Engineering Fundamentals

**🧠 Learn (80 min):**
- 📖 [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) — 40 min
- 📖 [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — 25 min
- 🎥 [Prompt Engineering Overview — IBM](https://www.youtube.com/watch?v=_ZvnD96BPjU) — 15 min

**💻 Build (120 min):**
```python
# Exercise 9.1: Build a Prompt Template System
# File: src/llm/prompts.py

from dataclasses import dataclass, field
from typing import Any

@dataclass
class PromptTemplate:
    """Reusable prompt template with variable substitution."""
    
    template: str
    input_variables: list[str]
    name: str = ""
    description: str = ""
    
    def format(self, **kwargs) -> str:
        missing = set(self.input_variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing variables: {missing}")
        extra = set(kwargs.keys()) - set(self.input_variables)
        if extra:
            raise ValueError(f"Unexpected variables: {extra}")
        return self.template.format(**kwargs)

# Exercise 9.2: Build a Prompt Library for the RAG Platform
RAG_ANSWER_PROMPT = PromptTemplate(
    name="rag_answer",
    description="Answer a question using retrieved context",
    template="""You are a helpful assistant. Answer the user's question based ONLY 
on the provided context. If the context doesn't contain the answer, say 
"I don't have enough information to answer this question."

Context:
{context}

Question: {question}

Instructions:
- Be concise and accurate
- Cite which part of the context supports your answer
- If uncertain, express your uncertainty level""",
    input_variables=["context", "question"]
)

DOCUMENT_SUMMARY_PROMPT = PromptTemplate(
    name="doc_summary",
    template="""Summarize the following document in {max_sentences} sentences.
Focus on the key technical concepts and main arguments.

Document Title: {title}
Document Content:
{content}

Summary:""",
    input_variables=["content", "title", "max_sentences"]
)

# Exercise 9.3: Test different prompt patterns
CHAIN_OF_THOUGHT_PROMPT = PromptTemplate(
    name="cot_analysis",
    template="""Analyze this code for potential issues.

Code:
```{language}
{code}
```

Think step by step:
1. First, understand what the code is trying to do
2. Check for bugs or logical errors
3. Evaluate error handling
4. Assess performance implications
5. Suggest improvements

Analysis:""",
    input_variables=["language", "code"]
)

# Exercise 9.4: Build a Prompt Runner that logs everything
class PromptRunner:
    def __init__(self, llm_client: BaseLLMClient):
        self.client = llm_client
        self.history: list[dict] = []
    
    async def run(
        self, 
        template: PromptTemplate, 
        system_prompt: str = "You are a helpful assistant.",
        **kwargs
    ) -> LLMResponse:
        user_message = template.format(**kwargs)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = await self.client.chat(messages)
        
        # Log for observability
        self.history.append({
            "template": template.name,
            "inputs": kwargs,
            "response": response.content,
            "tokens": response.tokens_used,
            "latency_ms": response.latency_ms
        })
        
        return response
    
    def get_total_tokens(self) -> int:
        return sum(h["tokens"] for h in self.history)
    
    def get_average_latency(self) -> float:
        if not self.history:
            return 0
        return sum(h["latency_ms"] for h in self.history) / len(self.history)

# Exercise 9.5: Test with actual prompts — compare results
# Try: zero-shot vs few-shot vs chain-of-thought on same question
```

---

### Day 10 (Fri) — Week 2 Integration + Checkpoint

**🧠 Learn (80 min):**
- 📖 [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) — 40 min
- 🎥 [3Blue1Brown — But What is a GPT?](https://www.youtube.com/watch?v=wjZofJX0v4M) — 25 min
- 📖 [Tokenization Explained](https://platform.openai.com/tokenizer) — 15 min (play with the tokenizer)

**💻 Build (120 min):**
```python
# Exercise 10.1: Integration test — Full flow
# File: tests/test_integration.py

import pytest
import asyncio
from src.llm.openai_client import OpenAIClient
from src.llm.prompts import PromptRunner, RAG_ANSWER_PROMPT

@pytest.mark.asyncio
async def test_full_rag_flow():
    """Test: prompt template → LLM call → structured response."""
    client = OpenAIClient()
    runner = PromptRunner(client)
    
    context = """
    Retrieval-Augmented Generation (RAG) is a technique that combines 
    information retrieval with text generation. It works by first retrieving 
    relevant documents from a knowledge base, then using those documents 
    as context for a language model to generate accurate, grounded answers.
    """
    
    response = await runner.run(
        RAG_ANSWER_PROMPT,
        context=context,
        question="What is RAG and how does it work?"
    )
    
    assert response.content  # Not empty
    assert response.tokens_used > 0
    assert response.latency_ms > 0
    assert "retriev" in response.content.lower()  # Basic relevance check
    
    # Check runner stats
    assert runner.get_total_tokens() > 0
    assert len(runner.history) == 1

# Exercise 10.2: Build a simple CLI for your RAG platform
# File: src/cli.py
import asyncio
import click

@click.group()
def cli():
    """RAG Platform CLI"""
    pass

@cli.command()
@click.argument('question')
def ask(question: str):
    """Ask a question (without retrieval for now)."""
    async def _ask():
        from src.llm.openai_client import OpenAIClient
        client = OpenAIClient()
        response = await client.chat([
            {"role": "user", "content": question}
        ])
        click.echo(f"\n🤖 {response.content}")
        click.echo(f"\n📊 Tokens: {response.tokens_used} | Latency: {response.latency_ms:.0f}ms")
    
    asyncio.run(_ask())

if __name__ == '__main__':
    cli()
```

**📝 Week 2 Checkpoint (`Layer1-Final/week-02/checkpoint.md`):**
```markdown
## Week 2 Self-Assessment

### Can I...
- [ ] Write Python decorators with proper functools.wraps?
- [ ] Use async/await for non-blocking I/O?
- [ ] Make API calls to OpenAI and parse responses?
- [ ] Design an abstract base class with multiple implementations?
- [ ] Build a prompt template system with validation?
- [ ] Write integration tests that call external APIs?
- [ ] Explain what a transformer is at a high level?
- [ ] Explain what tokenization is and why it matters?

### What I built this week:
- LLM client abstraction (OpenAI + Ollama)
- Prompt template system
- PromptRunner with observability logging
- CLI tool
- Tests for everything

### What confused me:
- [Write honest reflections here]

### Tokens spent this week: ___
### Average API latency: ___ms
```

---

## 📅 WEEK 3: Data Processing + Embeddings

> **Flagship tie-in:** Building the document ingestion pipeline

### Day 11 — Document Loading & Text Extraction

**🧠 Learn (80 min):**
- 📖 [LangChain Document Loaders](https://python.langchain.com/docs/how_to/#document-loaders) — 30 min
- 🎥 [Building a PDF Parser — James Briggs](https://www.youtube.com/watch?v=cHjlperESbg) — 25 min
- 📖 [PyPDF2/pymupdf docs](https://pymupdf.readthedocs.io/) — 25 min

**💻 Build (120 min):**
```python
# File: src/ingestion/loaders.py
"""Document loaders for the RAG Platform."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LoadedDocument:
    content: str
    metadata: dict
    source: str
    page_count: int | None = None

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> list[LoadedDocument]:
        pass

class TextFileLoader(BaseLoader):
    def load(self, filepath: str) -> list[LoadedDocument]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        content = path.read_text(encoding='utf-8')
        return [LoadedDocument(
            content=content,
            metadata={"filename": path.name, "extension": path.suffix},
            source=filepath
        )]

class PDFLoader(BaseLoader):
    def load(self, filepath: str) -> list[LoadedDocument]:
        import fitz  # pymupdf
        doc = fitz.open(filepath)
        pages = []
        full_text = ""
        for page_num, page in enumerate(doc):
            text = page.get_text()
            full_text += text + "\n"
        
        return [LoadedDocument(
            content=full_text.strip(),
            metadata={"filename": Path(filepath).name, "pages": len(doc)},
            source=filepath,
            page_count=len(doc)
        )]

class WebPageLoader(BaseLoader):
    def load(self, url: str) -> list[LoadedDocument]:
        import httpx
        from bs4 import BeautifulSoup
        response = httpx.get(url, follow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        return [LoadedDocument(
            content=text,
            metadata={"url": url, "title": soup.title.string if soup.title else ""},
            source=url
        )]

# Factory
class LoaderFactory:
    @staticmethod
    def create(source: str) -> BaseLoader:
        if source.startswith(('http://', 'https://')):
            return WebPageLoader()
        path = Path(source)
        match path.suffix.lower():
            case '.txt' | '.md':
                return TextFileLoader()
            case '.pdf':
                return PDFLoader()
            case _:
                raise ValueError(f"Unsupported file type: {path.suffix}")
```

### Day 12 — Text Chunking Strategies

**🧠 Learn (80 min):**
- 🎥 [Greg Kamradt — Chunking for RAG (5 Levels)](https://www.youtube.com/watch?v=8OJC21T2SL4) — 40 min
- 📖 [LangChain Text Splitters](https://python.langchain.com/docs/how_to/#text-splitters) — 40 min

**💻 Build (120 min):**
```python
# File: src/ingestion/chunker.py
"""Multiple chunking strategies for different use cases."""

from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class TextChunk:
    content: str
    index: int
    metadata: dict
    start_char: int
    end_char: int

class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, text: str, metadata: dict = None) -> list[TextChunk]:
        pass

class FixedSizeChunker(BaseChunker):
    """Simple fixed-size chunking with overlap."""
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str, metadata: dict = None) -> list[TextChunk]:
        words = text.split()
        chunks = []
        start = 0
        index = 0
        
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = ' '.join(words[start:end])
            
            # Calculate character positions
            char_start = len(' '.join(words[:start])) + (1 if start > 0 else 0)
            char_end = char_start + len(chunk_text)
            
            chunks.append(TextChunk(
                content=chunk_text,
                index=index,
                metadata={**(metadata or {}), "chunk_method": "fixed_size"},
                start_char=char_start,
                end_char=char_end
            ))
            
            start = end - self.overlap
            index += 1
            
            if end >= len(words):
                break
        
        return chunks

class SentenceChunker(BaseChunker):
    """Chunk by sentences, respecting natural boundaries."""
    def __init__(self, max_sentences: int = 5, overlap_sentences: int = 1):
        self.max_sentences = max_sentences
        self.overlap = overlap_sentences
    
    def chunk(self, text: str, metadata: dict = None) -> list[TextChunk]:
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        start = 0
        index = 0
        
        while start < len(sentences):
            end = min(start + self.max_sentences, len(sentences))
            chunk_text = ' '.join(sentences[start:end])
            
            chunks.append(TextChunk(
                content=chunk_text,
                index=index,
                metadata={**(metadata or {}), "chunk_method": "sentence"},
                start_char=0,  # Simplified
                end_char=len(chunk_text)
            ))
            
            start = end - self.overlap
            index += 1
            
            if end >= len(sentences):
                break
        
        return chunks

# TODO (Exercise for Ahmed): Implement RecursiveChunker
# that splits by paragraph → sentence → word, 
# similar to LangChain's RecursiveCharacterTextSplitter
```

### Day 13 — Embeddings Deep Dive

**🧠 Learn:**
- 📖 [Jay Alammar — Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/) — 40 min
- 🎥 [What are Embeddings? — Computerphile](https://www.youtube.com/watch?v=gQddtTdmG_8) — 15 min
- 📖 [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) — 25 min

**💻 Build:** Embedding service + cosine similarity search from scratch

### Day 14 — Vector Similarity Search (No Vector DB Yet)

**💻 Build:** NumPy-based vector store with cosine similarity, brute-force search

### Day 15 — Week 3 Checkpoint: Full Ingestion Pipeline Test

**💻 Build:** End-to-end: `Load PDF → Chunk → Embed → Store → Query → Retrieve`

---

## 📅 WEEK 4: Vector Databases + RAG v1

### Day 16 — ChromaDB Setup
- 📖 [ChromaDB Docs](https://docs.trychroma.com/) 
- Build: Replace NumPy store with ChromaDB

### Day 17 — RAG Pipeline v1
- Wire: Query → Embed → ChromaDB Search → Context Assembly → LLM → Answer

### Day 18 — RAG Evaluation Metrics
- Build: Faithfulness, relevance, context precision metrics

### Day 19 — Error Handling + Fallbacks
- Build: LLM provider fallback (OpenAI → Ollama), circuit breaker pattern

### Day 20 — Week 4 Checkpoint: RAG Platform Demo
- Demo: Upload a PDF, ask questions, get cited answers

---

## WEEKS 5–10: RAG ENGINEERING (Flagship #1 Deep Build)

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| **5** | Advanced Retrieval: Hybrid Search (BM25 + Dense), Re-ranking | Improved retrieval accuracy |
| **6** | Conversational RAG: Memory, multi-turn, follow-ups | Chat interface with history |
| **7** | Multi-document RAG + Metadata Filtering | Cross-document Q&A |
| **8** | Streaming Responses + Streamlit UI | Real-time chat UI |
| **9** | RAG Evaluation Framework + A/B Testing Prompts | Automated eval pipeline |
| **10** | **Flagship #1 Completion**: Docker, deploy, documentation | Production-ready RAG platform |

**Key Resources for Weeks 5-10:**
- 📖 [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- 📖 [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- 🎥 [James Briggs — RAG Playlist](https://www.youtube.com/playlist?list=PLIUOU7oqGTLgBf0X_KzRlsqyM2Cs7Dxp)
- 📖 [RAGAS — RAG Evaluation Framework](https://docs.ragas.io/)
- 📖 [Streamlit Documentation](https://docs.streamlit.io/)
- 📖 [Docker Getting Started](https://docs.docker.com/get-started/)
- 📖 [Evidently AI — ML System Design Case Studies](https://www.evidentlyai.com/ml-system-design) (from your Gemini plan)

---

## WEEKS 11–16: AI AGENTS (Flagship #2)

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| **11** | Tool Use + Function Calling (OpenAI) | Agent makes API calls |
| **12** | LangGraph: Stateful Agent Graphs | Multi-step agent workflow |
| **13** | Multi-Agent Systems (CrewAI) | Agents collaborating on tasks |
| **14** | Agent Memory: Short-term + Long-term | Persistent agent memory |
| **15** | Agent Evaluation + Safety (Prompt Injection) | Adversarial testing suite |
| **16** | **Flagship #2 Completion**: Full agent system | Production AI agent |

**Key Resources for Weeks 11-16:**
- 📖 [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- 📖 [CrewAI Documentation](https://docs.crewai.com/)
- 📖 [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- 📖 [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- 🎥 [AI Jason — Building AI Agents](https://www.youtube.com/@AIJasonZ)
- 📖 [Prompt Injection Defense](https://simonwillison.net/2022/Sep/12/prompt-injection/)

---

## WEEKS 17–22: PRODUCTION ENGINEERING

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| **17** | Observability: Logging, Monitoring, LLM Tracing | Dashboards for both flagships |
| **18** | Authentication + Authorization (JWT, API Keys) | Secured API endpoints |
| **19** | Caching (Redis) + Rate Limiting | Cost-controlled, fast API |
| **20** | Cloud Deployment (AWS/GCP/Railway) | Live production URL |
| **21** | CI/CD Pipeline (GitHub Actions) | Automated testing + deploy |
| **22** | Load Testing + Performance Optimization | System handles 1000 req/min |

**Key Resources for Weeks 17-22:**
- 📖 [LangSmith (LLM Observability)](https://docs.smith.langchain.com/)
- 📖 [Weights & Biases](https://wandb.ai/)
- 📖 [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- 📖 [Redis Documentation](https://redis.io/docs/)
- 📖 [GitHub Actions](https://docs.github.com/en/actions)
- 📖 [Railway Deployment](https://railway.app/) (simple alternative to AWS)
- 📖 [Locust Load Testing](https://locust.io/)

### Gemini Plan Integration: Production Hardening

Per the Gemini plan's Phase 3 requirements:
```python
# Week 19-20: Implement the Gemini plan's resilience patterns

class LLMLoadBalancer:
    """Dynamic load balancing across multiple LLM providers.
    Falls back to Gemini/Ollama if OpenAI has outage."""
    
    def __init__(self):
        self.providers = [
            {"name": "openai", "client": OpenAIClient(), "priority": 1, "healthy": True},
            {"name": "ollama", "client": OllamaClient(), "priority": 2, "healthy": True},
        ]
        self.circuit_breakers = {}
    
    async def chat(self, messages, **kwargs) -> LLMResponse:
        for provider in sorted(self.providers, key=lambda p: p["priority"]):
            if not provider["healthy"]:
                continue
            try:
                return await provider["client"].chat(messages, **kwargs)
            except Exception as e:
                provider["healthy"] = False
                self._schedule_health_check(provider["name"])
                continue
        raise RuntimeError("All LLM providers are down")

# Week 22: Implement hyperscale constraints from Gemini plan
# - Multi-tier caching (in-memory → Redis → persistent)
# - Semantic cache (cache by embedding similarity, not exact match)
# - Budget tracking ($50/month limit with alerts)
```

---

## WEEKS 23–28: CAPSTONE + JOB READINESS

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| **23** | Portfolio Website + Project Documentation | Live portfolio site |
| **24** | ML System Design Interview Prep | 5 practiced mock designs |
| **25** | Capstone: Combine RAG + Agents into one system | Unified AI platform |
| **26** | Open Source Contribution | 1 merged PR to an AI project |
| **27** | Egyptian AI Ecosystem Engagement | Conference/meetup attendance |
| **28** | Final Review + Job Applications | Resume, portfolio, applications |

### Week 24 Detail: ML System Design (From Your Gemini Plan)

The Gemini plan's 6-step framework, practiced daily:

```markdown
## ML System Design Practice Template

### Problem: "Design a RAG-based customer support system for an Egyptian e-commerce company"

**Step 1: Requirements (5 min)**
- Scale: 10K queries/day, <3s latency
- Languages: Arabic + English
- Domain: Product catalog, policies, FAQs
- Metric: Resolution rate, customer satisfaction

**Step 2: Data Pipeline (5 min)**
- Sources: Product DB, policy PDFs, FAQ pages
- Processing: Arabic tokenization (AraGPT), bilingual embeddings
- Storage: PostgreSQL (metadata) + Qdrant (vectors)
- Update frequency: Daily product sync, weekly policy review

**Step 3: Architecture (10 min)**
- Embedding model: multilingual-e5-large (Arabic support)
- Retriever: Hybrid (BM25 for Arabic + dense for semantic)
- Generator: GPT-4 with Arabic system prompt
- Fallback: Transfer to human agent after 2 failed retrievals

**Step 4: Training/Evaluation (5 min)**
- Offline: Precision@5, NDCG, faithfulness score
- Online: Resolution rate, escalation rate, CSAT

**Step 5: Deployment (5 min)**
- FastAPI on AWS ECS, auto-scaling
- Shadow deployment for new models
- A/B testing for prompt variations

**Step 6: Monitoring (5 min)**
- Track: hallucination rate, retrieval relevance drift
- Alert: latency >3s, token cost spike, low relevance scores
- Retraining: Monthly embedding model refresh
```

**Study Resources for System Design:**
- 📖 [Evidently AI — 800 ML System Design Case Studies](https://www.evidentlyai.com/ml-system-design) ⭐
- 📖 [System Design Handbook — AI Questions](https://www.systemdesignhandbook.com/blog/ai-system-design-interview-questions/)
- 📖 [Exponent — ML System Design Guide](https://www.tryexponent.com/blog/machine-learning-system-design-interview-guide)
- 📖 [mallahyari/ml-practical-usecases](https://github.com/mallahyari/ml-practical-usecases) (650 case studies)

### Week 27: Egyptian AI Ecosystem (From Your Gemini Plan)

```markdown
## Action Items for Egyptian AI Ecosystem Integration

### Events to Attend/Monitor:
- [ ] Ai Everything MEA Egypt 2026 (Feb 2026, NCIEC Cairo) — aieverythingegypt.com
- [ ] Data Science Conference MENA — dscmena.com
- [ ] Cairo ICT & Techne Summit (Nov 2026) — cairoict.com

### Communities to Join:
- [ ] Egypt AI WhatsApp/Telegram groups
- [ ] AUC Venture Lab events
- [ ] ITIDA-sponsored developer programs
- [ ] Arabic NLP open-source projects (EgyBERT)

### Portfolio Projects with Egyptian Context:
- [ ] Arabic-English bilingual RAG system
- [ ] Egyptian government document Q&A (public data)
- [ ] Cairo restaurant recommendation agent
```

---

# PART C: REPO FILE MAPPING

## How Your Existing Repo Structure Maps to This Curriculum

| Repo Component | Curriculum Usage | Status |
|---|---|---|
| `Layer1-Final/` | **PRIMARY** — All weekly exercises go here | ✅ Use as-is |
| `Layer1-Final/guides/DAY-00-DIAGNOSTIC.py` | Run on Day 1 to assess starting point | ✅ Run first |
| `Layer1-Final/guides/GUIDE-FOR-AI-ASSISTANTS.md` | Rules for AI tutors (5-level Teaching Ladder) | ✅ Reference |
| `Layer1-Final/guides/MIGRATION-GUIDE.md` | Map old 54-chapter progress to new track | ✅ Check Day 1 |
| `_ARCHIVE_2026-03/` | Old curricula — reference only, don't study | ⚠️ Don't use |
| `_ARCHIVE_2026-03/Layer1-original/` | 40-day intensive (archived) | ❌ Deprecated |
| `_ARCHIVE_2026-03/Layer2/` | 54-chapter comprehensive (archived) | ❌ Deprecated |
| `_ARCHIVE_2026-03/Modified/` | 32-week track (archived) | ❌ Deprecated |
| `_PLANNING-2026-03/` | Planning docs for the consolidation | 📋 Reference |

## Files You Need to CREATE

```bash
# Flagship Project #1
mkdir -p flagship-1-rag-platform/{src/{api,database,ingestion,retrieval,generation,llm,utils},tests}
touch flagship-1-rag-platform/pyproject.toml
touch flagship-1-rag-platform/Dockerfile
touch flagship-1-rag-platform/README.md

# Flagship Project #2 (Start Week 11)
mkdir -p flagship-2-ai-agent/{src/{agents,tools,memory,evaluation},tests}

# Weekly exercise folders
for i in $(seq -w 1 28); do
    mkdir -p Layer1-Final/week-$i/{exercises,notes}
    touch Layer1-Final/week-$i/checkpoint.md
done
```

---

# PART D: KEY DIFFERENCES FROM MY ORIGINAL ANSWER

| My Original 90-Day Plan | This Revised Plan | Why Changed |
|---|---|---|
| 21 days on Python basics + math | 4 days on Python + SQL (Week 1) | Gemini plan: "value is in application layer" |
| 21 days building CNNs/RNNs from scratch | 0 days (understand architectures, don't build) | Both docs: AI Engineers orchestrate, not train |
| Separate toy projects each week | Two evolving Flagship projects | BMad repo: continuous iteration > throwaway code |
| 3-5 hrs/day assumed | 4 hrs/day (80/120/40 split) | BMad repo: structured time allocation |
| No SQL at all | SQL on Day 1 | BMad repo: "Backend-first (SQL Week 1)" |
| Testing introduced Week 9 | Testing from Week 1, Day 4 | BMad repo: "Testing-threaded from Week 2" |
| No LLM call until Day 43 | First LLM call on Day 8 | Gemini plan: get to the "AI" part fast |
| Linear progression | Spiral: learn → build → revisit → harden | Both docs: spaced repetition + iterative depth |

---

# 🚀 YOUR IMMEDIATE NEXT STEPS

```markdown
## Today (Day 0):
1. ✅ Run `Layer1-Final/guides/DAY-00-DIAGNOSTIC.py`
2. ✅ Check `_PLANNING-2026-03/MIGRATION-GUIDE.md` for credit from old 35%
3. ✅ Set up your development environment
4. ✅ Create the Flagship project directory structures

## This Week (Week 1):
- Follow Days 1-5 above exactly
- Commit daily with conventional commits
- Fill out Week 1 checkpoint on Friday

## Ongoing Daily Rhythm:
- 🧠 80 min: Watch/Read (multimodal, not pure text)
- 💻 120 min: Code on Flagship projects
- 📝 40 min: Document, commit, journal

## 30-Min Express Days (when busy):
- 10 min: One concept video
- 15 min: One function or test
- 5 min: Commit + 1-sentence note
```

**The curriculum is designed. The repo structure exists. The only thing left is execution. Let's build. 🔨**