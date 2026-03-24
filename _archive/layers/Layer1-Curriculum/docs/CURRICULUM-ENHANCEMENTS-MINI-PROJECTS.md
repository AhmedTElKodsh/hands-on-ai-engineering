# Curriculum Enhancement Guide: Mini-Project Coverage

**Purpose**: This document provides clear guidance on mini-project enhancements to ensure all concepts are thoroughly covered through hands-on practice.

**How to Use**: Insert the sections below into DAILY-CURRICULUM-PLAN-V4.md at the specified locations.

---

## Enhancement Type 1: Concept Coverage Tables

Add these tables to each day to make concept-to-practice mapping explicit.

### Day 1 Enhancement - Insert after "Tighten the Bolts" section

```markdown
### Concept Coverage Verification

| Concept Introduced                    | Practiced In            | Success Criteria                          |
| ------------------------------------- | ----------------------- | ----------------------------------------- |
| API authentication                    | First Wrench Turn       | Script runs without auth errors           |
| Message roles (system/user/assistant) | CLI chatbot feature #2  | Conversation maintains context            |
| System prompts                        | CLI chatbot feature #3  | Bot exhibits specified personality        |
| Streaming responses                   | CLI chatbot feature #4  | Tokens appear progressively               |
| Session state management              | Streamlit UI feature #5 | Chat history persists across interactions |
| Environment variable security         | Road Test item #6       | .env in .gitignore, no hardcoded keys     |

**Missing Coverage Check**: All concepts covered ✓
```

### Day 2 Enhancement - Insert after "Tighten the Bolts" section

```markdown
### Concept Coverage Verification

| Concept Introduced       | Practiced In      | Success Criteria                     |
| ------------------------ | ----------------- | ------------------------------------ |
| Zero-shot classification | Pattern #1 script | Classifies without examples          |
| Few-shot learning        | Pattern #2 script | Uses 3 examples to guide format      |
| Chain-of-thought         | Pattern #3 script | Shows reasoning steps                |
| System role engineering  | Pattern #4 script | Persona affects responses            |
| Structured JSON output   | Pattern #5 script | Valid JSON every time                |
| Temperature effects      | Pattern #6 script | Measurable difference 0.0 vs 1.0     |
| Token counting & cost    | Pattern #7 script | Accurate token count + cost estimate |
| Prompt chaining          | Pattern #8 script | Output 1 feeds into prompt 2         |
| Pydantic validation      | Road Test item #5 | LLM output validated with Pydantic   |

**Missing Coverage Check**: All concepts covered ✓

### Optional Deep Dive Extension

**Prompt Pattern Battle** (~1 hour)

- Take ONE complex task: "Extract all entities (people, places, organizations, dates) from a news article"
- Solve it using 4 different patterns: zero-shot, few-shot, chain-of-thought, structured output
- Document which pattern works best and why
- This reinforces: pattern selection is context-dependent
```

### Day 3 Enhancement - Insert after "Tighten the Bolts" section

```markdown
### Concept Coverage Verification

| Concept Introduced         | Practiced In      | Success Criteria                 |
| -------------------------- | ----------------- | -------------------------------- |
| Embedding generation       | First Wrench Turn | 10 embeddings created            |
| Cosine similarity (manual) | Embedding Lab #2  | Implemented from scratch         |
| L2 distance (manual)       | Embedding Lab #2  | Implemented from scratch         |
| Dot product (manual)       | Embedding Lab #2  | Implemented from scratch         |
| Distance metric comparison | Embedding Lab #3  | Rankings differ, documented      |
| Semantic vs keyword search | Embedding Lab #4  | 3+ cases where semantic wins     |
| Embedding visualization    | Embedding Lab #5  | 2D plot shows intuitive clusters |

**Missing Coverage Check**: All concepts covered ✓

### Optional Deep Dive Extension

**Distance Metric Edge Cases** (~45 min)

- Create 5 adversarial test cases:
  1. Very short text (3 words) vs long text (100 words)
  2. Identical meaning, different length ("car" vs "automobile vehicle")
  3. Same words, different order ("dog bites man" vs "man bites dog")
  4. Negation ("I love this" vs "I don't love this")
  5. Technical jargon vs plain language
- Test all 3 metrics on each case
- Document when each metric fails or succeeds
- This reinforces: no single metric is perfect
```

### Day 4 Enhancement - Insert after "Tighten the Bolts" section

```markdown
### Concept Coverage Verification

| Concept Introduced       | Practiced In         | Success Criteria                   |
| ------------------------ | -------------------- | ---------------------------------- |
| Document loading         | First Wrench Turn #1 | Text file loaded                   |
| Text chunking            | First Wrench Turn #2 | Split into chunks                  |
| Chunk embedding          | First Wrench Turn #3 | All chunks embedded                |
| Embedding storage        | First Wrench Turn #4 | Stored in Python list              |
| Query embedding          | First Wrench Turn #5 | Question embedded                  |
| Similarity search        | First Wrench Turn #5 | Top 3 chunks retrieved             |
| Context injection        | First Wrench Turn #6 | Chunks added to prompt             |
| Answer generation        | First Wrench Turn #7 | LLM generates answer               |
| Recursive text splitting | Better Chunking #1   | Tries paragraph → sentence → word  |
| Chunk overlap            | Better Chunking #2   | Last N chars = first N chars       |
| Chunk size experiments   | Better Chunking #3   | 200, 500, 1000 tested + documented |
| Top-k tuning             | Better Search        | top-1, top-3, top-10 compared      |
| Hallucination prevention | Better Prompt        | Refuses when no context            |
| Error handling           | Error Handling       | Empty docs + no-match handled      |

**Missing Coverage Check**: All concepts covered ✓

### Optional Deep Dive Extension

**RAG Failure Mode Analysis** (~1 hour)

- Deliberately break your RAG system 5 ways:
  1. Ask about content NOT in documents (hallucination test)
  2. Use chunks that are too small (context loss)
  3. Use chunks that are too large (noise)
  4. Ask ambiguous questions (retrieval confusion)
  5. Use documents with contradictory information
- Document what breaks and why
- Implement fixes for each failure mode
- This reinforces: RAG is fragile without proper guardrails
```

### Day 5 Enhancement - Insert after "Tighten the Bolts" section

```markdown
### Concept Coverage Verification

| Concept Introduced             | Practiced In         | Success Criteria            |
| ------------------------------ | -------------------- | --------------------------- |
| ChromaDB collection creation   | First Wrench Turn #1 | Collection created          |
| Embedding storage in vector DB | First Wrench Turn #2 | Day 4 chunks stored         |
| Vector similarity query        | First Wrench Turn #3 | Top-k retrieval works       |
| Result comparison              | First Wrench Turn #4 | Matches Day 4 manual search |
| Corpus creation (50+ docs)     | Semantic Search #1   | 50+ snippets in JSON        |
| Persistent storage             | Semantic Search #2   | ChromaDB persists to disk   |
| Streamlit query interface      | Semantic Search #3   | UI returns top-5 results    |
| Metadata storage & filtering   | Semantic Search #4   | Filter by category works    |
| Distance metric comparison     | Semantic Search #5   | cosine, l2, ip compared     |

**Missing Coverage Check**: All concepts covered ✓
```

### Day 6 Enhancement - Insert after "Tighten the Bolts" section

```markdown
### Concept Coverage Verification

| Concept Introduced         | Practiced In       | Success Criteria            |
| -------------------------- | ------------------ | --------------------------- |
| FastAPI endpoint creation  | First Wrench Turn  | POST /search works          |
| Health check endpoint      | First Wrench Turn  | GET /health returns 200     |
| Swagger UI auto-generation | First Wrench Turn  | /docs accessible            |
| Pydantic request models    | API Enhancement #1 | SearchRequest defined       |
| Pydantic response models   | API Enhancement #1 | SearchResponse defined      |
| HTTP error handling        | API Enhancement #2 | Empty query returns 400     |
| CORS middleware            | API Enhancement #3 | Frontend can call API       |
| Query parameters           | API Enhancement #4 | top_k parameter works       |
| Cost tracking              | API Enhancement #5 | Token cost logged           |
| Dockerfile creation        | Dockerize #1       | Dockerfile builds           |
| requirements.txt pinning   | Dockerize #2       | Versions pinned             |
| Docker build               | Dockerize #3       | Image builds successfully   |
| Docker run with env vars   | Dockerize #4       | Container runs with API key |
| Container networking       | Dockerize #5       | API accessible from host    |

**Missing Coverage Check**: All concepts covered ✓
```

### Days 7-8 Enhancement - Insert after "Road Test Checklist"

```markdown
### Concept Coverage Verification (Both Days)

| Concept Introduced             | Practiced In          | Success Criteria          |
| ------------------------------ | --------------------- | ------------------------- |
| PyPDFLoader                    | Day 7 First Wrench #1 | PDF loaded                |
| RecursiveCharacterTextSplitter | Day 7 First Wrench #2 | Chunks created            |
| OpenAIEmbeddings               | Day 7 First Wrench #3 | Chunks embedded           |
| Chroma vectorstore             | Day 7 First Wrench #4 | Stored in ChromaDB        |
| RetrievalQA chain              | Day 7 First Wrench #5 | Query works               |
| Text splitter comparison       | Day 7 Tighten Bolts   | 3 splitters tested        |
| Similarity vs MMR search       | Day 7 Tighten Bolts   | Both types compared       |
| Source document return         | Day 7 Tighten Bolts   | Chunks shown with answers |
| Multi-format loading           | Day 8 Build #1        | PDFs + text + web loaded  |
| Metadata storage               | Day 8 Build #2        | Source + page stored      |
| Cross-document search          | Day 8 Build #3        | Searches all docs         |
| Source attribution             | Day 8 Build #4        | Shows doc + page          |
| Streamlit chat interface       | Day 8 Build #5        | Multi-turn conversation   |

**Missing Coverage Check**: All concepts covered ✓
```

### Days 9-10 Enhancement - Insert after "Prime the Pump" section

```markdown
### Concept Coverage Verification (Both Days)

| Concept Introduced         | Practiced In      | Success Criteria             |
| -------------------------- | ----------------- | ---------------------------- |
| Context Relevance metric   | Day 9 Manual Eval | 15 questions rated           |
| Groundedness metric        | Day 9 Manual Eval | Hallucinations identified    |
| Answer Relevance metric    | Day 9 Manual Eval | Off-topic answers caught     |
| RAGAS installation         | Day 9 RAGAS Setup | Library installed            |
| RAGAS evaluation run       | Day 9 RAGAS Setup | Scores generated             |
| Metric interpretation      | Day 9 RAGAS Setup | Weakest dimension identified |
| Chunk size experiments     | Day 10 Chunking   | 3+ sizes tested              |
| Overlap experiments        | Day 10 Chunking   | 3+ overlaps tested           |
| Retrieval k experiments    | Day 10 Chunking   | top-1, 3, 5, 10 tested       |
| Systematic comparison      | Day 10 Chunking   | Results in comparison table  |
| Improvement implementation | Day 10 Chunking   | Best config applied          |

**Missing Coverage Check**: All concepts covered ✓

### Optional Deep Dive Extension

**RAGAS Metric Deep Dive** (~2 hours)

- For each of the 3 metrics, create 5 test cases that SHOULD fail:
  - Context Relevance: irrelevant chunks retrieved
  - Groundedness: answer contains info not in context
  - Answer Relevance: answer doesn't address the question
- Verify RAGAS catches all 15 failures
- Fix your RAG system to pass all tests
- This reinforces: evaluation metrics have specific failure modes
```

---

## Enhancement Type 2: Phase Integration Tasks

Add these integration checkpoints at the end of each phase to reinforce cross-day learning.

### Integration Task 1 - Insert after Day 10

```markdown
---

## PHASE 1 INTEGRATION CHECKPOINT
**Integration Task | ~3 hours | Difficulty: ⭐⭐⭐**

### The Challenge
Build a complete RAG system FROM MEMORY without referring to previous days' code. This tests whether you truly understand the concepts or just copied code.

### Requirements
1. **Document Q&A System** with these features:
   - Load 3+ documents (any format)
   - Chunk with overlap
   - Store in ChromaDB with metadata
   - FastAPI endpoint: POST /ask
   - Dockerized
   - RAGAS evaluation showing all 3 metrics > 0.7

2. **Constraints**:
   - No looking at previous code
   - No copy-paste from tutorials
   - Must complete in 3 hours
   - Must run without errors

3. **Success Criteria**:
   - [ ] Answers 10 test questions correctly
   - [ ] RAGAS scores: Context Relevance > 0.7, Groundedness > 0.7, Answer Relevance > 0.7
   - [ ] Docker container runs on first try
   - [ ] API responds in < 2 seconds
   - [ ] No hardcoded API keys

### Why This Matters
If you can't build this from memory, you don't understand the fundamentals. Go back and rebuild Days 3-10 until you can.

### Reflection Questions
- What did you forget? (That's what you need to review)
- What was easier than expected? (That's what you mastered)
- What would you do differently? (That's your learning edge)

---
```

### Integration Task 2 - Insert after Day 17

```markdown
---

## PHASE 2 INTEGRATION CHECKPOINT
**Integration Task | ~4 hours | Difficulty: ⭐⭐⭐⭐**

### The Challenge
Take your Phase 1 integration system and add production-grade features:

### Requirements
1. **Add Agent Capabilities**:
   - ReAct agent that can search documents OR call external APIs
   - LangGraph state management
   - Tool use with at least 3 tools

2. **Add Production Features**:
   - Prompt injection detection
   - Cost tracking per request
   - Response time monitoring
   - Error logging
   - CI/CD pipeline (GitHub Actions)

3. **Success Criteria**:
   - [ ] Agent correctly routes between tools
   - [ ] Blocks at least 3 types of prompt injection
   - [ ] Logs show cost per request
   - [ ] CI/CD runs tests on every commit
   - [ ] System handles 10 concurrent requests

### Why This Matters
This is the difference between a demo and a production system. Hiring managers look for production thinking.

---
```

### Integration Task 3 - Insert after Day 23

```markdown
---

## PHASE 3 INTEGRATION CHECKPOINT
**Integration Task | ~4 hours | Difficulty: ⭐⭐⭐⭐**

### The Challenge
Deploy your Phase 2 system to the cloud with monitoring and fine-tuning.

### Requirements
1. **Cloud Deployment**:
   - Deploy to Railway/Render/Fly.io
   - Live URL accessible
   - Environment variables configured
   - Health check endpoint

2. **Monitoring**:
   - Track: latency, cost, error rate, user queries
   - Alert on: errors > 5%, latency > 3s, cost > $1/hour
   - Dashboard showing last 24 hours

3. **Fine-Tuning**:
   - Fine-tune gpt-4o-mini on 50+ domain-specific examples
   - A/B test: base model vs fine-tuned
   - Document: accuracy improvement, cost change, latency change

4. **Success Criteria**:
   - [ ] Live URL works from any device
   - [ ] Monitoring dashboard shows real data
   - [ ] Fine-tuned model shows measurable improvement
   - [ ] System costs < $0.10 per 100 queries

### Why This Matters
This is your portfolio piece. This is what you show in interviews.

---
```

---

## Enhancement Type 3: Concept Reinforcement for Multi-Day Projects

### Days 11-13 Enhancement - Insert after Day 13 "Road Test Checklist"

```markdown
### Concept Coverage Verification (Days 11-13)

| Concept Introduced     | Practiced In | Success Criteria                      |
| ---------------------- | ------------ | ------------------------------------- |
| ReAct pattern          | Day 11       | Thought-Action-Observation loop works |
| Tool definition        | Day 11       | 3+ tools defined                      |
| Tool execution         | Day 11       | Tools called correctly                |
| Stopping condition     | Day 11       | Agent stops when done                 |
| LangGraph nodes        | Day 12       | 3+ nodes defined                      |
| LangGraph edges        | Day 12       | Routing works                         |
| State management       | Day 12       | State persists across nodes           |
| Conditional routing    | Day 12       | Decisions based on state              |
| Graph visualization    | Day 12       | Mermaid diagram generated             |
| Corrective RAG         | Day 13       | Bad retrievals trigger web search     |
| Self-correction        | Day 13       | Agent fixes own mistakes              |
| Multi-source retrieval | Day 13       | Vector DB + web search                |

**Missing Coverage Check**: All concepts covered ✓

### Integration Mini-Task

**Agent Stress Test** (~1 hour)

- Give your Day 13 agent 10 adversarial queries:
  1. Question with no answer in docs (should trigger web search)
  2. Question requiring multi-step reasoning
  3. Question with contradictory info in docs
  4. Question requiring external API call
  5. Ambiguous question needing clarification
  6. Question with prompt injection attempt
  7. Question requiring math calculation
  8. Question about very recent events (not in docs)
  9. Question requiring comparison across sources
  10. Question with typos and grammar errors
- Document: which queries succeed, which fail, why
- This reinforces: agents need robust error handling
```

### Days 18-19 Enhancement - Insert after Day 19 "Road Test Checklist"

```markdown
### Concept Coverage Verification (Days 18-19)

| Concept Introduced           | Practiced In | Success Criteria                  |
| ---------------------------- | ------------ | --------------------------------- |
| BM25 keyword search          | Day 18       | Implemented                       |
| Dense vector search          | Day 18       | Already working from Phase 1      |
| Hybrid fusion (RRF)          | Day 18       | BM25 + dense combined             |
| Hybrid evaluation            | Day 18       | Beats pure semantic on 10 queries |
| Cross-encoder reranking      | Day 19       | Top-20 reranked to top-5          |
| Query rewriting              | Day 19       | Ambiguous queries clarified       |
| Query decomposition          | Day 19       | Complex queries split             |
| HyDE (Hypothetical Document) | Day 19       | Generates ideal answer first      |
| Multi-query generation       | Day 19       | 1 query → 3 variations            |

**Missing Coverage Check**: All concepts covered ✓

### Integration Mini-Task

**Search Quality Showdown** (~1.5 hours)

- Create 20 test queries across 4 categories:
  1. Exact match (keyword should win)
  2. Semantic match (dense should win)
  3. Hybrid match (fusion should win)
  4. Ambiguous (query rewriting should help)
- Test 5 configurations:
  1. Pure BM25
  2. Pure dense
  3. Hybrid (no reranking)
  4. Hybrid + reranking
  5. Hybrid + reranking + query rewriting
- Document: which config wins each category
- This reinforces: no single search method is best for everything
```

### Days 20-21 Enhancement - Insert after Day 21 "Road Test Checklist"

```markdown
### Concept Coverage Verification (Days 20-21)

| Concept Introduced       | Practiced In | Success Criteria              |
| ------------------------ | ------------ | ----------------------------- |
| Multi-agent architecture | Day 20       | 3 agents defined              |
| Agent specialization     | Day 20       | Each agent has specific role  |
| Agent coordination       | Day 20       | Planner routes to specialists |
| Conditional loops        | Day 20       | Researcher loops per subtopic |
| Quality gates            | Day 20       | Reviewer can reject and retry |
| Max iteration limits     | Day 20       | Prevents infinite loops       |
| LangSmith tracing        | Day 21       | Traces visible in dashboard   |
| MCP tool integration     | Day 21       | External tools callable       |
| Agent observability      | Day 21       | Can debug agent decisions     |

**Missing Coverage Check**: All concepts covered ✓

### Integration Mini-Task

**Multi-Agent Failure Analysis** (~1 hour)

- Deliberately break your multi-agent system 5 ways:
  1. Planner routes to wrong agent
  2. Researcher returns irrelevant info
  3. Writer produces low-quality output
  4. Reviewer rejects everything (infinite loop)
  5. One agent crashes mid-execution
- For each failure:
  - Document what broke
  - Implement a fix
  - Verify fix with test case
- This reinforces: multi-agent systems need robust error handling and circuit breakers
```

---

## Summary: What to Add Where

### Quick Reference Table

| Location                             | Enhancement Type       | Time to Add | Impact                         |
| ------------------------------------ | ---------------------- | ----------- | ------------------------------ |
| After each day's "Tighten the Bolts" | Concept Coverage Table | 5 min       | High - makes gaps visible      |
| Days 2, 3, 4, 9-10                   | Optional Deep Dive     | 10 min      | Medium - for advanced learners |
| After Day 10                         | Phase 1 Integration    | 15 min      | Critical - tests understanding |
| After Day 17                         | Phase 2 Integration    | 15 min      | Critical - production thinking |
| After Day 23                         | Phase 3 Integration    | 15 min      | Critical - portfolio piece     |
| After Days 11-13, 18-19, 20-21       | Integration Mini-Tasks | 10 min each | High - stress tests concepts   |

### Total Time to Implement All Enhancements

- Concept Coverage Tables: ~2 hours (40 days × 3 min average)
- Optional Deep Dives: ~1 hour (6 deep dives × 10 min)
- Integration Tasks: ~1 hour (3 major + 3 mini × 12 min)
- **Total: ~4 hours of curriculum enhancement work**

### Expected Student Impact

- **Concept Coverage Tables**: Students can self-verify they've practiced everything
- **Optional Deep Dives**: Advanced students stay challenged
- **Integration Tasks**: Forces synthesis, reveals gaps, builds confidence
- **Overall**: Completion rate should increase 15-25% due to clearer expectations

---

## Implementation Priority

If time is limited, implement in this order:

1. **Phase Integration Tasks** (Days 10, 17, 23) - Highest impact
2. **Concept Coverage Tables** (Days 1-10) - Foundation phase is critical
3. **Integration Mini-Tasks** (Days 11-13, 18-19, 20-21) - Reinforces advanced concepts
4. **Optional Deep Dives** - Nice to have for advanced learners
5. **Concept Coverage Tables** (Days 11-40) - Lower priority, concepts already complex

---

## Notes for Curriculum Maintainers

- All enhancements follow the existing "Mechanic's Workflow" pedagogy
- Tables use markdown for easy copy-paste
- Integration tasks are time-boxed to prevent scope creep
- Success criteria are measurable and objective
- Extensions are clearly marked as optional
- All additions maintain the "build first, understand after" philosophy
