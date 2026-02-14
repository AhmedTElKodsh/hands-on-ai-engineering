# Chapter 12A: Asyncio Fundamentals
**Concurrent API Calls, Streaming, and Production-Ready Async Patterns**

**Chapter Type**: Foundation | **Difficulty**: ⭐⭐ | **Time**: 2 hours
**Prerequisites**: Chapter 6B (Error Handling), Chapter 7-8 (LLM Basics)
**Builds Toward**: **CRITICAL** for Ch 13+ (async embeddings), streaming responses, concurrent API calls, all production apps

**What You'll Build**: Concurrent LLM API calls using asyncio for parallel processing, efficient resource usage, and production scalability.

**Why This Matters**: Modern AI applications are async. Every major framework (FastAPI, LangChain, LlamaIndex) uses asyncio. Whether you're streaming LLM responses, making concurrent API calls, building real-time chatbots, or deploying production apps—asyncio is essential. By the end of this chapter, you'll write production-ready async code with confidence.

---

## 🎯 Learning Objectives

By the end of this chapter, you will:

- ✅ Understand async/await syntax and when to use it
- ✅ Make concurrent API calls with `asyncio.gather()`
- ✅ Implement async context managers (`async with`)
- ✅ Handle errors in async code properly
- ✅ Know when to use async vs sync
- ✅ Understand Python's GIL and its implications
- ✅ Build production-ready async LLM clients
- ✅ Avoid common async pitfalls

---

## Part 1: The Hook - Your First Concurrent API Calls (8 Minutes)

### The Goal

You'll make **3 LLM calls in parallel** and see all 3 responses arrive concurrently—much faster than sequential calls.

### The Setup

First, let's create a simple async LLM caller (we'll simplify for now—full implementation comes later):

```python
# async_demo.py
import asyncio
import time

# Simulate an LLM API call (we'll use real ones later)
async def call_llm(prompt, delay=2):
    """Simulate an LLM API call that takes 'delay' seconds"""
    print(f"🚀 Starting: {prompt[:30]}...")
    await asyncio.sleep(delay)  # Simulates network request
    response = f"Response to: {prompt}"
    print(f"✅ Finished: {prompt[:30]}...")
    return response

# Make 3 calls in parallel
async def main():
    start = time.time()

    # The magic: asyncio.gather() runs all 3 concurrently!
    results = await asyncio.gather(
        call_llm("Tell me a joke"),
        call_llm("Write a poem"),
        call_llm("Explain asyncio")
    )

    elapsed = time.time() - start

    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"📊 Received {len(results)} responses")

# Run it
asyncio.run(main())
```

**Run it**:
```bash
python async_demo.py
```

**Output**:
```
🚀 Starting: Tell me a joke...
🚀 Starting: Write a poem...
🚀 Starting: Explain asyncio...
✅ Finished: Tell me a joke...
✅ Finished: Write a poem...
✅ Finished: Explain asyncio...

⏱️  Total time: 2.01s
📊 Received 3 responses
```

**🎉 Success!** You just made 3 concurrent API calls in **~2 seconds** instead of **~6 seconds** (sequential).

---

### What If We Did This Synchronously?

Let's compare with a non-async version:

```python
# sync_demo.py
import time

def call_llm_sync(prompt, delay=2):
    """Synchronous version"""
    print(f"🚀 Starting: {prompt[:30]}...")
    time.sleep(delay)
    print(f"✅ Finished: {prompt[:30]}...")
    return f"Response to: {prompt}"

start = time.time()

# Sequential calls (one after another)
results = [
    call_llm_sync("Tell me a joke"),
    call_llm_sync("Write a poem"),
    call_llm_sync("Explain asyncio")
]

elapsed = time.time() - start
print(f"\n⏱️  Total time: {elapsed:.2f}s")
```

**Output**:
```
🚀 Starting: Tell me a joke...
✅ Finished: Tell me a joke...
🚀 Starting: Write a poem...
✅ Finished: Write a poem...
🚀 Starting: Explain asyncio...
✅ Finished: Explain asyncio...

⏱️  Total time: 6.01s
```

**Key Insight**: Async version took **~2 seconds** (all run together), sync took **~6 seconds** (one at a time). That's a **3x speedup** for I/O-bound tasks!

---

## Part 2: Understanding What Just Happened (Deep Dive)

Now that you've seen async work, let's understand **why** and **how**.

### What Is `async`? What Is `await`?

**`async def`**: Defines an **async function** (also called a **coroutine**).

```python
async def fetch_data():
    # This is a coroutine
    return "data"
```

**`await`**: Pauses execution until the awaited operation completes, allowing other tasks to run.

```python
result = await fetch_data()  # Waits for fetch_data() to finish
```

**Analogy**: Think of `await` like a pause button. When you hit pause on Task A, the system can switch to Task B, then back to Task A when it's ready. This is called **cooperative multitasking**.

---

### Async vs Sync: The Restaurant Analogy

**Synchronous (Blocking)**:
You're a waiter. You take Order 1 to the kitchen, **stand there waiting** until it's ready, bring it to the table, then take Order 2. Inefficient!

**Asynchronous (Non-Blocking)**:
You take Order 1 to the kitchen, **leave it there**, take Order 2, Order 3, etc. When the kitchen finishes an order, you deliver it. Much more efficient!

**In Code**:
```python
# Sync: Wait for each call to finish before starting the next
response1 = call_llm("prompt1")  # Wait...
response2 = call_llm("prompt2")  # Wait...

# Async: Start all calls, then wait for all to finish
responses = await asyncio.gather(
    call_llm("prompt1"),  # Starts immediately
    call_llm("prompt2"),  # Starts immediately
)
```

---

### When Should You Use Async?

**✅ Use Async When**:
- Making API calls (LLMs, databases, external services)
- Reading/writing to disk (large files)
- Network operations (downloading, uploading)
- Waiting for user input
- **I/O-bound tasks** (waiting for something outside your code)

**❌ Don't Use Async When**:
- Doing CPU-intensive calculations (math, image processing)
- Code that doesn't wait for anything
- **CPU-bound tasks** (your code is the bottleneck, not external resources)

**Why?** Async is about **waiting efficiently**. If there's nothing to wait for, async adds complexity without benefit.

---

## Part 3: The Event Loop - Your Async Orchestrator

### What Is the Event Loop?

The **event loop** is the engine that runs async code. It manages all your coroutines and decides which one to run next.

**Analogy**: The event loop is like a manager at a restaurant kitchen. It tracks which orders are waiting, which are ready, and coordinates the waiters.

```python
import asyncio

async def task():
    await asyncio.sleep(1)
    return "Done"

# This line creates an event loop, runs task(), then closes the loop
result = asyncio.run(task())
```

**Key Point**: You typically don't manage the event loop directly. `asyncio.run()` handles it for you.

---

### Running Multiple Tasks: `asyncio.gather()`

`asyncio.gather()` runs multiple coroutines concurrently and waits for all to complete:

```python
async def main():
    results = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
    # results is a list: [result1, result2, result3]
```

**What happens**:
1. `task1()`, `task2()`, `task3()` all **start immediately**
2. The event loop switches between them as they wait (e.g., for network)
3. `gather()` waits until **all** are done
4. Returns a list of results **in order**

---

### Practical Example: Concurrent LLM Calls

Let's upgrade our demo to use a real pattern (without actual API calls—we'll add those in later chapters):

```python
import asyncio
import time

async def generate_with_llm(prompt, model="gpt-4"):
    """Simulate LLM generation"""
    print(f"📝 {model}: {prompt[:40]}...")

    # Simulate API call (in reality, this would be httpx.post() or similar)
    await asyncio.sleep(1.5)

    response = f"[{model}] Generated response to: {prompt}"
    print(f"✅ {model}: Done!")
    return response

async def compare_models(prompt):
    """Compare the same prompt across multiple models"""
    print(f"🔍 Testing prompt: {prompt}\n")

    start = time.time()

    # Run all models in parallel!
    results = await asyncio.gather(
        generate_with_llm(prompt, "gpt-4"),
        generate_with_llm(prompt, "claude-v1"),
        generate_with_llm(prompt, "llama-2")
    )

    elapsed = time.time() - start

    print(f"\n⏱️  Total: {elapsed:.2f}s (vs {1.5 * 3:.2f}s if sequential)")

    for result in results:
        print(f"  - {result}")

# Run it
asyncio.run(compare_models("Explain quantum computing in simple terms"))
```

**Output**:
```
🔍 Testing prompt: Explain quantum computing in simple terms

📝 gpt-4: Explain quantum computing in simple terms...
📝 claude-v1: Explain quantum computing in simple terms...
📝 llama-2: Explain quantum computing in simple terms...
✅ gpt-4: Done!
✅ claude-v1: Done!
✅ llama-2: Done!

⏱️  Total: 1.51s (vs 4.50s if sequential)
  - [gpt-4] Generated response to: Explain quantum computing in simple terms
  - [claude-v1] Generated response to: Explain quantum computing in simple terms
  - [llama-2] Generated response to: Explain quantum computing in simple terms
```

**Speedup**: 1.51s async vs 4.5s sync = **~3x faster!**

---

## Part 4: Async Context Managers - `async with`

### Why `async with`?

Just like regular `with` statements ensure resources are cleaned up, `async with` does the same for async resources.

**Example**: Opening an async HTTP client

```python
import httpx  # Async HTTP library

async def fetch_url(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# The client is automatically closed when exiting the 'async with' block
```

**Without `async with`** (manual cleanup):
```python
async def fetch_url(url):
    client = httpx.AsyncClient()
    try:
        response = await client.get(url)
        return response.text
    finally:
        await client.aclose()  # Must manually close!
```

**Key Insight**: `async with` guarantees cleanup, even if errors occur.

---

### Practical Example: Async LLM Client with Cleanup

```python
import asyncio

class AsyncLLMClient:
    """Async LLM client with proper resource management"""

    async def __aenter__(self):
        """Called when entering 'async with' block"""
        print("🔌 Connecting to LLM service...")
        # In reality, you'd create a connection pool here
        await asyncio.sleep(0.1)  # Simulate connection
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'async with' block"""
        print("🔌 Disconnecting from LLM service...")
        # In reality, you'd close connections here
        await asyncio.sleep(0.1)  # Simulate cleanup

    async def generate(self, prompt):
        """Generate response"""
        await asyncio.sleep(1)  # Simulate API call
        return f"Response to: {prompt}"

async def main():
    # The client is automatically cleaned up!
    async with AsyncLLMClient() as client:
        result = await client.generate("Hello")
        print(f"Got: {result}")

asyncio.run(main())
```

**Output**:
```
🔌 Connecting to LLM service...
Got: Response to: Hello
🔌 Disconnecting from LLM service...
```

**Even if an error occurs**, the cleanup (`__aexit__`) still runs!

---

## Part 5: Error Handling in Async Code

### Errors in `asyncio.gather()`

By default, `gather()` stops on the first error:

```python
async def task_that_fails():
    await asyncio.sleep(1)
    raise ValueError("Something went wrong!")

async def task_that_succeeds():
    await asyncio.sleep(1)
    return "Success"

async def main():
    try:
        results = await asyncio.gather(
            task_that_succeeds(),
            task_that_fails(),  # This will raise an error
        )
    except ValueError as e:
        print(f"❌ Error: {e}")

asyncio.run(main())
```

**Output**:
```
❌ Error: Something went wrong!
```

---

### Continue on Error: `return_exceptions=True`

If you want **all tasks to run** even if some fail:

```python
async def main():
    results = await asyncio.gather(
        task_that_succeeds(),
        task_that_fails(),
        return_exceptions=True  # Don't stop on errors
    )

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i}: ❌ {result}")
        else:
            print(f"Task {i}: ✅ {result}")

asyncio.run(main())
```

**Output**:
```
Task 0: ✅ Success
Task 1: ❌ Something went wrong!
```

**Use Case**: When calling multiple LLMs, you want responses from all that succeed, even if one fails.

---

### Practical Example: Resilient Multi-Model Calls

```python
import asyncio

async def call_model(model, prompt):
    """Call a specific model"""
    await asyncio.sleep(1)

    # Simulate: claude fails, others succeed
    if model == "claude":
        raise ConnectionError(f"{model} is unavailable")

    return f"[{model}] Response to: {prompt}"

async def resilient_multi_model(prompt):
    """Call multiple models, collect all successful responses"""
    models = ["gpt-4", "claude", "llama-2"]

    results = await asyncio.gather(
        *[call_model(m, prompt) for m in models],
        return_exceptions=True
    )

    successful = []
    failed = []

    for model, result in zip(models, results):
        if isinstance(result, Exception):
            failed.append((model, result))
        else:
            successful.append((model, result))

    print(f"✅ {len(successful)} succeeded, ❌ {len(failed)} failed\n")

    for model, response in successful:
        print(f"{model}: {response}")

    for model, error in failed:
        print(f"{model}: ❌ {error}")

asyncio.run(resilient_multi_model("Explain AI"))
```

**Output**:
```
✅ 2 succeeded, ❌ 1 failed

gpt-4: [gpt-4] Response to: Explain AI
llama-2: [llama-2] Response to: Explain AI
claude: ❌ claude is unavailable
```

**Key Insight**: `return_exceptions=True` makes your code resilient—one failure doesn't crash everything.

---

## Part 6: Advanced Pattern - Task Management

### Creating Tasks with `asyncio.create_task()`

Sometimes you want to **start a task** without waiting for it immediately:

```python
async def background_job():
    await asyncio.sleep(5)
    print("Background job done!")

async def main():
    # Start the task (runs in background)
    task = asyncio.create_task(background_job())

    # Do other work
    print("Doing other work...")
    await asyncio.sleep(1)
    print("Still working...")

    # Now wait for background task
    await task
    print("All done!")

asyncio.run(main())
```

**Output**:
```
Doing other work...
Still working...
Background job done!
All done!
```

---

### Cancelling Tasks

```python
async def long_running_task():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Task was cancelled!")
        raise  # Re-raise to properly propagate cancellation

async def main():
    task = asyncio.create_task(long_running_task())

    # Cancel after 2 seconds
    await asyncio.sleep(2)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Confirmed: Task cancelled")

asyncio.run(main())
```

**Output**:
```
Task was cancelled!
Confirmed: Task cancelled
```

**Use Case**: User cancels a long-running LLM generation.

---

## Part 7: Python's GIL and Why Async Matters

### What Is the GIL?

The **Global Interpreter Lock (GIL)** is a mechanism in Python that allows only **one thread** to execute Python bytecode at a time—even on multi-core CPUs.

**Analogy**: Imagine a library with 10 librarians but only 1 key to the book vault. Even though you have 10 librarians, only 1 can access books at a time.

### GIL's Impact

**For CPU-bound tasks** (calculations, processing):
- **Threading doesn't help** (GIL bottleneck)
- **Multiprocessing works** (separate processes, separate GILs)

**For I/O-bound tasks** (API calls, file I/O):
- **Async works great** (while one task waits for I/O, others run)
- **Threading can work** (but async is simpler and more efficient)

---

### Why Asyncio > Threading for LLM Apps

**I/O-bound workload**: LLM API calls spend most time waiting for network responses.

**Async advantages**:
1. **Efficient**: Doesn't create threads (lower overhead)
2. **Explicit**: You control exactly when tasks can switch (`await` points)
3. **Scalable**: Can handle thousands of concurrent connections
4. **Ecosystem**: Modern libraries (httpx, aiohttp, FastAPI) are async-first

**Threading drawbacks**:
1. **GIL limitations**: No true parallelism for Python code
2. **Implicit switching**: OS decides when to switch threads (less control)
3. **Overhead**: Each thread consumes memory
4. **Complexity**: Race conditions, locks, harder to debug

**Key Takeaway**: For LLM applications (API calls, streaming, I/O), **asyncio is the right choice**.

---

## Part 8: Real-World Pattern - Async LLM Client

Let's build a production-ready async LLM client:

```python
# async_llm_client.py
import asyncio
from typing import List, Dict

class AsyncLLMClient:
    """Production-ready async LLM client"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate a single response"""
        # In reality, use httpx or openai.AsyncClient here
        await asyncio.sleep(1)  # Simulate API call
        return f"[{self.model}] Response to: {prompt}"

    async def generate_batch(self, prompts: List[str]) -> List[str]:
        """Generate responses for multiple prompts concurrently"""
        tasks = [self.generate(p) for p in prompts]
        return await asyncio.gather(*tasks)

    async def compare_temperatures(self, prompt: str, temps: List[float]) -> Dict[float, str]:
        """Compare outputs at different temperatures"""
        tasks = [self.generate(prompt, temp) for temp in temps]
        results = await asyncio.gather(*tasks)
        return dict(zip(temps, results))

async def main():
    client = AsyncLLMClient(api_key="your-key", model="gpt-4")

    # Example 1: Batch processing
    print("📊 Batch processing 5 prompts...")
    prompts = [f"Prompt {i}" for i in range(5)]
    responses = await client.generate_batch(prompts)
    print(f"✅ Got {len(responses)} responses\n")

    # Example 2: Temperature comparison
    print("🌡️  Comparing temperatures...")
    comparison = await client.compare_temperatures(
        "Write a haiku",
        temps=[0.0, 0.5, 1.0]
    )
    for temp, response in comparison.items():
        print(f"  Temp {temp}: {response[:50]}...")

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 🧪 Try This! Exercises

### Exercise 1: Parallel Document Processing

**Goal**: Simulate processing multiple documents concurrently.

**Tasks**:
1. Create an async function `process_document(doc_id)` that:
   - Prints "Processing doc {doc_id}"
   - Waits 2 seconds (simulates processing)
   - Returns `f"Processed: {doc_id}"`
2. Use `asyncio.gather()` to process 10 documents in parallel
3. Measure total time (should be ~2 seconds, not ~20!)

**Starter Code**:
```python
import asyncio
import time

async def process_document(doc_id):
    # Your code here
    pass

async def main():
    start = time.time()
    # Your code here
    elapsed = time.time() - start
    print(f"Processed 10 docs in {elapsed:.2f}s")

asyncio.run(main())
```

---

### Exercise 2: Resilient Multi-Source Data Fetch

**Goal**: Fetch data from 3 sources, handle failures gracefully.

**Tasks**:
1. Create 3 async functions:
   - `fetch_source_1()`: succeeds after 1s
   - `fetch_source_2()`: fails with `ConnectionError`
   - `fetch_source_3()`: succeeds after 1.5s
2. Use `asyncio.gather(..., return_exceptions=True)`
3. Print which succeeded, which failed

**Expected Output**:
```
✅ source_1: Success
❌ source_2: ConnectionError
✅ source_3: Success
```

---

## 📚 Summary: Key Takeaways

1. **✅ `async def` defines a coroutine**: Must be awaited with `await`.

2. **✅ `await` pauses execution**: Allows other tasks to run while waiting.

3. **✅ `asyncio.run()` manages the event loop**: Run your main coroutine with this.

4. **✅ `asyncio.gather()` runs tasks concurrently**: Waits for all, returns results in order.

5. **✅ Use async for I/O-bound tasks**: API calls, file I/O, network operations.

6. **✅ Don't use async for CPU-bound tasks**: Calculations don't benefit from async.

7. **✅ `async with` for resource management**: Like regular `with`, but for async resources.

8. **✅ `return_exceptions=True` for resilience**: Let all tasks run even if some fail.

9. **✅ Python's GIL limits threading**: For I/O-bound LLM work, async > threading.

10. **✅ Modern AI frameworks are async**: FastAPI, LangChain, LlamaIndex all use asyncio.

---

## 🔗 What's Next?

With asyncio mastered, you're ready to:

- **Chapter 13+**: Build async embedding generators, concurrent vector searches
- **Streaming LLM responses**: Real-time token-by-token streaming
- **Production apps**: FastAPI endpoints handling thousands of concurrent requests
- **All advanced chapters**: Multi-agent systems, RAG pipelines, production deployments

**Asyncio is the foundation of modern AI applications**. Every production system you build will use these patterns.

---

## ✅ Verification: Test Your Knowledge

Run this verification script:

```python
# verify_chapter_12a.py
import asyncio
import time

async def test_basic_async():
    """Test basic async/await"""
    async def simple_task():
        await asyncio.sleep(0.1)
        return "done"

    result = await simple_task()
    assert result == "done"
    print("✅ Basic async/await works")

async def test_gather():
    """Test asyncio.gather()"""
    async def task(n):
        await asyncio.sleep(0.1)
        return n * 2

    results = await asyncio.gather(task(1), task(2), task(3))
    assert results == [2, 4, 6]
    print("✅ asyncio.gather() works")

async def test_concurrent_speed():
    """Test that concurrent is faster"""
    async def slow_task():
        await asyncio.sleep(0.5)

    start = time.time()
    await asyncio.gather(slow_task(), slow_task(), slow_task())
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Should take <1s, took {elapsed:.2f}s"
    print(f"✅ Concurrent execution works (took {elapsed:.2f}s, not 1.5s)")

async def test_error_handling():
    """Test error handling with return_exceptions"""
    async def failing_task():
        raise ValueError("Test error")

    async def passing_task():
        return "success"

    results = await asyncio.gather(
        passing_task(),
        failing_task(),
        return_exceptions=True
    )

    assert results[0] == "success"
    assert isinstance(results[1], ValueError)
    print("✅ Error handling works")

async def test_async_context_manager():
    """Test async with"""
    class AsyncResource:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

    async with AsyncResource() as resource:
        assert resource is not None

    print("✅ Async context managers work")

async def run_all_tests():
    await test_basic_async()
    await test_gather()
    await test_concurrent_speed()
    await test_error_handling()
    await test_async_context_manager()
    print("\n🎉 All tests passed! You've mastered asyncio fundamentals!")

if __name__ == '__main__':
    asyncio.run(run_all_tests())
```

**Run it**:
```bash
python verify_chapter_12a.py
```

**Expected Output**:
```
✅ Basic async/await works
✅ asyncio.gather() works
✅ Concurrent execution works (took 0.51s, not 1.5s)
✅ Error handling works
✅ Async context managers work

🎉 All tests passed! You've mastered asyncio fundamentals!
```

---

**You're ready for production AI development!** Async patterns are now in your toolkit. Next up: **Chapter 13 - Understanding Embeddings** (with async embedding generation!) 🚀
