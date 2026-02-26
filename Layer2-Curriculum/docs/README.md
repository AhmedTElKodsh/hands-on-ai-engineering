# Curriculum Documentation
**Core planning and reference documents for AI Engineering curriculum**

**Last Updated**: February 10, 2026
**Status**: Active and organized

---

## 🎯 Start Here

### For Curriculum Development
**Read these documents in order:**

1. **[CURRICULUM-EVOLUTION-DECISIONS.md](CURRICULUM-EVOLUTION-DECISIONS.md)** - START HERE
   - Single source of truth for all curriculum design decisions
   - Core philosophy, Phase 0-1 structure, 23 pedagogical principles
   - Research foundations, file organization decisions
   - ~12,000 words - comprehensive reference

2. **[CURRICULUM-IMPLEMENTATION-ROADMAP.md](CURRICULUM-IMPLEMENTATION-ROADMAP.md)** - NEXT STEPS
   - Clear 4-week action plan for Phase 1 completion
   - Sprint-by-sprint breakdown (Chapters 8-16)
   - Quality gates, risk management, progress tracking
   - ~10,000 words - detailed implementation guide

3. **[curriculum-sources-deep-research.md](curriculum-sources-deep-research.md)** - RESEARCH
   - Analysis of 100+ open-source AI engineering resources
   - Research consensus patterns and best practices
   - Foundation for curriculum design decisions

4. **[roadmap-v6.md](roadmap-v6.md)** - CURRENT CURRICULUM
   - Complete curriculum structure (59 chapters, 10 phases, 78 hours)
   - Will become roadmap-v7.0.md after Phase 1 restructure

---

## 📚 Quick Reference

### Current Status
- **Phase 1 Progress**: 10% complete (1/10 chapters)
- **Latest Chapter**: Chapter 7 - "Your First LLM Call" ✅
- **Next Chapters**: 8 (Ollama), 9 (System Prompts), 10 (Multi-Provider)

### Key Decisions
- ✅ Keep Phase 0 (Python foundations) intact
- ✅ Add "Your First LLM Call" to Phase 1 (beginner-friendly)
- ✅ Focus on learning objectives & subjects (NOT domain transformation)
- ✅ 50+ diverse mini-projects (NOT single monolithic project)
- ✅ Research alignment: 40% → 95%

---

## 📁 Directory Structure

```
curriculum/docs/
├── README.md (this file)
│
├── CURRICULUM-EVOLUTION-DECISIONS.md ✅ Core decisions
├── CURRICULUM-IMPLEMENTATION-ROADMAP.md ✅ Implementation plan
├── curriculum-sources-deep-research.md ✅ Research analysis
├── roadmap-v6.md ✅ Current curriculum
├── REORGANIZATION-ANALYSIS.md ✅ File cleanup analysis
│
└── archive/
    ├── aitea-reference/ (Disposed AITEA curriculum docs)
    ├── planning-2026-01/ (January 2026 planning documents)
    ├── session-notes/ (Historical session completion notes)
    └── workflows/ (Superseded workflow documents)
```

---

## 🔗 Related Documentation

### Templates & Guides (../templates/, ../guides/)
**For writing chapters:**
- [MASTER-CHAPTER-TEMPLATE-V2.md](../templates/MASTER-CHAPTER-TEMPLATE-V2.md) - Complete chapter skeleton (v2.2)
- [WRITING-STYLE-GUIDE.md](../guides/WRITING-STYLE-GUIDE.md) - Pedagogical writing patterns
- [LANGUAGE-EXPANSION-GUIDE.md](../guides/LANGUAGE-EXPANSION-GUIDE.md) - 23 pedagogical principles
- [QUALITY-CHECKLIST.md](../guides/QUALITY-CHECKLIST.md) - Quality verification

### Prompts (../prompts/)
**For AI assistants:**
- [UNIFIED_CURRICULUM_PROMPT_v6.md](../prompts/UNIFIED_CURRICULUM_PROMPT_v6.md) - AI assistant curriculum prompt

### Planning & Analysis (../../_bmad-output/active/)
**Detailed analysis:**
- [curriculum-subjects-and-projects-analysis.md](../../_bmad-output/active/curriculum-subjects-and-projects-analysis.md) - 22,000-word gap analysis
- [phase-1-restructure-plan.md](../../_bmad-output/active/phase-1-restructure-plan.md) - Phase 1 detailed plan

---

## 📦 Archive

The `archive/` directory contains historical documents for reference:

### archive/aitea-reference/
**Disposed AITEA curriculum materials:**
- README.md - AITEA curriculum overview
- ENVIRONMENT_SETUP.md - AITEA environment setup
- SETUP_SUMMARY.md - AITEA setup summary

**Why archived**: AITEA curriculum was disposed and replaced with current structure. Kept as reference for historical context.

---

### archive/planning-2026-01/
**January 2026 planning documents:**
- CURRICULUM-ORGANIZATION.md - Old directory structure
- FILE-REORGANIZATION-PLAN-2026-01-20.md - Planning doc
- PATH-D-STRATEGIC-HYBRID.md - Old curriculum approach
- CHAPTER-7-ENHANCEMENT-PLAN.md - Chapter 7 enhancement plan (completed)
- ROADMAP-V6.1-ENHANCEMENTS.md - Old enhancements list

**Why archived**: These led to current CURRICULUM-EVOLUTION-DECISIONS.md. Historical record of evolution, now superseded.

---

### archive/session-notes/
**Session completion summaries:**
- SESSION-COMPLETE-FRAMEWORK-AND-TESTING-2026-01-20.md
- SESSION-FRAMEWORK-ENHANCEMENT-COMPLETE-2026-01-20.md

**Why archived**: Historical record of progress, useful for understanding decision timeline.

---

### archive/workflows/
**Workflow documents:**
- PILOT-SCAFFOLDING-ENHANCEMENT-WORKFLOW.md
- CHAPTER-ENHANCEMENT-WORKFLOW.md

**Why archived**: Superseded by MASTER-CHAPTER-TEMPLATE-V2.md which provides comprehensive chapter creation workflow.

---

## 🎓 How to Use This Documentation

### For New Contributors
1. Read CURRICULUM-EVOLUTION-DECISIONS.md (understand the vision)
2. Read CURRICULUM-IMPLEMENTATION-ROADMAP.md (see what's next)
3. Check roadmap-v6.md (understand current structure)
4. Read MASTER-CHAPTER-TEMPLATE-V2.md (learn chapter structure)
5. Start contributing!

### For Chapter Writing
1. Review CURRICULUM-IMPLEMENTATION-ROADMAP.md (find next chapter)
2. Use MASTER-CHAPTER-TEMPLATE-V2.md (chapter skeleton)
3. Follow WRITING-STYLE-GUIDE.md (writing patterns)
4. Apply LANGUAGE-EXPANSION-GUIDE.md (23 principles)
5. Verify with QUALITY-CHECKLIST.md (quality standards)

### For Understanding Decisions
1. Check CURRICULUM-EVOLUTION-DECISIONS.md (current decisions)
2. Review curriculum-sources-deep-research.md (research foundation)
3. Check archive/planning-2026-01/ (historical evolution)

---

## 📊 Document Status

| Document | Status | Purpose | Update Frequency |
|----------|--------|---------|------------------|
| CURRICULUM-EVOLUTION-DECISIONS.md | ✅ Current | Authoritative decisions | When major decisions made |
| CURRICULUM-IMPLEMENTATION-ROADMAP.md | ✅ Current | Implementation plan | Weekly (progress updates) |
| curriculum-sources-deep-research.md | ✅ Current | Research foundation | Quarterly (new resources) |
| roadmap-v6.md | ✅ Current | Current curriculum | When phases restructure |
| archive/* | 📦 Archived | Historical reference | Never (frozen) |

---

## 🚀 Next Steps

**Immediate (This Week)**:
- Write Chapter 8: Local Models with Ollama
- Write Chapter 9: System Prompts & Personalities
- Write Chapter 10: Multi-Provider Architecture

**See CURRICULUM-IMPLEMENTATION-ROADMAP.md for detailed sprint plans.**

---

## 📝 Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-10 | 1.0 | Created after reorganization | BMad Master |

---

**Document Purpose**: This README serves as the entry point for all curriculum documentation, guiding contributors to the right resources and explaining the organization.
