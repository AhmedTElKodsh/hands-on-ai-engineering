# Curriculum Directories Reorganization Analysis
**Comprehensive Audit and Cleanup Plan**

**Date**: February 10, 2026
**Scope**: curriculum/docs, guides, prompts, templates, examples
**Goal**: Eliminate duplicates, archive outdated files, create clean structure

---

## 📊 Directory-by-Directory Analysis

### 1. curriculum/docs/ (16 files)

#### ✅ KEEP (Current & Essential)
1. **CURRICULUM-EVOLUTION-DECISIONS.md** - NEW, authoritative decisions doc (12,000 words)
2. **CURRICULUM-IMPLEMENTATION-ROADMAP.md** - NEW, implementation plan (10,000 words)
3. **curriculum-sources-deep-research.md** - Research foundation (100+ resources)
4. **roadmap-v6.md** - Current curriculum structure (will become v7.0)

#### 📦 ARCHIVE (Outdated/Completed)

**AITEA-Related (Disposed Curriculum)**:
5. **README.md** - AITEA curriculum overview (disposed, not current)
6. **ENVIRONMENT_SETUP.md** - AITEA environment setup (not current curriculum)
7. **SETUP_SUMMARY.md** - AITEA setup summary (not current curriculum)

**Planning Documents (Superseded)**:
8. **CURRICULUM-ORGANIZATION.md** - Old directory structure (Jan 20, needs update or archive)
9. **FILE-REORGANIZATION-PLAN-2026-01-20.md** - Planning doc from Jan 20 (superseded)
10. **PATH-D-STRATEGIC-HYBRID.md** - Old curriculum approach (superseded)

**Enhancement Plans (Completed Work)**:
11. **CHAPTER-7-ENHANCEMENT-PLAN.md** - Chapter 7 enhancement plan (Ch 7 now complete)
12. **ROADMAP-V6.1-ENHANCEMENTS.md** - Old enhancements list (check if superseded)

**Session Notes**:
13. **SESSION-COMPLETE-FRAMEWORK-AND-TESTING-2026-01-20.md** - Session notes (historical)
14. **SESSION-FRAMEWORK-ENHANCEMENT-COMPLETE-2026-01-20.md** - Session notes (historical)

**Workflow Documents (Review)**:
15. **PILOT-SCAFFOLDING-ENHANCEMENT-WORKFLOW.md** - Workflow guide (check if current)
16. **CHAPTER-ENHANCEMENT-WORKFLOW.md** - Workflow guide (check if superseded by template)

---

### 2. curriculum/guides/ (4 files)

#### ✅ ALL GOOD - KEEP ALL
1. **ANALOGY-LIBRARY.md** - Reusable analogies collection
2. **LANGUAGE-EXPANSION-GUIDE.md** - 23 pedagogical principles (1,343 lines)
3. **QUALITY-CHECKLIST.md** - Quality verification standards
4. **WRITING-STYLE-GUIDE.md** - Pedagogical writing patterns (485 lines)

**Action**: No changes needed - all are current, authoritative guides

---

### 3. curriculum/prompts/ (1 file)

#### ✅ GOOD - KEEP
1. **UNIFIED_CURRICULUM_PROMPT_v6.md** - AI assistant prompt

**Action**: No changes needed

---

### 4. curriculum/templates/ (4 files)

#### ✅ ALL GOOD - KEEP ALL
1. **README.md** - Templates directory index
2. **chapter-template-cafe-style.md** - Cafe-style template
3. **chapter-template-guide.md** - How to use templates
4. **MASTER-CHAPTER-TEMPLATE-V2.md** - Primary template (v2.2)

**Action**: No changes needed - all are current templates

---

### 5. examples/ (5 files + __pycache__)

#### ✅ KEEP (Code Examples)
1. **autogen_estimation_example.py** - AutoGen example
2. **crewai_estimation_example.py** - CrewAI example
3. **chapter_17_simple_rag.py** - Simple RAG example

#### 🗑️ DELETE (Build Artifacts)
4. **__pycache__/conversion_demo.cpython-313.pyc** - Python cache (generated)
5. **__pycache__/template_framework_demo.cpython-313.pyc** - Python cache (generated)

**Action**: Delete __pycache__ directory, keep Python source files

---

## 🎯 Recommended Actions

### Phase 1: Create Archive Structure

```bash
mkdir -p curriculum/docs/archive/aitea-reference
mkdir -p curriculum/docs/archive/planning-2026-01
mkdir -p curriculum/docs/archive/session-notes
mkdir -p curriculum/docs/archive/workflows
```

---

### Phase 2: Move Files to Archive

#### AITEA Reference Materials
```
curriculum/docs/README.md → archive/aitea-reference/
curriculum/docs/ENVIRONMENT_SETUP.md → archive/aitea-reference/
curriculum/docs/SETUP_SUMMARY.md → archive/aitea-reference/
```

#### January 2026 Planning Documents
```
curriculum/docs/CURRICULUM-ORGANIZATION.md → archive/planning-2026-01/
curriculum/docs/FILE-REORGANIZATION-PLAN-2026-01-20.md → archive/planning-2026-01/
curriculum/docs/PATH-D-STRATEGIC-HYBRID.md → archive/planning-2026-01/
curriculum/docs/CHAPTER-7-ENHANCEMENT-PLAN.md → archive/planning-2026-01/
curriculum/docs/ROADMAP-V6.1-ENHANCEMENTS.md → archive/planning-2026-01/ (if superseded)
```

#### Session Notes
```
curriculum/docs/SESSION-*.md → archive/session-notes/
```

#### Workflow Documents (Review First)
```
curriculum/docs/PILOT-SCAFFOLDING-ENHANCEMENT-WORKFLOW.md → archive/workflows/ (if outdated)
curriculum/docs/CHAPTER-ENHANCEMENT-WORKFLOW.md → archive/workflows/ (if superseded by MASTER-CHAPTER-TEMPLATE-V2.md)
```

---

### Phase 3: Clean Examples

```bash
rm -rf examples/__pycache__
```

---

### Phase 4: Create New Index Files

#### curriculum/docs/README.md (NEW)
Create new README pointing to current structure:
- CURRICULUM-EVOLUTION-DECISIONS.md (start here)
- CURRICULUM-IMPLEMENTATION-ROADMAP.md (next steps)
- curriculum-sources-deep-research.md (research)
- roadmap-v6.md (current curriculum)
- archive/ (historical documents)

---

## 📁 Proposed Final Structure

```
curriculum/
├── docs/
│   ├── README.md (NEW - directory guide)
│   ├── CURRICULUM-EVOLUTION-DECISIONS.md ✅
│   ├── CURRICULUM-IMPLEMENTATION-ROADMAP.md ✅
│   ├── curriculum-sources-deep-research.md ✅
│   ├── roadmap-v6.md ✅
│   └── archive/
│       ├── aitea-reference/
│       │   ├── README.md (AITEA curriculum overview)
│       │   ├── ENVIRONMENT_SETUP.md
│       │   └── SETUP_SUMMARY.md
│       ├── planning-2026-01/
│       │   ├── CURRICULUM-ORGANIZATION.md
│       │   ├── FILE-REORGANIZATION-PLAN-2026-01-20.md
│       │   ├── PATH-D-STRATEGIC-HYBRID.md
│       │   ├── CHAPTER-7-ENHANCEMENT-PLAN.md
│       │   └── ROADMAP-V6.1-ENHANCEMENTS.md
│       ├── session-notes/
│       │   ├── SESSION-COMPLETE-FRAMEWORK-AND-TESTING-2026-01-20.md
│       │   └── SESSION-FRAMEWORK-ENHANCEMENT-COMPLETE-2026-01-20.md
│       └── workflows/
│           ├── PILOT-SCAFFOLDING-ENHANCEMENT-WORKFLOW.md
│           └── CHAPTER-ENHANCEMENT-WORKFLOW.md
│
├── guides/
│   ├── ANALOGY-LIBRARY.md ✅
│   ├── LANGUAGE-EXPANSION-GUIDE.md ✅
│   ├── QUALITY-CHECKLIST.md ✅
│   └── WRITING-STYLE-GUIDE.md ✅
│
├── prompts/
│   └── UNIFIED_CURRICULUM_PROMPT_v6.md ✅
│
├── templates/
│   ├── README.md ✅
│   ├── chapter-template-cafe-style.md ✅
│   ├── chapter-template-guide.md ✅
│   └── MASTER-CHAPTER-TEMPLATE-V2.md ✅
│
└── examples/
    ├── autogen_estimation_example.py ✅
    ├── crewai_estimation_example.py ✅
    └── chapter_17_simple_rag.py ✅
```

---

## 📊 Impact Summary

### Before Reorganization
- **curriculum/docs**: 16 files (mixed current/outdated/duplicates)
- **Confusion**: Which files are current?
- **AITEA references**: Mixed with current curriculum
- **Planning docs**: Scattered across root directory

### After Reorganization
- **curriculum/docs**: 4 current files + organized archive/
- **Clarity**: All current docs clearly visible
- **AITEA**: Cleanly archived as reference
- **Planning**: Organized by date in archive
- **Clean examples**: No build artifacts

---

## ✅ Execution Checklist

### Prepare
- [ ] Create archive directory structure
- [ ] Backup current state (git commit)

### Move AITEA Materials
- [ ] Move README.md → archive/aitea-reference/
- [ ] Move ENVIRONMENT_SETUP.md → archive/aitea-reference/
- [ ] Move SETUP_SUMMARY.md → archive/aitea-reference/

### Move Planning Documents
- [ ] Move CURRICULUM-ORGANIZATION.md → archive/planning-2026-01/
- [ ] Move FILE-REORGANIZATION-PLAN-2026-01-20.md → archive/planning-2026-01/
- [ ] Move PATH-D-STRATEGIC-HYBRID.md → archive/planning-2026-01/
- [ ] Move CHAPTER-7-ENHANCEMENT-PLAN.md → archive/planning-2026-01/
- [ ] Move ROADMAP-V6.1-ENHANCEMENTS.md → archive/planning-2026-01/

### Move Session Notes
- [ ] Move SESSION-COMPLETE-FRAMEWORK-AND-TESTING-2026-01-20.md → archive/session-notes/
- [ ] Move SESSION-FRAMEWORK-ENHANCEMENT-COMPLETE-2026-01-20.md → archive/session-notes/

### Move Workflow Documents
- [ ] Review PILOT-SCAFFOLDING-ENHANCEMENT-WORKFLOW.md (keep or archive?)
- [ ] Review CHAPTER-ENHANCEMENT-WORKFLOW.md (superseded by template?)
- [ ] Move outdated workflows → archive/workflows/

### Clean Examples
- [ ] Delete examples/__pycache__/ directory

### Create New Documentation
- [ ] Create curriculum/docs/README.md (directory guide)
- [ ] Update CURRICULUM-EVOLUTION-DECISIONS.md if needed

### Verify
- [ ] All current docs remain in curriculum/docs/
- [ ] All archived docs in curriculum/docs/archive/
- [ ] No build artifacts in examples/
- [ ] New README.md guides users correctly

---

## 🎓 Rationale for Each Archive

### AITEA Materials
**Why archived**: AITEA curriculum was disposed and replaced with current structure. Kept as reference for historical context and previous pedagogical decisions.

### Planning Documents (Jan 2026)
**Why archived**: These planning documents led to the current CURRICULUM-EVOLUTION-DECISIONS.md and CURRICULUM-IMPLEMENTATION-ROADMAP.md. Historical record of evolution, but superseded.

### Session Notes
**Why archived**: Completion summaries from past sessions. Useful for understanding decision timeline but not current guidance.

### Workflow Documents
**Why archived (if applicable)**: Superseded by MASTER-CHAPTER-TEMPLATE-V2.md which provides comprehensive chapter creation workflow.

---

**Status**: ✅ Analysis complete - Ready for execution
