"""
Day 00 Python Diagnostic Auto-Grader

Run this script to grade your diagnostic test.
Time limit: 90 minutes (no AI assistance)

Usage:
    python grade_diagnostic.py
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def run_command(cmd: list[str], description: str) -> tuple[bool, str]:
    """Run a command and return success status and output."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        print(output)
        return success, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: Test took too long (>30 seconds)"
    except Exception as e:
        return False, f"ERROR: {str(e)}"


def grade_task_1() -> tuple[bool, str]:
    """Grade Task 1: CSV Pipeline."""
    return run_command(
        [sys.executable, "-m", "diagnostic.task_1_csv_pipeline"],
        "Task 1: CSV Pipeline"
    )


def grade_task_2() -> tuple[bool, str]:
    """Grade Task 2: OOP Class."""
    success, output = run_command(
        [sys.executable, "-m", "diagnostic.task_2_oop_class"],
        "Task 2: OOP Class"
    )
    
    # Check if output contains expected results
    if success:
        if "Final: BankAccount" in output and "1300.0" in output:
            return True, output
        else:
            return False, output + "\nERROR: Output format incorrect"
    
    return False, output


def grade_task_3() -> tuple[bool, str]:
    """Grade Task 3: API Client."""
    return run_command(
        [sys.executable, "-m", "diagnostic.task_3_api_client"],
        "Task 3: API Client"
    )


def grade_task_4() -> tuple[bool, str]:
    """Grade Task 4: Type Hints + Filtering."""
    success, output = run_command(
        [sys.executable, "-m", "diagnostic.task_4_type_hints"],
        "Task 4: Type Hints + Filtering"
    )
    
    # Check if output contains expected results
    if success:
        if "['Mouse']" in output and "['Desk Chair', 'Laptop', 'Monitor', 'Mouse']" in output:
            return True, output
        else:
            return False, output + "\nERROR: Output format incorrect"
    
    return False, output


def grade_task_5() -> tuple[bool, str]:
    """Grade Task 5: Pytest Tests."""
    return run_command(
        [sys.executable, "-m", "pytest", "diagnostic/task_5_pytest.py", "-v", "--tb=short"],
        "Task 5: Pytest Tests"
    )


def main():
    """Run diagnostic grading."""
    print("\n" + "="*60)
    print("DAY 00 PYTHON DIAGNOSTIC - AUTO-GRADER")
    print("="*60)
    print("\n⚠️  IMPORTANT: If you used AI assistance, stop now.")
    print("   This diagnostic must be completed without AI help.")
    print("\nStarting grading...\n")
    
    results = {}
    total_score = 0
    
    # Grade each task
    tasks = [
        ("Task 1: CSV Pipeline", grade_task_1),
        ("Task 2: OOP Class", grade_task_2),
        ("Task 3: API Client", grade_task_3),
        ("Task 4: Type Hints + Filtering", grade_task_4),
        ("Task 5: Pytest Tests", grade_task_5),
    ]
    
    for task_name, task_func in tasks:
        success, output = task_func()
        score = 1 if success else 0
        total_score += score
        
        results[task_name] = {
            "passed": success,
            "score": score,
            "output": output[:500] if len(output) > 500 else output  # Truncate for brevity
        }
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{task_name}: {status}")
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC RESULTS")
    print("="*60)
    print(f"\nTotal Score: {total_score}/5\n")
    
    for task_name, result in results.items():
        status = "✅" if result["passed"] else "❌"
        print(f"{status} {task_name}")
    
    # Recommendation
    print("\n" + "="*60)
    print("RECOMMENDATION")
    print("="*60)
    
    if total_score == 5:
        print("\n🎉 EXCELLENT! You're ready for Week 1.")
        print("   Skip Week 0 and proceed directly to Week 1 content.\n")
    elif total_score >= 3:
        print("\n📚 GOOD FOUNDATION. Consider compressed Week 0 (3 days).")
        print("   Focus on your weak areas before starting Week 1.\n")
    else:
        print("\n⚠️  NEEDS IMPROVEMENT. Complete full Week 0 (5 days).")
        print("   This will strengthen your Python fundamentals.\n")
    
    # Save results
    results_dir = Path("diagnostic_results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = results_dir / f"results_{timestamp}.json"
    
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "total_score": total_score,
            "max_score": 5,
            "tasks": results
        }, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    print("\n" + "="*60)
    
    return total_score


if __name__ == "__main__":
    sys.exit(main())
