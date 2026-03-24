# Curriculum Implementation Roadmap

**Next Steps for AI Engineering Curriculum Evolution**

**Document Owner**: Ahmed
**Last Updated**: February 10, 2026 (v7.0 update)
**Status**: Active Planning
**Purpose**: Clear action plan for completing curriculum enhancements

---

## 📍 Quick Navigation

**Current Work (v7.0)**:

- [🚀 v7.0 Critical Additions](#-v70-critical-additions-current-priority) ← **START HERE**
- [📊 Current Status](#-current-status)
- [🎯 Next Steps After v7.0](#-next-steps-after-v70)

**Planning & Reference**:

- [🎯 Vision & Goals](#-vision--goals)
- [📋 Phase 2-10 Planning](#-phase-2-10-planning-future-sprints)
- [📚 Historical Reference](#-historical-reference-pre-v70)

---

## ⚠️ Version Note

**Current Version**: v7.0 (February 2026)

**For v7.0 Implementation**: See [v7.0 Critical Additions](#-v70-critical-additions-current-priority) section below for **IMMEDIATE NEXT STEPS**

**Historical Context**: Pre-v7.0 sprint plans are preserved in [Historical Reference](#-historical-reference-pre-v70) section at bottom

---

## 🎯 Vision & Goals

### Overall Vision

Transform the AI Engineering curriculum from good to exceptional by implementing research-backed pedagogical patterns while maintaining beginner accessibility and project diversity.

### Success Definition

- ✅ 95%+ alignment with research best practices
- ✅ Beginner-friendly progression (LLM magic in 15 minutes)
- ✅ 50+ diverse mini-projects across all phases
- ✅ 23 pedagogical principles applied consistently
- ✅ 80%+ quality checklist scores for all chapters

---

## 📊 Current Status

### Completed ✅

**Foundation Work**:

- [x] Analyzed 100+ open-source AI engineering resources
- [x] Identified critical curriculum gaps
- [x] Documented 23 pedagogical principles
- [x] Created MASTER-CHAPTER-TEMPLATE-V2.md (v2.2)
- [x] Enhanced WRITING-STYLE-GUIDE.md (485 lines)
- [x] Enhanced LANGUAGE-EXPANSION-GUIDE.md (1,343 lines)
- [x] Created comprehensive QUALITY-CHECKLIST.md

**Phase 1 Work**:

- [x] Designed beginner-friendly Phase 1 structure (10 chapters)
- [x] Wrote Chapter 7: "Your First LLM Call" (~25,000 words)
- [x] Applied 17 of 23 pedagogical principles to Chapter 7
- [x] Created verification scripts for Chapter 7

**Documentation**:

- [x] Created CURRICULUM-EVOLUTION-DECISIONS.md (consolidated guidelines)
- [x] Created this roadmap (CURRICULUM-IMPLEMENTATION-ROADMAP.md)

---

### In Progress 🔄

**File Reorganization**:

- [x] Archive outdated analysis files ✅
- [x] Reorganize \_bmad-output/ directory structure ✅
- [x] Update \_bmad-output/README.md ✅

**v7.0 Roadmap Updates**:

- [x] Update roadmap-v6.md → v7.0 ✅
- [x] Add Chapter 6D and 12A entries ✅
- [x] Update CURRICULUM-EVOLUTION-DECISIONS.md ✅
- [x] Update PHASE-0-TOPICS-ANALYSIS.md ✅

---

## 🚀 v7.0 Critical Additions (CURRENT PRIORITY)

> **⚡ IMMEDIATE ACTION REQUIRED**: These two chapters are essential foundations that must be written before proceeding with other curriculum work.

### Overview

v7.0 adds two critical foundation chapters that were missing from the curriculum:

- **Chapter 6D: File Handling & Path Management** (Phase 0) - Essential for all AI projects
- **Chapter 12A: Asyncio Fundamentals** (Phase 1) - **CRITICAL** for streaming, concurrent APIs, production apps

### Implementation Tasks

#### Task 1: Create Chapter 6D - File Handling & Path Management

**Time Estimate**: 4-5 hours
**Difficulty**: ⭐
**Location**: `curriculum/chapters/phase-0-foundations/chapter-06D-file-handling.md`

**Requirements**:

- [ ] Follow ACTION-FIRST-DEEP-DIVE-GUIDE.md pattern
- [ ] Apply 17+ of 23 pedagogical principles
- [ ] Quick success: Read a file and print contents (5 minutes)
- [ ] Comprehensive deep dive after success
- [ ] Time allocation: 1.5 hours of content

**Content Outline**:

1. **Phase 1: The Hook (0-8 min)**
   - Minimal intro: "You'll read a file in 3 lines of code"
   - Quick code: `with open('prompt.txt') as f: print(f.read())`
   - Success celebration

2. **Phase 2: Deep Dive (8-90 min)**
   - Reading files (text, CSV, JSON)
   - Writing files safely
   - File modes (r, w, a, r+, w+)
   - pathlib vs os.path
   - File context managers
   - Binary files
   - File iteration (line by line)
   - Directory operations
   - Error handling for file operations
   - Loading prompts from files
   - Saving LLM outputs

**Verification**:

- [x] Create verification script ✅
- [x] Test verification script (8/8 tests passed) ✅
- [ ] Test all code examples
- [ ] Run quality checklist
- [ ] Verify 17+ principles applied

---

#### Task 2: Create Chapter 12A - Asyncio Fundamentals

**Time Estimate**: 5-6 hours
**Difficulty**: ⭐⭐
**Location**: `curriculum/chapters/phase-1-llm-fundamentals/chapter-12A-asyncio-fundamentals.md`

**Requirements**:

- [ ] Follow ACTION-FIRST-DEEP-DIVE-GUIDE.md pattern
- [ ] Apply 17+ of 23 pedagogical principles
- [ ] Quick success: Concurrent API calls with asyncio.gather() (5-8 minutes)
- [ ] Comprehensive deep dive after success
- [ ] Time allocation: 2 hours of content
- [ ] **CRITICAL**: Must exist before students reach embeddings/streaming chapters

**Content Outline**:

1. **Phase 1: The Hook (0-8 min)**
   - Minimal intro: "You'll make 3 LLM calls in parallel"
   - Quick code: `await asyncio.gather(call1(), call2(), call3())`
   - Success: See all 3 responses arrive concurrently
   - "Now let's understand what just happened..."

2. **Phase 2: Deep Dive (8-120 min)**
   - async/await syntax explained
   - Coroutines vs regular functions
   - Asyncio event loop basics (not deep internals)
   - asyncio.gather() for parallel execution
   - async with context managers
   - Error handling in async code
   - When to use async vs sync
   - Brief GIL explanation (1-2 paragraphs)
   - Practical: Concurrent API calls to multiple LLMs
   - Common pitfalls and how to avoid them

**Why This Matters** (include in chapter):

- Modern AI applications are async
- Streaming LLM responses require async
- Concurrent API calls for efficiency
- Real-time chatbots need async
- Production scalability depends on async
- Every major AI framework uses async (FastAPI, LangChain, LlamaIndex)

**Verification**:

- [x] Create verification script with async tests ✅
- [x] Test verification script (8/8 tests passed) ✅
- [ ] Test all code examples (sync and async versions)
- [ ] Run quality checklist
- [ ] Verify 17+ principles applied
- [ ] Ensure error handling examples work

---

### Success Criteria for v7.0

**Chapter 6D Complete When**:

- ✅ Students can read and write files in 5 minutes
- ✅ Comprehensive coverage of all file I/O patterns
- ✅ All code examples tested and working
- ✅ 17+ pedagogical principles applied
- ✅ Quality checklist score 80%+

**Chapter 12A Complete When**:

- ✅ Students can make concurrent API calls in 8 minutes
- ✅ Deep understanding of async/await patterns
- ✅ Clear explanation of when to use async vs sync
- ✅ All code examples tested and working
- ✅ 17+ pedagogical principles applied
- ✅ Quality checklist score 80%+

**v7.0 Complete When**:

- ✅ Both chapters written and verified
- ✅ Roadmap updated to v7.0 ✅ (DONE)
- ✅ CURRICULUM-EVOLUTION-DECISIONS.md updated ✅ (DONE)
- ✅ All guiding files reference v7.0
- ✅ Verification scripts created and passing
- ✅ Git commit with clear v7.0 tag

### Verification Scripts Status

**Script 1: `curriculum/verification/verify_chapter_06D.py`** ✅ COMPLETE

Tests implemented:

- ✅ Basic file reading with context managers
- ✅ File writing operations
- ✅ CSV file operations (reading and writing)
- ✅ JSON file operations (reading and writing)
- ✅ pathlib operations (cross-platform paths)
- ✅ Error handling for missing files
- ✅ Directory operations (creation, listing, glob patterns)
- ✅ File iteration (line by line reading)

**Test Results**: 8/8 tests passed ✅

**Script 2: `curriculum/verification/verify_chapter_12A.py`** ✅ COMPLETE

Tests implemented:

- ✅ Basic async/await syntax
- ✅ asyncio.gather() for concurrent execution
- ✅ Async context managers (async with)
- ✅ Error handling in async code
- ✅ Async vs sync performance comparison
- ✅ Coroutines vs regular functions
- ✅ Concurrent API calls (simulated)
- ✅ Task cancellation

**Test Results**: 8/8 tests passed ✅

- Test async/await syntax
- Test asyncio.gather() for concurrent calls
- Test async context managers
- Test error handling in async code
- Test async vs sync performance comparison

---

## 🎯 Next Steps After v7.0

Once Chapter 6D and 12A are complete, proceed with:

### Immediate (Next 2-4 weeks)

**1. Write Remaining Phase 1 Chapters (Ch 8-12, 13-16)**

- Chapter 8: Local Models with Ollama
- Chapter 9: System Prompts & Personalities
- Chapter 10: Multi-Provider Architecture
- Chapter 11-12: Prompt Engineering (Foundations & Advanced)
- Chapter 13-16: Streaming, Structured Output, Error Handling, Cost Optimization

**2. Create Phase 1 Integration Project**

- Multi-provider chatbot
- Streaming + structured output
- Error handling + cost tracking
- Brings together Ch 7-16

**3. Phase 1 Completion Report**

- Summary of all chapters
- Quality metrics achieved
- Lessons learned
- Recommendations for Phase 2+

### Medium-Term (1-3 months)

**Phase 2-10 Enhancements** (see [Phase 2-10 Planning](#-phase-2-10-planning-future-sprints) below):

- Add "Build from Scratch" chapters before framework chapters
- Add fine-tuning chapters (Phase 7)
- Add MCP (Model Context Protocol) chapters
- Add deployment & production chapters (Phase 10)
- Transform Phase 3-10 chapters with diverse mini-projects

---

---

## � Historical Reference (Pre-v7.0)

> **Note**: The sprint plans below reflect the earlier curriculum structure (pre-v7.0). They are preserved for historical context but have been superseded by the v7.0 approach documented above. The v7.0 structure prioritizes writing Chapter 6D and 12A first, then proceeding with remaining Phase 1 chapters.

### Sprint 1: File Cleanup & Phase 1 Foundations (Week 1)

**Duration**: 5-8 hours
**Goal**: Clean workspace, complete 3 chapters

#### Tasks

**Cleanup (2 hours)**:

- [ ] Archive curriculum-transformation-analysis.md → \_bmad-output/archive/outdated-analysis/
- [ ] Archive curriculum-diversity-transformation.md → \_bmad-output/archive/outdated-analysis/
- [ ] Create \_bmad-output/active/ directory
- [ ] Move curriculum-subjects-and-projects-analysis.md → active/
- [ ] Move phase-1-restructure-plan.md → active/
- [ ] Create \_bmad-output/archive/sessions/ directory
- [ ] Move all SESSION-\*.md files → archive/sessions/
- [ ] Create \_bmad-output/archive/enhancements/ directory
- [ ] Move all chapter-_-enhancement-_.md → archive/enhancements/
- [ ] Update \_bmad-output/README.md with new structure
- [ ] Delete EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md (content in guides)
- [ ] Delete EDUCATIONAL-ENHANCEMENT-CONSOLIDATION-2026-01-20.md (session notes)
- [ ] Delete CHAPTER-ENHANCEMENT-GUIDE-UNIVERSAL.md (overlaps with template)

**Chapter Writing (6 hours)**:

- [ ] Write Chapter 8: Local Models with Ollama (2 hours)
  - Llama 3, Mistral, Phi models
  - Installation, basic usage
  - Comparison with cloud APIs
  - Free experimentation benefits
  - Apply 17+ pedagogical principles

- [ ] Write Chapter 9: System Prompts & Personalities (2 hours)
  - Role assignment patterns
  - Tone and style control
  - Building AI personas
  - Apply 17+ pedagogical principles

- [ ] Write Chapter 10: Multi-Provider Architecture (2 hours)
  - Abstract provider interface
  - OpenAI, Anthropic, Ollama support
  - Provider switching patterns
  - Apply 17+ pedagogical principles

**Deliverables**:

- Clean, organized file structure
- 3 new chapters (8-10) complete
- Verification scripts for each

---

### Sprint 2: Prompt Engineering Deep Dive (Week 2)

**Duration**: 5-6 hours
**Goal**: Complete prompt engineering chapters with depth

#### Tasks

- [ ] Write Chapter 11: Prompt Engineering Foundations (2 hours)
  - Zero-shot, one-shot, few-shot learning
  - Instruction clarity patterns
  - Role-based prompting
  - Prompt templates and variables
  - Apply 17+ pedagogical principles

- [ ] Write Chapter 12: Advanced Prompt Engineering (2.5 hours)
  - Chain-of-thought reasoning
  - ReAct (Reasoning + Acting)
  - Self-consistency
  - Tree-of-thought
  - Prompt optimization strategies
  - Apply 17+ pedagogical principles

- [ ] Create prompt engineering playground project (0.5 hour)
  - Interactive Jupyter notebook
  - Test different techniques
  - Compare results

**Deliverables**:

- 2 advanced prompt engineering chapters
- Interactive playground project
- Verification scripts

---

### Sprint 3: Production Patterns (Week 3)

**Duration**: 5-6 hours
**Goal**: Complete streaming, structured output, error handling

#### Tasks

- [ ] Write Chapter 13: Streaming Responses (1.5 hours)
  - Async/await patterns with LLMs
  - Token-by-token streaming
  - Server-Sent Events (SSE)
  - User experience considerations
  - Apply 17+ pedagogical principles

- [ ] Write Chapter 14: Structured Output (2 hours)
  - JSON mode
  - Pydantic model integration
  - Function calling
  - Structured data extraction
  - Apply 17+ pedagogical principles

- [ ] Write Chapter 15: Error Handling & Retries (2 hours)
  - Rate limiting strategies
  - Exponential backoff
  - Timeout handling
  - Circuit breaker pattern
  - Graceful degradation
  - Apply 17+ pedagogical principles

**Deliverables**:

- 3 production-focused chapters
- Complete error handling library
- Verification scripts

---

### Sprint 4: Cost Optimization & Phase 1 Wrap-Up (Week 4)

**Duration**: 4-6 hours
**Goal**: Complete Phase 1, update roadmap

#### Tasks

- [ ] Write Chapter 16: Token Counting & Cost Optimization (1.5 hours)
  - tiktoken library usage
  - Cost calculation patterns
  - Caching strategies (prompt caching, response caching)
  - Model selection for cost/quality
  - Monitoring and budgeting
  - Apply 17+ pedagogical principles

- [ ] Create Phase 1 integration project (1 hour)
  - Multi-provider chatbot
  - Streaming + structured output
  - Error handling + cost tracking
  - Brings together Ch 7-16

- [ ] Update roadmap-v6.md → roadmap-v7.0.md (1 hour)
  - Incorporate Phase 1 changes
  - Update chapter numbers
  - Update time estimates
  - Add new topics identified in research

- [ ] Update PROJECT-THREAD.md (0.5 hour)
  - Document Phase 1 component dependencies
  - Show evolution from simple to complex

- [ ] Create Phase 1 Completion Report (1 hour)
  - Summary of all chapters
  - Quality metrics achieved
  - Lessons learned
  - Next phase recommendations

**Deliverables**:

- Chapter 16 complete
- Phase 1 integration project
- Updated roadmap v7.0
- Phase 1 completion report

---

## 📋 Phase 2-10 Planning (Future Sprints)

### Phase 2: Embeddings & Vector Search

**Status**: Keep current structure, add enhancements

**Planned Additions**:

- [ ] Add visualization project (t-SNE, PCA)
- [ ] Add semantic search comparison project
- [ ] Enhance with diverse mini-projects

**Timeline**: Week 5-6

---

### Phase 3: RAG Fundamentals

**Status**: Needs "build from scratch" chapter

**Planned Additions**:

- [ ] Chapter 17: RAG from Scratch (NEW)
  - Simple retrieval without frameworks
  - Basic chunking and similarity search
  - Understand the fundamentals

- [ ] Chapter 18: Advanced Chunking Strategies
  - Keep existing, enhance

- [ ] Add diverse RAG projects:
  - Personal knowledge base
  - Document Q&A system
  - Code documentation search

**Timeline**: Week 7-9

---

### Phase 4-6: Advanced RAG & Frameworks

**Status**: Good foundation, add diversity

**Planned Additions**:

- [ ] Add "Agent from Scratch" before LangGraph
- [ ] Add MCP (Model Context Protocol) expansion
- [ ] Add diverse agent projects

**Timeline**: Week 10-14

---

### Phase 7: Fine-Tuning (NEW PHASE)

**Status**: Missing entirely - HIGH PRIORITY

**Chapters to Add**:

- [ ] Chapter 37: Introduction to Fine-Tuning
  - When and why to fine-tune
  - Data preparation
  - Base model selection

- [ ] Chapter 38: Fine-Tuning with Unsloth
  - LoRA and QLoRA
  - Parameter-efficient fine-tuning
  - Free Colab notebooks

- [ ] Chapter 39: Custom Dataset Creation
  - Data collection strategies
  - Quality over quantity
  - Format and validation

- [ ] Chapter 40: Fine-Tuning Evaluation
  - Metrics and benchmarks
  - Comparing base vs. fine-tuned
  - Iteration strategies

- [ ] Chapter 41: Deployment of Fine-Tuned Models
  - Hosting options
  - Inference optimization
  - Cost considerations

**Timeline**: Week 15-18

---

### Phase 8: Guardrails & Safety (ENHANCED)

**Status**: Add new chapters

**Planned Additions**:

- [ ] Guardrails AI integration
- [ ] Content moderation
- [ ] Output validation
- [ ] Safety evaluation

**Timeline**: Week 19-20

---

### Phase 9: Multi-Agent Systems

**Status**: Good foundation, keep structure

**Enhancements**:

- [ ] Add diverse multi-agent projects
- [ ] Add coordination patterns

**Timeline**: Week 21-23

---

### Phase 10: Deployment & Production (ENHANCED)

**Status**: Needs expansion

**Planned Additions**:

- [ ] Chapter 55: FastAPI for AI Applications
- [ ] Chapter 56: Docker for AI Services
- [ ] Chapter 57: CI/CD for AI Projects
- [ ] Chapter 58: Monitoring & Observability
- [ ] Chapter 59: Scaling & Performance

**Timeline**: Week 24-26

---

## 🎯 Quality Gates

### Per-Chapter Quality Gate

**Must Pass Before Moving to Next Chapter**:

- [ ] Follows MASTER-CHAPTER-TEMPLATE-V2.md structure
- [ ] Coffee Shop Intro: 250-350 words
- [ ] 17+ of 23 pedagogical principles applied
- [ ] 5-7 analogies included
- [ ] 2+ "Try This!" exercises with hints
- [ ] 3-5 verification scripts (all passing)
- [ ] 7+ summary bullet points
- [ ] 80%+ on QUALITY-CHECKLIST.md
- [ ] Code examples tested and working
- [ ] Peer review complete (if applicable)

---

### Phase Quality Gate

**Must Pass Before Moving to Next Phase**:

- [ ] All chapters in phase complete
- [ ] Integration project demonstrates phase skills
- [ ] All verification scripts passing
- [ ] PROJECT-THREAD.md updated
- [ ] Roadmap updated
- [ ] Phase completion report written

---

## 📊 Progress Tracking

### Phase 1 Progress (10 Chapters)

- [x] Ch 7: Your First LLM Call ✅
- [ ] Ch 8: Local Models with Ollama (0%)
- [ ] Ch 9: System Prompts & Personalities (0%)
- [ ] Ch 10: Multi-Provider Architecture (0%)
- [ ] Ch 11: Prompt Engineering Foundations (0%)
- [ ] Ch 12: Advanced Prompt Engineering (0%)
- [ ] Ch 13: Streaming Responses (0%)
- [ ] Ch 14: Structured Output (0%)
- [ ] Ch 15: Error Handling & Retries (0%)
- [ ] Ch 16: Token Counting & Cost Optimization (0%)

**Overall**: 10% complete (1/10 chapters)

---

### Full Curriculum Progress (69 Planned Chapters)

- **Phase 0**: 9 chapters (complete)
- **Phase 1**: 10 chapters (1 complete, 9 remaining)
- **Phase 2**: 4 chapters (complete, enhancements planned)
- **Phase 3**: 6 chapters (complete, add RAG from scratch)
- **Phase 4**: 4 chapters (complete)
- **Phase 5**: 4 chapters (complete)
- **Phase 6**: 8 chapters (complete)
- **Phase 7**: 5 chapters (NEW - fine-tuning)
- **Phase 8**: 6 chapters (complete, add guardrails)
- **Phase 9**: 6 chapters (complete)
- **Phase 10**: 7 chapters (complete, add deployment)

**Total**: 69 chapters planned, 54 complete from roadmap-v6.md + 15 new

---

## 🚨 Risk Management

### Identified Risks

**Risk 1: Chapter Burnout**

- **Impact**: Quality drops, motivation decreases
- **Mitigation**:
  - Write 2-3 chapters per week maximum
  - Take breaks between sprints
  - Celebrate completions

**Risk 2: Scope Creep**

- **Impact**: Timeline extends indefinitely
- **Mitigation**:
  - Stick to 23 pedagogical principles (don't add more)
  - Use template structure (don't reinvent per chapter)
  - Focus on Phase 1 completion before Phase 2-10 enhancements

**Risk 3: Pedagogical Principle Inconsistency**

- **Impact**: Quality varies across chapters
- **Mitigation**:
  - Use QUALITY-CHECKLIST.md for every chapter
  - Reference Chapter 7 as gold standard
  - Peer review critical chapters

**Risk 4: Research Divergence**

- **Impact**: Curriculum falls behind industry
- **Mitigation**:
  - Review curriculum-sources-deep-research.md quarterly
  - Add new resources as discovered
  - Update chapters if major patterns change

---

## 🎓 Learning from Chapter 7

### What Worked Well ✅

1. **Coffee Shop Intro** (328 words)
   - Engaging story with Alex character
   - Set emotional tone
   - Clear learning objectives preview

2. **Progressive Complexity**
   - Started with 5-line example
   - Layered complexity gradually
   - "Simple → Nuanced → Complete" pattern

3. **Metacognitive Prompts**
   - 3 well-placed checkpoints
   - Students reflect on learning
   - Increased retention

4. **Error Prediction Exercises**
   - 2 "What will happen?" scenarios
   - Build debugging intuition
   - Failure-forward learning

5. **Real-World War Story**
   - $1,000 API bill anecdote
   - Memorable and practical
   - Shows consequences

6. **Verification Scripts**
   - verify_setup.py with 5 tests
   - Clear pass/fail criteria
   - Builds confidence

### What to Improve 🔧

1. **More Analogies**
   - Target: 5-7 per chapter
   - Chapter 7 had: ~4
   - Add 1-2 more in varied sections

2. **Learning Style Indicators**
   - Not fully implemented
   - Add visual/auditory/kinesthetic cues

3. **Concept Map Diagram**
   - Mentioned but not fully visualized
   - Create actual Mermaid diagram

### Apply to Future Chapters

**Template Checklist**:

- [ ] 17+ pedagogical principles (proven in Ch 7)
- [ ] Coffee Shop Intro: 250-350 words
- [ ] 5-7 analogies minimum
- [ ] 2-3 metacognitive prompts
- [ ] 1-2 error prediction exercises
- [ ] 1-2 real-world war stories
- [ ] Verification script with 3-5 tests
- [ ] Progressive complexity layering

---

## 🔗 Dependencies & Relationships

### Document Dependencies

**This Roadmap Depends On**:

- CURRICULUM-EVOLUTION-DECISIONS.md (strategic guidelines)
- curriculum-subjects-and-projects-analysis.md (gap analysis)
- phase-1-restructure-plan.md (Phase 1 details)
- MASTER-CHAPTER-TEMPLATE-V2.md (chapter structure)

**This Roadmap Informs**:

- roadmap-v7.0.md (when created, timeline and structure)
- Weekly/monthly progress reports
- Phase completion summaries
- Contributor onboarding

---

### Chapter Dependencies (Phase 1)

```
Ch 7 (First LLM Call)
  ↓
Ch 8 (Ollama) ← depends on Ch 7 concepts
  ↓
Ch 9 (System Prompts) ← depends on Ch 7
  ↓
Ch 10 (Multi-Provider) ← depends on Ch 7, 8
  ↓
Ch 11 (Prompt Eng Basics) ← depends on Ch 9
  ↓
Ch 12 (Advanced Prompts) ← depends on Ch 11
  ↓
Ch 13 (Streaming) ← depends on Ch 7
  ↓
Ch 14 (Structured Output) ← depends on Phase 0 (Pydantic)
  ↓
Ch 15 (Error Handling) ← depends on Ch 7, 13
  ↓
Ch 16 (Cost Optimization) ← depends on all prior chapters
```

**Critical Path**: Ch 7 → Ch 8 → Ch 10 → Ch 11 → Ch 12
**Parallel Work Possible**: Ch 9, 13, 14 can be written concurrently after Ch 7

---

## 📞 Support & Resources

### When Stuck

**Writing Block**:

- Review Chapter 7 as reference
- Use WRITING-STYLE-GUIDE.md patterns
- Start with Coffee Shop Intro (easiest section)
- Apply one pedagogical principle at a time

**Quality Concerns**:

- Run QUALITY-CHECKLIST.md
- Compare to Chapter 7
- Ask: "Would I want to learn from this?"
- Get peer feedback

**Technical Issues**:

- Test all code examples
- Run verification scripts
- Use Ollama for free local testing

---

### Resources

**Templates & Guides**:

- curriculum/templates/MASTER-CHAPTER-TEMPLATE-V2.md
- curriculum/guides/WRITING-STYLE-GUIDE.md
- curriculum/guides/LANGUAGE-EXPANSION-GUIDE.md
- curriculum/guides/QUALITY-CHECKLIST.md

**Reference Implementation**:

- curriculum/chapters/phase-1-llm-fundamentals/chapter-07-your-first-llm-call.md

**Research**:

- curriculum/docs/curriculum-sources-deep-research.md

---

## 🎉 Celebration Milestones

**When to Celebrate**:

- ✅ **Chapter 7 Complete** - First new chapter! 🎊
- [ ] **3 Chapters Complete** (Ch 7-9) - Momentum building! 🚀
- [ ] **6 Chapters Complete** (Ch 7-12) - Halfway through Phase 1! 🎯
- [ ] **Phase 1 Complete** (Ch 7-16) - Major milestone! 🏆
- [ ] **10 Chapters Enhanced** - Double-digit progress! 💯
- [ ] **All 69 Chapters Complete** - Full curriculum! 🌟

---

## 📝 Revision History

| Date       | Version | Changes                  | Author      |
| ---------- | ------- | ------------------------ | ----------- |
| 2026-02-10 | 1.0     | Initial roadmap creation | BMad Master |

---

**Document Status**: ✅ Active - Use this roadmap to guide all implementation work. Update progress weekly.
