# Week-by-Week Roadmap - Pragmatic GenAI Engineer Curriculum

**Total Duration:** 32 weeks (28 core + 4 flex)  
**Time Commitment:** 20 hours/week (4 hours/day × 5 days)  
**Target:** AI/GenAI Engineer role with portfolio-ready projects

---

## Phase 0: Python Foundations (Weeks 1-2)

### Week 1: Python Essentials
**Goal:** Enough Python to not get stuck on syntax

**Monday-Wednesday: Core Python**
- Variables, types, strings, lists, dicts
- Control flow (if/elif/else, loops)
- Functions, scope, lambda
- **Resource:** Python Daily Practice Days 1-6
- **Ship:** 5 working functions with passing tests

**Thursday-Friday: Python for AI**
- Error handling (try/except, custom exceptions)
- File I/O (read/write, context managers)
- Basic pytest
- **Ship:** File processor with error handling + tests

**Learning Checkpoints:**
- [ ] Can write a function with type hints
- [ ] Can handle errors gracefully
- [ ] Can write and run pytest tests
- [ ] Can read/write files safely

**Flex:** If Python is easy, skip to Week 2. If struggling, repeat exercises.

---

### Week 2: Python for AI Apps
**Goal:** Master tools you'll use constantly in AI engineering

**Monday-Tuesday: Pydantic + Type Hints**
- Pydantic BaseModel basics
- Field validation and defaults
- Type hints for functions and classes
- **Ship:** Config loader with Pydantic validation

**Wednesday-Thursday: Async/Await**
- Why async matters for LLM APIs
- async/await syntax
- asyncio.gather for concurrent calls
- **Ship:** Async API client (mock API is fine)

**Friday: Environment + Context Managers**
- .env files and python-dotenv
- Context managers (with statement)
- Environment variable validation
- **Ship:** Secure config system with .env

**Learning Checkpoints:**
- [ ] Can create Pydantic models with validation
- [ ] Can write async functions
- [ ] Can use context managers
- [ ] Can load and validate environment variables

**Resources:**
- Pydantic docs: https://docs.pydantic.dev
- Real Python async tutorial
- Python Daily Practice Week 2

---

## Phase 1: LLM Foundations (Weeks 3-6)

### Week 3: First LLM Call
**Goal:** Working LLM app in production by Week 6

**Monday: Setup + First Call**
- OpenAI API setup
- First completion (5 lines of code)
- Understanding messages format
- **Ship:** Script that talks to GPT

**Tuesday: Structured Outputs**
- JSON mode
- Pydantic models for responses
- Prompt templates
- **Ship:** CLI tool with structured JSON output

**Wednesday: Retry Logic + Error Handling**
- Rate limits and timeouts
- Exponential backoff
- Error logging
- **Ship:** Robust LLM client

**Thursday: Streaming Responses**
- Why streaming matters
- Implementing streaming
- Token-by-token display
- **Ship:** Streaming chatbot

**Friday: Debug Lab**
- Fix broken prompts
- Handle edge cases
- Test with various inputs

**Learning Checkpoints:**
- [ ] Can make LLM API calls
- [ ] Can parse structured outputs
- [ ] Can handle errors and retries
- [ ] Can implement streaming

**Mini-Project:** CLI chatbot with conversation history

---

### Week 4: Multi-Provider Client
**Goal:** Production-grade LLM client with fallbacks

**Monday-Tuesday: Provider Abstraction**
- Add Anthropic/Groq support
- Provider interface design
- Fallback logic
- **Starter Code:** `mini-projects/llm-client/`

**Wednesday: Token Counting + Cost Tracking**
- Token counting per request
- Cost calculation
- Usage logging
- **Ship:** Client with cost tracking

**Thursday: Testing**
- Mocking API calls
- Unit tests for fallback logic
- Integration tests
- **Ship:** Test suite with 80%+ coverage

**Friday: Debug Lab + Documentation**
- Fix failing tests
- Write README
- Record demo

**Learning Checkpoints:**
- [ ] Can explain fallback strategy
- [ ] Can calculate costs accurately
- [ ] Can test external APIs
- [ ] Can document API design

**Deliverable:** Multi-provider LLM client (Mini-Project 1)

---

### Week 5: FastAPI Service
**Goal:** Wrap LLM client in production API

**Monday-Tuesday: FastAPI Basics**
- Request/response models
- Endpoints and routing
- Pydantic integration
- **Ship:** Hello World API

**Wednesday: Add LLM Endpoint**
- Integrate Week 4 client
- Async endpoints
- Error responses
- **Ship:** LLM API service

**Thursday: Production Concerns**
- Structured logging (JSON)
- Health checks
- CORS configuration
- **Ship:** Production-ready API

**Friday: Testing + Deployment**
- API testing with pytest
- Test with curl/Postman
- Run locally with uvicorn

**Learning Checkpoints:**
- [ ] Can build FastAPI endpoints
- [ ] Can integrate async LLM calls
- [ ] Can add logging and health checks
- [ ] Can test APIs

**Deliverable:** LLM API running locally

---

### Week 6: Docker + Deploy
**Goal:** First deployed system (Flagship 0.5)

**Monday-Tuesday: Docker**
- Dockerfile for Python app
- docker-compose setup
- Environment variables in Docker
- **Ship:** Containerized API

**Wednesday: Deploy**
- Choose platform (Render/Railway/Fly.io)
- Deploy container
- Configure environment
- **Ship:** Live URL

**Thursday: Monitoring**
- Log aggregation
- Uptime monitoring
- Basic alerting
- **Ship:** Monitored service

**Friday: Demo Day**
- Test deployed API
- Show someone your work
- Write blog post draft

**Learning Checkpoints:**
- [ ] Can containerize Python apps
- [ ] Can deploy to cloud platform
- [ ] Can monitor production service
- [ ] Can demo your work

**Deliverable:** 🎯 **FLAGSHIP 0.5** - Deployed LLM API

---

## Phase 2: RAG Core (Weeks 7-12)

### Week 7: Embeddings + Vector Store
**Goal:** Understand semantic search fundamentals

**Monday-Tuesday: Embeddings**
- What are embeddings?
- Sentence transformers
- Embedding generation
- **Ship:** Embedding generator

**Wednesday: Vector Store Setup**
- Chroma installation
- Collection creation
- Document ingestion
- **Ship:** 50+ documents indexed

**Thursday: Similarity Search**
- Query embeddings
- Distance metrics (cosine, euclidean)
- Top-k retrieval
- **Ship:** Search interface

**Friday: Experiments**
- Test different embedding models
- Compare retrieval quality
- Document findings

**Learning Checkpoints:**
- [ ] Can explain what embeddings are
- [ ] Can generate embeddings
- [ ] Can use vector database
- [ ] Can perform similarity search

**Deliverable:** Document search system

---

### Week 8: First RAG System
**Goal:** Retrieval + Generation working end-to-end

**Monday-Tuesday: RAG Pipeline**
- Retrieve relevant docs
- Build context prompt
- Generate answer
- **Ship:** Basic RAG

**Wednesday: Citation Tracking**
- Source metadata
- Citation formatting
- Linking answers to sources
- **Ship:** RAG with citations

**Thursday: "I Don't Know" Handling**
- Confidence thresholds
- Refusal logic
- Fallback responses
- **Ship:** RAG with refusal

**Friday: Debug Lab**
- Test edge cases
- Fix retrieval failures
- Improve prompts

**Learning Checkpoints:**
- [ ] Can explain RAG pipeline
- [ ] Can track citations
- [ ] Can handle low-confidence queries
- [ ] Can debug retrieval issues

**Deliverable:** RAG assistant with citations

---

### Week 9: Chunking Strategies
**Goal:** Optimize document ingestion

**Monday-Tuesday: Chunking Approaches**
- Fixed-size chunking
- Recursive chunking
- Semantic chunking
- **Starter Code:** `mini-projects/document-indexer/`

**Wednesday: Metadata Design**
- Document type, date, section
- Filtering strategies
- Metadata in retrieval
- **Ship:** Indexer with metadata

**Thursday: Re-index + Compare**
- Re-index with better chunking
- Compare retrieval quality
- Document differences
- **Ship:** Improved pipeline

**Friday: Optimization**
- Batch processing
- Caching embeddings
- Performance profiling

**Learning Checkpoints:**
- [ ] Can explain chunking trade-offs
- [ ] Can design metadata schema
- [ ] Can compare strategies empirically
- [ ] Can optimize ingestion

**Deliverable:** Document indexer (Mini-Project 2)

---

### Week 10: Retrieval Quality
**Goal:** Advanced retrieval techniques

**Monday: Multi-Query Retrieval**
- Generate multiple queries
- Aggregate results
- Deduplication
- **Ship:** Multi-query RAG

**Tuesday: Reranking**
- Cross-encoder reranking
- Cohere rerank API
- Score-based filtering
- **Ship:** RAG with reranking

**Wednesday: Hybrid Search**
- Dense + sparse (BM25)
- Score fusion
- When to use hybrid
- **Ship:** Hybrid RAG

**Thursday: Query Rewriting**
- Clarification
- Expansion
- Simplification
- **Ship:** RAG with query rewriting

**Friday: Measure Improvements**
- Before/after comparison
- Document which helped most
- Cost/quality trade-offs

**Learning Checkpoints:**
- [ ] Can implement multi-query retrieval
- [ ] Can add reranking
- [ ] Can combine dense + sparse search
- [ ] Can measure improvements

**Deliverable:** RAG v2 with documented improvements

---

### Week 11: Evaluation Harness
**Goal:** Measure RAG quality systematically

**Monday-Tuesday: Golden Dataset**
- Create 20 Q&A pairs
- Include edge cases
- Document expected behavior
- **Starter Code:** `mini-projects/rag-evaluator/`

**Wednesday: Retrieval Metrics**
- Precision@K
- Mean Reciprocal Rank (MRR)
- Recall
- **Ship:** Retrieval evaluator

**Thursday: Generation Metrics**
- Faithfulness (LLM-as-judge)
- Relevance scoring
- Citation accuracy
- **Ship:** Generation evaluator

**Friday: Full Evaluation**
- Run eval suite
- Document failures
- Prioritize improvements

**Learning Checkpoints:**
- [ ] Can create golden datasets
- [ ] Can calculate retrieval metrics
- [ ] Can evaluate generation quality
- [ ] Can identify failure patterns

**Deliverable:** RAG evaluation harness (Mini-Project 3)

---

### Week 12: Flagship 1 - Production RAG
**Goal:** Portfolio-ready RAG system

**Phase 1: Architecture Design (Mon-Tue)**
- Choose domain (legal, technical, research)
- Write 10 example queries
- Draw architecture diagram
- List 5 failure modes

**Phase 2: Core Implementation (Wed-Thu)**
- Integrate all RAG components
- Add evaluation harness
- Implement error handling
- **Ship:** Working RAG system

**Phase 3: Production Hardening (Fri + Weekend)**
- Add to FastAPI
- Docker + deploy
- Logging + monitoring
- Security basics

**Phase 4: Documentation (Next Mon)**
- README with architecture
- Design decisions doc
- Evaluation report
- Demo video (3-5 min)

**Learning Checkpoints:**
- [ ] Can design RAG architecture
- [ ] Can integrate multiple components
- [ ] Can deploy production system
- [ ] Can document decisions

**Deliverable:** 🎯 **FLAGSHIP 1** - Production RAG System

---

### FLEX WEEK 13: Catch Up / Explore
**Use this week to:**
- Polish Flagship 1
- Catch up on incomplete weeks
- Deep-dive into confusing concepts
- Explore advanced RAG patterns
- Write blog post about Flagship 1
- Take a break if needed

---

## Phase 3: Agents + Workflows (Weeks 14-20)

### Week 14: LangChain Basics
**Goal:** Understand LangChain patterns

**Monday-Tuesday: Chains + LCEL**
- LangChain Expression Language
- Chain composition
- Parallel execution
- **Ship:** Multi-step chain

**Wednesday: Memory**
- Conversation buffer
- Summary memory
- Vector store memory
- **Ship:** Conversational RAG

**Thursday: Callbacks**
- Token tracking
- Logging callbacks
- Custom callbacks
- **Ship:** Instrumented chain

**Friday: Debug Lab**
- Chain debugging
- Error handling
- Performance profiling

**Learning Checkpoints:**
- [ ] Can build LangChain chains
- [ ] Can add conversation memory
- [ ] Can use callbacks for observability
- [ ] Can debug chain failures

**Deliverable:** Conversational RAG with memory

---

### Week 15: Tool Calling
**Goal:** LLMs that can use tools

**Monday-Tuesday: Function Calling Basics**
- OpenAI function calling
- Tool schemas
- Tool execution
- **Ship:** LLM with 1 tool

**Wednesday: Multiple Tools**
- Build 3 tools (calculator, search, database)
- Tool selection logic
- Error handling per tool
- **Ship:** LLM with 3+ tools

**Thursday: Tool Validation**
- Input validation
- Output validation
- Safety checks
- **Ship:** Safe tool system

**Friday: Testing**
- Mock tools for testing
- Test tool selection
- Test error cases

**Learning Checkpoints:**
- [ ] Can implement function calling
- [ ] Can build custom tools
- [ ] Can validate tool inputs/outputs
- [ ] Can test tool systems

**Deliverable:** LLM with validated tools

---

### Week 16: ReAct Agent
**Goal:** Reasoning + Acting pattern

**Monday-Tuesday: ReAct Pattern**
- Understand ReAct loop
- Implement simple agent
- Observation → Thought → Action
- **Ship:** Basic ReAct agent

**Wednesday: Guardrails**
- Max iterations
- Timeouts
- Stuck detection
- **Ship:** Bounded agent

**Thursday: Observability**
- Log every step
- Trace reasoning
- Cost tracking
- **Ship:** Instrumented agent

**Friday: Debug Lab**
- Fix infinite loops
- Handle tool failures
- Improve reasoning

**Learning Checkpoints:**
- [ ] Can explain ReAct pattern
- [ ] Can implement agent loop
- [ ] Can add guardrails
- [ ] Can trace agent decisions

**Deliverable:** Bounded ReAct agent

---

### Week 17: LangGraph Workflows
**Goal:** State machines for complex workflows

**Monday-Tuesday: State Graphs**
- Nodes and edges
- State management
- Conditional routing
- **Ship:** Simple workflow

**Wednesday: Human-in-the-Loop**
- Approval checkpoints
- State inspection
- Resume from checkpoint
- **Ship:** Workflow with approval

**Thursday: Error Handling**
- Retry nodes
- Fallback paths
- State rollback
- **Ship:** Robust workflow

**Friday: Visualization**
- Graph visualization
- Execution traces
- Debug tools

**Learning Checkpoints:**
- [ ] Can build state graphs
- [ ] Can add human checkpoints
- [ ] Can handle errors in workflows
- [ ] Can visualize execution

**Deliverable:** Multi-step workflow with approval

---

### Weeks 18-19: Flagship 2 - Agentic Workflow
**Goal:** Controlled agentic system

**Week 18: Design + Build**
- Choose use case (research/analysis/content)
- Design state machine
- Implement tools
- Build workflow
- **Ship:** Working agentic system

**Week 19: Harden + Document**
- Add evaluation
- Add observability
- Security testing
- Documentation + demo
- **Ship:** 🎯 **FLAGSHIP 2**

**Learning Checkpoints:**
- [ ] Can design agentic workflows
- [ ] Can implement state management
- [ ] Can add human oversight
- [ ] Can evaluate agent decisions

**Deliverable:** 🎯 **FLAGSHIP 2** - Controlled Agentic Workflow

---

### FLEX WEEK 20: Catch Up / Explore
**Use this week to:**
- Polish Flagship 2
- Explore multi-agent systems
- Deep-dive into agent patterns
- Write blog post
- Rest

---

## Phase 4: Production Engineering (Weeks 21-26)

### Week 21: Testing AI Systems
**Monday-Tuesday: Property-Based Testing**
- Hypothesis library
- Properties for LLM outputs
- Generative testing
- **Ship:** Property tests

**Wednesday: Adversarial Testing**
- Prompt injection tests
- Jailbreak attempts
- Edge case generation
- **Ship:** Security test suite

**Thursday-Friday: Regression Testing**
- Golden dataset tests
- Performance regression
- Cost regression
- **Ship:** Full test suite

---

### Week 22: Observability
**Monday-Tuesday: LangSmith / Phoenix**
- Setup observability platform
- Distributed tracing
- Trace visualization
- **Ship:** Traced applications

**Wednesday-Thursday: Metrics + Analytics**
- Token usage tracking
- Cost analytics
- Latency monitoring
- **Ship:** Metrics dashboard

**Friday: Alerting**
- Error rate alerts
- Cost alerts
- Latency alerts

---

### Week 23: Security + Guardrails
**Monday: Prompt Injection Defense**
- Detection techniques
- Input sanitization
- Prompt boundaries
- **Ship:** Hardened prompts

**Tuesday: Input Validation**
- Schema validation
- Content filtering
- Rate limiting
- **Ship:** Validated inputs

**Wednesday: Output Filtering**
- PII detection
- Harmful content filtering
- Bias detection
- **Ship:** Filtered outputs

**Thursday-Friday: Security Audit**
- Audit both flagships
- Fix vulnerabilities
- Document security measures

---

### Week 24: Performance + Caching
**Monday: Latency Profiling**
- Identify bottlenecks
- Measure each component
- Optimization targets
- **Ship:** Performance report

**Tuesday-Wednesday: Semantic Caching**
- Cache similar queries
- Embedding-based cache
- Cache invalidation
- **Ship:** Cached RAG

**Thursday: Concurrent Requests**
- Async patterns
- Connection pooling
- Load testing
- **Ship:** Optimized service

**Friday: Cost Optimization**
- Model selection
- Prompt optimization
- Caching ROI

---

### Week 25: CI/CD + MLOps Lite
**Monday-Tuesday: GitHub Actions**
- Test automation
- Deployment automation
- Environment management
- **Ship:** CI/CD pipeline

**Wednesday: Experiment Tracking**
- MLflow basics
- Track experiments
- Compare runs
- **Ship:** Tracked experiments

**Thursday-Friday: Deployment**
- Staging environment
- Production deployment
- Rollback procedures

---

### Week 26: SQL for AI Systems
**Monday-Tuesday: Postgres Basics**
- CRUD operations
- Joins and aggregations
- Indexes
- **Ship:** SQL queries

**Wednesday: Schema Design**
- RAG metadata schema
- User interaction logs
- Analytics tables
- **Ship:** Database schema

**Thursday-Friday: Analytics**
- User behavior queries
- Document usage stats
- Cost analysis queries
- **Ship:** SQL-backed analytics

---

### FLEX WEEK 27: Catch Up / Production Polish
**Use this week to:**
- Add tests/monitoring to flagships
- Fix technical debt
- Improve documentation
- Performance optimization

---

## Phase 5: Advanced Topics (Weeks 28-32)

### Week 28: Multi-Agent Systems (Survey)
**Monday-Tuesday: CrewAI or AutoGen**
- Pick one framework
- Build simple multi-agent
- Compare to single agent
- **Ship:** Multi-agent experiment

**Wednesday-Friday: Analysis**
- When to use multi-agent?
- Coordination patterns
- Trade-offs
- **Ship:** Comparison writeup

---

### Week 29: Advanced RAG Patterns
**Monday: Contextual Compression**
**Tuesday: Parent-Document Retrieval**
**Wednesday: HyDE**
**Thursday: GraphRAG (survey)**
**Friday: Pick one, integrate**

**Deliverable:** Advanced RAG enhancement

---

### Week 30: Open Source Models
**Monday-Tuesday: Ollama Setup**
- Local model serving
- Model comparison
- **Ship:** Local LLM app

**Wednesday-Thursday: Comparison**
- GPT-4 vs Llama vs Mistral
- Cost/quality/latency
- **Ship:** Comparison report

**Friday: Decision Framework**
- When to use local vs API
- Trade-offs
- **Ship:** Decision guide

---

### Week 31: Fine-Tuning Primer
**Monday-Tuesday: When to Fine-Tune**
- Fine-tuning vs RAG vs prompting
- Use cases
- Cost/benefit
- **Ship:** Decision framework

**Wednesday-Thursday: LoRA/QLoRA**
- Concepts
- Small experiment
- **Ship:** Fine-tuning experiment

**Friday: Lessons Learned**
- Document findings
- When would you fine-tune?

---

### Week 32: Portfolio Polish + Flagship 3
**Monday-Tuesday: Polish Flagships**
- Update READMEs
- Add architecture diagrams
- Fix bugs
- **Ship:** Polished portfolio

**Wednesday-Thursday: Flagship 3 (Optional)**
- Your choice project
- Apply everything learned
- **Ship:** Third flagship

**Friday: Interview Prep**
- Practice explaining projects
- Review design decisions
- Prepare talking points

---

## FLEX WEEKS 32+: Job Search / Advanced Topics
**Use remaining time for:**
- Job applications
- Interview preparation
- Advanced topics (GraphRAG, fine-tuning depth)
- Contributing to open source
- Building more projects

---

## Weekly Checklist Template

Copy this for each week:

```markdown
## Week X: [Topic]

### Monday
- [ ] Read concept material (1 hour)
- [ ] Implement core feature (2 hours)
- [ ] Document progress (1 hour)

### Tuesday
- [ ] Continue implementation (3 hours)
- [ ] Write tests (1 hour)

### Wednesday
- [ ] Add enhancement (2 hours)
- [ ] Debug issues (2 hours)

### Thursday
- [ ] Polish implementation (2 hours)
- [ ] Update documentation (2 hours)

### Friday - Debug Lab
- [ ] Fix broken things (2 hours)
- [ ] Write learnings (1 hour)
- [ ] Plan next week (1 hour)

### Learning Checkpoints
- [ ] Checkpoint 1
- [ ] Checkpoint 2
- [ ] Checkpoint 3

### Deliverable
- [ ] [What you're shipping this week]
```

---

## Progress Tracking

Track your progress:

```markdown
## My Progress

### Completed Weeks
- [x] Week 1: Python Essentials
- [x] Week 2: Python for AI Apps
- [ ] Week 3: First LLM Call
- [ ] ...

### Flagship Projects
- [ ] Flagship 0.5: Deployed LLM API (Week 6)
- [ ] Flagship 1: Production RAG (Week 12)
- [ ] Flagship 2: Agentic Workflow (Week 19)
- [ ] Flagship 3: Your Choice (Week 32)

### Flex Weeks Used
- [ ] Flex Week 13: [What you did]
- [ ] Flex Week 20: [What you did]
- [ ] Flex Week 27: [What you did]

### Blog Posts Written
- [ ] Post 1: [Title]
- [ ] Post 2: [Title]
- [ ] Post 3: [Title]
```

---

## Next Steps

1. **Copy this roadmap** to your own repo
2. **Customize timeline** based on your pace
3. **Start Week 1** (or Week 3 if Python-ready)
4. **Track progress** weekly
5. **Use flex weeks** when needed
6. **Ship flagships** on schedule

**Remember:** This is a guide, not a prison. Adjust as needed. Focus on shipping working systems.

Let's build. 🚀
