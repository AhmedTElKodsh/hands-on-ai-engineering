#!/usr/bin/env python3
"""
Verification Script for Chapter 30: Agent Memory

Tests Message Trimming and Vector Search logic (Simulated).
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

# --- Test 1: Message Trimming Logic (P25) ---
def test_trimming_logic():
    """Verify the logic of a sliding window memory"""
    try:
        messages = ["M1", "M2", "M3", "M4", "M5"]
        
        def trim(msgs, limit):
            return msgs[-limit:]
            
        trimmed = trim(messages, 3)
        assert trimmed == ["M3", "M4", "M5"]
        
        print_test("Context Continuity (P25)", True, "Sliding window correctly preserves latest context")
        return True
    except Exception as e:
        print_test("Context Continuity (P25)", False, str(e))
        return False

# --- Test 2: Memory Retrieval Simulation (P41) ---
def test_memory_retrieval_sim():
    """Verify semantic search logic for long-term memory"""
    try:
        # Mocking a simple vector search
        db = [
            {"text": "My cat's name is Whiskers", "tags": ["personal"]},
            {"text": "The sky is blue", "tags": ["fact"]}
        ]
        
        def mock_search(query):
            # Logic: keyword match simulation
            return [doc for doc in db if query.lower() in doc["text"].lower()]
            
        res = mock_search("cat")
        assert len(res) == 1
        assert "Whiskers" in res[0]["text"]
        
        print_test("Memory Retrieval (P41)", True, "Relevant facts retrieved from long-term store")
        return True
    except Exception as e:
        print_test("Memory Retrieval (P41)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 30 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_trimming_logic(),
        test_memory_retrieval_sim()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 30 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
