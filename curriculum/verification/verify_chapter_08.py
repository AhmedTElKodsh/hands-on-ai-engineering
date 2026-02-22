#!/usr/bin/env python3
"""
Verification Script for Chapter 8: Multi-Provider LLM Client

Tests the Action-First "Universal Adapter" pattern and the Resilience logic.
Includes tests for Project 3 (Cost Optimizer) and Project 4 (Health Checker).
"""

import sys
import time
import unittest
from typing import Dict, List
from collections import deque
from unittest.mock import MagicMock

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Universal Adapter (Action-First Code) ---
def test_universal_adapter_pattern():
    """Verify the polymorphism logic of the Action-First example"""
    try:
        class AI_Adapter:
            def chat(self, msg): raise NotImplementedError
        
        class MockOpenAI(AI_Adapter):
            def chat(self, msg): return "OpenAI Response"
            
        class MockAnthropic(AI_Adapter):
            def chat(self, msg): return "Claude Response"
            
        def get_client(name):
            return MockOpenAI() if name == "openai" else MockAnthropic()
            
        # Test Swapping
        c1 = get_client("openai")
        c2 = get_client("anthropic")
        
        assert c1.chat("Hi") == "OpenAI Response"
        assert c2.chat("Hi") == "Claude Response"
        
        print_test("Universal Adapter Pattern", True, "Polymorphism works correctly")
        return True
    except Exception as e:
        print_test("Universal Adapter Pattern", False, str(e))
        return False

# --- Test 2: Resilient Router (Fallback Logic) ---
def test_resilient_router_logic():
    """Verify fallback logic works when primary fails"""
    try:
        # Mock Clients
        primary = MagicMock()
        primary.chat.side_effect = Exception("500 Server Error") # Fails
        
        backup = MagicMock()
        backup.chat.return_value = "Backup Success" # Succeeds
        
        class ResilientRouter:
            def __init__(self, providers):
                self.providers = providers
            
            def chat(self, msg):
                for p in self.providers:
                    try:
                        return p.chat(msg)
                    except:
                        continue
                raise Exception("All failed")
                
        # Run Router
        router = ResilientRouter([primary, backup])
        result = router.chat("Hello")
        
        assert result == "Backup Success"
        assert primary.chat.call_count == 1
        assert backup.chat.call_count == 1
        
        print_test("Resilient Fallback Logic", True, "Successfully switched to backup")
        return True
    except Exception as e:
        print_test("Resilient Fallback Logic", False, str(e))
        return False

# --- Test 3: Imports ---
def test_imports():
    try:
        import openai
        import anthropic
        print_test("Package Imports", True, "openai and anthropic installed")
        return True
    except ImportError as e:
        print_test("Package Imports", False, f"Missing: {e}")
        return False

# --- Test 4: Cost Optimizer (Project 3) ---
def test_cost_optimizer():
    """Test Cost Optimizer logic - provider cost comparison"""
    try:
        class CostOptimizer:
            def __init__(self):
                self.providers = {
                    "gpt-3.5-turbo": {"input_cost": 0.0015, "output_cost": 0.002},
                    "claude-haiku": {"input_cost": 0.00025, "output_cost": 0.00125},
                    "groq-mixtral": {"input_cost": 0.0005, "output_cost": 0.001}
                }

            def estimate_tokens(self, text: str) -> int:
                """Rough token estimate (1 token ≈ 4 characters)"""
                return max(1, len(text) // 4)

            def estimate_cost(self, provider: str, input_tokens: int, output_tokens: int) -> float:
                """Calculate cost for given provider and token counts"""
                pricing = self.providers[provider]
                input_cost = (input_tokens / 1000) * pricing["input_cost"]
                output_cost = (output_tokens / 1000) * pricing["output_cost"]
                return input_cost + output_cost

            def select_cheapest(self, prompt: str, expected_output: int = 100) -> tuple:
                """Find cheapest provider for given input/output"""
                input_tokens = self.estimate_tokens(prompt)

                costs = {}
                for provider in self.providers:
                    costs[provider] = self.estimate_cost(provider, input_tokens, expected_output)

                cheapest = min(costs, key=costs.get)
                most_expensive = max(costs, key=costs.get)
                savings = costs[most_expensive] - costs[cheapest]

                return cheapest, costs[cheapest], savings

        # Test cost calculation
        optimizer = CostOptimizer()

        # Test 1: Long prompt (should favor cheaper input cost)
        prompt = "A" * 1000  # ~250 tokens
        provider, cost, savings = optimizer.select_cheapest(prompt, expected_output=500)

        assert provider in optimizer.providers, "Should return valid provider"
        assert cost > 0, "Cost should be positive"
        assert savings >= 0, "Savings should be non-negative"
        assert provider == "claude-haiku", "Should select Claude Haiku for long prompts"

        # Test 2: Cost comparison
        cost_haiku = optimizer.estimate_cost("claude-haiku", 1000, 500)
        cost_gpt = optimizer.estimate_cost("gpt-3.5-turbo", 1000, 500)
        assert cost_haiku < cost_gpt, "Haiku should be cheaper for this workload"

        # Test 3: Verify pricing accuracy
        # GPT-3.5: (1000/1000 * 0.0015) + (500/1000 * 0.002) = 0.0025
        expected_gpt_cost = 0.0025
        assert abs(cost_gpt - expected_gpt_cost) < 0.0001, f"GPT cost calculation incorrect"

        print_test("Cost Optimizer (Project 3)", True,
                  f"Haiku ${cost_haiku:.6f} vs GPT ${cost_gpt:.6f} (saves ${savings:.6f})")
        return True
    except Exception as e:
        print_test("Cost Optimizer (Project 3)", False, str(e))
        return False

# --- Test 5: Health Checker (Project 4) ---
def test_health_checker():
    """Test Health Checker logic - provider health monitoring"""
    try:
        class HealthChecker:
            def __init__(self, providers: dict, failure_threshold: int = 3):
                self.providers = providers
                self.failure_threshold = failure_threshold
                self.health_status = {}

                for name in providers:
                    self.health_status[name] = {
                        "is_healthy": True,
                        "consecutive_failures": 0,
                        "total_requests": 0,
                        "total_failures": 0,
                        "response_times": deque(maxlen=10),
                        "avg_response_time": 0.0
                    }

            def ping_provider(self, provider_name: str) -> tuple:
                """Simulate health check (returns success, response_time)"""
                if provider_name == "failing":
                    return False, 0.0
                return True, 0.1

            def check_provider(self, provider_name: str):
                """Check single provider health"""
                status = self.health_status[provider_name]
                status["total_requests"] += 1

                success, response_time = self.ping_provider(provider_name)

                if success:
                    status["consecutive_failures"] = 0
                    status["is_healthy"] = True
                    status["response_times"].append(response_time)
                else:
                    status["consecutive_failures"] += 1
                    status["total_failures"] += 1

                    if status["consecutive_failures"] >= self.failure_threshold:
                        status["is_healthy"] = False

                # Update average response time
                if status["response_times"]:
                    status["avg_response_time"] = sum(status["response_times"]) / len(status["response_times"])

            def get_healthy_providers(self) -> list:
                """Return list of healthy provider names"""
                return [name for name, status in self.health_status.items()
                       if status["is_healthy"]]

        # Test health checker
        providers = {
            "openai": {"endpoint": "https://api.openai.com"},
            "anthropic": {"endpoint": "https://api.anthropic.com"},
            "failing": {"endpoint": "https://failing.com"}
        }

        checker = HealthChecker(providers, failure_threshold=3)

        # Test 1: All providers start healthy
        healthy = checker.get_healthy_providers()
        assert len(healthy) == 3, "All providers should start healthy"

        # Test 2: Successful checks maintain health
        checker.check_provider("openai")
        checker.check_provider("openai")
        assert checker.health_status["openai"]["is_healthy"], "Should remain healthy"
        assert checker.health_status["openai"]["consecutive_failures"] == 0

        # Test 3: Multiple consecutive failures mark unhealthy
        checker.check_provider("failing")
        checker.check_provider("failing")
        checker.check_provider("failing")
        assert not checker.health_status["failing"]["is_healthy"], "Should be unhealthy after 3 failures"
        assert checker.health_status["failing"]["consecutive_failures"] == 3

        # Test 4: Response time tracking
        assert len(checker.health_status["openai"]["response_times"]) == 2
        assert checker.health_status["openai"]["avg_response_time"] == 0.1

        print_test("Health Checker (Project 4)", True,
                  f"Health tracking works: {len(checker.get_healthy_providers())}/3 providers healthy")
        return True
    except Exception as e:
        print_test("Health Checker (Project 4)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 8 Verification{Colors.RESET}")
    print("="*60)

    tests = [
        test_imports,
        test_universal_adapter_pattern,
        test_resilient_router_logic,
        test_cost_optimizer,
        test_health_checker
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

    print("="*60)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print(f"\n{Colors.GREEN}✅ All Chapter 8 tests passed!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
