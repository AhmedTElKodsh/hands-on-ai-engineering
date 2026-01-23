# Scaffolding Conversion Template
**Purpose**: Convert complete code solutions to educational scaffolding  
**Version**: 1.0  
**Date**: 2026-01-21

---

## Quick Reference: Before & After

### ❌ BEFORE (Complete Solution)
```python
def log_calls(func):
    """Decorator that logs function calls"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"Returned: {result}")
        return result
    return wrapper
```

### ✅ AFTER (Scaffolding)
```python
def log_calls(func):
    """
    Decorator that logs function calls
    
    Should:
    1. Print the function name before calling
    2. Call the original function
    3. Print the return value
    4. Return the result
    """
    def wrapper(*args, **kwargs):
        # TODO: Print function name
        # Hint: Use func.__name__ to get the name
        # Hint: Use f-string: f"Calling {func.__name__}()"
        
        # TODO: Call the original function
        # Hint: Use func(*args, **kwargs)
        result = # Your code here
        
        # TODO: Print the return value
        # Hint: f"Returned: {result}"
        
        # TODO: Return the result
        return # Your code here
    
    return wrapper
```

---

## Conversion Steps

### Step 1: Identify Complete Solutions

**Look for**:
- Working code blocks in main content
- No TODO markers
- No "Your code here" placeholders
- Implementations before exercises

**Mark for conversion**: Any code that students could copy-paste and run immediately.

---

### Step 2: Extract Learning Objectives

**Ask**:
1. What concept does this code teach?
2. What should students understand after implementing it?
3. What are the key steps in the logic?
4. What are common mistakes students make?

**Document**: Write these as comments in the scaffolding.

---

### Step 3: Create Function Skeleton

**Template**:
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Brief description of what this function does
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Steps:
    1. First major step
    2. Second major step
    3. Third major step
    """
    # Implementation goes here
    pass
```

**Keep**:
- Function signature with type hints
- Docstring with clear description
- Parameter and return descriptions
- High-level step outline

**Remove**:
- All implementation code
- Specific logic
- Working examples

---

### Step 4: Add TODO Markers

**Guidelines**:
- One TODO per logical step
- 3-5 TODOs per function (not too many, not too few)
- Each TODO should be completable in 2-5 lines of code

**Template**:
```python
# TODO: [Action Verb] [What to do]
# Hint: [Specific guidance]
# Hint: [API call or pattern]
variable = # Your code here
```

**Examples**:
```python
# TODO: Extract content from the chunk
# Hint: Access chunk.choices[0].delta.content
# Hint: Content can be None, check before using
content = # Your code here

# TODO: Build the prompt with context
# Hint: Use an f-string with {context} and {question}
# Hint: Include instruction to only use provided context
prompt = # Your code here
```

---

### Step 5: Add Progressive Hints

**Structure**:
```markdown
### 🔬 Try This! (Hands-On Practice #X)

**Challenge**: [Clear description of what to implement]

**Starter Code**:
```python
# Scaffolded code here
```

<details>
<summary>💡 Hint 1: [Topic]</summary>
[First level hint - conceptual guidance]
</details>

<details>
<summary>💡 Hint 2: [Topic]</summary>
[Second level hint - more specific guidance]
</details>

<details>
<summary>💡 Hint 3: [Topic]</summary>
[Third level hint - almost the answer]
</details>

<details>
<summary>✅ Solution (Check after you've tried!)</summary>

```python
# Complete working solution here
```

**Explanation**:
[Why this solution works]
[Key concepts demonstrated]
[Common mistakes avoided]

</details>
```

**Hint Levels**:
1. **Conceptu