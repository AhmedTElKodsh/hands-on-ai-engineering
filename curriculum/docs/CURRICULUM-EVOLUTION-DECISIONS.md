# Curriculum Evolution Decisions
**Consolidated Guidelines and Strategic Decisions for AI Engineering Curriculum**

**Document Owner**: Ahmed
**Last Updated**: February 10, 2026
**Status**: Active - Authoritative Reference
**Purpose**: Single source of truth for all curriculum design decisions

---

## 🎯 Core Curriculum Philosophy

### Guiding Principles

1. **Inclusiveness Over Specialization**
   - Prioritize learning objectives and subjects over domain-specific applications
   - Welcome learners from all backgrounds (not just Civil Engineering)
   - Provide diverse projects representing multiple industries and use cases

2. **Beginner-Friendly Progressive Teaching**
   - "LLM magic" in first 15 minutes (immediate gratification)
   - Simple examples first, complexity layered gradually
   - Keep Phase 0 (Python foundations) intact
   - Start Phase 1 with accessible "Your First LLM Call"

3. **Project Diversity Over Monolithic Projects**
   - 50+ mini-projects throughout curriculum (not one continuous system)
   - Each chapter gets a focused, standalone project
   - Students build varied portfolio, not single application

4. **Research-Aligned Subject Coverage**
   - Based on analysis of 100+ open-source AI engineering resources
   - Topics: LLMs, embeddings, RAG, agents, fine-tuning, deployment
   - Patterns: Build from scratch → then frameworks
   - Missing topics added: Ollama, advanced prompting, fine-tuning, MCP

---

## 📚 Curriculum Structure Decisions

### Phase 0: Foundations (KEEP AS-IS)
**Decision**: Preserve existing Python fundamentals (Chapters 1-6)

**Rationale**:
- Strong foundation needed for later chapters
- Decorators, context managers, OOP are prerequisites
- Students can skip if already proficient
- Advanced Python is appropriate for pre-LLM work

**Chapters**:
- Ch 1: Environment Setup
- Ch 2: Enums & Type Hints
- Ch 3-4: Pydantic Models (Basic & Advanced)
- Ch 5: Validation Utilities
- Ch 6: Template System
- Ch 6A: Decorators & Context Managers
- Ch 6B: Error Handling Patterns
- Ch 6C: OOP Intermediate

---

### Phase 1: LLM Fundamentals (RESTRUCTURED)
**Decision**: Add beginner-friendly "Your First LLM Call" as Chapter 7

**Rationale**:
- Research shows "LLM call in 15 minutes" pattern is critical
- Immediate dopamine hit builds motivation
- Simple 5-line example before architectural complexity
- Aligns with Microsoft GenAI, Unsloth, LangChain tutorials

**New Structure** (Approved in phase-1-restructure-plan.md):

**Ch 7: Your First LLM Call (NEW)**
- Super simple, 5 lines of code
- Single provider (OpenAI or Anthropic)
- Working chatbot immediately
- Time: 1.5 hours | Difficulty: ⭐

**Ch 8: Local Models with Ollama (NEW)**
- Free experimentation without API costs
- Llama, Mistral, Phi models
- Privacy & offline development
- Time: 2 hours | Difficulty: ⭐⭐

**Ch 9: System Prompts & Personalities**
- Role assignment, tone control
- Building AI personas
- Time: 1.5 hours | Difficulty: ⭐

**Ch 10: Multi-Provider Architecture (ENHANCED from old Ch 8)**
- OpenAI, Anthropic, Ollama abstraction
- Provider switching
- Time: 2 hours | Difficulty: ⭐⭐

**Ch 11: Prompt Engineering Foundations**
- Few-shot learning, chain-of-thought
- Prompt templates
- Time: 2 hours | Difficulty: ⭐⭐

**Ch 12: Advanced Prompt Engineering**
- ReAct, self-consistency
- Prompt optimization
- Time: 2.5 hours | Difficulty: ⭐⭐⭐

**Ch 13: Streaming Responses**
- Async streaming, token-by-token
- Time: 1.5 hours | Difficulty: ⭐⭐

**Ch 14: Structured Output**
- JSON mode, Pydantic models
- Time: 2 hours | Difficulty: ⭐⭐

**Ch 15: Error Handling & Retries**
- Rate limits, timeouts, exponential backoff
- Time: 2 hours | Difficulty: ⭐⭐

**Ch 16: Token Counting & Cost Optimization**
- tiktoken, cost calculation
- Caching strategies
- Time: 1.5 hours | Difficulty: ⭐⭐

**Total**: 10 chapters, 20 hours

---

### v7.0 Enhancements (February 2026)
**Decision**: Add critical foundation chapters for file operations and asyncio

**Rationale**:
- Every AI project needs file I/O (reading prompts, saving outputs, document processing)
- Modern AI applications require async patterns (streaming, concurrent API calls, production scalability)
- Analysis of curriculum gaps identified missing core topics
- Industry frameworks (FastAPI, LangChain, LlamaIndex) all use asyncio extensively

**New Chapters Added**:

**Ch 6D: File Handling & Path Management (Phase 0 - NEW)**
- Read/write text, CSV, JSON files
- pathlib for cross-platform paths
- File context managers
- Loading prompts from files
- Saving LLM outputs
- Time: 1.5 hours | Difficulty: ⭐

**Ch 12A: Asyncio Fundamentals (Phase 1 - NEW CRITICAL)**
- async/await syntax
- Asyncio event loop
- asyncio.gather() for parallel calls
- Async context managers
- Error handling in async code
- Brief GIL explanation
- Time: 2 hours | Difficulty: ⭐⭐

**Teaching Pattern Evolution**:
- **Action-First, Then Deep Dive** - Quick success (5-8 min) → comprehensive explanations
- Documented in guides/ACTION-FIRST-DEEP-DIVE-GUIDE.md
- Keep ALL comprehensive content, just reorder for engagement
- Applied Principle 24 in LANGUAGE-EXPANSION-GUIDE.md

**Impact**:
- Phase 0: 9 chapters → 10 chapters (13.5h → 15h)
- Phase 1: 10 chapters → 11 chapters (20h → 22h)
- Total curriculum: 59 chapters → 61 chapters (78h → 81.5h)

**Documentation**:
- See docs/PHASE-0-TOPICS-ANALYSIS.md for complete rationale
- See guides/ACTION-FIRST-DEEP-DIVE-GUIDE.md for teaching pattern
- See guides/GUIDES-UPDATE-SUMMARY-2026-02-10.md for guide changes

---

### Phase 2-10 (FUTURE ENHANCEMENTS)
**Decision**: Keep current structure, add diversity later

**Planned Additions** (from curriculum-subjects-and-projects-analysis.md):
- Fine-tuning chapters (Phase 7)
- MCP (Model Context Protocol) expansion
- Build-from-scratch chapters before framework chapters
- Deployment & production patterns (Phase 10)
- Guardrails & safety (Phase 8)

---

## 🎓 Pedagogical Framework

### The 23 Pedagogical Principles
**Source**: MASTER-CHAPTER-TEMPLATE-V2.md, EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md

**Implementation Status**: ✅ Template documented, applied to Chapter 7

**Core Principles** (Always Apply):
1. Progressive Complexity Layering
2. Anticipatory Question Addressing
3. Failure-Forward Learning
4. Contextual Bridges
5. Emotional Checkpoints
6. Multi-Modal Explanations
7. Metacognitive Prompts
8. Error Prediction Exercises
9. Real-World War Stories
10. Confidence Calibration
11. Spaced Repetition Callbacks
12. Graduated Scaffolding
13. Practical Application Hooks
14. Concept Mapping Diagrams
15. Learning Style Indicators
16. Cognitive Load Management
17. Conversational Asides
18. Expand Language (no abbreviations)
19. Increase Descriptiveness
20. Enhance Analogies (5-7 per chapter)
21. Reduce Bullets (70% narrative, 30% bullets)
22. Expand Sections (Coffee Shop Intro: 250-350 words)
23. Spaced Repetition Markers

**Implementation Tiers**:
- **Tier 1** (High Impact, Low Effort): Principles 7-10, 20-22 (apply first)
- **Tier 2** (High Impact, Medium Effort): Principles 3-6, 11-12 (apply second)
- **Tier 3** (Medium Impact, Higher Effort): Principles 13-17 (apply last)
- **Core** (Always Present): Principles 1-2, 18-19, 23

---

### Content Quality Standards

**Coffee Shop Intro**: 250-350 words
**Analogies**: 5-7 per chapter (varied complexity)
**Code Examples**: 3-5 per concept, progressive
**Try This! Exercises**: Minimum 2 per chapter
**Anticipatory Questions**: 4-6 per chapter
**Metacognitive Prompts**: 2-3 per chapter
**Error Prediction**: 1-2 exercises per chapter
**Real-World War Stories**: 1-2 per chapter
**Verification Scripts**: 3-5 per chapter
**Summary Bullets**: Minimum 7 key points

**Narrative vs. Bullets**: 70% narrative, 30% bullets

---

## 🔬 Research Foundations

### Analysis Source
**File**: curriculum/docs/curriculum-sources-deep-research.md
**Resources Analyzed**: 100+ open-source AI engineering projects
**Total Stars**: 500,000+ combined

### Top Research Sources

1. **Microsoft GenAI for Beginners** (103k stars)
   - Pattern: 21 lessons = 21 standalone projects
   - Insight: Diverse projects, not monolithic

2. **Ollama** (120k stars)
   - Pattern: Local models first, API second
   - Insight: Free experimentation critical for learning

3. **mlabonne/llm-course** (73.7k stars)
   - Pattern: Theory → Practice → Projects
   - Insight: Comprehensive roadmap with hands-on

4. **DAIR.AI Prompt Engineering Guide** (66.4k stars)
   - Pattern: Techniques → Examples → Applications
   - Insight: Prompt engineering is deep subject

5. **Unsloth** (30k stars)
   - Pattern: Fine-tuning made accessible
   - Insight: Fine-tuning is core, not advanced

6. **NirDiamant/RAG_Techniques** (24k stars)
   - Pattern: 30+ self-contained implementations
   - Insight: Build from scratch before frameworks

### Key Research Findings

**Consensus Patterns**:
- ✅ LLM call in first 15 minutes
- ✅ Build from scratch → then frameworks
- ✅ Diverse projects (15-30+) over single monolithic project
- ✅ Local models (Ollama) for cost-free experimentation
- ✅ Fine-tuning as core topic (not advanced)
- ✅ Prompt engineering depth (multiple chapters)
- ✅ Multi-provider architecture (avoid vendor lock-in)

**Alignment Assessment**:
- **Before**: 40% alignment with research
- **After (with Phase 1 restructure)**: 95% alignment

---

## 📁 File Organization Decisions

### What to Keep (Authoritative References)

**Core Guides** (curriculum/guides/):
- WRITING-STYLE-GUIDE.md (485 lines, cafe-style patterns)
- LANGUAGE-EXPANSION-GUIDE.md (1,343 lines, 23 principles)
- QUALITY-CHECKLIST.md (verification standards)
- ANALOGY-LIBRARY.md (reusable analogies)

**Templates** (curriculum/templates/):
- MASTER-CHAPTER-TEMPLATE-V2.md (v2.2, complete skeleton)
- chapter-template-cafe-style.md (alternative template)
- chapter-template-guide.md (writing guide)

**Active Planning** (_bmad-output/):
- curriculum-subjects-and-projects-analysis.md (22,000 words, correct analysis)
- phase-1-restructure-plan.md (10,000 words, approved plan)

**Research & Roadmap** (curriculum/docs/):
- curriculum-sources-deep-research.md (research foundation)
- roadmap-v6.md (current curriculum structure)

**Contributing** (root):
- CONTRIBUTING.md (contribution guidelines)

---

### What to Archive (Historical/Outdated)

**Outdated Analysis** (_bmad-output/):
- ❌ curriculum-transformation-analysis.md (based on AITEA misunderstanding)
- ❌ curriculum-diversity-transformation.md (domain transformation - user said no)

**Completed Session Files** (_bmad-output/):
- Move to _bmad-output/archive/sessions/
- Includes: SESSION-*.md, CHAPTER-*-IMPLEMENTATION-COMPLETE.md

**Completed Enhancement Plans** (_bmad-output/):
- Move to _bmad-output/archive/enhancements/
- Includes: chapter-*-enhancement-plan-*.md, chapter-*-enhancements-ALL-TIERS.md

**Educational Framework Consolidation** (curriculum/docs/):
- ❌ EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md (now in guides)
- ❌ EDUCATIONAL-ENHANCEMENT-CONSOLIDATION-2026-01-20.md (session notes)
- ❌ CHAPTER-ENHANCEMENT-GUIDE-UNIVERSAL.md (overlaps with template)

---

### New Organization Structure

```
curriculum/
├── docs/
│   ├── CURRICULUM-EVOLUTION-DECISIONS.md (this file - NEW)
│   ├── CURRICULUM-IMPLEMENTATION-ROADMAP.md (next steps - NEW)
│   ├── curriculum-sources-deep-research.md (keep)
│   └── roadmap-v6.md (keep, will become v7.0 after Phase 1)
├── guides/
│   ├── WRITING-STYLE-GUIDE.md (keep)
│   ├── LANGUAGE-EXPANSION-GUIDE.md (keep)
│   ├── QUALITY-CHECKLIST.md (keep)
│   └── ANALOGY-LIBRARY.md (keep)
├── templates/
│   ├── MASTER-CHAPTER-TEMPLATE-V2.md (keep)
│   ├── chapter-template-cafe-style.md (keep)
│   └── chapter-template-guide.md (keep)
├── prompts/
│   └── UNIFIED_CURRICULUM_PROMPT_v6.md (keep)
└── archive/
    ├── reference/
    │   ├── AITEA-curriculum-design.md (keep as reference)
    │   ├── ce-contexts.md (keep for examples)
    │   └── [other reference materials]
    └── [dated folders with session notes]

_bmad-output/
├── active/
│   ├── curriculum-subjects-and-projects-analysis.md (move here)
│   └── phase-1-restructure-plan.md (move here)
├── archive/
│   ├── outdated-analysis/
│   │   ├── curriculum-transformation-analysis.md (move here)
│   │   └── curriculum-diversity-transformation.md (move here)
│   ├── sessions/
│   │   └── [SESSION-*.md files]
│   ├── enhancements/
│   │   └── [chapter enhancement files]
│   └── pilot-scaffolding/
│       └── [existing pilot files]
└── README.md (update to explain structure)
```

---

## 🚀 Implementation Roadmap

### Completed ✅

1. **Phase 0 Foundation Analysis** - Phase 0 stays intact
2. **Phase 1 Restructure Plan** - 10-chapter beginner-friendly structure
3. **Chapter 7 Implementation** - "Your First LLM Call" complete (~25,000 words)
4. **Pedagogical Framework** - 23 principles documented and applied
5. **Consolidation Documentation** - This file created

---

### In Progress 🔄

1. **File Reorganization** - Moving outdated files to archive
2. **Documentation Cleanup** - Removing duplicates and overlaps

---

### Next Steps (Priority Order) 📋

**Immediate (Next Session)**:
1. Complete file reorganization (_bmad-output structure)
2. Create CURRICULUM-IMPLEMENTATION-ROADMAP.md
3. Update roadmap-v6.md → roadmap-v7.0.md (with Phase 1 changes)

**Phase 1 Completion (Weeks 1-4)**:
1. Write Chapter 8: Local Models with Ollama
2. Write Chapter 9: System Prompts & Personalities
3. Write Chapter 10: Multi-Provider Architecture
4. Write Chapter 11-12: Prompt Engineering (Foundations & Advanced)
5. Write Chapter 13-16: Streaming, Structured Output, Error Handling, Cost Optimization
6. Create verification scripts for all Phase 1 chapters
7. Update PROJECT-THREAD.md with Phase 1 component dependencies

**Phase 2+ Enhancements (Future)**:
1. Add "Build from Scratch" chapters before framework chapters
2. Add fine-tuning chapters (Phase 7)
3. Add MCP (Model Context Protocol) chapters
4. Add deployment & production chapters (Phase 10)
5. Add guardrails & safety chapters (Phase 8)
6. Transform Phase 3-10 chapters with diverse mini-projects

---

## 🎯 Success Metrics

### Phase 1 Success Criteria

**Completion Metrics**:
- ✅ 10 chapters written (7-16)
- ✅ All chapters follow MASTER-CHAPTER-TEMPLATE-V2.md
- ✅ 17+ of 23 pedagogical principles applied per chapter
- ✅ 80%+ quality checklist score
- ✅ Verification scripts pass for all chapters
- ✅ Coffee Shop Intros: 250-350 words each
- ✅ Total Phase 1 time: ~20 hours of content

**Learning Outcome Metrics**:
- Student can make LLM call in 15 minutes (Ch 7)
- Student understands local vs. cloud models (Ch 8)
- Student can craft effective prompts (Ch 11-12)
- Student can handle errors gracefully (Ch 15)
- Student can optimize costs (Ch 16)

---

## 📝 Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-10 | 1.1 | Added v7.0 enhancements (Ch 6D, 12A, action-first pattern) | Claude Sonnet 4.5 |
| 2026-02-10 | 1.0 | Initial consolidation of all curriculum decisions | BMad Master |

---

## 🔗 Related Documents

**Must Read Together**:
- curriculum/docs/CURRICULUM-IMPLEMENTATION-ROADMAP.md (next steps)
- _bmad-output/active/curriculum-subjects-and-projects-analysis.md (detailed analysis)
- _bmad-output/active/phase-1-restructure-plan.md (Phase 1 details)
- curriculum/templates/MASTER-CHAPTER-TEMPLATE-V2.md (chapter structure)
- curriculum/guides/WRITING-STYLE-GUIDE.md (writing patterns)

**Research Foundation**:
- curriculum/docs/curriculum-sources-deep-research.md (100+ resources)

**Reference**:
- curriculum/archive/reference/AITEA-curriculum-design.md (previous approach)
- CONTRIBUTING.md (contribution guidelines)

---

**Document Status**: ✅ Active - This is the authoritative reference for all curriculum design decisions. Update this file when major decisions are made.
