# Chapter 7 Comparison Analysis
**Phase 1 Baseline Review against Pedagogical + 3-Tier Enhancements**

**Date:** February 11, 2026  
**Reviewed Files:**
1. `chapter-07-your-first-llm-call.md`
2. `chapter-07-your-first-llm-call-ENHANCED.md`

---

## Executive Decision

Use `chapter-07-your-first-llm-call-ENHANCED.md` as the canonical Chapter 7 baseline for Phase 1.

Reason:
- Stronger coverage of Tier 1, Tier 2, and Tier 3 enhancement markers.
- Better scaffolding support sections (learning styles, spaced repetition, graduated scaffolding).
- Better principle density for future chapter templating.

---

## Objective Metrics (Marker-Based)

| Metric | Regular | Enhanced | Target |
|---|---:|---:|---:|
| Lines (approx) | ~1605 | ~2305 | n/a |
| Words (approx) | ~6628 | ~9939 | 8000-12000 (guideline) |
| Coffee Shop Intro words | 419 | 308 | 250-350 |
| `Try This!` headings | 1 | 2 | 2-3 |
| `Try This!` phrase mentions | 3 | 3 | 2+ |
| Metacognitive markers | 1 | 3 | 2-3+ |
| Error prediction challenges | 1 | 2 | 1-2 |
| War story markers | 1 | 2 | 1-2 |
| Confidence calibration markers | 1 | 2 | 1+ |
| Learning style section | 0 | 1 | 1 |
| Spaced repetition section | 0 | 1 | 1 |
| Graduated scaffolding section | 0 | 1 | 1 |
| Concept map section | 1 | 1 | 1 |
| Analogy mentions | 1 | 9 | 5-7 (minimum intent) |

Notes:
- Counts are keyword/heading heuristics (`rg` marker scan), not a full semantic audit.
- Enhanced now meets the `Try This!` heading target after this review pass.

---

## Pedagogical + 3-Tier Review

### Core Principle Fit (High-Level)
- Progressive complexity: Present in both, deeper in Enhanced.
- Failure-forward: Present in both, richer in Enhanced.
- Contextual bridges: Present in both, explicit scaffold sections in Enhanced.
- Cognitive load management: Present in both, more checkpoints in Enhanced.
- Narrative depth and descriptiveness: Higher in Enhanced.

### Tier 1 (High Impact)
- Metacognitive prompts: Enhanced stronger.
- Error prediction exercises: Enhanced stronger.
- Real-world war stories: Enhanced stronger.
- Confidence calibration: Enhanced stronger and explicit.

### Tier 2 (Medium Effort)
- Spaced repetition callbacks: Enhanced explicit.
- Graduated scaffolding: Enhanced explicit.
- Practical application hooks: Present in both, richer in Enhanced.

### Tier 3 (Higher Effort)
- Concept mapping: Present in both.
- Learning style indicators: Enhanced explicit.

---

## Changes Applied in This Pass (Chapter 7 Enhanced)

File updated: `curriculum/chapters/phase-1-llm-fundamentals/chapter-07-your-first-llm-call-ENHANCED.md`

1. Beginner accessibility alignment
- Difficulty metadata changed to absolute beginner.
- "Expected Difficulty" section aligned to absolute beginner.

2. Inclusiveness alignment
- Introduction rewritten to be cross-domain instead of single-domain.
- Project Thread generalized from one domain to a reusable "pick your track" chatbot.
- Project thread references renamed from CE-specific to domain-generic.

3. Pedagogical target alignment
- Added `Try This! (Practice #2)` for token-budget context trimming.
- Chapter now has two explicit `Try This!` sections (meets target range).

---

## Remaining Gaps to Watch

1. Regular chapter coffee intro is above target length (419 words).
2. Enhanced chapter has high analogy density; if readability drops, trim to the most instructive analogies.
3. No runnable Chapter 7 verification script currently passes in-repo (`complete_ch07.py` is malformed).

---

## Recommendation for Phase 1 Missing Chapters (Starting Pattern)

For each missing Phase 1 chapter, enforce this minimum template before deep expansion:

1. Action-first quick success (5-8 minutes).
2. Two explicit `Try This!` sections with hints and solutions.
3. Tier 1 trio: metacognitive prompts, error prediction, war story.
4. Confidence calibration before summary.
5. Spaced repetition + graduated scaffolding sections.
6. Concept map + learning style guide.

This Chapter 7 enhanced file should be treated as the reference implementation for that pattern.
