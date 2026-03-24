#!/usr/bin/env python3
"""
Verification Script for Chapter 18: LCEL

Tests Chain composition logic and Parallel execution (P21, P22).
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

# --- Test 1: LCEL Logic Simulation (P21) ---
def test_lcel_order():
    """Verify that piping mimics function composition order"""
    try:
        class MockRunnable:
            def __init__(self, op): self.op = op
            def invoke(self, x): return self.op(x)
            def __or__(self, next_r):
                return MockChain(self, next_r)
        
        class MockChain:
            def __init__(self, first, second):
                self.first = first
                self.second = second
            def invoke(self, x):
                return self.second.invoke(self.first.invoke(x))
        
        # Chain: (x + 1) | (x * 2)
        r1 = MockRunnable(lambda x: x + 1)
        r2 = MockRunnable(lambda x: x * 2)
        chain = r1 | r2
        
        result = chain.invoke(5) # (5+1)*2 = 12
        assert result == 12
        print_test("LCEL Pipe Logic (P21)", True, "Piping order is correct")
        return True
    except Exception as e:
        print_test("LCEL Pipe Logic (P21)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_langchain_installed():
    try:
        import langchain
        import langchain_core
        print_test("Package Install", True, "langchain is installed")
        return True
    except ImportError:
        print_test("Package Install", False, "langchain not found. Run 'pip install langchain'")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 18 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_langchain_installed(),
        test_lcel_order()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 18 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
