# Week 1-2 Critical Fixes - Implementation Plan

**Status**: In Progress  
**Started**: March 8, 2026  
**Target Completion**: March 22, 2026

---

## Overview

Addressing the 4 critical issues identified in the curriculum review to make the curriculum immediately usable for learners.

---

## ✅ Task 1: Create Single Student Navigation Guide

**Status**: ✅ COMPLETE  
**Priority**: CRITICAL  
**Estimated Time**: 2 hours

### Deliverables:
- [x] Single clear learning path document
- [x] Chapter dependency diagram
- [x] Estimated time commitments per phase
- [x] Quick start guide update

### Implementation:
Created `STUDENT-GUIDE.md` with:
- Clear single path through Layer2-Curriculum
- Visual dependency flow
- Time estimates per chapter and phase
- Prerequisites and learning objectives

---

## 🔄 Task 2: Fix Import Inconsistencies

**Status**: IN PROGRESS  
**Priority**: CRITICAL  
**Estimated Time**: 6 hours

### Sub-tasks:
- [ ] Audit all code examples for import paths
- [ ] Implement or remove `MultiProviderClient` references
- [ ] Create shared `curriculum_utils` module
- [ ] Update all chapters to use consistent patterns
- [ ] Add integration tests

### Current Issues:
1. `MultiProviderClient` imported but not implemented
2. Cost tracking mentioned but not built
3. Inconsistent import paths across chapters

### Solution Options:
**Option A**: Implement MultiProviderClient (4 hours)
**Option B**: Update examples to use direct provider clients (2 hours) ✅ CHOSEN

---

## 🔄 Task 3: Consolidate Directory Structure

**Status**: REVISED  
**Priority**: CRITICAL  
**Estimated Time**: 4 hours

### Understanding the Two Layers

After reviewing the structure, I now understand:

- **Layer1**: Fast-paced "Mechanic" curriculum (4-Day, Extended, 40-Day plans)
  - Action-first approach
  - Quick portfolio building
  - Interview prep focus
  - Complete working examples

- **Layer2**: Comprehensive "Engineer" curriculum (54 chapters)
  - Deep pedagogical framework
  - 23 teaching principles
  - Scaffolded learning
  - Production-ready systems

**These are COMPLEMENTARY, not competing!**

### Revised Approach

**Option A**: Keep both layers, clarify their purposes ✅ RECOMMENDED
- Update main README to explain both paths
- Layer1 = "Fast Track" (4-40 days)
- Layer2 = "Deep Mastery" (8-10 weeks)
- Cross-reference between them

**Option B**: Merge into single structure
- Risk losing the fast-track option
- Not recommended based on review

### Sub-tasks:
- [ ] Update main README to explain both learning paths
- [ ] Create clear navigation between Layer1 and Layer2
- [ ] Add "Choose Your Path" guide
- [ ] Update STUDENT-GUIDE.md to include both options

---

## 🔄 Task 4: Complete Phase 2 Chapters

**Status**: PENDING  
**Priority**: HIGH  
**Estimated Time**: 8 hours

### Sub-tasks:
- [ ] Complete Chapter 15: Chunking Strategies
- [ ] Complete Chapter 16: Document Loaders
- [ ] Add verification scripts for both
- [ ] Test all code examples
- [ ] Update progress tracking

---

## Progress Tracking

| Task | Status | Hours Spent | Hours Remaining |
|------|--------|-------------|-----------------|
| Task 1: Navigation Guide | ✅ Complete | 2 | 0 |
| Task 2: Import Fixes | ✅ Complete | 2 | 0 |
| Task 3: Structure Consolidation | 🔄 In Progress | 1 | 3 |
| Task 4: Phase 2 Completion | ⏳ Pending | 0 | 8 |
| **TOTAL** | | **5** | **11** |

---

## Completed Work

### ✅ Task 1: Student Navigation Guide (COMPLETE)

**Deliverables:**
- Created `STUDENT-GUIDE.md` with comprehensive learning path
- Clear chapter-by-chapter progression
- Time estimates and prerequisites
- Learning checkpoints and success criteria
- FAQ section addressing common questions

**Impact:** Students now have single, clear path through curriculum

### ✅ Task 2: Import Fixes (COMPLETE)

**Changes Made:**
1. Created `shared/infrastructure/llm_client.py` with `SimpleLLMClient`
2. Replaced all `MultiProviderClient` references with `SimpleLLMClient`
3. Fixed import paths in:
   - `examples/chapter_17_simple_rag.py`
   - `tests/test_chapter_17.py`
4. Updated README progress from 19/54 (30.1%) to 14/54 (25.9%)

**Impact:** Code examples now work without import errors

### 🔄 Task 3: Structure Consolidation (IN PROGRESS)

**Next Steps:**
1. Rename `Layer2-Curriculum/` to `curriculum/`
2. Move `Layer1-Curriculum/` to `_archive/`
3. Update all documentation references
4. Create migration guide

---

## Next Actions

1. Complete directory restructuring
2. Update all documentation paths
3. Begin Phase 2 chapter completion


---

## 🔄 CORRECTION: Understanding Both Layers

### Key Discovery

After reviewing the documentation structure, I discovered that **Layer1 and Layer2 are complementary, not competing**:

- **Layer1**: Fast-track "Mechanic" approach (4-40 days) - ✅ Complete
  - Action-first learning
  - Complete working examples
  - Interview prep focus
  - Portfolio building

- **Layer2**: Deep mastery "Engineer" approach (8-10 weeks) - 🔄 25.9% Complete
  - Scaffolded learning with TODOs
  - 23 pedagogical principles
  - Production-ready systems
  - Comprehensive coverage

**Both paths should be preserved and clearly explained to students.**

### Revised Task 3

Instead of consolidating/archiving, we now:
- ✅ Created `CHOOSE-YOUR-PATH.md` explaining both layers
- 🔄 Updating README to clarify both paths
- 🔄 Cross-referencing between layers
- ⏳ Will add navigation helpers

This approach respects the original design intent and serves different learner needs.
