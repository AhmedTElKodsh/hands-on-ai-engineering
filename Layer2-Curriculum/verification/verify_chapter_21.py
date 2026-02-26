#!/usr/bin/env python3
"""
Verification Script for Chapter 21: RAG Evaluation

Tests Metric aggregation and Judge logic (Simulated).
"""

import sys

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Metric Aggregation (P27) ---
def test_metric_calc():
    """Verify that average scores are calculated correctly"""
    scores = [1, 0, 1, 1, 0] # 3 pass, 2 fail
    try:
        avg = sum(scores) / len(scores)
        assert avg == 0.6
        print_test("Metric Calculation (P27)", True, "Average score logic is correct")
        return True
    except Exception as e:
        print_test("Metric Calculation (P27)", False, str(e))
        return False

# --- Test 2: Judge Logic (P28) ---
def test_judge_logic_sim():
    """Verify the logic used to detect hallucinations in context"""
    try:
        context = "A is true."
        
        # Scenario A: Faithful
        ans_good = "A is true."
        # Scenario B: Hallucination
        ans_bad = "A is true and B is false." # B is NOT in context
        
        def mock_judge(c, a):
            # Simplified 'logic' of the Judge prompt
            words_in_a = a.split()
            for word in words_in_a:
                if word not in c and word not in ["and", "is"]:
                    return False # Hallucination
            return True
            
        assert mock_judge(context, ans_good) == True
        assert mock_judge(context, ans_bad) == False
        
        print_test("Faithfulness Logic (P28)", True, "Hallucination detection logic verified")
        return True
    except Exception as e:
        print_test("Faithfulness Logic (P28)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 21 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_metric_calc(),
        test_judge_logic_sim()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 21 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
