# Chapter 10: Streaming Responses — The "Matrix" Effect

<!--
METADATA
Phase: 1 - LLM Fundamentals
Time: 1.5 hours (30 min reading + 60 min hands-on)
Difficulty: ⭐⭐
Type: Implementation
Prerequisites: Chapter 8 (Multi-Provider Client)
Builds Toward: Interactive UIs (Ch 32), Real-time Agents
Correctness Properties: P5 (Chunk Ordering), P6 (Response Reconstruction)
Project Thread: User Experience

NAVIGATION
→ Quick Reference: #quick-reference-card
→ Verification: #verification-required-section
→ What's Next: #whats-next
-->

---

## ☕ Coffee Shop Intro

> **Imagine this**: You're at a coffee shop, and you ask the barista for a complicated drink - a triple-shot, half-caf, oat milk latte with vanilla and cinnamon.
>
> **Option A (Batch Processing)**: The barista says "OK" and disappears into the back room. You wait. And wait. 5 minutes pass. You wonder if they forgot. You check your phone. You consider leaving. Finally, after 8 minutes, they emerge with your perfect drink. But you're annoyed - you had no idea what was happening!
>
> **Option B (Streaming)**: The barista says "OK, starting your drink!" You hear the espresso machine hiss. "Pulling shots..." You see them steam the milk. "Adding oat milk..." They sprinkle cinnamon. "Almost done..." They hand you the drink. Same 8 minutes, but you were engaged the whole time!
>
> **LLMs are like that complicated drink order.** Generating a 500-word essay takes 20-30 seconds. If you show a blank screen, users think your app crashed. If you stream the words as they're generated, it feels instant and alive - like watching someone type in real-time.
>
> **By the end of this chapter**, you'll transform your LLM client from "batch processing" to "real-time streaming", making your apps feel 10x faster even though the actual generation time is the same. You'll learn Python generators, streaming APIs, and the UX patterns that make AI feel magical. 🚀

---

## Prerequisites Check

```bash
# Verify Python version (generators behave consistently in 3.10+)
python --version
```

---

### 🔄 Quick Recall: Chapters 7-9 Concepts

Before we dive into streaming, let's refresh key concepts you'll need:

**Question 1**: From Chapter 8, what does the `MultiProviderClient` do?

<details>
<summary>Click to reveal answer</summary>
It abstracts away provider-specific details and provides fallback logic. If OpenAI fails, it automatically tries Anthropic. This pattern will be important for streaming too!
</details>

**Question 2**: From Chapter 9, what's the difference between `return` and `yield`?

<details>
<summary>Click to reveal answer</summary>
`return` gives you everything at once and ends the function. `yield` gives you one item, pauses, and can be resumed later. This is the foundation of streaming!
</details>

**Question 3**: From Chapter 7, what's a "token" in LLM terms?

<details>
<summary>Click to reveal answer</summary>
A token is roughly a word or word fragment. LLMs generate tokens one at a time, which is why streaming is natural - we're just exposing that token-by-token generation to the user!
</details>

**Why we're reviewing this**: Streaming builds on provider abstraction (Ch 8) and uses generators (Python fundamentals). If any felt fuzzy, take 5 minutes to review before continuing.

---

## 🎓 Scaffolding Level: Semi-Independent → Independent

**Where we've been**:

- Chapters 7-9: We provided complete implementations with detailed explanations
- You followed patterns and adapted them to your needs

**Where we are now (Chapter 10)**:

- We'll show you the streaming pattern
- You'll implement it across multiple providers
- You'll make decisions about error handling and UX
- You'll debug generator-specific issues

**Where we're going**:

- Chapter 11-15: You'll design your own data structures and APIs
- Chapter 17-22: You'll architect complete RAG systems
- You'll make architectural decisions about when to stream vs batch

**This is intentional growth.** You're moving from "implementing patterns" to "designing systems"!

**Current scaffolding in this chapter**:

- ✅ Generator pattern explained with examples
- ✅ Streaming API implementation provided
- ⏳ You decide when to use streaming vs batch
- ⏳ You handle streaming errors and edge cases
- ⏳ You design the UX for partial responses

**If you get stuck**: That's the learning zone! Think through the trade-offs before checking hints.

---

### 🗺️ Concept Map: How This Chapter Connects

```
Chapter 7: First LLM Call → Chapter 8: Multi-Provider → Chapter 10: Streaming
        ↓                            ↓                          ↓
   Basic API calls            Provider abstraction      Real-time responses
        ↓                            ↓                          ↓
Chapter 9: Prompts ← Chapter 10: Stream Prompts ← Chapter 32: Interactive UIs
```

**You are here**: Chapter 10 - Learning real-time streaming patterns

**What you've learned**:

- Basic LLM API calls (Ch 7)
- Multi-provider abstraction (Ch 8)
- Prompt engineering (Ch 9)
- Python generators (fundamentals)

**What you're learning**:

- Generator functions with yield
- Streaming API implementation
- Real-time UX patterns
- Error handling for streams
- Response reconstruction

**What's coming next**:

- Chapter 11: Structured output (JSON streaming)
- Chapter 32: Interactive chat UIs
- Chapter 39: Production streaming with monitoring

**The big picture**: Streaming is the standard for modern LLM applications. Every production chatbot, writing assistant, and AI tool uses streaming. This is a foundational skill!

---

## The Story: The "Frozen" App

### The Problem (The Wait)

You built a "Blog Post Generator".
User clicks "Generate".
... (5 seconds) ...
... (15 seconds) ...
... (30 seconds) ...
User: "It's broken." _Refreshes page_.

The server was working hard! But the user got zero feedback.

### The Naive Solution (Loading Spinner)

> "I'll just put a spinner on the screen!"

Better, but still boring. And for long tasks, users lose patience after ~10 seconds even with a spinner.

### The Elegant Solution (Streaming)

We want to show the first word the _millisecond_ it's ready.
To do this, we need to learn a Python superpower: **Generators**.

---

**Analogy: Water Fountain vs Water Bottle** 💧

**Batch Processing (return)**: Like filling a water bottle from a fountain. You wait for the entire bottle to fill (30 seconds), then you can drink. If you're thirsty NOW, you're out of luck.

**Streaming (yield)**: Like drinking directly from the fountain. Water flows immediately. You get the first sip in 1 second, and you keep drinking as it flows. Same total amount, but instant gratification!

**In code**:

```python
# Batch: Wait for everything
def get_water_batch():
    time.sleep(30)  # Fill entire bottle
    return "Full bottle of water"

# Stream: Get water immediately
def get_water_stream():
    for second in range(30):
        time.sleep(1)
        yield "💧"  # One sip at a time
```

**LLM Streaming**: Same concept! Instead of waiting 30 seconds for the full essay, you see words immediately as they're generated.

---

> ⚠️ **Production War Story #1: The $12,000 Timeout Disaster**
>
> A startup built a "Legal Document Analyzer" using GPT-4. They used non-streaming mode:
>
> ```python
> response = client.generate(long_document)  # Wait for full response
> return response
> ```
>
> **The problem**: GPT-4 took 45-60 seconds for long documents. Their web server had a 30-second timeout.
>
> **The result**:
>
> - Server killed the request after 30 seconds
> - But OpenAI still charged for the full generation (60 seconds of compute)
> - Users saw "Request Timeout" errors
> - They paid for responses they never received!
>
> **The cost**: $12,000 in wasted API calls over 2 months before they noticed.
>
> **The fix**: Switch to streaming:
>
> ```python
> for chunk in client.stream(long_document):
>     send_to_user(chunk)  # Send immediately, reset timeout
> ```
>
> Now the server stays alive because it's constantly sending data. No more timeouts!
>
> **Lesson**: Streaming isn't just about UX - it prevents timeout errors and wasted API costs!

---

## Part 1: Generators & `yield` (The Pause Button) 📖💻

Most functions `return` a value and stop.
**Generators** `yield` a value and _pause_. They can be resumed later.

---

**Analogy: Assembly Line Manufacturing** 🏭

**Traditional Function (return)**: Like a factory that builds 1000 cars, stores them in a warehouse, then ships them all at once. You need a HUGE warehouse (memory) and customers wait forever.

**Generator (yield)**: Like an assembly line that ships each car as soon as it's done. No warehouse needed (low memory), customers get cars immediately (low latency).

**In Python**:

```python
# Traditional: Build everything first (high memory)
def build_cars_batch():
    cars = []
    for i in range(1000):
        cars.append(f"Car {i}")  # Stores in memory
    return cars  # Returns all at once

# Generator: Build and ship one at a time (low memory)
def build_cars_stream():
    for i in range(1000):
        yield f"Car {i}"  # Ships immediately, no storage
```

**Why this matters for LLMs**: A long response might be 10,000 tokens. With `return`, you store all 10,000 in memory. With `yield`, you only hold one token at a time!

---

### 🔬 Try This! (Hands-On Practice #1) 💻🤝

Let's build a fake "slow downloader" to understand `yield`.

**Create `test_generator.py`**:

```python
import time

# Standard Function (The "Loading Bar")
def get_numbers_standard():
    print("Standard: Gathering numbers...")
    result = []
    for i in range(1, 4):
        time.sleep(1) # Simulate work
        result.append(i)
    return result # Returns EVERYTHING at the end

# Generator Function (The "Stream")
def get_numbers_stream():
    print("Stream: Starting...")
    for i in range(1, 4):
        time.sleep(1) # Simulate work
        yield i # Returns ONE item and pauses

print("--- Testing Standard ---")
# We have to wait 3 seconds before seeing ANYTHING
nums = get_numbers_standard()
print(nums)

print("\n--- Testing Stream ---")
# We see items AS they happen (every 1 second)
for num in get_numbers_stream():
    print(f"Received: {num}")
```

**Run it**. Notice how the "Stream" prints updates _during_ execution, while "Standard" waits until the very end? That's the magic.

---

### 🔍 Error Prediction Challenge #1

What will this code print?

```python
def my_generator():
    print("Starting...")
    yield 1
    print("Middle...")
    yield 2
    print("Ending...")

gen = my_generator()
print("Generator created")
```

**Your prediction**: **\*\***\_\_\_**\*\***

<details>
<summary>Click to reveal what happens</summary>

**Output**: `Generator created`

**Why**: Creating a generator does NOT execute its code! The function body only runs when you start iterating.

**The surprise**: None of the print statements inside `my_generator()` execute yet!

**What happens when you iterate**:

```python
gen = my_generator()
print("Generator created")  # Prints immediately
next(gen)  # NOW prints "Starting..." and returns 1
next(gen)  # Prints "Middle..." and returns 2
next(gen)  # Prints "Ending..." and raises StopIteration
```

**Lesson**: Generators are lazy! They don't do work until you ask for it. This is why streaming is memory-efficient - you never load the entire response into memory!

</details>

---

> 🤔 **Metacognitive Checkpoint #1: Generators vs Lists**
>
> Before we continue, pause and reflect:
>
> - Why does `yield` make streaming possible but `return` doesn't?
> - What happens to memory when you return a list of 1 million items vs yielding them one by one?
> - When would you NOT want to use streaming (hint: think about retries)?
>
> Write down your reasoning - understanding the trade-offs is crucial!

---

## Part 2: Updating the Base Class 📖💻

We need to teach our `LLMProvider` how to stream.

---

**Analogy: Restaurant Kitchen Updates** 🍽️

**Non-Streaming API**: You order food. The waiter disappears. 30 minutes later, they bring your meal. You had no idea if they forgot, if the kitchen was on fire, or if your food was coming.

**Streaming API**: You order food. The waiter says "Chef is preparing your appetizer... Appetizer ready!... Main course cooking... Main course ready!... Dessert coming..." You know exactly what's happening.

**In code**:

```python
# Non-streaming: Silent until done
def prepare_meal():
    cook_appetizer()
    cook_main()
    cook_dessert()
    return "Full meal"  # 30 minutes of silence, then boom

# Streaming: Updates as you go
def prepare_meal_stream():
    yield "Appetizer ready"
    cook_appetizer()
    yield "Main course ready"
    cook_main()
    yield "Dessert ready"
    cook_dessert()
```

**LLM Streaming**: Same pattern! Instead of silence followed by a wall of text, you get word-by-word updates.

---

### 🔬 Try This! (Hands-On Practice #2) 💻

Update your `shared/infrastructure/llm/base.py` to include a `stream` method.

```python
# shared/infrastructure/llm/base.py
from abc import ABC, abstractmethod
from typing import List, Iterator, Any # Add Iterator
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, messages: List[Message], **kwargs) -> str:
        """Non-streaming generation."""
        pass

    # NEW METHOD!
    @abstractmethod
    def stream(self, messages: List[Message], **kwargs) -> Iterator[str]:
        """Streaming generation (returns an iterator of chunks)."""
        pass
```

**What is `Iterator[str]`?**
It means this function returns a generator that yields strings (chunks of text) one by one.

---

## Part 3: Implementing OpenAI Streaming 💻

OpenAI supports streaming out of the box with `stream=True`.

---

**Analogy: GPS Navigation** 🗺️

**Batch Mode**: GPS calculates your entire route (5 minutes), then shows you all 47 turns at once. Overwhelming and useless!

**Streaming Mode**: GPS tells you "In 500 feet, turn left" (first instruction), then "In 2 miles, turn right" (next instruction). You get information exactly when you need it.

**In LLM terms**:

```python
# Batch: Overwhelming wall of text
response = client.generate("Write a 10-step tutorial")
print(response)  # All 10 steps at once after 30 seconds

# Stream: Digestible, real-time
for chunk in client.stream("Write a 10-step tutorial"):
    print(chunk, end="", flush=True)  # One word at a time
```

**Why users prefer streaming**: Human brains process information sequentially. Streaming matches how we naturally read and think!

---

### 🔬 Try This! (Hands-On Practice #3) 💻🤝

Update `shared/infrastructure/llm/openai_provider.py`.

```python
# Add to OpenAIProvider class:

    def stream(self, messages: List[Message], **kwargs) -> Iterator[str]:
        # 1. Format messages
        formatted_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]

        # 2. Call API with stream=True
        stream = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4o-mini"),
            messages=formatted_messages,
            temperature=kwargs.get("temperature", 0.7),
            stream=True # <--- THE MAGIC SWITCH
        )

        # 3. Yield chunks
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content: # content can be None (e.g. at the end)
                yield content
```

---

### 🔍 Error Prediction Challenge #2

What's wrong with this streaming code?

```python
def stream_response(prompt: str):
    try:
        stream = client.stream(prompt)
        return stream
    except Exception as e:
        print(f"Error: {e}")
        return None

# Usage
result = stream_response("Hello")
for chunk in result:
    print(chunk)
```

**Your prediction**: Will the try/except catch streaming errors?

<details>
<summary>Click to reveal the problem</summary>

**NO!** The try/except is in the wrong place!

**Why**: The `client.stream(prompt)` call returns a generator immediately - it doesn't execute the API call yet. The actual API call happens when you start iterating with `for chunk in result`.

**The bug**: If the API fails during streaming, the error happens OUTSIDE the try/except block, so it's never caught!

**The fix**: Wrap the iteration, not the generator creation:

```python
def stream_response(prompt: str):
    stream = client.stream(prompt)
    return stream

# Usage - Error handling at iteration time
result = stream_response("Hello")
try:
    for chunk in result:
        print(chunk)
except Exception as e:
    print(f"Streaming error: {e}")
```

Or handle errors inside the generator:

```python
def safe_stream(prompt: str):
    try:
        for chunk in client.stream(prompt):
            yield chunk
    except Exception as e:
        yield f"\n[Error: {e}]"
```

**Lesson**: Generator errors happen during iteration, not during creation! Always wrap the `for` loop in try/except!

</details>

---

> 🤔 **Metacognitive Checkpoint #2: Stream Error Handling**
>
> Think about what happens when streaming fails:
>
> - If the API fails after sending 50% of the response, can you retry?
> - How would you implement a fallback provider for streaming?
> - Should you buffer chunks before displaying them to the user?
>
> These aren't easy questions - they're the difference between demo code and production code!

---

## Part 4: Mocking the Matrix 💻

We need our `MockProvider` to support streaming too, so we can test without paying OpenAI.

### 🔬 Try This! (Hands-On Practice #4) 💻🤝

Update `shared/infrastructure/llm/mock_provider.py`.

```python
import time
from typing import Iterator

# Add to MockProvider class:

    def stream(self, messages: List[Message], **kwargs) -> Iterator[str]:
        print(f"👻 [MOCK] Streaming response...")
        words = self.fixed_response.split(" ")
        for word in words:
            time.sleep(0.1) # Simulate "thinking" time
            yield word + " "
```

---

> ⚠️ **Production War Story #2: The Partial Response Bug**
>
> A team built a chatbot that streamed responses. They stored the conversation history like this:
>
> ```python
> # WRONG!
> for chunk in client.stream(prompt):
>     print(chunk)
>     # Forgot to save chunks!
>
> # Next turn - history is incomplete!
> messages.append({"role": "assistant", "content": ???})
> ```
>
> **The problem**: They displayed chunks to the user but never reconstructed the full response for history.
>
> **The result**:
>
> - Second question: "What did you just say about X?"
> - Bot: "I don't recall saying anything about X"
> - Users thought the bot had amnesia!
>
> **The cost**: 2 weeks of debugging, angry beta testers, delayed launch.
>
> **The fix**: Always reconstruct the full response:
>
> ```python
> chunks = []
> for chunk in client.stream(prompt):
>     print(chunk, end="", flush=True)
>     chunks.append(chunk)  # Save it!
>
> full_response = "".join(chunks)
> messages.append({"role": "assistant", "content": full_response})
> ```
>
> **Lesson**: Streaming is for display, but you still need the full text for conversation history, logging, and analytics!

---

## Bringing It All Together: The Streaming Client 💻🤝

Finally, update the main Client to expose this new power.

**Update `shared/infrastructure/llm/client.py`**:

```python
from typing import Iterator

# Add to MultiProviderClient class:

    def stream(self, prompt: str) -> Iterator[str]:
        messages = [Message(role="user", content=prompt)]

        # Note: We're skipping fallback logic for simplicity here,
        # but in production you'd try/except the stream too!
        return self.primary_provider.stream(messages)
```

**Now, let's create the "Matrix" visualizer!**

**Create `matrix_chat.py`**:

```python
import sys
from shared.infrastructure.llm.client import MultiProviderClient

# Use Mock for free testing, or "openai" for real magic
client = MultiProviderClient(provider="mock") # Try changing to "openai" later!

prompt = "Write a haiku about coding."
print(f"User: {prompt}\n")
print("AI: ", end="", flush=True)

# The Streaming Loop
for chunk in client.stream(prompt):
    # print(chunk) -> This puts every word on a new line (Bad)
    # print(chunk, end="") -> This appends to the same line (Good)
    # flush=True -> Forces Python to show text IMMEDIATELY
    print(chunk, end="", flush=True)

print("\n\n(Stream Complete)")
```

**Run it**: `python matrix_chat.py`

**Observe**:

- With Mock: It prints word... by... word...
- With OpenAI: It flows like typing.

---

## Common Mistakes (Learn from Others!) 📖⚠️

### Mistake #1: Buffering Output

Python's `print()` buffers output by default. If you don't use `flush=True` (or configure your environment), you might see nothing for 5 seconds, then the whole chunk at once.
**Fix**: `print(chunk, end="", flush=True)`

### Mistake #2: Catching Errors in Streams

Errors inside a generator don't happen when you _call_ the function. They happen when you _loop_ over it.

```python
# This won't catch the error!
try:
    gen = client.stream(prompt)
except Exception: ...

# This WILL catch the error:
try:
    for chunk in gen: ...
except Exception: ...
```

### Mistake #3: Ignoring `None`

OpenAI chunks sometimes have `content=None` (e.g., the "stop" signal at the end).
**Fix**: Always check `if content:` before yielding.

---

> 🤔 **Metacognitive Checkpoint #3: UX Design Decisions**
>
> Reflect on the user experience trade-offs:
>
> - When is streaming better than showing a progress bar?
> - What if the first chunk takes 5 seconds to arrive - should you show a spinner first?
> - How do you handle streaming in a mobile app with spotty network?
>
> Great engineers think about the user, not just the code!

---

## Quick Reference Card 📖👁️

### Python Generators

```python
def my_gen():
    yield "Hello"
    yield " "
    yield "World"

# Usage
for part in my_gen():
    print(part, end="")
```

### Stream vs Non-Stream

| Feature         | `generate()` (Non-stream)        | `stream()` (Stream)   |
| --------------- | -------------------------------- | --------------------- |
| **Return Type** | `str`                            | `Iterator[str]`       |
| **Speed**       | Slow (waits for full completion) | Instant (first token) |
| **UX**          | Static                           | Dynamic               |
| **Cost**        | Same                             | Same                  |

---

## 🎯 Confidence Calibration Check

Before we verify your streaming implementation, let's calibrate your understanding.

### Before the Verification

Rate your confidence (1-5) on these skills:

1. **Understanding generators and yield**: \_\_\_/5
   - 1: No idea how yield works
   - 2: Can use generators but don't understand why
   - 3: Understand yield with heavy reference
   - 4: Can explain generators to others
   - 5: Can design complex generator patterns

2. **Implementing streaming APIs**: \_\_\_/5

3. **Handling streaming errors**: \_\_\_/5

4. **Reconstructing streamed responses**: \_\_\_/5

5. **Choosing when to stream vs batch**: \_\_\_/5

**Your average confidence**: \_\_\_/5

---

### After the Verification

Now rate yourself again after completing the verification:

1. **Understanding generators and yield**: \_\_\_/5
2. **Implementing streaming APIs**: \_\_\_/5
3. **Handling streaming errors**: \_\_\_/5
4. **Reconstructing streamed responses**: \_\_\_/5
5. **Choosing when to stream vs batch**: \_\_\_/5

**Your new average**: \_\_\_/5

---

### Calibration Insight

**If your confidence went UP**: Great! The hands-on practice solidified your understanding.

**If your confidence went DOWN**: Even better! You discovered edge cases you hadn't considered.
This is the "conscious incompetence" stage - you're aware of gaps, which means you can fill them.

**If your confidence stayed the same**: You might be overconfident OR underconfident.
Try implementing streaming in a real project to test yourself.

**Typical pattern**: Most learners rate themselves 4 before, then realize they're actually 2-3 after trying.
Streaming looks simple until you handle errors, timeouts, and partial responses!

---

## Verification (Test Your Knowledge!) 💻🤝

We need to prove that streaming yields the _correct_ text and ordering. This is Property **P5** and **P6**.

**Create `verify_streaming.py`**:

```python
"""
Verification script for Chapter 10.
Property P6: Reconstructed stream == Full text.
"""
from shared.infrastructure.llm.mock_provider import MockProvider
from shared.infrastructure.llm.base import Message

print("🧪 Running Streaming Verification...\n")

# Setup
expected_text = "This is a mock response."
mock = MockProvider(fixed_response=expected_text)
messages = [Message(role="user", content="hi")]

# 1. Run Stream
print("Test 1: Consuming Stream...")
chunks = []
for chunk in mock.stream(messages):
    chunks.append(chunk)
    # Validate P5: Chunk Ordering (basic check)
    # In mock, we split by space, so chunks should act like words
    assert len(chunk) > 0

# 2. Reconstruct
full_text = "".join(chunks).strip() # Mock adds trailing spaces
print(f"Reconstructed: '{full_text}'")

# 3. Verify P6: Correctness
assert full_text == expected_text
print("✅ P6 Passed: Streamed content matches original text exactly.")

print("\n🎉 Chapter 10 Complete! You have mastered the flow of time.")
```

**Run it:** `python verify_streaming.py`

---

## Summary

**What you learned:**

1. ✅ **Latency vs Perception**: Streaming makes apps _feel_ faster, even if the total time is the same.
2. ✅ **Generators**: `yield` allows Python functions to pause and resume.
3. ✅ **Streaming API**: How to toggle `stream=True` in OpenAI.
4. ✅ **UI Handling**: Using `flush=True` to bypass print buffering.
5. ✅ **Correctness**: Proving that the sum of the parts equals the whole (P6).

**Key Takeaway**: Streaming is the standard for LLM applications. Users expect it. It transforms a "batch process" into a "conversation."

**Skills unlocked**: 🎯

- Asynchronous-style programming (Generators)
- User Experience (UX) Engineering
- Real-time data handling

**Looking ahead**: Now we can talk to the LLM, and we can do it fast. But the LLM is just guessing. It creates unstructured text. In **Chapter 11**, we will force the LLM to output **Structured Data (JSON)** so we can use it in code reliably!

---

**Next**: [Chapter 11: Structured Output with Pydantic →](chapter-11-structured-output.md)
