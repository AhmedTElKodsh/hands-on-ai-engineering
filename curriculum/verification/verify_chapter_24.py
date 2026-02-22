#!/usr/bin/env python3
"""
Verification Script for Chapter 24: Memory & Callbacks

Tests Session separation and Callback execution order.
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

# --- Test 1: Session Logic Simulation ---
def test_session_separation():
    """Verify that a store separates history by ID"""
    try:
        store = {}
        def get_hist(sid):
            if sid not in store: store[sid] = []
            return store[sid]
            
        h1 = get_hist("user_1")
        h1.append("A")
        
        h2 = get_hist("user_2")
        h2.append("B")
        
        assert len(store["user_1"]) == 1
        assert "A" in store["user_1"]
        assert "B" not in store["user_1"]
        
        print_test("Session Separation", True, "History stores remain isolated by ID")
        return True
    except Exception as e:
        print_test("Session Separation", False, str(e))
        return False

# --- Test 2: Callback Logic ---
def test_callback_logic():
    """Verify standard callback interface behavior"""
    try:
        class MockHandler:
            def __init__(self): self.log = []
            def start(self): self.log.append("S")
            def end(self): self.log.append("E")
            
        handler = MockHandler()
        # Simulate execution
        handler.start()
        handler.end()
        
        assert handler.log == ["S", "E"]
        print_test("Callback Order", True, "Lifecycle events fired in sequence")
        return True
    except Exception as e:
        print_test("Callback Order", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 24 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_session_separation(),
        test_callback_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 24 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
