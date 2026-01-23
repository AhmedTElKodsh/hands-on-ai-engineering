# Chapter 6A: Decorators & Context Managers — Enhancing Functions Without Changing Code

<!--
METADATA
Phase: Python Bridge Module 1 (PBM-1)
Time: 1.5 hours (30 minutes reading + 60 minutes hands-on)
Difficulty: ⭐⭐
Type: Foundation (Python Intermediate)
Prerequisites: Chapters 1-6 (Functions, Classes, Basic Python)
Builds Toward: Chapters 7-12 (LLM infrastructure), 23-30 (Agents)
Correctness Properties: Function behavior preservation, Resource cleanup

NAVIGATION
→ Quick Reference: #quick-reference
→ Verification: #verification
→ What's Next: #whats-next
-->

---

## ☕ Coffee Shop Intro

> **Imagine this**: You're running a coffee shop app. Every time a customer places an order, you need to:
>
> 1. Log the order details
> 2. Check if the customer is authenticated
> 3. Measure how long the order took
> 4. Handle any errors that occur
>
> You could copy-paste this logging/timing/auth code into EVERY function... but imagine doing that for 50 functions! One tiny bug means fixing it 50 times. 😱
>
> What if you could write that code ONCE and "sprinkle" it onto any function you want? That's decorators!
>
> And what if Python could automatically clean up resources (close files, disconnect from databases) even if your code crashes? That's context managers!
>
> **By the end of this chapter**, you'll feel like you have superpowers - adding features to functions in one line, and never worrying about forgetting to close files again.

---

## Prerequisites Check

Let's make sure your Python is ready:

```bash
python -c "def greet(name): return f'Hello {name}'; print(greet('World'))"
```

**If this prints "Hello World"**, you're good to go! ✅

**If it fails**, head back to Chapter 1 to set up Python properly.

**You should feel comfortable with**:

- Writing functions and calling them
- Basic classes (don't worry, we'll review)
- Try/except (we covered this in Chapter 5)

_Don't stress if some concepts are fuzzy - we'll build them up step by step!_ 😊

---

### 🔄 Quick Recall: Chapters 1-5 Concepts

Before we dive into decorators, let's refresh key concepts you'll need:

**Question 1**: What does a function return if you don't specify a `return` statement?

<details>
<summary>Click to reveal answer</summary>
`None` - Python implicitly returns `None` if no return statement is present.
</details>

**Question 2**: What's the difference between `*args` and `**kwargs`?

<details>
<summary>Click to reveal answer</summary>
- `*args` captures positional arguments as a tuple
- `**kwargs` captures keyword arguments as a dictionary
</details>

**Question 3**: In a `try/except/finally` block, when does the `finally` block run?

<details>
<summary>Click to reveal answer</summary>
ALWAYS - even if there's an exception, even if there's a return statement in try/except.
This is why it's perfect for cleanup code!
</details>

**Why we're reviewing this**: Today's decorators and context managers build directly on these concepts.
If any felt fuzzy, take 5 minutes to skim the relevant chapter before continuing.

---

## 🎓 Scaffolding Level: Guided → Independent

**Where we've been**:

- Chapters 1-5: Full code examples with detailed explanations
- Every concept explained multiple ways

**Where we are now (Chapter 6A)**:

- We'll provide complete examples for new patterns
- You'll modify and extend them in exercises
- Hints available, but try without them first!

**Where we're going**:

- Chapter 7-12: You'll write more code from requirements
- Chapter 13+: You'll design solutions with minimal scaffolding

**This is intentional growth.** You're ready for more independence!

**Current scaffolding in this chapter**:

- ✅ Complete decorator examples provided
- ✅ Pattern templates you can copy
- ✅ Hints available for all exercises
- ⏳ You write the decorator logic (with guidance)
- ⏳ You decide when to use decorators vs context managers

**If you get stuck**: That's not failure—that's the learning zone! Use the hints, but try first.

---

## What You Already Know 🧩

### 📌 From Previous Chapters

Think of this chapter as building on top of what you've learned:

<table>
<tr>
<th>Concept You Know</th>
<th>How We'll Level It Up</th>
</tr>
<tr>
<td>Functions (Ch 1-2)</td>
<td>We'll learn to wrap functions inside other functions (it's cooler than it sounds!)</td>
</tr>
<tr>
<td>Error Handling (Ch 5)</td>
<td>We'll make Python automatically handle cleanup, even when things crash</td>
</tr>
<tr>
<td>Classes (Ch 3)</td>
<td>We'll use special methods (__enter__, __exit__) to create powerful resource managers</td>
</tr>
</table>

### 🔮 Where This Leads

You'll use these skills in:

- **Chapter 7-12**: Your LLM code will use decorators for retry logic and caching (so you don't re-call expensive APIs!)
- **Chapter 23-30**: AI agents use decorators to register tools and callbacks
- **Final Project (Ch 54)**: Your Civil Engineering system will use context managers to safely handle database connections and file operations

_Trust me, this stuff will make you feel like a professional developer!_ 💪

---

### 🗺️ Concept Map: How This Chapter Connects

```
Chapter 2: Functions → Chapter 6A: Decorators → Chapter 7: LLM Retry Logic
       ↓                      ↓                        ↓
First-class objects    Wrap functions         Production patterns
       ↓                      ↓                        ↓
Chapter 5: Error Handling ← Chapter 6A: Context Mgrs ← Chapter 12: DB Connections
```

**You are here**: Chapter 6A - Learning to enhance functions and manage resources

**What you've learned**:

- Functions are objects you can pass around (Ch 2)
- Error handling with try/except (Ch 5)
- Classes with special methods (Ch 3)

**What you're learning**:

- Decorators: Wrap functions to add behavior
- Context Managers: Guarantee resource cleanup

**What's coming next**:

- Chapter 7: Use `@retry` decorator for LLM API calls
- Chapter 12: Use context managers for database connections
- Chapter 23-30: Decorators register agent tools

**The big picture**: These patterns are EVERYWHERE in professional Python code.
Master them now, use them forever!

---

## The Story: Why This Matters (Let Me Paint a Picture)

### The Problem (This Gets Messy Fast)

Okay, picture this scenario. You're building an AI app that talks to three different LLM providers: OpenAI, Anthropic, and Groq.

Every single API call needs the same stuff:

- **Logging**: "Hey, I'm calling OpenAI with this prompt..."
- **Timing**: "This call took 2.3 seconds"
- **Retry logic**: "It failed, let me try again..."
- **Error handling**: "Catch errors and log them"

So your code looks like this... _and I'm warning you, it's painful to look at_:

```python
def call_openai(prompt: str) -> str:
    # 😫 START OF 100+ LINES OF BOILERPLATE
    import time
    start_time = time.time()
    logger.info(f"Calling OpenAI with prompt: {prompt[:50]}...")

    for attempt in range(3):  # Retry 3 times
        try:
            # Finally, the actual API call!
            result = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            elapsed = time.time() - start_time
            logger.info(f"OpenAI call completed in {elapsed:.2f}s")
            return result.choices[0].message.content

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt == 2:  # Last attempt
                raise
            time.sleep(2 ** attempt)  # Wait 1s, then 2s, then 4s
    # 😫 END OF BOILERPLATE

def call_anthropic(prompt: str) -> str:
    # 😭 OH NO, WE HAVE TO COPY ALL THAT AGAIN
    import time
    start_time = time.time()
    logger.info(f"Calling Anthropic with prompt: {prompt[:50]}...")

    for attempt in range(3):
        try:
            result = anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{"role": "user", "content": prompt}]
            )
            elapsed = time.time() - start_time
            logger.info(f"Anthropic call completed in {elapsed:.2f}s")
            return result.content[0].text
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

# And you have to do this for EVERY function! 😱
```

**See the problem?**

- ❌ You copied 100+ lines of code for each function
- ❌ Found a bug in the retry logic? Fix it in 20 places
- ❌ The actual business logic (the API call) is buried in boilerplate
- ❌ This is the definition of "code smell"

_If you're thinking "there HAS to be a better way," you're absolutely right!_

---

Now let's talk about the second problem: **resource management**.

Say you need to read a file AND connect to a database:

```python
def process_document(file_path: str):
    file = open(file_path, 'r')  # Open file
    try:
        db = connect_to_database()  # Connect to DB
        try:
            content = file.read()
            db.save(content)
            # What if an error happens HERE?
        finally:
            db.close()  # Must remember to close!
    finally:
        file.close()  # Must remember to close!

# This creates the dreaded "pyramid of doom"! 🏔️
```

**The pain points**:

- ❌ Nested `try/finally` blocks look ugly
- ❌ Easy to forget to close things
- ❌ If you add a third resource (like a cache), the pyramid grows taller!
- ❌ Hard to read, hard to maintain

_Don't worry - we're about to make ALL of this go away!_ ✨

---

### The Elegant Solution (Here Comes the Magic!)

Alright, deep breath. Let me show you the beautiful solution.

**With decorators**, your LLM code transforms into this:

```python
@log_calls        # ← One line: adds logging
@timing           # ← One line: adds timing
@retry(attempts=3) # ← One line: adds retry logic
def call_openai(prompt: str) -> str:
    # Just the business logic - clean and simple!
    return openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

@log_calls
@timing
@retry(attempts=3)
def call_anthropic(prompt: str) -> str:
    # Same decorators, different function - DRY principle!
    return anthropic.messages.create(
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}]
    ).content[0].text
```

**Holy moly, look at that!** 🤩

- ✅ Boilerplate is GONE (100+ lines → 3 lines)
- ✅ Fix a bug in `@retry` once, fixes everywhere
- ✅ Business logic is crystal clear
- ✅ Add new behavior? Just add another `@decorator`!

---

**With context managers**, your resource handling becomes:

```python
def process_document(file_path: str):
    with open(file_path, 'r') as file:
        with connect_to_database() as db:
            content = file.read()
            db.save(content)
    # Both file and DB automatically closed - even if there's an error!
    # Python GUARANTEES cleanup happens. 🎯
```

**So much better!**

- ✅ No nested `try/finally` pyramids
- ✅ Resources ALWAYS cleaned up (Python guarantees it)
- ✅ Readable, maintainable code
- ✅ Can't forget to close things

> **The Big Insight**:
>
> - **Decorators** = Add superpowers to functions without editing them
> - **Context Managers** = Guarantee cleanup happens automatically
>
> Both make your code cleaner, safer, and easier to maintain.

_Now let's learn how to build these! Don't worry, I'll walk you through it step by step._ 😊

---

## Part 1: Decorators (Let's Start Simple)

### 📖 What's a Decorator, Really? (Conceptual Explanation)

Okay, let's break this down with a real-world analogy.

**Analogy: Gift Wrapping** 🎁

Imagine you have a gift (your function). A decorator is like gift wrap - it goes AROUND the gift without changing what's inside. When someone opens the wrapping, they still get the original gift, but now it looks prettier!

In Python terms:

- **Original gift** = Your function (e.g., `add(5, 3)`)
- **Gift wrap** = Decorator (adds logging, timing, etc.)
- **Wrapped gift** = Enhanced function (still does `add`, but now logs it too!)

**Here's the syntax**:

```python
@decorator_name
def my_function():
    pass
```

That little `@` symbol is Python's way of saying "wrap this function with this decorator."

_Let's see this in action with the simplest possible decorator..._

---

### 💻 Your First Decorator: Hello World Style (Code Example)

Let's create a decorator that just says "Hi!" before calling your function:

```python
def say_hello(func):
    """A decorator that greets before calling the function"""

    def wrapper():
        print("👋 Hello! About to call the function...")
        func()  # Call the original function
        print("✅ Function finished!")

    return wrapper  # Return the wrapper (don't call it!)

# Now let's use it
@say_hello
def make_coffee():
    print("☕ Making coffee...")

# When we call make_coffee(), what happens?
make_coffee()
```

**Output**:

```
👋 Hello! About to call the function...
☕ Making coffee...
✅ Function finished!
```

**Let's break down what just happened** (because this is important!):

1. **`@say_hello`** wraps `make_coffee` - it's like Python saying: `make_coffee = say_hello(make_coffee)`
2. When you call `make_coffee()`, you're actually calling `wrapper()`
3. `wrapper()` says hello, calls the ORIGINAL `make_coffee`, then says finished

_See? The original function still works - we just added behavior around it!_

---

**Analogy: Security Checkpoint at Airport** 🛂

Think of a decorator like airport security:

- **Original function** = Your flight (the actual destination)
- **Decorator** = Security checkpoint (checks you before you board)
- **Wrapped function** = You still get to your destination, but now you've been screened

Just like security doesn't change your flight, decorators don't change what your function does—they just add checks/logging/timing around it!

**In code terms**:

- Security checkpoint = `@authenticate` decorator
- Your flight = `def book_ticket()` function
- Result = Ticket only booked if you pass authentication

---

### 🔬 Try This! (Hands-On Practice #1)

Let's make sure you understand by trying it yourself!

**Challenge**: Create a decorator called `@shout` that makes any function print in ALL CAPS.

**Starter code**:

```python
def shout(func):
    def wrapper():
        # Your code here: call func(), get result, return it in uppercase
        pass
    return wrapper

@shout
def greet():
    return "hello world"

print(greet())  # Should print: HELLO WORLD
```

<details>
<summary>💡 Hint (click if you need help)</summary>

You need to:

1. Call `func()` to get the result
2. Convert result to uppercase with `.upper()`
3. Return the uppercase result

</details>

<details>
<summary>✅ Solution (check after you try!)</summary>

```python
def shout(func):
    def wrapper():
        result = func()           # Call original function
        return result.upper()     # Return uppercase version
    return wrapper

@shout
def greet():
    return "hello world"

print(greet())  # Prints: HELLO WORLD
```

</details>

_Take a moment to actually type this out and run it. Seriously! The muscle memory helps._ 💪

---

> 🤔 **Metacognitive Checkpoint #1: Understanding Decorators**
>
> Before we continue, pause for 30 seconds and reflect:
>
> - Can you explain in your own words what a decorator does?
> - How is `@decorator` different from just calling `decorator(function)`?
> - What would happen if you forgot the `return wrapper` line?
>
> Write down your answers - we'll revisit them at the end!

---

### 🤝 Handling Function Arguments (Practice Together)

Okay, so far our decorators only work with functions that take no arguments. But what about `add(5, 3)` or `greet("Ahmed")`?

**The problem**:

```python
def say_hello(func):
    def wrapper():  # ← Only accepts zero arguments!
        print("Hello!")
        return func()
    return wrapper

@say_hello
def add(a, b):
    return a + b

add(5, 3)  # ❌ ERROR: wrapper() takes 0 arguments but 2 were given
```

**The solution**: Use `*args` and `**kwargs` (trust me, this is simpler than it sounds!)

```python
def say_hello(func):
    def wrapper(*args, **kwargs):  # ← Accept ANY arguments
        print(f"Hello! Called with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)  # ← Pass them through
    return wrapper

@say_hello
def add(a, b):
    return a + b

result = add(5, 3)  # ✅ Works perfectly!
# Prints: Hello! Called with args=(5, 3), kwargs={}
```

**Let me explain `*args` and `**kwargs` in plain English\*\*:

- `*args` = "Accept any number of regular arguments" (like 5, 3, "hello")
- `**kwargs` = "Accept any number of keyword arguments" (like name="Ahmed", age=30)
- Together they mean: "I can handle ANY function signature!"

**Think of it like a universal adapter** 🔌 - it works with ANY plug shape (any function signature).

---

**Analogy: Universal Remote Control** 🎮

`*args` and `**kwargs` are like a universal remote:

- **Regular remote** = Works with one specific TV (fixed parameters)
- **Universal remote** = Works with ANY device (flexible parameters)

```python
def regular_remote(channel):
    # Only works with TVs that have channels
    pass

def universal_remote(*args, **kwargs):
    # Works with TVs, stereos, lights, anything!
    pass
```

This is why we use `*args, **kwargs` in decorators—they work with ANY function signature!

---

### 🔬 Try This! (Hands-On Practice #2)

Now let's practice with arguments!

**Challenge**: Create a `@double_result` decorator that multiplies any function's return value by 2.

```python
def double_result(func):
    def wrapper(*args, **kwargs):
        # Your code: call func with the arguments, multiply result by 2
        pass
    return wrapper

@double_result
def add(a, b):
    return a + b

@double_result
def multiply(x, y):
    return x * y

print(add(5, 3))        # Should print: 16 (because (5+3)*2 = 16)
print(multiply(4, 5))   # Should print: 40 (because (4*5)*2 = 40)
```

<details>
<summary>✅ Solution</summary>

```python
def double_result(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper
```

</details>

_Try this one yourself before looking! The struggle is where the learning happens._ 🧠

---

### 🔍 Error Prediction Challenge #1

Look at this code. Before running it, predict:

1. Will it work?
2. If not, what error will occur?
3. Why?

```python
def uppercase(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@uppercase
def greet(name):
    return f"Hello {name}"

print(greet("Ahmed"))
```

**Your prediction**: **\_\_**

<details>
<summary>Click to reveal what actually happens</summary>

**Error**: `TypeError: wrapper() takes 0 positional arguments but 1 was given`

**Why**: The `wrapper()` function doesn't accept any arguments, but we're trying to pass `"Ahmed"` to it!

**The fix**: Use `*args, **kwargs`:

```python
def uppercase(func):
    def wrapper(*args, **kwargs):  # ← Accept any arguments
        result = func(*args, **kwargs)  # ← Pass them through
        return result.upper()
    return wrapper
```

**Lesson**: Always use `*args, **kwargs` in decorator wrappers unless you know the exact signature!

</details>

---

### 💻 A Practical Example: Logging Decorator (Code Example)

Alright, now let's build something USEFUL - a decorator that logs function calls:

```python
def log_calls(func):
    """Decorator that logs when a function is called"""

    def wrapper(*args, **kwargs):
        print(f"🔵 Calling {func.__name__}()")
        print(f"   Arguments: {args}")
        print(f"   Keyword arguments: {kwargs}")

        result = func(*args, **kwargs)

        print(f"✅ {func.__name__}() returned: {result}")
        return result

    return wrapper

# Let's use it on a few functions
@log_calls
def add(a, b):
    return a + b

@log_calls
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Try them out
add(10, 5)
print()
greet("Ahmed", greeting="Hi")
```

**Output**:

```
🔵 Calling add()
   Arguments: (10, 5)
   Keyword arguments: {}
✅ add() returned: 15

🔵 Calling greet()
   Arguments: ('Ahmed',)
   Keyword arguments: {'greeting': 'Hi'}
✅ greet() returned: Hi, Ahmed!
```

**See how powerful this is?** One decorator, works on ANY function, logs everything! 🎯

---

### 💻 Another Practical Example: Timing Decorator (Code Example)

Let's create a decorator to measure how long functions take to run:

```python
import time

def timing(func):
    """Measure how long a function takes to execute"""

    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start timer

        result = func(*args, **kwargs)  # Run function

        end_time = time.time()  # End timer
        elapsed = end_time - start_time

        print(f"⏱️  {func.__name__}() took {elapsed:.4f} seconds")
        return result

    return wrapper

@timing
def slow_function():
    """Simulate a slow operation"""
    time.sleep(2)  # Sleep for 2 seconds
    return "Done!"

@timing
def fast_function():
    """Simulate a fast operation"""
    return sum(range(1000))

# Try them
result1 = slow_function()  # ⏱️ slow_function() took 2.0023 seconds
result2 = fast_function()  # ⏱️ fast_function() took 0.0001 seconds
```

_Imagine using this on your LLM API calls - you'll instantly see which ones are slow!_ 🐌

---

### 🔬 Try This! (Hands-On Practice #3)

**Challenge**: Combine `@log_calls` and `@timing` by stacking them!

```python
# Use both decorators on the same function
@log_calls
@timing
def calculate_sum(n):
    """Sum all numbers from 1 to n"""
    return sum(range(n + 1))

# Try it
calculate_sum(1000)
```

**Question**: What order do the decorators execute in? (Try to predict before running!)

<details>
<summary>💡 Answer</summary>

Decorators execute **bottom to top**!

So `@timing` runs first (wraps `calculate_sum`), then `@log_calls` wraps the result.

Output order:

1. `log_calls` says "Calling calculate_sum()"
2. `timing` starts the timer
3. Original function runs
4. `timing` stops the timer and prints duration
5. `log_calls` prints the return value

</details>

---

### 📖 The `@wraps` Decorator (Important Detail!)

Okay, here's a tricky problem. When you decorate a function, it loses its identity:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def add(a, b):
    """Add two numbers together"""
    return a + b

# Let's check the function's name and docstring
print(add.__name__)  # Prints: wrapper (NOT "add"!)
print(add.__doc__)   # Prints: None (docstring is gone!)
```

**Why does this matter?** Tools like help(), debuggers, and documentation generators rely on `__name__` and `__doc__`. If they're wrong, things break!

**The fix**: Use `functools.wraps`:

```python
from functools import wraps  # Import this!

def my_decorator(func):
    @wraps(func)  # ← This one line fixes everything!
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def add(a, b):
    """Add two numbers together"""
    return a + b

print(add.__name__)  # Prints: add ✅
print(add.__doc__)   # Prints: Add two numbers together ✅
```

**Rule of thumb**: ALWAYS use `@wraps(func)` in your decorator's wrapper function. Just make it a habit!

---

### 🎧 Decorators with Arguments (The Final Boss!)

Alright, this is where decorators get a bit mind-bending, but stay with me! ☕

Sometimes you want to CONFIGURE your decorator:

```python
@repeat(times=3)  # ← We're passing an argument to the decorator!
def greet(name):
    print(f"Hello {name}!")

greet("Ahmed")
# Should print "Hello Ahmed!" three times
```

**How do we build this?** We need THREE levels of functions (I know, bear with me!):

```python
from functools import wraps

def repeat(times):
    """Decorator that repeats function execution"""

    # Level 1: Accept decorator arguments
    def decorator(func):
        # Level 2: This is the actual decorator

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Level 3: This is what runs when function is called

            result = None
            for i in range(times):
                print(f"  [Run {i+1}/{times}]")
                result = func(*args, **kwargs)
            return result

        return wrapper
    return decorator

# Now use it
@repeat(times=3)
def greet(name):
    print(f"    Hello {name}!")

greet("Ahmed")
```

**Output**:

```
  [Run 1/3]
    Hello Ahmed!
  [Run 2/3]
    Hello Ahmed!
  [Run 3/3]
    Hello Ahmed!
```

**Let me explain the three levels**:

1. **`repeat(times)`** - Called first with `times=3`, returns `decorator`
2. **`decorator(func)`** - Wraps the actual function `greet`
3. **`wrapper(\*args, **kwargs)`** - Runs when you call `greet("Ahmed")`

Think of it like nesting dolls 🪆: Each function wraps the next!

---

**Let me show you the pattern more clearly**:

```python
def decorator_with_args(arg1, arg2):
    """Level 1: Accept configuration"""
    def decorator(func):
        """Level 2: Accept the function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Level 3: Run when function is called"""
            # Use arg1 and arg2 here
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

_I know this looks complicated, but you'll get used to the pattern. Copy this template whenever you need it!_

---

> 🤔 **Metacognitive Checkpoint #2: Three-Level Thinking**
>
> The three-level decorator pattern is tricky. Take a moment to think:
>
> - Which level runs when you write `@repeat(times=3)`?
> - Which level runs when Python decorates the function?
> - Which level runs when you call `greet("Ahmed")`?
>
> If you're unsure, that's normal! This is one of Python's more advanced patterns.
> Try drawing a diagram showing the three levels.

---

### 🔬 Try This! (Hands-On Practice #4)

**Challenge**: Create a `@add_emoji` decorator that adds an emoji to the function's return value.

```python
def add_emoji(emoji):
    """Decorator that adds an emoji to function output"""
    # Your code here (three-level structure!)
    pass

@add_emoji(emoji="🎉")
def celebrate(name):
    return f"Congratulations {name}"

@add_emoji(emoji="☕")
def offer_coffee(name):
    return f"Coffee for {name}"

print(celebrate("Ahmed"))     # Should print: Congratulations Ahmed 🎉
print(offer_coffee("Ahmed"))  # Should print: Coffee for Ahmed ☕
```

<details>
<summary>✅ Solution</summary>

```python
from functools import wraps

def add_emoji(emoji):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{result} {emoji}"
        return wrapper
    return decorator
```

</details>

---

### 💻 Real-World Power Example: Retry Decorator (Production Code)

Okay, now let's build something you'll ACTUALLY use in your LLM projects - a retry decorator with exponential backoff!

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    """
    Retry a function if it fails

    Args:
        max_attempts: Maximum number of tries
        delay: Initial delay in seconds (doubles each retry)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    # Try to run the function
                    return func(*args, **kwargs)

                except Exception as e:
                    # If this was the last attempt, give up
                    if attempt == max_attempts:
                        print(f"❌ Failed after {max_attempts} attempts")
                        raise

                    # Otherwise, wait and try again
                    wait_time = delay * (2 ** (attempt - 1))
                    print(f"⚠️  Attempt {attempt} failed: {e}")
                    print(f"   Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

        return wrapper
    return decorator

# Let's test it with a flaky function (simulates unstable API)
import random

@retry(max_attempts=4, delay=1)
def flaky_api_call(endpoint):
    """Simulates an API call that fails randomly"""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("API unavailable")
    return f"Success! Data from {endpoint}"

# Try it - might take a few attempts
result = flaky_api_call("/users")
print(f"✅ {result}")
```

**Possible output**:

```
⚠️  Attempt 1 failed: API unavailable
   Retrying in 1 seconds...
⚠️  Attempt 2 failed: API unavailable
   Retrying in 2 seconds...
✅ Success! Data from /users
```

_This decorator will save you HOURS when dealing with unreliable APIs!_ 🎯

---

> ⚠️ **Production War Story #1: The $5,000 API Bill**
>
> A startup built an AI app that called OpenAI's API. They didn't use retry logic with exponential backoff.
> When OpenAI had a brief outage (5 minutes), their app retried IMMEDIATELY in a tight loop.
>
> **The result**: 50,000 failed API calls in 5 minutes. Each call cost $0.10.
> **The bill**: $5,000 for calls that all failed.
>
> **The fix**: Add a `@retry` decorator with exponential backoff (1s, 2s, 4s, 8s).
> New cost during outages: ~$2 (just a few retries).
>
> **Lesson**: Retry logic isn't just about reliability—it's about cost control.
> The `@retry` decorator you just learned would have saved them $4,998.

---

## Transition: From Decorators to Context Managers

Okay, you've mastered decorators! Give yourself a pat on the back. 🎉

Now let's shift gears to a different problem: **managing resources**.

**The setup**: Decorators are great for adding behavior to functions. But what about situations where you need to:

- Open a file → do something → close the file
- Connect to a database → run queries → disconnect
- Acquire a lock → do work → release the lock

These all follow the same pattern: **setup → do work → cleanup**.

And here's the critical part: **cleanup must happen even if there's an error**.

That's where **context managers** come in! Let's dive in...

---

## Part 2: Context Managers (Guaranteed Cleanup!)

### 📖 What's a Context Manager, Really? (Conceptual Explanation)

Let me paint you a picture with an analogy.

**Analogy: Borrowing a Library Book** 📚

1. **Check out the book** (setup/enter)
2. **Read the book** (do your work)
3. **Return the book** (cleanup/exit)

Now, here's the key insight: The library has a RULE that you MUST return the book, even if:

- You didn't finish reading it
- You dropped coffee on it
- You lost interest

**Context managers work the same way**: They GUARANTEE cleanup happens, no matter what!

---

### The Problem Without Context Managers

Let's see the old way of handling files:

```python
# ❌ Old way (manual cleanup)
file = open('data.txt', 'r')
try:
    content = file.read()
    # Do stuff with content
finally:
    file.close()  # Must remember to close!
```

**Problems**:

- ❌ Easy to forget `file.close()`
- ❌ Need to remember `try/finally` pattern
- ❌ If you have multiple resources, you get pyramids of `try/finally` blocks

---

### 💻 The Solution: The `with` Statement (Code Example)

Python's `with` statement handles cleanup automatically:

```python
# ✅ New way (automatic cleanup)
with open('data.txt', 'r') as file:
    content = file.read()
    # Do stuff with content
# File automatically closed here - GUARANTEED!
```

**What just happened?**

1. `with open(...)` calls `__enter__()` on the file object (setup)
2. Your code block runs
3. When the block ends, Python calls `__exit__()` automatically (cleanup)
4. This happens EVEN IF THERE'S AN ERROR!

_It's like Python is babysitting your resources - it makes sure they get cleaned up no matter what!_ 👶

---

**Analogy: Hotel Room Service** 🏨

Context managers are like hotel room service:

1. **`__enter__`** = Room service brings you breakfast
2. **Your code** = You eat breakfast
3. **`__exit__`** = Room service picks up the tray (even if you didn't finish!)

The hotel GUARANTEES they'll pick up the tray, even if:

- You fell asleep
- You left the room
- You made a mess

**In Python**:

```python
with HotelService() as breakfast:
    eat(breakfast)
# Tray automatically picked up - guaranteed!
```

This is why context managers are perfect for resources—cleanup is GUARANTEED.

---

### Let's See It in Action

Here's a side-by-side comparison:

```python
# ❌ Without 'with' - you might forget to close
file = open('log.txt', 'w')
file.write('Starting process...\n')
# Oops, forgot to close! File might not be saved properly!

# ✅ With 'with' - Python guarantees it closes
with open('log.txt', 'w') as file:
    file.write('Starting process...\n')
# File automatically closed and flushed to disk!
```

**Even if there's an error**:

```python
# File STILL gets closed, even though we crashed!
with open('log.txt', 'w') as file:
    file.write('Starting process...\n')
    raise ValueError("Oh no, something went wrong!")
    # File is closed before the error propagates
```

_This is HUGE for reliability!_ 🎯

---

### 🔬 Try This! (Hands-On Practice #5)

Let's practice using `with`:

```python
# Challenge: Write a log entry to a file using 'with'
# Then read it back and print it

# Part 1: Write to file
with open('my_log.txt', 'w') as file:
    file.write('Hello from Python!\n')
    file.write('This is my first log entry.\n')

# Part 2: Read from file
with open('my_log.txt', 'r') as file:
    content = file.read()
    print(content)
```

Now try this:

1. Run the code
2. Check that `my_log.txt` was created
3. Try adding a `raise Exception("test")` between the writes
4. Notice the file still exists and has partial content (because it was properly closed!)

_The point: Python ALWAYS closes the file, even when things go wrong!_

---

### 🤝 Building Your Own Context Manager (Class-Based Practice)

Alright, now let's learn to CREATE context managers!

**The pattern**: Implement two special methods:

- `__enter__()` - Setup code, runs when entering the `with` block
- `__exit__()` - Cleanup code, runs when exiting the `with` block

Let's start super simple - a timer context manager:

```python
import time

class Timer:
    """Context manager to measure execution time"""

    def __enter__(self):
        """This runs when you enter the 'with' block"""
        print("⏱️  Timer started!")
        self.start_time = time.time()
        return self  # The value after 'as' in 'with Timer() as t'

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """This runs when you exit the 'with' block"""
        end_time = time.time()
        elapsed = end_time - self.start_time
        print(f"⏱️  Elapsed time: {elapsed:.4f} seconds")

        # Return False = let exceptions propagate normally
        # Return True = suppress the exception
        return False

# Let's use it!
with Timer():
    print("  Doing some work...")
    time.sleep(1)
    print("  Still working...")
    time.sleep(0.5)

print("All done!")
```

**Output**:

```
⏱️  Timer started!
  Doing some work...
  Still working...
⏱️  Elapsed time: 1.5023 seconds
All done!
```

**Let me break down the `__exit__` parameters** (this confuses everyone at first!):

```python
def __exit__(self, exc_type, exc_value, exc_traceback):
    # If NO error occurred:
    #   exc_type = None
    #   exc_value = None
    #   exc_traceback = None

    # If an error occurred:
    #   exc_type = The exception class (e.g., ValueError)
    #   exc_value = The actual exception instance
    #   exc_traceback = Stack trace information
```

_Think of these as Python giving you information about what happened in the `with` block._

---

**Analogy: Emergency Exit Procedures** 🚨

The `__exit__` parameters are like an emergency exit briefing:

```python
def __exit__(self, exc_type, exc_value, exc_traceback):
    # exc_type = "What kind of emergency?" (Fire? Medical?)
    # exc_value = "What exactly happened?" (Smoke detected in row 12)
    # exc_traceback = "Where did it start?" (Kitchen, then spread to cabin)
```

If there's NO emergency:

- All three are `None` (normal landing)

If there IS an emergency:

- Python tells you what happened so you can respond appropriately
- Return `False` = "Let the emergency crew handle it" (propagate exception)
- Return `True` = "I handled it, all clear" (suppress exception)

**Most of the time**, you want to return `False` (let exceptions propagate).

---

### 📖 Handling Errors in Context Managers (Understanding Behavior)

Let's see how context managers handle errors:

```python
class DatabaseConnection:
    """Simulates a database connection"""

    def __enter__(self):
        print("🔌 Connecting to database...")
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            # No error - commit changes
            print("✅ Committing transaction...")
        else:
            # Error occurred - rollback
            print(f"❌ Error: {exc_value}")
            print("🔄 Rolling back transaction...")

        print("🔌 Closing connection...")
        self.connected = False

        return False  # Let the exception propagate

# Success case
print("--- Success Case ---")
with DatabaseConnection() as db:
    print("  Inserting data...")
    print("  Data saved!")

print()

# Error case
print("--- Error Case ---")
try:
    with DatabaseConnection() as db:
        print("  Inserting data...")
        raise ValueError("Invalid data format!")
except ValueError:
    print("Caught the exception outside")
```

**Output**:

```
--- Success Case ---
🔌 Connecting to database...
  Inserting data...
  Data saved!
✅ Committing transaction...
🔌 Closing connection...

--- Error Case ---
🔌 Connecting to database...
  Inserting data...
❌ Error: Invalid data format!
🔄 Rolling back transaction...
🔌 Closing connection...
Caught the exception outside
```

_See how the connection ALWAYS gets closed, regardless of success or failure? That's the power of context managers!_ 💪

---

> 🤔 **Metacognitive Checkpoint #3: Decorators vs Context Managers**
>
> Now that you've learned both, reflect on the differences:
>
> - When would you use a decorator vs a context manager?
> - What's the key guarantee that context managers provide?
> - Can you think of a situation where you'd use BOTH together?
>
> Understanding when to use each tool is as important as knowing how they work!

---

### 🔬 Try This! (Hands-On Practice #6)

**Challenge**: Create a `LogContext` context manager that logs when you enter/exit a block of code.

```python
class LogContext:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        # Print "Entering: {name}"
        # Return self
        pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Print "Exiting: {name}"
        # Return False
        pass

# Test it
with LogContext("data processing"):
    print("  Processing data...")
    time.sleep(0.5)
    print("  Done!")
```

**Expected output**:

```
Entering: data processing
  Processing data...
  Done!
Exiting: data processing
```

<details>
<summary>✅ Solution</summary>

```python
class LogContext:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Entering: {self.name}")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(f"Exiting: {self.name}")
        return False
```

</details>

---

### 🔍 Error Prediction Challenge #2

What will this code print? Predict the output before running:

```python
class FileManager:
    def __enter__(self):
        print("Opening file")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Closing file")
        return True  # ← Note: returning True!

with FileManager() as f:
    print("Working with file")
    raise ValueError("Something went wrong!")

print("After with block")
```

**Your prediction**: **\_\_**

<details>
<summary>Click to reveal the answer</summary>

**Output**:

```
Opening file
Working with file
Closing file
After with block
```

**Surprise**: The exception was SUPPRESSED! The code continued normally.

**Why**: When `__exit__` returns `True`, it tells Python "I handled the exception, don't propagate it."

**When to use this**:

- ✅ When you want to suppress specific exceptions (like `KeyboardInterrupt` for cleanup)
- ❌ NOT for general error handling (usually return `False` to let errors propagate)

**Best practice**: Return `False` unless you have a specific reason to suppress exceptions.

</details>

---

### 💻 The Easier Way: `@contextmanager` Decorator (Simpler Pattern)

Okay, I have good news! There's a simpler way to create context managers using a decorator.

Instead of writing a class with `__enter__` and `__exit__`, you can use `@contextmanager`:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    """Simpler timer using @contextmanager"""
    # Code before 'yield' = __enter__
    print("⏱️  Timer started!")
    start_time = time.time()

    try:
        yield  # ← Pause here, run the 'with' block
    finally:
        # Code after 'yield' (in finally) = __exit__
        elapsed = time.time() - start_time
        print(f"⏱️  Elapsed: {elapsed:.4f}s")

# Use it exactly like before!
with timer():
    print("  Working...")
    time.sleep(1)
```

**How this works**:

1. Code BEFORE `yield` = setup (`__enter__`)
2. `yield` = pause, let the `with` block run
3. Code AFTER `yield` (in `finally`) = cleanup (`__exit__`)

_This is way simpler than the class-based approach!_ ✨

---

**Here's the pattern**:

```python
from contextlib import contextmanager

@contextmanager
def my_context_manager():
    # Setup code here (like __enter__)
    print("Setting up...")

    try:
        yield  # Pause here, run the 'with' block
    finally:
        # Cleanup code here (like __exit__)
        print("Cleaning up...")
```

The `finally` block ensures cleanup ALWAYS happens, even on error!

---

### 💻 A Practical Example: Temporary Directory (Production Pattern)

Let's build something useful - a context manager that creates a temp directory and cleans it up:

```python
import os
import shutil
from contextlib import contextmanager

@contextmanager
def temporary_directory(dir_name="temp_dir"):
    """Create a temporary directory, delete it when done"""

    # Setup: Create the directory
    print(f"📁 Creating directory: {dir_name}/")
    os.makedirs(dir_name, exist_ok=True)

    try:
        yield dir_name  # Give the directory name to the caller
    finally:
        # Cleanup: Delete the directory
        print(f"🗑️  Deleting directory: {dir_name}/")
        shutil.rmtree(dir_name, ignore_errors=True)

# Use it
with temporary_directory("my_temp_files") as temp_dir:
    # Create some files in the temp directory
    with open(f"{temp_dir}/data.txt", "w") as f:
        f.write("Temporary data")

    print(f"✅ Created file in {temp_dir}")
    print(f"   Files: {os.listdir(temp_dir)}")

print("Temp directory is gone now!")
print(f"Still exists? {os.path.exists('my_temp_files')}")  # False
```

**Output**:

```
📁 Creating directory: my_temp_files/
✅ Created file in my_temp_files
   Files: ['data.txt']
🗑️  Deleting directory: my_temp_files/
Temp directory is gone now!
Still exists? False
```

_This is SUPER useful for testing - create temp files, do your work, everything auto-cleans up!_ 🧹

---

> ⚠️ **Production War Story #2: The Database Connection Leak**
>
> A company's web app started crashing every few hours. The error: "Too many database connections."
>
> **The problem**: Developers forgot to close database connections in error cases:
>
> ```python
> conn = get_db_connection()
> try:
>     result = conn.query("SELECT * FROM users")
>     return result
> except Exception:
>     return None  # ← Oops! Connection never closed!
> ```
>
> After 100 errors, all 100 connection slots were full. New requests failed.
>
> **The fix**: Use context managers:
>
> ```python
> with get_db_connection() as conn:
>     result = conn.query("SELECT * FROM users")
>     return result
> # Connection ALWAYS closed, even on error!
> ```
>
> **Lesson**: Context managers aren't just convenient—they prevent resource leaks that crash production systems.
> This is why every database library provides context manager support.

---

### 🔬 Try This! (Hands-On Practice #7)

**Challenge**: Create a context manager that changes the current directory temporarily, then changes back.

```python
import os
from contextlib import contextmanager

@contextmanager
def change_directory(new_dir):
    """Temporarily change to a different directory"""
    # Save current directory
    # Change to new directory
    # Yield
    # Change back to original directory
    pass

# Test it
print(f"Currently in: {os.getcwd()}")

with change_directory(".."):  # Go up one level
    print(f"Inside 'with': {os.getcwd()}")

print(f"Back to: {os.getcwd()}")
```

<details>
<summary>✅ Solution</summary>

```python
@contextmanager
def change_directory(new_dir):
    original_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(original_dir)
```

</details>

---

### 📖 Nesting Context Managers (The Clean Way)

Sometimes you need multiple resources. You could nest `with` statements:

```python
# Option 1: Nested 'with' statements
with open('input.txt', 'r') as input_file:
    with open('output.txt', 'w') as output_file:
        content = input_file.read()
        output_file.write(content.upper())
```

But Python lets you use multiple context managers in one line:

```python
# Option 2: Multiple context managers (cleaner!)
with open('input.txt', 'r') as input_file, \
     open('output.txt', 'w') as output_file:
    content = input_file.read()
    output_file.write(content.upper())
```

_Much cleaner! No "pyramid of doom"!_ 🎯

---

## 🎯 Confidence Calibration Check

Before we build the final project, let's calibrate your understanding.

### Before the Final Exercise

Rate your confidence (1-5) on these skills:

1. **Creating basic decorators**: \_\_\_/5
   - 1: No idea how to start
   - 2: Can follow examples but can't create from scratch
   - 3: Can create with heavy reference to examples
   - 4: Can create with light reference
   - 5: Can create without any help

2. **Using `\*args, **kwargs` in decorators\*\*: \_\_\_/5

3. **Creating decorators with arguments (3-level pattern)**: \_\_\_/5

4. **Creating class-based context managers**: \_\_\_/5

5. **Understanding when to use decorators vs context managers**: \_\_\_/5

**Your average confidence**: \_\_\_/5

---

### After the Final Exercise

Now rate yourself again after completing the project:

1. **Creating basic decorators**: \_\_\_/5
2. **Using `\*args, **kwargs` in decorators\*\*: \_\_\_/5
3. **Creating decorators with arguments**: \_\_\_/5
4. **Creating class-based context managers**: \_\_\_/5
5. **Understanding when to use each**: \_\_\_/5

**Your new average**: \_\_\_/5

---

### Calibration Insight

**If your confidence went UP**: Great! The practice solidified your understanding.

**If your confidence went DOWN**: Even better! You discovered what you don't know yet.
This is called the "Dunning-Kruger dip" - it means you're learning deeply.

**If your confidence stayed the same**: You might be overconfident OR underconfident.
Try the exercises again without looking at solutions to test yourself.

**Typical pattern**: Most learners rate themselves 3-4 before, then realize they're actually 2-3 after trying.
Recognizing this gap is the first step to closing it!

---

## 🤝 Bringing It All Together: Configuration Manager (Collaborative Project)

Alright, let's build something REAL that combines everything you've learned! We're going to create a Configuration Manager that uses BOTH decorators AND context managers.

**What it will do**:

- Load config from a JSON file
- Use a decorator (`@requires_config`) to ensure config is loaded before functions run
- Use a context manager to temporarily override config values
- Log all config access

This is the kind of code you'll write in professional projects!

---

### Step 1: Create `config_manager.py`

```python
"""
Configuration Manager - Combines Decorators and Context Managers!
"""
from contextlib import contextmanager
from functools import wraps
import json
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    """Manage application configuration"""

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._config_loaded = False

    def load_from_file(self, file_path: str):
        """Load configuration from JSON file"""
        print(f"📂 Loading config from {file_path}")

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(file_path, 'r') as f:
            self._config = json.load(f)

        self._config_loaded = True
        print(f"✅ Config loaded with keys: {list(self._config.keys())}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        # Support nested keys like "database.host"
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default

        print(f"🔍 Config.get('{key}') = {value}")
        return value

    def set(self, key: str, value: Any):
        """Set a configuration value"""
        print(f"📝 Config.set('{key}', {value})")
        self._config[key] = value

    @contextmanager
    def override(self, **kwargs):
        """
        Context manager: Temporarily override config values

        Usage:
            with config.override(database__host='localhost'):
                # Config temporarily changed here
            # Original config restored here
        """
        print(f"🔄 Overriding config: {kwargs}")

        # Save original values
        original_values = {}
        for key, value in kwargs.items():
            # Convert double underscore to dot notation
            # database__host -> database.host
            key = key.replace('__', '.')

            # Save original value
            original_values[key] = self.get(key)

            # Set new value
            keys = key.split('.')
            if len(keys) == 1:
                self._config[key] = value
            else:
                # Handle nested keys
                current = self._config
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                current[keys[-1]] = value

        try:
            yield self
        finally:
            # Restore original values
            print(f"↩️  Restoring config")
            for key, value in original_values.items():
                keys = key.split('.')
                if len(keys) == 1:
                    if value is None:
                        self._config.pop(key, None)
                    else:
                        self._config[key] = value
                else:
                    current = self._config
                    for k in keys[:-1]:
                        current = current[k]
                    current[keys[-1]] = value

    def requires_config(self, func):
        """
        Decorator: Ensure config is loaded before function runs

        Usage:
            @config.requires_config
            def my_function():
                pass
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self._config_loaded:
                raise RuntimeError(
                    f"❌ Config not loaded! "
                    f"Call config.load_from_file() before using {func.__name__}()"
                )
            return func(*args, **kwargs)
        return wrapper

# Create a global config instance
config = ConfigManager()
```

**Look at what we used**:

- ✅ `@contextmanager` decorator for `override()`
- ✅ Custom decorator `requires_config()`
- ✅ `@wraps(func)` to preserve function metadata
- ✅ `with open(...)` to safely read files

_This is professional-level code using everything you learned!_ 🏆

---

### Step 2: Create `app.py`

Now let's use our configuration manager:

```python
"""
Example application using ConfigManager
"""
from config_manager import config

@config.requires_config  # ← Decorator ensures config is loaded
def connect_to_database():
    """Connect to database using configuration"""
    host = config.get('database.host', 'localhost')
    port = config.get('database.port', 5432)
    print(f"🔌 Connecting to {host}:{port}")
    return f"Connected to {host}:{port}"

@config.requires_config
def send_email(to: str, subject: str):
    """Send email using configuration"""
    smtp = config.get('email.smtp_server')
    from_addr = config.get('email.from_address')
    print(f"📧 Sending email")
    print(f"   From: {from_addr}")
    print(f"   To: {to}")
    print(f"   Subject: {subject}")
    print(f"   SMTP Server: {smtp}")
    return "Email sent!"

def main():
    print("=== Testing Configuration Manager ===\n")

    # Try calling function before loading config
    print("--- Test 1: Call without loading config ---")
    try:
        connect_to_database()
    except RuntimeError as e:
        print(f"Caught error: {e}\n")

    # Load config
    print("--- Test 2: Load config ---")
    config.load_from_file('config.json')
    print()

    # Now functions work!
    print("--- Test 3: Use config normally ---")
    connect_to_database()
    print()

    send_email('user@example.com', 'Welcome!')
    print()

    # Temporarily override config using context manager
    print("--- Test 4: Override config temporarily ---")
    with config.override(database__host='staging-db.local', database__port=3306):
        print("Inside override context:")
        connect_to_database()

    print("\nAfter override context:")
    connect_to_database()

if __name__ == '__main__':
    main()
```

---

### Step 3: Create `config.json`

```json
{
  "database": {
    "host": "prod-db.example.com",
    "port": 5432,
    "username": "admin"
  },
  "email": {
    "smtp_server": "smtp.gmail.com",
    "from_address": "noreply@example.com"
  },
  "api": {
    "timeout": 30,
    "max_retries": 3
  }
}
```

---

### Step 4: Run It!

```bash
python app.py
```

**Expected output**:

```
=== Testing Configuration Manager ===

--- Test 1: Call without loading config ---
Caught error: ❌ Config not loaded! Call config.load_from_file() before using connect_to_database()

--- Test 2: Load config ---
📂 Loading config from config.json
✅ Config loaded with keys: ['database', 'email', 'api']

--- Test 3: Use config normally ---
🔍 Config.get('database.host') = prod-db.example.com
🔍 Config.get('database.port') = 5432
🔌 Connecting to prod-db.example.com:5432

🔍 Config.get('email.smtp_server') = smtp.gmail.com
🔍 Config.get('email.from_address') = noreply@example.com
📧 Sending email
   From: noreply@example.com
   To: user@example.com
   Subject: Welcome!
   SMTP Server: smtp.gmail.com

--- Test 4: Override config temporarily ---
🔄 Overriding config: {'database__host': 'staging-db.local', 'database__port': 3306}
Inside override context:
🔍 Config.get('database.host') = staging-db.local
🔍 Config.get('database.port') = 3306
🔌 Connecting to staging-db.local:3306
↩️  Restoring config

After override context:
🔍 Config.get('database.host') = prod-db.example.com
🔍 Config.get('database.port') = 5432
🔌 Connecting to prod-db.example.com:5432
```

**Amazing, right?** Look at what you've built:

- ✅ Decorator prevents using functions without config
- ✅ Context manager temporarily overrides config
- ✅ All resources properly managed
- ✅ Clean, professional code

_This is the kind of code you'll write in Chapters 7-54!_ 🎉

---

## Common Mistakes (Learn from Others!)

### Mistake #1: Forgetting to Return `wrapper`

```python
# ❌ WRONG - Calling wrapper() instead of returning it
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper()  # ← BUG: You're calling it!

# ✅ CORRECT - Return the function, don't call it
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # ← Just return the function object
```

**Why it matters**: Decorators need to return a FUNCTION, not the RESULT of calling that function!

---

### Mistake #2: Forgetting `@wraps`

```python
# ❌ WRONG - Function loses its identity
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ✅ CORRECT - Preserves function metadata
from functools import wraps

def my_decorator(func):
    @wraps(func)  # ← Always add this!
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

**Why it matters**: Without `@wraps`, your function's name and docstring disappear!

---

### Mistake #3: Suppressing Exceptions by Accident

```python
# ❌ WRONG - Accidentally hides ALL errors
def __exit__(self, exc_type, exc_value, exc_traceback):
    self.cleanup()
    return True  # ← BUG: This suppresses exceptions!

# ✅ CORRECT - Let exceptions propagate normally
def __exit__(self, exc_type, exc_value, exc_traceback):
    self.cleanup()
    return False  # ← Exceptions propagate as expected
```

**Why it matters**: Returning `True` from `__exit__` swallows exceptions - you'll never know when something breaks!

---

### Mistake #4: Not Using `*args, **kwargs`

```python
# ❌ WRONG - Only works with zero-argument functions
def my_decorator(func):
    @wraps(func)
    def wrapper():  # ← BUG: Can't accept arguments!
        return func()
    return wrapper

# ✅ CORRECT - Works with any function signature
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # ← Flexible!
        return func(*args, **kwargs)
    return wrapper
```

**Why it matters**: Without `*args, **kwargs`, your decorator breaks most functions!

---

## Quick Reference Card

### Decorator Template (Copy This!)

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper
```

### Decorator with Arguments Template

```python
from functools import wraps

def my_decorator(arg1, arg2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use arg1 and arg2 here
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Context Manager Template (Class-Based)

```python
class MyContextManager:
    def __enter__(self):
        # Setup code
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Cleanup code
        return False  # Don't suppress exceptions
```

### Context Manager Template (Function-Based)

```python
from contextlib import contextmanager

@contextmanager
def my_context_manager():
    # Setup code
    try:
        yield  # Run the 'with' block here
    finally:
        # Cleanup code
```

---

## Verification (Test Your Knowledge!)

Let's make sure everything stuck! Run these tests:

```python
from functools import wraps

print("🧪 Running verification tests...\n")

# Test 1: Decorator preserves metadata
print("Test 1: Decorator metadata preservation")
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def greet(name):
    """Say hello"""
    return f"Hello {name}"

assert greet.__name__ == "greet", "❌ Name not preserved!"
assert greet.__doc__ == "Say hello", "❌ Docstring not preserved!"
print("✅ Passed! Decorator preserves metadata\n")

# Test 2: Context manager cleans up on error
print("Test 2: Context manager cleanup on error")
class TestResource:
    def __enter__(self):
        self.cleaned_up = False
        return self

    def __exit__(self, *args):
        self.cleaned_up = True
        return False

resource = TestResource()
try:
    with resource:
        raise ValueError("Test error")
except ValueError:
    pass

assert resource.cleaned_up, "❌ Resource not cleaned up!"
print("✅ Passed! Context manager cleans up on error\n")

# Test 3: Stacked decorators work correctly
print("Test 3: Stacked decorators")
def add_one(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + 1
    return wrapper

def multiply_two(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) * 2
    return wrapper

@add_one
@multiply_two
def get_number():
    return 5

# Execution: get_number() = 5 → multiply_two (5*2=10) → add_one (10+1=11)
result = get_number()
assert result == 11, f"❌ Expected 11, got {result}"
print(f"✅ Passed! Stacked decorators: 5 → ×2 → +1 = {result}\n")

print("🎉 All tests passed! You understand decorators and context managers!")
```

---

## Assessment

### Quick Check Questions

1. **What does `@functools.wraps(func)` do and why is it important?**

2. **In a decorator, why do we use `*args` and `**kwargs` in the wrapper function?\*\*

3. **What are the two special methods needed for a class-based context manager?**

4. **If `__exit__` returns `True`, what happens to exceptions?**

5. **When you stack decorators like this:**
   ```python
   @decorator_a
   @decorator_b
   def my_function():
       pass
   ```
   **Which decorator executes first?**

<details>
<summary>Click to see answers</summary>

1. `@wraps` preserves the original function's metadata (name, docstring, etc.). Without it, decorated functions lose their identity!

2. To make the wrapper accept ANY function signature - any number of positional or keyword arguments.

3. `__enter__()` (setup) and `__exit__()` (cleanup)

4. The exception is SUPPRESSED (swallowed). Usually you want `return False` to let exceptions propagate normally!

5. `@decorator_b` executes first because decorators are applied bottom-to-top (like layers of wrapping paper!)

</details>

---

### Coding Challenge

**Challenge**: Create a `@cache` decorator that remembers function results to avoid re-computing them.

**Requirements**:

- If function is called with same arguments, return cached result
- Print "Cache hit!" when using cached value
- Print "Computing..." when calculating new value
- Use `functools.wraps`

**Starter code**:

```python
from functools import wraps

def cache(func):
    cached_results = {}  # Dictionary to store results

    @wraps(func)
    def wrapper(*args):
        # Your code here!
        # Hint: Check if args are in cached_results
        pass

    return wrapper

@cache
def fibonacci(n):
    """Calculate Fibonacci number (slow without caching!)"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test it
print(f"fib(10) = {fibonacci(10)}")  # Should show many "Cache hit!" messages
```

<details>
<summary>💡 Hint 1</summary>

Use `args` as a dictionary key: `if args in cached_results:`

</details>

<details>
<summary>💡 Hint 2</summary>

Store the result: `cached_results[args] = result`

</details>

<details>
<summary>✅ Full Solution</summary>

```python
from functools import wraps

def cache(func):
    cached_results = {}

    @wraps(func)
    def wrapper(*args):
        if args in cached_results:
            print(f"🎯 Cache hit for {func.__name__}{args}")
            return cached_results[args]

        print(f"💫 Computing {func.__name__}{args}")
        result = func(*args)
        cached_results[args] = result
        return result

    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"Result: {fibonacci(10)}")
```

**Try it and see how much faster it is!** Without caching, `fibonacci(35)` takes minutes. With caching, it's instant! 🚀

</details>

---

## What's Next?

Congratulations, Ahmed! You just learned intermediate Python skills that professional developers use every day! 🎉

### In Chapter 6B: Error Handling Patterns, you'll learn:

- Creating custom exception classes
- The Result type pattern (Success/Failure)
- How to propagate errors elegantly
- Logging best practices for debugging

### In Chapter 6C: OOP Intermediate, you'll learn:

- Inheritance and abstract classes
- Properties and computed fields
- Class methods vs instance methods
- When to use classes vs functions

### In Chapter 7: Your First LLM Call, you'll USE decorators for:

- `@retry` - Automatically retry failed API calls
- `@cache` - Cache expensive LLM responses
- `@timing` - Measure API call performance
- `with llm_client:` - Automatically clean up connections

_Everything you learned here will make Chapters 7-12 feel natural!_

---

## Summary

**Decorators** wrap functions to add behavior without modifying their code:

- **Pattern**: `@decorator` above function definition
- **Key**: Always use `@functools.wraps(func)`
- **Flexibility**: Use `*args, **kwargs` for any signature
- **Stacking**: Multiple decorators stack bottom-to-top
- **Use cases**: Logging, timing, caching, retry logic, authentication

**Context Managers** guarantee resource cleanup using the `with` statement:

- **Pattern**: `with resource_manager() as r:`
- **Class-based**: Implement `__enter__` and `__exit__`
- **Function-based**: Use `@contextmanager` with `yield`
- **Guarantee**: Cleanup ALWAYS happens, even on errors
- **Use cases**: File handling, database connections, locks, temporary resources

**You now have the Python skills for Chapters 7-12!** 🎉

Every time you see `@retry` or `with llm_client:` in the upcoming chapters, you'll understand EXACTLY what's happening under the hood.

---

**Next**: [Chapter 6B: Error Handling Patterns →](chapter-06B-error-handling-patterns.md)

_Great job making it through Chapter 6A! You're building professional developer skills! 💪_
