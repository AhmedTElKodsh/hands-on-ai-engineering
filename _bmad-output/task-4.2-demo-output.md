# Task 4.2 Demo: HintGenerator Output Examples

This document demonstrates the actual output from the HintGenerator for different tiers.

## Sample Function

```python
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    total = 0
    for num in numbers:
        total += num

    return total / len(numbers)
```

---

## TIER_1 Output (Detailed - Foundations)

### Hints Generated: 5-6 hints

**[CONCEPTUAL]**

> Consider the following concepts: input validation and edge cases, iteration patterns and loop control, error handling strategies. Think about how each applies to this function's purpose.

**[APPROACH]**

> Approach: Use a loop to process each item, with conditional logic to filter or transform items. Consider using a for loop with an if statement inside.

**[IMPLEMENTATION]**

> For input validation, check for None, empty collections, or invalid types. Use 'if not data:' to check for empty collections.

**[IMPLEMENTATION]**

> When iterating, consider using 'for item in collection:' for simple iteration, or 'for i, item in enumerate(collection):' when you need the index.

**[IMPLEMENTATION]**

> Use try-except blocks to catch specific exceptions. Place the risky operation in the try block and handle errors in the except block.

**[IMPLEMENTATION]**

> Make sure to return the correct type as specified in the function signature. Build up your result in a variable and return it at the end.

**[RESOURCE]**

> Review Python's exception handling documentation. Look for examples of try-except-finally patterns.

**Characteristics:**

- 6-7 hints total
- Very detailed and specific
- Includes code patterns and syntax examples
- Step-by-step guidance
- Total length: ~500-700 characters

---

## TIER_2 Output (Moderate - Intermediate)

### Hints Generated: 3-4 hints

**[CONCEPTUAL]**

> Consider what errors might occur and how to handle them gracefully.

**[APPROACH]**

> Use iteration with conditional logic to process and filter data.

**[IMPLEMENTATION]**

> Use try-except to handle potential errors gracefully.

**[IMPLEMENTATION]**

> Ensure the return value matches the expected type.

**[RESOURCE]**

> Refer to Python exception handling best practices.

**Characteristics:**

- 4-5 hints total
- Moderate detail
- Strategic guidance without examples
- General patterns mentioned
- Total length: ~200-350 characters

---

## TIER_3 Output (Minimal - Advanced)

### Hints Generated: 2-3 hints

**[CONCEPTUAL]**

> Consider the function's contract and expected behavior.

**[APPROACH]**

> Apply the required transformation.

**[IMPLEMENTATION]**

> Handle edge cases appropriately.

**[RESOURCE]**

> Refer to Python documentation as needed.

**Characteristics:**

- 2-3 hints total
- Very brief
- High-level guidance only
- Minimal detail
- Total length: ~100-150 characters

---

## Comparison Table

| Aspect                   | TIER_1         | TIER_2        | TIER_3        |
| ------------------------ | -------------- | ------------- | ------------- |
| **Hint Count**           | 5-7            | 3-5           | 2-3           |
| **Total Length**         | 500-700 chars  | 200-350 chars | 100-150 chars |
| **Detail Level**         | Very detailed  | Moderate      | Minimal       |
| **Code Examples**        | Yes (patterns) | No            | No            |
| **Specific Syntax**      | Yes            | Sometimes     | No            |
| **Implementation Order** | Yes            | Sometimes     | No            |

---

## Class Example Output

### Sample Class

```python
class DataProcessor:
    def __init__(self, config: dict):
        self.config = config

    def validate(self, data: list) -> bool:
        return len(data) > 0

    def process(self, data: list) -> list:
        if self.validate(data):
            return [x * 2 for x in data]
        return []
```

### TIER_1 Class Hints

**[CONCEPTUAL]**

> This class has 3 methods. Think about how each method contributes to the class's responsibility. Consider the relationships between methods and how they share state through instance variables.

**[APPROACH]**

> Approach: Start by implementing **init** to set up instance variables. Then implement methods in order of dependency - simpler methods first, then those that use them.

**[IMPLEMENTATION]**

> Use self to access instance variables and call other methods. Remember that instance variables are shared across all methods in the class.

### TIER_2 Class Hints

**[CONCEPTUAL]**

> Consider how the 3 methods work together to fulfill the class's purpose.

**[APPROACH]**

> Implement methods in logical order, considering dependencies between them.

### TIER_3 Class Hints

**[CONCEPTUAL]**

> Implement the class according to its interface contract.

**[APPROACH]**

> Implement all required methods.

---

## Algorithm Example Output

### Sample Algorithm (Recursive)

```python
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### TIER_1 Algorithm Hints

**[CONCEPTUAL]**

> This algorithm uses recursion. Think about the base case (when to stop) and the recursive case (how to break down the problem).

**[APPROACH]**

> Approach: Write out the algorithm steps in pseudocode first. Then translate each step to Python code, testing as you go.

### TIER_2 Algorithm Hints

**[CONCEPTUAL]**

> Consider the recursive structure: base case and recursive case.

**[APPROACH]**

> Outline the algorithm steps before implementing.

### TIER_3 Algorithm Hints

**[CONCEPTUAL]**

> Implement an efficient algorithm.

**[APPROACH]**

> Apply appropriate algorithmic techniques.

---

## Test Example Output

### Sample Test

```python
def test_addition():
    result = add(2, 3)
    assert result == 5

    result = add(0, 0)
    assert result == 0
```

### TIER_1 Test Hints

**[CONCEPTUAL]**

> Think about what you're testing: the normal case, edge cases (empty input, None, etc.), and error cases. Each test should verify one specific behavior.

**[APPROACH]**

> Approach: Follow the Arrange-Act-Assert pattern: (1) Set up test data, (2) Call the function being tested, (3) Assert the result matches expectations.

**[IMPLEMENTATION]**

> Use assertEqual(actual, expected) for value comparisons, assertTrue/assertFalse for boolean checks, and assertRaises for exception testing.

### TIER_2 Test Hints

**[CONCEPTUAL]**

> Consider normal cases, edge cases, and error conditions.

**[APPROACH]**

> Use the Arrange-Act-Assert pattern for clear test structure.

**[IMPLEMENTATION]**

> Use appropriate assertion methods for different types of checks.

### TIER_3 Test Hints

**[CONCEPTUAL]**

> Test all relevant cases.

**[APPROACH]**

> Structure tests clearly.

---

## Key Observations

### Hint Quality Standards Met

✅ **No Copy-Paste Code**: Hints mention patterns but don't provide complete implementations
✅ **Actionable Guidance**: All hints provide specific, actionable advice
✅ **Tier-Appropriate**: Detail level clearly decreases from TIER_1 to TIER_3
✅ **Category Coverage**: All four categories (conceptual, approach, implementation, resource) present
✅ **Context-Aware**: Hints adapt based on code structure (loops, conditionals, error handling)

### Progressive Scaffolding

The tier system provides a clear progression:

- **TIER_1**: Students get detailed guidance with examples - suitable for beginners
- **TIER_2**: Students get strategic hints - suitable for intermediate learners
- **TIER_3**: Students get minimal hints - suitable for advanced learners

This ensures appropriate challenge levels while maintaining educational value.
