# AITEA Project-Based AI Agents Curriculum

## Prompt for AI Assistant

You are an expert AI agent engineer, Python educator, and software architect.

Your job: take me from "zero to hero" in AI agents by building a real system end-to-end: **AITEA (AI Time Estimation Agent)**. The learning plan and project implementation are merged: every chapter teaches concepts AND delivers a working increment of AITEA.

---

## My Background

- I know basic Python syntax (functions, classes, loops, conditionals)
- I'm new to: dataclasses, type hints, abstract classes, property-based testing
- I'm new to: LLMs, agents, RAG, LangChain, LlamaIndex
- I learn best by building real things, not toy examples

---

## AITEA Project Context

AITEA helps project managers estimate software development time by:

1. Maintaining a feature library (e.g., "CRUD API = 4 hours", "WebSocket = 12 hours")
2. Importing tracked time from team members
3. Computing statistics (mean, median, P80) from historical data
4. Generating project estimates from feature lists or BRD documents

### Architecture (5 Packages)

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI/LLM Integration Layer                     │
│  ┌─────────────────────┐     ┌─────────────────────┐           │
│  │  aitea-langchain    │     │  aitea-llamaindex   │           │
│  │  • LCEL Chains      │     │  • Multi-Index      │           │
│  │  • LangGraph Agents │     │  • Hybrid Retrieval │           │
│  │  • LangSmith        │     │  • Query Engines    │           │
│  │  • RAG Pipeline     │     │  • Evaluation       │           │
│  └──────────┬──────────┘     └──────────┬──────────┘           │
│             └────────────┬───────────────┘                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                 Application Layer                                │
│  ┌─────────────┐     ┌───┴───────┐                              │
│  │  aitea-cli  │     │ aitea-web │                              │
│  │  • Typer    │     │ • FastAPI │                              │
│  │  • Rich     │     │ • NiceGUI │                              │
│  └──────┬──────┘     └─────┬─────┘                              │
│         └──────────────────┼─────────────────────────────────────┘
│                            │
│                   ┌────────▼────────┐
│                   │   aitea-core    │
│                   │  (FROM SCRATCH) │
│                   │  • Models       │
│                   │  • Services     │
│                   │  • Utilities    │
│                   └─────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

### Package Responsibilities

| Package              | Purpose                                   | AI/LLM? |
| -------------------- | ----------------------------------------- | ------- |
| **aitea-core**       | Data models, services, utilities          | ❌ No   |
| **aitea-cli**        | Command-line interface                    | ❌ No   |
| **aitea-langchain**  | LangChain/LangGraph/LangSmith integration | ✅ Yes  |
| **aitea-llamaindex** | Advanced RAG with LlamaIndex              | ✅ Yes  |
| **aitea-web**        | Web UI + API (optional, Phase 2)          | ✅ Yes  |

---

## Sample Data (Use Throughout)

### Feature Library Entry

```python
{
    "id": "feat_001",
    "name": "CRUD",
    "team": "backend",
    "process": "Data Operations",
    "seed_time_hours": 4.0,
    "synonyms": ["crud-api", "rest-crud", "data-operations"],
    "notes": "Create/Read/Update/Delete API endpoints"
}
```

### Tracked Time Entry

```python
{
    "id": "track_001",
    "team": "backend",
    "member_name": "BE-1",
    "feature": "CRUD",
    "tracked_time_hours": 4.5,
    "process": "Data Operations",
    "date": "2025-01-15"
}
```

### Sample CSV (tracked_time.csv)

```csv
team,member_name,feature,tracked_time_hours,process,date
backend,BE-1,CRUD,4.5,Data Operations,2025-01-15
backend,BE-2,CRUD,3.5,Data Operations,2025-01-16
frontend,FE-1,ui-Page,6.0,Content Management,2025-01-15
frontend,FE-1,tables,5.5,Content Management,2025-01-16
backend,BE-1,websocket,14.0,Real-time,2025-01-17
```

### Sample BRD Excerpt

```
Project: E-commerce Platform

Features Required:
- User authentication with role-based access control
- Product catalog with search and filtering
- Shopping cart and checkout flow
- Order management dashboard
- Real-time inventory updates
- Email notifications for order status
```

---

## Pinned Dependencies

```
# Core (no AI)
numpy==1.26.4
pandas==2.2.0
pydantic==2.6.0
hypothesis==6.98.0

# CLI
typer==0.9.0
rich==13.7.0

# LangChain Track
langchain==0.1.17
langchain-openai==0.1.6
langchain-community==0.0.38
langgraph==0.0.28
langsmith==0.1.40
chromadb==0.4.24

# LlamaIndex Track
llama-index==0.10.25
llama-index-llms-openai==0.1.12
llama-index-embeddings-openai==0.1.7
sentence-transformers==2.5.1
```

---

## Curriculum Structure

### Phase 1: Python Foundations (Builds aitea-core)

**No AI/LLM yet - pure Python skills**

| Ch  | Title                         | Time | Builds              | Key Concepts                                 |
| --- | ----------------------------- | ---- | ------------------- | -------------------------------------------- |
| 1   | Environment & Project Setup   | 1h   | Project structure   | venv, pip, pyproject.toml, .env files        |
| 2   | Enums & Type Hints            | 1.5h | `models/enums.py`   | Enum, type hints, mypy                       |
| 3   | Dataclasses & Data Models     | 2h   | `models/*.py`       | dataclass, field, Optional, List             |
| 4   | Abstract Classes & Interfaces | 2h   | Service interfaces  | ABC, @abstractmethod, dependency injection   |
| 5   | Service Implementation        | 3h   | `services/*.py`     | FeatureLibraryService, Result type           |
| 6   | Utility Functions             | 2h   | `utils/*.py`        | Statistics, normalization, outlier detection |
| 7   | Property-Based Testing        | 2h   | `tests/properties/` | Hypothesis, strategies, shrinking            |
| 8   | Error Handling & Validation   | 1.5h | Error types         | ValidationError, Result[T, E] pattern        |

**Deliverable:** Complete `aitea-core` package

### Phase 2: CLI Development (Builds aitea-cli)

**Still no AI - CLI patterns**

| Ch  | Title               | Time | Builds                    | Key Concepts                         |
| --- | ------------------- | ---- | ------------------------- | ------------------------------------ |
| 9   | CLI with Typer      | 2h   | `cli/main.py`             | Typer app, commands, options         |
| 10  | Rich Terminal UI    | 1.5h | Tables, progress          | Rich tables, panels, progress bars   |
| 11  | JSON Persistence    | 2h   | `services/persistence.py` | JSON serialization, file I/O         |
| 12  | CSV Import Pipeline | 2h   | Import command            | pandas, validation, error collection |

**Deliverable:** Working `aitea-cli` tool

### Phase 3: LLM Fundamentals (Introduces AI)

**Concepts before frameworks**

| Ch  | Title                 | Time | Builds           | Key Concepts                        |
| --- | --------------------- | ---- | ---------------- | ----------------------------------- |
| 13  | LLM Basics            | 2h   | Mock LLM client  | Tokens, temperature, prompting      |
| 14  | Prompt Engineering    | 2h   | Prompt templates | System/user messages, few-shot, CoT |
| 15  | Structured Outputs    | 2h   | Output parsers   | JSON mode, Pydantic parsing         |
| 16  | Tool Calling Patterns | 2.5h | Tool definitions | Function calling, schema validation |

**Deliverable:** Understanding of LLM fundamentals with mock implementations

### Phase 4: Agent Foundations (From Scratch)

**Build agents without frameworks first**

| Ch  | Title                   | Time | Builds               | Key Concepts                         |
| --- | ----------------------- | ---- | -------------------- | ------------------------------------ |
| 17  | What Are Agents?        | 1h   | Conceptual           | Agents vs chatbots vs workflows      |
| 18  | Agent Loop from Scratch | 3h   | `SimpleAgent` class  | Observe → Think → Act → Reflect      |
| 19  | Tool Registry           | 2h   | `ToolRegistry` class | Tool registration, schema validation |
| 20  | Planning Patterns       | 2.5h | ReAct implementation | ReAct, Plan-and-Execute              |
| 21  | Memory Patterns         | 2.5h | Memory classes       | Short-term, long-term, summarization |
| 22  | Guardrails & Safety     | 2h   | Safety checks        | Prompt injection, safe tool usage    |

**Deliverable:** From-scratch agent that can use aitea-core tools

### Phase 5: LangChain Track (Builds aitea-langchain)

**Agent engineering platform - map to from-scratch concepts**

| Ch  | Title                   | Time | Builds                 | Key Concepts                           |
| --- | ----------------------- | ---- | ---------------------- | -------------------------------------- |
| 23  | LangChain Agents        | 2.5h | `agents/*.py`          | High-level agent APIs, model providers |
| 24  | Custom Tools            | 2h   | `tools/*.py`           | @tool decorator, StructuredTool        |
| 25  | RAG Pipeline            | 3h   | `rag/*.py`             | Embeddings, vector store, retriever    |
| 26  | LangGraph Orchestration | 3h   | `agents/brd_parser.py` | StateGraph, memory, human-in-the-loop  |
| 27  | LangSmith Platform      | 2h   | `observability/*.py`   | Observability, evaluation, prompt eng  |
| 28  | Deep Agents             | 2h   | `deep_agents/*.py`     | Complex multi-step tasks, reflection   |

**Deliverable:** Complete `aitea-langchain` package

### Phase 6: LlamaIndex Track (Builds aitea-llamaindex)

**Agents and Workflows for knowledge-powered applications**

| Ch  | Title                  | Time | Builds             | Key Concepts                           |
| --- | ---------------------- | ---- | ------------------ | -------------------------------------- |
| 29  | LlamaIndex Agents      | 3h   | `agents/*.py`      | Knowledge assistants, RAG as tools     |
| 30  | Event-Driven Workflows | 3h   | `workflows/*.py`   | Multi-step processes, error correction |
| 31  | Advanced Retrieval     | 2.5h | `retrievers/*.py`  | Hybrid, HyDE, reranking                |
| 32  | Agentic RAG Patterns   | 2.5h | `agentic_rag/*.py` | Self-RAG, CRAG, Adaptive RAG           |
| 33  | RAG Evaluation         | 2.5h | `evaluation/*.py`  | Faithfulness, relevancy, metrics       |
| 34  | Workflow Deployment    | 2h   | Deployment config  | Production microservices               |

**Deliverable:** Complete `aitea-llamaindex` package with deployable workflows

### Phase 7: Advanced Topics (Optional)

**Production-ready patterns**

| Ch  | Title                    | Time | Builds               | Key Concepts                      |
| --- | ------------------------ | ---- | -------------------- | --------------------------------- |
| 35  | Multi-Agent Coordination | 3h   | Multi-agent example  | Supervisor, handoff patterns      |
| 36  | Reliability Patterns     | 2h   | Retry/fallback logic | Retries, timeouts, fallbacks      |
| 37  | Cost Optimization        | 2h   | Caching layer        | Caching, batching, smaller models |
| 38  | Deployment               | 3h   | FastAPI service      | API deployment, containerization  |

---

## Chapter Structure (Consistent Format)

Each chapter MUST include:

### 1. Header

```markdown
# Chapter X: [Title]

**Difficulty:** Beginner | Intermediate | Advanced
**Time:** X hours
**Prerequisites:** Chapters [list]
**AITEA Component:** [package/module being built]
```

### 2. Learning Objectives

- 3-5 specific, measurable objectives
- Use action verbs: "Implement", "Explain", "Debug", "Compare"

### 3. Key Concepts

- Intuition first (why does this exist?)
- Then formal definition
- Then implementation details

### 4. From Scratch Implementation

- Build the concept with minimal dependencies
- Show every line of code
- Explain design decisions

### 5. Framework Implementation (where applicable)

- Implement the same thing using LangChain or LlamaIndex
- Explicitly map: "This framework feature replaces our from-scratch X"
- Show what the framework abstracts away

### 6. Interactive Checkpoints

- "Your turn" exercises after each major concept
- Expected output shown
- Common errors and fixes

### 7. Debugging Scenario

- Present a broken code snippet
- Ask learner to identify the bug
- Show the fix and explain why

### 8. Quick Check Questions

- 5-10 short questions
- Mix of conceptual and code-based
- Answers provided at end

### 9. Mini-Project

- Clear requirements and acceptance criteria
- Starter scaffold provided
- Rubric for self-assessment
- Extension challenges for advanced learners

### 10. AITEA Integration

- What part of AITEA this chapter implements
- Which requirement(s) it satisfies
- How to verify it works (demo command or test)

---

## Difficulty Criteria

| Level            | Criteria                                                  |
| ---------------- | --------------------------------------------------------- |
| **Beginner**     | Single concept, <50 lines, no external deps beyond stdlib |
| **Intermediate** | 2-3 concepts combined, 50-200 lines, 1-2 external deps    |
| **Advanced**     | System design, >200 lines, multiple deps, error handling  |

---

## No-Key Fallback Requirement

Every chapter using LLMs MUST include:

```python
# config.py
import os
from enum import Enum

class LLMProvider(Enum):
    OPENAI = "openai"
    MOCK = "mock"

def get_llm_provider() -> LLMProvider:
    if os.getenv("OPENAI_API_KEY"):
        return LLMProvider.OPENAI
    return LLMProvider.MOCK

# mock_llm.py
class MockLLM:
    """Simulates LLM responses for learning without API keys."""

    RESPONSES = {
        "extract_features": {
            "features": ["CRUD", "authentication", "file-upload"],
            "confidence": 0.85
        },
        "estimate_project": {
            "total_hours": 48,
            "breakdown": [
                {"feature": "CRUD", "hours": 4},
                {"feature": "authentication", "hours": 8}
            ]
        }
    }

    def complete(self, prompt: str, task: str = "default") -> str:
        return json.dumps(self.RESPONSES.get(task, {"response": "Mock response"}))
```

Usage pattern:

```python
if get_llm_provider() == LLMProvider.MOCK:
    llm = MockLLM()
    print("⚠️  Running in MOCK mode - set OPENAI_API_KEY for real LLM")
else:
    llm = ChatOpenAI(model="gpt-4")
```

---

## Notebook Format

Default deliverable is **Jupyter notebooks** using percent format:

```python
# %% [markdown]
# # Chapter 1: Environment Setup
#
# **Difficulty:** Beginner | **Time:** 1 hour

# %%
# First, let's check our Python version
import sys
print(f"Python version: {sys.version}")

# %% [markdown]
# ## 1.1 Virtual Environment
#
# A virtual environment isolates your project dependencies...

# %%
# Exercise: Create a simple function
def greet(name: str) -> str:
    """Your turn: implement this function."""
    pass  # TODO: Return "Hello, {name}!"

# Test your implementation
assert greet("AITEA") == "Hello, AITEA!"
print("✅ Exercise passed!")
```

When .py files are needed (CLI, packages), the notebook must:

1. Explain the code
2. Import and demonstrate it
3. Include exercises

---

## Repository Structure (Evolves with Curriculum)

```
aitea/
├── README.md
├── pyproject.toml
├── .env.example                 # API keys template
├── .gitignore
│
├── notebooks/
│   ├── CH01_environment_setup.ipynb
│   ├── CH02_enums_type_hints.ipynb
│   ├── ...
│   └── CH34_framework_comparison.ipynb
│
├── src/
│   ├── aitea_core/              # Phase 1
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── aitea_cli/               # Phase 2
│   │   ├── __init__.py
│   │   ├── cli/
│   │   └── services/
│   │
│   ├── aitea_langchain/         # Phase 5
│   │   ├── __init__.py
│   │   ├── agents/
│   │   ├── chains/
│   │   ├── rag/
│   │   ├── tools/
│   │   └── observability/
│   │
│   └── aitea_llamaindex/        # Phase 6
│       ├── __init__.py
│       ├── indices/
│       ├── retrievers/
│       ├── query_engines/
│       └── evaluation/
│
├── tests/
│   ├── conftest.py
│   ├── test_core/
│   ├── test_cli/
│   ├── properties/              # Hypothesis tests
│   └── integration/
│
├── data/
│   ├── sample_features.json
│   ├── sample_tracked_time.csv
│   └── sample_brd.txt
│
└── docs/
    ├── LEARNING_PATH.md
    └── FRAMEWORK_COMPARISON.md
```

---

## Deliverable Sequencing

When I ask you to generate content, follow this order:

### Request 1: Roadmap

"Generate the complete roadmap table of contents with chapter summaries"

### Request 2-N: Individual Chapters

"Generate Chapter X notebook (complete)"

### Per-Chapter Output Format

```
## Chapter X: [Title]

### Files Created
- notebooks/CHxx_slug.ipynb
- src/aitea_xxx/module.py (if applicable)

### Notebook Content
[Full notebook in percent format]

### Module Content (if applicable)
[Full .py file content]

### Verification
Commands to run:
- `python -m pytest tests/test_xxx.py`
- `python -m aitea_cli feature list`

Expected output:
[Show expected output]

### What's Next
- Key concepts to review
- Questions to answer before proceeding
- Preview of next chapter
```

---

## Quality Checklist

Before delivering any chapter, verify:

- [ ] All code runs without errors
- [ ] Mock mode works without API keys
- [ ] Type hints on all functions
- [ ] Docstrings on all classes/functions
- [ ] At least 2 exercises per major concept
- [ ] Debugging scenario included
- [ ] AITEA integration clearly explained
- [ ] Prerequisites explicitly listed
- [ ] Time estimate is realistic

---

## Begin

Start by generating the complete roadmap table of contents, showing:

1. All chapters with titles
2. Time estimates
3. What AITEA component each builds
4. Dependencies between chapters

Then wait for me to request individual chapters.
