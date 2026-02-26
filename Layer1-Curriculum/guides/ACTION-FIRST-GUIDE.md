# Action-First Teaching Guide for Layer 1

## Getting Learners to Working Code Before Deep Explanation

**Philosophy**: A learner who has seen their code work will read the explanation eagerly. A learner who has not yet run anything reads the explanation with resistance.
**Layer**: Layer 1 — The Mechanic Level
**Last Updated**: 2026-02-25
**Applies To**: All 40 days, especially Days 1–10 (Phase 1: Foundations)

---

## 🔬 Before You Write: Research Modern Technologies

**CRITICAL**: Before creating any curriculum content, research the latest and best technologies for the task. Layer 1 teaches production-ready practices, not legacy approaches.

### Pre-Writing Technology Research Checklist

- [ ] Search for current best practices using `mcp_exa_web_search_exa` (e.g., "best Python package manager 2026")
- [ ] Verify with real-world usage via `mcp_github_search_code` (check recent repos, GitHub stars)
- [ ] Compare modern vs traditional approaches (document the trade-offs)
- [ ] Test the modern approach in a fresh environment
- [ ] Include both modern (primary) and traditional (reference) in setup instructions

**Example**: When writing Day 1 setup, research reveals `uv` is 10-100x faster than `pip` with better dependency resolution. The curriculum should use `uv` as the primary approach, with traditional `venv + pip` shown for educational context.

**Why this matters**: Learners who use modern tools signal to employers they stay current with industry trends and make informed technical decisions. See WRITING-STYLE-GUIDE.md Pattern 8 for detailed technology selection standards.

---

## 🎯 The Core Insight

Traditional curriculum design front-loads theory. You teach what something is, then you teach how it works, then you let the learner try it. This order feels logical to subject-matter experts. It is disastrous for motivation.

**Traditional order** (loses learners):

```
Theory (10 min) → Mental model (5 min) → Context (5 min) → FINALLY: code (20+ min in)
```

By minute 20, short attention spans have checked out. The learner has not yet experienced anything — only been told things.

**Action-first order** (engages learners):

```
Minimal frame (2 min) → CODE SUCCESS (15 min) →
"What just happened?" → Deep understanding (NOW they want to know)
```

At minute 15, the learner has working output and a question. That question is the most powerful learning state that exists: _I just did something and I want to understand it._

Layer 1 is built around this sequence. Every day, every scaffold file, every README must honor it.

---

## 🧠 Why This Works: The Psychology

**Success creates curiosity.** A learner who has just made an LLM respond to their code is not the same learner as one who has only read about LLMs. The first learner asks "how did that work?" The second asks "why does this matter?"

**Context makes sense after experience.** The explanation of how the `messages` list works as stateless memory is abstract until the learner has built a chatbot that forgets who they are when the list is not maintained. After that experience, the explanation is self-evident.

**Detailed explanations are earned, not owed.** A learner who succeeded wants the full picture — they read every word of the deep explanation because they are building a mental model of something real. A learner who has not yet succeeded reads the explanation with suspicion: "I don't know if I'll ever actually need this."

---

## 📐 The Layer 1 Action-First Structure

### Phase 1: The Frame (0–5 min) — MINIMAL

This is the Mechanic's Analogy + Prime the Pump. It should be short enough to read in 2–3 minutes and specific enough to set the direction without explaining the destination.

**What belongs here**:

- One analogy that orients the day's work (the Mechanic's Analogy)
- The 2–3 mental models without which the first 15 minutes would be confusing
- Any resource (video, doc) that must be consumed first, with a time estimate
- The explicit instruction: "Go build this now. Understanding comes after."

**What does NOT belong here**:

- Comprehensive theory
- All the edge cases
- The full mental model
- Comparison tables
- Production considerations

**Target length**: 100–200 words total for Prime the Pump. The Mechanic's Analogy is 50–100 words. Combined: under 5 minutes to read.

**Example — Good Prime the Pump (Day 1)**:

```markdown
### Prime the Pump

Before you write any code, understand these two things:

**LLMs are next-token predictors.** You send a sequence of messages, the model
predicts what comes next, one token at a time. That's it. Everything else is
built on top of this.

**The API is stateless.** The model has no memory between calls. Every time you
call it, you send the entire conversation history. This is why "memory" costs
money — you're re-sending everything every time.

That's all you need to know to write the first script. Go.
```

**Example — Bad Prime the Pump (too comprehensive, delays action)**:

```markdown
### Prime the Pump

Large Language Models (LLMs) are transformer-based neural networks trained on
vast corpora of text data. They operate through a process called next-token
prediction, wherein the model calculates the probability distribution over all
possible tokens in its vocabulary and selects the most probable one...
[continues for 500 words before any code]
```

---

### Phase 2: First Wrench Turn (5–30 min) — MINIMAL CODE, MAXIMUM IMPACT

The First Wrench Turn is the action-first core. It should produce working output in under 30 minutes — ideally under 15. The goal is a single, undeniable success: code ran, AI responded, something happened.

**Rules for the First Wrench Turn**:

1. **Scaffold file only** — point to `hello.py` or the simplest file. Do not explain `chatbot.py` yet.
2. **State the target time explicitly**: "Aim for 15 minutes." This creates accountability and frames the complexity correctly.
3. **Give just enough guidance to start** — not enough to do it for them. The TODOs in the scaffold file carry the teaching.
4. **End with a success moment** — the scaffold file should print a congratulatory message (not just the AI's response) when it works.

**Example — First Wrench Turn section (Day 1)**:

```markdown
### First Wrench Turn — Get AI Talking (aim for 15 minutes)

Open `hello.py`. Fill in the TODOs. Run it.

When it works, you'll see an AI response in your terminal. That's the goal.
Don't add anything extra yet. Don't improve it. Just get those five lines working.

`python hello.py`
```

**What NOT to do in First Wrench Turn**:

```markdown
# ❌ Bad — gives away too much before the learner has tried

### First Wrench Turn

Create a file called hello.py with the following code:

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role": "user", "content": "Say hello!"}]
)
print(response.choices[0].message.content)
```

The First Wrench Turn provides direction, not implementation. The scaffold file handles the teaching.

---

### Phase 3: The Bridge (0–5 min) — WHAT JUST HAPPENED?

After the first successful run, the learner is in the optimal state for learning: they have experienced something and want to understand it. The Bridge is a short section (3–5 sentences maximum) that names what just happened and transitions to the deep explanation.

**Purpose**: Create the question in the learner's mind before providing the answer.

**Example — Good Bridge**:

```markdown
**You just did something real.**

Your code sent a message to one of the most advanced AI systems ever built,
and got a response back. That response was generated token by token, in
real time, using a transformer model with billions of parameters.

Now let's understand exactly what happened — and what you'll need to know
to build on this.
```

The Bridge is not a celebration section (save that for the README's "What You Built" closer). It is a pivot point: "you just did X, now let's understand X."

---

### Phase 4: Tighten the Bolts (60–120 min) — COMPREHENSIVE UNDERSTANDING

Once the learner has code running, the Tighten the Bolts section provides the full picture. This is where progressive complexity, failure diagnostics, interview anchors, and spaced repetition hooks all live.

**Now it is safe to cover**:

- The complete mental model for the concept
- Edge cases and failure modes
- Production considerations
- Cost implications
- Interview anchors for each concept
- Comparisons (cosine vs L2, OpenAI vs Anthropic, etc.)

**Structure within Tighten the Bolts**:

1. **Feature list with priority order**: Number the features in build order. The learner knows what to do next at every step.
2. **Concept explanation per feature**: Before each non-trivial feature, explain the concept it depends on. Keep it to 2–4 sentences — enough to act, not a lecture.
3. **Interview anchor per concept**: After each concept, the "What You'd Say in an Interview" block.
4. **Broken-state reference**: Point to the SELF-CHECK section in each scaffold file for failure diagnosis.
5. **Guidance section**: After all features are listed, a guidance section with the specific "how" for the trickiest parts — not a walkthrough, but targeted answers to predictable confusion.

**Example — Tighten the Bolts feature list (Day 1)**:

```markdown
### Tighten the Bolts

Now build a proper CLI chatbot with these features, in this order:

1. **Conversation loop** — keep chatting until the user types "quit"
2. **Message history** — the AI remembers what was said (hint: you accumulate messages in a list)
3. **System prompt** — give your chatbot a personality
4. **Streaming** — print tokens as they arrive instead of waiting for the full response
5. **Streamlit UI** — wrap your chatbot in a simple web interface

Open `chatbot.py` and `app.py`. The TODOs guide you through each feature.

### What's Happening Under the Hood

**Message history** is the most important thing to understand today. The API is
stateless — the model does not remember anything between calls. YOU send the entire
conversation history every time. This means:

- Turn 1 sends 1 message (your question)
- Turn 2 sends 3 messages (your question, AI's answer, your next question)
- Turn 10 sends 19 messages (the full conversation so far)

Cost grows with conversation length. In production, systems truncate old messages
or summarize them to keep costs manageable.

### What You'd Say in an Interview

> "I implemented conversation memory by accumulating all messages in a Python list
> and resending the full history on every API call. The model itself is stateless —
> it has no persistence between calls. This means cost scales with conversation
> length, which is why production systems use truncation or summarization."
```

---

### Phase 5: Road Test + Close (20–30 min)

The Road Test is a binary pass/fail gate. The close is a motivating forward bridge.

**Road Test principles**:

- Every item is verifiable without interpretation
- One item must test the critical failure mode (memory, streaming, etc.)
- Every file in the day's folder has at least one item

**Close principles**:

- Name what the learner can now do that they could not do at the start of the day
- Connect it to the next day's work explicitly
- Keep it to 3–5 sentences — momentum, not summary

**Example — Close section**:

```markdown
## You Built It

You have a working AI chatbot that streams responses, maintains conversation
context, and runs in a web UI. The same architecture — stateless API, accumulated
message history, streaming tokens — powers production applications at companies
like Notion, Intercom, and GitHub Copilot.

**Tomorrow**: You will learn to make the AI return exactly the data structure
you need, reliably. Structured outputs and prompt engineering — the foundation
of every AI-powered feature in production software.
```

---

## 📋 Action-First Implementation Checklist

Use this checklist when reviewing any day's content for action-first compliance:

- [ ] **Prime the Pump is under 200 words** (minimal frame, not comprehensive theory)
- [ ] **First Wrench Turn has an explicit target time** (15–30 min stated)
- [ ] **First Wrench Turn points to the simplest scaffold file only** (not the full day's files)
- [ ] **First Wrench Turn does not give away the implementation** (TODOs carry the teaching)
- [ ] **The Bridge appears after First Wrench Turn** (names what happened, pivots to depth)
- [ ] **Tighten the Bolts comes after the Bridge** (deep understanding after success, not before)
- [ ] **Tighten the Bolts has a numbered feature list** (learner knows what to do next at every step)
- [ ] **Interview anchor present per concept in Tighten the Bolts**
- [ ] **Day closes with a forward bridge** (what you built + what's next)

---

## ⚠️ Common Action-First Failures

### Failure 1: Prime the Pump becomes a lecture

**Symptom**: Prime the Pump is 400+ words and covers the full mental model before code
**Fix**: Cut everything that is not required to attempt the First Wrench Turn. Move the rest to Tighten the Bolts, after the learner has code running.

### Failure 2: The Bridge is missing

**Symptom**: After First Wrench Turn, the README jumps directly to Tighten the Bolts without acknowledging what just happened
**Fix**: Add 3–5 sentences that name what just worked and explicitly transition the learner into the "now I want to understand this" state.

### Failure 3: First Wrench Turn gives away the solution

**Symptom**: The README shows the complete implementation before the learner has tried
**Fix**: First Wrench Turn should say what to do and where to open — not how to implement it. The scaffold file's TODOs carry the how.

### Failure 4: Tighten the Bolts has no ordering

**Symptom**: The Tighten the Bolts section lists features but does not number them or tell the learner what order to tackle them
**Fix**: Number all features. State explicitly: "Build them in this order. Test each before moving to the next."

### Failure 5: Concept explanations precede the code that demonstrates them

**Symptom**: A concept explanation appears before the TODO that uses it
**Fix**: In Tighten the Bolts, the concept explanation for feature N should appear immediately before feature N's TODO — not in a separate section above all the TODOs.

---

## 📚 Related Guides

- `WRITING-STYLE-GUIDE.md` — Full voice, tone, and pattern standards
- `QUALITY-CHECKLIST.md` — Complete review criteria including action-first compliance
- `LANGUAGE-EXPANSION-GUIDE.md` — How to expand content once the ordering is correct

---

**Layer**: Layer 1 — The Mechanic Level
**Last Updated**: 2026-02-25
**Adapted from**: Layer 2 Action-First Deep-Dive Guide, compressed and reoriented for Layer 1 scaffold-file teaching model
