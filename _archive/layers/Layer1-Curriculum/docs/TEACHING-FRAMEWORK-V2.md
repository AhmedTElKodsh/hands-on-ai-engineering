# Layer 1 v2.0: 28-Week Production AI Engineer Curriculum

**Teaching Philosophy**: Action-first, production-ready, interview-calibrated
**Target Outcome**: Job-ready AI Engineer in 28 weeks (672 hours @ 4h/day, 6 days/week)
**Last Updated**: 2026-03-08
**Based On**: layer1-plan-v2-modified.md + Layer1 teaching methodologies

---

## 🎯 Core Teaching Principles (Adapted for v2.0)

### 1. Action-First, Depth Second
Every week follows: **Minimal frame (Day 1) → CODE SUCCESS (Days 1-2) → Deep understanding (Days 3-5) → Ship (Day 6)**

At Day 2, learners have working output. That success creates the curiosity needed for deep learning.

### 2. The Mechanic's Workflow (Weekly Structure)
Each week is a complete build cycle:
- **Days 1-2**: First Wrench Turn (core feature working)
- **Days 3-4**: Tighten the Bolts (extend + failure handling)
- **Day 5**: Road Test (evaluation + tests + improvement)
- **Day 6**: Polish (refactor + docs + demo + reflection)
- **Day 7**: Rest (mandatory)

### 3. Production Signals from Day 1
Not "toy demos" — every artifact includes:
- Tests (unit + integration)
- CI/CD (GitHub Actions from Week 1)
- Documentation (README with setup + architecture)
- Demo video (60-120 seconds)
- "What Failed & What Changed" section

### 4. Interview Anchoring Throughout
Every major concept closes with: **"What you'd say in an interview"**

Not just "know it" — practice saying it out loud.

### 5. Checkpoint Gates Prevent Gaps
5 explicit quality gates (Weeks 4, 8, 12, 16, 22) with pass/fail criteria.
**Quality > Speed** — if you fail a gate, spend 2-3 extra days fixing.

---

## 📚 Weekly Content Structure

### Week Template (Adapted from Mechanic's Workflow)

Each week's guide follows this structure:

```markdown
# Week X: [Feature Name]

## 🔧 The Mechanic's Analogy (50-100 words)
[One analogy framing the week's work]

## 🎯 This Week's Build
[What you're shipping by Day 6]

## 📋 Prerequisites
[What you need before starting]

---

## Day 1-2: First Wrench Turn

### Prime the Pump (15 minutes)
[Minimal concepts needed to start]

### Build Target (2-4 hours)
[Get something working fast]

### Success Criteria
- [ ] Feature X works
- [ ] Output matches expected
- [ ] Committed to Git

---

## Day 3-4: Tighten the Bolts

### Extend the Build (4-6 hours)
[Add complexity + failure handling]

### Deep Dive: [Concept]
[Now that it works, understand WHY]

### Interview Anchor
**"How would you explain [concept] in an interview?"**
[Practice answer]

---

## Day 5: Road Test

### Testing Checklist
- [ ] Unit tests for [X]
- [ ] Integration test for [Y]
- [ ] Property-based test for [Z]

### Evaluation
[Measure quality/performance]

### Improvement
[One measurable improvement]

---

## Day 6: Polish & Ship

### Refactor
[Clean up code]

### Documentation
- Update README
- Add architecture diagram
- Document "What Failed & What Changed"

### Demo Video (60-120s)
[Record walkthrough]

### Weekly Reflection (15 minutes)
[Use Appendix A template]

### Ship
- [ ] Tag release `v0.X.0`
- [ ] Push to GitHub
- [ ] CI passes

---

## 🎓 What Good Looks Like

[Concrete examples of quality]

## 🔍 Common Pitfalls

[What usually goes wrong + fixes]

## 📚 Resources

[Docs, videos, references]
```

---

## 🏗️ Phase-by-Phase Teaching Approach

### Phase 1: Foundation (Weeks 1-2)
**Teaching Focus**: Establish professional habits from Day 1

- **Heavy scaffolding**: Detailed TODOs with WHY/PATTERN/HINT
- **Success fast**: Working code in 15-30 minutes
- **Build confidence**: "I can do this"
- **Establish rhythm**: Daily commits, weekly ships

**Pedagogical Pattern**: Worked examples → Guided practice → Independent execution

---

### Phase 2: LLM Integration (Weeks 3-4)
**Teaching Focus**: Reliability before fancy features

- **Moderate scaffolding**: TODOs with patterns, fewer hints
- **Failure diagnosis**: Show broken output alongside working
- **Production thinking**: Retries, timeouts, cost tracking
- **Checkpoint Gate 1**: Quality gate at Week 4

**Pedagogical Pattern**: Problem → Attempt → Guided solution → Reflection

---

### Phase 3: RAG Core (Weeks 5-8)
**Teaching Focus**: Systematic experimentation

- **Light scaffolding**: Goal-driven challenges, minimal hints
- **Productive failure**: Try chunking strategies, measure, compare
- **Evidence-based decisions**: "I tested 3 approaches, here's why I chose X"
- **Checkpoint Gate 2**: RAG fundamentals at Week 8

**Pedagogical Pattern**: Hypothesis → Experiment → Measure → Iterate

---

### Phase 4: Production Backend (Weeks 9-12)
**Teaching Focus**: End-to-end ownership

- **Minimal scaffolding**: Requirements + architecture, you design
- **Real-world constraints**: Multi-tenancy, auth, rate limiting
- **Observability**: Instrument everything
- **Checkpoint Gate 3**: Production readiness at Week 12

**Pedagogical Pattern**: Requirements → Design → Build → Validate

---

### Flex Week A (Week 13)
**Teaching Focus**: Reflection and consolidation

- **No new content**: Catch up or deepen
- **Metacognition**: What's working? What's not?
- **Portfolio review**: External feedback
- **Energy check**: Adjust pace if needed

---

### Phase 5: Agents (Weeks 14-16)
**Teaching Focus**: Reasoning and tool safety

- **Build raw first**: Understand agent loop before frameworks
- **Then frameworks**: LangGraph for production
- **Tool governance**: Allowlists, scopes, audit logs
- **Checkpoint Gate 4**: Agent fundamentals at Week 16

**Pedagogical Pattern**: Raw implementation → Framework adoption → Production hardening

---

### Phase 6: Specialization (Week 17)
**Teaching Focus**: Decision-making skills

- **Explicit framework**: 4-step decision process
- **Job market analysis**: What do postings actually want?
- **Portfolio gaps**: What's missing from your artifacts?
- **ROI thinking**: Is this worth 1 week of effort?

**Pedagogical Pattern**: Analyze → Decide → Execute → Document rationale

---

### Phase 7: Deployment/Ops (Weeks 18-22)
**Teaching Focus**: Operational excellence

- **Real deployment**: Not localhost, actual cloud
- **Monitoring**: Nightly evals, alerting, rollback
- **Performance**: Measure, optimize, measure again
- **Security**: Defense-in-depth, testable
- **Checkpoint Gate 5**: Deployment readiness at Week 22

**Pedagogical Pattern**: Deploy → Monitor → Optimize → Harden

---

### Flex Week B (Week 23)
**Teaching Focus**: Preparation for capstone

- **Catch up**: Complete Gate 5 if needed
- **Deepen**: Optional framework survey
- **Plan capstone**: Domain selection, architecture

---

### Phase 8: Capstone (Weeks 24-26)
**Teaching Focus**: Synthesis and autonomy

- **Minimal guidance**: You own the system
- **All skills integrated**: RAG + agents + eval + observability + security
- **Portfolio quality**: This is what recruiters see
- **Iteration evidence**: "What Failed & What Changed"

**Pedagogical Pattern**: Design → Build → Evaluate → Iterate → Document

---

### Phase 9: Polish & Prep (Weeks 27-28)
**Teaching Focus**: Interview readiness

- **Portfolio polish**: Recruiter-friendly READMEs
- **System design practice**: RAG/agent architecture
- **Interview simulation**: "Build mini-RAG in 45 minutes"
- **Applications**: 10+ jobs, tailored resumes

**Pedagogical Pattern**: Practice → Feedback → Refine → Apply

---

## 🎓 Pedagogical Techniques (Evidence-Based)

### Retrieval Practice (Spaced Repetition)
- **Weekly reflection**: Recall previous concepts
- **Spaced review questions**: Every Day 6
- **Code rebuild challenges**: Recreate from scratch

### Productive Failure (Desirable Difficulty)
- **Phase 1-2**: Heavy scaffolding (prevent dropout)
- **Phase 3-4**: Light scaffolding (productive struggle)
- **Phase 5+**: Minimal scaffolding (autonomous building)

### Elaborative Interrogation (Self-Explanation)
- **WHY comments**: Explain every design decision
- **Interview anchors**: Practice explaining out loud
- **Logbook prompts**: Synthesis, not just recall

### Interleaving (Mixed Practice)
- **Week 5**: Chunking experiments (compare strategies)
- **Week 8**: Evaluation (multiple metrics)
- **Week 21**: Performance optimization (multiple approaches)

### Teaching Others (Feynman Technique)
- **Weekly reflection**: "Explain to a study buddy"
- **README documentation**: Write for others
- **Demo videos**: Teach by showing

---

## 🔍 Quality Signals (What Good Looks Like)

### Week 1-4: Foundation Quality
- ✅ Repo compiles, tests run in CI
- ✅ README has setup instructions (< 5 minutes)
- ✅ Code is typed (mypy passes)
- ✅ Commits are daily, messages are clear

### Week 5-12: Production Quality
- ✅ Tests cover core functionality (>70%)
- ✅ Integration tests hit real services
- ✅ Observability instrumented (logs, traces, metrics)
- ✅ Documentation includes architecture diagrams

### Week 13-22: Deployment Quality
- ✅ Deployed to cloud (not localhost)
- ✅ Monitoring dashboard shows real data
- ✅ Security hardened (18/20 prompt injection tests pass)
- ✅ Performance optimized (p95 < 2s)

### Week 23-28: Portfolio Quality
- ✅ Live demo (clickable link)
- ✅ Demo video (2-3 minutes)
- ✅ "What Failed & What Changed" documented
- ✅ Quantified results (metrics in tables)

---

## 📊 Success Metrics (Track Weekly)

### Weekly Checklist
- [ ] Artifact shipped and tagged
- [ ] Tests passing in CI
- [ ] Demo video recorded
- [ ] README updated
- [ ] Weekly reflection completed

### Monthly Checklist (Every 4 Weeks)
- [ ] Portfolio review with external feedback
- [ ] Cost tracking vs. budget
- [ ] Energy/motivation check (7+/10)
- [ ] Checkpoint gate passed (if applicable)

### Final Checklist (Week 28)
- [ ] 4-6 portfolio artifacts complete
- [ ] Flagship system deployed
- [ ] 10+ job applications submitted
- [ ] 3+ technical interviews scheduled

---

## 🎯 Interview Anchoring (Every Week)

### System Design Practice
Every major feature includes: **"How would you design this in an interview?"**

Example (Week 7 - RAG):
```
Interviewer: "Design a RAG system for customer support."

Your answer:
"I'd start with the data flow: documents → chunking → embeddings → vector store.
For chunking, I'd test recursive vs semantic and measure retrieval precision.
For retrieval, I'd use hybrid search (dense + BM25) with reranking.
For generation, I'd include citations and 'I don't know' handling.
For evaluation, I'd track faithfulness, relevance, and latency.
For production, I'd add multi-tenancy, auth, and cost tracking."
```

### Common Questions Mapped to Weeks
- "Explain embeddings" → Week 6
- "How do you evaluate RAG?" → Week 8
- "How do you handle prompt injection?" → Week 10, 22
- "Describe your deployment process" → Week 19
- "How do you monitor production systems?" → Week 20

---

## 🚀 Getting Started

### For Curriculum Creators
1. Use this guide as the teaching framework
2. Create weekly guides following the template above
3. Include checkpoint gate checklists (Appendix B)
4. Add "What Good Looks Like" examples (Appendix C)

### For Learners
1. Read this guide once (30 minutes)
2. Start with Week 1 in `layer1-plan-v2-modified.md`
3. Follow the daily structure religiously
4. Use weekly reflection template (Appendix A)
5. Don't skip checkpoint gates

---

## 📚 Related Documents

**In Project Root:**
- `layer1-plan-v2-modified.md` - Full 28-week plan with appendices
- `_bmad-output/README.md` - Analysis and comparison

**In Layer1-Curriculum/guides/:**
- `ACTION-FIRST-GUIDE.md` - Action-first teaching methodology
- `WRITING-STYLE-GUIDE.md` - Voice, tone, formatting standards
- `QUALITY-CHECKLIST.md` - Review criteria for content

**In Layer1-Curriculum/docs/:**
- `Extended-Plan.md` - Original Layer1 philosophy
- `DAILY-CURRICULUM-PLAN-V4.md` - 40-day detailed plan (reference)

---

## 🎓 Teaching Philosophy Summary

**Action before theory** - Code runs in 15 minutes, explanation follows
**Mechanic's language** - Practical, tool-focused, "here's what to turn"
**Interview anchoring** - Every concept → "What you'd say"
**Failure diagnosis** - Show broken output, explain fixes
**Scaffold progression** - Heavy → Light → Minimal
**Checkpoint gates** - Quality > Speed
**Weekly reflection** - Metacognition prevents burnout
**Production signals** - Tests, CI/CD, docs, demos from Day 1

---

**Created**: 2026-03-08
**Version**: 2.0 (aligned with layer1-plan-v2-modified.md)
**Status**: Ready for weekly guide creation
