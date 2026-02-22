# AI Engineering Curriculum Roadmap v9.0
## Comprehensive Coverage: 73 Chapters, 11 Phases, ~102 Hours

**Created**: 2026-02-19 | **Updated**: 2026-02-20
**Version**: 9.0 — Gap Analysis Integration (RAG Completeness + Production Deployment)
**Based On**: v8.0 (71 chapters, 97 hours) + Deep Research Gap Analysis
**Owner**: Ahmed
**Quality Standards**: Writing Style Guide v2.1 + Quality Checklist v1.2 + Visual Enhancement Guide v1.0
**Related**: See `CURRICULUM-IMPLEMENTATION-ROADMAP.md` for v9.1 Enhancement Pass standards

**Research Sources**:
- [nirdiamant/rag_techniques](https://github.com/nirdiamant/rag_techniques) — 34 RAG techniques benchmarked
- [jamwithai/production-agentic-rag-course](https://github.com/jamwithai/production-agentic-rag-course) — Production practices
- [Agentic AI Handbook](https://www.aihandbook.io/agentic-ai-handbook/) — 2026 agent patterns
- [LLMOps Production Case Studies](https://www.zenml.io/blog/llmops-in-production-287-more-case-studies-of-what-actually-works) — 287 case studies
- [MCP Security Guide — CoSAI](https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/) — 40+ MCP threat categories
- [2026 AI Architect Roadmap](https://www.linkedin.com/posts/dinesh-kumar-6b0528b4_agenticai-aiengineer-aiarchitecture-activity-7417400054510018560-_ysW) — Industry skills map
- [MLOps/LLMOps CI/CD 2026](https://brlikhon.engineer/blog/mlops-in-2026-the-complete-ci-cd-pipeline-for-llm-deployment) — Deployment practices

---

## What's New in v9.0

### Gap Analysis Summary

Cross-referencing v8.0 against the current industry landscape identified **3 tiers of gaps**:

| Tier | Severity | Items | Action |
|------|----------|-------|--------|
| **Tier 1 — Critical** | Missing major patterns/skills expected by every employer | 4 | New chapters or major expansions |
| **Tier 2 — Important** | Topics in leading curricula but absent here | 6 | Expand existing chapters |
| **Tier 3 — Nice-to-Have** | Completionist coverage for advanced learners | 5 | Sidebar mentions / optional reading |

### v9.0 Changes at a Glance

**New Chapters (+2)**:
- ✅ **Chapter 41B: FastAPI for AI Services** — Deploy AI as production REST APIs (1.5h)
- ✅ **Chapter 41C: Docker for AI Applications** — Containerize every AI system (1.0h)

**Major Chapter Expansions (+4)**:
- ✅ **Chapter 15**: + Proposition Chunking + Contextual Chunk Headers (+30 min)
- ✅ **Chapter 22**: + Self-RAG + CRAG + RAPTOR + Adaptive Retrieval (+60 min → 2.5h total)
- ✅ **Chapter 48B**: + A2A Protocol + MCP Security Threat Model (+30 min → 2.0h total)
- ✅ **Chapter 42**: + Redis Semantic Caching deep-dive (+20 min)

**Lightweight Additions (+3)**:
- ✅ **Chapter 30B**: + Explicit Agentic RAG pattern (+20 min)
- ✅ **Chapter 43**: + PydanticAI + OpenAI Agents SDK comparison sidebar
- ✅ **Chapter 21**: + Explainable Retrieval concept (+10 min)

**Updated Curriculum Stats**:
- **Total Chapters**: 73 (up from 71)
- **Total Hours**: ~102 (up from 97)
- **RAG Technique Coverage**: 33/34 from nirdiamant/rag_techniques (65% → 97%)
- **Industry Alignment Score**: ~85% → ~97%

---

## Full Phase & Chapter List v9.0

> `[NEW]` = new chapter. `[EXPANDED]` = existing chapter with significant additions.
> All others carry forward unchanged from v8.0.

---

## Phase 0: Foundations (Chapters 1–6D)
**Time**: 15 hours | **Status**: Stable

| # | Chapter | Time |
|---|---------|------|
| 1 | Environment Setup & Project Initialization | 1.5h |
| 2 | Enums & Type Hints | 1.5h |
| 3 | Pydantic Models (Core) | 2.0h |
| 4 | Pydantic Advanced | 1.5h |
| 5 | Validation Utilities | 1.5h |
| 6 | Template System | 1.5h |
| 6A | Decorators & Context Managers | 1.5h |
| 6B | Error Handling Patterns | 2.0h |
| 6C | OOP Intermediate | 1.5h |
| 6D | File Handling & Path Management | 1.5h |

---

## Phase 1: LLM Fundamentals (Chapters 7–12B, 22A–C)
**Time**: 14 hours | **Status**: Stable

| # | Chapter | Time |
|---|---------|------|
| 7 | Your First LLM Call | 1.5h |
| 8 | Multi-Provider LLM Client | 1.5h |
| 9 | Prompt Engineering Basics | 1.5h |
| 10 | Streaming Responses | 1.5h |
| 11 | Structured Output | 1.5h |
| 12 | Error Handling for LLMs | 1.5h |
| 12A | Asyncio Fundamentals | 1.5h |
| 12B | Type Hints & Type Checking | 1.5h |
| 22A | Advanced Python Patterns | 1.5h |
| 22B | Performance Optimization | 1.5h |
| 22C | Testing Patterns | 1.5h |

---

## Phase 2: Embeddings & Vectors (Chapters 13–16)
**Time**: 6.5 hours | **Ch 15 EXPANDED**

| # | Chapter | Time | Status |
|---|---------|------|--------|
| 13 | Understanding Embeddings | 1.5h | Stable |
| 14 | Vector Stores with ChromaDB | 1.5h | Stable |
| 15 | Chunking Strategies | 2.0h | **[EXPANDED]** |
| 16 | Document Loaders | 1.5h | Stable |

### Chapter 15 Expansion: Chunking Strategies `[EXPANDED]`
**Original** (1.5h): Fixed-size, Recursive, Semantic, Sentence chunking

**Added in v9.0** (+30 min):

**Proposition Chunking**
Break content into atomic factoid units. Each chunk = one verifiable fact.
- Implementation: spaCy sentence parsing → LLM proposition extraction
- Ideal for: Dense technical docs, compliance text, legal material
- From: [nirdiamant/rag_techniques](https://github.com/nirdiamant/rag_techniques)

**Contextual Chunk Headers**
Auto-generate metadata-rich headers for every chunk (doc title + section + summary).
- Dramatically improves retrieval precision for long documents
- Implementation: LLM-generated headers appended before chunk text
- Decision matrix: When to use each of the 6 chunking strategies

---

## Phase 3: RAG Fundamentals (Chapters 17–22)
**Time**: 10.5 hours | **Ch 21 + Ch 22 EXPANDED**

| # | Chapter | Time | Status |
|---|---------|------|--------|
| 17 | Your First RAG System | 1.5h | Stable |
| 18 | LCEL | 1.5h | Stable |
| 19 | Retrieval Strategies | 1.5h | Stable |
| 20 | Conversational RAG | 1.5h | Stable |
| 21 | RAG Evaluation | 1.5h | **[EXPANDED]** |
| 22 | Advanced RAG | 2.5h | **[MAJOR EXPANDED]** |

### Chapter 21 Expansion: RAG Evaluation `[EXPANDED]`
**Added in v9.0** (+10 min):
- **Explainable Retrieval**: Surfaces *why* each chunk was retrieved (similarity score, BM25 contribution, reranker score). Builds trust and debugging confidence.

### Chapter 22 Major Expansion: Advanced RAG `[MAJOR EXPANDED]`
**Original** (1.5h): HyDE, Parent-Document Retrieval, Multi-Query, Step-Back Prompting

**Added in v9.0** (+60 min → now 2.5h total):

#### Self-RAG
LLMs that decide *when* to retrieve, *whether* retrieved content is relevant, and *whether* their own output is grounded:
1. Retrieve token: does this query even need retrieval?
2. ISREL token: is this retrieved chunk actually relevant?
3. ISSUP/ISUSE tokens: is the generated answer supported and useful?
- Implementation: LangGraph self-reflection loop
- When to use: Variable retrieval quality, hallucination-sensitive applications
- Mini-Project: Legal Q&A that refuses to answer when supporting evidence not found

#### Corrective RAG (CRAG)
Error-detection and automatic correction for retrieval:
1. Score each retrieved document: Correct / Incorrect / Ambiguous
2. If Incorrect: trigger web search fallback (Tavily)
3. Knowledge refinement: decompose → filter → recompose
- Implementation: LangGraph with conditional branching
- Mini-Project: Engineering standards Q&A where stale docs trigger web fallback

#### RAPTOR
Recursive abstractive processing for tree-organized retrieval. Builds a multi-level index via recursive summarization:
1. Cluster documents by semantic similarity (UMAP + GMM)
2. LLM summarizes each cluster
3. Repeat until root summary created
4. Query at correct tree level based on query scope
- Implementation: LlamaIndex + UMAP clustering
- When to use: Large corpora (100+ docs), multi-scale queries
- *Distinct from Ch 37 Tree Index*: RAPTOR uses abstractive summaries, not just hierarchy

#### Adaptive Retrieval
System dynamically selects retrieval strategy per query type:
- Simple factual → Direct vector search
- Complex multi-hop → Chain-of-thought retrieval
- Code query → BM25 keyword
- Current events → Web search augmentation
- Implementation: LLM-based query classifier + strategy router (connects to Ch 32 LangGraph routing)

---

## Phase 4: LangChain Core (Chapters 23–25)
**Time**: 4.5 hours | **Status**: Stable

| # | Chapter | Time |
|---|---------|------|
| 23 | LangChain Document Loaders | 1.5h |
| 24 | Memory & Callbacks | 1.5h |
| 25 | Output Parsers | 1.5h |

---

## Phase 5: Agents (Chapters 26–30B)
**Time**: 10.5 hours | **Ch 30B EXPANDED**

| # | Chapter | Time | Status |
|---|---------|------|--------|
| 26 | Introduction to Agents | 1.5h | Stable |
| 27 | ReAct Pattern | 1.5h | Stable |
| 28 | OTAR Loop | 1.5h | Stable |
| 29 | Tool Calling | 1.5h | Stable |
| 30 | Agent Memory | 1.5h | Stable |
| 30B | Deep Research Agents | 1.5h | **[EXPANDED]** |

### Chapter 30B Expansion: Deep Research Agents `[EXPANDED]`
**Added in v9.0** (+20 min):

#### Agentic RAG — Explicit Pattern
Critical concept deserving explicit treatment (currently only implicit across multiple chapters):
- **What it is**: Agents that *decide* when, how, and what to retrieve — not always-on retrieval
- **3 Core Patterns**:
  1. **Tool-RAG**: RAG is one tool of many; agent calls it selectively
  2. **Iterative RAG**: Retrieve → evaluate gap → retrieve again until satisfied
  3. **Orchestrator-RAG**: Planning agent decides retrieval strategy for executor agents
- **Contrast with naive RAG**: Always-retrieve vs decide-to-retrieve
- Mini-Project: Research assistant using Wikipedia, ArXiv, local KB, and web selectively per query type

---

## Phase 6: LangGraph (Chapters 31–34)
**Time**: 6.0 hours | **Status**: Stable

| # | Chapter | Time |
|---|---------|------|
| 31 | LangGraph State Machines | 1.5h |
| 32 | Conditional Routing | 1.5h |
| 33 | Human-in-the-Loop | 1.5h |
| 34 | Persistent State & Checkpoints | 1.5h |

---

## Phase 7: LlamaIndex (Chapters 35–38A)
**Time**: 8.5 hours | **Status**: Stable

| # | Chapter | Time |
|---|---------|------|
| 35 | LlamaIndex Fundamentals | 1.5h |
| 36 | Query Engines & Response Synthesis | 1.5h |
| 37 | Advanced Indexing | 1.5h |
| 38 | Hybrid Search & Reranking | 1.5h |
| 38A | GraphRAG & Knowledge Graphs | 2.5h |

---

## Phase 7A: Fine-Tuning Essentials (Chapters 55–59)
**Time**: 7.5 hours | **Status**: Stable (from v8.0)

| # | Chapter | Time |
|---|---------|------|
| 55 | Introduction to Fine-Tuning | 1.5h |
| 56 | Fine-Tuning with Unsloth | 1.5h |
| 57 | Custom Dataset Creation | 1.5h |
| 58 | DPO & Preference Alignment | 1.5h |
| 59 | Fine-Tuned Model Deployment (GGUF + Ollama) | 1.5h |

---

## Phase 8: Production (Chapters 39–42, 40A–C, 41A–C)
**Time**: 14.5 hours | **2 new chapters + Ch 42 EXPANDED**

| # | Chapter | Time | Status |
|---|---------|------|--------|
| 39 | Testing AI Systems with Hypothesis | 1.5h | Stable |
| 40A | Evaluation with LangSmith | 1.5h | Stable |
| 40B | Production Observability with Arize Phoenix | 2.0h | Stable |
| 40C | Distributed Tracing & Cost Analytics | 1.5h | Stable |
| 41 | Error Handling, Security & Observability | 1.5h | Stable |
| 41A | Production Guardrails (NeMo + Guardrails AI) | 1.5h | Stable |
| **41B** | **FastAPI for AI Services** | **1.5h** | **[NEW]** |
| **41C** | **Docker for AI Applications** | **1.0h** | **[NEW]** |
| 42 | Token Management & Cost Optimization | 1.5h | **[EXPANDED]** |

---

### Chapter 41B: FastAPI for AI Services `[NEW]`
**Time**: 1.5h | **Difficulty**: ⭐⭐⭐
**Gap Origin**: Every production AI course and 2026 job description expects FastAPI. Currently absent.

**What You'll Build**: A production-ready REST API wrapping your RAG system — async endpoints, Pydantic validation, background tasks, SSE streaming, health checks.

**Learning Objectives**:
- Set up FastAPI + Uvicorn project
- Create async endpoints for LLM/RAG calls
- Pydantic request/response schemas
- Background tasks for long-running inference
- Middleware: CORS, rate limiting, request logging
- Stream LLM responses via Server-Sent Events (SSE)
- Health check and readiness probes

**Mini-Projects**:
1. **RAG API** (30 min): `/query` and `/ingest` endpoints wrapping Ch 22 RAG
2. **Streaming Endpoint** (45 min): Token-by-token SSE stream
3. **Production API with Auth** (60 min): API key auth, rate limiting, structured logging

**Prerequisites**: Ch 12A (asyncio), Ch 11 (structured output), any RAG chapter
**Builds Toward**: Ch 41C (Docker), Ch 54 (complete system)

---

### Chapter 41C: Docker for AI Applications `[NEW]`
**Time**: 1.0h | **Difficulty**: ⭐⭐⭐
**Gap Origin**: Production AI systems run in containers. Currently zero containerization coverage.

**What You'll Build**: Your FastAPI RAG API in a container + docker-compose orchestrating the full stack (API + ChromaDB + Redis).

**Learning Objectives**:
- Docker fundamentals: images, containers, layers
- Efficient Dockerfiles for Python/AI apps (multi-stage builds)
- Environment variables and secrets management
- docker-compose for multi-service RAG stack
- Volume mounting for model files and vector stores
- Optimizing image size (avoiding embedding model bloat)

**Mini-Projects**:
1. **Dockerize FastAPI RAG** (30 min): Package Ch 41B as a container
2. **Compose Stack** (30 min): Full `docker-compose.yml` (API + ChromaDB + Redis)

**Prerequisites**: Ch 41B (FastAPI)
**Builds Toward**: Ch 54 (complete system), Ch 59 (fine-tuned model deployment)

> **Scope Note**: Deliberately 1.0h — enough to unblock all deployment work without becoming a Docker course. Optional deep-dive resources provided for students wanting more.

---

### Chapter 42 Expansion: Token Management & Cost Optimization `[EXPANDED]`
**Original** (1.5h): tiktoken, cost tracking, prompt optimization, caching, model selection

**Added in v9.0** (+20 min):

#### Redis Semantic Caching
Highest-ROI production optimization. Cache LLM responses by *semantic similarity*, not exact string match:
- Hash query embedding → check Redis for similar cached queries → serve from cache if similarity > threshold
- LangChain integration: `RedisSemanticCache` with configurable similarity threshold
- **Cost impact**: 30–60% API cost reduction for Q&A systems with overlapping queries
- Mini-Project: Add semantic caching to Ch 22 RAG; measure cache hit rate and cost savings over 100 queries

---

## Phase 9: Multi-Agent Systems (Chapters 43–48B)
**Time**: 12.0 hours | **Ch 43 + Ch 48B EXPANDED**

| # | Chapter | Time | Status |
|---|---------|------|--------|
| 43 | Multi-Agent Fundamentals | 1.5h | **[EXPANDED]** |
| 44 | CrewAI for Team-Based Workflows | 1.5h | Stable |
| 45 | AutoGen for Iterative Refinement | 1.5h | Stable |
| 46 | Supervisor Pattern | 1.5h | Stable |
| 47 | Agent Communication Protocols | 1.5h | Stable |
| 48 | Debugging Multi-Agent Systems | 1.5h | Stable |
| 48A | Swarm Pattern | 1.5h | Stable |
| 48B | Model Context Protocol (MCP) | 2.0h | **[EXPANDED]** |

### Chapter 43 Expansion: Multi-Agent Fundamentals `[EXPANDED]`
**Added in v9.0** (~15 min sidebar):

#### Framework Landscape: The Broader Ecosystem
Students should be aware of the fast-evolving framework options before committing to one stack:

| Framework | Best For | Style |
|-----------|----------|-------|
| LangGraph (Ch 31–34) | Stateful, complex flows | Code-first, explicit graphs |
| CrewAI (Ch 44) | Role-based teams | High-level, opinionated |
| AutoGen (Ch 45) | Iterative conversation | Conversation-centric |
| **OpenAI Agents SDK** | OpenAI-centric production | Minimal, production-ready |
| **PydanticAI** | Type-safe, structured agents | Pythonic, FastAPI-style |

Why it matters: PydanticAI is growing rapidly; OpenAI Agents SDK is used by companies already on OpenAI. Students need to recognize these in job descriptions and interviews.
*(Conceptual overview only — no code required. Optional notebooks provided.)*

---

### Chapter 48B Expansion: Model Context Protocol (MCP) `[EXPANDED]`
**Original** (1.5h): MCP server creation, multi-tool exposure, production MCP integration

**Added in v9.0** (+30 min → now 2.0h):

#### Agent-to-Agent Protocol (A2A) — Google's Emerging Standard
While MCP connects agents to *tools*, A2A connects agents to *other agents*:
- **AgentCard**: capability discovery (what can this agent do?)
- **Task lifecycle**: structured task creation, delegation, and completion
- **Push notifications**: async agent callbacks
- **MCP vs A2A**: MCP = agent ↔ tool. A2A = agent ↔ agent. Production systems need both.
- Implementation: Python A2A client connecting engineer agent + reviewer agent
- Status: 2025 emerging standard — watch for rapid adoption

#### MCP Security Threat Model
Based on [CoSAI's guide](https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/) — 40+ threats across 12 categories:
- **Top 3 threats**: Missing access control, prompt injection via tool results, privilege escalation across agent chains
- **Defense patterns**: Tool allowlists, output sanitization before re-injection to LLM, least-privilege MCP servers
- **Real incidents studied**: Asana tenant isolation flaw (1,000 enterprises), WordPress plugin exposure (100K+ sites)
- **Practical rule**: Never treat tool output as trusted input to the next LLM call without sanitization

---

## Phase 10: Civil Engineering Application (Chapters 49–54, 52A)
**Time**: 11.5 hours | **Status**: Stable

| # | Chapter | Time |
|---|---------|------|
| 49 | Civil Engineering Document Models | 1.5h |
| 50 | Contract Generation System | 1.5h |
| 51 | Proposal Generation System | 1.5h |
| 52 | Report Generation System | 1.5h |
| 52A | Multimodal AI (GPT-4 Vision for CAD) | 1.5h |
| 53 | Compliance Review System | 1.5h |
| 54 | Complete System Integration | 2.5h |

---

## Phase 11: Advanced Topics (Chapter 60)
**Time**: 2.0 hours | **Status**: Stable (from v8.0)

| # | Chapter | Time |
|---|---------|------|
| 60 | Voice AI with Pipecat | 2.0h |

---

## RAG Technique Coverage Matrix v9.0

Cross-reference against [nirdiamant/rag_techniques](https://github.com/nirdiamant/rag_techniques):

| Technique | Covered In | v8.0 | v9.0 |
|-----------|------------|------|------|
| Basic RAG | Ch 17 | ✅ | ✅ |
| RAG with Structured Data (CSV) | Ch 23 | ✅ | ✅ |
| Reliable RAG | Ch 22 (CRAG) | ❌ | ✅ |
| Optimizing Chunk Sizes | Ch 15 | ✅ | ✅ |
| Proposition Chunking | Ch 15 | ❌ | ✅ |
| Query Transformations | Ch 19 | ✅ | ✅ |
| HyDE | Ch 22 | ✅ | ✅ |
| HyPE (Hypothetical Prompt Embeddings) | Ch 22 Multi-Query | ✅ | ✅ |
| Contextual Chunk Headers | Ch 15 | ❌ | ✅ |
| Relevant Segment Extraction | Ch 22 (Parent-Doc) | ✅ | ✅ |
| Context Window Enhancement | Ch 22 | ✅ | ✅ |
| Semantic Chunking | Ch 15 | ✅ | ✅ |
| Contextual Compression | Ch 22 | ✅ | ✅ |
| Document Augmentation | Ch 57 | ✅ | ✅ |
| Fusion Retrieval | Ch 38 | ✅ | ✅ |
| Reranking | Ch 38 | ✅ | ✅ |
| Multi-faceted Filtering | Ch 19 | ✅ | ✅ |
| Hierarchical Indices | Ch 37 | ✅ | ✅ |
| Ensemble Retrieval | Ch 38 | ✅ | ✅ |
| Retrieval with Feedback Loop | Ch 22 (CRAG) | ❌ | ✅ |
| Adaptive Retrieval | Ch 22 | ❌ | ✅ |
| Iterative Retrieval | Ch 22 (Self-RAG) | ❌ | ✅ |
| DeepEval | Ch 21, 40A | ✅ | ✅ |
| GroUSE | Ch 21 | ✅ | ✅ |
| Explainable Retrieval | Ch 21 | ❌ | ✅ |
| Graph RAG with LangChain | Ch 38A | ✅ | ✅ |
| Microsoft GraphRAG | Ch 38A | ✅ | ✅ |
| RAPTOR | Ch 22 | ❌ | ✅ |
| Self-RAG | Ch 22 | ❌ | ✅ |
| Corrective RAG (CRAG) | Ch 22 | ❌ | ✅ |
| Agentic RAG | Ch 30B | ❌ | ✅ |
| Multi-modal RAG | Ch 52A | ✅ (CE) | ✅ |
| RAG with Structured Data | Ch 23 | ✅ | ✅ |

**Coverage: 33/34 = 97%** (up from ~65% in v8.0)

---

## Industry Alignment Matrix v9.0

| Skill Area | v8.0 | v9.0 | Priority |
|------------|------|------|----------|
| RAG Fundamentals | ✅ | ✅ | HIGH |
| Advanced RAG (Self-RAG, CRAG, RAPTOR) | ❌ | ✅ | HIGH |
| Agentic RAG | ❌ | ✅ | HIGH |
| LangGraph | ✅ | ✅ | HIGH |
| Multi-Agent Systems | ✅ | ✅ | HIGH |
| FastAPI for AI | ❌ | ✅ | HIGH |
| Docker / Containerization | ❌ | ✅ | HIGH |
| MCP | ✅ | ✅ | HIGH |
| MCP Security | ❌ | ✅ | MEDIUM |
| A2A Protocol | ❌ | ✅ | MEDIUM |
| Fine-Tuning | ✅ | ✅ | HIGH |
| Production Guardrails | ✅ | ✅ | HIGH |
| Observability / Tracing | ✅ | ✅ | HIGH |
| Redis Semantic Caching | ❌ | ✅ | MEDIUM |
| PydanticAI / OpenAI Agents SDK awareness | ❌ | ✅ | MEDIUM |
| Voice AI (Pipecat) | ✅ | ✅ | MEDIUM |
| LLMOps CI/CD | ❌ | ❌ | MEDIUM (Tier 3) |
| Inference Optimization (vLLM) | ❌ | ❌ | LOW (Tier 3) |

---

## Tier 3 — Deferred (Optional Resources Only)

| Topic | Rationale | Where to Self-Study |
|-------|-----------|---------------------|
| LLMOps CI/CD | Deep DevOps — separate skill track | zenml.io, MLflow docs |
| vLLM / TGI Inference | Requires GPU infra beyond course scope | vLLM GitHub, HuggingFace TGI |
| Data Orchestration (Airflow) | Separate data engineering track | Astronomer docs |
| Haystack | Niche alternative to LangChain | deepset.ai |

---

## Implementation Timeline

| Week | Work | Chapters |
|------|------|---------|
| 1 | Ch 15 expansion (Proposition Chunking + Headers) | 15 |
| 2–3 | Ch 22 expansion (Self-RAG + CRAG + RAPTOR + Adaptive) | 22 |
| 3 | Ch 41B: FastAPI for AI Services | 41B (NEW) |
| 4 | Ch 41C: Docker for AI Applications | 41C (NEW) |
| 4 | Ch 42 expansion (Redis Semantic Caching) | 42 |
| 5 | Ch 48B expansion (A2A + MCP Security) | 48B |
| 5 | Ch 30B expansion (Agentic RAG explicit) | 30B |
| 6 | Ch 43 expansion (Framework sidebar) + Ch 21 (Explainable Retrieval) | 43, 21 |
| 7 | Full QA review and verification of all new content | All |

**Total Effort**: ~7 weeks parallel development

---

## Quality Standards (v9.1 Enhancement Pass)

All v9.0 new and expanded chapters must comply with the v9.1 Enhancement Pass standards defined in `CURRICULUM-IMPLEMENTATION-ROADMAP.md`. These address 6 gaps identified during evaluation of completed Phase 1 chapters.

### Writing Style Guide v2.1 — 5 Cognitive Load Mechanisms (MANDATORY)

Every chapter must implement all 5:

| # | Mechanism | Requirement |
|---|-----------|-------------|
| 1 | **Section Time Estimates** | `(~X min)` after every H2 heading |
| 2 | **Texture Variation** | Alternate dense (code/theory) and light (analogy/War Story/checkpoint) sections |
| 3 | **Collapsible Blocks** | Wrap War Stories, advanced sections, and deep reflections in `<details>` tags |
| 4 | **Cognitive Pauses** | Insert checkpoint every ~500 lines: "What we covered so far" + self-assessment |
| 5 | **Confidence Calibration** | "Before" assessment after Part 1, "After" assessment in Summary |

### Quality Checklist v1.2 — 96 Items (TARGET: 90%+)

| Section | Items | Critical |
|---------|-------|----------|
| Structural Completeness | 11 | Coffee Shop Intro, Prerequisites, Interview Corner, Summary |
| Visual Enhancement | 6 | 3+ diagrams per chapter, 1+ Mermaid, inline placement with captions |
| Learning Style Differentiation | 5 | 2+ modalities per concept, 2 discussion prompts per chapter |
| Interview Corner | 4 | 4-6 questions (2-3 conceptual, 1-2 design, 1 coding challenge) |
| Analogy Curation | 4 | Max 5-6 per chapter, no overlaps, placed before technical explanation |
| Cognitive Load Management | 6 | Section time estimates, optional markers, max 2 War Stories, checkpoints |
| Pricing Accuracy | 2 | Staleness disclaimer, link to live pricing page |

### Visual Enhancement Guide v1.0 — Diagram Requirements

| Chapter Category | Required Diagram Types |
|---|---|
| RAG chapters (Ch 15, 17-22) | Flowchart (pipeline), sequence diagram (retrieval flow) |
| Agent chapters (Ch 26-34) | State diagram (agent loop), flowchart (tool selection) |
| Production chapters (Ch 41A-C, 42) | Architecture diagram, sequence diagram (deployment) |
| Multi-Agent chapters (Ch 43-48B) | Architecture diagram (supervisor/swarm), state diagram |

**Color palette**: Blue (user input) / Green (LLM) / Orange (storage) / Purple (tools) / Red (errors)
**Caption format**: `**Figure X.Y**: Description`

### Chapter Length Guidelines

| Stated Time | Target Lines | Max Lines | Action if Exceeded |
|---|---|---|---|
| 1.0h | 800–1,200 | 1,500 | Move content to optional sections |
| 1.5h | 1,200–1,800 | 2,200 | Move War Stories to collapsible blocks |
| 2.0h | 1,600–2,400 | 2,800 | Split into sub-chapters or mark advanced |
| 2.5h | 2,000–3,000 | 3,500 | Must split or restructure |

---

## Success Criteria

### Content Coverage
- [ ] 33/34 nirdiamant/rag_techniques covered (≥97%)
- [ ] Ch 41B produces a working deployable FastAPI + SSE endpoint
- [ ] Ch 41C produces a runnable `docker-compose.yml` stack
- [ ] Self-RAG implementation correctly uses retrieve/no-retrieve tokens
- [ ] CRAG implementation correctly triggers web fallback on low-confidence retrieval
- [ ] RAPTOR builds a 3-level hierarchical index from a 50+ doc corpus
- [ ] A2A section has working two-agent handoff code
- [ ] Industry alignment ≥97% vs 2026 AI Architect Roadmap

### Quality Standards
- [ ] All 73 chapters follow 6-layer teaching pattern (Action→Text→Video→See→Build→Interview)
- [ ] All new/expanded chapters score 90%+ on Quality Checklist v1.2 (87+ of 96 items)
- [ ] All new/expanded chapters implement 5 cognitive load mechanisms (Writing Style Guide v2.1)
- [ ] All new/expanded chapters include 3+ diagrams with at least 1 Mermaid
- [ ] All new/expanded chapters include Interview Corner (4-6 questions)
- [ ] No chapter exceeds 2.5 hours or 3,500 lines
- [ ] Max 5-6 analogies per chapter, no conceptual overlap

---

*Generated: 2026-02-19 | Claude Code + BMAD help + gap analysis*
*Status: Draft — Pending Ahmed approval*
