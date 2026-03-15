# Cost Log — Layer 1 Final (28-Week AI Engineer Accelerator)

**Student Name:** ___________________
**Start Date:** ___________________
**Last Updated:** ___________________

---

## 📊 WHY TRACK COSTS?

**Purpose:**
- Build cost awareness for production AI systems
- Understand token economics
- Make informed model selection decisions
- Demonstrate business awareness to employers

**What to Track:**
- Every LLM API call (OpenAI, Anthropic, etc.)
- Embedding generation costs
- Local model costs (electricity/time if relevant)
- Cloud infrastructure costs (optional but recommended)

**Update Frequency:** Every study day (Days 1-5 each week)

---

## WEEK 3: FIRST LLM INTEGRATION

### Week 3 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Prompt testing | OpenAI | GPT-4o | | | | |
| | Prompt testing | OpenAI | GPT-4o-mini | | | | |
| | Prompt testing | Anthropic | Claude-3.5-Sonnet | | | | |
| | Data extractor | OpenAI | GPT-4o | | | | |
| | Local model | Ollama | Mistral-7B | N/A | N/A | $0.00 | Local |

**Weekly Totals:**
- **Total Spend:** $__________
- **Most Expensive Task:** _________________________________
- **Cheapest Alternative Found:** _________________________________
- **Optimization Idea for Next Week:** _________________________________

---

## WEEK 4: EMBEDDINGS + VECTOR SEARCH

### Week 4 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Embedding generation | OpenAI | text-embedding-3-small | | | | |
| | Embedding generation | OpenAI | text-embedding-3-large | | | | |
| | Embedding generation | Cohere | embed-v3 | | | | |
| | Retrieval tests | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Most Expensive Task:** _________________________________
- **Best Cost/Quality Model:** _________________________________
- **Optimization Idea:** _________________________________

---

## WEEK 5: RAG PIPELINE V1

### Week 5 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | RAG answer generation | | | | | | |
| | Citation tracking | | | | | | |
| | Testing/evaluation | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Average Cost per RAG Query:** $__________
- **Queries This Week:** _____
- **Optimization Idea:** _________________________________

---

## WEEK 6: RAG PIPELINE V2 (ADVANCED RETRIEVAL)

### Week 6 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Reranking | Cohere | rerank-v3 | | | | |
| | HyDE implementation | | | | | | |
| | Multi-query (×3 queries) | | | | | | |
| | Parent-child retrieval | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cost Impact of Reranking:** $__________ per query
- **Cost Impact of Multi-Query:** $__________ per query
- **Is the quality improvement worth the cost?** ⬜ Yes ⬜ No
- **Optimization Idea:** _________________________________

---

## WEEK 7: RAG EVALUATION

### Week 7 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | RAGAS evaluation (LLM-as-judge) | | | | | | |
| | Faithfulness scoring | | | | | | |
| | Answer relevancy scoring | | | | | | |
| | 8+ config A/B tests | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Evaluation Cost (one full run):** $__________
- **Number of Configurations Tested:** _____
- **Best Cost/Performance Config:** _________________________________
- **Optimization Idea:** _________________________________

---

## WEEK 8: LANGCHAIN + LLAMAINDEX

### Week 8 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | LangChain RAG | | | | | | |
| | LlamaIndex RAG | | | | | | |
| | LangSmith tracing | | | | | | |
| | Framework comparison tests | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Framework Overhead Cost:** (which framework uses more tokens?)
- **LangSmith Cost:** $__________
- **Optimization Idea:** _________________________________

---

## WEEK 10: PRODUCTION RAG DEPLOYMENT

### Week 10 Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Production API calls | | | | | | |
| | Cloud infrastructure | AWS/GCP | | N/A | N/A | | Compute + DB |
| | Redis caching | | | N/A | N/A | | |
| | Load testing | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cloud Infrastructure Cost:** $__________
- **Cost per Query (Production):** $__________
- **Cache Hit Rate:** _____%
- **Cost Savings from Caching:** $__________
- **Optimization Idea:** _________________________________

---

## WEEK 11-15: AGENTS PHASE

### Week 11: Agent Fundamentals

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | ReAct agent loops | | | | | | |
| | Tool execution (×5 tools) | | | | | | |
| | Multi-step tasks | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Average Cost per Agent Task:** $__________
- **Most Expensive Tool:** _________________________________
- **Optimization Idea:** _________________________________

---

### Week 12: LangGraph

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | LangGraph agent | | | | | | |
| | Human-in-the-loop | | | | | | |
| | Agentic RAG routing | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cost Impact of Human-in-the-Loop:** $__________
- **Optimization Idea:** _________________________________

---

### Week 13: MCP

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | MCP server calls | | | | | | |
| | Multi-tool workflows | | | | | | |
| | A2A communication | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **MCP Overhead Cost:** $__________
- **Optimization Idea:** _________________________________

---

### Week 14: Multi-Agent Systems

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | CrewAI crew | | | | | | |
| | LangGraph multi-agent | | | | | | |
| | Agent evaluation (10 tasks) | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cost per Multi-Agent Task:** $__________
- **CrewAI vs LangGraph Cost:** _________________________________
- **Optimization Idea:** _________________________________

---

### Week 15: Advanced Agent Patterns

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Streaming agent | | | | | | |
| | Model routing (cheap→expensive) | | | | | | |
| | Checkpoint/resume | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cost Savings from Model Routing:** $__________
- **Percentage of Tasks Handled by Cheap Model:** _____%
- **Optimization Idea:** _________________________________

---

## WEEK 17-22: PRODUCTION ENGINEERING

### Week 17: LLMOps + Observability

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Experiment tracking | | | | | | |
| | Prompt A/B tests | | | | | | |
| | Monitoring overhead | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **LLMOps Tool Cost:** $__________
- **Optimization Idea:** _________________________________

---

### Week 18: Auth + Multi-Tenancy

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Multi-tenant RAG | | | | | | |
| | Per-tenant cost tracking | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cost per Tenant (average):** $__________
- **Optimization Idea:** _________________________________

---

### Week 19: Cloud Deployment

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Cloud inference (Bedrock/Vertex) | | | | | | |
| | K8s cluster | AWS/GCP | | N/A | N/A | | Compute |
| | Managed services comparison | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Cloud Infrastructure:** $__________
- **Managed AI Service:** $__________
- **Cost Comparison (API vs Managed):** _________________________________
- **Optimization Idea:** _________________________________

---

### Week 21: Full-Stack UI

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | UI-driven queries | | | | | | |
| | Streaming responses | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Average Cost per UI Session:** $__________
- **Optimization Idea:** _________________________________

---

### Week 22: Security + Ethics

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Security audit tests | | | | | | |
| | PII detection | | | | | | |
| | Moderation layer | | | | | | |

**Weekly Totals:**
- **Total Spend:** $__________
- **Security/Moderation Overhead:** $__________ per query
- **Optimization Idea:** _________________________________

---

## WEEK 23-24: CAPSTONE INTEGRATION

### Capstone Cost Summary

| Date | Task | Provider | Model | Input Tokens | Output Tokens | Cost (USD) | Notes |
|------|------|----------|-------|--------------|---------------|------------|-------|
| | Flagship #1 final | | | | | | |
| | Flagship #2 final | | | | | | |
| | Load testing | | | | | | |
| | Optimization runs | | | | | | |

**Total Capstone Spend:** $__________

---

## 📊 CUMULATIVE COST ANALYSIS

### Total Costs by Phase

| Phase | Total Spend | Key Learnings |
|-------|-------------|---------------|
| Phase 1 (Weeks 1-4) | $__________ | |
| Phase 2 (Weeks 5-10) | $__________ | |
| Phase 3 (Weeks 11-16) | $__________ | |
| Phase 4 (Weeks 17-22) | $__________ | |
| Phase 5 (Weeks 23-28) | $__________ | |
| **GRAND TOTAL** | **$__________** | |

---

### Cost Optimization Wins

**Best Optimization #1:**
- What: _________________________________
- Savings: $__________ per week
- Implementation: _________________________________

**Best Optimization #2:**
- What: _________________________________
- Savings: $__________ per week
- Implementation: _________________________________

**Best Optimization #3:**
- What: _________________________________
- Savings: $__________ per week
- Implementation: _________________________________

---

### Model Selection Decisions

| Use Case | Chosen Model | Why | Cost/Month at Scale |
|----------|--------------|-----|---------------------|
| Simple Q&A | | | |
| Complex reasoning | | | |
| Embeddings | | | |
| Reranking | | | |
| Agent tasks | | | |

---

### Production Cost Estimates

**If deployed to 1000 users/day:**
- **Current cost per query:** $__________
- **Queries per day (estimated):** _____
- **Daily cost:** $__________
- **Monthly cost:** $__________

**After optimizations:**
- **Optimized cost per query:** $__________
- **Optimized daily cost:** $__________
- **Optimized monthly cost:** $__________
- **Monthly savings:** $__________

---

## 💡 COST OPTIMIZATION PLAYBOOK

### Strategies Tried

| Strategy | Tried? (Y/N) | Savings | Quality Impact | Worth It? |
|----------|--------------|---------|----------------|-----------|
| Caching (Redis) | | | | |
| Model routing (cheap→expensive) | | | | |
| Prompt optimization | | | | |
| Smaller models for simple tasks | | | | |
| Batch processing | | | | |
| Local models (Ollama) | | | | |
| Response streaming | | | | |
| Context compression | | | | |

---

### Lessons Learned

**What I learned about LLM costs:**
1. _________________________________
2. _________________________________
3. _________________________________

**What I'd do differently in production:**
1. _________________________________
2. _________________________________
3. _________________________________

---

**Remember:** Cost awareness is a hiring differentiator. Employers want engineers who build systems that are not just functional, but economically viable.

**Last Updated:** ___________________
