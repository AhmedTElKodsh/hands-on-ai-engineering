# Diagnostic Conversion Tools

Complete toolkit for managing your Jupyter Notebook diagnostic workflow.

## 📋 Quick Reference

### Command 0: Launch Notebook in Jupyter Notebook ⭐
```bash
python launch_diagnostic_notebook.py
```

**What it does:**
- Checks if Jupyter Notebook (classic) is installed
- Installs it automatically if missing (with your confirmation)
- Opens `DAY-00-DIAGNOSTIC.ipynb` in your default browser
- Starts Jupyter Notebook server

---

### Command 1: Convert Notebook to Checkable Python File
```bash
python convert_notebook_to_checkable.py
```

**What it does:**
- Reads `DAY-00-DIAGNOSTIC.ipynb`
- Extracts all code cells
- Removes test/execution code
- Preserves TODO comments and function signatures
- Creates `DAY-00-DIAGNOSTIC.checkable.py` for grading

**Output:** Ready-to-grade Python file

---

### Command 2: Reset Notebook to TODO State
```bash
python reset_notebook_to_todo.py
```

**What it does:**
- Reads `DAY-00-DIAGNOSTIC.ipynb`
- Replaces implemented code with TODO placeholders
- Preserves function signatures, docstrings, and structure
- Creates automatic backup: `DAY-00-DIAGNOSTIC.backup.YYYYMMDD_HHMMSS.ipynb`
- Overwrites original notebook with fresh TODO version

**⚠ Warning:** Removes all your implemented code! Backup is created automatically.

---

## 🔄 Complete Workflow

### Step 1: Open Notebook in Jupyter Notebook
```bash
# Launch notebook directly in Jupyter Notebook (classic)
cd Layer1-Final/guides
python launch_diagnostic_notebook.py

# Jupyter Notebook opens in your browser automatically
# Complete all TODO sections in interactive cells
# Test each cell as you go
```

### Step 2: Convert for Grading
```bash
# Convert notebook to checkable Python file
cd Layer1-Final/guides
python convert_notebook_to_checkable.py

# Run the grader
python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py

# Check results
ls diagnostic_results/
```

### Step 3: Reset for Another Attempt (Optional)
```bash
# Reset notebook to fresh TODO state
python reset_notebook_to_todo.py

# Confirm when prompted
# Backup is created automatically

# Start fresh with clean TODO placeholders
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `DAY-00-DIAGNOSTIC.ipynb` | Interactive Jupyter Notebook (your working file) |
| `DAY-00-DIAGNOSTIC.checkable.py` | Converted Python file for grading |
| `DAY-00-DIAGNOSTIC.backup.*.ipynb` | Automatic backups before reset |
| `launch_diagnostic_notebook.py` | **Launcher script** (opens Jupyter Notebook) |
| `convert_notebook_to_checkable.py` | Conversion script (tool) |
| `reset_notebook_to_todo.py` | Reset script (tool) |

---

## 🎯 Usage Examples

### Example 1: First Time Diagnostic
```bash
# 1. Launch notebook in Jupyter Notebook
cd Layer1-Final/guides
python launch_diagnostic_notebook.py

# 2. Complete all tasks in interactive cells

# 3. Convert for grading
python convert_notebook_to_checkable.py

# 4. Run grader
python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py
```

### Example 2: Retake After Study
```bash
# 1. Reset notebook to fresh state
python reset_notebook_to_todo.py
# Type "yes" when prompted

# 2. Launch fresh notebook
python launch_diagnostic_notebook.py

# 3. Complete tasks again

# 4. Convert and grade
python convert_notebook_to_checkable.py
python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py
```

### Example 3: Multiple Practice Sessions
```bash
# Session 1
python reset_notebook_to_todo.py  # Creates backup.001
# ... work in notebook ...
python convert_notebook_to_checkable.py
python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py

# Session 2
python reset_notebook_to_todo.py  # Creates backup.002
# ... work in notebook ...
python convert_notebook_to_checkable.py
python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py
```

---

## ⚠️ Important Notes

1. **Backup is automatic** - Every reset creates a timestamped backup
2. **Checkable file is temporary** - `DAY-00-DIAGNOSTIC.checkable.py` is overwritten on each conversion
3. **Keep your backups** - Don't delete backup files until you're done with all attempts
4. **Grade the checkable file** - Always run grader on `.checkable.py`, not `.ipynb`

---

## 🛠️ Troubleshooting

### Error: "Notebook not found"
```bash
# Make sure you're in the correct directory
cd d:\AI\Gentech\POCs\hands-on-ai-engineering\Layer1-Final\guides

# Or run with full path
python d:\AI\Gentech\POCs\hands-on-ai-engineering\Layer1-Final\guides\convert_notebook_to_checkable.py
```

### Error: "grade_diagnostic.py not found"
```bash
# The grader is in the parent directory
cd ..
python grade_diagnostic.py guides/DAY-00-DIAGNOSTIC.checkable.py
```

### Want to restore from backup
```bash
# Copy backup back to original
cp DAY-00-DIAGNOSTIC.backup.20260320_143022.ipynb DAY-00-DIAGNOSTIC.ipynb
```

---

## 📊 Grading Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    DIAGNOSTIC WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. START: Launch notebook                                  │
│     python launch_diagnostic_notebook.py                    │
│     ↓                                                        │
│  2. WORK: Complete tasks in Jupyter Notebook (interactive)  │
│     ↓                                                        │
│  3. CONVERT: python convert_notebook_to_checkable.py        │
│     ↓                                                        │
│  4. GRADE: python grade_diagnostic.py DAY-00-DIAGNOSTIC...  │
│     ↓                                                        │
│  5. REVIEW: Check diagnostic_results/                       │
│     ↓                                                        │
│  [OPTIONAL] RETAKE:                                         │
│     ↓                                                        │
│  6. RESET: python reset_notebook_to_todo.py                 │
│     ↓                                                        │
│  7. BACK TO STEP 1                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

**Need help?** Run either script with `--help` flag (if implemented) or check this README.
