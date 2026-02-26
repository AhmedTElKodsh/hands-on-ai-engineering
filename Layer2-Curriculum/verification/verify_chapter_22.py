#!/usr/bin/env python3
"""
Verification Script for Chapter 22: Advanced RAG Patterns

Tests Hash-based change detection (P30) and Parent-Child logic (Simulated).
"""

import hashlib
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

# --- Test 1: Hash Change Detection (P30) ---
def test_hashing_logic():
    """Verify that hashing detects changes in document content"""
    content_v1 = "Document version 1"
    content_v2 = "Document version 2"
    
    def get_hash(c): return hashlib.sha256(c.encode()).hexdigest()
    
    try:
        h1 = get_hash(content_v1)
        h1_check = get_hash(content_v1)
        h2 = get_hash(content_v2)
        
        assert h1 == h1_check # Deterministic
        assert h1 != h2       # Detects change
        
        print_test("Hash Detection (P30)", True, "Document changes correctly identified via hashing")
        return True
    except Exception as e:
        print_test("Hash Detection (P30)", False, str(e))
        return False

# --- Test 2: Parent-Child Simulation (P29) ---
def test_parent_child_sim():
    """Verify the logic of looking up a parent from a child ID"""
    try:
        # Mocking the DocStore
        parent_store = {
            "p1": "FULL DOCUMENT TEXT FOR PROJECT ALPHA",
            "p2": "FULL DOCUMENT TEXT FOR PROJECT BETA"
        }
        
        # Mocking the Child metadata
        child_chunk = {
            "id": "c1",
            "parent_id": "p1",
            "text": "PROJECT ALPHA"
        }
        
        # The logic: Retrieval gives child -> Code looks up parent
        retrieved_parent = parent_store.get(child_chunk["parent_id"])
        
        assert retrieved_parent == parent_store["p1"]
        assert "FULL" in retrieved_parent
        
        print_test("Parent-Child Logic (P29)", True, "Parent retrieval via child pointer verified")
        return True
    except Exception as e:
        print_test("Parent-Child Logic (P29)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 22 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_hashing_logic(),
        test_parent_child_sim()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 22 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
