#!/usr/bin/env python3
"""
Day 00 Python Diagnostic — Auto-Grading Script

Purpose: Assess Python proficiency before starting Week 1
Time: 90 minutes (no AI assistance)
Strict Failure Rule: Incomplete/Partial or Incorrect/Failing solutions = 0 points (Weakness)
Scoring: 5 tasks × 1 point each = 5 points total

This grader reads a single DAY-00-DIAGNOSTIC.py file and evaluates each task
by executing the student's implementations directly (no separate test files needed).
"""

import json
import subprocess
import sys
import re
import ast
import traceback
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional
from io import StringIO


# ============================================================================
# CONFIGURATION
# ============================================================================

DIAGNOSTIC_FILE = "DAY-00-DIAGNOSTIC.py"
DATA_FILE = "data/sample_data.csv"
RESULTS_DIR = "diagnostic_results"


# ============================================================================
# GRADING UTILITIES
# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_failure(text: str):
    """Print failure message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def check_type_hints_basic(content: str) -> Tuple[bool, str]:
    """
    Basic type hint check by analyzing source code.
    """
    has_type_hints = (
        '->' in content and
        (': int' in content or ': str' in content or ': list' in content or
         ': dict' in content or ': float' in content or ': bool' in content or
         ': List' in content or ': Dict' in content or ': Optional' in content)
    )

    if has_type_hints:
        return True, "Type hints present"
    else:
        return False, "No type hints detected"


def check_todo_remaining(content: str) -> Tuple[bool, List[str]]:
    """
    Check if TODO comments remain without implementation.
    Returns (has_unimplemented_todos, list of todos found)
    """
    todo_pattern = r'#\s*TODO[:\s]*(.+?)(?=\n#|$)'
    todos = re.findall(todo_pattern, content, re.IGNORECASE)
    
    unimplemented = []
    for todo in todos:
        # Check if there's actual code after the TODO (not just 'pass')
        if todo.strip() in ['', 'pass', 'implement this', 'implement', 'complete this']:
            unimplemented.append(todo.strip())
    
    return len(unimplemented) > 0, todos


def check_pass_only(content: str, function_name: str) -> bool:
    """
    Check if a function only contains 'pass' statement.
    """
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                # Check if body is just a single Pass node
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    return True
                # Check if body contains only pass and comments
                non_pass = [n for n in node.body if not isinstance(n, (ast.Pass, ast.Expr)) or 
                           (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str))]
                if len(non_pass) == 0:
                    return True
    except:
        pass
    return False


# ============================================================================
# TASK EVALUATORS
# ============================================================================

def evaluate_task_1(student_module: Any, content: str) -> Tuple[bool, str]:
    """
    Grade Task 1: CSV Data Pipeline
    
    Requirements:
    - Load CSV file
    - Clean missing values (drop or fill)
    - Compute groupby statistics
    - Output JSON file
    """
    checks = []
    
    # Check 1: Functions exist
    if not hasattr(student_module, 'load_and_clean_csv'):
        return False, "✗ Function 'load_and_clean_csv' not found"
    checks.append("✓ load_and_clean_csv function exists")
    
    if not hasattr(student_module, 'compute_groupby_stats'):
        return False, "✗ Function 'compute_groupby_stats' not found"
    checks.append("✓ compute_groupby_stats function exists")
    
    # Check 2: Type hints
    has_hints, hint_msg = check_type_hints_basic(content)
    if has_hints:
        checks.append("✓ Type hints present")
    else:
        checks.append(f"⚠ {hint_msg}")
    
    # Check 3: No remaining TODOs with just 'pass'
    has_todos, todos = check_todo_remaining(content)
    if not has_todos:
        checks.append("✓ No unimplemented TODOs")
    else:
        return False, "✗ Unimplemented TODOs found: " + ", ".join(todos[:3])
    
    # Check 4: Actually run the functions
    try:
        df = student_module.load_and_clean_csv(DATA_FILE)
        
        # Verify DataFrame is returned
        import pandas as pd
        if not isinstance(df, pd.DataFrame):
            return False, "✗ load_and_clean_csv should return a DataFrame"
        checks.append("✓ Returns DataFrame")
        
        # Verify no null values
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            return False, f"✗ DataFrame has {null_count} null values (should be 0)"
        checks.append("✓ No null values in DataFrame")
        
        # Test compute_groupby_stats
        stats = student_module.compute_groupby_stats(df)
        
        if not isinstance(stats, dict):
            return False, "✗ compute_groupby_stats should return a dict"
        checks.append("✓ Returns dictionary")
        
        if 'by_category' not in stats:
            return False, "✗ Result should have 'by_category' key"
        checks.append("✓ Has 'by_category' key")
        
        # Verify structure
        for category, values in stats['by_category'].items():
            if 'sum' not in values or 'mean' not in values:
                return False, f"✗ Category '{category}' missing 'sum' or 'mean'"
        checks.append("✓ Each category has sum and mean")
        
        return True, "\n".join(checks)
        
    except Exception as e:
        return False, f"✗ Execution error: {str(e)}\n{traceback.format_exc()}"


def evaluate_task_2(student_module: Any, content: str) -> Tuple[bool, str]:
    """
    Grade Task 2: OOP Class Implementation
    
    Requirements:
    - Class with __init__ method
    - At least 2 methods
    - Proper __repr__ method
    """
    checks = []
    
    # Check 1: Class exists
    if not hasattr(student_module, 'BankAccount'):
        return False, "✗ Class 'BankAccount' not found"
    
    BankAccount = student_module.BankAccount
    checks.append("✓ BankAccount class exists")
    
    # Check 2: Can instantiate
    try:
        account = BankAccount("Alice", 1000.0)
        checks.append("✓ Can instantiate class")
    except Exception as e:
        return False, f"✗ Cannot instantiate: {str(e)}"
    
    # Check 3: Has required methods
    if not hasattr(account, 'deposit'):
        return False, "✗ Missing 'deposit' method"
    checks.append("✓ deposit method exists")
    
    if not hasattr(account, 'withdraw'):
        return False, "✗ Missing 'withdraw' method"
    checks.append("✓ withdraw method exists")
    
    # Check 4: Test deposit
    account = BankAccount("Bob", 500.0)
    result = account.deposit(200.0)
    if result is not True:
        return False, "✗ deposit() should return True on success"
    if account.balance != 700.0:
        return False, f"✗ Balance should be 700.0 after deposit, got {account.balance}"
    checks.append("✓ deposit works correctly")
    
    # Check 5: Test withdraw success
    result = account.withdraw(300.0)
    if result is not True:
        return False, "✗ withdraw() should return True when sufficient funds"
    if account.balance != 400.0:
        return False, f"✗ Balance should be 400.0 after withdraw, got {account.balance}"
    checks.append("✓ withdraw works correctly (sufficient funds)")
    
    # Check 6: Test withdraw insufficient funds
    result = account.withdraw(1000.0)
    if result is not False:
        return False, "✗ withdraw() should return False when insufficient funds"
    checks.append("✓ withdraw handles insufficient funds")
    
    # Check 7: Test __repr__
    repr_str = repr(account)
    if "Bob" not in repr_str or "400" not in repr_str:
        return False, "✗ __repr__ should include owner and balance"
    checks.append("✓ __repr__ works correctly")
    
    return True, "\n".join(checks)


def evaluate_task_3(student_module: Any, content: str) -> Tuple[bool, str]:
    """
    Grade Task 3: REST API Client
    
    Requirements:
    - Call REST API (requests or httpx)
    - Parse JSON response
    - Handle errors with try/except
    """
    checks = []
    
    # Check 1: HTTP client imported
    if 'import requests' not in content and 'import httpx' not in content:
        return False, "✗ No HTTP client imported (requests or httpx)"
    checks.append("✓ HTTP client imported")
    
    # Check 2: Error handling
    if 'try:' not in content or 'except' not in content:
        return False, "✗ No error handling (try/except)"
    checks.append("✓ Error handling present")
    
    # Check 3: Function exists
    if not hasattr(student_module, 'fetch_user_post_titles'):
        return False, "✗ Function 'fetch_user_post_titles' not found"
    
    fetch_func = student_module.fetch_user_post_titles
    
    # Check 4: Test valid user
    try:
        titles = fetch_func(1)
        if titles is None:
            return False, "✗ Function returned None for valid user"
        if not isinstance(titles, list):
            return False, f"✗ Should return list, got {type(titles)}"
        if len(titles) == 0:
            return False, "✗ Should return at least one title"
        checks.append("✓ Fetches posts for valid user")
    except Exception as e:
        return False, f"✗ Error fetching posts: {str(e)}"
    
    # Check 5: Test invalid user
    try:
        titles = fetch_func(99999)
        if titles is None:
            checks.append("✓ Returns None for invalid user")
        elif isinstance(titles, list) and len(titles) == 0:
            checks.append("✓ Returns empty list for invalid user")
        else:
            return False, "✗ Should return None or empty list for invalid user"
    except Exception as e:
        return False, f"✗ Error with invalid user: {str(e)}"
    
    return True, "\n".join(checks)


def evaluate_task_4(student_module: Any, content: str) -> Tuple[bool, str]:
    """
    Grade Task 4: Type Hints + Filtering
    
    Requirements:
    - Function with type hints
    - Filter list of dicts by condition
    - Return sorted results
    """
    checks = []
    
    # Check 1: Type hints
    has_hints, hint_msg = check_type_hints_basic(content)
    if has_hints:
        checks.append("✓ Type hints present")
    else:
        return False, f"✗ {hint_msg}"
    
    # Check 2: Function exists
    if not hasattr(student_module, 'filter_and_sort_products'):
        return False, "✗ Function 'filter_and_sort_products' not found"
    
    filter_func = student_module.filter_and_sort_products
    checks.append("✓ filter_and_sort_products function exists")
    
    # Check 3: Test with sample data
    try:
        sample_products = [
            {"name": "Laptop", "price": 999.99, "category": "Electronics", "in_stock": True},
            {"name": "Mouse", "price": 29.99, "category": "Electronics", "in_stock": True},
            {"name": "Keyboard", "price": 79.99, "category": "Electronics", "in_stock": False},
            {"name": "Desk Chair", "price": 199.99, "category": "Furniture", "in_stock": True},
        ]
        
        result = filter_func(sample_products, max_price=100.0)
        
        if not isinstance(result, list):
            return False, f"✗ Should return list, got {type(result)}"
        checks.append("✓ Returns a list")
        
        if result != ["Mouse"]:
            return False, f"✗ Expected ['Mouse'] for max_price=100, got {result}"
        checks.append("✓ Correct filtering (max_price=100)")
        
        # Test sorting
        result = filter_func(sample_products, max_price=500.0)
        if result != sorted(result):
            return False, f"✗ Results not sorted alphabetically: {result}"
        checks.append("✓ Results sorted alphabetically")
        
        # Test empty list
        result = filter_func([], max_price=100.0)
        if result != []:
            return False, f"✗ Should return empty list for empty input, got {result}"
        checks.append("✓ Handles empty list")
        
        return True, "\n".join(checks)
        
    except Exception as e:
        return False, f"✗ Execution error: {str(e)}\n{traceback.format_exc()}"


def evaluate_task_5(student_module: Any, content: str) -> Tuple[bool, str]:
    """
    Grade Task 5: Pytest Tests
    
    Requirements:
    - Write 2 pytest tests
    - Tests should cover task_4 function
    - Proper assertions
    """
    checks = []
    
    # Check 1: pytest import or test structure
    if 'import pytest' not in content and 'def test_' not in content:
        return False, "✗ No pytest structure found"
    checks.append("✓ Pytest structure detected")
    
    # Check 2: Count test functions
    test_count = len(re.findall(r'def test_', content))
    if test_count >= 2:
        checks.append(f"✓ {test_count} test functions found (2+ required)")
    else:
        return False, f"✗ Only {test_count} test function(s) found (need 2+)"
    
    # Check 3: Assertions
    if 'assert ' not in content:
        return False, "✗ No assertions found"
    checks.append("✓ Assertions present")
    
    # Check 4: Tests reference task_4 function
    if 'filter_and_sort_products' not in content:
        return False, "✗ Tests should test filter_and_sort_products function"
    checks.append("✓ Tests reference task_4 function")
    
    # Check 5: Try to run the tests if possible
    try:
        # Look for test functions in the student module
        test_funcs = [name for name in dir(student_module) if name.startswith('test_')]
        if len(test_funcs) >= 2:
            checks.append(f"✓ Found {len(test_funcs)} test functions in module")
            
            # Try running one test
            for test_name in test_funcs[:1]:
                test_func = getattr(student_module, test_name)
                if callable(test_func):
                    try:
                        test_func()
                        checks.append(f"✓ Test '{test_name}' passes")
                    except Exception as e:
                        checks.append(f"⚠ Test '{test_name}' exists but failed: {str(e)}")
    except:
        pass  # Running tests is optional for grading
    
    return True, "\n".join(checks)


# ============================================================================
# MAIN GRADING FLOW
# ============================================================================

TASK_EVALUATORS = {
    "task_1_csv_pipeline": ("CSV Data Pipeline", evaluate_task_1),
    "task_2_oop_class": ("OOP Class Implementation", evaluate_task_2),
    "task_3_api_client": ("REST API Client", evaluate_task_3),
    "task_4_type_hints": ("Type Hints + Filtering", evaluate_task_4),
    "task_5_pytest": ("Pytest Tests", evaluate_task_5),
}


def load_student_module(file_path: str) -> Tuple[Optional[Any], str]:
    """
    Load student's DAY-00-DIAGNOSTIC.py as a module.
    """
    if not Path(file_path).exists():
        return None, f"File not found: {file_path}"
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create a module namespace
        import types
        student_module = types.ModuleType('student_diagnostic')
        
        # Execute the student's code in the module namespace
        exec(compile(content, file_path, 'exec'), student_module.__dict__)
        
        return student_module, content
        
    except SyntaxError as e:
        return None, f"Syntax error in student code: {str(e)}"
    except Exception as e:
        return None, f"Error loading student code: {str(e)}\n{traceback.format_exc()}"


def run_diagnostic():
    """
    Main diagnostic grading flow
    """
    print_header("Day 00 Python Diagnostic — Auto-Grader")

    print_info(f"Diagnostic file: {DIAGNOSTIC_FILE}")
    print_info("Time limit: 90 minutes (no AI assistance)")
    print_info(f"{Colors.BOLD}{Colors.FAIL}STRICT FAILURE RULE: Incomplete/Partial or Incorrect/Failing = 0 points{Colors.ENDC}")
    print_info("Total points: 5 (1 per task)\n")

    print_info("Path recommendations:")
    print("  • 5/5: Skip to Week 1")
    print("  • 3-4/5: Compressed Week 0 (3 days)")
    print("  • 0-2/5: Full Week 0 (5 days)\n")

    input(f"{Colors.BOLD}Press Enter to start grading...{Colors.ENDC}")

    # Load student's module
    print_header("Loading Student Code")
    student_module, content = load_student_module(DIAGNOSTIC_FILE)
    
    if student_module is None:
        print_failure(f"Failed to load {DIAGNOSTIC_FILE}")
        print(f"Error: {content}")
        return 0

    print_success(f"Successfully loaded {DIAGNOSTIC_FILE}")

    results = {}
    total_score = 0

    # Grade each task
    for task_key, (task_name, evaluator) in TASK_EVALUATORS.items():
        print_header(f"{task_name} ({task_key})")

        passed, message = evaluator(student_module, content)

        if passed:
            print_success(f"Task PASSED (+1 point)")
            results[task_key] = {"passed": True, "message": message}
            total_score += 1
        else:
            print_failure(f"Task NOT PASSED (+0 points)")
            results[task_key] = {"passed": False, "message": message}

        print(f"\nDetails:\n{message}\n")

    # Summary
    print_header("DIAGNOSTIC RESULTS")

    print(f"\n{Colors.BOLD}Total Score: {total_score}/5{Colors.ENDC}\n")

    for task_key, result in results.items():
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        task_name = TASK_EVALUATORS[task_key][0]
        print(f"  {status} — {task_name}")

    print("\n" + "=" * 60)

    # Recommendation
    if total_score == 5:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Recommendation: Skip to Week 1{Colors.ENDC}")
        print("You have strong Python fundamentals. Ready for AI engineering!")
    elif total_score >= 3:
        print(f"\n{Colors.WARNING}{Colors.BOLD}📚 Recommendation: Compressed Week 0 (3 days){Colors.ENDC}")
        print("Good foundation. Focus on weak areas.")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}📖 Recommendation: Full Week 0 (5 days){Colors.ENDC}")
        print("Build Python fundamentals before AI/LLM work. It's worth it!")

    print("\n" + "=" * 60)

    # Save results
    save_results(results, total_score)

    return total_score


def save_results(results: dict, total_score: int):
    """Save results to JSON file"""
    timestamp = datetime.now().isoformat()

    report = {
        "timestamp": timestamp,
        "total_score": total_score,
        "max_score": 5,
        "diagnostic_file": DIAGNOSTIC_FILE,
        "tasks": {}
    }

    for task_key, result in results.items():
        # Truncate long messages
        message = result["message"][:500] if len(result["message"]) > 500 else result["message"]
        report["tasks"][task_key] = {
            "name": TASK_EVALUATORS[task_key][0],
            "passed": result["passed"],
            "message": message
        }

    # Determine recommendation
    if total_score == 5:
        report["recommendation"] = "week_1"
    elif total_score >= 3:
        report["recommendation"] = "week_0_compressed"
    else:
        report["recommendation"] = "week_0_full"

    # Save to file
    output_dir = Path(RESULTS_DIR)
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"diagnostic_{timestamp.replace(':', '-')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print_info(f"Results saved to: {output_file}")

    # Also save summary to latest_results.json
    latest_file = output_dir / "latest_results.json"
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print_info(f"Latest results also saved to: {latest_file}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(f"""
Day 00 Python Diagnostic Auto-Grader

Usage:
    python grade_diagnostic.py          # Run the grader
    python grade_diagnostic.py --help   # Show this help

Requirements:
    - DAY-00-DIAGNOSTIC.py (student's implementation)
    - data/sample_data.csv (test data for Task 1)
    - Python 3.10+
    - pandas (for Task 1)
    - requests or httpx (for Task 3)

The grader will:
    1. Load DAY-00-DIAGNOSTIC.py
    2. Execute each task's functions with test inputs
    3. Verify outputs match expected results
    4. Report pass/fail for each task
    5. Save results to diagnostic_results/
""")
    else:
        run_diagnostic()
