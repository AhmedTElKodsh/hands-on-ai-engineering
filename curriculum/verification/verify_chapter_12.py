#!/usr/bin/env python3
"""
Verification Script for Chapter 12: Error Handling & Retries

Tests Tenacity decorator logic and retry limits (P9).
Includes tests for Projects 3-5 (Circuit Breaker, Rate Limiter, Dashboard).
"""

import sys
import time
from enum import Enum
from tenacity import retry, stop_after_attempt, wait_fixed

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Retry Limit (P9) ---
def test_retry_limit():
    """Verify that stop_after_attempt(3) stops after 3 tries"""
    counter = 0
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(0.01), reraise=True)
    def failing_fn():
        nonlocal counter
        counter += 1
        raise ValueError("Intentional Fail")
    
    try:
        failing_fn()
        print_test("Retry Limit (P9)", False, "Should have raised ValueError after 3 tries")
        return False
    except ValueError:
        assert counter == 3
        print_test("Retry Limit (P9)", True, "Retried exactly 3 times and stopped")
        return True
    except Exception as e:
        print_test("Retry Limit (P9)", False, f"Unexpected error: {e}")
        return False

# --- Test 2: Tenacity Import ---
def test_tenacity_installed():
    try:
        import tenacity
        print_test("Package Install", True, "tenacity is installed")
        return True
    except ImportError:
        print_test("Package Install", False, "tenacity is NOT installed. Run 'pip install tenacity'")
        return False

# --- Test 3: Circuit Breaker (Project 3) ---
def test_circuit_breaker():
    """Test Circuit Breaker state transitions"""
    class CircuitState(Enum):
        CLOSED = "closed"
        OPEN = "open"
        HALF_OPEN = "half_open"

    class CircuitBreaker:
        def __init__(self, failure_threshold=3, timeout=1):
            self.failure_threshold = failure_threshold
            self.timeout = timeout
            self.failure_count = 0
            self.state = CircuitState.CLOSED
            self.last_failure_time = None

        def call(self, func):
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time >= self.timeout:
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit OPEN")

            try:
                result = func()
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    self.state = CircuitState.OPEN
                raise e

    try:
        breaker = CircuitBreaker(failure_threshold=3, timeout=1)

        # Trigger failures to open circuit
        for _ in range(3):
            try:
                breaker.call(lambda: (_ for _ in ()).throw(Exception("Fail")))
            except:
                pass

        # Verify circuit opened
        assert breaker.state == CircuitState.OPEN

        # Test circuit blocks requests
        try:
            breaker.call(lambda: "success")
            print_test("Circuit Breaker (Project 3)", False, "Should block when OPEN")
            return False
        except Exception as e:
            assert "Circuit OPEN" in str(e)

        # Wait for timeout and test half-open
        time.sleep(1.1)
        breaker.call(lambda: "success")  # Should transition to HALF_OPEN then CLOSED
        assert breaker.state == CircuitState.CLOSED

        print_test("Circuit Breaker (Project 3)", True, "State transitions work correctly")
        return True
    except Exception as e:
        print_test("Circuit Breaker (Project 3)", False, str(e))
        return False

# --- Test 4: Rate Limiter (Project 4) ---
def test_rate_limiter():
    """Test Rate Limiter token bucket logic"""
    class RateLimiter:
        def __init__(self, tokens_per_second, burst_size):
            self.rate = tokens_per_second
            self.burst_size = burst_size
            self.tokens = burst_size
            self.last_update = time.time()

        def _refill_tokens(self):
            now = time.time()
            elapsed = now - self.last_update
            new_tokens = elapsed * self.rate
            self.tokens = min(self.burst_size, self.tokens + new_tokens)
            self.last_update = now

        def try_acquire(self, tokens_needed=1):
            self._refill_tokens()
            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

    try:
        # Test burst capacity
        limiter = RateLimiter(tokens_per_second=2, burst_size=5)
        allowed = sum(1 for _ in range(7) if limiter.try_acquire())
        assert allowed == 5, f"Burst should allow 5, got {allowed}"

        # Test refill
        time.sleep(1)  # Allow 2 tokens to refill
        assert limiter.try_acquire(), "Should refill after waiting"

        print_test("Rate Limiter (Project 4)", True, "Token bucket logic works")
        return True
    except Exception as e:
        print_test("Rate Limiter (Project 4)", False, str(e))
        return False

# --- Test 5: Resilience Dashboard (Project 5) ---
def test_resilience_dashboard():
    """Test Dashboard metrics tracking"""
    from collections import defaultdict

    class Dashboard:
        def __init__(self):
            self.metrics = defaultdict(lambda: {"total": 0, "success": 0, "failed": 0})

        def record_call(self, endpoint, success):
            m = self.metrics[endpoint]
            m["total"] += 1
            if success:
                m["success"] += 1
            else:
                m["failed"] += 1

        def get_success_rate(self, endpoint):
            m = self.metrics[endpoint]
            if m["total"] == 0:
                return 0
            return (m["success"] / m["total"]) * 100

    try:
        dashboard = Dashboard()

        # Simulate mixed calls
        for i in range(10):
            dashboard.record_call("api1", i % 3 != 0)  # 67% success rate

        # Verify tracking
        assert dashboard.metrics["api1"]["total"] == 10
        rate = dashboard.get_success_rate("api1")
        assert 60 <= rate <= 70, f"Expected ~67%, got {rate}%"

        print_test("Resilience Dashboard (Project 5)", True,
                  f"Metrics tracking works ({rate:.0f}% success rate)")
        return True
    except Exception as e:
        print_test("Resilience Dashboard (Project 5)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 12 Verification{Colors.RESET}")
    print("="*60)

    tests = [
        test_tenacity_installed,
        test_retry_limit,
        test_circuit_breaker,
        test_rate_limiter,
        test_resilience_dashboard
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
        print(f"\n{Colors.GREEN}✅ All Chapter 12 tests passed!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
