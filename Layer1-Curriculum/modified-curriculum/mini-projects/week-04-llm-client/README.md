# Mini-Project 1: Multi-Provider LLM Client

**Week 4 | Duration: 1 week | Difficulty: ⭐⭐**

---

## Problem Statement

Build a production-grade LLM client that:
- Supports multiple providers (OpenAI, Anthropic, Groq)
- Implements automatic fallback on failure
- Tracks token usage and cost
- Handles rate limits with retries
- Logs all requests for debugging

---

## Learning Goals

By completing this project, you will:
- ✅ Understand API design and error handling patterns
- ✅ Master async programming for I/O-bound operations
- ✅ Implement cost tracking and observability
- ✅ Test external APIs with mocking
- ✅ Build reusable, production-ready components

---

## Prerequisites

Before starting:
- [ ] Completed Week 3 (First LLM Call)
- [ ] Understand async/await basics
- [ ] Familiar with Pydantic models
- [ ] Have API keys for OpenAI (required), Anthropic (optional)

---

## Requirements

### Must Have (Core Features)
- [ ] Support 3+ providers with priority order
- [ ] Automatic fallback if primary fails
- [ ] Track tokens and cost per request
- [ ] Retry with exponential backoff for rate limits
- [ ] Structured logging (JSON format)
- [ ] Unit tests with mocked APIs
- [ ] Integration test with real API

### Nice to Have (Stretch Goals)
- [ ] Streaming support
- [ ] Caching layer
- [ ] Request/response validation
- [ ] Metrics dashboard

---

## Success Criteria

You've succeeded when:
- [ ] All tests pass
- [ ] Can explain fallback logic
- [ ] Can calculate cost accurately
- [ ] Logs are readable and useful
- [ ] Can demo to someone else

---

## Architecture Design (Do This First!)

### Before Writing Code

**Answer these questions:**

1. **Provider Priority**
   - How do you store the provider order?
   - How do you iterate through providers?
   - When do you stop trying providers?

2. **Error Handling**
   - What errors can happen?
   - Which errors should retry?
   - Which errors should fallback?
   - Which errors should fail immediately?

3. **Cost Tracking**
   - Where do you get token counts?
   - Where do you get pricing?
   - How do you handle unknown models?

4. **Testing Strategy**
   - How do you test without real API calls?
   - What scenarios to test?
   - How do you verify cost calculation?

**Draw this flow on paper:**
```
[User Request]
      ↓
[Try Provider 1] → Success? → [Return Response]
      ↓ Fail
[Log Error]
      ↓
[Try Provider 2] → Success? → [Return Response]
      ↓ Fail
[Log Error]
      ↓
[Raise Exception]
```

---

## Time Estimate

- **Design:** 1 hour (architecture, flow diagrams)
- **Implementation:** 4-6 hours (core features)
- **Testing:** 2-3 hours (unit + integration)
- **Documentation:** 1 hour (README, comments)

**Total:** ~8-11 hours over 1 week

---

## Getting Started

### Step 1: Setup (15 minutes)
```bash
cd mini-projects/week-04-llm-client
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### Step 2: Design (1 hour)
1. Read `hints/hint_01_architecture.md`
2. Draw your architecture diagram
3. Answer the design questions above
4. Review with someone (or rubber duck)

### Step 3: Implement (4-6 hours)
1. Start with `starter_code/models.py` (complete the TODOs)
2. Move to `starter_code/core.py` (implement the client)
3. Test as you go: `pytest tests/ -v`
4. Check `hints/hint_02_implementation.md` if stuck

### Step 4: Test (2-3 hours)
1. Complete `tests/test_core.py`
2. Run full test suite: `pytest tests/ -v --cov`
3. Aim for 80%+ coverage

### Step 5: Document (1 hour)
1. Write clear README
2. Add docstrings to functions
3. Document design decisions
4. Record a demo (optional but recommended)

---

## Project Structure

```
week-04-llm-client/
├── README.md                 # This file
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── .gitignore
│
├── starter_code/             # Your implementation goes here
│   ├── __init__.py
│   ├── models.py             # Pydantic models (partially complete)
│   ├── core.py               # Main client (TODOs)
│   └── utils.py              # Helper functions
│
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_models.py        # Model validation tests
│   ├── test_core.py          # Client tests (you complete)
│   └── test_integration.py   # Real API tests
│
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   └── advanced_usage.py
│
└── hints/                    # Progressive hints
    ├── hint_01_architecture.md
    ├── hint_02_implementation.md
    └── hint_03_debugging.md
```

---

## Learning Checkpoints

### Before Implementation
- [ ] Can draw the fallback flow
- [ ] Can explain why fallback order matters
- [ ] Can list 5 potential errors
- [ ] Can explain cost calculation approach

### During Implementation
- [ ] Can explain why async instead of sync
- [ ] Can explain exponential backoff
- [ ] Can explain provider abstraction
- [ ] Can explain error handling strategy

### After Implementation
- [ ] Can walk through the code with someone
- [ ] Can explain what happens if all providers fail
- [ ] Can calculate cost for a given request
- [ ] Can demonstrate the system working

### Final Checkpoint
**Explain to someone (or record yourself):**
1. Walk through the entire flow
2. Why did you choose this architecture?
3. What's the hardest bug you fixed?
4. What would you do differently?
5. How would you scale this to 10 providers?

---

## Common Pitfalls

### ❌ Pitfall 1: Not Handling All Errors
**Problem:** Only catching generic `Exception`  
**Fix:** Catch specific errors (RateLimitError, AuthError, TimeoutError)

### ❌ Pitfall 2: Hardcoding Provider Logic
**Problem:** Separate function for each provider  
**Fix:** Use strategy pattern or provider interface

### ❌ Pitfall 3: Forgetting to Log Failures
**Problem:** Silent failures make debugging impossible  
**Fix:** Log every attempt with error details

### ❌ Pitfall 4: Not Testing Edge Cases
**Problem:** Only testing happy path  
**Fix:** Test all failures, all providers fail, rate limits

### ❌ Pitfall 5: Blocking on Async Calls
**Problem:** Using sync code in async context  
**Fix:** Use `await` for all I/O operations

---

## Resources

### Documentation
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Anthropic API Docs](https://docs.anthropic.com/claude/reference)
- [Pydantic Docs](https://docs.pydantic.dev)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

### Concepts to Review
- Async/await in Python
- Exponential backoff
- Strategy pattern
- Mocking in tests
- Cost calculation

---

## Submission Checklist

Before moving to Week 5:
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code coverage >80% (`pytest --cov`)
- [ ] README is complete
- [ ] Design decisions documented
- [ ] Can explain to someone
- [ ] Passed all learning checkpoints

---

## What's Next?

After completing this project:
- **Week 5:** Wrap this client in a FastAPI service
- **Week 6:** Deploy the service with Docker
- **Week 12:** Use this client in your RAG system

This client becomes a **reusable component** for all future projects!

---

## Getting Help

### If Stuck (Try in Order)
1. **Timebox:** Spend 30 minutes trying yourself
2. **Hints:** Check `hints/hint_01_architecture.md`
3. **Examples:** Look at `examples/basic_usage.py`
4. **AI Assistant:** Ask for guidance (not solutions!)
5. **Community:** Post in Discord/Reddit with specific question

### Good Questions to Ask
- "I'm trying to implement fallback logic. Should I use a loop or recursion?"
- "My tests are failing with 'coroutine was never awaited'. What does this mean?"
- "How do I mock the OpenAI client in tests?"

### Bad Questions to Ask
- "Can you write the code for me?"
- "It doesn't work" (without error message)
- "What's the answer to TODO #3?"

---

## Reflection Questions

After completing the project, write answers to:

1. **What did you learn?**
   - What concept finally clicked?
   - What surprised you?

2. **What was hard?**
   - What took the longest?
   - What would you do differently?

3. **What's next?**
   - What would you add with more time?
   - How would you improve it?

---

**Ready to start? Begin with `starter_code/models.py`!**

**Remember:** The goal is not perfect code. The goal is working code that you understand.

Let's build. 🚀
