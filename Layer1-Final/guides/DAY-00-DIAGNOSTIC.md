# ⚠️ DAY 00 DIAGNOSTIC — UPDATED FORMAT

**This file has been superseded.** The Day 00 Diagnostic now uses a **single Python file** format for simplicity.

---

## 📍 Current Location

**Active File:** [`DAY-00-DIAGNOSTIC.py`](./DAY-00-DIAGNOSTIC.py)

**Setup Instructions:** [`README-DIAGNOSTIC.md`](./README-DIAGNOSTIC.md)

**Auto-Grader:** [`grade_diagnostic.py`](./grade_diagnostic.py)

---

## 🚀 Quick Start

### Step 1: Open the Task File

Open **`DAY-00-DIAGNOSTIC.py`** in VSCode. This is where you'll write all your code.

### Step 2: Complete All TODOs

The file contains 5 tasks with `# TODO:` comments. Replace each TODO with your implementation.

**Time limit:** 90 minutes (no AI assistance)

### Step 3: Run the Grader

```bash
# From the guides folder
python grade_diagnostic.py
```

### Step 4: Check Results

Results are saved to `diagnostic_results/latest_results.json`

---

## 📋 What Changed

### Old Format (Deprecated — This File)
- Instructions in `.md` file
- Student copies code blocks to separate `.py` files
- Multiple test files required
- Manual file management

### New Format (Current — Use This)
- **Single `DAY-00-DIAGNOSTIC.py` file** — all tasks in one place
- **No copy-paste** — code directly in the file
- **No separate test files** — grader evaluates dynamically
- **Simpler setup** — just one file to open

---

## 📁 File Structure

```
guides/
├── DAY-00-DIAGNOSTIC.py       ← OPEN THIS FILE (student task file)
├── grade_diagnostic.py         ← Run this to grade
├── README-DIAGNOSTIC.md        ← Setup instructions
├── data/
│   └── sample_data.csv         ← Test data for Task 1
└── DAY-00-DIAGNOSTIC.md        ← This file (historical reference only)
```

---

## 🎯 Tasks Overview

| Task | Topic | Time | Function(s) to Implement |
|------|-------|------|-------------------------|
| 1 | CSV Data Pipeline | 20 min | `load_and_clean_csv()`, `compute_groupby_stats()` |
| 2 | OOP Class | 15 min | `BankAccount` class with methods |
| 3 | REST API Client | 20 min | `fetch_user_post_titles()`, `fetch_post_by_id()` |
| 4 | Type Hints + Filtering | 20 min | `filter_and_sort_products()`, `filter_products_by_category()` |
| 5 | Pytest Tests | 15 min | Write 2+ test functions |

**Total:** 90 minutes, 5 points

---

## 📊 Scoring & Path Recommendations

| Score | Recommendation |
|-------|---------------|
| **5/5** | Skip to Week 1 |
| **3-4/5** | Compressed Week 0 (3 days) |
| **0-2/5** | Full Week 0 (5 days) |

---

## ⚠️ STRICT FAILURE RULE

- **Incomplete/Partial** = 0 points (Weakness)
- **Incorrect/Failing** = 0 points (Weakness)
- **AI Usage** = Immediate reset

---

## 🔗 Quick Links

- **Start Here:** [README-DIAGNOSTIC.md](./README-DIAGNOSTIC.md)
- **Task File:** [DAY-00-DIAGNOSTIC.py](./DAY-00-DIAGNOSTIC.py)
- **Grader:** [grade_diagnostic.py](./grade_diagnostic.py)

---

**Last Updated:** March 14, 2026  
**Status:** Superseded by `DAY-00-DIAGNOSTIC.py`
