# 🎓 Hands-On AI Engineering Curriculum

**Last Updated:** March 10, 2026  
**Status:** ✅ **Reorganized - Single Canonical Path**  

---

## 🚨 START HERE

### 👉 **Go to: [`LAYER1-FINAL/`](LAYER1-FINAL/)**

This is your **single canonical curriculum** for becoming an AI Engineer in 28 weeks.

**Quick Links:**
- 📚 **Main Curriculum:** [`LAYER1-FINAL/README.md`](LAYER1-FINAL/README.md)
- 📝 **Python Diagnostic:** [`LAYER1-FINAL/guides/DAY-00-DIAGNOSTIC.md`](LAYER1-FINAL/guides/DAY-00-DIAGNOSTIC.md)
- 📊 **Progress Tracker:** [`LAYER1-FINAL/guides/PROGRESS-TRACKER.md`](LAYER1-FINAL/guides/PROGRESS-TRACKER.md)
- 🤖 **For AI Assistants:** [`LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md`](LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md)

---

## 📋 What Changed (March 2026)

**We consolidated to a single, market-calibrated curriculum:**

| Before | After |
|--------|-------|
| ❌ Multiple curricula (Layer1, Layer2, Modified) | ✅ **Single path: LAYER1-FINAL** |
| ❌ SQL in Week 26 | ✅ **SQL in Week 1** |
| ❌ Testing in Week 21 | ✅ **Testing Week 2 + threaded** |
| ❌ Security in Week 23 | ✅ **Security Week 2 + threaded** |
| ❌ 32 weeks, 3 standalone flagships | ✅ **28 weeks, 2 evolving flagships** |

**Read the full story:** [`_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md`](_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md)

---

## 🎯 LAYER1-FINAL at a Glance

**Duration:** 28 weeks (672 hours @ 4h/day, 6 days/week)

**What You'll Build:**

### Flagship Product: Knowledge Assistant Platform
A production-style RAG + agent system with:
- 📊 Postgres with pgvector for hybrid storage
- 🔍 Advanced retrieval with reranking and citations
- 🤖 Tool-using agents with safety guardrails
- 📈 Evaluation harness with automated testing
- 👁️ Observability with OpenTelemetry tracing
- 🔒 Multi-tenant security with auth and rate limiting
- 🚀 Cloud deployment with CI/CD pipeline

### Portfolio Artifacts (5 Total)
1. **Structured Extraction Service** (Week 4)
2. **RAG v1 with Evaluation Harness** (Week 8)
3. **Productionized RAG Service** (Week 12)
4. **Agent + MCP Integration** (Week 15)
5. **Domain Capstone** (Weeks 23-25)

---

## 📅 28-Week Overview

| Phase | Weeks | Focus | Checkpoint |
|-------|-------|-------|------------|
| **Foundation** | 1-2 | FastAPI + SQL + Docker | - |
| **LLM Integration** | 3-4 | LLM client + structured outputs | ✅ Gate 1 (Week 4) |
| **RAG Core** | 5-8 | Ingestion + vectors + RAG + eval | ✅ Gate 2 (Week 8) |
| **Production Backend** | 9-12 | Multi-tenant + auth + CI/CD | ✅ Gate 3 (Week 12) |
| **Flex Week A** | 13 | Catch-up / Deepen | - |
| **Agents** | 14-16 | Raw agents + LangGraph + MCP | ✅ Gate 4 (Week 17) |
| **Specialization** | 17 | NL2SQL / Docs / Fine-tuning | - |
| **Deployment/Ops** | 18-22 | Cloud + monitoring + security | ✅ Gate 5 (Week 22) |
| **Flex Week B** | 23 | Catch-up / Deepen | - |
| **Capstone** | 24-26 | Domain system build | - |
| **Polish/Prep** | 27-28 | Portfolio + interviews | - |

---

## 🚀 Quick Start

### For New Students

1. **Read Decisions:** [`_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md`](_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md)
2. **Start Here:** [`LAYER1-FINAL/README.md`](LAYER1-FINAL/README.md)
3. **Take Diagnostic:** [`LAYER1-FINAL/guides/DAY-00-DIAGNOSTIC.md`](LAYER1-FINAL/guides/DAY-00-DIAGNOSTIC.md)
4. **Track Progress:** [`LAYER1-FINAL/guides/PROGRESS-TRACKER.md`](LAYER1-FINAL/guides/PROGRESS-TRACKER.md)

### For Current Students (Using Modified Curriculum)

**Migrate at your next phase boundary:**

| Your Week | Action |
|-----------|--------|
| **Weeks 1-4** | Finish Phase 1, migrate to LAYER1-FINAL Phase 2 |
| **Weeks 5-10** | Finish Phase 2, migrate to LAYER1-FINAL Phase 3 |
| **Weeks 11-16** | Finish Phase 3, migrate to LAYER1-FINAL Phase 4 |
| **Weeks 17+** | Finish current phase, migrate to LAYER1-FINAL Phase 5 |

**Full migration guide:** [`_PLANNING-2026-03/MIGRATION-GUIDE.md`](_PLANNING-2026-03/MIGRATION-GUIDE.md)

### For AI Assistants

**Teaching Guide:** [`LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md`](LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md)

**Key Principles:**
1. Use the 5-level teaching ladder
2. Verify understanding with checkpoints
3. Teach, don't vibe-code
4. Log failures as learning opportunities

---

## 📁 Folder Structure

```
hands-on-ai-engineering/
│
├── 📚 LAYER1-FINAL/                    # ✅ CANONICAL - START HERE
│   ├── README.md                       # Main curriculum
│   ├── guides/                         # Student guides
│   └── docs/                           # Supplementary docs
│
├── 📋 _PLANNING-2026-03/               # 📋 March 2026 Planning
│   ├── CURRICULUM-DECISIONS-2026-03.md # ⭐ Read this first
│   ├── FOLDER-ORGANIZATION-2026-03.md  # Folder structure guide
│   ├── MIGRATION-GUIDE.md              # Migration instructions
│   └── cleanup-old-folders.ps1         # Cleanup script
│
├── 🗄️ _ARCHIVE_2026-03/                # ⚠️ Archived (Reference)
│   ├── ARCHIVED-Layer1-Curriculum/
│   ├── ARCHIVED-Layer2-Curriculum/
│   └── ARCHIVED-layer1-phase1/
│
├── 📚 docs/                            # Supplementary docs
├── 💡 examples/                        # Code examples
├── 📖 books/                           # Recommended reading
└── 🔧 shared/                          # Shared resources
```

---

## 🎓 Learning Philosophy

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

### Weekly Deliverables

Every week ends with:
- ✅ Tagged GitHub release (`v0.X.0`)
- ✅ Demo video (60-120 seconds)
- ✅ README update with "What Failed & What Changed"
- ✅ 15-minute reflection

---

## 🎯 What Makes This Different

| Feature | Other Curricula | LAYER1-FINAL |
|---------|----------------|--------------|
| **SQL Placement** | Late or missing | **Week 1** (with FastAPI) |
| **Testing** | One week | **Week 2 + threaded** throughout |
| **Security** | Bolted on late | **Week 2 + threaded** throughout |
| **Cost Tracking** | Not included | **Week 3 onward** (weekly logs) |
| **Failure Logging** | Not included | **Weekly mandatory** |
| **System Design** | Not included | **Weeks 8, 12, 20, 26** |
| **MCP** | Mentioned | **Week 13** (full week) |
| **Flagships** | 3 standalone | **2 evolving** (v1→v2→v3) |
| **Flex Weeks** | 0-4 weeks | **2 weeks** (buffer built-in) |

---

## 📞 Need Help?

### Documentation

- **Curriculum Decisions:** [`_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md`](_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md)
- **Folder Organization:** [`_PLANNING-2026-03/FOLDER-ORGANIZATION-2026-03.md`](_PLANNING-2026-03/FOLDER-ORGANIZATION-2026-03.md)
- **Migration Guide:** [`_PLANNING-2026-03/MIGRATION-GUIDE.md`](_PLANNING-2026-03/MIGRATION-GUIDE.md)

### In LAYER1-FINAL

- **Main Curriculum:** [`LAYER1-FINAL/README.md`](LAYER1-FINAL/README.md)
- **Teaching Guide:** [`LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md`](LAYER1-FINAL/guides/GUIDE-FOR-AI-ASSISTANTS.md)
- **Checkpoints:** [`LAYER1-FINAL/guides/CHECKPOINT-RUBRICS.md`](LAYER1-FINAL/guides/CHECKPOINT-RUBRICS.md)

---

## ✅ Cleanup Status

**Reorganization:** ✅ **COMPLETE** (March 10, 2026)

**Archives Created:**
- ✅ `_ARCHIVE_2026-03/ARCHIVED-Layer1-Curriculum/`
- ✅ `_ARCHIVE_2026-03/ARCHIVED-Layer2-Curriculum/`
- ✅ `_ARCHIVE_2026-03/ARCHIVED-layer1-phase1/`

**Planning Docs:**
- ✅ `_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md`
- ✅ `_PLANNING-2026-03/FOLDER-ORGANIZATION-2026-03.md`
- ✅ `_PLANNING-2026-03/MIGRATION-GUIDE.md`

**Ready to Cleanup:**
- ⏳ Run: `_PLANNING-2026-03/cleanup-old-folders.ps1`
- ⏳ Verify LAYER1-FINAL still exists
- ⏳ Update any broken links

---

## 🎉 Ready to Start?

### Your First Steps

1. **Read:** [`_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md`](_PLANNING-2026-03/CURRICULUM-DECISIONS-2026-03.md) (5 min)
2. **Go to:** [`LAYER1-FINAL/`](LAYER1-FINAL/) 
3. **Take:** [`DAY-00-DIAGNOSTIC`](LAYER1-FINAL/guides/DAY-00-DIAGNOSTIC.md) (90 min)
4. **Start:** Week 1 of [`LAYER1-FINAL/README.md`](LAYER1-FINAL/README.md)

**Let's build. 🚀**

---

**Last Updated:** March 10, 2026  
**Curriculum Version:** LAYER1-FINAL (28 weeks, market-calibrated)  
**Status:** ✅ Production-Ready
