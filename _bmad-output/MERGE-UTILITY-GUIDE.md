# Chapter Merge Utility Guide

## Overview

The `merge_chapter.py` script is a utility for merging chapter continuation content into enhanced chapter files during the curriculum improvement process.

## Purpose

When enhancing chapters, sometimes the content becomes too large to manage in a single editing session. The merge utility allows you to:

1. Work on chapter enhancements in separate continuation files
2. Merge the continuation content into the main enhanced chapter file
3. Maintain clean version control and editing workflow

## Usage

### Basic Usage

```bash
python _bmad-output/merge_chapter.py
```

### Script Structure

```python
#!/usr/bin/env python3
"""Merge chapter continuation into main enhanced file"""

# Read continuation content
with open('_bmad-output/chapter-XX-continuation.md', 'r', encoding='utf-8') as f:
    continuation = f.read()

# Append to main enhanced file
with open('curriculum/chapters/phase-X-name/chapter-XX-topic-ENHANCED.md', 'a', encoding='utf-8') as f:
    f.write('\n' + continuation)

print("✅ Chapter XX continuation merged successfully!")
```

## Workflow

### Step 1: Create Continuation File

When working on large chapter enhancements:

```bash
# Create continuation file in _bmad-output/
touch _bmad-output/chapter-09-continuation.md
```

### Step 2: Write Continuation Content

Add the remaining enhancement content to the continuation file:

```markdown
## Common Mistakes (Learn from Others!)

### Mistake 1: Over-Prompting

...

## Verification (Test Your Knowledge!)

...
```

### Step 3: Update merge_chapter.py

Edit the script with the correct chapter number and paths:

```python
# Update these paths for your chapter
continuation_file = '_bmad-output/chapter-09-continuation.md'
target_file = 'curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md'
```

### Step 4: Run the Merge

```bash
python _bmad-output/merge_chapter.py
```

### Step 5: Verify the Merge

```bash
# Check the merged content
cat curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md
```

## Example: Chapter 9 Merge

### Before Merge

**Main file**: `chapter-09-prompt-engineering-basics-ENHANCED.md`

- Contains: Introduction, Part 1-3, Bringing It All Together

**Continuation file**: `chapter-09-continuation.md`

- Contains: Common Mistakes, Verification, Concept Map, Summary

### After Merge

**Main file**: `chapter-09-prompt-engineering-basics-ENHANCED.md`

- Contains: All content from both files in proper order

### Merge Script Used

```python
#!/usr/bin/env python3
"""Merge chapter continuation into main enhanced file"""

# Read continuation
with open('_bmad-output/chapter-09-continuation.md', 'r', encoding='utf-8') as f:
    continuation = f.read()

# Append to main file
with open('curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md', 'a', encoding='utf-8') as f:
    f.write('\n' + continuation)

print("✅ Chapter 9 continuation merged successfully!")
```

## Best Practices

### 1. Use Descriptive Filenames

```bash
# Good
chapter-09-continuation.md
chapter-12-advanced-sections.md

# Avoid
temp.md
extra.md
```

### 2. Add Newline Before Merge

The script adds `\n` before the continuation to ensure proper spacing:

```python
f.write('\n' + continuation)  # ← Adds newline separator
```

### 3. Backup Before Merging

```bash
# Create backup of main file
cp curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md \
   curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md.backup
```

### 4. Verify Content Order

Ensure the continuation file starts where the main file ends:

**Main file ends with**:

```markdown
...

## Bringing It All Together
```

**Continuation file starts with**:

```markdown
## Common Mistakes (Learn from Others!)
```

### 5. Clean Up After Merge

```bash
# Optional: Archive the continuation file after successful merge
mv _bmad-output/chapter-09-continuation.md \
   _bmad-output/implementation-artifacts/chapter-09-continuation-archived.md
```

## Troubleshooting

### Issue: File Not Found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory`

**Solution**: Check file paths are correct relative to project root:

```python
# Run from project root
python _bmad-output/merge_chapter.py

# Not from _bmad-output directory
cd _bmad-output  # ❌ Don't do this
python merge_chapter.py  # ❌ Will fail
```

### Issue: Encoding Errors

**Error**: `UnicodeDecodeError`

**Solution**: Ensure UTF-8 encoding is specified:

```python
with open(file, 'r', encoding='utf-8') as f:  # ← Add encoding='utf-8'
    content = f.read()
```

### Issue: Duplicate Content

**Problem**: Running merge script multiple times appends content repeatedly

**Solution**:

1. Restore from backup or git
2. Run merge script only once
3. Delete continuation file after successful merge

```bash
# Restore from git
git checkout curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md

# Run merge once
python _bmad-output/merge_chapter.py

# Remove continuation to prevent re-merge
rm _bmad-output/chapter-09-continuation.md
```

## Integration with Enhancement Workflow

The merge utility fits into the larger enhancement workflow:

```
1. Plan Enhancement
   ↓
2. Create Enhancement Spec (ALL-TIERS.md)
   ↓
3. Create Detailed Plan (DETAILED.md)
   ↓
4. Implement Enhancements
   ├─ Edit main chapter file
   └─ Create continuation file (if needed)
   ↓
5. Merge Continuation ← merge_chapter.py
   ↓
6. Verify Implementation
   ↓
7. Create Completion Report
```

## Related Files

- **Enhancement Specs**: `chapter-XX-enhancements-ALL-TIERS.md`
- **Detailed Plans**: `chapter-XX-enhancement-plan-DETAILED.md`
- **Completion Reports**: `CHAPTER-XX-IMPLEMENTATION-COMPLETE.md`
- **Continuation Files**: `chapter-XX-continuation.md`
- **Main Chapters**: `curriculum/chapters/phase-X/chapter-XX-*.md`

## Version History

| Version | Date     | Changes                             |
| ------- | -------- | ----------------------------------- |
| 1.0     | Jan 2026 | Initial version for Chapter 9 merge |
| 1.1     | Jan 2026 | Documentation created               |

## See Also

- [\_bmad-output/README.md](_bmad-output/README.md) - Directory overview
- [PROGRESS-SUMMARY.md](../PROGRESS-SUMMARY.md) - Overall curriculum progress
- [curriculum/templates/](../curriculum/templates/) - Chapter templates

---

**Last Updated**: January 21, 2026  
**Maintained By**: BMAD Enhancement Team
