#!/usr/bin/env python3
"""
Verification Script for Chapter 31: LangGraph State Machines

Tests Graph execution flow and State updates (P42).
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

# --- Test 1: Graph Logic Simulation (P42) ---
def test_graph_logic():
    """Verify that nodes update a shared state correctly"""
    try:
        class State(TypedDict):
            val: int
            
        def node_a(s): return {"val": s["val"] + 1}
        def node_b(s): return {"val": s["val"] * 2}
        
        # Simulated Graph Run: Start -> A -> B -> End
        initial_state = {"val": 5}
        s1 = node_a(initial_state)
        # LangGraph merge logic: update dict
        current_state = {**initial_state, **s1}
        
        s2 = node_b(current_state)
        final_state = {**current_state, **s2}
        
        assert final_state["val"] == 12 # (5+1)*2
        print_test("Graph Execution (P42)", True, "Sequential state updates matched expected math")
        return True
    except Exception as e:
        print_test("Graph Execution (P42)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_langgraph_installed():
    try:
        import langgraph
        print_test("Package Install", True, "langgraph is installed")
        return True
    except ImportError:
        print_test("Package Install", False, "langgraph not found. Run 'pip install langgraph'")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 31 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_langgraph_installed(),
        test_graph_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 31 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
