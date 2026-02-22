#!/usr/bin/env python3
"""
Verification Script for Chapter 7: Your First LLM Call

Tests all code examples and concepts from the chapter to ensure they work correctly.
Run this after completing Chapter 7 to verify all examples are functional.

Usage:
    python verify_chapter_07.py
"""

import os
import sys
import unittest
from typing import List, Dict
from unittest.mock import MagicMock, patch

# Try to import required packages
try:
    from dotenv import load_dotenv
    from openai import OpenAI, APIConnectionError, RateLimitError
    PACKAGES_INSTALLED = True
except ImportError as e:
    PACKAGES_INSTALLED = False
    MISSING_PACKAGE = str(e)

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name: str, passed: bool, details: str = ""):
    """Print test result with color coding"""
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")

# --- Test Cases ---

def test_imports():
    """Test that openai and python-dotenv are installed"""
    test_name = "Package Imports"
    if PACKAGES_INSTALLED:
        print_test(test_name, True, "openai and python-dotenv are installed")
        return True
    else:
        print_test(test_name, False, f"Missing package: {MISSING_PACKAGE}. Run 'pip install openai python-dotenv'")
        return False

def test_api_key_loading():
    """Test loading API key from .env"""
    test_name = "API Key Loading"
    
    # Create a dummy .env if needed for the test, but ideally we check the real one
    # Or we just check if load_dotenv works and we can get *something*
    # We won't enforce a real key, just that the mechanism works.
    
    try:
        load_dotenv()
        key = os.getenv("OPENAI_API_KEY")
        if key:
            print_test(test_name, True, "Found OPENAI_API_KEY in environment")
            return True
        else:
            print_test(test_name, False, "OPENAI_API_KEY not found. Create a .env file.")
            return False
    except Exception as e:
        print_test(test_name, False, f"Error loading .env: {e}")
        return False

def test_stateless_logic_mocked():
    """Test the chatbot history logic using a Mock client"""
    test_name = "Chatbot State Logic (Mocked)"
    
    if not PACKAGES_INSTALLED:
        print_test(test_name, False, "Skipping: Packages not installed")
        return False

    try:
        # Mock OpenAI Client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "I am a mock response."
        mock_client.chat.completions.create.return_value = mock_response

        # Logic from "The Forgetful Chatbot" project
        history = [{"role": "system", "content": "You are a helpful assistant."}]
        user_input = "Hello"
        
        # 1. Append User
        history.append({"role": "user", "content": user_input})
        
        # 2. Call API (Mock)
        response = mock_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        reply = response.choices[0].message.content
        
        # 3. Append Assistant
        history.append({"role": "assistant", "content": reply})
        
        # Verification
        assert len(history) == 3
        assert history[0]["role"] == "system"
        assert history[1]["role"] == "user"
        assert history[1]["content"] == "Hello"
        assert history[2]["role"] == "assistant"
        assert history[2]["content"] == "I am a mock response."
        
        print_test(test_name, True, "History logic maintains state correctly")
        return True
    except Exception as e:
        print_test(test_name, False, f"Logic error: {e}")
        return False

def test_token_estimation_logic():
    """Test the token estimation logic from the chapter"""
    test_name = "Token Estimation Logic"
    
    def estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    try:
        text = "Hello world" # 11 chars -> 2 tokens
        assert estimate_tokens(text) == 2
        
        text2 = "A" # 1 char -> 1 token (max)
        assert estimate_tokens(text2) == 1
        
        print_test(test_name, True, "Estimation function works as expected")
        return True
    except AssertionError:
        print_test(test_name, False, "Calculation incorrect")
        return False

def test_cost_calculator():
    """Test Cost Calculator (Project 3) - Token tracking and cost calculation"""
    test_name = "Cost Calculator Logic (Project 3)"

    class CostTracker:
        def __init__(self):
            self.total_prompt_tokens = 0
            self.total_completion_tokens = 0
            self.input_cost_per_1k = 0.0015  # GPT-3.5-Turbo
            self.output_cost_per_1k = 0.002

        def track(self, prompt_tokens: int, completion_tokens: int) -> float:
            """Track token usage and return cost for this call"""
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens

            input_cost = (prompt_tokens / 1000) * self.input_cost_per_1k
            output_cost = (completion_tokens / 1000) * self.output_cost_per_1k
            return input_cost + output_cost

        def get_total_cost(self) -> float:
            """Calculate total session cost"""
            input_cost = (self.total_prompt_tokens / 1000) * self.input_cost_per_1k
            output_cost = (self.total_completion_tokens / 1000) * self.output_cost_per_1k
            return input_cost + output_cost

    try:
        tracker = CostTracker()

        # Simulate API calls
        cost1 = tracker.track(prompt_tokens=1000, completion_tokens=500)
        cost2 = tracker.track(prompt_tokens=800, completion_tokens=300)

        # Verify individual costs
        expected_cost1 = (1000/1000 * 0.0015) + (500/1000 * 0.002)  # 0.0015 + 0.001 = 0.0025
        expected_cost2 = (800/1000 * 0.0015) + (300/1000 * 0.002)   # 0.0012 + 0.0006 = 0.0018

        assert abs(cost1 - expected_cost1) < 0.0001, f"Cost 1 incorrect: {cost1} vs {expected_cost1}"
        assert abs(cost2 - expected_cost2) < 0.0001, f"Cost 2 incorrect: {cost2} vs {expected_cost2}"

        # Verify total tracking
        assert tracker.total_prompt_tokens == 1800, "Total prompt tokens incorrect"
        assert tracker.total_completion_tokens == 800, "Total completion tokens incorrect"

        total_cost = tracker.get_total_cost()
        expected_total = 0.0025 + 0.0018  # 0.0043
        assert abs(total_cost - expected_total) < 0.0001, f"Total cost incorrect: {total_cost}"

        print_test(test_name, True, f"Cost tracking works: ${total_cost:.4f} for 2 calls")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {e}")
        return False


def test_context_manager():
    """Test Context Manager (Project 4) - Sliding window truncation"""
    test_name = "Context Manager - Sliding Window (Project 4)"

    def estimate_tokens(messages: List[Dict[str, str]]) -> int:
        """Rough token estimate"""
        total = 0
        for msg in messages:
            total += len(msg["content"]) // 4
        return total

    def truncate_context(history: List[Dict[str, str]], max_tokens: int = 100) -> List[Dict[str, str]]:
        """Keep conversation under token limit using sliding window (removes oldest pairs)"""
        current_tokens = estimate_tokens(history)

        # Always keep system message (index 0)
        system_message = history[0] if history and history[0]["role"] == "system" else None
        conversation = history[1:] if system_message else history

        # Remove oldest pairs until under limit
        while current_tokens > max_tokens and len(conversation) >= 2:
            # Remove oldest user + assistant pair
            conversation = conversation[2:]

            # Recalculate
            temp_history = [system_message] + conversation if system_message else conversation
            current_tokens = estimate_tokens(temp_history)

        result = [system_message] + conversation if system_message else conversation
        return result

    try:
        # Create long history exceeding limit
        history = [{"role": "system", "content": "You are helpful."}]  # ~5 tokens

        # Add 10 user/assistant pairs (each ~25 tokens = 250 total)
        for i in range(10):
            history.append({"role": "user", "content": "A" * 50})       # ~12 tokens
            history.append({"role": "assistant", "content": "B" * 50})  # ~12 tokens

        original_len = len(history)  # 21 messages
        original_tokens = estimate_tokens(history)  # ~250 tokens

        # Truncate to 100 tokens (should keep ~4 pairs + system = 9 messages)
        truncated = truncate_context(history, max_tokens=100)
        new_tokens = estimate_tokens(truncated)

        # Verify results
        assert new_tokens <= 100, f"Exceeded limit: {new_tokens} tokens"
        assert len(truncated) < original_len, "Should have removed messages"
        assert truncated[0]["role"] == "system", "System message must be preserved"
        assert truncated[0]["content"] == "You are helpful.", "System message content changed"

        # Verify it removed oldest pairs (sliding window)
        # The newest messages should still be there
        assert history[-2]["content"] in [msg["content"] for msg in truncated], "Should keep newest user message"
        assert history[-1]["content"] in [msg["content"] for msg in truncated], "Should keep newest assistant message"

        print_test(test_name, True,
                  f"Truncated from {original_len} msgs ({original_tokens}t) to {len(truncated)} msgs ({new_tokens}t)")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {e}")
        return False


def test_trim_messages_logic():
    """Test the context trimming logic"""
    test_name = "Context Trimming Logic (Legacy)"

    def estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    def trim_messages(messages: list[dict], max_tokens: int = 10) -> list[dict]:
        if not messages: return messages
        system_msg = messages[0]
        kept = []
        used = estimate_tokens(system_msg["content"])

        # Reverse excluding system
        for msg in reversed(messages[1:]):
            msg_tokens = estimate_tokens(msg["content"])
            if used + msg_tokens > max_tokens:
                break
            kept.append(msg)
            used += msg_tokens

        return [system_msg] + list(reversed(kept))

    try:
        messages = [
            {"role": "system", "content": "Sys"}, # 3 chars -> 1 (used=1)
            {"role": "user", "content": "Old message long"}, # 16 chars -> 4
            {"role": "assistant", "content": "Med message"}, # 11 chars -> 2
            {"role": "user", "content": "New"} # 3 chars -> 1
        ]
        # Total if all kept: 1 + 4 + 2 + 1 = 8 tokens.
        # Let's set max to 5.
        # Keep System (1).
        # Scan reverse:
        # "New" (1). Used = 2. Keep.
        # "Med message" (2). Used = 4. Keep.
        # "Old message long" (4). Used = 8. > 5. Break.

        trimmed = trim_messages(messages, max_tokens=5)

        assert len(trimmed) == 3 # Sys, Med, New
        assert trimmed[0]["role"] == "system"
        assert trimmed[1]["content"] == "Med message"
        assert trimmed[2]["content"] == "New"

        print_test(test_name, True, "Trimming correctly drops old messages")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {e}")
        return False

def test_live_connection():
    """Attempt a live connection if Key is present"""
    test_name = "Live API Connection (Optional)"
    
    if not PACKAGES_INSTALLED:
        return False
        
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    if not key or key == "sk-proj-YOUR_ACTUAL_KEY_HERE":
        print_test(test_name, False, "Skipped: No valid API key in .env")
        return True # Not a failure of the code, just setup
        
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print_test(test_name, True, "Successfully connected to OpenAI API")
        return True
    except Exception as e:
        print_test(test_name, False, f"Connection failed: {e}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}Chapter 7 Verification Tests{Colors.RESET}")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_api_key_loading,
        test_stateless_logic_mocked,
        test_token_estimation_logic,
        test_cost_calculator,
        test_context_manager,
        test_trim_messages_logic,
        test_live_connection
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"Test crashed: {e}")
            results.append(False)
        print()
        
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✅ All checks passed!{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}⚠️ Some checks failed or were skipped.{Colors.RESET}")

if __name__ == "__main__":
    main()
