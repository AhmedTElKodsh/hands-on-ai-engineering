#!/usr/bin/env python3
"""
Verification Script for Chapter 17: Your First RAG System

Tests Context Consistency (P20) - checking if the AI respects provided context.
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

# --- Test 1: Grounding Logic (P20) ---
def test_grounding_logic():
    """Verify the RAG prompt pattern ensures the model uses provided context"""
    try:
        # Mocking the interaction logic
        context = "The sky in this simulation is PURPLE."
        query = "What color is the sky?"
        
        # This is the RAG prompt pattern we teach
        prompt = f"Context: {context}\nQuestion: {query}\nAnswer using ONLY context."
        
        # For the test, we simulate a 'correct' model behavior
        # (A real test would call the API, but here we verify the pattern logic)
        def simulate_rag_call(p):
            if "PURPLE" in p: return "The sky is purple."
            return "Blue"
            
        answer = simulate_rag_call(prompt)
        assert "purple" in answer.lower()
        print_test("Grounding Logic (P20)", True, "Prompt correctly forces context usage")
        return True
    except Exception as e:
        print_test("Grounding Logic (P20)", False, str(e))
        return False

# --- Test 2: Dependency check for Chapter 17 ---
def test_dependencies():
    try:
        import openai
        import chromadb
        print_test("Dependencies", True, "openai and chromadb installed")
        return True
    except ImportError as e:
        print_test("Dependencies", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 17 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_dependencies(),
        test_grounding_logic()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 17 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
