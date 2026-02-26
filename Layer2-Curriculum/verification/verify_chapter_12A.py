#!/usr/bin/env python3
"""
Verification Script for Chapter 12A: Asyncio Fundamentals

Tests all code examples and concepts from the chapter to ensure they work correctly.
Run this after completing Chapter 12A to verify all async examples are functional.

Usage:
    python verify_chapter_12A.py
"""

import asyncio
import sys
import time
from typing import List


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


async def test_basic_async_await():
    """Test basic async/await syntax"""
    test_name = "Basic Async/Await Syntax"
    
    try:
        async def simple_async_function():
            await asyncio.sleep(0.1)
            return "Hello from async!"
        
        result = await simple_async_function()
        assert result == "Hello from async!"
        
        print_test(test_name, True, "Successfully executed async function")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def test_asyncio_gather():
    """Test asyncio.gather() for concurrent execution"""
    test_name = "Asyncio.gather() - Concurrent Execution"
    
    try:
        async def task(n: int, delay: float):
            await asyncio.sleep(delay)
            return f"Task {n} complete"
        
        # Measure time for concurrent execution
        start = time.time()
        results = await asyncio.gather(
            task(1, 0.1),
            task(2, 0.1),
            task(3, 0.1)
        )
        elapsed = time.time() - start
        
        # Verify results
        assert len(results) == 3
        assert results[0] == "Task 1 complete"
        assert results[1] == "Task 2 complete"
        assert results[2] == "Task 3 complete"
        
        # Verify concurrent execution (should be ~0.1s, not 0.3s)
        assert elapsed < 0.2, f"Tasks ran sequentially ({elapsed:.2f}s), not concurrently"
        
        print_test(test_name, True, f"3 tasks completed concurrently in {elapsed:.2f}s")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def test_async_context_manager():
    """Test async context managers (async with)"""
    test_name = "Async Context Managers (async with)"
    
    try:
        class AsyncResource:
            def __init__(self):
                self.opened = False
                self.closed = False
            
            async def __aenter__(self):
                await asyncio.sleep(0.01)
                self.opened = True
                return self
            
            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await asyncio.sleep(0.01)
                self.closed = True
        
        # Test async context manager
        async with AsyncResource() as resource:
            assert resource.opened
            assert not resource.closed
        
        # Verify cleanup happened
        assert resource.closed
        
        print_test(test_name, True, "Successfully used async context manager")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def test_error_handling_async():
    """Test error handling in async code"""
    test_name = "Error Handling in Async Code"
    
    try:
        async def failing_task():
            await asyncio.sleep(0.01)
            raise ValueError("Intentional error")
        
        async def successful_task():
            await asyncio.sleep(0.01)
            return "Success"
        
        # Test individual error handling
        try:
            await failing_task()
            print_test(test_name, False, "Expected ValueError was not raised")
            return False
        except ValueError as e:
            assert str(e) == "Intentional error"
        
        # Test gather with return_exceptions
        results = await asyncio.gather(
            successful_task(),
            failing_task(),
            return_exceptions=True
        )
        
        assert results[0] == "Success"
        assert isinstance(results[1], ValueError)
        
        print_test(test_name, True, "Successfully handled async errors")
        return True
    except Exception as e:
        print_test(test_name, False, f"Unexpected error: {str(e)}")
        return False


async def test_async_vs_sync_performance():
    """Test performance difference between async and sync"""
    test_name = "Async vs Sync Performance Comparison"
    
    try:
        # Simulate I/O-bound operations
        async def async_io_task(n: int):
            await asyncio.sleep(0.1)
            return n * 2
        
        def sync_io_task(n: int):
            time.sleep(0.1)
            return n * 2
        
        # Test async (concurrent)
        start = time.time()
        async_results = await asyncio.gather(*[async_io_task(i) for i in range(5)])
        async_time = time.time() - start
        
        # Test sync (sequential)
        start = time.time()
        sync_results = [sync_io_task(i) for i in range(5)]
        sync_time = time.time() - start
        
        # Verify results are same
        assert async_results == sync_results
        
        # Verify async is faster (should be ~0.1s vs ~0.5s)
        assert async_time < sync_time / 2, "Async should be significantly faster"
        
        speedup = sync_time / async_time
        print_test(test_name, True, 
                  f"Async: {async_time:.2f}s, Sync: {sync_time:.2f}s, Speedup: {speedup:.1f}x")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def test_coroutine_vs_function():
    """Test understanding of coroutines vs regular functions"""
    test_name = "Coroutines vs Regular Functions"
    
    try:
        # Regular function
        def regular_function():
            return "regular"
        
        # Coroutine function
        async def coroutine_function():
            await asyncio.sleep(0.01)
            return "coroutine"
        
        # Test regular function
        result1 = regular_function()
        assert result1 == "regular"
        
        # Test coroutine (must await)
        result2 = await coroutine_function()
        assert result2 == "coroutine"
        
        # Verify coroutine without await returns coroutine object
        coro = coroutine_function()
        assert asyncio.iscoroutine(coro)
        await coro  # Clean up
        
        print_test(test_name, True, "Successfully distinguished coroutines from functions")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def test_concurrent_api_calls_simulation():
    """Test simulated concurrent API calls pattern"""
    test_name = "Concurrent API Calls (Simulated)"
    
    try:
        # Simulate API calls to different services
        async def call_api(service: str, delay: float):
            await asyncio.sleep(delay)
            return {
                "service": service,
                "status": "success",
                "data": f"Response from {service}"
            }
        
        # Make concurrent calls
        start = time.time()
        results = await asyncio.gather(
            call_api("OpenAI", 0.1),
            call_api("Anthropic", 0.1),
            call_api("Groq", 0.1)
        )
        elapsed = time.time() - start
        
        # Verify all calls succeeded
        assert len(results) == 3
        assert all(r["status"] == "success" for r in results)
        assert results[0]["service"] == "OpenAI"
        assert results[1]["service"] == "Anthropic"
        assert results[2]["service"] == "Groq"
        
        # Verify concurrent execution
        assert elapsed < 0.2, "API calls should run concurrently"
        
        print_test(test_name, True, f"3 API calls completed concurrently in {elapsed:.2f}s")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def test_task_cancellation():
    """Test task cancellation"""
    test_name = "Task Cancellation"
    
    try:
        async def long_running_task():
            try:
                await asyncio.sleep(10)
                return "completed"
            except asyncio.CancelledError:
                return "cancelled"
        
        # Create and cancel task
        task = asyncio.create_task(long_running_task())
        await asyncio.sleep(0.01)  # Let it start
        task.cancel()
        
        result = await task
        assert result == "cancelled"
        
        print_test(test_name, True, "Successfully cancelled async task")
        return True
    except Exception as e:
        print_test(test_name, False, f"Error: {str(e)}")
        return False


async def main():
    """Run all verification tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Chapter 12A Verification Tests{Colors.RESET}")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_async_await,
        test_asyncio_gather,
        test_async_context_manager,
        test_error_handling_async,
        test_async_vs_sync_performance,
        test_coroutine_vs_function,
        test_concurrent_api_calls_simulation,
        test_task_cancellation,
    ]
    
    results = []
    for test in tests:
        results.append(await test())
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
    print(f"  Passed: {Colors.GREEN}{passed}{Colors.RESET}/{total}")
    print(f"  Failed: {Colors.RED}{total - passed}{Colors.RESET}/{total}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}")
        print(f"Chapter 12A async examples are working correctly.\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.RESET}")
        print(f"Please review the failed tests above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
