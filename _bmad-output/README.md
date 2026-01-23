# BMAD Output Directory

This directory contains enhancement plans, implementation artifacts, and utility scripts for the curriculum chapter improvement process.

## 📁 Directory Structure

```
_bmad-output/
├── README.md                           # This file
├── merge_chapter.py                    # Utility script for merging chapter content
├── implementation-artifacts/           # Generated code and examples
├── chapter-*-enhancements-ALL-TIERS.md # Enhancement specifications
├── chapter-*-enhancement-plan-*.md     # Detailed enhancement plans
├── CHAPTER-*-IMPLEMENTATION-COMPLETE.md # Completion reports
└── PHASE-*-IMPLEMENTATION-STATUS.md    # Phase-level status tracking
```

## 🛠️ Utility Scripts

### merge_chapter.py

**Purpose**: Merges chapter continuation content into enhanced chapter files.

**Quick Usage**:

```bash
python _bmad-output/merge_chapter.py
```

**Documentation**: See [MERGE-UTILITY-GUIDE.md](MERGE-UTILITY-GUIDE.md) for detailed usage, examples, and troubleshooting.

**What it does**:

- Reads continuation content from `chapter-XX-continuation.md`
- Appends content to the corresponding enhanced chapter file
- Provides success confirmation

**Example**:

```python
# Merges chapter 9 continuation into enhanced file
with open('_bmad-output/chapter-09-continuation.md', 'r') as f:
    continuation = f.read()

with open('curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md', 'a') as f:
    f.write('\n' + continuation)
```

**Note**: The script is currently empty/cleared. Restore from git history if needed, or refer to the guide for the template.

## 📋 Enhancement Files

### Enhancement Specifications (ALL-TIERS)

Files like `chapter-06B-enhancements-ALL-TIERS.md` contain:

- **Tier 1**: High impact, low effort enhancements (metacognitive prompts, war stories)
- **Tier 2**: High impact, medium effort (expanded intros, analogies, scaffolding)
- **Tier 3**: Medium impact, higher effort (concept maps, learning style indicators)

### Enhancement Plans (DETAILED)

Files like `chapter-06B-enhancement-plan-DETAILED.md` contain:

- Detailed implementation steps
- Specific line numbers for insertions
- Code examples and content blocks
- Quality improvement targets (e.g., 65% → 90-95%)

### Completion Reports

Files like `chapter-06B-FINAL-COMPLETION-REPORT.md` contain:

- Summary of implemented enhancements
- Quality metrics before/after
- Verification checklist
- Next steps

## 🎯 Current Status

### Phase 0 (Foundations)

- ✅ Chapter 6A: Complete
- ✅ Chapter 6B: Complete (90-95% quality)
- ✅ Chapter 6C: Complete

### Phase 1 (LLM Fundamentals)

- ✅ Chapter 7: Complete
- ✅ Chapter 8: Complete
- ✅ Chapter 9: Complete

See `PHASE-*-IMPLEMENTATION-STATUS.md` files for detailed progress.

## 🔄 Workflow

1. **Plan**: Create enhancement specification (ALL-TIERS)
2. **Detail**: Create detailed implementation plan
3. **Implement**: Apply enhancements to chapter files
4. **Verify**: Run verification scripts
5. **Report**: Generate completion report
6. **Merge**: Use merge_chapter.py if needed for continuations

## 📝 File Naming Conventions

- `chapter-XX-*`: Chapter-specific files
- `CHAPTER-XX-*`: Completion/status files (uppercase)
- `PHASE-X-*`: Phase-level tracking
- `SESSION-*`: Session-specific notes

## 🚀 Quick Reference

**To enhance a chapter**:

1. Review `chapter-XX-enhancements-ALL-TIERS.md`
2. Follow `chapter-XX-enhancement-plan-DETAILED.md`
3. Apply changes to `curriculum/chapters/phase-X/chapter-XX-*.md`
4. Verify with chapter's verification script
5. Document in `CHAPTER-XX-IMPLEMENTATION-COMPLETE.md`

**To merge continuation content**:

1. Ensure continuation file exists: `chapter-XX-continuation.md`
2. Update `merge_chapter.py` with correct paths
3. Run: `python _bmad-output/merge_chapter.py`
4. Verify merged content in target chapter file

## 📚 Related Documentation

- **Merge Utility**: `MERGE-UTILITY-GUIDE.md` - Detailed guide for merge_chapter.py
- Main curriculum: `curriculum/chapters/`
- Templates: `curriculum/templates/`
- Progress tracking: `PROGRESS-SUMMARY.md`
- Project overview: `README.md`

---

**Last Updated**: January 21, 2026
**Maintained By**: BMAD Enhancement Team
