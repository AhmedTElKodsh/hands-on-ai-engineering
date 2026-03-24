# Layer One AI Engineer Accelerator Plan for 2026 Hiring Reality

**Document Status:** Modified v2.0 - Analyzed and restructured per BMAD workflow standards  
**Last Updated:** 2026-03-08  
**Owner:** Ahmed  
**Purpose:** Production-calibrated 26-week curriculum for AI Engineer roles

---

## Executive Summary

This plan delivers a **production-ready AI Engineer** in 26 weeks (624 study hours @ 4h/day, 6 days/week) through systematic skill building aligned with 2026 market demands. Core output: one flagship **Knowledge Assistant Platform** (RAG + agents + evaluation + observability + security) plus 4 portfolio artifacts demonstrating end-to-end ownership.

**Key Differentiators:**
- Backend-first approach (FastAPI + Postgres + SQL from Week 2)
- Evaluation and observability as core disciplines, not afterthoughts
- Security/guardrails integrated throughout, not bolted on
- Realistic scope: 4-6 deep projects vs. 20 shallow demos
- Framework pragmatism: build raw first, then adopt one deeply

**Market Alignment:** Directly addresses requirements from NielsenIQ, Cognilium, Particula, and similar 2026 AI Engineer postings emphasizing production systems over research breadth.

---

## What the 2026 job market consistently signals

Across recent, real job descriptions for AI Engineer / GenAI backend roles, the “core” is no longer classic ML breadth; it is **shipping dependable LLM features end-to-end**: backend engineering + retrieval + evaluation + operations.

A representative example: NielsenIQ’s “Software Engineer (Python, FastAPI, LLM, GenAI, RAG)” role explicitly frames the work around **Python + FastAPI**, **cloud-native microservices**, **RAG pipelines**, **agent workflows**, **observability/instrumentation**, **CI/CD**, and **strong SQL** (plus Docker and cloud exposure). citeturn13view0 Another example (Cognilium AI) describes the job as building **production-grade RAG with grounding/citations/guardrails**, **high-performance async FastAPI**, plus “real backend” responsibilities like **authentication, rate limiting, background jobs**, and **observability/monitoring**, with deployment to cloud (AWS-first) and Docker/CI/CD. citeturn13view1

This same pattern repeats in the Particula “AI/ML Engineer (LLMs & RAG)” posting: build LLM features end-to-end, ingest/clean/index data for RAG, establish **evaluation and observability for RAG**, optimize for hallucinations/latency/cost, plus Docker and CI/CD; it even name-checks MLflow and RAGAS as examples for tracking and evaluation. citeturn13view3

Two implications matter for your rewritten plan:

First, **evaluation and monitoring are not “advanced extras” anymore**—they are part of the definition of production AI. Databricks’ RAG guidance makes this explicit: evaluation and monitoring determine whether a RAG system meets **quality, cost, and latency** requirements, and RAG is a multi-component system where changes cascade, so you must evaluate components and the full chain. citeturn15view1 OpenAI’s Applied Evals role reinforces this industry direction: building evals/harnesses and “reproducible signals” is a central engineering job, especially for multi-turn/tool-using systems. citeturn15view2

Second, **security and guardrails are now mainstream engineering requirements** for any RAG/agent system exposed to users. AWS publishes concrete, production-minded guidance on prompt injection defenses, describing guardrails as necessary and emphasizing token-cost-aware guardrails (because guardrails add tokens and can reduce accuracy if overengineered). citeturn16view0turn16view1 Recent research similarly shows prompt injection is a real, testable failure mode for RAG-enabled agents and argues for benchmark-driven, multi-layer defenses. citeturn16view2

Finally, **tool standards are forming**. MCP (Model Context Protocol) is described in LangChain’s documentation as an open protocol for describing tools/data sources so LLM systems can discover/use them via structured APIs, and today’s MCP roadmap explicitly focuses on enterprise readiness items like audit trails/observability and enterprise auth patterns. citeturn14view1turn14view0

These signals strongly favor a Layer One plan that prioritizes: FastAPI + SQL/Postgres (often with vectors), retrieval and ranking, evaluation harnesses, observability/cost, and security/guardrails—over long blocks of unrelated classic ML and deep learning training.

---

## Critical Analysis: Original Plan vs. Market Reality

### Strengths Identified
- Build-first philosophy with daily commits
- Weekly deliverables creating momentum
- Spiral reinforcement of concepts
- Recognition of framework ecosystem

### Critical Gaps Requiring Modification

**1. Workload Realism**  
Original plan: 728 hours requiring 7-day weeks for 26 weeks with zero buffer.  
**Issue:** No accommodation for debugging, framework changes, life events.  
**Fix:** 624-hour plan (6 days/week) with built-in iteration time.

The biggest issue is the implied workload. Your plan sums to **728 hours**, which only “fits” if you study **7 days/week for 26 weeks** (no rest weeks, no travel, no illness, no life). That is mathematically consistent but practically fragile; even the Layer1 repo’s own “realistic timeline” guidance warns to budget for debugging, framework breakage, and the reality that self-taught learners take longer (and it explicitly calls out that frameworks like LangChain change frequently, making older tutorials break). citeturn9view0turn7view0

The second issue is topic prioritization. Your plan devotes **6 full weeks** to classic ML foundations and deep learning (regression/classification, CNNs, LSTMs, ResNet fine-tuning, BERT fine-tuning), before you reach the “money zone.” For the 2026 AI Engineer market, that is usually not the bottleneck. Many roles are explicitly backend + RAG + agents + ops. NielsenIQ emphasizes cloud-native backend engineering, RAG, agents, observability, CI/CD, SQL. citeturn13view0 Cognilium emphasizes async APIs, service boundaries, auth/rate limiting/background jobs, evaluation/monitoring/rollback/cost governance. citeturn13view1 Those are the skills that typically separate “demo builders” from “hired engineers.”

Third, you propose **20 portfolio projects**. That volume tends to produce shallow projects and repeated scaffolding overhead. Layer1’s own extended plan explicitly warns what looks like a tutorial clone (e.g., MNIST/Titanic) and says portfolio quality is signaled by unique corpus, documented experiments, failure analysis, cost analysis, and evidence of iteration. citeturn9view4 In hiring, 3–6 strong projects with deep engineering signals usually beat 20 small ones.

Fourth, your plan makes fine-tuning sound mandatory. In reality it is **often a “nice-to-have”** for many AI engineer jobs (for example NielsenIQ lists fine-tuning as a plus, not as a requirement). citeturn13view0 Some roles do demand LoRA/QLoRA (even fully), but those are typically more specialized or more senior (example: a “RAG & Fine-Tuning Specialist” posting explicitly asks for LoRA/QLoRA plus RAG and AWS—yet it also lists 5+ years experience). citeturn18view0 So fine-tuning should be positioned in Layer One as a **decision skill + optional specialization sprint**, not as a universal requirement.

Fifth, your plan says to “kill the standalone Python repo.” That is not aligned with what you already built: your Python-Daily-Practice repo is a well-structured testing-based system with a Day 00 diagnostic and progressive weekly projects, which can be reused as targeted remediation without becoming a separate “preparation season.” citeturn11view0turn12view0turn12view1

**Bottom line:** the plan does not need to be thrown away; it needs to be **reweighted**. The modified Layer One below keeps your best design choices but shifts time from classic ML/DL into production-grade AI backend engineering, retrieval quality, evaluation/observability, and security—because those are consistently demanded. citeturn13view0turn13view1turn13view3turn15view1turn16view0

## Design constraints and rules for the rewritten Layer One

This revised plan is written to be realistic, portfolio-effective, and aligned with both your repositories and 2026 hiring signals.

Your own Layer1 curriculum documents already contain a strong daily pedagogy: “guided action-first,” a rapid first win, daily commits, and spaced review/logbook; they also warn about dependency breakage and recommend pinning versions. citeturn7view0 Layer2’s evolution decisions also explicitly endorse “LLM magic early,” “build from scratch then frameworks,” and added topics like Ollama, advanced prompting, fine-tuning, and MCP, while preserving a Python foundations phase learners can skip if proficient. citeturn10view0 The rewrite below follows those principles, but optimized for employability.

Core operating rules:

A realistic schedule is **6 study days/week** (4 hours/day) with one rest day, plus built-in buffer weeks. This yields ~624 hours of capacity over 26 weeks, but because debugging and iteration are where the learning happens, this plan deliberately does *not* attempt to “consume” all hours with new topics.

Python is learned *through* AI tasks, but not by deleting your Python repo. Instead: use **Day 00 diagnostic** once in Week 1, then use 2–3 targeted drills/week only where weak. citeturn11view0turn12view0turn12view1

Each week ends with one “shippable artifact”: a tagged GitHub release, a demo video (even 60–120 seconds), and a README update that includes “what failed and what we changed.” This aligns with the portfolio signals emphasized in your Layer1 extended plan. citeturn9view4

Framework breadth is controlled. You will implement core components “raw” first (as your curriculum design intends), then adopt one orchestration framework deeply (LangGraph or LangChain) and treat others as electives. citeturn10view0turn2view0

Security is not a late add-on. Every time you introduce retrieval, tool-use, or multi-tenancy, you also introduce a corresponding guardrail and a test. AWS guidance emphasizes guardrails for prompt injection and warns overengineering can hurt accuracy and cost. citeturn16view0turn16view1

## The rewritten Layer One plan

This is a full replacement Layer One that you can paste into your repo as `Layer1-Curriculum/docs/LAYER1-V2-26-WEEK-PLAN.md`. It preserves your “build-first” DNA, but changes the weightings to match how teams actually hire and ship GenAI systems in 2026. citeturn13view0turn13view1turn15view1turn16view0

### Plan overview

You will build **one flagship system** and evolve it through 5 releases:

**Flagship product:** a production-style **Knowledge Assistant Platform** (RAG + agent tools + evaluation + observability + guardrails) delivered as a FastAPI service with Postgres (including pgvector), background jobs, and a simple UI (Streamlit first; optional lightweight web UI later). This mirrors the real job expectations of end-to-end delivery and “owning the system” described in postings like NielsenIQ and Cognilium. citeturn13view0turn13view1

You will also build **two smaller artifacts** that increase hiring signal without exploding scope:
- A **Structured Extraction service** (LLM + schemas + validation + retry/cost policies).
- A **Tool/Agent sandbox** (safe tool execution, prompt injection tests, agent eval harness).

Fine-tuning becomes an **optional specialization sprint** (2 weeks max) with a strict ROI decision rule: do it only if your target roles mention it or your chosen capstone domain benefits from it. This matches market reality where fine-tuning is sometimes valued but often “nice-to-have.” citeturn13view0turn18view0

MCP is treated as an **integration and standards week**, not a multi-week detour: learn what it is, expose one tool server, consume one external MCP server, log called tools, and move on. citeturn14view1turn14view0

### Weekly cadence template

Each study day is 4 hours:

- **Learn (60–75 min):** read docs + one reference implementation; write *one page* of notes that you can reuse in interviews.
- **Build (150–165 min):** ship the feature; keep scope minimal enough to finish.
- **Ship (30 min):** tests, README update, and commit.

Weekly rhythm (recommended):
- **Days 1–2:** implement core feature.
- **Days 3–4:** extend + add failure handling.
- **Day 5:** evaluation + tests + measured improvement.
- **Day 6:** refactor + documentation + short demo video + system design notes.
- **Day 7:** rest.

### Detailed 26-week schedule

What follows is the “full detailed” plan. It is intentionally written as week-by-week with day clusters so it remains executable, not just aspirational.

#### Foundation and baseline engineering

**Week one: engineering environment and Python reality-check**
- Days 1–2: Set up repo structure for a real service (`src/`, `tests/`, `infra/`, `docs/`, `scripts/`), run `pytest`, and add a CI workflow that runs tests on push (even if tests are trivial at first). Your current curricula emphasize automated verification and daily commits; establish that from day one. citeturn7view0turn2view0  
- Days 3–4: Run Python-Daily-Practice Day 00 diagnostic and record which areas fail. Then patch only the weak areas with 1–2 drills (do not “finish Python first”). citeturn11view0  
- Day 5: Add configuration management (`.env`, Pydantic settings), structured logging baseline, and a minimal CLI entrypoint (`python -m app`).  
- Day 6 deliverable: “Week 1 release” = repo compiles, tests run in CI, README has setup steps, and a 60s video showing a “hello world” command.

**Week two: FastAPI + SQL essentials early**
This is non-negotiable because many roles demand it explicitly (Python + FastAPI + SQL). citeturn13view0turn13view1  
- Days 1–2: Build a FastAPI skeleton with `/health`, `/version`, request IDs, and Pydantic request/response models.  
- Days 3–4: Add Postgres with migrations (Alembic or equivalent) and implement one table (`conversations`, `messages`, or `documents`). Build “create/read/list” endpoints.  
- Day 5: Basic SQL proficiency sprint: joins, aggregates, indexes. Use a local dataset and build one query that would matter in production: “top queries by cost,” “top retrieval misses,” etc.  
- Day 6 deliverable: docker-compose that runs API + Postgres, with seeded data and a README showing how to hit endpoints.

#### LLM integration as a backend discipline

**Week three: LLM interface design (reliability before fancy prompts)**
Your Layer2 philosophy calls for “LLM magic early” and accessible first calls; do it here, but engineer it properly. citeturn10view0turn7view0  
- Days 1–2: Implement a provider-agnostic LLM client wrapper (even if you only use one provider initially): retries, timeouts, request IDs, and structured error types.  
- Days 3–4: Add streaming responses over HTTP (server-sent events or websocket streaming) and store streamed outputs in the DB.  
- Day 5: Cost controls: token counting, per-request cost estimation, caching for “repeat prompts.” Layer1’s plan already highlights cost awareness and model selection. citeturn7view0  
- Day 6 deliverable: “LLM Chat API v1” with streaming, persisted conversation history, and a cost log table.

**Week four: structured outputs and extraction service**
Structured extraction is repeatedly requested in job postings (entity extraction/classification, structured outputs), and it’s one of the cleanest ways to demonstrate “I can ship reliable LLM code.” citeturn13view3turn13view0  
- Days 1–2: Implement JSON-structured output using strict schemas (Pydantic) and validation with retry-on-parse-failure.  
- Days 3–4: Build a mini “Document Extractor” endpoint: upload text (later PDF) → extract fields → return validated JSON + confidence notes.  
- Day 5: Add adversarial tests: malformed input, partial inputs, prompt injection attempt inside the “document.” Use guardrails guidance from AWS as the baseline approach (defense-in-depth, avoid huge guardrails). citeturn16view0turn16view1  
- Day 6 deliverable: **Portfolio Artifact 1** — Structured Extraction service with tests and a demo dataset.

#### Retrieval engineering and RAG quality

This block is the heart of AI Engineering hiring. It should be deeper than “chat with PDF,” and your own Layer1 docs emphasize that advanced RAG requires experiments, debugging, cost analysis, and iteration—not a tutorial clone. citeturn9view4turn13view1

**Week five: ingestion pipeline and chunking experiments**
- Days 1–2: Build ingestion pipeline v1: load markdown/txt first, store raw docs + metadata, generate chunks.  
- Days 3–4: Add PDFs (basic parsing first), store “document → chunks” lineage and chunking parameters in DB.  
- Day 5: Run controlled chunking experiments (size/overlap/semantic splitting) and log retrieval outcomes.  
- Day 6 deliverable: ingestion CLI + ingestion API + “chunking experiment report” in README.

**Week six: embeddings and vector storage on Postgres**
Many production stacks use Postgres with vectors to keep transactional and vector data together; many job descriptions also demand strong SQL. citeturn13view0turn13view1turn13view3  
- Days 1–2: Add embeddings generation module with a clear interface (supports provider embeddings or local embeddings later).  
- Days 3–4: Add pgvector index and implement similarity search with metadata filtering (document type, tenant, tags).  
- Day 5: Implement retrieval metrics logging (top-k, latency, hit rate).  
- Day 6 deliverable: “Retrieval service v1” with reproducible ingestion and retrieval tests.

**Week seven: RAG assembly with citations and failure modes**
Cognilium explicitly mentions grounding/citations/guardrails as part of production RAG. citeturn13view1  
- Days 1–2: Implement RAG prompt assembly that always returns “answer + sources,” with a strict rule: if retrieval score is too low, respond with “I don’t know” + suggested query reformulation.  
- Days 3–4: Add reranking (cross-encoder or lightweight reranker) and compare quality vs. baseline.  
- Day 5: Build a “RAG debug endpoint” that returns retrieved chunks, scores, and reranker decisions—this is a huge interview differentiator.  
- Day 6 deliverable: “RAG v1” service with citations and a debug UI.

**Week eight: evaluation harness for RAG**
This is where your suggested plan is directionally correct, but it should happen earlier, because evaluation is part of production reality. Databricks explicitly says you need an evaluation set, metric definitions, LLM judges, and an evaluation harness. citeturn15view1  
- Days 1–2: Create an evaluation dataset (50–150 Q/A pairs) derived from your own corpus.  
- Days 3–4: Implement offline evaluation runs: retrieval metrics (precision@k / nDCG if you can), answer faithfulness/groundedness checks, and latency/cost summaries.  
- Day 5: Integrate RAGAS-style metrics (or equivalent) and log results per configuration; Particula mentions RAGAS as an example evaluation framework. citeturn13view3turn19search1  
- Day 6 deliverable: **Portfolio Artifact 2** — “RAG v1 with evaluation harness,” plus a README section: “What we changed and why,” matching the portfolio-quality signal in your own Layer1 writing. citeturn9view4

#### Production backend features for AI systems

**Week nine: multi-tenancy and data boundaries**
Multi-tenant and data boundary thinking is a premium signal because RAG systems often contain sensitive company data. AWS guidance stresses security/privacy alignment in enterprise LLM deployments. citeturn16view1  
- Days 1–2: Add tenants/users tables and enforce tenant scoping at the query layer (retrieval must never cross tenants).  
- Days 3–4: Add per-tenant indexing: each tenant has separate document collections; retrieval filters enforce authorization.  
- Day 5: Add “data deletion” endpoint and test it (right-to-delete simulation).  
- Day 6 deliverable: multi-tenant RAG MVP with “cannot leak across tenants” test.

**Week ten: authentication, rate limiting, and prompt-injection guardrails**
This week exists because real job roles mention auth and rate limiting directly. citeturn13view1turn13view0  
- Days 1–2: Implement API key auth or JWT auth (choose one), and role-based access for admin vs. user.  
- Days 3–4: Add rate limiting + per-tenant budgets (requests/day, tokens/day, $/day).  
- Day 5: Add prompt injection defenses to the ingestion and RAG stages: sanitize instructions in retrieved text, restrict tool access, and add “refuse to follow document instructions.” Follow AWS prescriptive guardrail guidance as your baseline, keeping guardrails token-efficient. citeturn16view0turn16view2  
- Day 6 deliverable: security README with threat model + guardrail checklist + tests.

**Week eleven: observability and cost accounting**
This is explicitly demanded (observability) in NielsenIQ and Particula, and it’s central to evaluation/monitoring guidance. citeturn13view0turn13view3turn15view1  
- Days 1–2: Add structured logs with correlation IDs and a standard event schema (request start/end, retrieval, rerank, LLM call).  
- Days 3–4: Add tracing with OpenTelemetry (API request span → retrieval span → rerank span → LLM span). This is now common enough that there are vendor reference guides (Elastic, NVIDIA) showing RAG tracing and OTel use. citeturn19search26turn19search10turn15view1  
- Day 5: Create a basic dashboard (Grafana/Prometheus or Elastic or even a simplified internal dashboard) showing latency, cost, error rate, and “retrieval empty rate.”  
- Day 6 deliverable: “Observability pack” + screenshots in README.

**Week twelve: CI/CD, integration testing, and load testing**
NielsenIQ explicitly mentions CI/CD, unit testing, quality, and production support. citeturn13view0  
- Days 1–2: Expand `pytest` coverage: unit tests for chunking, embedding, retrieval filtering; integration tests that spin up docker-compose and hit endpoints.  
- Days 3–4: Add GitHub Actions pipeline: lint/type-check/test/build Docker image.  
- Day 5: Add basic load testing (Locust/k6) on `/ask` with a small eval set; log p95 latency and error rate.  
- Day 6 deliverable: **Portfolio Artifact 3** — “Productionized RAG service repo”: tests, CI/CD, docker-compose, metrics screenshots.

#### Agent workflows and tool integration

Agents matter in many roles, but the hiring signal is not “used 4 frameworks.” It is: you can reason about tool safety, state, evaluation, and reliability. citeturn13view0turn15view2turn16view2

**Week thirteen: build a tool-using agent without frameworks**
- Days 1–2: Implement a minimal agent loop (plan → tool call → observe → finalize). Tools: calculator, retrieval, and a safe “database query tool” that only allows approved read queries.  
- Days 3–4: Add tool audit logging: every tool call recorded with inputs/outputs and redactions.  
- Day 5: Add agent eval harness: task completion rate, tool call count, latency/cost. OpenAI’s Applied Evals role language shows this evaluation mindset is a real engineering specialization. citeturn15view2  
- Day 6 deliverable: small “Ops Agent” demo that answers with citations and uses safe tools.

**Week fourteen: LangGraph for stateful, testable workflows**
Your own curriculum emphasizes LangGraph and structured workflows, and LangChain’s ecosystem documentation shows MCP/A2A endpoints and deployment topics are now mature enough to integrate. citeturn2view0turn14view1  
- Days 1–2: Rebuild Week 13 agent using LangGraph state graphs (typed state, steps, failure routing).  
- Days 3–4: Add human-in-the-loop checkpoints for risky tool calls (approval step).  
- Day 5: Add retry/fallback policies (LLM fallback model or “no-tool mode” under outages).  
- Day 6 deliverable: “LangGraph agent v1” with workflow diagram in README.

**Week fifteen: MCP as a real integration capability**
This week exists because MCP is becoming a standard tool interface and the MCP roadmap explicitly focuses on enterprise readiness like audit trails and enterprise auth. citeturn14view0turn14view1  
- Days 1–2: Build a minimal MCP server that exposes 2–3 tools (retrieve documents, query DB with allowlist, compute).  
- Days 3–4: Connect your LangGraph agent to MCP tools and log which tool was discovered/used. (LangChain docs provide a concrete model: MCP endpoint at `/mcp`, plus auth considerations.) citeturn14view1  
- Day 5: Add “tool governance”: tool allowlist by tenant, tool scopes, and rate limits.  
- Day 6 deliverable: **Portfolio Artifact 4** — “Agent + MCP integration” with audit logs and simple screenshots.

**Week sixteen: specialization sprint (choose one)**
Pick exactly one track based on your target jobs and interests; keep it tight.
- Track A: **NL2SQL assistant** (RAG + DB + tool safety). This aligns with postings emphasizing enterprise RAG and database-backed workflows. citeturn13view1turn13view0  
- Track B: **Document intelligence** (PDF parsing + extraction + schema validation + human review loop).  
- Track C: **Fine-tuning decision + minimal LoRA/QLoRA** (optional). If you choose this, your output is not “I trained a big model”; it is a decision memo: fine-tune vs. RAG vs. prompt engineering, and a small LoRA demo if appropriate. Fine-tuning is often a plus, not a baseline requirement. citeturn13view0turn18view0  

Deliverable: a focused feature merged into your flagship project, plus a write-up that explains why you chose that specialization.

#### Deployment and operational excellence

**Week seventeen: production containerization and worker architecture**
This week exists because “Docker + CI/CD + background jobs” is repeatedly demanded. citeturn13view1turn13view3turn13view0  
- Days 1–2: Build production docker images (multi-stage, non-root, env vars).  
- Days 3–4: Add background jobs for ingestion and embedding generation (queue + worker).  
- Day 5: Add caching (Redis) for retrieval results and/or LLM responses.  
- Day 6 deliverable: full docker-compose “platform in a box”: API + worker + Postgres + Redis.

**Week eighteen: cloud deployment (choose one provider and go deep enough)**
Your suggested plan tries to cover AWS/GCP/Azure + serverless + k8s. That is too broad. Job postings typically want one: “experience building on AWS” or similar. citeturn13view3turn13view1  
- Days 1–2: Pick AWS *or* GCP (based on your target market).  
- Days 3–4: Deploy API + DB (managed) and configure secrets properly.  
- Day 5: Add basic deployment automation (CI deploy step or scripted deploy).  
- Day 6 deliverable: public demo endpoint (even if password-protected) + deployment docs.

**Week nineteen: operational monitoring and synthetic evaluation**
This week turns evals into an operational loop, matching Databricks’s “evaluation during development, monitoring in production” view. citeturn15view1  
- Days 1–2: Convert your evaluation dataset into a scheduled job (nightly synthetic tests).  
- Days 3–4: Add alerting thresholds (e.g., faithfulness drop, retrieval empty rate spike, cost spike).  
- Day 5: Add a rollback plan (config versioning for prompts/chunkers/retrievers).  
- Day 6 deliverable: “Ops runbook” that reads like real production documentation.

**Week twenty: performance and cost optimization week**
Many roles explicitly mention cost/latency control. citeturn13view1turn15view1turn13view3  
- Days 1–2: Benchmark latency and cost drivers (retrieval, rerank, LLM).  
- Days 3–4: Introduce model routing (cheap model for simple tasks; stronger for hard).  
- Day 5: Add context compression strategies and compare.  
- Day 6 deliverable: performance report with before/after graphs and real numbers.

**Week twenty-one: security hardening and abuse testing**
This week operationalizes AWS and research guidance: prompt injection is testable; defenses should be layered. citeturn16view0turn16view2turn16view1  
- Days 1–2: Build a prompt-injection test suite with “malicious docs in corpus.”  
- Days 3–4: Add defenses: instruction hierarchy, tool restrictions, content filters, response verification for high-risk actions.  
- Day 5: Add PII handling policy, log redaction, and a compliance-friendly audit log.  
- Day 6 deliverable: security section in README: threat model, mitigations, and test results.

#### Capstone, portfolio, and job readiness

**Week twenty-two: capstone selection and architecture**
Now you decide whether your flagship system *is* the capstone or whether you build a domain-focused layer on it. Your Layer1 extended plan emphasizes that domain specialization + iteration evidence boosts portfolio quality. citeturn9view4  
- Deliverables: a capstone spec (problem, target users, KPIs, eval measurements, threat model) + architecture diagram + milestones.

**Week twenty-three to week twenty-four: capstone build**
Two weeks, build-only. No new courses. Output must include:
- Multi-tenant or at least multi-collection safety
- Evaluation harness + a monitoring view
- Observability instrumentation
- Guardrails against prompt injection for your domain
- Deployment instructions and demo

These are exactly the “runs in production” qualities demanded in production-first postings. citeturn13view1turn13view0turn13view3turn15view1

**Week twenty-five: portfolio polish week**
- Rewrite READMEs of your top 3 repos into recruiter-friendly structure.
- Add screenshots, an architecture diagram, and a 2–3 minute demo video.
- Add a short “decision log” section: what you tried, what failed, what improved (your own curriculum documents emphasize that this signals real engineering). citeturn9view4

**Week twenty-six: interview readiness and applications**
This week is not generic LeetCode-only. It is AI system design + production debugging + explaining your work.
- Practice system design for RAG/agents: data flow, retrieval choices, evaluation loop, observability, cost, security.
- Practice one “build a mini-RAG in 45 minutes” interview simulation (your Layer1 materials already embrace time-boxed build-first practice). citeturn7view2turn7view0  
- Apply with tailored resumes and project links.

## What this modified plan changes from your suggested plan

It removes the long classic ML and deep learning blocks (regression/classification weeks, CNN/LSTM weeks) because they are not the most consistent hiring bottleneck for “AI Engineer building with models.” Instead, it makes retrieval engineering, evaluation/monitoring, backend ownership, and guardrails the center—aligned with job postings and authoritative guidance. citeturn13view0turn13view1turn15view1turn16view0

It also reduces “project count” and increases “project depth.” Rather than 20 shallow projects, you finish with **4–6 strong portfolio artifacts** that show end-to-end production thinking (tests, CI/CD, observability, security, evals, deployment). This matches the portfolio-quality criteria your own Layer1 extended plan highlights. citeturn9view4

Finally, it keeps your Python repo alive—but uses it correctly: as a diagnostic and targeted drills, not as a multi-week prerequisite gate. citeturn11view0turn12view0turn12view1

If you implement this exactly as written, you end the 26 weeks with the clearest market signal available in 2026: **a deployed, observable, evaluated, secured RAG/agent backend you can explain and defend—like a real engineer on a real team.** citeturn13view1turn13view0turn15view1turn16view1