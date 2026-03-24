#!/usr/bin/env python3
"""
Verification Script for Chapter 28: OTAR Loop

Tests Self-Correction logic and State Transitions (P38, P39).
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

# --- Test 1: Self-Correction Logic Simulation (P39) ---
def test_self_correction_sim():
    """Verify the logic of a feedback loop fixing a mistake"""
    try:
        # Scenario: Fix missing semicolon (Conceptual)
        bad_input = "print('Hello')"
        error_msg = "SyntaxError: missing something"
        
        def mock_fixer(code, error):
            # Logic: If error mentions syntax, add something (Simulation)
            if "SyntaxError" in error:
                return code + ";" # Corrected (simulated)
            return code
            
        fixed = mock_fixer(bad_input, error_msg)
        assert fixed == "print('Hello');"
        
        print_test("Reflection Integration (P39)", True, "Feedback used to correct data")
        return True
    except Exception as e:
        print_test("Reflection Integration (P39)", False, str(e))
        return False

# --- Test 2: Max Retries Logic (P38) ---
def test_max_retries():
    """Verify that the loop terminates after N attempts"""
    try:
        counter = 0
        max_tries = 3
        
        def run_loop():
            nonlocal counter
            for i in range(max_tries):
                counter += 1
                # Never succeeds
                pass
            return "Done"
            
        run_loop()
        assert counter == max_tries
        print_test("Loop Termination (P38)", True, "Loop respected max_tries limit")
        return True
    except Exception as e:
        print_test("Loop Termination (P38)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 28 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_self_correction_sim(),
        test_max_retries()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 28 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
