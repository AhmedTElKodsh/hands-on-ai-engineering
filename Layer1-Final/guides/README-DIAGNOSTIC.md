# Day 00 Python Diagnostic — Setup Instructions

**Purpose:** Assess your Python proficiency before starting Week 1  
**Time:** 90 minutes (no AI assistance)  
**Scoring:** 5 tasks × 1 point each = 5 points total

---

## 📋 What You'll Find

| File | Purpose |
|------|---------|
| `DAY-00-DIAGNOSTIC.py` | **Your task file** — Replace all TODOs with your code |
| `grade_diagnostic.py` | Auto-grader — Run this after completing tasks |
| `data/sample_data.csv` | Test data for Task 1 |
| `README-DIAGNOSTIC.md` | This file — Setup and instructions |

---

## 🚀 Quick Start

### Step 1: Set Up Environment

```bash
# Navigate to guides folder
cd Layer1-Final/guides

# Create virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install pytest requests httpx pandas
```

### Step 3: Complete the Diagnostic

1. Open `DAY-00-DIAGNOSTIC.py` in VSCode
2. Replace **ALL** `# TODO:` comments with your implementation
3. Do **NOT** use AI assistance (ChatGPT, Claude, etc.)
4. Time limit: 90 minutes

### Step 4: Run the Grader

```bash
python grade_diagnostic.py
```

### Step 5: Check Your Results

Results will be saved to:
- `diagnostic_results/latest_results.json` — Latest results
- `diagnostic_results/diagnostic_YYYY-MM-DD.json` — Timestamped copy

---

## 📊 Scoring & Path Recommendations

| Score | Recommendation | What It Means |
|-------|---------------|---------------|
| **5/5** | Skip to Week 1 | Strong Python fundamentals. Ready for AI engineering! |
| **3-4/5** | Compressed Week 0 (3 days) | Good foundation. Focus on weak areas: Pydantic, async, testing. |
| **0-2/5** | Full Week 0 (5 days) | Build Python fundamentals before AI/LLM work. It's worth it! |

---

## ⚠️ STRICT FAILURE RULE

- **Incomplete/Partial** solutions = **0 points** (recorded as Weakness)
- **Incorrect/Failing** solutions = **0 points** (recorded as Weakness)
- **AI Usage** = Immediate reset of diagnostic

This diagnostic establishes a **binary pass/fail baseline** for engineering readiness.

---

## 📝 Task Breakdown

| Task | Topic | Time | Points |
|------|-------|------|--------|
| 1 | CSV Data Pipeline (pandas) | 20 min | 1 |
| 2 | OOP Class Implementation | 15 min | 1 |
| 3 | REST API Client | 20 min | 1 |
| 4 | Type Hints + Filtering | 20 min | 1 |
| 5 | Pytest Tests | 15 min | 1 |

**Total Time:** 90 minutes  
**Total Points:** 5

---

## 🆘 Troubleshooting

### "File not found: DAY-00-DIAGNOSTIC.py"
Make sure you're running the grader from the `guides` folder:
```bash
cd Layer1-Final/guides
python grade_diagnostic.py
```

### "pytest not found"
Install pytest:
```bash
pip install pytest
```

### "ModuleNotFoundError: No module named 'pandas'"
Install pandas:
```bash
pip install pandas
```

### "Syntax error in student code"
Check that you didn't accidentally delete important code. Make sure:
- All function definitions have `:` at the end
- All parentheses are closed
- Indentation is consistent (use 4 spaces)

---

## ✅ After Completing

1. Save your results JSON file
2. Follow the path recommendation (Week 0 or Week 1)
3. Move forward with the curriculum!

**Good luck! 🍀**
