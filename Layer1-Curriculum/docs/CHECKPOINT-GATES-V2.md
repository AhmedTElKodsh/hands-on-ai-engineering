# Checkpoint Gates: Quality Assurance for Layer 1 v2.0

**Purpose**: Explicit pass/fail criteria for 5 checkpoint gates
**Philosophy**: Quality > Speed - Better to spend 2-3 extra days fixing than advance with gaps
**Based On**: layer1-plan-v2-modified.md Appendix B
**Last Updated**: 2026-03-08

---

## 🎯 Why Checkpoint Gates Matter

**The Problem**: Learners advance with gaps, compound confusion, eventually quit.

**The Solution**: 5 explicit quality gates that prevent advancement until fundamentals are solid.

**The Rule**: If you fail a gate, spend 2-3 extra days fixing. Use Flex Weeks (13, 23) if needed.

---

## ✅ Gate 1: Portfolio Artifact Quality (Week 4)

**What You're Validating**: Structured Extraction Service is production-quality

### Pass Criteria

#### Functionality (Must Pass All)
- [ ] Extraction works on 10/10 test documents (100% success rate)
- [ ] Validation catches malformed outputs (test with 5 deliberately broken inputs)
- [ ] Retry logic improves success rate (measure: attempts 1 vs 2 vs 3)
- [ ] Confidence scores are reasonable (0.0-1.0 range, correlate with quality)

#### Security (Must Pass All)
- [ ] Adversarial tests documented (minimum 5 attack vectors)
- [ ] Prompt injection test fails safely (doesn't return fake data)
- [ ] Input sanitization works (test with: empty, too long, non-English, special chars)
- [ ] Mitigations documented in README

#### Code Quality (Must Pass All)
- [ ] Code is typed (mypy passes with no errors)
- [ ] Tests pass in CI (GitHub Actions green)
- [ ] Test coverage > 70% (run `pytest --cov`)
- [ ] No commented-out code or TODOs left

#### Documentation (Must Pass All)
- [ ] Demo video shows end-to-end flow (60-120 seconds)
- [ ] README has "What Failed & What Changed" section
- [ ] Architecture diagram present (Mermaid or image)
- [ ] Setup instructions work (test in fresh environment)

### Common Failures & Fixes

**Failure**: Extraction works on toy examples but fails on real documents
- **Fix**: Test with messy real-world data (PDFs with tables, scanned images, multi-column)
- **Time**: +1 day

**Failure**: Prompt injection test succeeds (returns fake data)
- **Fix**: Implement instruction hierarchy, sanitize inputs, add output verification
- **Time**: +1 day

**Failure**: No evidence of iteration in README
- **Fix**: Document v1 → v2 → v3 with metrics showing improvement
- **Time**: +0.5 day

### Self-Assessment Questions

1. **Would you deploy this to production?** (If no, what's missing?)
2. **Could someone else run this in 5 minutes?** (Test with a friend)
3. **Can you explain every design decision?** (Practice out loud)

### If You Fail This Gate

**Spend 2-3 extra days fixing.** Do NOT advance to Week 5 until this passes.

**Priority order**:
1. Fix functionality (extraction must work)
2. Fix security (prompt injection must fail safely)
3. Fix documentation (README must be complete)
4. Polish code quality (types, tests, formatting)

---

## ✅ Gate 2: RAG Fundamentals (Week 8)

**What You're Validating**: RAG system with evaluation harness is working and measurable

### Pass Criteria

#### Evaluation Infrastructure (Must Pass All)
- [ ] Evaluation harness runs automatically (single command)
- [ ] Evaluation dataset has 50+ Q/A pairs (from your corpus)
- [ ] Metrics are reproducible (same results on re-run)
- [ ] Cost per eval run is tracked (tokens + $)

#### Quality Metrics (Must Meet Targets)
- [ ] Faithfulness > 0.70 (LLM-as-judge or RAGAS)
- [ ] Retrieval Precision@5 > 0.60 (relevant docs in top 5)
- [ ] Answer relevance > 0.70 (answers the question)
- [ ] Latency p95 < 3s (acceptable for most use cases)

#### Iteration Evidence (Must Pass All)
- [ ] At least one A/B test documented (e.g., chunking strategy comparison)
- [ ] Metrics show measurable improvement from baseline (v1 → v2 → v3)
- [ ] README explains trade-offs (quality vs latency vs cost)
- [ ] Demo video shows before/after comparison

#### Production Readiness (Must Pass All)
- [ ] Citations link back to source chunks (traceable)
- [ ] "I don't know" triggers correctly (test with out-of-domain questions)
- [ ] Reranking improves relevance (measure with/without)
- [ ] Debug endpoint shows full pipeline (retrieval → rerank → generation)

### Common Failures & Fixes

**Failure**: Metrics don't improve from v1 to v2
- **Fix**: Try different chunking strategies, add reranking, tune retrieval threshold
- **Time**: +1-2 days

**Failure**: Evaluation is not reproducible (different results each run)
- **Fix**: Set random seeds, use deterministic models, version eval dataset
- **Time**: +0.5 day

**Failure**: No A/B test documented
- **Fix**: Compare 2 approaches (e.g., fixed vs recursive chunking), measure, document
- **Time**: +1 day

### Self-Assessment Questions

1. **Can you explain why your RAG system works?** (Not just "it works")
2. **What would you change if latency was critical?** (Trade-offs)
3. **How would you debug a bad answer?** (Use debug endpoint)

### If You Fail This Gate

**Spend 2-3 extra days fixing.** RAG quality is critical for everything that follows.

**Priority order**:
1. Fix evaluation infrastructure (must run automatically)
2. Improve metrics to targets (iterate on chunking/retrieval)
3. Document iteration (show v1 → v2 → v3)
4. Add production features (citations, "I don't know", debug)

---

## ✅ Gate 3: Production Readiness (Week 12)

**What You're Validating**: Service is production-grade with CI/CD, tests, and observability

### Pass Criteria

#### CI/CD Pipeline (Must Pass All)
- [ ] CI/CD pipeline runs automatically (GitHub Actions or equivalent)
- [ ] Pipeline includes: lint, type-check, test, build Docker image
- [ ] Integration tests pass in CI (spin up docker-compose, hit endpoints)
- [ ] Docker image builds successfully (no errors)

#### Testing (Must Pass All)
- [ ] Test coverage > 70% (run `pytest --cov`)
- [ ] Unit tests for core functions (chunking, embedding, retrieval)
- [ ] Integration tests for endpoints (test real Postgres, real LLM)
- [ ] Property-based test for critical invariant (e.g., "retrieval respects tenant boundaries")

#### Performance (Must Meet Targets)
- [ ] Load test shows acceptable performance (p95 < 2s for `/ask` endpoint)
- [ ] Load test completes without errors (10 concurrent users, 100 requests)
- [ ] Bottlenecks identified (database? LLM? retrieval?)
- [ ] Performance benchmarks documented in README

#### Observability (Must Pass All)
- [ ] Structured logs with correlation IDs (JSON format)
- [ ] Traces show all spans (API → retrieval → rerank → LLM)
- [ ] Metrics dashboard exists (latency, cost, error rate)
- [ ] Dashboard shows real data (not mock)

#### Documentation (Must Pass All)
- [ ] README has complete deployment instructions
- [ ] Architecture diagram shows all components
- [ ] "What Good Looks Like" examples included
- [ ] Someone else can deploy (test with peer)

### Common Failures & Fixes

**Failure**: Integration tests fail in CI but pass locally
- **Fix**: Check environment variables, database state, network access
- **Time**: +1 day

**Failure**: Load test shows p95 > 5s
- **Fix**: Profile code, optimize database queries, add caching, use faster LLM
- **Time**: +1-2 days

**Failure**: Observability dashboard shows no data
- **Fix**: Verify instrumentation, check log aggregation, test trace propagation
- **Time**: +0.5 day

### Self-Assessment Questions

1. **Could you deploy this to production tomorrow?** (What's missing?)
2. **How would you debug a slow request?** (Use traces)
3. **What breaks first under load?** (Identify bottleneck)

### If You Fail This Gate

**Spend 2-3 extra days fixing.** Production readiness is non-negotiable.

**Priority order**:
1. Fix CI/CD (must run automatically)
2. Fix tests (coverage > 70%, integration tests pass)
3. Fix performance (p95 < 2s)
4. Fix observability (traces + metrics working)

---

## ✅ Gate 4: Agent Fundamentals (Week 16)

**What You're Validating**: Agent system with MCP integration is safe and auditable

### Pass Criteria

#### Agent Functionality (Must Pass All)
- [ ] Agent completes multi-step tasks (test with 20 eval tasks)
- [ ] Task completion rate > 70% (14/20 tasks succeed)
- [ ] Agent reasons about tool selection (not random)
- [ ] Agent handles tool failures gracefully (retry, fallback, or fail safely)

#### MCP Integration (Must Pass All)
- [ ] MCP integration works end-to-end (agent discovers and uses tools)
- [ ] MCP server responds to discovery requests (test with curl)
- [ ] Agent can invoke MCP tools (test with 3 different tools)
- [ ] Tool responses are parsed correctly (no JSON errors)

#### Tool Governance (Must Pass All)
- [ ] Tool allowlist blocks unauthorized tools (test with disallowed tool)
- [ ] Tool scopes enforced (read-only vs read-write)
- [ ] Per-tool rate limits work (test by exceeding limit)
- [ ] Tool governance is configurable (per-tenant allowlists)

#### Audit & Safety (Must Pass All)
- [ ] Audit logs capture all tool calls (tool name, inputs, outputs, timestamp)
- [ ] Audit logs are complete (no missing calls)
- [ ] Audit logs are searchable (query by tool, user, time range)
- [ ] Sensitive data is redacted (API keys, PII)

#### Evaluation (Must Pass All)
- [ ] Agent eval harness works (automated testing)
- [ ] Metrics tracked: completion rate, tool call count, latency, cost
- [ ] Evaluation is reproducible (same results on re-run)
- [ ] Demo video shows real use case (not toy example)

### Common Failures & Fixes

**Failure**: Agent completion rate < 70%
- **Fix**: Improve prompts, add more tools, better error handling, clearer instructions
- **Time**: +1-2 days

**Failure**: Tool allowlist doesn't block unauthorized tools
- **Fix**: Implement allowlist check before tool execution, add tests
- **Time**: +0.5 day

**Failure**: Audit logs missing some tool calls
- **Fix**: Add logging at tool execution layer, verify all code paths
- **Time**: +0.5 day

### Self-Assessment Questions

1. **Would you trust this agent with production data?** (Why or why not?)
2. **How would you debug a failed task?** (Use audit logs)
3. **What's the worst thing this agent could do?** (Test that scenario)

### If You Fail This Gate

**Spend 2-3 extra days fixing.** Agents are critical for many roles.

**Priority order**:
1. Fix agent functionality (completion rate > 70%)
2. Fix MCP integration (end-to-end working)
3. Fix tool governance (allowlist, scopes, rate limits)
4. Fix audit logs (complete, searchable, redacted)

---

## ✅ Gate 5: Deployment Readiness (Week 22)

**What You're Validating**: System is deployed, monitored, optimized, and secured

### Pass Criteria

#### Deployment (Must Pass All)
- [ ] Application deployed to cloud (not localhost)
- [ ] Public demo endpoint works (password-protected)
- [ ] HTTPS enabled (valid SSL certificate)
- [ ] Secrets loaded correctly (from cloud secrets manager)

#### Monitoring & Alerting (Must Pass All)
- [ ] Monitoring dashboard shows real data (not mock)
- [ ] Nightly synthetic evals run automatically (scheduled job)
- [ ] Alerts trigger correctly (test by violating SLO)
- [ ] Ops runbook is complete (how to respond to alerts)

#### Performance (Must Meet Targets)
- [ ] Latency reduced by 20%+ from baseline (measure before/after)
- [ ] Cost reduced by 30%+ from baseline (measure before/after)
- [ ] Quality maintained (eval metrics stable or improved)
- [ ] Optimizations are configurable (can toggle on/off)

#### Security (Must Pass All)
- [ ] 18/20 prompt injection tests pass (defense-in-depth)
- [ ] PII redacted in logs (test with sample PII)
- [ ] Audit log is complete (who accessed what, when)
- [ ] Threat model documented (attack vectors + mitigations)

#### Operational Excellence (Must Pass All)
- [ ] Rollback procedure tested (revert to previous version)
- [ ] Rollback works (system recovers)
- [ ] Cost tracking operational (daily cost visible)
- [ ] Deployment is repeatable (documented, automated)

### Common Failures & Fixes

**Failure**: Prompt injection tests succeed (attacks work)
- **Fix**: Implement defense-in-depth (input sanitization, instruction hierarchy, tool restrictions, output verification)
- **Time**: +1-2 days

**Failure**: Monitoring dashboard shows no data
- **Fix**: Verify instrumentation, check data pipeline, test metric collection
- **Time**: +0.5 day

**Failure**: Performance not improved
- **Fix**: Profile code, identify bottlenecks, implement optimizations (caching, model routing, context compression)
- **Time**: +1-2 days

### Self-Assessment Questions

1. **Would you be comfortable on-call for this system?** (Why or why not?)
2. **How would you respond to a cost spike alert?** (Use runbook)
3. **What's the recovery time if deployment fails?** (Test rollback)

### If You Fail This Gate

**Spend 2-3 extra days fixing.** Production readiness is the goal.

**Priority order**:
1. Fix deployment (must be live in cloud)
2. Fix security (18/20 prompt injection tests pass)
3. Fix monitoring (dashboard + alerts working)
4. Fix performance (latency -20%, cost -30%)

---

## 🎯 Using Checkpoint Gates Effectively

### Before Each Gate

**1 week before**:
- [ ] Review gate criteria
- [ ] Identify gaps
- [ ] Plan fixes

**3 days before**:
- [ ] Run self-assessment
- [ ] Fix critical gaps
- [ ] Test everything

**1 day before**:
- [ ] Final verification
- [ ] Document results
- [ ] Prepare for gate

### At Each Gate

**Run all checks**:
- [ ] Go through criteria one by one
- [ ] Mark pass/fail for each
- [ ] Document failures

**If you pass**:
- [ ] Celebrate! 🎉
- [ ] Tag release
- [ ] Move to next phase

**If you fail**:
- [ ] Don't panic - this is normal
- [ ] Prioritize fixes (see "Priority order" above)
- [ ] Spend 2-3 extra days
- [ ] Re-test

### After Each Gate

**Reflect**:
- What was hardest?
- What would you do differently?
- What did you learn?

**Update portfolio**:
- Add gate completion to README
- Update demo video if needed
- Document improvements

---

## 📊 Gate Completion Tracking

Use this table to track your progress:

| Gate | Week | Status | Date Passed | Notes |
|------|------|--------|-------------|-------|
| Gate 1 | 4 | ⏳ Pending | - | Portfolio Artifact Quality |
| Gate 2 | 8 | ⏳ Pending | - | RAG Fundamentals |
| Gate 3 | 12 | ⏳ Pending | - | Production Readiness |
| Gate 4 | 16 | ⏳ Pending | - | Agent Fundamentals |
| Gate 5 | 22 | ⏳ Pending | - | Deployment Readiness |

**Status codes**:
- ⏳ Pending
- 🔄 In Progress
- ✅ Passed
- ❌ Failed (fixing)

---

## 🚀 Remember

**Quality > Speed**

It's better to spend 2-3 extra days fixing gaps than to advance with weak foundations.

Use Flex Weeks (13, 23) if you need catch-up time.

Every gate you pass makes you more job-ready.

---

**Created**: 2026-03-08
**Version**: 2.0 (aligned with layer1-plan-v2-modified.md)
**Status**: Ready for use
