# Curriculum Decisions - March 2026

**Document Created:** March 10, 2026  
**Decision Date:** March 8-10, 2026  
**Status:** ✅ **DECIDED & IMPLEMENTED**  
**Owner:** Ahmed  

---

## 🎯 Executive Summary

After comprehensive review and adversarial testing, we have **consolidated to a single canonical curriculum**: **LAYER1-FINAL** (28 weeks, market-calibrated).

**Key Decision:** Archive all previous versions and standardize on LAYER1-FINAL as the single source of truth for AI Engineering education.

---

## 📋 Decision Timeline

### March 8, 2026 - Curriculum Review

**Review Conducted:** Comprehensive validation and adversarial review

**Findings:**
- ✅ **Strengths:** Excellent pedagogical design, comprehensive scope, industry-aligned
- 🔴 **Critical Issues:** Infrastructure gaps, structural inconsistencies, completion status mismatch
- 🟡 **High Priority:** SQL placement, testing integration, security threading

**Review Score:** 8.2/10 - Excellent foundation with specific improvement areas

### March 8, 2026 - Migration Analysis

**Comparison:** Modified Curriculum (32 weeks) vs. LAYER1-FINAL (28 weeks)

**Critical Misalignments Found:**
1. ❌ **SQL:** Week 26 (modified) → Week 1 (LAYER1-FINAL)
2. ❌ **Testing:** Week 21 (modified) → Week 2 + threaded (LAYER1-FINAL)
3. ❌ **Security:** Week 23 (modified) → Week 2 + threaded (LAYER1-FINAL)
4. ❌ **Flagships:** 3 standalone → 2 evolving (v1→v2→v3)

**Recommendation:** Archive modified curriculum, adopt LAYER1-FINAL as canonical

### March 10, 2026 - Final Decision

**Decision:** ✅ **LAYER1-FINAL is now the single canonical curriculum**

**Actions Taken:**
1. ✅ Archived all previous curriculum versions
2. ✅ Created clean folder structure
3. ✅ Documented decisions and rationale
4. ✅ Updated navigation and guides

---

## 🏗️ Canonical Curriculum Structure

### What We're Using (LAYER1-FINAL)

**Duration:** 28 weeks (672 hours @ 4h/day, 6 days/week)

**Structure:**
```
LAYER1-FINAL/
├── README.md                          # START HERE: 28-week curriculum
├── GUIDE-FOR-AI-ASSISTANTS.md         # Teaching methodology
├── CHECKPOINT-RUBRICS.md              # Phase verification
├── PROGRESS-TRACKER.md                # Student tracking
├── COST-LOG.md                        # API cost tracking (Week 3+)
├── FAILURE-LOG.md                     # Weekly failure logging
├── DAY-00-DIAGNOSTIC.md               # Python assessment
├── WEEK-16-SPECIALIZATION.md          # Specialization tracks
├── WEEK-21-REFINED.md                 # Frontend scope
└── GIT-COLLABORATION-WEEK1.md         # Git workflow
```

**Key Features:**
- ✅ Backend-first (FastAPI + Postgres from Week 2)
- ✅ Evaluation & observability as core disciplines
- ✅ Security/guardrails threaded throughout
- ✅ Realistic scope: 4-6 deep projects
- ✅ Built-in flex weeks (2 total)
- ✅ Market-calibrated for 2026 AI Engineer roles

### What We Archived

**Archived in:** `_ARCHIVE_2026-03/`

| Curriculum | Status | Reason |
|------------|--------|--------|
| **Layer1-Curriculum** (original) | ⚠️ Archived | Superseded by LAYER1-FINAL |
| **Layer1-Curriculum/modified** | ⚠️ Archived | Structural misalignments |
| **Layer2-Curriculum** | ⚠️ Archived | Chapter-based approach deprecated |
| **layer1-phase1** | ⚠️ Archived | Built as code, not teaching curriculum |

**Preserved Components:**
- ✅ Teaching methodology (5-level ladder) → In LAYER1-FINAL
- ✅ Checkpoint system (4 types) → In LAYER1-FINAL
- ✅ Guided discovery philosophy → In LAYER1-FINAL
- ✅ Weekly structure (20 hours/week) → In LAYER1-FINAL

---

## 📊 Curriculum Comparison

### LAYER1-FINAL (Canonical) vs. Previous Versions

| Aspect | Modified (32w) | Original L1 (40d) | LAYER1-FINAL (28w) |
|--------|---------------|-------------------|-------------------|
| **Duration** | 32 weeks | 40 days | **28 weeks** ✅ |
| **SQL** | Week 26 | Day 15-20 | **Week 1** ✅ |
| **Testing** | Week 21 | Day 5-7 | **Week 2 + threaded** ✅ |
| **Security** | Week 23 | Not emphasized | **Week 2 + threaded** ✅ |
| **MCP** | Mentioned | Not covered | **Week 13** ✅ |
| **Cost Tracking** | Week 24 | Not included | **Week 3+** ✅ |
| **Git Collaboration** | Not included | Basic | **Week 1** ✅ |
| **Failure Logging** | Not included | Not included | **Weekly** ✅ |
| **System Design** | Not included | Not included | **Weeks 8,12,20,26** ✅ |
| **Specialization** | Week 32 "Choose" | Not structured | **Week 16 (tracks)** ✅ |
| **Frontend** | Full React | Full-stack | **Streamlit-first** ✅ |
| **Flagships** | 3 standalone | Many projects | **2 evolving** ✅ |
| **Flex Weeks** | 4 weeks | None | **2 weeks** ✅ |

**Winner:** LAYER1-FINAL (28 weeks, market-calibrated)

---

## 🎓 Teaching Philosophy

### What We Believe

1. **Build-First, Theory-Second** - Learn by doing, understand by reflecting
2. **Production Habits from Day 1** - Type hints, tests, docs, logging
3. **Failure is Data** - Log failures, iterate, improve
4. **Spiral Learning** - Revisit topics at increasing depth
5. **Portfolio Over Certificates** - Ship real projects, show iteration
6. **Market-Aligned** - Build what employers actually hire for

### Daily Cadence (4 hours/day, 6 days/week)

**Learn (60-75 min):**
- Read official docs + one reference implementation
- Write one-page notes for interview prep
- Focus on "why" not just "how"

**Build (150-165 min):**
- Ship the feature with minimal viable scope
- Commit early, commit often
- Keep it working at all times

**Ship (30 min):**
- Write tests (unit + integration)
- Update README with what you learned
- Record 60-120 second demo video

### Weekly Rhythm

- **Days 1-2:** Implement core feature
- **Days 3-4:** Extend + add failure handling
- **Day 5:** Evaluation + tests + measured improvement
- **Day 6:** Refactor + documentation + demo video + reflection
- **Day 7:** Rest (mandatory)

---

## 📁 Folder Structure (Post-Cleanup)

### Root Level
```
hands-on-ai-engineering/
├── LAYER1-FINAL/                      # ✅ CANONICAL CURRICULUM
├── _ARCHIVE_2026-03/                  # ⚠️ Archived versions
│   ├── ARCHIVED-Layer1-Curriculum/
│   ├── ARCHIVED-Layer2-Curriculum/
│   └── ARCHIVED-layer1-phase1/
├── _PLANNING-2026-03/                 # 📋 March planning documents
│   ├── CURRICULUM-REVIEW-2026-03-08.md
│   ├── MIGRATION-GUIDE.md
│   └── MODIFIED-CURRICULUM-INDEX.md
├── docs/                              # 📚 Supplementary documentation
├── books/                             # 📖 Recommended reading
├── examples/                          # 💡 Code examples
└── shared/                            # 🔧 Shared resources
```

### What to Delete (Safe to Remove)

After verifying archives are complete:

- ❌ `Layer1-Curriculum/` (original, not LAYER1-FINAL)
- ❌ `Layer2-Curriculum/`
- ❌ `layer1-phase1/`
- ❌ `Layer1-Curriculum/archive/modified-curriculum/`
- ❌ `MODIFIED-CURRICULUM-INDEX.md` (root level)
- ❌ `MIGRATION-GUIDE.md` (root level)
- ❌ `CURRICULUM-REVIEW-2026-03-08.md` (root level)

**Note:** Keep `LAYER1-FINAL/` - this is the canonical curriculum!

---

## 🎯 What Students Should Use

### New Students (Starting Today)

1. **Start Here:** `LAYER1-FINAL/README.md`
2. **Take Diagnostic:** `LAYER1-FINAL/guides/DAY-00-DIAGNOSTIC.md`
3. **Track Progress:** `LAYER1-FINAL/guides/PROGRESS-TRACKER.md`
4. **Log Costs:** `LAYER1-FINAL/guides/COST-LOG.md` (from Week 3)
5. **Log Failures:** `LAYER1-FINAL/guides/FAILURE-LOG.md` (weekly)

### Current Students (Using Modified Curriculum)

**Migrate at next phase boundary:**

| Your Current Week | Action |
|-------------------|--------|
| **Weeks 1-4** (Phase 1) | Finish Phase 1, migrate to LAYER1-FINAL Phase 2 |
| **Weeks 5-10** (Phase 2) | Finish Phase 2, migrate to LAYER1-FINAL Phase 3 |
| **Weeks 11-16** (Phase 3) | Finish Phase 3, migrate to LAYER1-FINAL Phase 4 |
| **Weeks 17+** (Phase 4+) | Finish current phase, migrate to LAYER1-FINAL Phase 5 |

**Migration Guide:** See `_PLANNING-2026-03/MIGRATION-GUIDE.md`

### AI Assistants

**Teaching Guide:** `LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md`

**Key Principles:**
1. Use the 5-level teaching ladder
2. Verify understanding with checkpoints
3. Never vibe-code - teach, don't solve
4. Log failures as learning opportunities

---

## 📈 28-Week Overview (LAYER1-FINAL)

| Phase | Weeks | Hours | Focus | Checkpoint |
|-------|-------|-------|-------|------------|
| **Foundation** | 1-2 | 48h | Environment + FastAPI + SQL | - |
| **LLM Integration** | 3-4 | 48h | LLM client + structured outputs | ✅ Gate 1 (Week 4) |
| **RAG Core** | 5-8 | 96h | Ingestion + vectors + RAG + eval | ✅ Gate 2 (Week 8) |
| **Production Backend** | 9-12 | 96h | Multi-tenant + auth + observability + CI/CD | ✅ Gate 3 (Week 12) |
| **Flex Week A** | 13 | 24h | Catch-up / Deepen RAG or Backend | - |
| **Agents** | 14-16 | 72h | Raw agents + LangGraph + MCP | ✅ Gate 4 (Week 17) |
| **Specialization** | 17 | 24h | NL2SQL / Docs / Fine-tuning (choose 1) | - |
| **Deployment/Ops** | 18-22 | 120h | Containers + cloud + monitoring + perf + security | ✅ Gate 5 (Week 22) |
| **Flex Week B** | 23 | 24h | Catch-up / Deepen Deployment | - |
| **Capstone** | 24-26 | 72h | Domain-focused system build | - |
| **Polish/Prep** | 27-28 | 48h | Portfolio + interviews + applications | - |

**Total:** 672 hours over 28 weeks

---

## 🎯 What You'll Build

### Flagship Product: Knowledge Assistant Platform

A production-style RAG + agent system delivered as a FastAPI service with:

- 📊 Postgres with pgvector for hybrid storage
- 🔍 Advanced retrieval with reranking and citations
- 🤖 Tool-using agents with safety guardrails
- 📈 Evaluation harness with automated testing
- 👁️ Observability with OpenTelemetry tracing
- 🔒 Multi-tenant security with auth and rate limiting
- 🚀 Cloud deployment with CI/CD pipeline

### Portfolio Artifacts (4 Core + 1 Capstone)

1. **Structured Extraction Service** (Week 4) - LLM + schemas + validation
2. **RAG v1 with Evaluation Harness** (Week 8) - Retrieval + metrics + iteration
3. **Productionized RAG Service** (Week 12) - Tests + CI/CD + observability
4. **Agent + MCP Integration** (Week 15) - Tool safety + audit logs
5. **Domain Capstone** (Weeks 23-25) - Full-stack specialized system

---

## ✅ Action Items

### Immediate (Week 1)

- [x] ✅ Archive old curriculum versions
- [x] ✅ Create clean folder structure
- [x] ✅ Document decisions and rationale
- [ ] ⏳ Verify LAYER1-FINAL folder is complete
- [ ] ⏳ Update main README with clear navigation
- [ ] ⏳ Delete old folders (after verification)

### Week 2

- [ ] Create student onboarding guide
- [ ] Set up progress tracking templates
- [ ] Test all LAYER1-FINAL links and references
- [ ] Create quickstart scripts

### Week 3

- [ ] Record demo videos for each phase
- [ ] Create study group guidelines
- [ ] Set up community discussion space
- [ ] Gather feedback from first students

---

## 📚 Reference Documents

### In _PLANNING-2026-03/

- `CURRICULUM-REVIEW-2026-03-08.md` - Validation review (8.2/10 score)
- `MIGRATION-GUIDE.md` - How to migrate from modified to LAYER1-FINAL
- `MODIFIED-CURRICULUM-INDEX.md` - Archived curriculum index

### In LAYER1-FINAL/

- `README.md` - Main 28-week curriculum
- `guides/DAY-00-DIAGNOSTIC.md` - Python assessment
- `guides/PROGRESS-TRACKER.md` - Student tracking
- `guides/GUIDE-FOR-AI-ASSISTANTS.md` - Teaching methodology
- `guides/CHECKPOINT-RUBRICS.md` - Phase verification
- `docs/ANALYSIS-COMMENTS.md` - Detailed review synthesis

---

## 🎉 Final Notes

**This consolidation brings:**

1. ✅ **Clarity** - Single canonical path, no confusion
2. ✅ **Focus** - 28 weeks, market-calibrated, realistic scope
3. ✅ **Quality** - Production habits from Day 1
4. ✅ **Support** - Teaching methodology, checkpoints, tracking

**What makes LAYER1-FINAL special:**

- **Backend-first** - SQL Week 1, not Week 26
- **Testing threaded** - Week 2 + throughout, not Week 21
- **Security threaded** - Week 2 + throughout, not Week 23
- **Iteration evidence** - 2 evolving flagships (v1→v2→v3)
- **Real-world habits** - Cost tracking, failure logs, system design

**Let's build. 🚀**

---

**Document Version:** 1.0  
**Last Updated:** March 10, 2026  
**Next Review:** March 17, 2026 (or after first student feedback)
