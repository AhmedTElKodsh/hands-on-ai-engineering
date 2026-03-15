# Curriculum Alignment Review — Modified vs. LAYER1-FINAL

**Review Date:** March 8, 2026
**Purpose:** Ensure modified-curriculum aligns with LAYER1-FINAL (28-week canonical version)
**Reviewer:** Bmad Master Analysis

---

## 🎯 EXECUTIVE SUMMARY

**Status:** ⚠️ **PARTIAL ALIGNMENT — Updates Required**

The existing `modified-curriculum/` (32-week version) has **good pedagogical foundations** but contains **significant structural misalignments** with the new `LAYER1-FINAL/` (28-week canonical version).

**Key Issues:**
1. ❌ **Timeline mismatch:** 32 weeks vs. 28 weeks
2. ❌ **SQL placement:** Week 26 in modified → Week 1 in LAYER1-FINAL (critical fix)
3. ❌ **Flagship count:** 3 flagships in modified → 2 evolving flagships in LAYER1-FINAL
4. ❌ **Missing components:** No COST-LOG, FAILURE-LOG, Git collaboration, specialization tracks
5. ❌ **Checkpoint rubrics:** Present but not standardized with LAYER1-FINAL

**Recommendation:** **Archive modified-curriculum as reference, adopt LAYER1-FINAL as canonical**

---

## 📊 DETAILED ALIGNMENT ANALYSIS

### 1. Timeline & Structure

| Aspect | Modified Curriculum | LAYER1-FINAL | Aligned? |
|--------|--------------------|--------------|----------|
| **Total Duration** | 32 weeks | 28 weeks | ❌ No |
| **Flex Weeks** | 4 (Weeks 13, 20, 27, 32+) | 2 (Weeks 9, 27) | ❌ No |
| **Phases** | 5 phases | 5 phases | ✅ Yes |
| **Weekly Structure** | 20 hours/week | 20 hours/week | ✅ Yes |
| **Daily Split** | 4 hours/day × 5 days | 4 hours/day × 5 days | ✅ Yes |

**Action Required:**
- If keeping modified: Update to 28 weeks (remove 2 flex weeks, compress Phase 5)
- **Recommended:** Deprecate modified in favor of LAYER1-FINAL

---

### 2. Critical Content Placement

| Topic | Modified Curriculum | LAYER1-FINAL | Impact |
|-------|--------------------|--------------|--------|
| **SQL/PostgreSQL** | Week 26 | **Week 1** | 🔴 **CRITICAL** |
| **FastAPI** | Week 5 | Week 1 | 🔴 **CRITICAL** |
| **Testing** | Week 21 | Week 2 + threaded | 🔴 **CRITICAL** |
| **Security** | Week 23 | Week 2 + Week 22 + threaded | 🔴 **CRITICAL** |
| **MCP** | Mentioned | Week 13 (full week) | 🟡 Moderate |
| **Cost Tracking** | Week 24 | Week 3 onward | 🟡 Moderate |
| **System Design** | Not included | Weeks 8, 12, 20, 26 | 🟡 Moderate |
| **Git Collaboration** | Not included | Week 1 | 🟡 Moderate |
| **Failure Logging** | Not included | Weekly (mandatory) | 🟡 Moderate |

**Why This Matters:**
- Modified curriculum teaches SQL **26 weeks too late** for job readiness
- Testing and security are **bolted on late** instead of threaded throughout
- LAYER1-FINAL front-loads production habits (correct approach)

**Action Required:**
- **Do not use modified curriculum** for SQL/Testing/Security sequencing
- Adopt LAYER1-FINAL week-by-week structure

---

### 3. Project Structure

| Aspect | Modified Curriculum | LAYER1-FINAL | Aligned? |
|--------|--------------------|--------------|----------|
| **Mini-Projects** | 3 (Weeks 4, 9, 11) | 2 (Weeks 4, 7) | ⚠️ Partial |
| **Flagship Projects** | 3 (Weeks 12, 19, 32) | 2 evolving (v1→v2→v3→final) | ❌ No |
| **Iteration Evidence** | Not required | Required (v1→v2→v3) | ❌ No |
| **Specialization** | "Your Choice" (Week 32) | Structured tracks (Week 16) | ❌ No |

**LAYER1-FINAL Improvements:**
- Flagship 1 starts Week 5 (RAG), evolves through Weeks 6, 10, 18
- Flagship 2 starts Week 12 (Agent), evolves through Weeks 13-15
- Specialization is Week 16 (structured tracks: NL2SQL, Doc Intelligence, Fine-Tuning)
- Iteration logs are mandatory

**Action Required:**
- Update modified project structure to match LAYER1-FINAL
- Add iteration log requirements
- Replace Week 32 "Your Choice" with Week 16 structured tracks

---

### 4. Teaching Methodology

| Component | Modified Curriculum | LAYER1-FINAL | Aligned? |
|-----------|--------------------|--------------|----------|
| **Teaching Ladder** | 5 levels | 5 levels | ✅ Yes |
| **Checkpoint System** | 4 types | 4 types + rubrics | ⚠️ Partial |
| **Response Templates** | Yes | Yes + curriculum-specific | ⚠️ Partial |
| **Red Flags** | Yes | Yes + expanded | ⚠️ Partial |
| **AI Assistant Guide** | TEACHING-METHODOLOGY.md | GUIDE-FOR-AI-ASSISTANTS.md | ⚠️ Partial |

**Good News:** Teaching methodology is **well-aligned** conceptually

**Gaps:**
- Modified lacks **checkpoint rubrics** (scoring 0-5 with clear criteria)
- Modified lacks **curriculum-specific guidance** (which week, what to expect)
- LAYER1-FINAL has **phase-specific checkpoint questions** with expected answers

**Action Required:**
- Replace `guides/CHECKPOINT-SYSTEM.md` with `CHECKPOINT-RUBRICS.md`
- Update `guides/TEACHING-METHODOLOGY.md` to reference LAYER1-FINAL structure

---

### 5. Production Habits

| Habit | Modified Curriculum | LAYER1-FINAL | Aligned? |
|-------|--------------------|--------------|----------|
| **Cost Tracking** | Week 24 only | Week 3 onward (weekly) | ❌ No |
| **Failure Logging** | Not included | Weekly (mandatory) | ❌ No |
| **Git Collaboration** | Not included | Week 1 (branches, PRs, review) | ❌ No |
| **Production Habits Column** | Not included | Every week (40 min) | ❌ No |

**Why This Matters:**
- Cost awareness is a **hiring differentiator**
- Failure logs create **interview stories**
- Git collaboration is **table stakes for teams**

**Action Required:**
- Add `COST-LOG.md` and `FAILURE-LOG.md` templates to modified
- Add Git collaboration workflow to Week 1
- Add "Production Habit" column to weekly tables

---

### 6. Documentation Files

| File | Modified Curriculum | LAYER1-FINAL | Status |
|------|--------------------|--------------|--------|
| **Overview** | PRAGMATIC-CURRICULUM-OVERVIEW.md | README.md (in LAYER1-FINAL) | ⚠️ Merge |
| **Roadmap** | WEEK-BY-WEEK-ROADMAP.md | README.md (detailed) | ⚠️ Merge |
| **Teaching Guide** | guides/TEACHING-METHODOLOGY.md | GUIDE-FOR-AI-ASSISTANTS.md | ⚠️ Replace |
| **Checkpoints** | guides/CHECKPOINT-SYSTEM.md | CHECKPOINT-RUBRICS.md | ⚠️ Replace |
| **Progress Tracker** | Not included | PROGRESS-TRACKER.md | ❌ Add |
| **Cost Log** | Not included | COST-LOG.md | ❌ Add |
| **Failure Log** | Not included | FAILURE-LOG.md | ❌ Add |
| **Git Workflow** | Not included | GIT-COLLABORATION-WEEK1.md | ❌ Add |
| **Specialization** | Not included | WEEK-16-SPECIALIZATION.md | ❌ Add |
| **Frontend Scope** | Not included | WEEK-21-REFINED.md | ❌ Add |
| **Diagnostic** | Not included | grade_diagnostic.py + DAY-00-DIAGNOSTIC.md | ❌ Add |

---

## 🔴 CRITICAL MISALIGNMENTS

### 1. SQL Placement (Week 26 vs. Week 1)

**Modified (WRONG):**
```
Week 26: SQL for AI Systems
- Postgres basics
- Schema design
- Analytics queries
```

**LAYER1-FINAL (CORRECT):**
```
Week 1: FastAPI + SQL + Git Foundations
- Day 2: SQL foundations with PostgreSQL
- Day 3: SQLAlchemy ORM + Alembic migrations
- Week 4: pgvector for embeddings
```

**Why It Matters:**
- Job postings demand SQL from day one
- pgvector is needed for RAG (Week 5)
- Can't teach embeddings without SQL in Week 4

**Fix:** **Do not use modified curriculum Week 26 for SQL.** Adopt LAYER1-FINAL Week 1.

---

### 2. Testing Approach (Week 21 vs. Threaded)

**Modified (WRONG):**
```
Week 21: Testing AI Systems
- Property-based testing
- Adversarial testing
- Regression testing
```

**LAYER1-FINAL (CORRECT):**
```
Week 2: Testing + Docker + CI/CD
- pytest deep-dive (15+ tests for Week 1 API)
- Coverage badges
- CI pipeline

Every week thereafter: "Production Habit (40 min)" includes testing
```

**Why It Matters:**
- Students build 20 weeks of untested code in modified
- Testing becomes an afterthought, not a habit

**Fix:** **Adopt LAYER1-FINAL Week 2 testing + weekly production habits.**

---

### 3. Flagship Project Structure

**Modified (WEAKER):**
```
Flagship 1: Week 12 (standalone)
Flagship 2: Week 19 (standalone)
Flagship 3: Week 32 ("Your Choice")
```

**LAYER1-FINAL (STRONGER):**
```
Flagship 1: Starts Week 5 (RAG v1)
  → Week 6: RAG v2 (reranking, HyDE, caching)
  → Week 10: RAG v3 (production deployment)
  → Week 18: RAG v4 (multi-tenant, auth)
  → Week 24: Final polish

Flagship 2: Starts Week 12 (Agent v1)
  → Week 13: Agent v2 (MCP integration)
  → Week 15: Agent v3 (streaming, cost optimization)
  → Week 24: Final polish

Specialization: Week 16 (structured tracks)
```

**Why It Matters:**
- Iteration evidence (v1→v2→v3) signals engineering maturity to employers
- "Your Choice" is too vague; structured tracks provide clear deliverables
- Two deep projects beat three shallow ones

**Fix:** **Adopt LAYER1-FINAL flagship evolution model.**

---

## 🟡 MODERATE MISALIGNMENTS

### 1. MCP Coverage

**Modified:** Mentioned briefly
**LAYER1-FINAL:** Full Week 13 with MCP servers, A2A, security

**Impact:** MCP is becoming table stakes (OpenAI adoption, Assistants API sunset)

**Fix:** Add MCP week or integrate into Week 13 of modified.

---

### 2. System Design Practice

**Modified:** Not included
**LAYER1-FINAL:** Weeks 8, 12, 20, 26 (explicit system design days)

**Impact:** System design is a key interview differentiator

**Fix:** Add system design days to modified curriculum.

---

### 3. Frontend Scope (Week 21)

**Modified:** Full-stack with React/Next.js expected
**LAYER1-FINAL:** Streamlit-first, React optional (see WEEK-21-REFINED.md)

**Impact:** Modified sets students up for overwhelm and failure

**Fix:** Adopt LAYER1-FINAL WEEK-21-REFINED.md scope.

---

## ✅ WHAT'S ALIGNED (Keep As-Is)

The following modified curriculum components are **well-designed** and align with LAYER1-FINAL philosophy:

1. ✅ **Teaching Ladder (5 levels)** — Conceptually identical
2. ✅ **Checkpoint Types (4 types)** — Design, Implementation, Testing, Reflection
3. ✅ **Guided Discovery Philosophy** — TODOs over solutions
4. ✅ **Flex Weeks Concept** — Acknowledges learning friction
5. ✅ **Weekly Structure (20 hours)** — Same time commitment
6. ✅ **Phase Structure (5 phases)** — Logical progression

**These can be preserved** when migrating to LAYER1-FINAL.

---

## 📋 RECOMMENDED ACTIONS

### Option A: Full Migration to LAYER1-FINAL (RECOMMENDED)

**Steps:**
1. Archive `modified-curriculum/` as `modified-curriculum-ARCHIVED/`
2. Copy `LAYER1-FINAL/` to `Layer1-Curriculum/docs/LAYER1-FINAL/`
3. Update `DOCUMENTATION-INDEX.md` to point to LAYER1-FINAL
4. Update `IMPLEMENTATION-PROGRESS.md` to track LAYER1-FINAL completion

**Pros:**
- Single canonical curriculum (no confusion)
- All critical fixes applied (SQL, testing, security)
- Complete template set (logs, rubrics, diagnostic)

**Cons:**
- Requires updating existing links/references
- Some modified content becomes reference-only

---

### Option B: Hybrid Merge (COMPLEX)

**Steps:**
1. Keep modified curriculum structure (32 weeks → 28 weeks)
2. Replace Week 1 with LAYER1-FINAL Week 1 (SQL + FastAPI)
3. Replace Week 2 with LAYER1-FINAL Week 2 (Testing + Docker)
4. Add COST-LOG.md and FAILURE-LOG.md templates
5. Add Git collaboration workflow to Week 1
6. Replace Week 21 with WEEK-21-REFINED.md scope
7. Replace Week 32 "Your Choice" with Week 16 specialization tracks
8. Add checkpoint rubrics from LAYER1-FINAL

**Pros:**
- Preserves modified curriculum investments
- Incorporates LAYER1-FINAL improvements

**Cons:**
- Complex merge process
- Risk of inconsistencies
- Still two curricula to maintain

---

### Option C: Status Quo (NOT RECOMMENDED)

**Keep both curricula as-is.**

**Problems:**
- Students confused about which to follow
- Modified teaches SQL 26 weeks too late
- Missing critical components (logs, Git, rubrics)
- Maintenance burden doubled

**Verdict:** ❌ **Do not recommend.**

---

## 🎯 FINAL RECOMMENDATION

**Adopt Option A: Full Migration to LAYER1-FINAL**

**Rationale:**
1. LAYER1-FINAL is **market-calibrated** (SQL Week 1, testing threaded, security integrated)
2. LAYER1-FINAL has **complete template set** (logs, rubrics, diagnostic, Git)
3. **One canonical path** eliminates learner confusion
4. Modified curriculum requires **more fixes than preservation**

**Migration Plan:**

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Archive modified-curriculum as reference | Immediate |
| 2 | Copy LAYER1-FINAL to Layer1-Curriculum/docs/ | Immediate |
| 3 | Update DOCUMENTATION-INDEX.md | Week 1 |
| 4 | Update root README.md | Week 1 |
| 5 | Create student onboarding guide | Week 2 |
| 6 | Test with 2-3 beta students | Week 3-4 |
| 7 | Iterate based on feedback | Week 5-6 |

---

## 📊 ALIGNMENT SCORECARD

| Category | Score | Notes |
|----------|-------|-------|
| **Timeline & Structure** | 3/5 | 28 vs. 32 weeks, flex week mismatch |
| **Content Placement** | 1/5 | SQL Week 26 vs. Week 1 (critical) |
| **Project Structure** | 2/5 | 3 standalone vs. 2 evolving flagships |
| **Teaching Methodology** | 4/5 | Well-aligned conceptually |
| **Production Habits** | 1/5 | Missing logs, Git, cost tracking |
| **Documentation** | 2/5 | Many missing files in modified |
| **Overall** | **13/30 (43%)** | ⚠️ Partial alignment |

---

## 📝 FILES REQUIRING UPDATES

### Modified Curriculum Files to Update/Replace:

| File | Action | Reason |
|------|--------|--------|
| `docs/PRAGMATIC-CURRICULUM-OVERVIEW.md` | Replace | Timeline mismatch (32 vs. 28 weeks) |
| `docs/WEEK-BY-WEEK-ROADMAP.md` | Replace | SQL/Testing/Security placement wrong |
| `guides/TEACHING-METHODOLOGY.md` | Update | Add curriculum-specific guidance |
| `guides/CHECKPOINT-SYSTEM.md` | Replace | Use CHECKPOINT-RUBRICS.md |
| `IMPLEMENTATION-PROGRESS.md` | Update | Track LAYER1-FINAL progress |
| `README.md` | Replace | Point to LAYER1-FINAL as canonical |

### Files to Add to Modified:

| File | Source | Purpose |
|------|--------|---------|
| `PROGRESS-TRACKER.md` | LAYER1-FINAL | Student progress tracking |
| `COST-LOG.md` | LAYER1-FINAL | API cost tracking |
| `FAILURE-LOG.md` | LAYER1-FINAL | Weekly failure documentation |
| `CHECKPOINT-RUBRICS.md` | LAYER1-FINAL | Phase checkpoint questions |
| `GIT-COLLABORATION-WEEK1.md` | LAYER1-FINAL | Git branches, PRs, review |
| `WEEK-16-SPECIALIZATION.md` | LAYER1-FINAL | 3 specialization tracks |
| `WEEK-21-REFINED.md` | LAYER1-FINAL | Frontend scope refinement |
| `grade_diagnostic.py` | LAYER1-FINAL | Day 00 auto-grader |
| `DAY-00-DIAGNOSTIC.md` | LAYER1-FINAL | Diagnostic starter files |

---

## 🔥 HARD TRUTHS

1. **Modified curriculum teaches SQL 26 weeks too late.** This is indefensible given job market demands.

2. **Modified curriculum has students building 20 weeks of untested code.** Testing in Week 21 is an afterthought, not a habit.

3. **Modified curriculum lacks iteration evidence.** Three standalone flagships don't show v1→v2→v3 evolution.

4. **Modified curriculum is missing hiring differentiators.** No cost tracking, no failure logs, no Git collaboration.

5. **LAYER1-FINAL is the stronger curriculum.** It's market-calibrated, complete, and production-focused.

---

## ✅ CONCLUSION

**The modified curriculum has excellent pedagogical foundations** (teaching methodology, checkpoint system, guided discovery).

**However, critical content placement errors** (SQL Week 26, Testing Week 21) and **missing components** (logs, Git, rubrics, specialization) make it **unsuitable as the primary curriculum**.

**Recommendation:** **Archive modified-curriculum as reference, adopt LAYER1-FINAL as the single canonical path.**

---

**Review Completed By:** Bmad Master Analysis
**Date:** March 8, 2026
**Next Review:** After student testing (Week 4)

---

**Quick Links:**
- [LAYER1-FINAL Overview](../LAYER1-FINAL/README.md)
- [Modified Curriculum Overview](docs/PRAGMATIC-CURRICULUM-OVERVIEW.md)
- [Alignment Scorecard](#alignment-scorecard)
- [Recommended Actions](#-recommended-actions)
