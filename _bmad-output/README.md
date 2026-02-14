# BMAD Output Directory
**AI-Generated Planning, Analysis, and Implementation Documents**

**Last Updated**: February 10, 2026
**Status**: Active - Reorganized for clarity

---

## 📁 Directory Structure

### `/active/` - Current Planning Documents
**Purpose**: Authoritative, actively-used planning and analysis documents

**Contents**:
- `curriculum-subjects-and-projects-analysis.md` - 22,000-word analysis of learning objectives, subjects, and project diversity based on 100+ resource research
- `phase-1-restructure-plan.md` - Approved plan for beginner-friendly Phase 1 (10 chapters, "Your First LLM Call" onboarding)

**Usage**: Reference these documents for current curriculum decisions and implementation guidance.

---

### `/archive/` - Historical Reference
**Purpose**: Completed, outdated, or superseded documents for historical context

#### `/archive/outdated-analysis/`
**Outdated planning documents** that were based on incorrect assumptions or superseded by better analysis:

- `curriculum-transformation-analysis.md` - Based on AITEA misunderstanding (AITEA was disposed, not current curriculum)
- `curriculum-diversity-transformation.md` - Domain transformation focus (user clarified: focus on subjects/objectives, not domains)

**Why Archived**: User clarified that (1) AITEA is disposed documentation only, (2) focus should be on learning objectives and subjects rather than domain transformation.

#### `/archive/sessions/`
**Session completion summaries** from various work sessions:

- `SESSION-*.md` - Daily/weekly session notes
- Historical record of progress
- Useful for understanding decision evolution

#### `/archive/enhancements/`
**Chapter enhancement plans and completion reports**:

- `chapter-*-enhancement-*.md` - Enhancement planning documents
- `CHAPTER-*-IMPLEMENTATION-COMPLETE.md` - Completion reports
- `IMPLEMENTATION-GUIDE-*.md` - Implementation guides
- `PHASE-*-IMPLEMENTATION-STATUS.md` - Phase status tracking

**Why Archived**: These represent completed work or superseded by newer templates/approaches.

---

### `/pilot-scaffolding/` - Pilot Program Materials
**Purpose**: Beta testing and pilot program for new curriculum patterns

**Contents**:
- Beta testing materials
- Student feedback templates
- Pilot completion reports
- Scaling patterns and guides

**Status**: Completed pilot, archived for reference

---

### Root Files (Transitional)
**Files remaining in root** (to be moved or deleted as appropriate):

**Keep**:
- `README.md` (this file)
- `FRAMEWORK-CLARIFICATION-23-vs-17.md` (pedagogical framework reference)
- `QUICK-DECISION-GUIDE.md` (quick reference guide)
- `MERGE-UTILITY-GUIDE.md` (merge utility documentation)
- `merge_chapter.py` (utility script)

**Review/Cleanup**:
- Various scaffolding, testing, and task files
- Move completed materials to appropriate archive folders

---

## 🛠️ Utility Scripts

### merge_chapter.py

**Purpose**: Merges chapter continuation content into enhanced chapter files.

**Quick Usage**:
```bash
python _bmad-output/merge_chapter.py
```

**Documentation**: See [MERGE-UTILITY-GUIDE.md](MERGE-UTILITY-GUIDE.md) for detailed usage.

---

## 🎯 How to Use This Directory

### For Current Work
**Start here**:
1. Read `active/curriculum-subjects-and-projects-analysis.md` for comprehensive gap analysis
2. Read `active/phase-1-restructure-plan.md` for Phase 1 implementation details
3. Reference `/curriculum/docs/CURRICULUM-EVOLUTION-DECISIONS.md` (consolidated guidelines)
4. Reference `/curriculum/docs/CURRICULUM-IMPLEMENTATION-ROADMAP.md` (next steps)

### For Historical Context
**Understand evolution**:
1. Check `archive/outdated-analysis/` to see initial (incorrect) approaches
2. Review `archive/sessions/` for decision chronology
3. Review `archive/enhancements/` for completed chapter work

### For Contributions
**Before contributing**:
1. Read main `/CONTRIBUTING.md`
2. Check `active/` for current priorities
3. Avoid duplicating work in `archive/`

---

## 📊 Document Lifecycle

### Active Documents
**Criteria**: Currently guiding implementation decisions

**Maintenance**:
- Review quarterly
- Update when curriculum decisions change
- Keep aligned with main curriculum docs

**Lifecycle**: Active → Archive (when superseded)

---

### Archived Documents
**Criteria**: Completed, outdated, or superseded

**Maintenance**:
- No updates needed
- Keep for historical reference
- Delete only if truly obsolete (rare)

**Lifecycle**: Archive → Delete (only if no historical value)

---

## 🔗 Related Documentation

**Main Curriculum Docs** (`/curriculum/docs/`):
- `CURRICULUM-EVOLUTION-DECISIONS.md` - **START HERE** - Consolidated guidelines
- `CURRICULUM-IMPLEMENTATION-ROADMAP.md` - Next steps and timeline
- `curriculum-sources-deep-research.md` - Research foundation (100+ resources)
- `roadmap-v6.md` - Current curriculum structure (will become v7.0 after Phase 1)

**Guides** (`/curriculum/guides/`):
- `WRITING-STYLE-GUIDE.md` - Pedagogical writing patterns
- `LANGUAGE-EXPANSION-GUIDE.md` - 23 pedagogical principles
- `QUALITY-CHECKLIST.md` - Quality verification
- `ANALOGY-LIBRARY.md` - Reusable analogies

**Templates** (`/curriculum/templates/`):
- `MASTER-CHAPTER-TEMPLATE-V2.md` - Complete chapter skeleton (v2.2)
- `chapter-template-cafe-style.md` - Alternative template
- `chapter-template-guide.md` - Writing guide

---

## 📝 Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-10 | 2.0 | Complete reorganization - active/archive structure | BMad Master |
| 2024-01-20 | 1.0 | Initial README | BMad Master |

---

## 🎓 Key Decisions Documented

### Why Two Analysis Documents in Archive?
1. **curriculum-transformation-analysis.md**: Based on misunderstanding that AITEA was current curriculum (it's disposed)
2. **curriculum-diversity-transformation.md**: Focused on domain transformation (Healthcare, Finance, etc.) - user redirected to focus on subjects/objectives instead

**Current Approach**: `active/curriculum-subjects-and-projects-analysis.md` focuses correctly on learning objectives, subjects, and mini-project diversity.

### Why Phase 1 Restructure?
- Research shows "LLM call in 15 minutes" pattern is critical
- Current curriculum had decorators before first AI call (beginner barrier)
- Solution: Keep Phase 0 (Python foundations), enhance Phase 1 to start with simple LLM call

**Approved Plan**: `active/phase-1-restructure-plan.md` - 10 beginner-friendly chapters

---

**Directory Status**: ✅ Reorganized and documented - This structure supports ongoing curriculum evolution while preserving historical context.
