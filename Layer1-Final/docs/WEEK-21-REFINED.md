# Week 21: Full-Stack AI Application — Refined Scope

**Version:** 1.0 — March 2026
**Purpose:** Clarify frontend expectations and prevent overwhelm

---

## ⚠️ SCOPE WARNING

**This week is aggressive.** The original curriculum expects:
- Streamlit advanced features
- HTML/CSS/JS basics
- React/Next.js sprint
- WebSocket streaming
- User feedback loops

**Reality check:** Most AI engineer roles **do not require React**. Streamlit is sufficient for demos and portfolios.

---

## 🎯 PRIORITIZED DELIVERABLES

### MUST HAVE (Core Requirements — All Students)

| Priority | Deliverable | Time Estimate | Why It Matters |
|----------|-------------|---------------|----------------|
| **P1** | Streamlit UI (multi-page, session state, caching) | 2 days | Demonstrates full-stack capability, sufficient for demos |
| **P1** | Basic chat interface with streaming | 1 day | Shows real-time LLM integration |
| **P1** | Source citations display | 0.5 days | Critical for RAG trust |
| **P1** | Feedback collection (thumbs up/down) | 0.5 days | Shows production thinking |
| **P2** | Responsive design (mobile-friendly) | 0.5 days | Basic UX consideration |
| **P2** | Simple analytics dashboard | 0.5 days | Shows data awareness |

**Total Core Time:** ~5 days (20 hours)

---

### SHOULD HAVE (Stretch Goals — If Time Permits)

| Priority | Deliverable | Time Estimate | Why It Matters |
|----------|-------------|---------------|----------------|
| **P3** | Conversation history sidebar | 0.5 days | UX improvement |
| **P3** | Query suggestions/autocomplete | 0.5 days | Shows advanced thinking |
| **P3** | Export conversations (PDF/Markdown) | 0.5 days | Practical feature |

**Total Stretch Time:** ~1.5 days (6 hours)

---

### NICE TO HAVE (Optional — Only If Targeting Full-Stack Roles)

| Deliverable | Time Estimate | When to Do |
|-------------|---------------|------------|
| React chat component | 1-2 days | Only if you have frontend experience or targeting full-stack roles |
| WebSocket streaming (advanced) | 1 day | Only after core is complete |
| Custom CSS theming | 0.5 days | Only for portfolio polish |

---

## 📅 REVISED DAY-BY-DAY PLAN

### Day 86: Streamlit Foundations

**Learning (80 min):**
- Streamlit installation + basic concepts
- `st.chat_message`, `st.session_state`, `st.cache_data`
- Multi-page apps with `st.pages`

**Build (120 min):**
- Basic chat UI with message history
- Session state for conversation persistence
- Caching for expensive operations (embeddings, LLM calls)

**Production Habit (40 min):**
- Push to GitHub with screenshots
- Add to FAILURE-LOG.md

**Checkpoint:**
- [ ] Chat UI displays messages
- [ ] Session state persists across reruns
- [ ] Caching reduces redundant API calls

---

### Day 87: Advanced Streamlit Features

**Learning (80 min):**
- Sidebar navigation
- File upload for documents
- Configuration options (model selection, temperature)
- Progress indicators

**Build (120 min):**
- Multi-page app: Home, Chat, Documents, Settings
- Document upload → ingestion pipeline
- Model selection dropdown
- Real-time progress bar for long operations

**Production Habit (40 min):**
- Write README section on Streamlit decisions
- Update COST-LOG.md

**Checkpoint:**
- [ ] Multi-page navigation works
- [ ] Document upload triggers ingestion
- [ ] Settings affect LLM behavior

---

### Day 88: Chat Interface + Streaming

**Learning (80 min):**
- Streaming responses with `st.empty()`
- Displaying citations/sources
- Typing indicators

**Build (120 min):**
- Streaming chat interface (token-by-token display)
- Source citations below each answer
- "Thinking..." indicator during LLM call

**Production Habit (40 min):**
- Record 30-second demo GIF
- Update FAILURE-LOG.md

**Checkpoint:**
- [ ] Streaming works smoothly
- [ ] Citations display correctly
- [ ] No UI flickering during streaming

---

### Day 89: Feedback + Analytics

**Learning (80 min):**
- Feedback collection patterns
- Basic analytics visualization
- Storing feedback in PostgreSQL

**Build (120 min):**
- Thumbs up/down buttons per response
- Optional feedback text field
- Simple analytics: queries/day, avg. rating, popular queries
- Store feedback in PostgreSQL

**Production Habit (40 min):**
- Push analytics dashboard screenshots
- Update COST-LOG.md

**Checkpoint:**
- [ ] Feedback buttons work
- [ ] Feedback stored in database
- [ ] Analytics dashboard displays data

---

### Day 90: Polish + Deployment

**Learning (80 min):**
- Streamlit Cloud deployment
- Responsive design basics
- Error handling in UI

**Build (120 min):**
- Deploy to Streamlit Cloud
- Mobile-responsive layout
- Error boundaries (graceful failures)
- Final README with setup instructions

**Production Habit (40 min):**
- Record 2-minute demo video
- Write "What I learned about frontend" reflection
- Update FAILURE-LOG.md

**Checkpoint:**
- [ ] Deployed and accessible via URL
- [ ] Works on mobile
- [ ] Errors handled gracefully
- [ ] Demo video recorded

---

## 🚨 COMMON PITFALLS + SOLUTIONS

### Pitfall 1: React Overwhelm

**Problem:** Student has no frontend experience, tries to learn React in 1 day.

**Solution:**
```
Skip React entirely. Streamlit is sufficient for AI engineer roles.

Focus on:
- Streamlit chat interface (core)
- Streaming responses
- Feedback collection

React is optional only if:
- You have prior frontend experience
- You're targeting full-stack roles
- You have extra time after core is complete
```

---

### Pitfall 2: WebSocket Complexity

**Problem:** Student tries to implement WebSocket streaming before mastering basic streaming.

**Solution:**
```
Use Server-Sent Events (SSE) or HTTP streaming first.

Streamlit + FastAPI streaming:
```python
# FastAPI endpoint
@app.post("/chat/stream")
async def chat_stream(query: str):
    async for token in llm.generate_stream(query):
        yield token

# Streamlit client
response = requests.post(url, stream=True)
for chunk in response.iter_content():
    st.empty().write(chunk.decode())
```

WebSocket is optional. HTTP streaming works for 95% of demos.
```

---

### Pitfall 3: Over-Engineering the UI

**Problem:** Student spends 3 days on custom CSS instead of core functionality.

**Solution:**
```
Use Streamlit's default theme. It's fine.

Priority order:
1. Core functionality works (chat, streaming, citations)
2. Feedback collection
3. Analytics
4. Custom theming (only if time permits)

Ugly but functional > Beautiful but broken.
```

---

### Pitfall 4: Ignoring Mobile

**Problem:** UI only works on desktop, breaks on mobile.

**Solution:**
```
Test on mobile early (Day 87).

Streamlit is mobile-responsive by default, but:
- Avoid wide tables
- Use `st.columns` for layout
- Test on your phone before deployment
```

---

## 📝 CHECKPOINT QUESTIONS (Week 21 End)

Answer these before proceeding to Week 22:

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | Why use Streamlit for AI demos instead of React? | - Faster development (hours vs. days)<br>- Built-in components for chat, file upload, etc.<br>- Sufficient for demos and portfolios<br>- Most AI engineer roles don't require React |
| **2** | What's the value of a standalone UI vs. API only? | - Demonstrates full-stack capability<br>- Easier for non-technical stakeholders to evaluate<br>- Shows user empathy (not just backend thinking)<br>- Better portfolio piece (visual + interactive) |
| **3** | How do you collect and use user feedback? | - Thumbs up/down per response<br>- Optional text field for detailed feedback<br>- Store in database with query/response<br>- Analyze patterns: which queries get low ratings?<br>- Use to improve RAG/agent behavior |

---

## 🎯 ALTERNATIVE PATHS

### Path A: Backend-Focused Student (Recommended for 80%)

**Goal:** Demonstrate full-stack capability without frontend depth.

**Deliverables:**
- Streamlit UI (all P1 items)
- Basic analytics dashboard
- Deployed and accessible

**Time:** 4-5 days

**Skip:** React, WebSocket, custom CSS

---

### Path B: Full-Stack Aspirational Student

**Goal:** Demonstrate both backend and frontend skills.

**Deliverables:**
- Streamlit UI (all P1 items)
- React chat component (basic)
- WebSocket streaming (if time permits)

**Time:** 6-7 days (use flex time if needed)

**Note:** Only choose this path if you have prior frontend experience.

---

### Path C: Time-Crunched Student

**Goal:** Minimum viable UI for portfolio.

**Deliverables:**
- Streamlit chat interface (P1 only)
- Deployed with demo video

**Time:** 3 days

**Skip:** Analytics, feedback, multi-page, responsive polish

**Make up:** Use Week 27 flex time to add feedback + analytics.

---

## 📊 SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| Streamlit UI deployed | ✅ Yes | Live URL |
| Streaming works | ✅ Yes | Demo video |
| Feedback collection | ✅ Yes | Database entries |
| Mobile-responsive | ✅ Yes | Test on phone |
| Demo video recorded | ✅ Yes | 2-minute video |

---

## 🔗 RESOURCES

### Streamlit
- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit for AI Chatbots](https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-community-cloud)

### Alternatives to Streamlit
- [Gradio](https://www.gradio.app) — Even simpler, good for demos
- [Chainlit](https://chainlit.io) — Chat-optimized, LangChain integration

### If You Choose React
- [Next.js Tutorial](https://nextjs.org/learn)
- [Vercel AI SDK](https://sdk.vercel.ai/docs) — Streaming helpers

---

## 💡 FINAL ADVICE

**From AI Engineers Who've Been Hired:**

> "I built my RAG demo in Streamlit. Interviewers cared that it worked, not what framework I used."
> — Senior AI Engineer at Big Tech

> "Don't waste weeks on React. Build the AI system, wrap it in Streamlit, ship it."
> — AI Startup CTO

> "I've hired 5 AI engineers. None of them needed to know React. All of them needed to know RAG."
> — Engineering Manager

---

**Remember:** The goal is not to become a frontend engineer. The goal is to demonstrate your AI system works end-to-end.

**Ship it. Polish it later.** 🚀

**Last Updated:** March 8, 2026
