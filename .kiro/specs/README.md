# AITEA Specification Structure

## Overview

AITEA (AI Time Estimation Agent) is organized as a comprehensive learning project covering:

- **From-scratch fundamentals** (aitea-core, aitea-cli)
- **LangChain ecosystem** (aitea-langchain)
- **LlamaIndex advanced RAG** (aitea-llamaindex)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AITEA Learning Ecosystem                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    AI/LLM Integration Layer                          │   │
│  │                                                                      │   │
│  │  ┌──────────────────────┐     ┌──────────────────────┐              │   │
│  │  │   aitea-langchain    │     │   aitea-llamaindex   │              │   │
│  │  │                      │     │                      │              │   │
│  │  │  • LangChain (LCEL)  │     │  • Multi-Index Types │              │   │
│  │  │  • LangGraph Agents  │     │  • Hybrid Retrieval  │              │   │
│  │  │  • LangSmith Tracing │     │  • Query Engines     │              │   │
│  │  │  • RAG Pipeline      │     │  • ReAct Agents      │              │   │
│  │  │  • Custom Tools      │     │  • Evaluation        │              │   │
│  │  └──────────┬───────────┘     └──────────┬───────────┘              │   │
│  │             │                            │                          │   │
│  │             └────────────┬───────────────┘                          │   │
│  │                          │                                          │   │
│  └──────────────────────────┼──────────────────────────────────────────┘   │
│                             │                                               │
│  ┌──────────────────────────┼──────────────────────────────────────────┐   │
│  │                    Application Layer                                 │   │
│  │                          │                                          │   │
│  │  ┌─────────────┐     ┌───┴───────┐     ┌─────────────┐              │   │
│  │  │  aitea-cli  │     │ aitea-web │     │   Future    │              │   │
│  │  │             │     │ (Phase 2) │     │   Apps...   │              │   │
│  │  │  • Typer    │     │           │     │             │              │   │
│  │  │  • Rich     │     │  • FastAPI│     │             │              │   │
│  │  │  • JSON     │     │  • NiceGUI│     │             │              │   │
│  │  └──────┬──────┘     └─────┬─────┘     └──────┬──────┘              │   │
│  │         │                  │                  │                     │   │
│  │         └──────────────────┼──────────────────┘                     │   │
│  │                            │                                        │   │
│  └────────────────────────────┼────────────────────────────────────────┘   │
│                               │                                             │
│                      ┌────────▼────────┐                                    │
│                      │   aitea-core    │                                    │
│                      │  (FROM SCRATCH) │                                    │
│                      │                 │                                    │
│                      │  • Models       │                                    │
│                      │  • Services     │                                    │
│                      │  • Utilities    │                                    │
│                      └─────────────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Learning Path

### Phase 1: From-Scratch Fundamentals

| Package        | What You'll Learn                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------- |
| **aitea-core** | Dataclasses, enums, type hints, abstract base classes, service patterns, property-based testing |
| **aitea-cli**  | CLI development with Typer, Rich terminal UI, JSON persistence                                  |

### Phase 2: LangChain Ecosystem

| Component       | What You'll Learn                                         |
| --------------- | --------------------------------------------------------- |
| **LCEL Chains** | Composable chain syntax, prompt templates, output parsers |
| **LangGraph**   | Stateful agent workflows, conditional edges, tool calling |
| **RAG**         | Vector stores, embeddings, retrieval patterns             |
| **LangSmith**   | Tracing, debugging, evaluation, prompt versioning         |

### Phase 3: LlamaIndex Advanced RAG

| Component         | What You'll Learn                                    |
| ----------------- | ---------------------------------------------------- |
| **Index Types**   | VectorStore, Tree, Keyword, KnowledgeGraph           |
| **Retrieval**     | Hybrid search, HyDE, reranking, query transformation |
| **Query Engines** | Router, sub-question, citation engines               |
| **Evaluation**    | Faithfulness, relevancy, retrieval metrics           |

---

## Packages

### 1. aitea-core (Foundation - FROM SCRATCH)

Shared library containing data models, core services, and utilities.

| Component     | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| **Models**    | Feature, TrackedTimeEntry, ProjectEstimate, EstimationConfig  |
| **Services**  | FeatureLibraryService, TimeTrackingService, EstimationService |
| **Utilities** | Statistics, normalization, outlier detection, confidence      |

**Dependencies:** numpy, pandas, pydantic

**Spec:** [aitea-core/](./aitea-core/)

---

### 2. aitea-cli (CLI Tool - FROM SCRATCH)

Command-line interface for project estimation.

| Feature                | Description                                |
| ---------------------- | ------------------------------------------ |
| **Feature Management** | Add, list, search, update, delete features |
| **Time Tracking**      | Import CSV, view statistics                |
| **Estimation**         | BRD parsing, feature estimation, export    |
| **Data Quality**       | Duplicate detection, anomaly alerts        |
| **Reporting**          | Distribution charts, comparisons           |

**Dependencies:** aitea-core, typer, rich

**Spec:** [aitea-cli/](./aitea-cli/)

---

### 3. aitea-langchain (LangChain + LangGraph + LangSmith)

AI-powered estimation using the LangChain ecosystem.

| Feature              | Description                           |
| -------------------- | ------------------------------------- |
| **BRD Parser Agent** | LangGraph agent for document parsing  |
| **LCEL Chains**      | Feature extraction, estimation chains |
| **RAG Pipeline**     | Vector store, semantic search         |
| **Custom Tools**     | Wrap aitea-core services as LLM tools |
| **Observability**    | LangSmith tracing and evaluation      |

**Dependencies:** aitea-core, langchain, langgraph, langsmith, chromadb

**Spec:** [aitea-langchain/](./aitea-langchain/)

---

### 4. aitea-llamaindex (Advanced RAG)

Advanced RAG capabilities using LlamaIndex.

| Feature              | Description                                   |
| -------------------- | --------------------------------------------- |
| **Multi-Index**      | Vector, Tree, Keyword, KnowledgeGraph indices |
| **Hybrid Retrieval** | Combined retrieval with reranking             |
| **Query Engines**    | Router, sub-question, citation engines        |
| **ReAct Agent**      | Interactive estimation agent                  |
| **Evaluation**       | Comprehensive RAG evaluation framework        |

**Dependencies:** aitea-core, llama-index, sentence-transformers

**Spec:** [aitea-llamaindex/](./aitea-llamaindex/)

---

### 5. aitea-web (Phase 2 - Web Application)

Web application with external integrations.

| Feature          | Description               |
| ---------------- | ------------------------- |
| **Web UI**       | NiceGUI-based dashboard   |
| **REST API**     | FastAPI backend           |
| **Integrations** | GitHub, Clockify, ClickUp |

**Dependencies:** aitea-core, fastapi, nicegui

**Spec:** [aitea-web/](./aitea-web/)

---

## Implementation Order

```
1. aitea-core          ──► Foundation (FROM SCRATCH)
       │
       ▼
2. aitea-cli           ──► CLI Tool (FROM SCRATCH)
       │
       ├───────────────────┐
       ▼                   ▼
3. aitea-langchain    4. aitea-llamaindex
   (LangChain)           (LlamaIndex)
       │                   │
       └─────────┬─────────┘
                 ▼
         5. Comparison & Benchmarks
                 │
                 ▼
         6. aitea-web (Optional)
```

## Key Design Decisions

| Decision                   | Rationale                                         |
| -------------------------- | ------------------------------------------------- |
| **From-scratch core**      | Learn Python fundamentals without framework magic |
| **Separate AI packages**   | Compare LangChain vs LlamaIndex approaches        |
| **Property-based testing** | Learn Hypothesis for robust testing               |
| **Both frameworks**        | Understand strengths/weaknesses of each           |
| **Evaluation framework**   | Measure and compare RAG quality                   |

## Comparison Focus Areas

| Aspect             | LangChain                     | LlamaIndex             |
| ------------------ | ----------------------------- | ---------------------- |
| **Strength**       | Agent workflows, tool calling | Index types, retrieval |
| **RAG**            | General-purpose               | Specialized, optimized |
| **Agents**         | LangGraph (flexible)          | ReAct (structured)     |
| **Observability**  | LangSmith (excellent)         | Basic tracing          |
| **Learning Curve** | Moderate                      | Steeper                |
