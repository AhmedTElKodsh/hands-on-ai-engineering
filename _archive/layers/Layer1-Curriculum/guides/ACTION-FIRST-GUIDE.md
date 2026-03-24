# Action-First Teaching Guide for Layer 1

## Getting Learners to Working Code Before Deep Explanation

**Philosophy**: A learner who has seen their code work will read the explanation eagerly. A learner who has not yet run anything reads the explanation with resistance.
**Layer**: Layer 1 — The Mechanic Level
**Last Updated**: 2026-03-03
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

**Why this matters**: Learners who use modern tools signal to employers they stay current with industry trends and make informed technical decisions. See WRITING-STYLE-GUIDE.md Pattern 9 for detailed technology selection standards.

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

## 🔬 What the Research Actually Says: Evidence-Based Learning Strategies

The action-first approach is grounded in cognitive science research. However, "action first" alone is insufficient — **which type of action** matters enormously. The following table summarizes the evidence:

| Strategy | Evidence Strength | Source | Present in Current Curriculum? | Recommendation |
|---|---|---|---|---|
| **Retrieval practice** (test yourself with delay) | Very strong | Roediger & Butler 2011 | Weak — delay too short between notebook and scaffold files | Require code rebuild from scratch the next morning |
| **Productive failure** (struggle before solution) | Strong | Kapur 2008, 2014 | Absent — solution structure given before learner attempts | Add goal-driven challenges before revealing scaffolding |
| **Elaborative interrogation** (explain WHY each line) | Strong | Dunlosky 2013 | Partially — WHY comments exist but learner doesn't generate them | Add self-explanation checkpoints after key TODOs |
| **Interleaving** (mix problem types) | Strong | Rohrer 2012 | Absent — all Day 1 problems use same API | Mix in debugging tasks, code reading, API exploration |
| **Spaced repetition** (revisit after days) | Very strong | Ebbinghaus, Cepeda 2006 | Present in curriculum design via review questions | Strengthen by requiring code rebuilds, not just verbal recall |
| **Self-explanation** (explain code to yourself line by line) | Strong | Chi 1989 | Absent — no explicit prompt to explain code | Add "say out loud" checkpoints in scaffold files |
| **Worked examples** (study solved problems) | Strong for novices | Sweller 1988 | Present — concepts notebook serves this role | Keep but sequence AFTER an initial attempt (productive failure) |
| **Teaching others** (Feynman technique) | Strong | Roscoe & Chi 2007 | Logbook attempts this but easily skipped | Make it explicit: "Explain this to your study buddy" |
| **Desirable difficulty** (effortful processing) | Strong | Bjork 1994 | Low — scaffolding removes most difficulty | Reduce scaffolding density in Tighten the Bolts |

### Key Insight: The Scaffolding Paradox

Layer 1's exhaustive scaffolding (WHY/PATTERN/HINT for every TODO) is simultaneously its greatest strength and greatest weakness:

- **Strength**: It prevents learner dropout. Nobody quits because they're stuck on a cryptic TODO.
- **Weakness**: It caps learning at Bloom's Level 2–3 (Understanding/Applying). The learner never makes structural decisions, discovers failures through experience, or designs solutions from problem statements.

**The resolution**: Use heavy scaffolding for Phase 1 (First Wrench Turn) and lighter, goal-driven challenges for Phase 2 (Tighten the Bolts). The learner succeeds quickly (motivation preserved) and then struggles productively (deep learning activated).

### The Productive Failure Sequence (For Tighten the Bolts)

Replace the current pattern:

```
Current:  Explain concept → Show pattern → Hint → Build (transcription)
```

With:

```
Improved: State goal → Let learner attempt → They hit the wall → Explain why → Rebuild with understanding
```

**Example — chatbot.py conversation memory**:

```
CURRENT (recipe):
  "The API is stateless. Here's a diagram of the messages list growing.
   Here are the steps: a) init list, b) append user, c) call API, d) append assistant.
   Now implement it."

IMPROVED (productive failure):
  "Goal: Build a chatbot where the AI remembers your name after 3 turns.
   You have the API call pattern from hello.py. Build it. Test with 'What's my name?'
   [learner discovers the AI has amnesia because they only sent the last message]
   NOW read the concept explanation below about stateless APIs and message accumulation."
```

The failure teaches in 30 seconds what the diagram teaches in 5 minutes of passive reading — and the understanding is 10x deeper because it was discovered, not received.

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

## 🧪 Strengthening Retrieval Practice

The concepts notebook → close → build pattern is framed as retrieval practice, and the instinct is correct. But the execution undermines it:

1. The learner runs all notebook cells (seeing exact solutions)
2. Closes the notebook
3. Opens the scaffold file (which has the same patterns, hinted)
4. "Builds from memory" — but the notebook was open **10 minutes ago**

This is **short-term recall**, not retrieval practice. Cognitive science distinguishes between testing after 10 minutes (minimal benefit) and testing after a delay or context shift (significant benefit).

### Fixing Retrieval Practice in the Curriculum

**Level 1 — Within the same day** (minimum viable fix):

After the learner completes `chatbot.py`, add this instruction to the README:

```markdown
### Memory Lock (15 min — do not skip)

Close all files. Take a 5-minute break. Walk around.

When you return, open a new empty file called `chatbot_v2.py`.
Rebuild the conversation loop from memory — no peeking at chatbot.py or the notebook.

You will forget things. That is the point. Every gap you discover and fill yourself
is a concept that moves from "I read about it" to "I understand it."

When you're done, compare with chatbot.py. Note what you forgot.
```

**Level 2 — Across days** (stronger, recommended):

```markdown
### Day 2 Morning Warm-Up (20 min — before touching Day 2 code)

Open a new empty file. Without looking at any Day 1 code:

1. Write a script that sends one message to the API and prints the response
2. Add a conversation loop with memory
3. Add streaming

Time yourself. What did you remember? What did you forget?
This is the real measure of what you learned yesterday.
```

**Level 3 — Weekly rebuilds** (strongest):

At the end of each week (Days 5, 10, etc.), the learner rebuilds a simplified version of the week's key project from scratch. No references. This is the single highest-leverage intervention for long-term retention.

---

## 🎯 Scope Management: Depth Over Breadth

### The Scope Problem

A common failure in action-first curricula is compensating for the delayed theory by **adding more features** to demonstrate more concepts. This creates the illusion of comprehensive coverage while preventing deep understanding of any single concept.

**Day 1 example**: The current Day 1 covers API fundamentals, token counting, streaming, multi-turn memory, system prompts, Streamlit's execution model, web UI construction, and cross-provider comparison. That is 8 distinct concepts in 4 hours.

### The Fix: Fewer Concepts, Deeper Understanding

**Rule**: Each day should deeply cover 3–4 core concepts. Additional concepts belong on subsequent days.

**Day 1 recommended scope**:
- Core (must-have): API call, message roles, conversation memory, streaming
- Move to Day 2–3: Streamlit UI (this is web framework knowledge, not LLM knowledge)
- Keep as optional: Cross-provider comparison

**What to do with the freed time**: Spend it on **experiments** with the CLI chatbot:
- Try different system prompts and observe behavior changes
- Deliberately break memory (only send last message) and diagnose
- Observe token growth over 20 turns — watch the cost counter climb
- Implement a `/clear` command that resets conversation history
- Try sending a conversation with no system message — what changes?

These experiments build understanding. A Streamlit wrapper builds a demo.

### The Streamlit Question

Streamlit on Day 1 is pedagogically suspect for two reasons:

1. **It teaches web framework patterns**, not LLM patterns. Session state, rerun model, chat components — none of this is LLM knowledge.
2. **It creates the illusion of progress without depth.** The learner has a pretty chatbot in the browser but cannot, from a blank file, reconstruct the message accumulation pattern that makes it work.

**Recommendation**: Move Streamlit to Day 3 or later. On Day 1, the learner should be able to explain and rebuild the core API interaction — not just wrap it in a UI they don't deeply understand.

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
**Last Updated**: 2026-03-03
**Adapted from**: Layer 2 Action-First Deep-Dive Guide, compressed and reoriented for Layer 1 scaffold-file teaching model
