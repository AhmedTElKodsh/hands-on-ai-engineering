# Progress Tracker — Layer 1 Final (28-Week AI Engineer Accelerator)

**Student Name:** ___________________
**Start Date:** ___________________
**Expected Completion:** ___________________
**Last Updated:** ___________________

---

## 📊 OVERALL PROGRESS

| Phase | Status | Start Date | End Date | Checkpoint Score |
|-------|--------|------------|----------|------------------|
| Phase 0: Python Diagnostic | ⬜ Not Started | | | /5 |
| Phase 1: Engineering Foundations | ⬜ Not Started | | | /5 |
| Phase 2: RAG Engineering | ⬜ Not Started | | | /5 |
| Phase 3: AI Agents | ⬜ Not Started | | | /5 |
| Phase 4: Production Engineering | ⬜ Not Started | | | /5 |
| Phase 5: Capstone + Job Readiness | ⬜ Not Started | | | /5 |

**Legend:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

---

## 🐍 PHASE 0: PYTHON DIAGNOSTIC (Before Week 1)

### Day 00 Diagnostic Test

**Date Taken:** ___________________

**STRICT FAILURE RULE:** Incomplete/Partial and Incorrect/Failing solutions are both recorded as **Weaknesses** (0 points) for that competency.

| Task | Complete | Score (0-1) | Notes |
|------|----------|-------------|-------|
| 1. CSV load, clean, groupby, JSON output | ⬜ | | |
| 2. Class with `__init__`, 2 methods, `__repr__` | ⬜ | | |
| 3. REST API call, JSON parse, error handling | ⬜ | | |
| 4. Function with type hints, filter, sort | ⬜ | | |
| 5. Write 2 pytest tests | ⬜ | | |

**Total Score:** _____ /5

**Path Based on Score:**
- [ ] **5/5:** Skip to Week 1
- [ ] **3-4/5:** Compressed Week 0 (3 days)
- [ ] **0-2/5:** Full Week 0 (5 days)

**Retake Date (if needed):** ___________________
**Retake Score:** _____ /5

---

## 📚 PHASE 1: ENGINEERING FOUNDATIONS + LLM (Weeks 1-4)

### Week 1: FastAPI + SQL + Git

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 1 | FastAPI CRUD API with 4 endpoints | ⬜ | |
| 2 | SQL queries + schema for API | ⬜ | |
| 3 | SQLAlchemy + Alembic migrations | ⬜ | |
| 4 | Async API conversion | ⬜ | |
| 5 | Git repo + pre-commit hooks | ⬜ | |

**Weekly Deliverable:** Async FastAPI CRUD API with PostgreSQL, migrations, OpenAPI docs

- [ ] API pushed to GitHub
- [ ] README with setup instructions
- [ ] OpenAPI docs accessible
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added (if applicable)

**Checkpoint Questions (Answer verbally without code):**
1. What's the difference between sync and async I/O? When does it matter?
2. Explain what an Alembic migration does and why you'd use it.
3. What happens if two API requests try to write to the same row simultaneously?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Sync vs Async | | |
| Q2: Alembic Migrations | | |
| Q3: Concurrent Writes | | |

**Checkpoint Score:** _____ /3

**Week 1 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 2: Testing + Docker + CI/CD

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 6 | 15+ pytest tests for Week 1 API | ⬜ | |
| 7 | Dockerfile + docker-compose | ⬜ | |
| 8 | GitHub Actions CI pipeline | ⬜ | |
| 9 | Structured logging + config management | ⬜ | |
| 10 | Rate limiting + health checks + error handling | ⬜ | |

**Weekly Deliverable:** Dockerized, tested, CI/CD-enabled API with logging

- [ ] Tests with 80%+ coverage
- [ ] Dockerfile (multi-stage)
- [ ] docker-compose.yml working
- [ ] CI pipeline passing
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. What's the difference between unit tests and integration tests?
2. Why multi-stage Docker builds?
3. How would you handle secrets in production vs. development?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Unit vs Integration | | |
| Q2: Multi-stage Docker | | |
| Q3: Secrets Management | | |

**Checkpoint Score:** _____ /3

**Week 2 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 3: First LLM Integration

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 11 | OpenAI + Anthropic API calls + token counter | ⬜ | |
| 12 | Prompt testing framework (5 strategies × 3 tasks) | ⬜ | |
| 13 | LLM data extractor (structured JSON output) | ⬜ | |
| 14 | Local model (Ollama) comparison | ⬜ | |
| 15 | Streaming + retry + fallback | ⬜ | |

**Weekly Deliverable:** LLM-powered data extractor with streaming, fallback, cost tracking

- [ ] Multi-provider support
- [ ] Structured output with validation
- [ ] Streaming responses
- [ ] Retry + fallback logic
- [ ] COST-LOG.md started
- [ ] FAILURE-LOG.md entry added
- [ ] 3 error case tests

**Checkpoint Questions:**
1. What are tokens? Why do they matter for cost and context?
2. When would you use a local model vs. an API?
3. How do you handle LLM API failures in production?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Tokens | | |
| Q2: Local vs API | | |
| Q3: Failure Handling | | |

**Checkpoint Score:** _____ /3

**Week 3 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 4: Embeddings + Vector Search

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 16 | Embedding generation + similarity from scratch | ⬜ | |
| 17 | pgvector setup + SQL similarity search | ⬜ | |
| 18 | ChromaDB implementation + comparison | ⬜ | |
| 19 | 3 embedding model benchmark | ⬜ | |
| 20 | Hybrid search (BM25 + vector) | ⬜ | |

**Weekly Deliverable:** Hybrid search engine with pgvector + BM25

- [ ] pgvector implementation
- [ ] ChromaDB implementation
- [ ] Comparison document
- [ ] Benchmark results
- [ ] Hybrid search working
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. Explain how cosine similarity works with embeddings in plain English.
2. When would pgvector be better than a dedicated vector DB?
3. What is hybrid search and why does it outperform pure vector search?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Cosine Similarity | | |
| Q2: pgvector vs Dedicated | | |
| Q3: Hybrid Search | | |

**Checkpoint Score:** _____ /3

**Week 4 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### 🏗️ MINI-PROJECT #1: Smart Document API (Weekend)

**Dates:** __________ to __________

- [ ] FastAPI + PostgreSQL + LLM integration
- [ ] Upload document → store metadata → extract with LLM → return JSON
- [ ] Dockerized + tested + CI/CD
- [ ] Deployed and accessible
- [ ] README with architecture diagram

**Mini-Project #1 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### PHASE 1 CHECKPOINT (End of Phase Verification)

**Date:** __________

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| 1. Explain async I/O and when it matters | | |
| 2. What does an Alembic migration do? | | |
| 3. What are tokens and why do they matter? | | |
| 4. Explain cosine similarity in plain English | | |
| 5. When would you use pgvector vs ChromaDB? | | |

**Phase 1 Checkpoint Score:** _____ /5

**Phase 1 Status:**
- [ ] **4-5/5:** Proceed to Phase 2
- [ ] **2-3/5:** Review weak areas, retry in 2 days
- [ ] **0-1/5:** Re-do Phase 1 projects with guidance

**Phase 1 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## 🔍 PHASE 2: RAG ENGINEERING (Weeks 5-10)

### Week 5: RAG Pipeline v1 (From Scratch)

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 21 | Naive RAG from scratch (no frameworks) | ⬜ | |
| 22 | Universal document loader (5+ formats) | ⬜ | |
| 23 | 4 chunking strategies comparison | ⬜ | |
| 24 | RAG prompt system with citations | ⬜ | |
| 25 | End-to-end RAG API | ⬜ | |

**Weekly Deliverable:** Working RAG API built from scratch

- [ ] Architecture diagram pushed
- [ ] 5+ document formats supported
- [ ] Chunking comparison table
- [ ] Citation tracking
- [ ] OpenAPI docs + 5 tests
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**🚩 FLAGSHIP PROJECT #1 STARTS HERE**

**Checkpoint Questions:**
1. Walk me through the RAG pipeline step by step.
2. Why does chunk size matter?
3. How do you track citations?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: RAG Pipeline | | |
| Q2: Chunk Size | | |
| Q3: Citations | | |

**Checkpoint Score:** _____ /3

**Week 5 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 6: RAG Pipeline v2 (Advanced Retrieval)

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 26 | Reranking layer + before/after metrics | ⬜ | |
| 27 | HyDE + multi-query implementation | ⬜ | |
| 28 | Parent-child chunking + metadata filters | ⬜ | |
| 29 | Conversation memory (last 5 turns) | ⬜ | |
| 30 | Redis caching + cost impact analysis | ⬜ | |

**Weekly Deliverable:** Flagship v2 — RAG with reranking, HyDE, parent-child chunks, caching

- [ ] Reranking implemented
- [ ] HyDE + multi-query working
- [ ] Parent-child chunking
- [ ] Conversation memory
- [ ] Redis caching with hit rate metrics
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. Why does reranking improve retrieval quality?
2. What is HyDE and when does it help?
3. What's the trade-off with caching?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Reranking | | |
| Q2: HyDE | | |
| Q3: Caching Trade-offs | | |

**Checkpoint Score:** _____ /3

**Week 6 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 7: RAG Evaluation

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 31 | Manual evaluation harness (20 Q&A pairs) | ⬜ | |
| 32 | RAGAS evaluation + score report | ⬜ | |
| 33 | Retrieval metrics (precision@k, MRR, NDCG) | ⬜ | |
| 34 | 5 intentional RAG failures + fixes | ⬜ | |
| 35 | Automated eval pipeline (8+ configurations) | ⬜ | |

**Weekly Deliverable:** Comprehensive RAG evaluation pipeline

- [ ] Evaluation dataset (20 Q&A pairs)
- [ ] RAGAS score report
- [ ] Retrieval metrics dashboard
- [ ] FAILURE-LOG.md with 5 failures
- [ ] Automated eval pipeline
- [ ] Best config analysis

**Checkpoint Questions:**
1. What's the difference between faithfulness and answer relevancy?
2. How do you calculate precision@k?
3. What's your weakest RAGAS metric and how will you improve it?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Faithfulness vs Relevancy | | |
| Q2: Precision@k | | |
| Q3: Improvement Target | | |

**Checkpoint Score:** _____ /3

**Week 7 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 8: LangChain + LlamaIndex + Architecture

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 36 | RAG rebuilt with LangChain | ⬜ | |
| 37 | RAG rebuilt with LlamaIndex | ⬜ | |
| 38 | LangSmith observability | ⬜ | |
| 39 | Framework decision guide (DECISION-GUIDE.md) | ⬜ | |
| 40 | **SYSTEM DESIGN DAY** — Multi-tenant RAG architecture | ⬜ | |

**Weekly Deliverable:** Flagship v2.5 — Same RAG in 3 ways + architecture doc

- [ ] LangChain implementation
- [ ] LlamaIndex implementation
- [ ] LangSmith tracing
- [ ] Framework comparison doc
- [ ] Architecture diagram pushed
- [ ] Written design doc
- [ ] FAILURE-LOG.md entry added

**Checkpoint Questions:**
1. You have 500K docs, strict PII, p95 < 2s. LangChain, LlamaIndex, or raw? Why?
2. Draw the data flow from user query to answer. Where are bottlenecks?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Framework Choice | | |
| Q2: Data Flow + Bottlenecks | | |

**Checkpoint Score:** _____ /2

**Week 8 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### WEEK 9: FLEX WEEK

**Dates:** __________ to __________

**Use this week for:**
- [ ] Catch up on incomplete weeks
- [ ] Deep-dive into weakest area from Weeks 1-8
- [ ] Polish Mini-Project #1
- [ ] Improve Flagship RAG v2.5
- [ ] Re-take checkpoint questions you couldn't answer

**Flex Week Goals:**
1. _________________________________
2. _________________________________
3. _________________________________

**Flex Week Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 10: Production RAG Deployment

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 41 | Prometheus metrics + Grafana dashboard | ⬜ | |
| 42 | Guardrails (PII filter + injection defense) | ⬜ | |
| 43 | Async document processing (task queue) | ⬜ | |
| 44 | Load testing + bottleneck identification | ⬜ | |
| 45 | Cloud deployment with live URL | ⬜ | |

**Weekly Deliverable:** Flagship v3 — Production-deployed RAG with monitoring, guardrails

- [ ] Monitoring dashboard (screenshots)
- [ ] Guardrails with adversarial tests
- [ ] Async ingestion pipeline
- [ ] Load test results + optimization notes
- [ ] Live deployment URL
- [ ] Deployment guide
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. What metrics would you monitor in production RAG?
2. How do you detect and prevent prompt injection?
3. What was your biggest performance bottleneck?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Production Metrics | | |
| Q2: Prompt Injection | | |
| Q3: Performance Bottleneck | | |

**Checkpoint Score:** _____ /3

**Week 10 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### 🏗️ MINI-PROJECT #2: RAG Evaluation Dashboard (Weekend)

**Dates:** __________ to __________

- [ ] Streamlit dashboard
- [ ] Evaluation scores over time
- [ ] Worst queries display
- [ ] Configuration comparison
- [ ] Cost per query metrics

**Mini-Project #2 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### PHASE 2 CHECKPOINT (End of Phase Verification)

**Date:** __________

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| 1. Walk through RAG pipeline step by step | | |
| 2. Why does chunk size matter? What's the trade-off? | | |
| 3. How do you prevent hallucinations in RAG? | | |
| 4. Explain reranking and why it helps | | |
| 5. You have 500K docs, PII policy, p95 < 2s. What architecture? | | |

**Phase 2 Checkpoint Score:** _____ /5

**Phase 2 Status:**
- [ ] **4-5/5:** Proceed to Phase 3
- [ ] **2-3/5:** Review weak areas, retry in 2 days
- [ ] **0-1/5:** Re-do Phase 2 projects with guidance

**Phase 2 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## 🤖 PHASE 3: AI AGENTS (Weeks 11-16)

### Week 11: Agent Fundamentals

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 46 | ReAct agent from scratch (no frameworks) | ⬜ | |
| 47 | 5 custom tools (search, file, calculator, SQL, API) | ⬜ | |
| 48 | LLM function calling integration | ⬜ | |
| 49 | 3-tier memory (short, working, long-term) | ⬜ | |
| 50 | Policy engine (permissions, budgets, approvals) | ⬜ | |

**Weekly Deliverable:** Hand-built agent with tools, memory, safety

- [ ] Architecture diagram
- [ ] Tool registry pattern
- [ ] 5 multi-step test scenarios
- [ ] Memory tests
- [ ] Boundary violation tests
- [ ] FAILURE-LOG.md entry added

**Checkpoint Questions:**
1. Explain the ReAct loop.
2. Why do you need guardrails on agents?
3. How do you prevent infinite loops?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: ReAct Loop | | |
| Q2: Guardrails Why | | |
| Q3: Infinite Loop Prevention | | |

**Checkpoint Score:** _____ /3

**Week 11 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 12: LangGraph — Production Agent Framework

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 51 | Agent rebuilt in LangGraph with state | ⬜ | |
| 52 | Human-in-the-loop + checkpointing | ⬜ | |
| 53 | Agentic RAG (routes between RAG/search/direct/IDK) | ⬜ | |
| 54 | Multi-step research workflow | ⬜ | |
| 55 | **SYSTEM DESIGN DAY** — Customer support agent | ⬜ | |

**Weekly Deliverable:** LangGraph agentic RAG with human-in-the-loop

- [ ] State diagram
- [ ] Interrupt flow tested
- [ ] Routing accuracy metrics
- [ ] Research workflow with 3 test questions
- [ ] Design doc with diagrams
- [ ] FAILURE-LOG.md entry added

**🚩 FLAGSHIP PROJECT #2 STARTS HERE**

**Checkpoint Questions:**
1. What's the difference between workflow (LangGraph) and autonomous agent?
2. Why add human-in-the-loop checkpoints?
3. How do you handle agent failures?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Workflow vs Autonomous | | |
| Q2: Human-in-the-Loop | | |
| Q3: Failure Handling | | |

**Checkpoint Score:** _____ /3

**Week 12 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 13: MCP + Tool Ecosystems

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 56 | MCP server exposing RAG as tool | ⬜ | |
| 57 | 3 custom MCP servers | ⬜ | |
| 58 | Agent connected to MCP servers | ⬜ | |
| 59 | 2 agents communicating (A2A) | ⬜ | |
| 60 | Audit logging + permission model | ⬜ | |

**Weekly Deliverable:** MCP-enabled agent ecosystem with 3 servers

- [ ] MCP config + README
- [ ] 3 MCP servers tested
- [ ] Multi-tool workflow tested
- [ ] Conversation log (A2A)
- [ ] Security review doc
- [ ] FAILURE-LOG.md entry added

**Checkpoint Questions:**
1. What is MCP and why is it becoming table stakes?
2. How do you secure tool access in MCP?
3. What's the difference between MCP and A2A?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: MCP What + Why | | |
| Q2: Tool Security | | |
| Q3: MCP vs A2A | | |

**Checkpoint Score:** _____ /3

**Week 13 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 14: Multi-Agent Systems

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 61 | Supervisor pattern implementation | ⬜ | |
| 62 | CrewAI analysis crew (Researcher + Analyst + Writer) | ⬜ | |
| 63 | Same crew in LangGraph + comparison | ⬜ | |
| 64 | Agent evaluation harness (10 diverse tasks) | ⬜ | |
| 65 | 5 intentional agent failures documented | ⬜ | |

**Weekly Deliverable:** Multi-agent system with evaluation harness

- [ ] Pattern comparison doc
- [ ] Output quality evaluation
- [ ] Framework comparison
- [ ] Evaluation results
- [ ] FAILURE-LOG.md with 5 failures
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. When would you use multi-agent vs single agent?
2. What are the trade-offs between CrewAI and LangGraph for multi-agent?
3. How do you evaluate agent task completion?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Multi vs Single Agent | | |
| Q2: CrewAI vs LangGraph | | |
| Q3: Agent Evaluation | | |

**Checkpoint Score:** _____ /3

**Week 14 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 15: Advanced Agent Patterns + Flagship v2

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 66 | Streaming output (thinking → tool calls → results) | ⬜ | |
| 67 | Checkpoint/resume for long-running tasks | ⬜ | |
| 68 | Smart model routing (cheap vs expensive) | ⬜ | |
| 69 | Deployed agent API with WebSocket streaming | ⬜ | |
| 70 | **Secondary Flagship v2 Polish Day** | ⬜ | |

**Weekly Deliverable:** Secondary Flagship v2 — Deployed multi-agent system

- [ ] Streaming demo
- [ ] Crash recovery tested
- [ ] Cost comparison table
- [ ] Deployment docs + live URL
- [ ] README with architecture diagram
- [ ] Demo recording
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. Why add streaming to agents?
2. How do you handle crash recovery?
3. What's your cost optimization strategy?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Streaming Why | | |
| Q2: Crash Recovery | | |
| Q3: Cost Optimization | | |

**Checkpoint Score:** _____ /3

**Week 15 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### WEEK 16: FLEX WEEK + SPECIALIZATION SPRINT

**Dates:** __________ to __________

**Days 1-3:** Catch-up/polish if needed

**Days 4-5:** Specialization exploration (pick ONE track)

**Specialization Track Selected:** ⬜ A (NL2SQL) ⬜ B (Document Intelligence) ⬜ C (Fine-Tuning)

| Track | Deliverable | Complete |
|-------|-------------|----------|
| A: NL2SQL Agent | Agent converts NL → SQL → execute → explain | ⬜ |
| B: Document Intelligence | Multi-modal extractor (tables + images + text) | ⬜ |
| C: Fine-Tuning | QLoRA fine-tune of 7B model on custom dataset | ⬜ |

**All Tracks Require:**
- [ ] 10+ test queries/documents
- [ ] Security boundaries documented
- [ ] Deployed with UI or API
- [ ] Blog post explaining learnings

**Specialization Sprint Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### PHASE 3 CHECKPOINT (End of Phase Verification)

**Date:** __________

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| 1. Explain the ReAct loop | | |
| 2. Why do you need guardrails on agents? | | |
| 3. How do you prevent infinite loops? | | |
| 4. When would you use workflow vs autonomous agent? | | |
| 5. What is MCP and why is it table stakes? | | |

**Phase 3 Checkpoint Score:** _____ /5

**Phase 3 Status:**
- [ ] **4-5/5:** Proceed to Phase 4
- [ ] **2-3/5:** Review weak areas, retry in 2 days
- [ ] **0-1/5:** Re-do Phase 3 projects with guidance

**Phase 3 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## 🏭 PHASE 4: PRODUCTION ENGINEERING (Weeks 17-22)

### Week 17: LLMOps + Observability

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 71 | Experiment tracking (MLflow/W&B) | ⬜ | |
| 72 | Distributed tracing (OpenTelemetry) | ⬜ | |
| 73 | Automated alerts (quality, latency, cost) | ⬜ | |
| 74 | Prompt management with versioning | ⬜ | |
| 75 | Runbooks for 5 failure scenarios | ⬜ | |

**Weekly Deliverable:** Flagship v3.5 — Full observability stack

- [ ] Experiment dashboard
- [ ] Trace visualization
- [ ] Alerting rules configured
- [ ] Prompt version history
- [ ] RUNBOOKS.md with 5 scenarios
- [ ] FAILURE-LOG.md entry added

**Checkpoint Questions:**
1. What would you monitor in production RAG?
2. How do you detect response quality drift?
3. What's in a good runbook?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Production Monitoring | | |
| Q2: Quality Drift Detection | | |
| Q3: Runbook Contents | | |

**Checkpoint Score:** _____ /3

**Week 17 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 18: Auth + Multi-Tenancy + API Design

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 76 | JWT auth + API key auth | ⬜ | |
| 77 | Tenant isolation (own docs, embeddings) | ⬜ | |
| 78 | API versioning (v1 → v2) | ⬜ | |
| 79 | Job status endpoint | ⬜ | |
| 80 | Full API docs + Getting Started guide | ⬜ | |

**Weekly Deliverable:** Flagship v4 — Multi-tenant, authenticated, versioned RAG API

- [ ] Auth tests
- [ ] Tenant isolation tests
- [ ] Migration guide (v1 → v2)
- [ ] Job lifecycle tests
- [ ] Docs site
- [ ] FAILURE-LOG.md entry added

**Checkpoint Questions:**
1. What's the difference between JWT and API key auth?
2. How do you ensure tenant isolation?
3. Why version your API?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: JWT vs API Key | | |
| Q2: Tenant Isolation | | |
| Q3: API Versioning | | |

**Checkpoint Score:** _____ /3

**Week 18 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 19: Cloud Deployment + Infrastructure

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 81 | Deploy to cloud (managed PostgreSQL + Redis) | ⬜ | |
| 82 | Deploy to K8s cluster | ⬜ | |
| 83 | Managed AI service (Bedrock/Vertex/Azure OpenAI) | ⬜ | |
| 84 | Terraform for infrastructure | ⬜ | |
| 85 | Cost dashboard + budget alerts | ⬜ | |

**Weekly Deliverable:** Cloud-deployed Flagship with K8s, IaC, cost management

- [ ] Infrastructure diagram
- [ ] K8s manifests
- [ ] Service comparison doc
- [ ] terraform/ directory
- [ ] Cost analysis doc
- [ ] FAILURE-LOG.md entry added
- [ ] COST-LOG.md entry added

**Checkpoint Questions:**
1. What are the core AWS/GCP services for AI apps?
2. What problem does Kubernetes solve?
3. Why use Infrastructure as Code?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Cloud Services | | |
| Q2: Kubernetes Why | | |
| Q3: IaC Benefits | | |

**Checkpoint Score:** _____ /3

**Week 19 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### WEEK 20: FLEX WEEK + SYSTEM DESIGN PRACTICE

**Dates:** __________ to __________

**Days 1-3:** Catch-up and polish

**Days 4-5:** System design practice

**System Design Exercises Completed:**
- [ ] RAG system for 500K docs with PII policy and p95 < 2s
- [ ] Multi-agent customer support (1000 concurrent conversations)
- [ ] Content moderation pipeline (10K items/hour with human-in-the-loop)

**Deliverable:** 3 written system design documents with:
- [ ] Architecture diagrams
- [ ] Trade-off analysis
- [ ] Cost estimates

**Flex Week Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 21: Full-Stack AI Application

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 86 | Streamlit UI (multi-page, session state, caching) | ⬜ | |
| 87 | Standalone chat interface (HTML/CSS/JS) | ⬜ | |
| 88 | React chat component with streaming | ⬜ | |
| 89 | Real-time streaming + source display | ⬜ | |
| 90 | Feedback collection + analytics | ⬜ | |

**Weekly Deliverable:** Full-stack Flagship with Streamlit + chat UI

- [ ] Screenshots pushed
- [ ] Responsive design
- [ ] Streaming demo
- [ ] Feedback dashboard
- [ ] FAILURE-LOG.md entry added

**⚠️ SCOPE NOTE:** If struggling, prioritize:
1. Streamlit UI (MUST)
2. Basic chat interface (SHOULD)
3. WebSocket streaming (NICE)
4. React component (OPTIONAL)

**Checkpoint Questions:**
1. Why use Streamlit for AI demos?
2. What's the value of a standalone UI vs API only?
3. How do you collect and use user feedback?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Streamlit Why | | |
| Q2: UI vs API Only | | |
| Q3: Feedback Loop | | |

**Checkpoint Score:** _____ /3

**Week 21 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 22: Security + Ethics + Documentation

**Dates:** __________ to __________

| Day | Deliverable | Complete | Notes |
|-----|-------------|----------|-------|
| 91 | Security audit (10 attack vectors tested) | ⬜ | |
| 92 | PII detection + redaction pipeline | ⬜ | |
| 93 | Moderation layer + adversarial tests | ⬜ | |
| 94 | 3 Architecture Decision Records (ADRs) | ⬜ | |
| 95 | Full codebase refactor + cleanup | ⬜ | |

**Weekly Deliverable:** Security-audited, documented, production-polished Flagship

- [ ] Security audit report
- [ ] PII handling tests
- [ ] Moderation results
- [ ] docs/ directory with ADRs
- [ ] Clean codebase
- [ ] FAILURE-LOG.md entry added

**Checkpoint Questions:**
1. What are common prompt injection attacks?
2. How do you handle PII in RAG systems?
3. What goes in an Architecture Decision Record?

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Prompt Injection | | |
| Q2: PII Handling | | |
| Q3: ADR Contents | | |

**Checkpoint Score:** _____ /3

**Week 22 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### PHASE 4 CHECKPOINT (End of Phase Verification)

**Date:** __________

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| 1. What would you monitor in production RAG? | | |
| 2. How do you handle API failures? | | |
| 3. What security concerns exist in LLM apps? | | |
| 4. How do you measure system quality? | | |
| 5. Explain tenant isolation and why it matters | | |

**Phase 4 Checkpoint Score:** _____ /5

**Phase 4 Status:**
- [ ] **4-5/5:** Proceed to Phase 5
- [ ] **2-3/5:** Review weak areas, retry in 2 days
- [ ] **0-1/5:** Re-do Phase 4 projects with guidance

**Phase 4 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## 🎓 PHASE 5: CAPSTONE + JOB READINESS (Weeks 23-28)

### Weeks 23-24: Capstone Integration + Flagship Final Polish

**Dates:** __________ to __________

**Flagship #1 Final Polish:**
- [ ] Multi-tenant auth integrated
- [ ] Monitoring dashboard complete
- [ ] Cost tracking automated
- [ ] Evaluation pipeline running
- [ ] Feedback loop implemented
- [ ] Deployment automated
- [ ] Load tested + optimized
- [ ] README with tech decisions
- [ ] Architecture diagram
- [ ] Evaluation metrics
- [ ] Cost analysis
- [ ] Demo video (3 min)
- [ ] Iteration log (v1→v2→v3→final)
- [ ] Failure log complete

**Flagship #2 Final Polish:**
- [ ] Same checklist as Flagship #1

**Capstone Integration:**
- [ ] RAG + Agent merged into one platform
- [ ] Before/after optimization metrics
- [ ] Deployment checklist complete

**Weeks 23-24 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 25: Portfolio + Personal Brand

**Dates:** __________ to __________

| Day | Activity | Complete |
|-----|----------|----------|
| 106 | Audit all projects (READMEs, screenshots, tests) | ⬜ |
| 107 | Write technical blog post #1 (RAG architecture) | ⬜ |
| 108 | Create portfolio website | ⬜ |
| 109 | Open-source contribution (PR submitted) | ⬜ |
| 110 | LinkedIn + GitHub profile optimization | ⬜ |

**Deliverables:**
- [ ] All projects have clean READMEs
- [ ] Blog post #1 published (dev.to or Medium)
- [ ] Blog post #2 published (Agent safety) — can be Week 27
- [ ] Portfolio website live
- [ ] OSS PR merged or in review
- [ ] LinkedIn headline: "AI Engineer"
- [ ] GitHub profile README

**Week 25 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 26: Interview Preparation

**Dates:** __________ to __________

| Day | Activity | Complete |
|-----|----------|----------|
| 111 | AI System Design Practice (45 min timed) | ⬜ |
| 112 | Technical Deep Dive (recorded explanation) | ⬜ |
| 113 | Coding Interview (mini-RAG in 60 min) | ⬜ |
| 114 | Behavioral Interview (STAR stories) | ⬜ |
| 115 | Full Mock Interview | ⬜ |

**Deliverables:**
- [ ] System design document (timed)
- [ ] Recorded project explanation (watched + critiqued)
- [ ] Mini-RAG built in 60 minutes
- [ ] 3 STAR stories prepared
- [ ] Mock interview completed (with AI or peer)
- [ ] Mock interview feedback addressed

**Week 26 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### WEEK 27: FLEX WEEK (Final Buffer)

**Dates:** __________ to __________

**Use for:**
- [ ] Remaining catch-up
- [ ] Additional system design practice
- [ ] Extra portfolio polish
- [ ] Blog post #2 (if not done)
- [ ] Networking and community engagement

**Flex Week Goals:**
1. _________________________________
2. _________________________________
3. _________________________________

**Flex Week Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### Week 28: Job Search Launch

**Dates:** __________ to __________

| Day | Activity | Complete |
|-----|----------|----------|
| 116 | Resume writing (tailored for 3 job descriptions) | ⬜ |
| 117 | Job tracking spreadsheet + 20 target companies | ⬜ |
| 118 | Apply to first 5 positions (customized) | ⬜ |
| 119 | Networking (10 LinkedIn connections) | ⬜ |
| 120 | Continuous learning plan | ⬜ |

**Deliverables:**
- [ ] Resume tailored for AI Engineer roles
- [ ] Job tracking spreadsheet
- [ ] 5 applications submitted
- [ ] 10 LinkedIn connections with AI engineers
- [ ] RSS feeds + newsletters for continuous learning

**Week 28 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

### PHASE 5 CHECKPOINT (End of Phase Verification)

**Date:** __________

| Deliverable | Complete | Quality (1-5) |
|-------------|----------|---------------|
| Flagship #1 Final | ⬜ | |
| Flagship #2 Final | ⬜ | |
| Portfolio Website | ⬜ | |
| Blog Post #1 | ⬜ | |
| Blog Post #2 | ⬜ | |
| Mock Interview Pass | ⬜ | |

**Phase 5 Checkpoint Score:** _____ /30

**Phase 5 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## 🎯 FINAL COMPLETION CHECKLIST

### Portfolio Artifacts
- [ ] Flagship #1: Enterprise RAG Platform (deployed, documented, demo)
- [ ] Flagship #2: AI Agent System (deployed, documented, demo)
- [ ] Mini-Project #1: Smart Document API
- [ ] Mini-Project #2: RAG Evaluation Dashboard
- [ ] 3 System Design Documents
- [ ] 2 Blog Posts

### Job Readiness
- [ ] Resume tailored for AI Engineer
- [ ] LinkedIn profile optimized
- [ ] GitHub profile with pinned projects
- [ ] 20+ job applications submitted
- [ ] 3+ mock interviews completed

### Skills Verification
- [ ] Can explain RAG architecture verbally
- [ ] Can debug a broken RAG pipeline in <30 min
- [ ] Can design a system for 500K docs with PII policy
- [ ] Can explain agent safety approach

---

## 📊 COMPLETION SUMMARY

| Phase | Start Date | End Date | Checkpoint Score | Status |
|-------|------------|----------|------------------|--------|
| Phase 0 | | | /5 | |
| Phase 1 | | | /5 | |
| Phase 2 | | | /5 | |
| Phase 3 | | | /5 | |
| Phase 4 | | | /5 | |
| Phase 5 | | | /30 | |

**Total Weeks:** _____ /28

**Curriculum Completed:** ⬜ Yes ⬜ No

**Completion Date:** ___________________

**Next Steps:**
1. _________________________________
2. _________________________________
3. _________________________________

---

## 📝 NOTES + REFLECTIONS

### Week-by-Week Reflections

**Week 1:**
- What went well:
- What was hard:
- What I learned:

**Week 2:**
- What went well:
- What was hard:
- What I learned:

[Continue for each week...]

---

### Biggest Wins

1. _________________________________
2. _________________________________
3. _________________________________

---

### Biggest Challenges

1. _________________________________
2. _________________________________
3. _________________________________

---

### What I'd Do Differently

1. _________________________________
2. _________________________________
3. _________________________________

---

**Remember:** The goal is not to complete the curriculum. The goal is to become a developer who can build AI systems independently.

**Let's build. 🚀**
