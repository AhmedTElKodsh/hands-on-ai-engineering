# Scaffolding Transformation Guide

**Date**: 2026-01-21  
**Purpose**: Systematic guide for transforming complete code examples into proper scaffolding  
**Applies to**: Chapters 06A, 10, 11, 13, 14, 17 (and eventually all chapters 06A-54)

---

## Transformation Principles

### Core Philosophy

Students learn best by **doing**, not by **copying**. Our chapters should provide:

- ✅ **Structure** - Function signatures, class definitions, imports
- ✅ **Guidance** - TODO comments, hints about approach
- ✅ **Verification** - Tests to validate their implementation
- ❌ **Complete solutions** - No copy-paste ready code

### What Changes, What Stays

| Element                     | Action     | Reason                              |
| --------------------------- | ---------- | ----------------------------------- |
| Conceptual explanations     | **KEEP**   | Understanding concepts is essential |
| Analogies & stories         | **KEEP**   | These aid comprehension             |
| Function signatures         | **KEEP**   | Students need to know the interface |
| Import statements           | **KEEP**   | Students need to know dependencies  |
| Complete implementations    | **REMOVE** | Students must write this themselves |
| TODO comments               | **ADD**    | Guide students on what to implement |
| Algorithm hints             | **ADD**    | Provide approach without solution   |
| Verification scripts        | **KEEP**   | Students must test their work       |
| Error prediction challenges | **KEEP**   | These teach debugging               |

---

## Transformation Patterns

### Pattern 1: Simple Function Implementation

**BEFORE (Too Complete)**:

```python
def shout(func):
    def wrapper():
        result = func()           # Call original function
        return result.upper()     # Return uppercase version
    return wrapper
```

**AFTER (Proper Scaffolding)**:

```python
def shout(func):
    """
    Decorator that converts function output to uppercase

    Hints:
    - Create an inner wrapper() function
    - Call the original func() to get the result
    - Use .upper() method to convert to uppercase
    - Return the uppercase result
    """
    def wrapper():
        # TODO: Call func() and get the result
        # TODO: Convert result to uppercase
        # TODO: Return the uppercase result
        pass
    return wrapper
```

---

### Pattern 2: Decorator with Arguments

**BEFORE (Too Complete)**:

```python
def retry(max_attempts=3, delay=1):
    """Retry a function if it fails"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"❌ Failed after {max_attempts} attempts")
                        raise
                    wait_time = delay * (2 ** (attempt - 1))
                    print(f"⚠️  Attempt {attempt} failed: {e}")
                    print(f"   Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        return wrapper
    return decorator
```

**AFTER (Proper Scaffolding)**:

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """
    Retry a function if it fails with exponential backoff

    This is a THREE-LEVEL decorator pattern:
    - Level 1: retry(max_attempts, delay) - accepts configuration
    - Level 2: decorator(func) - accepts the function to wrap
    - Level 3: wrapper(*args, **kwargs) - runs when function is called

    Algorithm:
    1. Loop through attempts (1 to max_attempts)
    2. Try to execute the function
    3. If successful, return the result
    4. If exception occurs:
       - If last attempt, re-raise the exception
       - Otherwise, calculate wait_time using exponential backoff
       - Print retry message and sleep

    Exponential backoff formula: delay * (2 ** (attempt - 1))
    - Attempt 1: delay * 1 = 1 second
    - Attempt 2: delay * 2 = 2 seconds
    - Attempt 3: delay * 4 = 4 seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Implement retry logic with exponential backoff
            # Hint: Use a for loop from 1 to max_attempts + 1
            # Hint: Use try/except to catch exceptions
            # Hint: Calculate wait_time = delay * (2 ** (attempt - 1))
            # Hint: Use time.sleep(wait_time) to wait between attempts
            pass
        return wrapper
    return decorator
```

---

### Pattern 3: Class-Based Implementation

**BEFORE (Too Complete)**:

```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"Elapsed time: {self.elapsed:.4f} seconds")
```

**AFTER (Proper Scaffolding)**:

```python
import time

class Timer:
    """
    Context manager that measures execution time

    Usage:
        with Timer():
            # code to time

    Implementation hints:
    - __enter__ is called when entering the 'with' block
    - __exit__ is called when leaving the 'with' block
    - Store start time in __enter__
    - Calculate and print elapsed time in __exit__
    """

    def __enter__(self):
        """
        Called when entering the 'with' block

        TODO: Record the current time using time.time()
        TODO: Store it in self.start
        TODO: Return self (allows 'with Timer() as t:' syntax)
        """
        pass

    def __exit__(self, *args):
        """
        Called when exiting the 'with' block

        TODO: Record the current time as self.end
        TODO: Calculate elapsed time: self.end - self.start
        TODO: Print the elapsed time with 4 decimal places

        Note: *args captures exception info (type, value, traceback)
        We don't need to handle them here
        """
        pass
```

---

### Pattern 4: API Integration Example

**BEFORE (Too Complete)**:

```python
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

vector = get_embedding("Apple")
print(f"Dimensions: {len(vector)}")
print(f"First 5 numbers: {vector[:5]}")
```

**AFTER (Proper Scaffolding)**:

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_embedding(text):
    """
    Get embedding vector for text using OpenAI API

    API Documentation:
    - Method: client.embeddings.create()
    - Parameters:
      - input: the text to embed
      - model: "text-embedding-3-small"
    - Returns: response object with .data[0].embedding

    TODO: Call client.embeddings.create() with text and model
    TODO: Extract the embedding from response.data[0].embedding
    TODO: Return the embedding vector
    """
    pass

# Test your implementation
vector = get_embedding("Apple")
print(f"Dimensions: {len(vector)}")  # Should be 1536
print(f"First 5 numbers: {vector[:5]}")
```

---

### Pattern 5: Complete System Example (RAG)

**BEFORE (Too Complete)**:

```python
def ask_rag(question):
    print(f"\n❓ User asks: {question}")

    results = store.search(question, limit=2)
    context_text = "\n".join(results)
    print(f"🔎 System found these clues:\n{context_text}")

    prompt = f"""
    You are a helpful assistant for BuildCo.
    Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, say "I don't know."

    ---
    Context (Secret Knowledge):
    {context_text}
    ---

    Question: {question}
    """

    answer = client.generate(prompt)
    print(f"🤖 AI answers: {answer}")
    return answer
```

**AFTER (Proper Scaffolding)**:

```python
def ask_rag(question):
    """
    RAG (Retrieval-Augmented Generation) query function

    The RAG process has 3 steps:
    1. RETRIEVE: Search vector store for relevant documents
    2. AUGMENT: Add retrieved context to the prompt
    3. GENERATE: Send augmented prompt to LLM

    Parameters:
        question (str): User's question

    Returns:
        str: AI's answer based on retrieved context

    Implementation steps:
    1. Print the user's question
    2. Search the vector store for top 2 relevant documents
    3. Join the results into a single context string
    4. Create a prompt that includes:
       - System instruction (answer using ONLY context)
       - The context
       - The user's question
    5. Send prompt to LLM and get response
    6. Print and return the answer
    """
    print(f"\n❓ User asks: {question}")

    # TODO: Step 1 - RETRIEVE
    # Search the vector store for relevant documents
    # Hint: results = store.search(question, limit=2)

    # TODO: Step 2 - AUGMENT
    # Join results into context_text
    # Hint: context_text = "\n".join(results)

    print(f"🔎 System found these clues:\n{context_text}")

    # TODO: Step 3 - Create the augmented prompt
    # Include: system instruction, context, and question
    # Template provided below - fill in the variables

    prompt = f"""
    You are a helpful assistant for BuildCo.
    Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, say "I don't know."

    ---
    Context (Secret Knowledge):
    {context_text}
    ---

    Question: {question}
    """

    # TODO: Step 4 - GENERATE
    # Send prompt to LLM client
    # Hint: answer = client.generate(prompt)

    print(f"🤖 AI answers: {answer}")
    return answer
```

---

## Handling "Try This!" Sections

### Current Problem

Many "Try This!" sections provide complete solutions in `<details>` tags.

### Solution

Transform solutions into **hints** that guide without revealing.

**BEFORE**:

````markdown
<details>
<summary>✅ Solution</summary>

```python
def double_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper
```
````

</details>
```

**AFTER**:

````markdown
<details>
<summary>💡 Hint 1 - Structure</summary>

Your decorator needs:

1. An outer function that accepts `func`
2. An inner `wrapper` function that accepts `*args, **kwargs`
3. Call the original function and store the result
4. Multiply the result by 2
5. Return the doubled result

</details>

<details>
<summary>💡 Hint 2 - Code Skeleton</summary>

```python
def double_result(func):
    def wrapper(*args, **kwargs):
        # Step 1: Call the original function
        result = # TODO

        # Step 2: Double the result
        doubled = # TODO

        # Step 3: Return doubled result
        return # TODO
    return wrapper
```
````

</details>

<details>
<summary>💡 Hint 3 - Key Concepts</summary>

- Use `func(*args, **kwargs)` to call the original function
- Multiply by 2 using `* 2` operator
- Don't forget to return the wrapper function at the end

</details>
```

---

## Verification Scripts - KEEP THESE

Verification scripts are ESSENTIAL. Students need to test their implementations.

**These should remain complete and working**:

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
messages = [Message(role="user", "content="hi")]

# 1. Run Stream
print("Test 1: Consuming Stream...")
chunks = []
for chunk in mock.stream(messages):
    chunks.append(chunk)
    assert len(chunk) > 0

# 2. Reconstruct
full_text = "".join(chunks).strip()
print(f"Reconstructed: '{full_text}'")

# 3. Verify P6: Correctness
assert full_text == expected_text
print("✅ P6 Passed: Streamed content matches original text exactly.")

print("\n🎉 Chapter 10 Complete! You have mastered the flow of time.")
```

**Why keep these complete?**

- Students need working tests to validate their implementations
- Tests serve as specifications (they show what the code should do)
- Debugging broken tests teaches valuable skills

---

## Special Cases

### Conceptual Examples (KEEP Complete)

When showing a BAD example to illustrate a problem, keep it complete:

```python
# ❌ BAD EXAMPLE - Shows the problem we're solving
def call_openai(prompt: str) -> str:
    # 😫 START OF 100+ LINES OF BOILERPLATE
    import time
    start_time = time.time()
    logger.info(f"Calling OpenAI with prompt: {prompt[:50]}...")
    # ... (complete bad example)
```

**Why?** Students need to see the problem to understand why the solution matters.

### Demonstration Code (KEEP Complete)

When demonstrating a concept for the first time:

```python
# First example showing how decorators work
def say_hello(func):
    """A decorator that greets before calling the function"""
    def wrapper():
        print("👋 Hello! About to call the function...")
        func()
        print("✅ Function finished!")
    return wrapper
```

**Why?** Students need one complete example to understand the pattern before implementing it themselves.

---

## Chapter-Specific Notes

### Chapter 06A - Decorators & Context Managers

- **Keep complete**: First `say_hello` decorator (demonstrates concept)
- **Transform**: All "Try This!" practice sections
- **Transform**: `@retry`, `@timing`, `@log_calls` implementations
- **Keep complete**: Bad examples showing problems
- **Transform**: Context manager implementations

### Chapter 10 - Streaming Responses

- **Keep complete**: Conceptual generator examples
- **Transform**: OpenAI streaming implementation
- **Transform**: Mock provider streaming
- **Keep complete**: Verification scripts
- **Transform**: Error handling examples

### Chapter 11 - Structured Output

- **Transform**: Pydantic model implementations
- **Transform**: JSON parsing examples
- **Keep complete**: API response examples (for reference)
- **Keep complete**: Verification scripts

### Chapter 13 - Understanding Embeddings

- **Transform**: `get_embedding()` function
- **Transform**: `cosine_similarity()` function
- **Transform**: Mini search engine implementation
- **Keep complete**: Conceptual examples
- **Keep complete**: Verification scripts

### Chapter 14 - Vector Stores with Chroma

- **Transform**: VectorStore class implementation
- **Transform**: CRUD operations
- **Keep complete**: ChromaDB API examples (for reference)
- **Keep complete**: Verification scripts

### Chapter 17 - First RAG System

- **Transform**: `ask_rag()` function (CRITICAL)
- **Transform**: Document ingestion code
- **Transform**: Citation implementation
- **Keep complete**: Conceptual RAG flow diagram
- **Keep complete**: Verification scripts

---

## Implementation Checklist

For each chapter transformation:

- [ ] Read entire chapter to understand structure
- [ ] Identify all code blocks with complete implementations
- [ ] For each complete implementation:
  - [ ] Extract function signature and imports
  - [ ] Add comprehensive docstring with hints
  - [ ] Add TODO comments for each implementation step
  - [ ] Add algorithm description if complex
  - [ ] Replace body with `pass`
- [ ] Transform "Try This!" solutions to hints
- [ ] Verify all verification scripts remain complete
- [ ] Verify conceptual examples remain complete
- [ ] Test that chapter still makes sense pedagogically
- [ ] Create backup of original chapter

---

## Quality Assurance

After transformation, verify:

1. **Pedagogical Flow**: Does the chapter still teach effectively?
2. **Hint Quality**: Are hints helpful without giving away the answer?
3. **Completeness**: Are function signatures and imports present?
4. **Testability**: Can students verify their implementations?
5. **Consistency**: Does scaffolding level match chapter position in curriculum?

---

## Next Steps

1. **Review this guide** with Ahmed for approval
2. **Apply to Chapter 06A** as pilot
3. **Get feedback** on transformation quality
4. **Refine approach** based on feedback
5. **Apply systematically** to remaining 5 critical chapters
6. **Expand** to all 48 chapters (06A-54)

---

**The Master awaits your approval, Ahmed, before proceeding with the actual transformations.**
