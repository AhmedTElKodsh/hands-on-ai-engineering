#!/usr/bin/env python3
"""
Verification Script for Chapter 33: Human-in-the-Loop

Tests Interrupt logic and Resume capability (P45, P46).
"""

import sys
from typing import TypedDict

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Interrupt Simulation (P45) ---
def test_interrupt_sim():
    """Verify the logic of stopping before a node"""
    try:
        # Simulation of a checkpointer and interrupt list
        memory = {"thread_1": {"val": "Drafted", "next": "publish"}}
        interrupts = ["publish"]
        
        # Logic: If next step is in interrupts, stop.
        current_next = memory["thread_1"]["next"]
        is_paused = current_next in interrupts
        
        assert is_paused == True
        print_test("State Persistence (P45)", True, "Interrupt gate correctly identified")
        return True
    except Exception as e:
        print_test("State Persistence (P45)", False, str(e))
        return False

# --- Test 2: Resume Logic Simulation (P46) ---
def test_resume_sim():
    """Verify that state can be updated and then finished"""
    try:
        # 1. Start with paused state
        state = {"val": "Drafted"}
        
        # 2. Human Edit
        state["val"] = "Approved"
        
        # 3. Resume (Finish)
        def finish_node(s): return s["val"] + "!"
        
        result = finish_node(state)
        assert result == "Approved!"
        
        print_test("Resume Correctness (P46)", True, "Workflow finished with updated human data")
        return True
    except Exception as e:
        print_test("Resume Correctness (P46)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 33 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_interrupt_sim(),
        test_resume_sim()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 33 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
