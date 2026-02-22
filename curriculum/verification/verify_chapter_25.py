#!/usr/bin/env python3
"""
Verification Script for Chapter 25: Output Parsers

Tests Output Parsing logic and Schema Adherence (P7).
"""

import sys
import json

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: JSON Parsing Logic (P7) ---
def test_json_parsing_logic():
    """Verify that a string with markdown noise can be parsed (Conceptual)"""
    raw_llm_output = "Here is the data: ```json
{"score": 10, "name": "Test"}
``` hope this helps!"
    
    # This is the logic a standard parser performs
    def mock_parser(text):
        try:
            # 1. Strip noise
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            # 2. Extract JSON
            return json.loads(text.strip())
        except:
            return None
            
    try:
        result = mock_parser(raw_llm_output)
        assert result["score"] == 10
        assert result["name"] == "Test"
        print_test("Output Parsing Logic (P7)", True, "Markdown noise correctly stripped and JSON parsed")
        return True
    except Exception as e:
        print_test("Output Parsing Logic (P7)", False, str(e))
        return False

# --- Test 2: Dependency Check ---
def test_langchain_parsers_installed():
    try:
        import langchain_core.output_parsers
        print_test("Package Install", True, "langchain-core parsers installed")
        return True
    except ImportError:
        print_test("Package Install", False, "langchain-core not found")
        return False

def main():
    print(f"
{Colors.BOLD}Chapter 25 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_langchain_parsers_installed(),
        test_json_parsing_logic()
    ]
    
    if all(results):
        print(f"
{Colors.GREEN}✅ Chapter 25 Logic Verified!{Colors.RESET}")
    else:
        print(f"
{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
