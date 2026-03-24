# Pragmatic GenAI Engineer Curriculum - Layer 1 Overview

**Version:** 2.0 — ⚠️ **ARCHIVED March 8, 2026**
**Status:** ❌ **SUPERSEDED by LAYER1-FINAL**
**Last Updated:** March 8, 2026
**Target Role:** AI/GenAI Engineer (RAG, Agents, LLM Applications)
**Philosophy:** Ship working systems, learn through building, embrace real friction

---

## 🚨 IMPORTANT NOTICE

**This curriculum is ARCHIVED. Use LAYER1-FINAL for new study.**

**→ Start Here:** [`../../LAYER1-FINAL/README.md`](../../LAYER1-FINAL/README.md)

**Why Archived?**
- ❌ SQL placement wrong (Week 26 vs. Week 1)
- ❌ Testing bolted on late (Week 21 vs. Week 2)
- ❌ Security bolted on late (Week 23 vs. threaded)
- ❌ 32 weeks vs. 28 weeks (LAYER1-FINAL is market-calibrated)
- ❌ Missing COST-LOG, FAILURE-LOG, Git collaboration

**See:** [../ALIGNMENT-REVIEW.md](../ALIGNMENT-REVIEW.md) for migration analysis.

---

## ✅ USE LAYER1-FINAL INSTEAD

| Document | Purpose | Link |
|----------|---------|------|
| **LAYER1-FINAL README** | Main curriculum (28 weeks, SQL Week 1) | [`../../LAYER1-FINAL/README.md`](../../LAYER1-FINAL/README.md) |
| **Guide for AI Assistants** | Teaching methodology | [`../../LAYER1-FINAL/GUIDE-FOR-AI-ASSISTANTS.md`](../../LAYER1-FINAL/GUIDE-FOR-AI-ASSISTANTS.md) |
| **Checkpoint Rubrics** | Phase verification | [`../../LAYER1-FINAL/CHECKPOINT-RUBRICS.md`](../../LAYER1-FINAL/CHECKPOINT-RUBRICS.md) |
| **Progress Tracker** | Student tracking | [`../../LAYER1-FINAL/PROGRESS-TRACKER.md`](../../LAYER1-FINAL/PROGRESS-TRACKER.md) |
| **Cost Log** | API cost tracking | [`../../LAYER1-FINAL/COST-LOG.md`](../../LAYER1-FINAL/COST-LOG.md) |
| **Failure Log** | Weekly debugging | [`../../LAYER1-FINAL/FAILURE-LOG.md`](../../LAYER1-FINAL/FAILURE-LOG.md) |
| **Day 00 Diagnostic** | Python assessment | [`../../LAYER1-FINAL/DAY-00-DIAGNOSTIC.md`](../../LAYER1-FINAL/DAY-00-DIAGNOSTIC.md) |

---

## 📚 LEGACY CONTENT (Reference Only)

This document is preserved for reference. The following components **live on in LAYER1-FINAL**:

1. ✅ Teaching Methodology — 5-level teaching ladder
2. ✅ Checkpoint System — 4 checkpoint types
3. ✅ Guided Discovery Philosophy — TODOs over solutions
4. ✅ Flex Weeks Concept — Adapted to 2 weeks
5. ✅ Weekly Structure — 20 hours/week

---

## What Changed from Original Layer 1

### Original Approach (40-day plan)
- 40 sequential days with daily mini-projects
- Theory-first with "Prime the Pump" conceptual grounding
- Comprehensive coverage of all AI engineering topics
- Linear progression through concepts

### Modified Approach (32-week plan)
- **Week-based structure** with flex weeks for real learning friction
- **Project-first** with just-in-time theory
- **Focused on GenAI Engineer role** (removed ML/research topics)
- **Guided learning** with TODOs, not complete solutions
- **Built-in slack** for rabbit holes and concept gaps

---

## Core Modifications

### 1. Timeline Restructure
**Original:** 40 days × 4-6 hours = 160-240 hours  
**Modified:** 32 weeks × 20 hours/week = 640 hours (with 4 flex weeks)

**Rationale:** Real learning has setbacks. Week-based structure allows for:
- Deeper understanding per topic
- Time to debug and fix broken code
- Portfolio-quality projects, not just working demos
- Breathing room for life events

### 2. Project Architecture
**Original:** Daily mini-projects with complete code examples  
**Modified:** Scaffolded projects with TODOs and guided discovery

**Key Changes:**
- Starter code with clear TODOs
- Progressive hints (try 30min → hint 1 → try more → hint 2)
- Learning checkpoints ("Explain before proceeding")
- Design-first approach (draw architecture before coding)

### 3. Teaching Methodology
**Original:** "Build first, understand after"  
**Modified:** "Build with guidance, understand through explaining"

**Implementation:**
- AI assistants explain concepts, don't write code
- Students must articulate design decisions
- Evaluation includes "can you explain it?" criteria
- Documentation is part of every project

### 4. Scope Reduction
**Removed from Layer 1:**
- Classical ML (sklearn, feature engineering)
- Deep learning training (PyTorch from scratch)
- MLOps heavy tooling (Kubeflow, SageMaker)
- Data engineering (Spark, Airflow)
- GraphRAG depth (survey only)

**Kept and Enhanced:**
- LLM APIs and structured outputs
- RAG (chunking, retrieval, evaluation)
- Agents (tool calling, workflows, state management)
- Production concerns (FastAPI, Docker, monitoring)
- Security and testing

---

## Curriculum Mapping: Original Days → Modified Weeks

| Original Days | Topic | Modified Weeks | Changes |
|---------------|-------|----------------|---------|
| Day 1 | Hello LLM | Week 3 | Moved after Python foundations |
| Day 2 | Structured Outputs | Week 3 | Combined with first LLM call |
| Days 3-5 | Embeddings + RAG | Weeks 7-8 | Expanded with more practice time |
| Day 6 | FastAPI | Week 5 | Moved earlier for quick deployment |
| Days 7-10 | Advanced RAG | Weeks 9-11 | Expanded with evaluation focus |
| Days 11-15 | LangChain | Week 14 | Compressed to essentials |
| Days 16-20 | Agents | Weeks 15-17 | Expanded with more guardrails |
| Days 21-25 | LangGraph | Week 17 | Integrated with agents |
| Days 26-30 | Production | Weeks 21-26 | Distributed throughout |
| Days 31-35 | Advanced Topics | Weeks 28-31 | Made optional/survey |
| Days 36-40 | Capstone | Weeks 12, 19, 32 | Three flagships instead of one |

---

## Three-Tier Project Structure

### Tier 1: Mini-Projects (Weeks 3-11)
**Purpose:** Learn specific skills in isolation  
**Duration:** 1 week each  
**Deliverable:** Working component with tests

**Examples:**
- Multi-Provider LLM Client (Week 4)
- Document Indexer (Week 9)
- RAG Evaluation Harness (Week 11)

**Teaching Approach:**
- Scaffolded starter code with TODOs
- Progressive hints (3 levels)
- Learning checkpoints
- Must explain implementation

### Tier 2: Flagship Projects (Weeks 12, 19, 32)
**Purpose:** Integrate multiple skills into production system  
**Duration:** 2-4 weeks each  
**Deliverable:** Deployed system with documentation

**The Three Flagships:**
1. **Production RAG System** (Week 12)
   - Full ingestion → retrieval → generation pipeline
   - Evaluation harness
   - FastAPI + Docker deployment
   
2. **Controlled Agentic Workflow** (Week 19)
   - Tool calling + state management
   - Human-in-the-loop
   - Observability and guardrails
   
3. **Your Choice** (Week 32)
   - Apply everything to novel problem
   - Demonstrate mastery

**Teaching Approach:**
- 4-phase structure: Design → Implement → Harden → Document
- Architecture-first (draw before coding)
- Learning checkpoints at each milestone
- Required design decisions documentation

### Tier 3: Flex Weeks (Weeks 13, 20, 27, 32+)
**Purpose:** Handle real learning friction  
**Duration:** 1 week each (4 total)  
**Use For:**
- Catching up on incomplete weeks
- Deep-diving into confusing concepts
- Fixing bugs in flagship projects
- Exploring rabbit holes (GraphRAG, fine-tuning)
- Burnout prevention

---

## Weekly Structure

### Monday-Thursday (Build Days)
**4 hours/day breakdown:**
- **Hour 1:** Read/watch concept material (minimum viable understanding)
- **Hour 2:** Implement (copy-paste-modify is OK at first)
- **Hour 3:** Debug + test (make it work)
- **Hour 4:** Document (README, comments, notes)

### Friday (Debug Lab + Reflection)
**4 hours breakdown:**
- **Hours 1-2:** Fix the week's broken things
- **Hour 3:** Write what you learned (blog draft, notes)
- **Hour 4:** Plan next week (what's the ship target?)

### When You Get Stuck (Inevitable)
1. **Timebox:** Spend max 2 hours debugging alone
2. **Ask:** ChatGPT, Claude, or community (Discord, Reddit)
3. **Simplify:** Remove features until it works, then add back
4. **Skip:** Mark as "come back later" and move on
5. **Flex week:** Use buffer weeks to catch up

---

## Learning Checkpoints System

Every project includes mandatory checkpoints where students must demonstrate understanding before proceeding.

### Checkpoint Types

**1. Design Checkpoints (Before Coding)**
- Draw architecture diagram
- Answer design questions
- List 5 potential failure modes
- Justify technology choices

**2. Implementation Checkpoints (During Coding)**
- Explain what each TODO does before implementing
- Describe edge cases being handled
- Justify algorithm/approach choice

**3. Testing Checkpoints (After Coding)**
- Explain what each test validates
- Demonstrate failure cases
- Show before/after metrics

**4. Reflection Checkpoints (After Completion)**
- Walk through code with someone (or rubber duck)
- Explain trade-offs made
- Describe what you'd do differently
- Answer "why" questions

### Example Checkpoint Questions

**For RAG System:**
- [ ] Why did you choose this chunk size?
- [ ] What happens if no documents match the query?
- [ ] How do you prevent hallucinations?
- [ ] What's the bottleneck in your system?
- [ ] How would you scale to 1M documents?

**For Agentic Workflow:**
- [ ] Why workflow control vs autonomous agent?
- [ ] How do you prevent infinite loops?
- [ ] What triggers human review?
- [ ] How do you evaluate agent decisions?
- [ ] What happens if a tool fails?

---

## Teaching Methodology: AI Assistant Guidelines

### What AI Assistants SHOULD Do ✅

**1. Explain Concepts**
```
"Embeddings are vector representations of text that capture semantic 
meaning. Similar concepts have similar vectors, which lets you find 
related documents using distance metrics like cosine similarity."
```

**2. Suggest Approaches**
```
"You could use either fixed-size or semantic chunking. Fixed-size is 
simpler and faster, but semantic chunking respects sentence boundaries 
which often gives better retrieval quality. What's more important for 
your use case: speed or quality?"
```

**3. Debug Errors**
```
"That error means your API key isn't loaded. Check:
1. Is .env file in the same directory?
2. Did you call load_dotenv()?
3. Is the variable name exactly 'OPENAI_API_KEY'?"
```

**4. Ask Guiding Questions**
```
"Why did you choose chunk size 512? What happens if you use 256? 
Have you tested both on your evaluation set?"
```

**5. Provide Examples**
```
"Here's how Chroma's query method works:
results = collection.query(
    query_texts=['your question'],
    n_results=5
)
The results include documents, distances, and metadata."
```

**6. Review Code**
```
"Your error handling looks good, but what happens if ALL providers 
fail? Should you raise an exception or return a default response?"
```

### What AI Assistants Should NOT Do ❌

**1. Write Complete Implementations**
```
❌ Don't give full function bodies for TODOs
✅ Instead: "Think about the steps: 1) Load text, 2) Split into chunks, 
   3) Create embeddings. Try implementing step 1 first."
```

**2. Make Design Decisions**
```
❌ "Use Chroma for your vector store"
✅ "What are your requirements? Chroma is good for local development, 
   Pinecone for production scale, Weaviate for hybrid search."
```

**3. Skip Learning Checkpoints**
```
❌ "Here's the code, move on to the next section"
✅ "Before we continue, can you explain why you chose this chunking 
   strategy? What trade-offs did you consider?"
```

**4. Optimize Prematurely**
```
❌ "You should use async/await and batch processing"
✅ "Get it working first. Once it works, we can profile and optimize 
   if needed."
```

**5. Remove Struggle**
```
❌ Immediately providing solutions when student is stuck
✅ "You've been stuck for 20 minutes. Let's check hint_01. If still 
   stuck after trying that, we'll debug together."
```

---

## Project Evaluation Rubric

### For Each Project (100 points total)

**Implementation (40 points)**
- [ ] Core functionality works (20 pts)
- [ ] Error handling is present (10 pts)
- [ ] Code is readable (5 pts)
- [ ] Tests pass (5 pts)

**Understanding (30 points)**
- [ ] Can explain design decisions (10 pts)
- [ ] Can explain trade-offs (10 pts)
- [ ] Can explain failure modes (5 pts)
- [ ] Can answer "why" questions (5 pts)

**Documentation (20 points)**
- [ ] README is clear (8 pts)
- [ ] Architecture is documented (6 pts)
- [ ] Setup instructions work (4 pts)
- [ ] Demo is recorded (2 pts)

**Production Quality (10 points)**
- [ ] Logging is present (3 pts)
- [ ] Deployment works (3 pts)
- [ ] Monitoring exists (2 pts)
- [ ] Security basics covered (2 pts)

**Passing Grade:** 70+ points  
**Portfolio-Ready:** 85+ points

---

## Success Metrics (Not Perfection Metrics)

### By Week 6
- [ ] Deployed LLM API that someone else can use
- [ ] Can explain: prompt engineering, structured outputs, error handling
- [ ] First public demo or blog post

### By Week 13 (After Flagship 1)
- [ ] Production RAG system with evaluation
- [ ] Can explain: embeddings, chunking, retrieval strategies, citations
- [ ] GitHub repo with clear README and architecture diagram

### By Week 20 (After Flagship 2)
- [ ] Agentic workflow with human oversight
- [ ] Can explain: tool calling, state management, ReAct pattern, guardrails
- [ ] Demo video showing system in action

### By Week 27 (After Production Phase)
- [ ] Both flagships have tests, monitoring, CI/CD
- [ ] Can explain: observability, security, performance optimization
- [ ] Technical blog post explaining trade-offs

### By Week 32 (Completion)
- [ ] 2-3 portfolio projects with demos
- [ ] Technical blog posts explaining design decisions
- [ ] Can pass GenAI Engineer interviews
- [ ] Public GitHub profile showing consistent commits

---

## Integration with Existing Layer 1

### Files to Keep (Reference Material)
- `docs/DAILY-CURRICULUM-PLAN-V4.md` - Original 40-day plan
- `docs/AI-Engineer-Interview-100-Questions-Answers.md` - Interview prep
- `guides/ACTION-FIRST-GUIDE.md` - Teaching philosophy
- `guides/WRITING-STYLE-GUIDE.md` - Documentation standards
- `day-01-hello-llm/` - Example of complete day structure

### Files to Add (This Modification)
- `docs/PRAGMATIC-CURRICULUM-OVERVIEW.md` - This file
- `docs/WEEK-BY-WEEK-ROADMAP.md` - Detailed weekly breakdown
- `docs/PROJECT-SCAFFOLDING-GUIDE.md` - How to create guided projects
- `docs/TEACHING-METHODOLOGY.md` - AI assistant guidelines
- `guides/CHECKPOINT-SYSTEM.md` - Learning verification system
- `guides/FLEX-WEEK-GUIDE.md` - How to use buffer weeks

### How to Use Both
1. **Start with Modified Curriculum** (this document) for overall structure
2. **Reference Original Days** for specific technical content
3. **Use Original Mini-Projects** as inspiration for scaffolded versions
4. **Keep Interview Questions** for spaced repetition
5. **Follow Original Writing Style** for any new content

---

## Migration Path for Existing Students

### If You're on Day 1-10 of Original
→ Switch to Week 1-6 of Modified (Python + LLM Foundations)

### If You're on Day 11-20 of Original
→ Switch to Week 7-13 of Modified (RAG Core + Flagship 1)

### If You're on Day 21-30 of Original
→ Switch to Week 14-20 of Modified (Agents + Flagship 2)

### If You're on Day 31-40 of Original
→ Switch to Week 21-32 of Modified (Production + Advanced)

**Key Difference:** Take more time per topic. Build portfolio-quality projects, not just working demos.

---

## FAQ

**Q: Why 32 weeks instead of 40 days?**  
A: Real learning has friction. 40 days assumes perfect execution. 32 weeks allows for debugging, concept gaps, and life events.

**Q: Can I go faster?**  
A: Yes! Flex weeks are optional. If you're moving quickly, use them for advanced topics or start job hunting.

**Q: What if I fall behind?**  
A: Use flex weeks to catch up. Focus on flagship projects over mini-projects. Ship working systems, not perfect code.

**Q: Do I need to do all mini-projects?**  
A: No. Mini-projects teach specific skills. If you already know a skill, skip to the flagship projects.

**Q: Can I use this with the original Layer 1?**  
A: Yes! Use this for structure and pacing. Use original for technical content and examples.

**Q: What about Layer 2 curriculum?**  
A: Layer 2 (54 chapters) is more comprehensive. This modified Layer 1 is faster and more focused on GenAI Engineer role.

**Q: Is this enough to get a job?**  
A: If you complete 2 flagship projects with documentation and can explain your decisions, yes. Add SQL basics and you're competitive.

---

## Next Steps

1. **Read:** `WEEK-BY-WEEK-ROADMAP.md` for detailed weekly breakdown
2. **Read:** `PROJECT-SCAFFOLDING-GUIDE.md` to understand project structure
3. **Read:** `TEACHING-METHODOLOGY.md` for AI assistant guidelines
4. **Start:** Week 1 - Python Sprint (or Week 3 if Python-ready)
5. **Ship:** First working system by Week 6

**Remember:** Perfect is the enemy of shipped. Working code > perfect understanding.

Let's build. 🚀
