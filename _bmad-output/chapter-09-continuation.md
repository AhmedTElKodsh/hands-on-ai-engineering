## Common Mistakes

### Mistake #1: Loose Braces `{}` in Prompts

If you are generating JSON examples inside a Python f-string or `.format()` call, you need to escape braces.
**Bad**: `template = "Return JSON: {"key": "value"}"` (Python thinks `{key}` is a variable).
**Good**: `template = "Return JSON: {{ \"key\": \"value\" }}"` (Double braces escape them).

### Mistake #2: Huge Prompts

Don't put 50 examples in the prompt. It costs money (tokens) and confuses the model ("Lost in the Middle" phenomenon). 3-5 examples is usually the sweet spot.

### Mistake #3: Silent Failures

If you use simple string replacement (`str.replace()`) instead of `.format()`, you won't get errors if you miss a variable. The prompt will just contain `{name}` literally, and the LLM will be very confused.

---

## Quick Reference Card

### CIF Pattern

- **C**ontext (Persona)
- **I**nstructions (Task)
- **F**ormat (Output style)

### Python Formatting

```python
template = "Hello {name}"
output = template.format(name="Ahmed")
```

### Escaping JSON in Templates

```python
# To output: {"status": "ok"}
template = "{{ \"status\": \"ok\" }}"
```

---

## 🎯 Confidence Calibration Check

**Before moving to verification, assess your understanding:**

Rate your confidence (1-5) on each skill:

**1. CIF Pattern Application**

- Can you identify Context, Instructions, and Format in a prompt?
- Can you write a prompt using the CIF pattern?
- **Self-rating:** \_\_\_/5

**2. Template Variable Substitution**

- Can you create a `PromptTemplate` with variables?
- Can you predict errors from missing/extra variables?
- **Self-rating:** \_\_\_/5

**3. Few-Shot Example Design**

- Can you write 3-5 effective examples for a task?
- Can you identify when examples contradict instructions?
- **Self-rating:** \_\_\_/5

**4. Prompt Debugging**

- Can you debug template validation errors?
- Can you fix inconsistent few-shot examples?
- **Self-rating:** \_\_\_/5

**5. Production Prompt Management**

- Do you understand when to use templates vs f-strings?
- Can you design a centralized prompt registry?
- **Self-rating:** \_\_\_/5

<details>
<summary>💡 <strong>Calibration Guide</strong></summary>

**If you rated yourself 4-5 on all skills:**

- ✅ You're ready for verification
- ✅ Proceed with confidence
- ✅ Consider helping others learn

**If you rated yourself 3 on any skill:**

- ⚠️ Review that section before verification
- ⚠️ Try the hands-on exercises again
- ⚠️ You'll probably pass verification but might struggle

**If you rated yourself 1-2 on any skill:**

- ❌ Re-read that section carefully
- ❌ Complete all hands-on exercises
- ❌ Don't proceed to verification yet

**Calibration check:**

- Did you actually complete all 3 "Try This!" exercises?
- Did you attempt the error prediction exercises?
- Did you read the war stories and reflect on the lessons?

**If you skipped exercises:** Your confidence ratings are probably inflated. Go back and do the hands-on work.

**Production wisdom:**

> "Confidence without competence is dangerous. Competence without confidence is wasted. Calibrate both." — Engineering Manager

</details>

**Action:** If any rating is below 3, review that section now before proceeding to verification.

---

## Verification (REQUIRED SECTION)

Let's verify your Prompting System.

**Create `verify_prompts.py`**:

```python
"""
Verification script for Chapter 9.
"""
from shared.utils.prompting import PromptTemplate
import sys

print("🧪 Running Prompt Engineering Verification...\n")

# Test 1: Basic Substitution
print("Test 1: Variable Substitution...")
try:
    pt = PromptTemplate("Hello {name}", ["name"])
    res = pt.format(name="World")
    assert res == "Hello World"
    print("✅ Substitution works")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# Test 2: Validation (Missing Variable)
print("Test 2: Validation Logic...")
try:
    pt.format()  # Missing 'name'
    print("❌ Failed: Should have raised error")
    sys.exit(1)
except ValueError as e:
    assert "Missing" in str(e)
    print("✅ Caught missing variable error")

# Test 3: Validation (Template Mismatch)
print("Test 3: Template Definition Validation...")
try:
    # 'age' is in input_variables but not in string
    PromptTemplate("Hello {name}", ["name", "age"])
    print("❌ Failed: Should have detected missing placeholder")
    sys.exit(1)
except ValueError as e:
    assert "expected but not found" in str(e)
    print("✅ Caught definition mismatch")

# Test 4: Multiple Variables
print("Test 4: Multiple Variable Substitution...")
try:
    pt = PromptTemplate(
        "Hello {name}, you are {age} years old",
        ["name", "age"]
    )
    res = pt.format(name="Alice", age=30)
    assert "Alice" in res and "30" in res
    print("✅ Multiple variables work")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

# Test 5: JSON Escaping
print("Test 5: JSON Brace Escaping...")
try:
    pt = PromptTemplate(
        'Return JSON: {{"status": "{status}"}}',
        ["status"]
    )
    res = pt.format(status="ok")
    assert '{"status": "ok"}' in res
    print("✅ JSON escaping works")
except Exception as e:
    print(f"❌ Failed: {e}")
    sys.exit(1)

print("\n🎉 Chapter 9 Complete! You can now manage prompts like code.")
```

**Run it:** `python verify_prompts.py`

### Expected output:

```
🧪 Running Prompt Engineering Verification...

Test 1: Variable Substitution...
✅ Substitution works
Test 2: Validation Logic...
✅ Caught missing variable error
Test 3: Template Definition Validation...
✅ Caught definition mismatch
Test 4: Multiple Variable Substitution...
✅ Multiple variables work
Test 5: JSON Brace Escaping...
✅ JSON escaping works

🎉 Chapter 9 Complete! You can now manage prompts like code.
```

**If any test fails:** Review the corresponding section and fix your implementation before continuing.

---

## 🗺️ Concept Map: Prompt Engineering Ecosystem

```
                    PROMPT ENGINEERING
                           |
        ┌──────────────────┼──────────────────┐
        |                  |                  |
    STRUCTURE          TEMPLATES         FEW-SHOT
        |                  |                  |
   CIF Pattern      PromptTemplate      Examples
        |                  |                  |
  ┌─────┼─────┐      ┌────┼────┐       ┌────┼────┐
  |     |     |      |    |    |       |    |    |
Context Inst Format Vars Valid Reuse  Zero 3-5  Fine-tune
                                       Shot Exs  (expensive)

BACKWARD CONNECTIONS:
← Chapter 7: Message roles (system, user, assistant)
← Chapter 8: MultiProviderClient (test prompts across providers)

FORWARD CONNECTIONS:
→ Chapter 10: Streaming (real-time prompt responses)
→ Chapter 17: RAG (prompt templates for retrieval)
→ Chapter 26: Agents (advanced prompt engineering)

CROSS-CUTTING CONCERNS:
• Token economics (longer prompts = higher cost)
• Version control (prompts as code)
• Testing (validate prompts like functions)
• Production patterns (centralized registries)
```

**Key relationships:**

- **CIF + Templates** = Reusable, validated prompts
- **Templates + Few-Shot** = Production-ready prompt system
- **Few-Shot vs Fine-Tuning** = Cost/accuracy trade-off

**Mental model:** Prompts are specifications. Treat them with the same rigor as database schemas or API contracts.

---

## Summary

**What you learned:**

1. ✅ **Prompt anatomy** — CIF pattern (Context, Instructions, Format)
2. ✅ **Template systems** — Reusable prompts with variable substitution and validation
3. ✅ **Few-shot learning** — Teaching through 3-5 examples for consistent output
4. ✅ **Production patterns** — Centralized prompt management, version control
5. ✅ **Cost optimization** — Few-shot vs fine-tuning trade-offs
6. ✅ **Error prevention** — Template validation catches bugs before production
7. ✅ **Real-world lessons** — $80K prompt versioning disaster, $150K saved by few-shot

**Key Takeaway**: A prompt is not just a question. It is a precise specification. Treat it with the same care you treat your database schema.

**Skills unlocked**: 🎯

- Prompt Engineering (CIF pattern)
- String Interpolation & Templating
- Few-Shot Prompting
- Production Prompt Management

**Production wisdom you gained:**

- "Prompts are configuration, not code" — Centralize them
- "Examples trump instructions" — Make them consistent
- "Try few-shot before fine-tuning" — Save $150K/year
- "Specificity is a dial, not a switch" — Find your Goldilocks Zone

**Looking ahead**: Now we have a Client (Ch 8) and a Prompt System (Ch 9). In **Chapter 10**, we will learn how to make the AI respond **word-by-word** (Streaming) for that real-time "thinking" feel!

---

**Next**: [Chapter 10: Streaming Responses →](chapter-10-streaming-responses.md)
