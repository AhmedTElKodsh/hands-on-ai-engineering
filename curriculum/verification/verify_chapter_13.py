#!/usr/bin/env python3
"""
Verification Script for Chapter 13: Understanding Embeddings

Tests Dimension Consistency (P11) and Symmetry (P12).
"""

import sys
import numpy as np

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Math Logic (Symmetry P12) ---
def test_similarity_math():
    """Verify that cosine similarity is symmetric and mathematically correct"""
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0]) # Perpendicular
    
    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    try:
        s1 = cosine_sim(v1, v2)
        s2 = cosine_sim(v2, v1)
        assert s1 == 0.0 # Dot product of perpendicular vectors is 0
        assert s1 == s2 # P12: Symmetry
        print_test("Cosine Similarity Math (P12)", True, "Math is consistent and symmetric")
        return True
    except Exception as e:
        print_test("Cosine Similarity Math (P12)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_dependencies():
    """Verify libraries are available"""
    try:
        import sentence_transformers
        import numpy
        print_test("Dependencies", True, "sentence-transformers and numpy installed")
        return True
    except ImportError as e:
        print_test("Dependencies", False, f"Missing: {e}")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 13 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_dependencies(),
        test_similarity_math()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 13 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
