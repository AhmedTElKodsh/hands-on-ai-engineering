# Checkpoint Rubrics — Layer 1 Final (28-Week AI Engineer Accelerator)

**Purpose:** Verify understanding before proceeding to next phase
**Philosophy:** Understanding > Completion | Explain to proceed

---

## 📋 HOW TO USE CHECKPOINT RUBRICS

### For Students:
1. At the end of each phase, review the checkpoint questions
2. Answer verbally (record yourself) or in writing **without looking at code**
3. Score yourself honestly using the rubric
4. If borderline/fail, review weak areas before proceeding

### For AI Assistants:
1. Ask checkpoint questions randomly (not in order)
2. Listen for understanding, not memorization
3. Score using the rubric below
4. Require re-do for scores < 2/5

### For Peers/Mentors:
1. Ask questions and listen for clarity
2. Challenge vague answers with "Can you be more specific?"
3. Score honestly — you're helping them by identifying gaps

---

## 🎯 SCORING RUBRIC (All Phases)

| Score | Level | Criteria | Action |
|-------|-------|----------|--------|
| **5/5** | Teaching Level | Can explain with analogies, answer unexpected questions, critique own decisions, propose improvements | Proceed confidently |
| **4/5** | Deep Understanding | Can explain in own words, answer "why" questions, identify trade-offs, explain alternatives | Proceed |
| **3/5** | Basic Understanding | Can explain conceptually, answer basic "what" questions, identify obvious trade-offs | Proceed but flag for review |
| **2/5** | Surface Understanding | Can repeat definitions, can't explain in own words, can't answer "why" questions | Review weak areas, retry in 2 days |
| **1/5** | Gap | Can't explain concepts, can't answer basic questions | Re-do phase projects with guidance |
| **0/5** | No Understanding | No meaningful responses | Re-do phase from start |

---

## PHASE 1: ENGINEERING FOUNDATIONS + LLM (Weeks 1-4)

### Checkpoint Questions (5 questions)

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | What's the difference between sync and async I/O? When does it matter? | - Sync: one operation at a time, blocks until complete<br>- Async: can start multiple operations, doesn't block<br>- Matters for: I/O-bound operations (API calls, DB queries, file operations)<br>- Example: LLM API calls benefit from async |
| **2** | Explain what an Alembic migration does and why you'd use it. | - Tracks database schema changes over time<br>- Allows rolling forward/backward between versions<br>- Enables team collaboration (everyone has same schema)<br>- Prevents manual SQL errors in production |
| **3** | What are tokens? Why do they matter for cost and context? | - Tokens are how LLMs count text (~1000 tokens = 750 words)<br>- Cost: you pay per input + output token<br>- Context: models have max token limits (e.g., 128K)<br>- Latency: more tokens = slower responses |
| **4** | Explain how cosine similarity works with embeddings in plain English. | - Embeddings are vectors representing text meaning<br>- Cosine similarity measures angle between vectors<br>- 1.0 = identical, 0 = unrelated, -1 = opposite<br>- Similar concepts have similar vectors (close in space) |
| **5** | When would you use pgvector vs. a dedicated vector DB like ChromaDB? | - pgvector: when you already use Postgres, want transactional + vector in one DB, simpler ops<br>- ChromaDB: when you need dedicated vector features, better scaling, simpler API<br>- Trade-off: simplicity vs. features, ops complexity vs. performance |

### Phase 1 Scoring

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Sync vs Async | | |
| Q2: Alembic Migrations | | |
| Q3: Tokens | | |
| Q4: Cosine Similarity | | |
| Q5: pgvector vs ChromaDB | | |

**Phase 1 Total:** _____ /5

**Phase 1 Status:**
- [ ] **4-5/5:** Proceed to Phase 2
- [ ] **2-3/5:** Review weak areas (see notes), retry in 2 days
- [ ] **0-1/5:** Re-do Phase 1 projects with guidance

**Weak Areas to Review:** _________________________________

**Retry Date (if needed):** ___________________

**Phase 1 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## PHASE 2: RAG ENGINEERING (Weeks 5-10)

### Checkpoint Questions (5 questions)

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | Walk me through the RAG pipeline step by step. | - User query → embedding generation<br>- Embedding → vector DB similarity search<br>- Top-K documents retrieved<br>- Documents + query → prompt assembly<br>- Prompt → LLM → answer with citations<br>- Bonus: mention reranking, caching |
| **2** | Why does chunk size matter? What's the trade-off? | - Small chunks: precise retrieval, less context, more chunks to manage<br>- Large chunks: more context, noisier retrieval, fewer chunks<br>- Trade-off: precision vs. context<br>- Sweet spot: 256-1024 tokens depending on content type |
| **3** | How do you prevent hallucinations in RAG? | - Ground answers in retrieved context (faithfulness)<br>- Add "I don't know" logic when retrieval confidence is low<br>- Show citations so users can verify<br>- Use LLM-as-judge to detect hallucinations post-generation |
| **4** | Explain reranking and why it improves retrieval quality. | - Initial retrieval: fast approximate search (dense vector)<br>- Reranking: slower, more accurate cross-encoder on top-K results<br>- Cross-encoder sees query + doc together (better relevance)<br>- Improves precision@K, especially for ambiguous queries |
| **5** | You have 500K documents, strict PII policy, p95 latency < 2s. What architecture do you pick and why? | - Vector DB: pgvector (PII stays in your Postgres, no external calls)<br>- Chunking: recursive (respects document structure)<br>- Retrieval: hybrid (BM25 + vector for recall)<br>- Reranking: Cohere rerank (quality) or skip for latency<br>- Caching: Redis for repeated queries<br>- PII: filter before embedding, redact in responses |

### Phase 2 Scoring

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: RAG Pipeline | | |
| Q2: Chunk Size Trade-offs | | |
| Q3: Hallucination Prevention | | |
| Q4: Reranking Why | | |
| Q5: System Design (500K docs) | | |

**Phase 2 Total:** _____ /5

**Phase 2 Status:**
- [ ] **4-5/5:** Proceed to Phase 3
- [ ] **2-3/5:** Review weak areas (see notes), retry in 2 days
- [ ] **0-1/5:** Re-do Phase 2 projects with guidance

**Weak Areas to Review:** _________________________________

**Retry Date (if needed):** ___________________

**Phase 2 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## PHASE 3: AI AGENTS (Weeks 11-16)

### Checkpoint Questions (5 questions)

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | Explain the ReAct loop (Observe-Think-Act). | - Observe: get current state/tool outputs<br>- Think: LLM reasons about what to do next<br>- Act: execute tool/function call<br>- Repeat until task complete or max iterations<br>- Example: Research task → search → read → synthesize → answer |
| **2** | Why do you need guardrails on agents? What could go wrong? | - Agents can take unintended actions without constraints<br>- Risks: infinite loops, expensive tool calls, data exfiltration, prompt injection via tools<br>- Guardrails: max iterations, budget limits, tool permissions, human approval for dangerous actions |
| **3** | How do you prevent infinite loops in agent execution? | - Max iteration limit (e.g., 10 steps)<br>- Detect repeated states/actions<br>- Timeout per task<br>- Exit condition: "task complete" or "cannot complete"<br>- Log every step for debugging |
| **4** | When would you use workflow (LangGraph) vs. autonomous agent? | - Workflow: predictable steps, compliance requirements, human handoff needed, debugging important<br>- Autonomous: exploratory tasks, open-ended problems, agent can self-correct<br>- Hybrid: workflow with agent nodes for flexible steps |
| **5** | What is MCP and why is it becoming table stakes? | - Model Context Protocol: standard for exposing tools to AI<br>- Like REST API but for AI tools<br>- Why table stakes: OpenAI adopted it, Assistants API sunsetting in 2026, 1000+ MCP servers exist<br>- Benefit: tools are discoverable, reusable, interoperable |

### Phase 3 Scoring

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: ReAct Loop | | |
| Q2: Guardrails Why | | |
| Q3: Infinite Loop Prevention | | |
| Q4: Workflow vs Autonomous | | |
| Q5: MCP What + Why | | |

**Phase 3 Total:** _____ /5

**Phase 3 Status:**
- [ ] **4-5/5:** Proceed to Phase 4
- [ ] **2-3/5:** Review weak areas (see notes), retry in 2 days
- [ ] **0-1/5:** Re-do Phase 3 projects with guidance

**Weak Areas to Review:** _________________________________

**Retry Date (if needed):** ___________________

**Phase 3 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## PHASE 4: PRODUCTION ENGINEERING (Weeks 17-22)

### Checkpoint Questions (5 questions)

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | What would you monitor in a production RAG system? | - Latency: p50, p95, p99 per endpoint<br>- Cost: tokens/day, cost/query, by model<br>- Quality: RAGAS scores over time, user feedback (thumbs up/down)<br>- Retrieval: empty rate, avg. distance, cache hit rate<br>- Errors: rate by type, correlation with deploys |
| **2** | How do you handle API failures in production? | - Retry with exponential backoff (for transient errors)<br>- Fallback: secondary provider or cheaper model<br>- Circuit breaker: stop calling if failure rate > threshold<br>- Queue + retry later for non-urgent tasks<br>- Alert on-call for sustained failures |
| **3** | What security concerns exist in LLM applications? | - Prompt injection: malicious instructions in retrieved docs<br>- Data exfiltration: agent tools leaking sensitive data<br>- PII leakage: embeddings or responses containing PII<br>- Jailbreaking: users bypassing system instructions<br>- Mitigation: input sanitization, output filtering, tool permissions, audit logs |
| **4** | How do you measure system quality beyond accuracy? | - Faithfulness: answers grounded in context<br>- Answer relevancy: addresses user query<br>- User satisfaction: thumbs up/down, session length<br>- Cost efficiency: cost per successful query<br>- Latency: p95 under SLA<br>- Coverage: % queries answered (vs. "I don't know") |
| **5** | Explain tenant isolation and why it matters. | - Each tenant's data must never leak to other tenants<br>- Implementation: tenant_id filter on every query, separate embeddings per tenant, auth checks at API layer<br>- Why: legal compliance (GDPR), customer trust, business requirement<br>- Test: query tenant A's data while authenticated as tenant B |

### Phase 4 Scoring

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Production Monitoring | | |
| Q2: API Failure Handling | | |
| Q3: Security Concerns | | |
| Q4: Quality Metrics | | |
| Q5: Tenant Isolation | | |

**Phase 4 Total:** _____ /5

**Phase 4 Status:**
- [ ] **4-5/5:** Proceed to Phase 5
- [ ] **2-3/5:** Review weak areas (see notes), retry in 2 days
- [ ] **0-1/5:** Re-do Phase 4 projects with guidance

**Weak Areas to Review:** _________________________________

**Retry Date (if needed):** ___________________

**Phase 4 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## PHASE 5: CAPSTONE + JOB READINESS (Weeks 23-28)

### Checkpoint Questions (5 questions)

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | Walk me through your Flagship #1 architecture. | - Clear component diagram (API, DB, vector store, LLM)<br>- Data flow: user query → retrieval → generation → response<br>- Key decisions: why this vector DB, this chunking strategy, this model<br>- Trade-offs acknowledged: what you sacrificed for what benefit |
| **2** | What was your biggest technical challenge and how did you overcome it? | - Specific challenge (not vague "everything was hard")<br>- Debugging process: how you identified root cause<br>- Solution: what you tried, what worked<br>- Lesson: what you'd do differently |
| **3** | How would you scale your RAG system to 10,000 queries/day? | - Caching: Redis for repeated queries<br>- Async processing: queue for ingestion, batch embeddings<br>- Model routing: cheap model for simple queries, expensive for complex<br>- Horizontal scaling: multiple API instances behind load balancer<br>- Database: connection pooling, read replicas |
| **4** | When would you fine-tune vs. use RAG vs. prompt engineering? | - Prompt engineering: first choice, fastest, cheapest, test first<br>- RAG: when you need model to access external knowledge, proprietary data<br>- Fine-tuning: when you need specific style/format, domain adaptation, RAG not enough<br>- Decision framework: try prompts → add RAG → consider fine-tuning |
| **5** | Explain a time you had to make a trade-off between quality and cost/latency. | - Specific example from projects<br>- Options considered<br>- Decision made and why<br>- How you measured impact<br>- What you'd do differently |

### Phase 5 Scoring

| Question | Score (0-1) | Notes |
|----------|-------------|-------|
| Q1: Flagship Architecture | | |
| Q2: Biggest Challenge | | |
| Q3: Scaling to 10K Queries | | |
| Q4: Fine-tune vs RAG vs Prompt | | |
| Q5: Trade-off Story | | |

**Phase 5 Total:** _____ /5

**Phase 5 Status:**
- [ ] **4-5/5:** Ready for job interviews
- [ ] **2-3/5:** Practice more mock interviews, review weak areas
- [ ] **0-1/5:** More project practice needed before interviewing

**Weak Areas to Review:** _________________________________

**Mock Interview Score (separate):** _____ /5

**Phase 5 Completed:** ⬜ Yes ⬜ No | **Date:** __________

---

## 📊 COMPREHENSIVE SKILL MATRIX

### Use this to track growth across all phases

| Skill Area | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Target |
|------------|---------|---------|---------|---------|---------|--------|
| Python/Async | | N/A | N/A | | | 4/5 |
| SQL/PostgreSQL | | | N/A | | | 4/5 |
| FastAPI | | N/A | N/A | | | 4/5 |
| LLM APIs | | | | N/A | | 4/5 |
| RAG Architecture | N/A | | | | | 5/5 |
| Vector Databases | N/A | | | | | 4/5 |
| Evaluation | N/A | | N/A | | | 4/5 |
| Agent Design | N/A | N/A | | | | 4/5 |
| LangGraph | N/A | N/A | | | | 4/5 |
| MCP | N/A | N/A | | | | 3/5 |
| Observability | N/A | N/A | N/A | | | 4/5 |
| Security | N/A | N/A | N/A | | | 4/5 |
| Cloud Deployment | N/A | N/A | N/A | | | 4/5 |
| System Design | | | | | | 4/5 |
| Communication | | | | | | 4/5 |

**Legend:**
- 5/5: Can teach others
- 4/5: Can implement independently
- 3/5: Can implement with guidance
- 2/5: Understands concepts, can't implement
- 1/5: Limited understanding
- N/A: Not assessed this phase

---

## 🎯 MOCK INTERVIEW RUBRIC (Phase 5)

### Use this for final readiness assessment

| Category | Score (1-5) | Notes |
|----------|-------------|-------|
| **Technical Depth** | | Can explain RAG/agents in detail |
| **System Design** | | Can design scalable architecture |
| **Problem Solving** | | Can debug unfamiliar issues |
| **Communication** | | Explains clearly, uses analogies |
| **Trade-off Thinking** | | Acknowledges pros/cons |
| **Production Mindset** | | Thinks about monitoring, failures |
| **Business Awareness** | | Considers cost, user impact |

**Mock Interview Total:** _____ /35

**Ready for Interviews:**
- [ ] **30-35/35:** Highly ready
- [ ] **25-29/35:** Ready with minor prep
- [ ] **20-24/35:** Need more practice
- [ ] **<20/35:** Not ready, more study needed

---

## 📝 CHECKPOINT SESSION TEMPLATE

### For AI Assistants/Peers conducting checkpoints

```
CHECKPOINT SESSION RECORD

Student: ___________________
Phase: _____
Date: ___________________

QUESTIONS ASKED:
Q1: _________________________________
   Response summary: _________________
   Score: ___/1

Q2: _________________________________
   Response summary: _________________
   Score: ___/1

Q3: _________________________________
   Response summary: _________________
   Score: ___/1

Q4: _________________________________
   Response summary: _________________
   Score: ___/1

Q5: _________________________________
   Response summary: _________________
   Score: ___/1

TOTAL SCORE: _____/5

FOLLOW-UP QUESTIONS ASKED:
1. _________________________________
2. _________________________________

STRENGTHS OBSERVED:
1. _________________________________
2. _________________________________

WEAK AREAS IDENTIFIED:
1. _________________________________
2. _________________________________

RECOMMENDATION:
⬜ Proceed to next phase
⬜ Review weak areas, retry in 2 days
⬜ Re-do phase projects with guidance

RETRY DATE (if applicable): ___________________

CONDUCTED BY: ___________________
```

---

**Remember:** Checkpoints are not about perfection. They're about ensuring you understand enough to succeed in the next phase.

**Honest self-assessment > False confidence**

**Last Updated:** ___________________
