# Layer 1 Curriculum Quality Checklist

## Review Tool for the Mechanic-Level AI Engineering Bootcamp

**Purpose**: Verify every day's content meets Layer 1 quality standards before it is used with learners
**Layer**: Layer 1 — The Mechanic Level
**Usage**: Self-review by content author, then peer review before publishing
**North Star**: A learner who completes this day can build the thing AND explain it in an interview

---

## 🎯 How to Use This Checklist

### Review Process

1. **Author self-review**: Check your own day's content against every item before calling it done
2. **Peer review**: A second reviewer checks using the same list
3. **Learner test**: If possible, have one learner attempt the day — note where they get stuck

### Priority Levels

- 🔴 **Critical**: The day cannot be published without this. If absent, the learner will fail silently or learn incorrectly.
- 🟡 **Important**: Significantly affects learning quality. Should be resolved before publishing.
- 🟢 **Enhancement**: Improves quality but is not blocking.

### Scoring

- **45–50 checks**: ✅ Excellent — ready to use
- **38–44 checks**: ⚠️ Good — minor revisions needed
- **30–37 checks**: ⚠️ Adequate — significant improvements required
- **< 30 checks**: ❌ Insufficient — major revision required

---

## 📋 The Checklist

### Section 1: Structural Completeness (10 items)

#### 1.1 Required Sections Present 🔴

- [ ] **Mechanic's Analogy** present and scoped to 50–100 words
- [ ] **Prime the Pump** present (100–200 words; conceptual minimum only — not comprehensive)
- [ ] **First Wrench Turn** present with explicit target time (15–30 min) and scaffold file reference
- [ ] **Tighten the Bolts** present with full feature list and scaffold file references
- [ ] **Road Test Checklist** present with binary pass/fail items
- [ ] **Spaced Review** present with questions from 2+ days ago (not just yesterday)
- [ ] **Logbook Prompts** present (synthesis questions, not recall)
- [ ] **What You Built / What's Next** section closes the README (3–5 sentences)
- [ ] **Interview Anchor Block** present for every major concept in the day
- [ ] **Git Checkpoint** instruction present (commit command + message format)

**Score**: \_\_\_/10

---

### Section 2: Scaffold File Quality (10 items)

#### 2.1 TODO Standards 🔴

- [ ] **Continuous numbering**: TODOs numbered sequentially across the entire file without gaps or restarts inside functions
- [ ] **Three-part TODOs**: Every TODO includes (a) what to do, (b) WHY it matters, (c) a HINT — never a solution
- [ ] **Hint taxonomy used**: `# HINT:` (conceptual), `# PATTERN:` (structural), `# EXPECTED:` (output) used consistently
- [ ] **Navigation comment**: Files with TODOs spanning multiple functions have an `IMPLEMENTATION ORDER` comment near the top
- [ ] **Broken-state diagnostics**: `WHAT BROKEN LOOKS LIKE` section present and placed early (not buried at end)
- [ ] **Broken states covered**: At least two failure modes described with symptom, diagnosis, and fix
- [ ] **SELF-CHECK section**: Present at the end with expected working output and expected broken output side by side
- [ ] **Inline references**: TODOs that are confusing reference the SELF-CHECK section explicitly
- [ ] **Python version guard**: `hello.py`-style entry scripts check `sys.version_info >= (3, 10)`
- [ ] **No solution leakage**: TODOs provide hints and patterns but do not give the complete implementation

**Score**: \_\_\_/10

---

### Section 3: Learning Method Quality (12 items)

#### 3.1 Action-First Ordering 🔴

- [ ] **Code runs within 15–30 min**: The First Wrench Turn delivers a working output before any extended theory
- [ ] **Theory follows success**: Conceptual depth in Tighten the Bolts comes after the learner has code running, not before
- [ ] **Prime the Pump is minimal**: Does not attempt to cover everything — only covers what's needed to make the first 15 minutes coherent

#### 3.2 Interview Readiness 🔴

- [ ] **Interview anchor per concept**: Every significant concept has a "What You'd Say in an Interview" block
- [ ] **First-person framing**: Interview anchors are written as the learner would say them ("I built...", "I implemented...")
- [ ] **Technical specificity**: Each interview anchor includes at least one specific architectural detail
- [ ] **Production consideration**: Each interview anchor includes at least one "in production you'd..." statement
- [ ] **Answer length**: Interview anchors are under 100 words — concise by design

#### 3.3 Spaced Review Integration 🟡

- [ ] **Cross-day questions**: Spaced review draws from at least 2 different prior days (not just Day N-1)
- [ ] **Verbal recall instruction**: The README explicitly says "answer out loud before checking your notes"
- [ ] **Graduated difficulty**: Review questions for older material are harder than review questions for yesterday's material
- [ ] **Logbook synthesis**: Logbook prompts require application, speculation, or cross-concept connection — not factual recall

**Score**: \_\_\_/12

---

### Section 4: Mechanic's Voice & Tone (8 items)

#### 4.1 Voice Consistency 🟡

- [ ] **Mechanic's Analogy is in the garage domain**: Day-opening analogy maps to car/engine/garage vocabulary
- [ ] **No "just" or "simply"**: These words do not appear in the content
- [ ] **No "wall of bullets"**: Conceptual explanations are in narrative prose; bullets used only for steps or checklists
- [ ] **Direct address**: Content speaks to "you" (the learner), not "students" or "users" or "developers"
- [ ] **Failure acknowledged**: At least one point in the day where difficulty is openly acknowledged
- [ ] **No phantom audience**: No "some learners might..." — always direct ("you might find that...")
- [ ] **Active voice**: "You will build" not "It will be built"
- [ ] **Mechanic celebrates at the right moment**: Celebration language appears at genuine milestones, not on every trivial step

**Score**: \_\_\_/8

---

### Section 5: Concept Explanation Quality (8 items)

#### 5.1 Depth and Accuracy 🔴

- [ ] **"Why" before "how"**: For every major concept, the motivation appears before the mechanism
- [ ] **Failure modes covered**: Every major concept includes what breaks and how to diagnose it
- [ ] **Concrete output shown**: Every scaffold file shows what correct output looks like (not just "it works")
- [ ] **Concepts tied to interview questions**: Every concept has an explicit connection to how it would appear in an interview

#### 5.2 Progressive Complexity 🟡

- [ ] **Simple mental model first**: Abstract concepts introduced with a simple mental model before adding nuance
- [ ] **Nuance in Tighten the Bolts**: The deeper, more accurate explanation comes after the learner has used the concept
- [ ] **Analogy per concept**: At least one analogy per major new concept (drawn from the Analogy Library or the mechanic domain)
- [ ] **Cost implications called out**: Wherever API costs are relevant (token counts, message history length), the cost implication is stated explicitly

**Score**: \_\_\_/8

---

### Section 6: Road Test Checklist Quality (5 items)

#### 6.1 Checklist Rigor 🔴

- [ ] **Binary items only**: Every checklist item can be verified as pass or fail without interpretation
- [ ] **Covers all scaffold files**: Every `.py` file in the day's folder has at least one checklist item
- [ ] **Memory test included**: At least one item tests that conversation context is working (ask "what did I just say?")
- [ ] **Security item included**: `.env` not in git / API key not hardcoded item is present on relevant days
- [ ] **No optional items in Road Test**: Optional items are in a separate "Stretch Goals" section

**Score**: \_\_\_/5

---

### Section 7: Code Quality (8 items)

#### 7.1 Code Standards 🔴

- [ ] **Runnable**: All code in scaffold files and README examples can be run in a fresh virtual environment
- [ ] **Pinned dependencies**: `requirements.txt` has pinned versions (not floating)
- [ ] **Error handling shown**: At least one example of error handling for common failure modes (API errors, etc.)
- [ ] **No "..." abbreviations**: Code blocks are complete — no unexplained ellipsis
- [ ] **Comments explain WHY**: Code comments explain the reasoning, not just what the line does
- [ ] **Model specified**: All API calls specify a model explicitly (`gpt-4o-mini` for budget, noted otherwise)
- [ ] **Environment variables**: API keys come from `os.getenv()` — never hardcoded, never in code blocks
- [ ] **Modern tooling**: Setup instructions use current best practices (e.g., `uv` over `pip`, modern package managers) with traditional alternatives shown for educational context

**Score**: \_\_\_/8

---

## 📊 Scoring Summary

| Section                    | Items  | Score         | %         |
| -------------------------- | ------ | ------------- | --------- |
| 1. Structural Completeness | 10     | \_\_\_/10     | \_\_%     |
| 2. Scaffold File Quality   | 10     | \_\_\_/10     | \_\_%     |
| 3. Learning Method Quality | 12     | \_\_\_/12     | \_\_%     |
| 4. Voice & Tone            | 8      | \_\_\_/8      | \_\_%     |
| 5. Concept Explanation     | 8      | \_\_\_/8      | \_\_%     |
| 6. Road Test Quality       | 5      | \_\_\_/5      | \_\_%     |
| 7. Code Quality            | 8      | \_\_\_/8      | \_\_%     |
| **TOTAL**                  | **61** | **\_\_\_/61** | **\_\_%** |

### Quality Thresholds

- **90–100%** (55–61 items): ✅ Excellent — publish immediately
- **80–89%** (49–54 items): ⚠️ Good — minor revisions, then publish
- **70–79%** (43–48 items): ⚠️ Adequate — significant improvements needed
- **< 70%** (< 43 items): ❌ Insufficient — major revision required

**Minimum target**: 80% (49/61) before learners use the content

---

## 🔍 Critical Items: Required for Any Day to Be Publishable

These items are absolute requirements. A day missing any of them must be revised before use.

### Critical 1: Broken-State Diagnostics in Scaffold Files

**Why**: Learners will hit bugs. If they cannot tell the difference between "my code is wrong" and "I need to do the next TODO," they will waste hours or quit.
**Verification**: Read each `.py` scaffold file. Find the `WHAT BROKEN LOOKS LIKE` section. Confirm it appears before the second TODO, not at the end.

### Critical 2: Interview Anchor per Concept

**Why**: The North Star of Layer 1 is interview readiness. A day that teaches without anchoring to the interview outcome has failed its primary objective.
**Verification**: For each major concept covered in the day, find the "What You'd Say in an Interview" block. Count them. There should be one per concept.

### Critical 3: First Wrench Turn Produces Output Within 30 Minutes

**Why**: If the learner does not see a result within 30 minutes, motivation drops sharply and does not recover.
**Verification**: Time yourself completing the First Wrench Turn from a blank environment. It should produce visible output in under 30 minutes with no prior knowledge of the day's topic.

### Critical 4: Road Test Checklist — All Binary

**Why**: A checklist with subjective items ("does it feel responsive?") is not a checklist — it is a suggestion. Binary items hold the learner to a real standard.
**Verification**: Read each checklist item and ask: "Could two different people reasonably disagree on whether this passes?" If yes, rewrite it.

### Critical 5: Spaced Review Draws From 2+ Prior Days

**Why**: Review of only yesterday's material is not spaced review — it is repetition. The spacing effect requires time between encoding and recall.
**Verification**: Check the spaced review section. Confirm that at least one question references a day more than 2 days earlier.

---

## 🎯 Day 1-Specific Requirements

Day 1 has additional requirements because it is the learner's first experience with the curriculum format.

- [ ] **Success print statement**: `hello.py` prints a congratulatory message after the API response, not just the response itself
- [ ] **Common Setup Errors**: README includes a troubleshooting table for the 3–4 most common setup failures (auth errors, version errors, missing packages)
- [ ] **Mechanic voice established**: The Mechanic's Analogy is the strongest and clearest of all days — this is the frame that carries for 40 days
- [ ] **Forward bridge is prominent**: The "What You Built / What's Next" section at the end of Day 1 is motivating — names what the learner has accomplished and makes Day 2 feel inevitable
- [ ] **No environment assumptions**: Day 1 assumes nothing is pre-installed. Every setup step is explicit.

---

## 🎯 Common Issues and Fixes

### Issue 1: "My scaffold file only has blank TODOs"

**Diagnosis**: TODOs written as task labels rather than teaching artifacts
**Fix**: For each TODO, add (a) WHY this step matters to the system, (b) the PATTERN (what shape the code takes), (c) a HINT that nudges without solving. See WRITING-STYLE-GUIDE.md Pattern 2 for examples.

### Issue 2: "My interview anchors are too long or too vague"

**Diagnosis**: Either writing an essay or writing a title
**Fix**: Write the exact words the learner would say in a 90-second interview answer. One specific decision, one trade-off, one production consideration. Under 100 words.

### Issue 3: "My logbook prompts are basically quiz questions"

**Diagnosis**: Prompts ask for facts that have one right answer
**Fix**: Reframe as conditional or counterfactual: "What would you do if...?", "How would this change if...?", "When would this approach fail?"

### Issue 4: "My Road Test has ambiguous items"

**Diagnosis**: Items like "streaming works correctly" or "the UI looks good"
**Fix**: Make it verifiable: "Typing 'What did I just say?' returns the correct previous message (memory works)" or "Tokens appear progressively — not all at once — when the chatbot responds."

### Issue 5: "The day has no forward bridge"

**Diagnosis**: Day ends with logbook prompts and nothing else
**Fix**: Add a 3–5 sentence section after the logbook that names: (1) what capability the learner now has that they did not have yesterday, (2) how this connects to Day N+1, (3) what the full 10-day phase is building toward.

---

## 📚 Related Guides

- `WRITING-STYLE-GUIDE.md` — Full voice, tone, and pattern reference
- `ANALOGY-LIBRARY.md` — Indexed analogies by concept, for use in Interview Anchors and Mechanic's Analogies
- `ACTION-FIRST-GUIDE.md` — Action-first ordering patterns in detail
- `LANGUAGE-EXPANSION-GUIDE.md` — How to expand thin scaffold files and READMEs

---

**Layer**: Layer 1 — The Mechanic Level
**Last Updated**: 2026-02-25
**Adapted from**: Layer 2 Quality Checklist, reoriented for Mechanic's Workflow and interview-readiness objectives
