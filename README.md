# Hands-On AI Engineering: Zero to Production Systems

A 28-week, hands-on curriculum that teaches you to build production-ready AI systems
through real-world Civil Engineering applications.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Start Here

**The active curriculum lives in [`Layer1-Final/`](Layer1-Final/).**

Open [`QUICKSTART.md`](QUICKSTART.md) for step-by-step setup, or go directly to
`Layer1-Final/` and read the week-by-week guides.

---

## Project Structure

```
hands-on-ai-engineering/
├── Layer1-Final/          ← ACTIVE curriculum (28 weeks, student-facing)
│   ├── docs/              ← Analysis notes, suggestions
│   └── guides/            ← Diagnostic, rubrics, progress tracker, AI guide
├── src/                   ← Production FastAPI app and LLM layer
├── tests/                 ← Test suite
├── docs/                  ← Root-level reference docs
├── shared/                ← Shared utilities (models, infrastructure, ingest)
├── _bmad/                 ← Active BMAD framework config
├── _archive/              ← Superseded material (layers, planning, old docs)
├── examples/              ← Working code examples
├── books/                 ← Reference books / reading materials
└── conductor/             ← Conductor tooling
```

Key files at the root:

| File | Purpose |
|------|---------|
| `QUICKSTART.md` | Detailed setup and first-run guide |
| `STUDENT-GUIDE.md` | Learning tips and workflow |
| `CONTRIBUTING.md` | How to contribute |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

---

## Quick Start (5 minutes)

```bash
# 1. Clone
git clone https://github.com/AhmedTElKodsh/hands-on-ai-engineering.git
cd hands-on-ai-engineering

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys (OpenAI, Anthropic, etc.)

# 5. Open the curriculum
# Start at: Layer1-Final/
```

---

## What You'll Build

By the end of Layer 1 you will have built a **complete AI-powered Civil Engineering
Document System** covering:

- Multi-provider LLM clients (OpenAI, Anthropic, Groq, Ollama)
- Embeddings, vector stores, and hybrid search (dense + BM25)
- RAG pipelines with semantic chunking and query rewriting
- Agent patterns: ReAct, OTAR, LangGraph state graphs
- Multi-agent teams with CrewAI and AutoGen
- Production hardening: property-based testing, cost tracking, security

---

## Archived Material

Older curriculum layers, planning documents, and stale root-level docs have been moved
to [`_archive/`](_archive/). See [`_archive/README.md`](_archive/README.md) for a full
inventory and rationale.

---

## License

MIT — see [LICENSE](LICENSE) for details.
