#!/usr/bin/env python3
"""
Verification Script for Chapter 29: Tool Calling

Tests Schema Adherence (P40) and Tool Call validity (P34).
"""

import sys
from pydantic import BaseModel, Field

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Tool Schema Logic (P40) ---
def test_tool_schema_logic():
    """Verify that Pydantic models correctly define tool arguments"""
    try:
        class MockArgs(BaseModel):
            query: str = Field(description="Search term")
            limit: int = Field(default=5)
            
        from langchain_core.tools import tool
        
        @tool("mock_search", args_schema=MockArgs)
        def mock_search(query: str, limit: int = 5):
            """Search logic."""
            return f"{query} {limit}"
            
        # Check if langchain extracted the schema correctly
        schema = mock_search.args
        assert schema["query"]["type"] == "string"
        assert schema["limit"]["default"] == 5
        
        print_test("Schema Adherence (P40)", True, "Pydantic model correctly mapped to tool schema")
        return True
    except Exception as e:
        print_test("Schema Adherence (P40)", False, str(e))
        return False

# --- Test 2: Tool Call Payload Logic (P34) ---
def test_tool_call_payload():
    """Verify the logic of processing a 'tool_call' dictionary"""
    try:
        # Mocking an AI response payload
        tool_call = {
            "name": "calc",
            "args": {"a": 10, "b": 20},
            "id": "call_123"
        }
        
        # Simulated execution logic
        def execute(name, args):
            if name == "calc": return args["a"] + args["b"]
            return 0
            
        result = execute(tool_call["name"], tool_call["args"])
        assert result == 30
        
        print_test("Tool Call Validity (P34)", True, "Tool call payload correctly parsed and executed")
        return True
    except Exception as e:
        print_test("Tool Call Validity (P34)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 29 Verification{Colors.RESET}")
    print("="*40)
    
    results = [
        test_tool_schema_logic(),
        test_tool_call_payload()
    ]
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ Chapter 29 Logic Verified!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
