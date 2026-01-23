# Curriculum Pedagogical Enhancement Spec

## Overview

This spec defines a system for applying 17 research-backed pedagogical enhancements to curriculum chapters. It transforms scaffolded chapters (output of the **curriculum-scaffolding-conversion** spec) into high-quality educational content with superior pedagogical features.

## Relationship to Other Specs

```
Complete Solution Chapters
    ↓
[Spec 1: curriculum-scaffolding-conversion]
    ↓
Scaffolded Chapters (signatures, TODOs, basic hints)
    ↓
[Spec 2: curriculum-pedagogical-enhancement] ← THIS SPEC
    ↓
Enhanced Chapters (scaffolding + 17 pedagogical improvements)
```

## The 17 Enhancements

### Tier 1: High Impact, Low Effort (8 enhancements)

1. **Metacognitive Prompts** (3 per chapter)
2. **Error Prediction Exercises** (2 per chapter)
3. **Real-World War Stories** (2 per chapter)
4. **Confidence Calibration** (1 per chapter)
5. **Emotional Checkpoints** (3-4 per chapter)
6. **Anticipatory Questions** (4-6 per chapter)
7. **Expand Language** (reduce abbreviations)
8. **Increase Descriptiveness** (more "why" and "how")

### Tier 2: High Impact, Medium Effort (7 enhancements)

9. **Expanded Coffee Shop Intro** (250-350 words)
10. **Spaced Repetition Callbacks** (2-3 per chapter)
11. **Graduated Scaffolding** (chapter start indicator)
12. **Enhanced Analogies** (4 per chapter, varied complexity)
13. **Failure-Forward Learning** (2-3 mistakes per chapter)
14. **Contextual Bridges** (2-3 connections to prior chapters)
15. **Practical Application Hooks** (section ends)

### Tier 3: Medium Impact, Higher Effort (2 enhancements)

16. **Concept Map** (1 per chapter)
17. **Learning Style Indicators** (📖 👁️ 💻 🎧 🤝 throughout)

## Key Principles

1. **Context-Aware**: All enhancements reference actual chapter content, not generic templates
2. **Tier-Appropriate**: Enhancement detail adjusts based on difficulty level (TIER_1, TIER_2, TIER_3)
3. **Quality-Verified**: Minimum 85% quality score required before completion
4. **Systematic**: All 17 enhancements applied consistently to every chapter
5. **Efficient**: 2-3 hours per chapter for complete enhancement

## Expected Results

- **Quality Improvement**: 65% → 90-95% (baseline to excellent)
- **Pedagogical Score**: 10/15 → 14/15 (67% → 93%)
- **Student Engagement**: Significantly improved through varied enhancement types
- **Learning Outcomes**: Better retention through spaced repetition and metacognition

## Scope

- **Input**: ~55 scaffolded chapters across 11 phases
- **Output**: ~55 enhanced chapters with 17 pedagogical improvements each
- **Time**: 2-3 hours per chapter × 55 chapters = 110-165 hours total
- **Timeline**: 8-10 weeks at 15-20 hours per week

## Files in This Spec

- **requirements.md** - 24 requirements defining all enhancement types and quality standards
- **design.md** - Architecture for enhancement generators, context analyzers, and quality verification (TO BE CREATED)
- **tasks.md** - Implementation tasks for building the enhancement system (TO BE CREATED)

## Reference Documents

Located in `_bmad-output/`:

- `FRAMEWORK-CLARIFICATION-23-vs-17.md` - Explains the 17 vs 23 enhancement frameworks
- `chapter-06B-enhancements-ALL-TIERS.md` - Example of all 17 enhancements applied
- `MERGE-UTILITY-GUIDE.md` - Guide for handling large chapter enhancements
- `chapter-scaffolding-conversion-template.md` - Scaffolding patterns from previous spec

## Status

- ✅ Requirements document complete (24 requirements)
- ⏳ Design document (to be created)
- ⏳ Tasks document (to be created)
- ⏳ Implementation (not started)

## Next Steps

1. Create design.md with enhancement generator architecture
2. Create tasks.md with implementation plan
3. Begin implementation of enhancement generators
4. Test on sample chapters
5. Apply to full curriculum

---

**Created**: January 21, 2026  
**Owner**: Ahmed  
**Related Spec**: curriculum-scaffolding-conversion
