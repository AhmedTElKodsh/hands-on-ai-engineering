# Day 00 Python Diagnostic - Quick Start Guide

## 🚀 3 Simple Commands

### 1️⃣ Open Notebook (Start Here)
```bash
cd d:\AI\Gentech\POCs\hands-on-ai-engineering\Layer1-Final\guides
python launch_diagnostic_notebook.py
```
✅ Opens notebook in Jupyter Notebook (classic) automatically  
✅ Installs Jupyter Notebook if missing  
✅ Tests each cell as you work

---

### 2️⃣ Convert for Grading (When Done)
```bash
python convert_notebook_to_checkable.py
python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py
```
✅ Creates checkable Python file  
✅ Runs the official grader  
✅ Shows results in `diagnostic_results/`

---

### 3️⃣ Reset for Retake (Optional)
```bash
python reset_notebook_to_todo.py
```
✅ Clears your code back to TODO state  
✅ Creates automatic backup  
✅ Start fresh anytime

---

## 📋 Complete Workflow

```
1. python launch_diagnostic_notebook.py
   ↓ Opens in Jupyter Notebook
2. Complete all TODO cells
   ↓ Test as you go
3. python convert_notebook_to_checkable.py
   ↓ Creates checkable file
4. python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py
   ↓ View results
5. (Optional) python reset_notebook_to_todo.py
   ↓ Retake anytime
```

---

## ⏱️ Time Breakdown

| Task | Time |
|------|------|
| Task 1: CSV Pipeline | 20 min |
| Task 2: OOP Class | 15 min |
| Task 3: REST API | 20 min |
| Task 4: Type Hints | 20 min |
| Task 5: Pytest Tests | 15 min |
| **Total** | **90 min** |

---

## 🎯 Scoring

- **5/5** → Skip to Week 1
- **3-4/5** → Compressed Week 0 (3 days)
- **0-2/5** → Full Week 0 (5 days)

---

## 🆘 Troubleshooting

**Jupyter Notebook not opening?**
```bash
pip install notebook
python launch_diagnostic_notebook.py
```

**Need to see your backup files?**
```bash
dir DAY-00-DIAGNOSTIC.backup.*
```

**Want to restore a backup?**
```bash
copy DAY-00-DIAGNOSTIC.backup.20260320_*.ipynb DAY-00-DIAGNOSTIC.ipynb
```

---

## 📞 Quick Reference

| Command | What It Does |
|---------|--------------|
| `python launch_diagnostic_notebook.py` | Opens notebook in Jupyter Lab |
| `python convert_notebook_to_checkable.py` | Converts to checkable Python |
| `python reset_notebook_to_todo.py` | Resets to TODO state |
| `python grade_diagnostic.py DAY-00-DIAGNOSTIC.checkable.py` | Runs grader |

---

**Good luck, Ahmed! You've got this! 💪**
