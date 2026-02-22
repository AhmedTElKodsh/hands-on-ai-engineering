#!/usr/bin/env python3
"""
Verification Script for Chapter 32: Conditional Routing

Tests Branching logic and Decision evaluation (Simulated).
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

# --- Test 1: Routing Evaluation (P43) ---
def test_routing_logic_sim():
    """Verify the logic of a conditional edge mapper"""
    try:
        # The mapper dictionary
        edge_map = {"math": "math_node", "writing": "writing_node"}
        
        # Simulated router function
        def router(val):
            if "calc" in val: return "math"
            return "writing"
            
        assert edge_map[router("calculate tax")] == "math_node"
        assert edge_map[router("write story")] == "writing_node"
        
        print_test("Routing Evaluation (P43)", True, "Intent correctly mapped to destination node")
        return True
    except Exception as e:
        print_test("Routing Evaluation (P43)", False, str(e))
        return False

# --- Test 2: Branch Coverage (P44) ---
def test_branch_coverage_sim():
    """Verify that all mapped outputs lead to valid nodes"""
    try:
        edge_map = {"A": "node_a", "B": "node_b"}
        valid_nodes = ["node_a", "node_b", "END"]
        
        # Check if every target in the map exists in the graph
        for target in edge_map.values():
            assert target in valid_nodes
            
        print_test("Branch Coverage (P44)", True, "All routing paths lead to existing destinations")
        return True
    except Exception as e:
        print_test("Branch Coverage (P44)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 32 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_routing_logic_sim(),
        test_branch_coverage_sim()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 32 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
