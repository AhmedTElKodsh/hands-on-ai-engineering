#!/usr/bin/env python3
"""
Verification Script for Chapter 19: Retrieval Strategies

Tests Multi-Query Expansion logic and Query Diversity (P23).
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

# --- Test 1: Expansion Diversity (P23) ---
def test_query_expansion_logic():
    """Verify that expansion produces multiple strings"""
    try:
        # Mocking the output of the expansion chain
        raw_llm_output = "Password recovery\nLogin help\nAccount access"
        
        # This is the logic we teach in the Action section
        variations = [v.strip() for v in raw_llm_output.split("\n") if v.strip()]
        
        assert len(variations) == 3
        assert "Password recovery" in variations
        print_test("Query Expansion Logic (P23)", True, "Variations split correctly")
        return True
    except Exception as e:
        print_test("Query Expansion Logic (P23)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_rank_bm25_installed():
    try:
        import rank_bm25
        print_test("Package Install", True, "rank_bm25 is installed")
        return True
    except ImportError:
        print_test("Package Install", False, "rank_bm25 not found. Run 'pip install rank_bm25'")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 19 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_rank_bm25_installed(),
        test_query_expansion_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 19 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
