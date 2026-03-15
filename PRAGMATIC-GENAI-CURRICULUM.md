# Pragmatic GenAI Engineer Curriculum
## Ship Fast, Learn Real, Build Portfolio

**Target Role:** AI/GenAI Engineer (RAG, Agents, LLM Apps)  
**Timeline:** 32 weeks (flexible, not rigid)  
**Pace:** 4 hours/day, 5 days/week = 20h/week  
**Philosophy:** Working code > perfect understanding. Ship, break, fix, repeat.

---

## Core Principles

1. **Ship by Week 3** - First working LLM app deployed
2. **Fail forward** - Every week includes "debug lab" time for when things break
3. **Portfolio over chapters** - 3 flagship projects, not 54 completed lessons
4. **Just-in-time learning** - Learn what you need when you need it
5. **Flex weeks built in** - 4 buffer weeks for rabbit holes and concept gaps

---

## Phase 0: Python Sprint (Weeks 1-2)
**Goal:** Enough Python to not get stuck on syntax

### Week 1: Python Essentials
- **Mon-Wed:** Python Daily Practice Days 1-6 (variables, strings, lists, dicts, control flow, functions)
- **Thu-Fri:** Error handling + file I/O + basic testing with pytest
- **Ship:** 5 working functions with passing tests
- **Flex:** If stuck, repeat exercises. If easy, skip to Week 2.

### Week 2: Python for AI Apps
- **Mon-Tue:** Pydantic models + type hints (you'll use this CONSTANTLY)
- **Wed-Thu:** Async/await basics (LLM APIs are async)
- **Fri:** Context managers + environment variables
- **Ship:** Config loader that validates API keys with Pydantic
- **Flex:** If async is confusing, use sync for now. Come back later.

**Exit Criteria:** Can write a function, handle errors, validate data with Pydantic, read .env files

---

## Phase 1: LLM Foundations (Weeks 3-6)
**Goal:** Working LLM app in production by Week 6

### Week 3: First LLM Call
- **Mon:** OpenAI API setup + first completion
- **Tue:** Structured outputs with Pydantic (JSON mode)
- **Wed:** Prompt templates + variable injection
- **Thu:** Retry logic + error handling
- **Fri:** Debug lab - fix broken prompts
- **Ship:** CLI tool that takes user input → LLM → structured JSON output

### Week 4: Multi-Provider Client
- **Mon-Tue:** Add Anthropic/Groq fallback
- **Wed:** Token counting + cost tracking
- **Thu:** Streaming responses
- **Fri:** Debug lab - handle rate limits
- **Ship:** Reusable LLM client module with fallbacks

### Week 5: FastAPI Service
- **Mon-Tue:** FastAPI basics + request/response models
- **Wed:** Add your LLM client as endpoint
- **Thu:** Logging + health checks
- **Fri:** Debug lab - test with curl/Postman
- **Ship:** LLM API service running locally

### Week 6: Docker + Deploy
- **Mon-Tue:** Dockerfile + docker-compose
- **Wed:** Deploy to Render/Railway/Fly.io (pick one)
- **Thu:** Add basic monitoring (logs, uptime)
- **Fri:** Demo day - show someone your deployed API
- **Ship:** 🎯 **FLAGSHIP 0.5** - Deployed LLM API service

**Exit Criteria:** You have a live URL that accepts prompts and returns structured responses

---

## Phase 2: RAG Core (Weeks 7-12)
**Goal:** Production RAG system with evaluation

### Week 7: Embeddings + Vector Store
- **Mon-Tue:** Sentence transformers + embedding basics
- **Wed:** Chroma setup + document ingestion
- **Thu:** Similarity search experiments
- **Fri:** Debug lab - why are results bad?
- **Ship:** Document indexer that stores 50+ docs

### Week 8: First RAG System
- **Mon-Tue:** Retrieval + prompt augmentation
- **Wed:** Citation tracking (source metadata)
- **Thu:** "I don't know" handling
- **Fri:** Debug lab - retrieval failures
- **Ship:** RAG assistant that cites sources

### Week 9: Chunking Strategies
- **Mon-Tue:** Fixed vs recursive vs semantic chunking
- **Wed:** Metadata design (doc type, date, section)
- **Thu:** Re-index with better chunking
- **Fri:** Compare before/after retrieval quality
- **Ship:** Improved indexing pipeline

### Week 10: Retrieval Quality
- **Mon:** Multi-query retrieval
- **Tue:** Reranking (Cohere or cross-encoder)
- **Wed:** Hybrid search (dense + BM25)
- **Thu:** Query rewriting
- **Fri:** Debug lab - measure what actually improved
- **Ship:** RAG v2 with documented improvements

### Week 11: Evaluation Harness
- **Mon-Tue:** Create 20 golden Q&A pairs
- **Wed:** Retrieval metrics (precision@k, MRR)
- **Thu:** Generation metrics (faithfulness, relevance)
- **Fri:** Run eval suite, document failures
- **Ship:** Automated evaluation script

### Week 12: RAG Production Polish
- **Mon:** Add to FastAPI service
- **Tue:** Docker + deploy
- **Wed:** Add tracing/logging (LangSmith or custom)
- **Thu:** Security basics (input validation, rate limiting)
- **Fri:** Demo + documentation
- **Ship:** 🎯 **FLAGSHIP 1** - Production RAG System

**FLEX WEEK 13:** Catch up, fix bugs, improve docs, or start early on Phase 3

**Exit Criteria:** Deployed RAG system with citations, evaluation harness, and clear README

---

## Phase 3: Agents + Workflows (Weeks 14-20)
**Goal:** Controlled agentic system (not autonomous chaos)

### Week 14: LangChain Basics
- **Mon-Tue:** Chains + LCEL (LangChain Expression Language)
- **Wed:** Memory (conversation history)
- **Thu:** Callbacks (token tracking, logging)
- **Fri:** Debug lab - chain debugging
- **Ship:** Conversational RAG with memory

### Week 15: Tool Calling
- **Mon-Tue:** Function calling basics (OpenAI/Anthropic)
- **Wed:** Build 3 simple tools (calculator, search, database query)
- **Thu:** Tool selection + execution
- **Fri:** Debug lab - tool failures
- **Ship:** LLM that can use tools

### Week 16: ReAct Agent
- **Mon-Tue:** ReAct pattern (Reason + Act loop)
- **Wed:** Implement simple ReAct agent
- **Thu:** Add guardrails (max iterations, timeouts)
- **Fri:** Debug lab - infinite loops
- **Ship:** Bounded ReAct agent

### Week 17: LangGraph Workflows
- **Mon-Tue:** State graphs + nodes
- **Wed:** Conditional routing
- **Thu:** Human-in-the-loop checkpoint
- **Fri:** Debug lab - state inspection
- **Ship:** Multi-step workflow with approval gate

### Week 18-19: Agentic System Build
- **Week 18:** Design + implement your agentic workflow
- **Week 19:** Add evaluation, observability, error handling
- **Ship:** 🎯 **FLAGSHIP 2** - Controlled Agentic Workflow

**FLEX WEEK 20:** Polish Flagship 2, add monitoring, write blog post

**Exit Criteria:** Agentic system with state management, human oversight, and trace logs

---

## Phase 4: Production Engineering (Weeks 21-26)
**Goal:** Make your systems production-grade

### Week 21: Testing AI Systems
- **Mon-Tue:** Property-based testing with Hypothesis
- **Wed:** Adversarial testing (prompt injection, jailbreaks)
- **Thu:** Regression tests for RAG/agents
- **Fri:** Debug lab - flaky tests
- **Ship:** Test suite for Flagship 1 & 2

### Week 22: Observability
- **Mon-Tue:** LangSmith or Arize Phoenix setup
- **Wed:** Distributed tracing
- **Thu:** Cost analytics + token tracking
- **Fri:** Debug lab - trace a failure
- **Ship:** Observability dashboard

### Week 23: Security + Guardrails
- **Mon:** Prompt injection defense
- **Tue:** Input validation + sanitization
- **Wed:** Output filtering (PII, harmful content)
- **Thu:** Rate limiting + abuse prevention
- **Fri:** Security audit of your systems
- **Ship:** Hardened applications

### Week 24: Performance + Caching
- **Mon:** Latency profiling
- **Tue:** Semantic caching
- **Wed:** Streaming optimizations
- **Thu:** Concurrent requests (async patterns)
- **Fri:** Load testing
- **Ship:** Performance report + improvements

### Week 25: CI/CD + MLOps Lite
- **Mon-Tue:** GitHub Actions for tests + deployment
- **Wed:** Environment management (dev/staging/prod)
- **Thu:** Experiment tracking (MLflow basics)
- **Fri:** Rollback procedures
- **Ship:** Automated deployment pipeline

### Week 26: SQL for AI Systems
- **Mon-Tue:** Postgres basics (CRUD, joins)
- **Wed:** Schema design for RAG metadata
- **Thu:** Analytics queries (user behavior, document usage)
- **Fri:** Connect SQL to your RAG system
- **Ship:** SQL-backed RAG with analytics

**FLEX WEEK 27:** Catch up on production concerns, fix technical debt

**Exit Criteria:** Both flagship projects have tests, monitoring, CI/CD, and security basics

---

## Phase 5: Advanced Topics (Weeks 28-32)
**Goal:** Differentiate your portfolio

### Week 28: Multi-Agent Systems (Survey)
- **Mon-Tue:** CrewAI or AutoGen (pick one)
- **Wed-Thu:** Build simple multi-agent workflow
- **Fri:** Compare to single-agent approach
- **Ship:** Multi-agent experiment + writeup

### Week 29: Advanced RAG Patterns
- **Mon:** Contextual compression
- **Tue:** Parent-document retrieval
- **Wed:** HyDE (Hypothetical Document Embeddings)
- **Thu:** GraphRAG concepts (survey only)
- **Fri:** Pick one, integrate into Flagship 1
- **Ship:** Advanced RAG enhancement

### Week 30: Open Source Models
- **Mon-Tue:** Ollama setup + local models
- **Wed:** Compare GPT-4 vs Llama vs Mistral
- **Thu:** Cost/quality/latency tradeoffs
- **Fri:** When to use local vs API models
- **Ship:** Model comparison report

### Week 31: Fine-Tuning Primer
- **Mon-Tue:** When to fine-tune vs RAG vs prompt engineering
- **Wed-Thu:** LoRA/QLoRA concepts + small experiment
- **Fri:** Document lessons learned
- **Ship:** Fine-tuning decision framework

### Week 32: Portfolio Polish + Interview Prep
- **Mon-Tue:** Polish all READMEs, add architecture diagrams
- **Wed:** Record demo videos for each flagship
- **Thu:** Write technical blog posts
- **Fri:** Practice explaining trade-offs
- **Ship:** 🎯 **COMPLETE PORTFOLIO** - 2 flagship projects + blog posts

---

## Projects Architecture: Guided Learning, Not Copy-Paste

**CRITICAL TEACHING PHILOSOPHY:**
- Projects provide **architecture guidance, starter templates, and TODO markers**
- Students implement core logic themselves with **hints, not solutions**
- AI assistants should **explain concepts, suggest approaches, debug errors** - NOT write complete implementations
- Each project includes **learning checkpoints** where students must explain their decisions

---

## Mini-Projects (Weeks 3-11)

### Mini-Project 1: Structured LLM Client (Week 4)
**Learning Goals:** API design, error handling, fallback strategies, cost tracking

**Provided Scaffolding:**
```python
# starter_code/llm_client.py
from pydantic import BaseModel
from typing import Optional, List

class LLMConfig(BaseModel):
    """TODO: Define config fields for API keys, model names, timeouts"""
    pass

class LLMResponse(BaseModel):
    """TODO: Define response structure with content, tokens, cost"""
    pass

class MultiProviderClient:
    def __init__(self, config: LLMConfig):
        """TODO: Initialize providers in priority order"""
        pass
    
    async def complete(self, prompt: str) -> LLMResponse:
        """
        TODO: Implement with:
        1. Try primary provider
        2. On failure, try fallback
        3. Track tokens and cost
        4. Log all attempts
        
        HINT: Use try/except for each provider
        HINT: Store provider order in a list
        """
        pass
```

**Guided Exercises:**
1. **Design Phase:** Draw the fallback flow on paper before coding
2. **Implementation:** Fill in TODOs with your logic
3. **Testing:** Write 3 test cases (success, primary fail, all fail)
4. **Reflection:** Why is fallback order important? When would you change it?

**Learning Checkpoints:**
- [ ] Explain: Why async instead of sync?
- [ ] Explain: How do you calculate cost per request?
- [ ] Explain: What happens if all providers fail?
- [ ] Demo: Show logs from a failed request

**Success Criteria:**
- Client switches providers on failure
- Costs are tracked accurately
- Tests pass
- You can explain the code to someone else

---

### Mini-Project 2: Document Indexer (Week 9)
**Learning Goals:** Chunking strategies, metadata design, vector storage

**Provided Scaffolding:**
```python
# starter_code/indexer.py
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Chunk:
    """TODO: Define chunk structure with text, metadata, embedding"""
    pass

class ChunkingStrategy:
    def chunk(self, text: str) -> List[Chunk]:
        """TODO: Implement chunking logic"""
        raise NotImplementedError

class FixedSizeChunker(ChunkingStrategy):
    """TODO: Implement fixed-size chunking with overlap"""
    pass

class SemanticChunker(ChunkingStrategy):
    """TODO: Implement sentence-boundary chunking"""
    pass

class DocumentIndexer:
    def __init__(self, chunker: ChunkingStrategy, vector_store):
        """TODO: Initialize with strategy pattern"""
        pass
    
    def index_document(self, filepath: str, metadata: Dict) -> int:
        """
        TODO: Implement pipeline:
        1. Load document
        2. Chunk with strategy
        3. Generate embeddings
        4. Store in vector DB
        5. Return chunk count
        
        HINT: Use sentence-transformers for embeddings
        HINT: Batch embeddings for efficiency
        """
        pass
```

**Guided Exercises:**
1. **Experiment:** Index same doc with 3 chunk sizes (256, 512, 1024). Which retrieves best?
2. **Metadata Design:** What metadata would help filter results? (date, doc_type, author, section)
3. **Edge Cases:** What if document is empty? Too large? Non-text format?

**Learning Checkpoints:**
- [ ] Explain: Why does chunk size matter?
- [ ] Explain: What's the trade-off between small and large chunks?
- [ ] Explain: How do embeddings capture semantic meaning?
- [ ] Demo: Show retrieval quality difference between chunking strategies

**Success Criteria:**
- Can index 50+ documents
- Metadata is queryable
- Can explain why you chose your chunking strategy
- Documented comparison of strategies

---

### Mini-Project 3: RAG Evaluation Harness (Week 11)
**Learning Goals:** Metrics, golden datasets, regression testing

**Provided Scaffolding:**
```python
# starter_code/evaluator.py
from typing import List, Dict
from pydantic import BaseModel

class EvalQuestion(BaseModel):
    """TODO: Define question, expected_answer, expected_sources"""
    pass

class EvalResult(BaseModel):
    """TODO: Define metrics (retrieval_precision, answer_quality, citation_accuracy)"""
    pass

class RAGEvaluator:
    def __init__(self, rag_system, golden_questions: List[EvalQuestion]):
        """TODO: Load golden dataset"""
        pass
    
    def evaluate_retrieval(self, question: str, retrieved_docs: List) -> float:
        """
        TODO: Calculate retrieval metrics
        - Precision@K: How many retrieved docs are relevant?
        - MRR: Mean Reciprocal Rank of first relevant doc
        
        HINT: Compare retrieved doc IDs to expected source IDs
        """
        pass
    
    def evaluate_answer(self, question: str, answer: str, expected: str) -> float:
        """
        TODO: Calculate answer quality
        - Use LLM-as-judge pattern
        - Check for hallucinations
        - Verify citation accuracy
        
        HINT: Prompt another LLM to score the answer
        """
        pass
    
    def run_full_eval(self) -> Dict[str, float]:
        """TODO: Run all questions, aggregate metrics, generate report"""
        pass
```

**Guided Exercises:**
1. **Golden Dataset:** Create 20 questions with known good answers
2. **Baseline:** Run eval on your current RAG system
3. **Improve:** Make one change (chunking, retrieval, prompt), re-run eval
4. **Compare:** Did metrics improve? By how much?

**Learning Checkpoints:**
- [ ] Explain: What's the difference between retrieval quality and answer quality?
- [ ] Explain: Why do you need a golden dataset?
- [ ] Explain: How do you detect hallucinations?
- [ ] Demo: Show before/after metrics from an improvement

**Success Criteria:**
- 20+ golden questions
- Automated eval script
- Metrics tracked over time
- Can explain what each metric means

---

## Flagship Projects (Weeks 12, 19, 32)

### Flagship 1: Production RAG System (Week 12)
**Learning Goals:** End-to-end system design, production concerns, deployment

#### Phase 1: Architecture Design (Before Coding)
**Guided Questions:**
1. What documents will you index? (Pick a real domain: legal contracts, technical docs, research papers)
2. What questions will users ask? (Write 10 example queries)
3. What's your chunking strategy? (Justify your choice)
4. How will you handle "I don't know"? (Design the logic)
5. What could go wrong? (List 5 failure modes)

**Deliverable:** Architecture diagram (draw.io, Excalidraw, or paper photo)

#### Phase 2: Core Implementation (Guided TODOs)
**Provided Scaffolding:**
```python
# flagship1/rag_system.py
class ProductionRAG:
    """
    TODO: Implement production-grade RAG with:
    - Document ingestion pipeline
    - Retrieval with citations
    - Answer generation with source tracking
    - Evaluation harness
    - Error handling
    - Logging
    """
    
    def __init__(self, config: RAGConfig):
        """
        TODO: Initialize components:
        - Vector store
        - LLM client
        - Chunking strategy
        - Evaluator
        
        DESIGN DECISION: Why did you choose this vector store?
        """
        pass
    
    async def query(self, question: str) -> RAGResponse:
        """
        TODO: Implement RAG pipeline:
        1. Retrieve relevant chunks
        2. Rerank (optional)
        3. Build context prompt
        4. Generate answer
        5. Extract citations
        6. Validate answer quality
        
        DESIGN DECISION: How many chunks to retrieve? Why?
        """
        pass
    
    def evaluate(self) -> EvalReport:
        """TODO: Run evaluation harness, return metrics"""
        pass
```

**Implementation Milestones:**
- **Milestone 1:** Basic retrieval works (no generation yet)
- **Milestone 2:** Generation with citations
- **Milestone 3:** Evaluation harness passes 80%+ questions
- **Milestone 4:** FastAPI wrapper
- **Milestone 5:** Docker + deployment

#### Phase 3: Production Hardening (Guided Checklist)
**Security Checklist:**
- [ ] Input validation (max length, allowed characters)
- [ ] Rate limiting (requests per user)
- [ ] Prompt injection tests (try 5 adversarial inputs)
- [ ] PII filtering (if applicable)

**Observability Checklist:**
- [ ] Structured logging (JSON logs with trace IDs)
- [ ] Latency tracking (p50, p95, p99)
- [ ] Cost tracking (tokens per request)
- [ ] Error alerting (what triggers an alert?)

**Testing Checklist:**
- [ ] Unit tests for chunking, retrieval, generation
- [ ] Integration test for full pipeline
- [ ] Regression tests (golden dataset)
- [ ] Load test (can it handle 10 concurrent requests?)

#### Phase 4: Documentation & Demo
**Required Documentation:**
1. **README.md:**
   - What problem does this solve?
   - Architecture diagram
   - Setup instructions (5 steps max)
   - Example queries
   - Known limitations

2. **DESIGN_DECISIONS.md:**
   - Why this chunking strategy?
   - Why this vector store?
   - Why this retrieval approach?
   - What trade-offs did you make?

3. **EVALUATION_REPORT.md:**
   - Metrics (retrieval precision, answer quality)
   - Failure analysis (what questions fail? why?)
   - Improvement ideas

4. **Demo Video (3-5 min):**
   - Show the system working
   - Show a failure case
   - Explain one design decision

**Learning Checkpoints:**
- [ ] Explain: Walk through the code with someone (rubber duck counts)
- [ ] Explain: What's the bottleneck in your system?
- [ ] Explain: How would you scale this to 1M documents?
- [ ] Explain: What would you do differently next time?

**Success Criteria:**
- Deployed and accessible via URL
- Evaluation harness shows 80%+ quality
- Documentation is clear enough for someone else to run it
- You can explain every design decision

---

### Flagship 2: Controlled Agentic Workflow (Week 19)
**Learning Goals:** State management, tool orchestration, human oversight

#### Phase 1: Workflow Design (Before Coding)
**Pick a Real Use Case:**
- **Option A:** Research Assistant (search → summarize → cite → review)
- **Option B:** Data Analyst (query → analyze → visualize → report)
- **Option C:** Content Generator (research → outline → draft → edit)
- **Option D:** Your own idea (must have 4+ steps)

**Guided Questions:**
1. What are the discrete steps? (Draw a flowchart)
2. Where does the human review? (Which step needs approval?)
3. What tools does the agent need? (List 3-5 tools)
4. What could go wrong? (List 5 failure modes)
5. How do you prevent infinite loops? (Max iterations? Timeout?)

**Deliverable:** State machine diagram with nodes, edges, and decision points

#### Phase 2: Tool Implementation (Guided TODOs)
**Provided Scaffolding:**
```python
# flagship2/tools.py
from typing import Dict, Any
from pydantic import BaseModel

class ToolResult(BaseModel):
    """TODO: Define success, data, error fields"""
    pass

class BaseTool:
    """Base class for all tools"""
    name: str
    description: str
    
    def execute(self, **kwargs) -> ToolResult:
        """TODO: Implement tool logic with error handling"""
        raise NotImplementedError

class SearchTool(BaseTool):
    """
    TODO: Implement web search or document search
    
    DESIGN DECISION: Web search (Tavily, SerpAPI) or local search (vector DB)?
    Why did you choose this?
    """
    pass

class AnalysisTool(BaseTool):
    """
    TODO: Implement data analysis or summarization
    
    HINT: Use LLM for analysis, but validate outputs
    """
    pass

class VisualizationTool(BaseTool):
    """
    TODO: Implement chart/graph generation
    
    HINT: Use matplotlib or plotly, return image path
    """
    pass
```

**Tool Development Checklist:**
- [ ] Each tool has clear input/output schema (Pydantic models)
- [ ] Each tool handles errors gracefully (try/except)
- [ ] Each tool has unit tests
- [ ] Each tool logs execution (input, output, duration)

#### Phase 3: State Machine Implementation (Guided TODOs)
**Provided Scaffolding:**
```python
# flagship2/workflow.py
from typing import Dict, List, Optional
from enum import Enum

class WorkflowState(Enum):
    """TODO: Define states (START, SEARCH, ANALYZE, REVIEW, COMPLETE, FAILED)"""
    pass

class WorkflowContext(BaseModel):
    """
    TODO: Define state data:
    - current_state
    - user_input
    - tool_results
    - iteration_count
    - human_feedback
    """
    pass

class AgenticWorkflow:
    def __init__(self, tools: List[BaseTool], max_iterations: int = 10):
        """
        TODO: Initialize workflow with:
        - Tool registry
        - State machine
        - LLM client
        - Max iteration guard
        
        DESIGN DECISION: Why max_iterations? What's a good default?
        """
        pass
    
    async def execute(self, user_input: str) -> WorkflowContext:
        """
        TODO: Implement workflow loop:
        1. Determine next action (LLM decides which tool)
        2. Execute tool
        3. Update state
        4. Check if human review needed
        5. Repeat until COMPLETE or FAILED
        
        DESIGN DECISION: How does LLM choose the next tool?
        HINT: Use function calling or ReAct prompting
        """
        pass
    
    def request_human_review(self, context: WorkflowContext) -> bool:
        """
        TODO: Pause workflow, show results, get approval
        
        DESIGN DECISION: What triggers human review?
        """
        pass
```

**Implementation Milestones:**
- **Milestone 1:** Single tool execution works
- **Milestone 2:** State transitions work (can move between states)
- **Milestone 3:** LLM selects correct tool for task
- **Milestone 4:** Human review checkpoint works
- **Milestone 5:** Full workflow completes successfully

#### Phase 4: Observability & Guardrails (Guided Checklist)
**Observability Requirements:**
- [ ] Trace every state transition (log: timestamp, state, action, result)
- [ ] Visualize workflow execution (ASCII diagram or web UI)
- [ ] Track token usage per step
- [ ] Measure latency per tool

**Guardrails Checklist:**
- [ ] Max iterations enforced (prevent infinite loops)
- [ ] Timeout per tool (prevent hanging)
- [ ] Retry logic for transient failures
- [ ] Graceful degradation (if tool fails, what happens?)
- [ ] Human override (can user stop workflow?)

**Testing Checklist:**
- [ ] Happy path test (workflow completes successfully)
- [ ] Tool failure test (one tool fails, workflow handles it)
- [ ] Max iteration test (workflow stops at limit)
- [ ] Human rejection test (user rejects at review, workflow adjusts)

#### Phase 5: Documentation & Demo
**Required Documentation:**
1. **README.md:**
   - What workflow does this automate?
   - State machine diagram
   - Example execution trace
   - Setup instructions

2. **WORKFLOW_DESIGN.md:**
   - Why this workflow structure?
   - Why these tools?
   - Why human review at this step?
   - What are the failure modes?

3. **COMPARISON.md:**
   - Why workflow > fully autonomous agent?
   - When would you use autonomous agent instead?
   - Trade-offs of human-in-the-loop

4. **Demo Video (3-5 min):**
   - Show successful workflow execution
   - Show human review step
   - Show failure handling

**Learning Checkpoints:**
- [ ] Explain: Why is state management important?
- [ ] Explain: How do you prevent the agent from going off-track?
- [ ] Explain: When would you add more tools?
- [ ] Explain: How would you evaluate agent decision quality?

**Success Criteria:**
- Workflow completes real task end-to-end
- Human review works smoothly
- Trace logs show every decision
- Documentation explains why workflow is controlled
- You can defend your design choices

---

### Flagship 3 (Optional): Your Choice (Week 32)
**Learning Goals:** Apply everything you've learned to a novel problem

#### Project Options:

**Option A: LLM Evaluation Platform**
- Compare 3+ models on same task
- Track cost, latency, quality
- Build leaderboard UI
- **Learning Focus:** Evaluation, benchmarking, metrics

**Option B: Domain-Specific RAG**
- Pick a domain (legal, medical, engineering)
- Build specialized chunking/retrieval
- Add domain-specific validation
- **Learning Focus:** Domain adaptation, specialized RAG

**Option C: Multi-Agent System**
- Build 3+ specialized agents
- Implement coordination pattern
- Add conflict resolution
- **Learning Focus:** Multi-agent orchestration

**Option D: Fine-Tuning Pipeline**
- Collect/generate training data
- Fine-tune with LoRA
- Compare base vs fine-tuned
- **Learning Focus:** Model adaptation

#### Universal Requirements (All Options):
1. **Problem Statement:** What problem are you solving? Why?
2. **Architecture Diagram:** How does the system work?
3. **Implementation:** Working code with tests
4. **Evaluation:** How do you measure success?
5. **Documentation:** README + design decisions + demo
6. **Reflection:** What did you learn? What would you do differently?

**Learning Checkpoints:**
- [ ] Explain: Why did you choose this project?
- [ ] Explain: What was the hardest part?
- [ ] Explain: What surprised you?
- [ ] Explain: How would you improve it with more time?

---

## Teaching Methodology: Guided Discovery

### What AI Assistants Should Do:
✅ **Explain concepts:** "Embeddings are vector representations of text that capture semantic meaning..."
✅ **Suggest approaches:** "You could use either fixed-size or semantic chunking. Fixed-size is simpler but..."
✅ **Debug errors:** "That error means your API key isn't loaded. Check your .env file..."
✅ **Ask guiding questions:** "Why did you choose chunk size 512? What happens if you use 256?"
✅ **Provide examples:** "Here's how Chroma's query method works: `collection.query(query_texts=['...'])`"
✅ **Review code:** "Your error handling looks good, but what happens if all providers fail?"

### What AI Assistants Should NOT Do:
❌ **Write complete implementations:** Don't give full function bodies for TODOs
❌ **Make design decisions:** Don't choose chunking strategy, vector store, or architecture
❌ **Skip learning checkpoints:** Don't let students move on without explaining concepts
❌ **Optimize prematurely:** Don't suggest advanced patterns before basics work
❌ **Remove struggle:** Some friction is necessary for learning

### Example Interaction:

**Student:** "How do I implement the chunking function?"

**Bad AI Response (Vibe-Coding):**
```python
def chunk(self, text: str) -> List[Chunk]:
    chunks = []
    for i in range(0, len(text), self.chunk_size):
        chunk_text = text[i:i+self.chunk_size]
        chunks.append(Chunk(text=chunk_text, metadata={}))
    return chunks
```

**Good AI Response (Teaching):**
"Let's think through the chunking logic step by step:

1. You need to split the text into pieces of `chunk_size` length
2. You'll iterate through the text, taking slices
3. Each slice becomes a Chunk object

Questions to consider:
- What happens if the text length isn't evenly divisible by chunk_size?
- Do you want overlap between chunks? (Hint: overlap helps with context)
- What metadata should each chunk have? (Hint: position, source document)

Try implementing it yourself first. If you get stuck, I can help debug specific errors."

---

## Project Evaluation Rubric

### For Each Project:

**Implementation (40%)**
- [ ] Core functionality works
- [ ] Error handling is present
- [ ] Code is readable (comments, naming)
- [ ] Tests pass

**Understanding (30%)**
- [ ] Can explain design decisions
- [ ] Can explain trade-offs
- [ ] Can explain failure modes
- [ ] Can answer "why" questions

**Documentation (20%)**
- [ ] README is clear
- [ ] Architecture is documented
- [ ] Setup instructions work
- [ ] Demo is recorded

**Production Quality (10%)**
- [ ] Logging is present
- [ ] Deployment works
- [ ] Monitoring exists
- [ ] Security basics covered

**Passing Grade:** 70%+ (you don't need perfection, you need working systems and understanding)

---

## Weekly Rhythm (4 hours/day)

### Monday-Thursday (Build Days)
- **Hour 1:** Read/watch concept material (minimum viable understanding)
- **Hour 2:** Implement (copy-paste-modify is OK at first)
- **Hour 3:** Debug + test (make it work)
- **Hour 4:** Document (README, comments, notes)

### Friday (Debug Lab + Reflection)
- **Hour 1-2:** Fix the week's broken things
- **Hour 3:** Write what you learned (blog draft, notes)
- **Hour 4:** Plan next week (what's the ship target?)

### When You Get Stuck (Inevitable)
1. **Timebox:** Spend max 2 hours debugging alone
2. **Ask:** ChatGPT, Claude, or community (Discord, Reddit)
3. **Simplify:** Remove features until it works, then add back
4. **Skip:** Mark as "come back later" and move on
5. **Flex week:** Use buffer weeks to catch up

---

## Flex Weeks (Built-In Slack)

- **Week 13:** After RAG core
- **Week 20:** After agents
- **Week 27:** After production engineering
- **Week 32+:** Portfolio polish + job search

**Use flex weeks for:**
- Catching up on incomplete weeks
- Deep-diving into confusing concepts
- Fixing bugs in flagship projects
- Exploring rabbit holes (GraphRAG, fine-tuning, etc.)
- Burnout prevention (take a break!)

---

## What We're NOT Doing (And Why)

| Skipped Topic | Why | When to Learn It |
|---------------|-----|------------------|
| Classical ML (sklearn) | Not core for GenAI Engineer roles | If applying to ML Engineer roles |
| Deep Learning Training (PyTorch) | RAG/agents use pre-trained models | If doing fine-tuning or research |
| MLOps (Kubeflow, SageMaker) | Overkill for LLM apps | If joining ML platform team |
| Kubernetes | Docker is enough for now | If deploying at scale |
| GraphRAG depth | Survey is enough | If you have graph data use case |
| Multi-agent swarms | Controlled workflows are more practical | After mastering single agents |
| Data Engineering (Spark, Airflow) | Not primary GenAI skill | If building data pipelines |

---

## Success Metrics (Not Perfection Metrics)

### By Week 6
- [ ] Deployed LLM API that someone else can use
- [ ] Can explain: prompt engineering, structured outputs, error handling

### By Week 13
- [ ] Production RAG system with evaluation
- [ ] Can explain: embeddings, chunking, retrieval strategies, citations

### By Week 20
- [ ] Agentic workflow with human oversight
- [ ] Can explain: tool calling, state management, ReAct pattern, guardrails

### By Week 27
- [ ] Both flagships have tests, monitoring, CI/CD
- [ ] Can explain: observability, security, performance optimization

### By Week 32
- [ ] 2-3 portfolio projects with demos
- [ ] Technical blog posts explaining trade-offs
- [ ] Can pass GenAI Engineer interviews

---

## Job-Ready Checklist (GenAI Engineer)

### Core Skills (Must Have)
- [x] Python + Pydantic + async
- [x] LLM APIs (OpenAI, Anthropic, Groq)
- [x] Prompt engineering + structured outputs
- [x] Embeddings + vector databases (Chroma, Pinecone, Weaviate)
- [x] RAG (chunking, retrieval, evaluation)
- [x] Agents (tool calling, ReAct, workflows)
- [x] LangChain + LangGraph
- [x] FastAPI + Docker
- [x] Testing (pytest, property-based, adversarial)
- [x] Observability (LangSmith, tracing, logging)
- [x] Security (prompt injection, input validation)

### Production Skills (Should Have)
- [x] CI/CD (GitHub Actions)
- [x] Deployment (Render, Railway, Fly.io, or AWS)
- [x] Monitoring + alerting
- [x] Cost tracking + optimization
- [x] SQL basics (Postgres)
- [x] Caching strategies

### Advanced Skills (Nice to Have)
- [ ] Multi-agent systems (CrewAI, AutoGen)
- [ ] Advanced RAG (hybrid search, reranking, GraphRAG)
- [ ] Fine-tuning (LoRA/QLoRA)
- [ ] Open source models (Ollama, vLLM)
- [ ] LlamaIndex

---

## Resources (Just-In-Time)

### Week 1-2 (Python)
- Python Daily Practice repo (your existing resource)
- Real Python tutorials (when stuck)

### Week 3-6 (LLM Basics)
- OpenAI Cookbook
- Anthropic Prompt Engineering Guide
- FastAPI docs

### Week 7-13 (RAG)
- LangChain RAG tutorials
- Chroma documentation
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)

### Week 14-20 (Agents)
- "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
- LangGraph documentation
- LangChain Agent guides

### Week 21-27 (Production)
- LangSmith evaluation guides
- OWASP LLM Top 10 (security)
- Hypothesis documentation (property-based testing)

### Week 28-32 (Advanced)
- CrewAI documentation
- "Self-RAG: Learning to Retrieve, Generate, and Critique" (Asai et al., 2023)
- LoRA paper (Hu et al., 2021)

---

## When Things Go Wrong (They Will)

### "I'm stuck on Week X"
→ Use a flex week. Skip to next topic. Come back later.

### "My code doesn't work"
→ Friday debug lab. Ask AI assistant. Simplify until it works.

### "I don't understand embeddings/agents/etc."
→ Build first, understand later. Working code teaches better than theory.

### "I'm behind schedule"
→ Schedule is a guide, not a prison. Adjust timeline. Focus on flagships.

### "I want to learn [advanced topic]"
→ Great! Use flex weeks or add after Week 32. Don't derail core path.

### "Is this good enough for a job?"
→ If you have 2 deployed projects with READMEs and can explain trade-offs, yes.

---

## Final Philosophy

**Perfect is the enemy of shipped.**

- Your first RAG system will be bad. Ship it anyway.
- Your first agent will be buggy. Ship it anyway.
- Your code will be messy. Refactor later.
- Your understanding will be incomplete. Learn by doing.

**The goal is not to know everything. The goal is to build things that work.**

By Week 32, you'll have:
- 2-3 deployed projects
- Real debugging experience
- Production engineering habits
- A portfolio that proves you can ship

That's more valuable than perfect theoretical knowledge.

---

## Start Now

**Week 1 starts Monday. Not "when you're ready." Monday.**

Clone the Python Daily Practice repo. Do Day 1. Ship 5 functions.

The curriculum will adjust to you. You won't adjust to the curriculum.

Let's build. 🚀
