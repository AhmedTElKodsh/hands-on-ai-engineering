# Curriculum Roadmap v6.1 Enhancements
**Date**: 2026-01-18
**Version**: 6.1 (Enhanced)
**Status**: Ready for Implementation

---

## 📊 Summary of Changes

### Version 6.0 → Version 6.1

| Metric | v6.0 | v6.1 | Change |
|--------|------|------|--------|
| **Total Chapters** | 54 core + 13 bridges = 67 | 59 core + 13 bridges = 72 | +5 chapters |
| **Total Hours** | 71 hours | 78 hours | +7 hours |
| **Correctness Properties** | P1-P79 (79 properties) | P1-P85 (85 properties) | +6 properties |
| **Coverage** | Strong foundation | Industry-leading 2026 | Comprehensive |

---

## 🆕 New Chapters Added

### 1. Chapter 38A: GraphRAG & Knowledge Graphs (NEW)
**Placement**: After Chapter 38 (Hybrid Search & Reranking)
**Phase**: 7 (LlamaIndex)
**Time**: 2.5 hours
**Difficulty**: ⭐⭐⭐⭐

**What You'll Build**: A GraphRAG system that combines vector search with knowledge graphs for superior retrieval accuracy.

**Why This Matters**: GraphRAG is emerging as the 2026 standard for complex retrieval, offering 40% better accuracy than pure vector search by capturing entity relationships.

**Learning Objectives**:
- Understand knowledge graphs (entities, relationships, properties)
- Build knowledge graphs from unstructured documents
- Implement hybrid retrieval (vectors + graphs)
- Use LlamaIndex `KnowledgeGraphIndex` and `GraphRAGQueryEngine`
- Apply to CE domain (extract material-building-load relationships)

**Key Concepts**: Knowledge graphs, graph databases (Neo4j), entity extraction, relationship mapping, hybrid retrieval, subgraph querying

**Correctness Properties**: [P80: Graph completeness, P81: Relationship accuracy]

**Code Example**:
```python
from llama_index import KnowledgeGraphIndex, GraphRAGQueryEngine

# Build knowledge graph from CE documents
docs = load_documents("structural_reports/")
kg_index = KnowledgeGraphIndex.from_documents(docs)

# Query with GraphRAG
rag_engine = GraphRAGQueryEngine(
    vector_store=chroma_store,
    knowledge_graph=kg_index
)
response = rag_engine.query(
    "What materials are used in buildings with >500kN capacity?"
)
```

---

### 2. Chapter 40A: Evaluation with LangSmith (REFACTORED)
**Placement**: Replaces original Chapter 40
**Phase**: 8 (Production)
**Time**: 1.5 hours (unchanged)
**Difficulty**: ⭐⭐⭐

**What Changed**: Original Chapter 40 content split into focused LangSmith-only coverage. More depth on LangChain-specific evaluation patterns.

**New Content**:
- Deeper dive into LangSmith datasets
- Advanced prompt comparison workflows
- LangChain integration best practices

---

### 3. Chapter 40B: Production Observability with Arize Phoenix (NEW)
**Placement**: After Chapter 40A
**Phase**: 8 (Production)
**Time**: 2 hours
**Difficulty**: ⭐⭐⭐⭐

**What You'll Build**: Production-grade observability for LLM systems using Arize Phoenix (open-source, vendor-neutral).

**Why This Matters**: 94% of production agents have observability. Phoenix is the leading open-source standard, used by teams that need vendor-neutral, OpenTelemetry-based monitoring.

**Learning Objectives**:
- Set up Arize Phoenix server
- Instrument LLM calls with Phoenix SDK
- Trace full RAG pipelines (retrieval → augmentation → generation)
- Identify bottlenecks (embedding time, retrieval latency, LLM latency)
- Monitor token usage & costs per trace
- Run evaluations on production traces
- A/B test prompt changes

**Key Concepts**: Observability, OpenTelemetry, tracing, Phoenix SDK, RAG pipeline monitoring, bottleneck analysis, token tracking, A/B testing

**Correctness Properties**: [P82: Trace completeness, P83: Latency measurement accuracy]

**Code Example**:
```python
from phoenix.trace import using_project
from phoenix.trace.langchain import LangChainInstrumentor

# Instrument with Phoenix
LangChainInstrumentor().instrument()

with using_project("ce-rag-system"):
    # Your RAG pipeline - fully traced
    response = rag_chain.invoke(query)

# View traces in Phoenix UI at http://localhost:6006
import phoenix as px
px.launch_app()
```

---

### 4. Chapter 40C: Distributed Tracing & Cost Analytics (NEW)
**Placement**: After Chapter 40B
**Phase**: 8 (Production)
**Time**: 1.5 hours
**Difficulty**: ⭐⭐⭐⭐

**What You'll Build**: Distributed tracing for multi-service architectures and comprehensive cost analytics.

**Why This Matters**: Production AI systems are distributed (frontend → backend → LLM → vector DB). You need tracing across services and granular cost tracking per user/project.

**Learning Objectives**:
- Implement distributed tracing for multi-service architectures
- Use correlation IDs across services
- Integrate OpenTelemetry for end-to-end visibility
- Track costs per user/session/project
- Set budget alerts and cost limits
- Build real-time monitoring dashboards (Grafana)
- Track SLAs (99.9% uptime, <2s latency)

**Key Concepts**: Distributed tracing, correlation IDs, OpenTelemetry, cost analytics, budget alerts, SLA tracking, Grafana dashboards

**Correctness Properties**: [P84: Correlation ID propagation, P85: Cost attribution accuracy]

**Code Example**:
```python
from opentelemetry import trace
from phoenix.trace import log_cost

tracer = trace.get_tracer(__name__)

# Distributed tracing across services
with tracer.start_as_current_span("rag-pipeline"):
    with tracer.start_as_current_span("retrieval"):
        docs = retriever.get_relevant(query)
    with tracer.start_as_current_span("generation"):
        with log_cost(user_id="ahmed", project="bridge-analysis"):
            answer = llm.generate(docs, query)
            # Automatically tracks tokens & cost per user/project
```

---

### 5. Chapter 48A: Swarm Pattern (Educational) (NEW)
**Placement**: After Chapter 48 (Debugging Multi-Agent Systems)
**Phase**: 9 (Multi-Agent Systems)
**Time**: 1.5 hours
**Difficulty**: ⭐⭐⭐

**What You'll Build**: Peer-to-peer agent handoff system using OpenAI Swarm pattern.

**Why This Matters**: Swarm teaches agent handoffs without central supervision - valuable for understanding peer-to-peer patterns. Educational tool, NOT for production.

**Learning Objectives**:
- Understand peer-to-peer agent communication
- Implement handoff instructions
- Let agents transfer control autonomously
- Recognize when Swarm is appropriate (learning, prototyping)
- Know when to migrate to production frameworks (LangGraph)

**Key Concepts**: Swarm pattern, peer-to-peer agents, handoffs, agent transfer, educational prototyping

**Correctness Properties**: [P86: Handoff accuracy, P87: Agent reachability]

**Code Example**:
```python
from swarm import Agent, Swarm

# Define 3-agent pipeline
extractor = Agent(
    name="Extractor",
    instructions="Extract key data from CE documents",
    functions=[extract_function],
    handoff_to=["Analyzer"]
)

analyzer = Agent(
    name="Analyzer",
    instructions="Analyze extracted data for compliance",
    functions=[analyze_function],
    handoff_to=["Reporter"]
)

reporter = Agent(
    name="Reporter",
    instructions="Generate final compliance report",
    functions=[report_function]
)

# Run swarm - agents autonomously hand off to each other
client = Swarm()
response = client.run(
    agent=extractor,
    messages=[{"role": "user", "content": "Process bridge_spec.pdf"}]
)
```

---

### 6. Chapter 52A: Multimodal AI for Civil Engineering (NEW)
**Placement**: After Chapter 52 (Technical Report Generation)
**Phase**: 10 (Civil Engineering Application)
**Time**: 2.5 hours
**Difficulty**: ⭐⭐⭐⭐

**What You'll Build**: Multimodal AI system that analyzes CAD drawings, site photos, and generates compliance reports with visual evidence.

**Why This Matters**: Leading CE firms (Civils.ai) use multimodal AI for automated drawing review, site inspections, and safety compliance. This is the future of CE automation.

**Learning Objectives**:
- Use multimodal LLMs (GPT-4 Vision, Claude 3)
- Extract text from CAD drawings (OCR)
- Parse structural diagrams
- Analyze drone photos for site inspection
- Detect safety violations automatically
- Generate inspection reports with image evidence
- Automated compliance checking from visuals

**Key Concepts**: Multimodal LLMs, GPT-4 Vision, Claude 3, CAD analysis, site inspection, safety violation detection, compliance checking

**Correctness Properties**: [P88: Image parsing accuracy, P89: Compliance detection from visuals]

**Code Example**:
```python
from openai import OpenAI

client = OpenAI()

# Analyze CAD drawing for compliance
with open("foundation_plan.png", "rb") as img:
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "system",
            "content": "You are a structural engineer checking ASCE 7 compliance."
        }, {
            "role": "user",
            "content": [
                {"type": "text", "text": "Does this design meet ASCE 7 requirements?"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                {"type": "text", "text": f"Requirements: {rfp_requirements}"}
            ]
        }]
    )

# Automated site inspection
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Identify safety violations in this construction site photo"},
            {"type": "image_url", "image_url": {"url": drone_photo_url}}
        ]
    }]
)
```

---

## 📝 Expanded Sections (Existing Chapters)

### Chapter 22: Advanced RAG Patterns (EXPANDED)
**New Section Added**: **Part 5: Production RAG - Incremental Updates** (+30 minutes)

**What's New**:
- Embedding staleness problem explained
- Hash-based change detection implementation
- Incremental indexing vs. full re-index
- Time-based, event-based, and hybrid refresh strategies
- Efficient upsert operations
- CE application: Evolving projects with new drawings

**Code Example**:
```python
class IncrementalRAG:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.doc_hashes = {}  # id -> hash mapping

    def add_documents(self, documents):
        # Only embed changed documents
        changed_docs = self.detect_changes(documents)
        if not changed_docs:
            return "No changes detected"

        embeddings = self.embed(changed_docs)
        self.vector_store.upsert(embeddings)
        self._update_hashes(changed_docs)

    def detect_changes(self, documents):
        changed = []
        for doc in documents:
            current_hash = self._hash(doc.content)
            if current_hash != self.doc_hashes.get(doc.id):
                changed.append(doc)
        return changed
```

---

### Chapter 47: Agent Communication Protocols (EXPANDED)
**New Sections Added**: **Parts 3-6: Advanced Communication Patterns** (+45 minutes)

**What's New**:
- Part 3: Advanced Communication Patterns
- Part 4: Blackboard Pattern (shared knowledge space)
- Part 5: Pub/Sub for Agents
- Part 6: Error Handling in Communication

**Key Concepts**: Message passing (direct, queued), blackboard pattern, pub/sub, synchronous vs. asynchronous communication, dead letter queues, message ordering

**Code Example**:
```python
class Blackboard:
    def __init__(self):
        self.data = {}
        self.subscribers = defaultdict(list)

    def write(self, key, value):
        self.data[key] = value
        self._notify(key, value)

    def subscribe(self, key, callback):
        self.subscribers[key].append(callback)

# Agent 1 writes
blackboard.write("extracted_entities", entities)

# Agent 2 reacts automatically
blackboard.subscribe("extracted_entities", lambda e: process(e))
```

---

### Chapter 53: Compliance Review Agent (EXPANDED)
**New Sections Added**: **Parts 6-7: RFI & Code Compliance Automation** (+1.5 hours)

**What's New**:
- Part 6: Automated RFI Generation
  - Cross-reference contracts, drawings, specs
  - Detect discrepancies automatically
  - Generate RFI drafts for clarification

- Part 7: Automated Code Compliance Checking
  - Ingest building codes (ASCE, ACI, OSHA) into RAG
  - Query relevant code sections
  - Compare design vs. code requirements
  - Flag non-compliances

**Code Example**:
```python
class RFIGenerator:
    def generate_rfis(self, contract, drawings):
        requirements = self.extract_requirements(contract)
        design = self.parse_drawings(drawings)
        discrepancies = self.compare(requirements, design)
        return [self.draft_rfi(d) for d in discrepancies]

class CodeComplianceChecker:
    def check_compliance(self, design, code_name="ACI318"):
        code_db = self.load_code(code_name)
        requirements = code_db.query(design.category)
        violations = self.verify(design, requirements)
        return ComplianceReport(violations=violations)
```

---

### Chapter 54: Complete Civil Engineering Document System (EXPANDED)
**New Sections Added**: **Parts 6-7: CAD Integration & Schedule Validation** (+1 hour)

**What's New**:
- Part 6: CAD Software Integration
  - Integrate with AutoCAD/Revit APIs
  - AI generates CAD commands from natural language
  - Automate drawing sheet generation

- Part 7: Schedule Validation
  - Extract schedules from multiple documents
  - Cross-check schedule of rates vs. variation orders
  - Flag discrepancies automatically

**Code Example**:
```python
class CADAutomation:
    def generate_drawing_sheet(self, description):
        # LLM converts natural language to CAD commands
        cad_commands = llm.complete(f"Convert to CAD: {description}")
        self.cad_api.execute_commands(cad_commands)
        return "drawing_sheet_001.dwg"

class ScheduleValidator:
    def validate(self, schedule_of_rates, variation_order):
        rates = self.extract_table(schedule_of_rates)
        variations = self.extract_table(variation_order)
        discrepancies = self.compare(rates, variations)
        return ValidationReport(discrepancies)
```

---

## 📊 Updated Statistics

### Property-Based Testing Coverage (Updated)

| Property | Description | Chapters |
|----------|-------------|----------|
| ... | (P1-P79 unchanged) | ... |
| **P80** | Graph completeness | 38A |
| **P81** | Relationship accuracy | 38A |
| **P82** | Trace completeness | 40B |
| **P83** | Latency measurement accuracy | 40B |
| **P84** | Correlation ID propagation | 40C |
| **P85** | Cost attribution accuracy | 40C |
| **P86** | Handoff accuracy | 48A |
| **P87** | Agent reachability | 48A |
| **P88** | Image parsing accuracy | 52A |
| **P89** | Compliance detection from visuals | 52A |

**Total Properties**: 89 (was 79)

---

## 🔄 Planned Structural Reorganization (Future v6.2)

**Note**: The following reorganization is RECOMMENDED but NOT YET IMPLEMENTED in v6.1. This will be addressed in a future update (v6.2).

### Current Structure (v6.1)
```
Phase 6: LangGraph (Ch 31-34)
Phase 9: Multi-Agent (Ch 43-48, 48A)
```

### Proposed Structure (v6.2)
```
Phase 6: Agent Orchestration Foundations (Ch 31-34)
  - Ch 31: Multi-agent Fundamentals (from Ch 43)
  - Ch 32: CrewAI (from Ch 44)
  - Ch 33: AutoGen (from Ch 45)
  - Ch 34: Supervisor Pattern (from Ch 46)

Phase 9: Advanced Orchestration with LangGraph (Ch 43-48)
  - Ch 43: LangGraph State Machines (from Ch 31)
  - Ch 44: LangGraph Conditional Routing (from Ch 32)
  - Ch 45: LangGraph Human-in-the-Loop (from Ch 33)
  - Ch 46: LangGraph Persistent State (from Ch 34)
  - Ch 47: Agent Communication Protocols (existing, expanded)
  - Ch 48: Debugging Multi-Agent Systems (existing)
  - Ch 48A: Swarm Pattern (new)
```

**Rationale**: Students should learn multi-agent concepts with easier frameworks (CrewAI, AutoGen) BEFORE graduating to production-grade LangGraph. This improves pedagogical flow.

**Status**: Deferred to v6.2 to minimize disruption. Can be implemented after initial v6.1 adoption.

---

## 🎯 Implementation Priority

### Priority 1: Critical Additions (Weeks 1-2) ⭐⭐⭐⭐⭐
1. Chapter 38A: GraphRAG & Knowledge Graphs
2. Chapter 40A-40C: Observability mini-series
3. Chapter 22 expansion: Incremental indexing

### Priority 2: Structural Improvements (Weeks 3-4) ⭐⭐⭐⭐
1. Chapter 47 expansion: Agent communication
2. Chapter 48A: Swarm Pattern

### Priority 3: CE-Specific Features (Weeks 5-6) ⭐⭐⭐⭐
1. Chapter 52A: Multimodal AI for CE
2. Chapter 53 expansion: RFI & code compliance
3. Chapter 54 expansion: CAD & schedule validation

---

## 📚 References

All enhancements are based on comprehensive industry research documented in:
- `CURRICULUM-ENHANCEMENT-ANALYSIS-2026.md` (comprehensive gap analysis)
- `ENHANCEMENT-IMPLEMENTATION-PLAN.md` (step-by-step implementation)

**Research Sources**: 15+ industry sources including State of Agents 2026, LLM Observability surveys, GraphRAG implementations, CE AI applications, and multi-agent framework comparisons.

---

## ✅ Approval Status

**Status**: ✅ **Ready for Implementation**
**Approved By**: Ahmed (pending)
**Date**: 2026-01-18

**Next Steps**:
1. Review this enhancement document
2. Approve implementation plan
3. Begin Phase 1 (Critical Additions)

---

**This enhancement transforms the curriculum from "strong foundation" to "definitive 2026 AI Engineering course."**
