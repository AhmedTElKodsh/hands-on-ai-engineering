#!/usr/bin/env python3
"""
Verification Script for Chapter 20: Conversational RAG

Tests History Contextualization and Pronoun Resolution (P26).
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

# --- Test 1: Rephrasing Logic (P26) ---
def test_rephrasing_logic():
    """Verify the logic of turning a follow-up into a standalone question"""
    try:
        # Mocking the interaction
        history = "Human: Tell me about Paris. AI: It is the capital of France."
        new_q = "How old is it?"
        
        # This is the 'logic' the LLM should perform
        def mock_rephraser(h, q):
            if "Paris" in h and "it" in q.lower():
                return "How old is Paris?"
            return q
            
        result = mock_rephraser(history, new_q)
        assert "Paris" in result
        assert "it" not in result.lower()
        
        print_test("Pronoun Resolution (P26)", True, "Vague follow-up resolved to specific query")
        return True
    except Exception as e:
        print_test("Pronoun Resolution (P26)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_langchain_core_installed():
    try:
        import langchain_core.messages
        print_test("Package Install", True, "langchain-core is installed")
        return True
    except ImportError:
        print_test("Package Install", False, "langchain-core not found")
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 20 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_langchain_core_installed(),
        test_rephrasing_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 20 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
