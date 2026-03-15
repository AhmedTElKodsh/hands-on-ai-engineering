# 🚀 LAYER 1 FINAL: THE AI ENGINEER ACCELERATOR

**Version:** 1.1 — March 9, 2026
**Status:** ✅ **CANONICAL — Use This Version**
**Duration:** 28 weeks (24 core + 2 flex + 2 job-prep)
**Time Commitment:** 20 hours/week (4 hours/day × 5 days)
**Target Role:** AI/GenAI Engineer (RAG, Agents, LLM Applications)

---

## 🎯 What This Is

### *One Path. 28 Weeks. 4 Hours/Day. Build-First. Portfolio-Driven.*

> **Design Philosophy:** The role of an AI Engineer has moved from building models to building with models. An AI engineer is an engineer who owns the design, evaluation, and production operation of systems built on foundation models. This curriculum is reverse-engineered from 1,000+ job postings and calibrated for a learner with 1 year of AI experience and 4 hours/day.

---

## 📋 Quick Start

### For New Students
1. **Take Day 00 Diagnostic:** [`guides/DAY-00-DIAGNOSTIC.md`](guides/DAY-00-DIAGNOSTIC.md)
2. **Track Progress:** [`guides/PROGRESS-TRACKER.md`](guides/PROGRESS-TRACKER.md)
3. **Start Week 1:** See Phase 1 below
4. **Log Costs:** [`guides/COST-LOG.md`](guides/COST-LOG.md) (from Week 3)
5. **Log Failures:** [`guides/FAILURE-LOG.md`](guides/FAILURE-LOG.md) (weekly)

### For AI Assistants (ChatGPT, Claude, etc.)
**→ Must Read:** [`guides/GUIDE-FOR-AI-ASSISTANTS.md`](guides/GUIDE-FOR-AI-ASSISTANTS.md)
- Teaching ladder (5 levels)
- Checkpoint rubrics
- Response templates
- Red flags when teaching wrong

---

## 📐 STRUCTURAL RULES

| Rule | Detail |
|------|--------|
| **Daily Split** | 🧠 80 min Learn → 🔨 120 min Build → 📝 40 min Document + Commit + Reflect |
| **One Repository** | All work lives in ONE portfolio repo. No separate Python repo. |
| **Weekly Deliverable** | Every week ends with a pushed, documented commit. No exceptions. |
| **Production Habits From Day 1** | Every piece of code has: type hints, docstrings, at least 1 test, proper error handling, and a README. |
| **Spiral Learning** | Topics revisit at increasing depth. RAG appears in Weeks 5, 7–10, 13, and the capstone. |
| **Failure Log** | Every week: "What broke, why, how I fixed it" in [`guides/FAILURE-LOG.md`](guides/FAILURE-LOG.md). |
| **System Design Practice** | Weeks 8, 12, 16, 20, 24: Draw architecture diagrams before coding. |
| **Cost Tracking** | From Week 3 onward: log every API call's token count and cost in [`guides/COST-LOG.md`](guides/COST-LOG.md). |

---

## 🗺️ Curriculum Overview

### Phase 0: Python Diagnostic (Before Week 1)

**Purpose:** Determine if you need Week 0 (remediation) or can skip straight to Week 1.

**The Test (90 minutes, no AI assistance):**
1. Load a CSV file, clean missing values, compute group-by statistics, output JSON
2. Write a class with __init__, 2 methods, and proper __repr__
3. Call a REST API, parse JSON response, handle errors with try/except
4. Write a function with type hints that takes a list of dicts, filters by a condition, and returns sorted results
5. Write 2 pytest tests for your function from #4

**STRICT FAILURE RULE:** Incomplete/Partial and Incorrect/Failing solutions are both recorded as **Weaknesses** (0 points) for that competency.

**Scoring:**
- **5/5 complete and clean:** Skip to Week 1. You're ready.
- **3–4/5:** Do Week 0 in 3 days (compressed), then start Week 1.
- **0–2/5:** Do full Week 0.

**→** [`guides/DAY-00-DIAGNOSTIC.md`](guides/DAY-00-DIAGNOSTIC.md)

---

### Phase 1: Engineering Foundations + LLM CONTACT (Weeks 1-4, 80 hours)

> In 2026, employers aren't just hiring for AI knowledge – they're hiring for strong engineers who can apply AI thoughtfully inside real products. The role is far more product- and systems-focused than many job titles suggest. We front-load backend engineering, SQL, and APIs because every AI engineer role demands them.

| Week | Topic | Key Deliverable |
|------|-------|-----------------|
| **1** | FastAPI + SQL + Git Foundations | Async CRUD API with PostgreSQL, migrations |
| **2** | Testing + Docker + CI/CD | Dockerized, tested API with CI pipeline |
| **3** | First LLM Integration | LLM-powered data extraction service with streaming |
| **4** | Embeddings + Vector Search Foundations | Hybrid search engine with pgvector + BM25 |

**🏗️ MINI-PROJECT #1: Smart Document API** (Weekend after Week 4)
Combine Weeks 1–3: FastAPI + PostgreSQL + LLM integration.

---

### Phase 2: RAG ENGINEERING — THE CORE SKILL (Weeks 5-10, 120 hours)

> Core responsibilities: Focus on building and operating end-to-end LLM applications such as RAG systems and agents, productionizing them with APIs, deployment, and monitoring, and ensuring quality through evaluation and guardrails. RAG is where you will spend the most time and where the market pays the most attention.

| Week | Topic | Key Deliverable |
|------|-------|-----------------|
| **5** | RAG Pipeline v1 — Build From Scratch | Working RAG API built from scratch, no frameworks |
| **6** | RAG Pipeline v2 — Advanced Retrieval | RAG with reranking, HyDE, caching, conversation memory |
| **7** | RAG Evaluation — The Skill That Gets You Hired | RAG evaluation pipeline with RAGAS |
| **8** | LangChain + LlamaIndex + Architecture Thinking | Same RAG rebuilt in 3 ways + architecture design doc |
| **9** | **FLEX WEEK** (Buffer + Catch-Up + Depth) | Catch-up / Polish / Advanced research |
| **10** | Production RAG Deployment | Cloud-deployed RAG with monitoring, guardrails, load-tested |

**🚩 FLAGSHIP PROJECT #1 STARTS WEEK 5**
Your Week 5 RAG system evolves through v1→v2→v3→final.

**🏗️ MINI-PROJECT #2: RAG Evaluation Dashboard** (Weekend after Week 10)

---

### Phase 3: AI AGENTS — THE GROWTH SKILL (Weeks 11-16, 120 hours)

> Agents have moved from research demos to production systems handling real money, real data and real consequences. The bar has shifted. Interviewers no longer want to hear about what agents could do — they want to know what breaks, what you've shipped and how you think about tradeoffs.

| Week | Topic | Key Deliverable |
|------|-------|-----------------|
| **11** | Agent Fundamentals | Hand-built agent with tools, memory, and safety guardrails |
| **12** | LangGraph — Production Agent Framework | LangGraph-based agentic RAG with human-in-the-loop |
| **13** | MCP + Tool Ecosystems | MCP-enabled agent ecosystem with 3 custom servers |
| **14** | Multi-Agent Systems | Multi-agent system with evaluation harness |
| **15** | Advanced Agent Patterns + Flagship v2 | Deployed multi-agent system with streaming, cost optimization |
| **16** | **FLEX + SPECIALIZATION SPRINT** | Track A/B/C mini-project |

**🚩 FLAGSHIP PROJECT #2 STARTS WEEK 12**
Your Week 12 agentic system evolves through v1→v2→final.

**Specialization Tracks (pick ONE):**
- **Track A:** NL2SQL Agent
- **Track B:** Document Intelligence
- **Track C:** Fine-Tuning Sprint

**→** [`docs/WEEK-16-SPECIALIZATION.md`](docs/WEEK-16-SPECIALIZATION.md)

---

### Phase 4: PRODUCTION ENGINEERING — WHAT GETS YOU HIRED (Weeks 17-22, 120 hours)

> Enterprise capability means: applied implementation experience, business outcome ownership, and scalable architecture mindset.

| Week | Topic | Key Deliverable |
|------|-------|-----------------|
| **17** | LLMOps + Observability | Full observability stack with tracing, monitoring, alerts |
| **18** | Auth + Multi-Tenancy + API Design | Multi-tenant, authenticated, versioned RAG API |
| **19** | Cloud Deployment + Infrastructure | Cloud-deployed Flagship with K8s, IaC (Terraform) |
| **20** | **FLEX WEEK + SYSTEM DESIGN PRACTICE** | 3 written system design documents |
| **21** | Full-Stack AI Application | Streamlit UI + chat interface + feedback loops |
| **22** | Security + Ethics + Documentation | Security-audited Flagship with ADRs |

**→** [`docs/WEEK-21-REFINED.md`](docs/WEEK-21-REFINED.md)

---

### Phase 5: CAPSTONE + JOB READINESS (Weeks 23-28, 120 hours)

| Week | Topic | Key Deliverable |
|------|-------|-----------------|
| **23-24** | Capstone Integration + Flagship Final Polish | Final integrated Flagships with full production polish |
| **25** | Portfolio + Personal Brand | Portfolio site, 2 blog posts, open-source contribution |
| **26** | Interview Preparation | Mock interviews, system design practice, coding prep |
| **27** | **FLEX WEEK** (Final Buffer) | Final polish / Specialization depth |
| **28** | Job Search Launch | Resumes, applications, networking |

---

## 📊 Portfolio Artifacts

| Artifact | Description | Shows |
|----------|-------------|-------|
| **Flagship #1: Enterprise RAG Platform** | Multi-tenant RAG with hybrid search, reranking, eval pipeline, monitoring, guardrails, cloud-deployed | RAG mastery, production engineering, evaluation thinking |
| **Flagship #2: AI Agent System** | Multi-agent system with MCP, LangGraph, tool-use, safety guardrails, streaming, deployed | Agent architecture, safety thinking, system design |
| **Mini-Project #1: Smart Document API** | FastAPI + PostgreSQL + LLM extraction | Backend engineering fundamentals |
| **Mini-Project #2: RAG Evaluation Dashboard** | Streamlit eval dashboard | Evaluation/metrics thinking |
| **3 System Design Documents** | Written architecture designs with trade-off analysis | System design interview readiness |
| **2 Blog Posts** | Technical writing about your architecture decisions | Communication skills |

---

## 🎓 Market Alignment

| Skill | Market Frequency | Where Covered |
|-------|-----------------|---------------|
| Python | 82.5% | Every single week |
| RAG | 35.9% | Weeks 5–10, Flagship #1 |
| Prompt Engineering | 29.1% | Week 3, used throughout |
| Docker | 31.0% | Week 2, used throughout |
| CI/CD | 29.3% | Week 2, used throughout |
| AWS/Cloud | 40.1% | Week 19, Flagship deployment |
| Kubernetes | 29.1% | Week 19 |
| LangChain | 18.8% | Week 8, used in agents |
| Agents | 14.4% | Weeks 11–16, Flagship #2 |
| MCP | Rising fast | Week 13 (dedicated) |
| Testing/Eval | Core req. | Week 2, Week 7, throughout |
| Monitoring | Core req. | Week 10, Week 17, throughout |

---

## 🔑 Key Differentiators

### What Makes LAYER 1 FINAL Different

| Feature | Other Curricula | LAYER 1 FINAL |
|---------|----------------|--------------|
| **SQL Placement** | Late or missing | **Week 1** (with FastAPI) |
| **Testing** | One week | **Week 2 + threaded** throughout |
| **Security** | Bolted on late | **Week 2 + Week 22 + threaded** |
| **Cost Tracking** | Not included | **Week 3 onward** (weekly logs) |
| **Failure Logging** | Not included | **Weekly mandatory** |
| **System Design** | Not included | **Weeks 8, 12, 20, 26** |
| **MCP** | Mentioned | **Week 13** (full week) |
| **Flagships** | 3 standalone | **2 evolving** (v1→v2→v3) |
| **Flex Weeks** | 0-4 weeks | **2 weeks** (Weeks 9, 27) |

---

## 🎯 Success Metrics (Summary)

- **Week 4:** Mini-Project #1 deployed.
- **Week 10:** Flagship #1 v3 deployed with evaluation.
- **Week 16:** Flagship #2 v2 deployed with MCP.
- **Week 22:** Both flagships production-ready with monitoring and security.
- **Week 28:** Portfolio complete, blog posts published, interviews ready.

---

**Detailed review and synthesis available in:** [`docs/ANALYSIS-COMMENTS.md`](docs/ANALYSIS-COMMENTS.md)

**Let's build. 🚀**
