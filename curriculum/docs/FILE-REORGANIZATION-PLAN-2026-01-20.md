# File Reorganization Plan - January 20, 2026

**Purpose**: Eliminate confusion, duplication, and conflicting information  
**Status**: Analysis Complete - Ready for Execution  
**Impact**: Single source of truth for all documentation

---

## 🎯 Problem Statement

**Current Issues**:

1. **Duplicate information** across multiple files
2. **Outdated files** (v2, v3 logs) mixed with current files
3. **Conflicting information** between old and new documents
4. **Unclear hierarchy** - which file is authoritative?
5. **Poor organization** - files scattered across multiple locations

**Result**: Confusion about what's current, what's accurate, what to follow

---

## 📊 Current File Inventory & Analysis

### Root Level Files (Project Root)

| File                                      | Status       | Action  | Reason                                                            |
| ----------------------------------------- | ------------ | ------- | ----------------------------------------------------------------- |
| `REBUILD_V2_COMPLETION_LOG.md`            | ❌ OUTDATED  | ARCHIVE | Superseded by v3 and current work                                 |
| `REBUILD_V3_ENHANCEMENT_LOG.md`           | ❌ OUTDATED  | ARCHIVE | Superseded by 2026-01-20 enhancements                             |
| `PROGRESS-SUMMARY.md`                     | ⚠️ OUTDATED  | UPDATE  | Needs current status (30.1% → current)                            |
| `CURRICULUM_PROMPT.md`                    | ❌ DUPLICATE | DELETE  | Duplicate of `curriculum/prompts/UNIFIED_CURRICULUM_PROMPT_v6.md` |
| `CURRICULUM-UPDATE-SUMMARY-2026-01-18.md` | ⚠️ PARTIAL   | MOVE    | Move to `curriculum/docs/archive/`                                |
| `QUICKSTART.md`                           | ✅ CURRENT   | UPDATE  | Update with latest status                                         |

### Curriculum Level Files

| File                                    | Status     | Action | Reason                          |
| --------------------------------------- | ---------- | ------ | ------------------------------- |
| `curriculum/CURRICULUM-ORGANIZATION.md` | ✅ CURRENT | KEEP   | Master index - recently updated |
| `curriculum/ENVIRONMENT_SETUP.md`       | ✅ CURRENT | KEEP   | Technical setup guide           |
| `curriculum/README.md`                  | ✅ CURRENT | KEEP   | Student-facing entry point      |

### curriculum/docs/ Directory

| File                                                  | Status        | Action  | Reason                        |
| ----------------------------------------------------- | ------------- | ------- | ----------------------------- |
| `EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md`   | ✅ CURRENT    | KEEP    | Core philosophy document      |
| `SESSION-ENHANCEMENT-2026-01-20.md`                   | ✅ CURRENT    | KEEP    | Phase 1 documentation         |
| `SESSION-PHASE-2-COMPLETION-2026-01-20.md`            | ✅ CURRENT    | KEEP    | Phase 2 documentation         |
| `CHAPTER-7-ENHANCEMENT-PLAN.md`                       | ✅ CURRENT    | KEEP    | Phase 3 planning              |
| `EDUCATIONAL-ENHANCEMENT-CONSOLIDATION-2026-01-20.md` | ✅ CURRENT    | KEEP    | Complete consolidation        |
| `roadmap-v6.md`                                       | ✅ CURRENT    | KEEP    | Curriculum structure          |
| `ROADMAP-V6.1-ENHANCEMENTS.md`                        | ✅ CURRENT    | KEEP    | Enhancement specifications    |
| `PATH-D-STRATEGIC-HYBRID.md`                          | ✅ CURRENT    | KEEP    | Strategic direction           |
| Other session logs                                    | ⚠️ HISTORICAL | ARCHIVE | Move to archive/ subdirectory |

### curriculum/guides/ Directory

| File                          | Status     | Action | Reason                  |
| ----------------------------- | ---------- | ------ | ----------------------- |
| `LANGUAGE-EXPANSION-GUIDE.md` | ✅ CURRENT | KEEP   | Transformation patterns |
| `WRITING-STYLE-GUIDE.md`      | ✅ CURRENT | KEEP   | Voice & tone guide      |
| `ANALOGY-LIBRARY.md`          | ✅ CURRENT | KEEP   | 50+ analogies           |
| `QUALITY-CHECKLIST.md`        | ✅ CURRENT | KEEP   | 62-item review tool     |

### curriculum/prompts/ Directory

| File                              | Status     | Action | Reason                 |
| --------------------------------- | ---------- | ------ | ---------------------- |
| `UNIFIED_CURRICULUM_PROMPT_v6.md` | ✅ CURRENT | KEEP   | AI teaching guidelines |

### curriculum/references/ Directory

| File                | Status     | Action | Reason              |
| ------------------- | ---------- | ------ | ------------------- |
| `PROJECT-THREAD.md` | ✅ CURRENT | KEEP   | Component evolution |
| `ce-contexts.md`    | ✅ CURRENT | KEEP   | CE scenario library |

### Duplicate/Nested Directories

| Directory                                       | Status       | Action | Reason                    |
| ----------------------------------------------- | ------------ | ------ | ------------------------- |
| `hands-on-ai-engineering/` (nested)             | ❌ DUPLICATE | DELETE | Duplicate of main project |
| `hands-on-ai-engineering/curriculum/templates/` | ❌ DUPLICATE | DELETE | Duplicate templates       |

---

## 🎯 Reorganization Strategy

### Phase 1: Create Archive Structure

Create organized archive for historical documents

### Phase 2: Move Outdated Files

Move outdated files to archive with clear naming

### Phase 3: Delete Duplicates

Remove duplicate files and directories

### Phase 4: Update Current Files

Update remaining files with current information

### Phase 5: Create Master Index

Create single authoritative index document

---

## 📁 Proposed New Structure

```
D:\AI\Gentech\POCs\hands-on-ai-engineering\
│
├── README.md ✅ (Project overview)
├── QUICKSTART.md ✅ (Updated - Quick start guide)
├── PROGRESS-SUMMARY.md ✅ (Updated - Current status)
│
├── curriculum/
│   ├── README.md ✅ (Student entry point)
│   ├── CURRICULUM-ORGANIZATION.md ✅ (Master index)
│   ├── ENVIRONMENT_SETUP.md ✅ (Technical setup)
│   │
│   ├── docs/ (Current planning & roadmap)
│   │   ├── roadmap-v6.md ✅
│   │   ├── ROADMAP-V6.1-ENHANCEMENTS.md ✅
│   │   ├── PATH-D-STRATEGIC-HYBRID.md ✅
│   │   ├── EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md ✅
│   │   ├── EDUCATIONAL-ENHANCEMENT-CONSOLIDATION-2026-01-20.md ✅
│   │   ├── CHAPTER-7-ENHANCEMENT-PLAN.md ✅
│   │   ├── FILE-REORGANIZATION-PLAN-2026-01-20.md ✅ (This file)
│   │   │
│   │   └── archive/ (Historical documents)
│   │       ├── 2026-01-17/
│   │       │   ├── SESSION-COMPLETION-2026-01-17-FINAL.md
│   │       │   ├── TEMPLATE-UPDATE-2026-01-17.md
│   │       │   └── CURRICULUM-AUDIT-2026-01-17.md
│   │       ├── 2026-01-18/
│   │       │   └── CURRICULUM-UPDATE-SUMMARY-2026-01-18.md
│   │       └── 2026-01-20/
│   │           ├── SESSION-ENHANCEMENT-2026-01-20.md
│   │           └── SESSION-PHASE-2-COMPLETION-2026-01-20.md
│   │
│   ├── guides/ (Writing & teaching guides)
│   │   ├── LANGUAGE-EXPANSION-GUIDE.md ✅
│   │   ├── WRITING-STYLE-GUIDE.md ✅
│   │   ├── ANALOGY-LIBRARY.md ✅
│   │   └── QUALITY-CHECKLIST.md ✅
│   │
│   ├── prompts/ (AI teaching prompts)
│   │   └── UNIFIED_CURRICULUM_PROMPT_v6.md ✅
│   │
│   ├── reference/ (Domain & context)
│   │   ├── PROJECT-THREAD.md ✅
│   │   └── ce-contexts.md ✅
│   │
│   ├── templates/ (Chapter templates)
│   │   ├── MASTER-CHAPTER-TEMPLATE-V2.md ✅
│   │   ├── chapter-template-cafe-style.md ✅
│   │   └── chapter-template-guide.md ✅
│   │
│   └── chapters/ (Curriculum content)
│       ├── phase-0-foundations/
│       ├── phase-1-llm-fundamentals/
│       └── ...
│
├── _archive/ (Project-level archive)
│   ├── rebuild-logs/
│   │   ├── REBUILD_V2_COMPLETION_LOG.md
│   │   └── REBUILD_V3_ENHANCEMENT_LOG.md
│   └── old-prompts/
│       └── CURRICULUM_PROMPT.md
│
├── shared/ (Shared code)
├── src/ (Source code)
├── tests/ (Test code)
└── examples/ (Example implementations)
```

---

## 🔄 Execution Plan

### Step 1: Create Archive Directories ✅

```
_archive/
_archive/rebuild-logs/
_archive/old-prompts/
curriculum/docs/archive/
curriculum/docs/archive/2026-01-17/
curriculum/docs/archive/2026-01-18/
curriculum/docs/archive/2026-01-20/
```

### Step 2: Move Outdated Root Files

- `REBUILD_V2_COMPLETION_LOG.md` → `_archive/rebuild-logs/`
- `REBUILD_V3_ENHANCEMENT_LOG.md` → `_archive/rebuild-logs/`
- `CURRICULUM_PROMPT.md` → `_archive/old-prompts/`
- `CURRICULUM-UPDATE-SUMMARY-2026-01-18.md` → `curriculum/docs/archive/2026-01-18/`

### Step 3: Move Historical Session Docs

- Session docs from `curriculum/docs/` → `curriculum/docs/archive/YYYY-MM-DD/`

### Step 4: Delete Duplicate Directories

- Delete `hands-on-ai-engineering/` (nested duplicate)

### Step 5: Update Current Files

- Update `QUICKSTART.md` with latest status
- Update `PROGRESS-SUMMARY.md` with current metrics
- Update `curriculum/CURRICULUM-ORGANIZATION.md` with new structure

### Step 6: Create Master Index

- Create `MASTER-INDEX.md` at project root
- Single source of truth for all documentation

---

## 📋 File Categories & Purposes

### Category 1: Entry Points (Keep at Root)

**Purpose**: First files users see

- `README.md` - Project overview
- `QUICKSTART.md` - Quick start guide
- `MASTER-INDEX.md` - Complete documentation index (NEW)
- `PROGRESS-SUMMARY.md` - Current status

### Category 2: Current Planning (curriculum/docs/)

**Purpose**: Active planning and roadmap

- `roadmap-v6.md` - Curriculum structure
- `ROADMAP-V6.1-ENHANCEMENTS.md` - Enhancement specs
- `PATH-D-STRATEGIC-HYBRID.md` - Strategic direction
- `EDUCATIONAL-PHILOSOPHY-ENHANCEMENTS-2026-01-20.md` - Core philosophy
- `EDUCATIONAL-ENHANCEMENT-CONSOLIDATION-2026-01-20.md` - Complete consolidation
- `CHAPTER-7-ENHANCEMENT-PLAN.md` - Phase 3 planning
- `FILE-REORGANIZATION-PLAN-2026-01-20.md` - This file

### Category 3: Practical Guides (curriculum/guides/)

**Purpose**: How-to guides for content creation

- `LANGUAGE-EXPANSION-GUIDE.md` - Transformation patterns
- `WRITING-STYLE-GUIDE.md` - Voice & tone
- `ANALOGY-LIBRARY.md` - 50+ analogies
- `QUALITY-CHECKLIST.md` - 62-item review

### Category 4: AI Teaching (curriculum/prompts/)

**Purpose**: AI assistant guidelines

- `UNIFIED_CURRICULUM_PROMPT_v6.md` - Complete teaching prompt

### Category 5: Reference (curriculum/reference/)

**Purpose**: Domain knowledge and context

- `PROJECT-THREAD.md` - Component evolution
- `ce-contexts.md` - CE scenarios

### Category 6: Templates (curriculum/templates/)

**Purpose**: Chapter creation templates

- `MASTER-CHAPTER-TEMPLATE-V2.md` - Primary template
- `chapter-template-cafe-style.md` - Style examples
- `chapter-template-guide.md` - Usage guide

### Category 7: Historical (Archives)

**Purpose**: Historical record, not for daily use

- Session completion logs
- Old rebuild logs
- Superseded documents

---

## ✅ Success Criteria

After reorganization:

- [ ] No duplicate files
- [ ] No conflicting information
- [ ] Clear hierarchy (current vs. historical)
- [ ] Single master index
- [ ] All current files easily findable
- [ ] Historical files preserved but archived
- [ ] Updated documentation reflects new structure

---

## 📊 Impact Analysis

### Before Reorganization

- **Root level files**: 6 (mix of current and outdated)
- **Duplicate directories**: 1 (hands-on-ai-engineering/)
- **Unclear status**: Multiple files with conflicting info
- **User confusion**: High - which file is current?

### After Reorganization

- **Root level files**: 4 (all current and clear purpose)
- **Duplicate directories**: 0
- **Clear status**: Current vs. archived
- **User confusion**: Low - master index + clear structure

---

## 🎯 Next Steps

1. ✅ Create this reorganization plan
2. ⏳ Execute reorganization (create archives, move files)
3. ⏳ Update current files with latest information
4. ⏳ Create MASTER-INDEX.md
5. ⏳ Verify all links still work
6. ⏳ Document changes in consolidation file

---

**Status**: Plan Complete - Ready for Execution  
**Estimated Time**: 30-45 minutes  
**Risk**: Low (all moves, no deletions of content)
