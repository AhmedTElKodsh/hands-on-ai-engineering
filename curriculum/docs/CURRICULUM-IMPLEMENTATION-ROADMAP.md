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

**Document Status**: ✅ Active - Use this roadmap to guide all implementation work. Update progress weekly.
