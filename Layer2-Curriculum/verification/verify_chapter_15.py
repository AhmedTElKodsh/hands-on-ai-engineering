#!/usr/bin/env python3
"""
Verification Script for Chapter 15: Chunking Strategies

Tests Fixed Slicing, Overlap Logic, and Token Counting.
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

# --- Test 1: Fixed Slicing with Overlap (P16) ---
def test_overlap_logic():
    """Verify that start index shifts correctly with overlap"""
    text = "0123456789" # 10 chars
    size = 5
    overlap = 2
    
    # Chunk 1: [0:5] -> "01234"
    # Chunk 2 Start: 5 - 2 = 3. [3:8] -> "34567"
    
    def get_chunks(t, s, o):
        chunks = []
        start = 0
        while start < len(t):
            chunks.append(t[start : start+s])
            if start + s >= len(t): break
            start += s - o
        return chunks

    try:
        chunks = get_chunks(text, size, overlap)
        assert chunks[0] == "01234"
        assert chunks[1] == "34567"
        assert "34" in chunks[0] and "34" in chunks[1] # Overlap check
        print_test("Overlap Logic (P16)", True, "Chunks overlap correctly")
        return True
    except Exception as e:
        print_test("Overlap Logic (P16)", False, str(e))
        return False

# --- Test 2: Token Counting ---
def test_token_lib():
    """Verify tiktoken is available"""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode("Hello")
        assert len(tokens) > 0
        print_test("Token Counting", True, "tiktoken installed and encoding works")
        return True
    except ImportError:
        print_test("Token Counting", False, "tiktoken not found")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 15 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_token_lib(),
        test_overlap_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 15 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
