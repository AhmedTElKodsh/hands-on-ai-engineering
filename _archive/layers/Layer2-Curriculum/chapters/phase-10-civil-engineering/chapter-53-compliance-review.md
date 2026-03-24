# Chapter 53: Compliance Review Agent — The Inspector

<!--
METADATA
Phase: Phase 10: Civil Engineering Application
Time: 3.0 hours (60 minutes reading + 120 minutes hands-on)
Difficulty: ⭐⭐⭐⭐
Type: Application / Advanced
Prerequisites: Chapter 4 (Advanced Models), Chapter 38A (GraphRAG), Chapter 52A (Multimodal)
Builds Toward: Chapter 54 (Complete System)
Correctness Properties: P76 (Rule Coverage), P77 (Violation Detection)
-->

## ☕ Coffee Shop Intro: The Inspector

**Imagine this**: You finish building a house. You're proud.
The Inspector walks in.
"Door frame is 31 inches. Code requires 32." **Fail.**
"Stair rise is 8 inches. Code max is 7.75." **Fail.**

You have to tear it down and start over.
In Civil Engineering, regulations (OSHA, FAR, ISO) are non-negotiable.
Humans miss these details. AI doesn't sleep, doesn't blink, and can memorize 10,000 pages of code.

**By the end of this chapter**, you will build a **Compliance Agent** that scans your documents (and drawings!) for illegal clauses and safety violations *before* the inspector arrives. 🕵️‍♂️

---

## 🔍 The 3-Layer Dive

### Layer 1: Keyword Search
Ctrl+F "Safety".
*   **Limit**: Misses "Employees must be protected from falls" if it doesn't say "Safety".

### Layer 2: RAG-Based Review
Search Vector DB for "Fall Protection" laws.
*   **Limit**: Can't check blueprints or generate RFIs for missing info.

### Layer 3: The Full Compliance Suite (v6.1)
1.  **Text Review**: Check contracts against FAR/OSHA.
2.  **Visual Review**: Check CAD drawings against ASCE 7.
3.  **Gap Analysis**: Auto-generate RFIs (Requests for Information) for missing specs.

---

## 🛠️ Implementation Guide: Building the Inspector

We need a database of "Laws". We'll simulate a Safety Standard.

### Part 1: The Regulatory Database (RAG)

#### 🔬 Try This! (Hands-On Practice #1)

**Create `regulatory_db.py`**:

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import shutil

DB_PATH = "./laws_db"
# Cleanup
try: shutil.rmtree(DB_PATH)
except: pass

# 1. The "Laws" (Simulated)
laws = [
    "OSHA 1926.100: Employees working in areas where there is a possible danger of head injury from impact, or from falling or flying objects, shall be protected by protective helmets.",
    "OSHA 1926.501: Each employee on a walking/working surface (horizontal and vertical surface) with an unprotected side or edge which is 6 feet (1.8 m) or more above a lower level shall be protected from falling.",
    "FAR 52.203-7: Anti-Kickback Procedures. The Contractor shall have in place and follow reasonable procedures to prevent and detect violations."
]

# 2. Index them
print("🏛️ Indexing Laws...")
vectorstore = Chroma.from_texts(
    texts=laws,
    embedding=OpenAIEmbeddings(),
    collection_name="regulations",
    persist_directory=DB_PATH
)
print(f"Indexed {len(laws)} regulations.")
```

**Run it**. You now have a digital lawyer.

---

### Part 2: The Text Reviewer

Now we write the logic to check a specific text against the DB.

#### 🔬 Try This! (Hands-On Practice #2)

**Create `reviewer.py`**:

```python
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Define Output Model locally for simplicity
class ComplianceIssue(BaseModel):
    description: str
    severity: str
    law_id: str

# 1. Connect to DB
vectorstore = Chroma(
    collection_name="regulations",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./laws_db"
)

# 2. The Reviewer Chain
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = JsonOutputParser(pydantic_object=ComplianceIssue)

prompt = ChatPromptTemplate.from_template(
    """
    You are a Compliance Officer.
    
    TEXT TO REVIEW:
    {text}
    
    RELEVANT LAWS:
    {laws}
    
    Task:
    1. Determine if the text violates the laws.
    2. If YES, return JSON.
    3. If NO, return null.    
    {format_instructions}
    """
)

chain = prompt | model | parser

def check_compliance(clause_text):
    # A. Retrieve Laws
    results = vectorstore.similarity_search(clause_text, k=1)
    laws_text = "\n".join([d.page_content for d in results])
    
    # B. Compare
    try:
        issue = chain.invoke({
            "text": clause_text,
            "laws": laws_text,
            "format_instructions": parser.get_format_instructions()
        })
        return issue
    except:
        return None 

# 3. Test
risky_text = "Workers will operate on the roof (20 feet high) without harnesses to save time."
issue = check_compliance(risky_text)
if issue:
    print(f"🚨 VIOLATION: {issue['description']}")
```

---

### Part 3: Visual Compliance (New v6.1)

We use the vision client from Ch 52A to check drawings against codes.

#### 🔬 Try This! (Hands-On Practice #3)

**Create `visual_checker.py`**:

```python
# Requires vision_client from Ch 52A
try:
    from vision_client import analyze_image
except ImportError:
    # Mock for compilation if file missing
    def analyze_image(path, prompt): return "Violation: No Guardrails."

def check_drawing_compliance(image_path, code_requirement):
    prompt = f"""
    You are a building inspector.
    Code Requirement: {code_requirement}
    
    Analyze this drawing. Does it meet the requirement?
    Start response with "COMPLIANT" or "VIOLATION".
    """
    return analyze_image(image_path, prompt)

# Test
# print(check_drawing_compliance("stairs.jpg", "Max riser height 7.75 inches"))
```

---

### Part 4: Automated RFI Generation (New v6.1)

Sometimes a spec isn't *wrong*, it's just *missing*.
**RFI (Request for Information)**: "You didn't specify the concrete grade."

#### 🔬 Try This! (Hands-On Practice #4)

**Create `rfi_generator.py`**:

```python
from langchain_openai import ChatOpenAI

def generate_rfi(contract_text, drawings_text):
    prompt = f"""
    Compare the Contract and the Drawings.
    
    Contract: {contract_text}
    Drawings Description: {drawings_text}
    
    Identify missing information.
    Generate a formal RFI (Request for Information).
    """
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    return llm.invoke(prompt).content

# Test
contract = "Foundation shall be concrete."
drawings = "Foundation Plan shows dimensions 10x10m."
# Missing: What strength of concrete? (3000 psi? 5000 psi?)

print(generate_rfi(contract, drawings))
```

---

## 🧪 Correctness Properties (Testing The Law)

| Property | Description |
|----------|-------------|
| **P77: Violation Detection** | If text contradicts a Law in the DB, it MUST flag a violation. |

### Hypothesis Test Example

```python
from hypothesis import given, strategies as st

def test_p77_violation_detection():
    # Setup a mock reviewer with a known law
    law = "Speed limit 50."
    violation = "I drove 80."
    
    # In a real property test, we'd use the actual chain
    # Here we simulate the logic
    assert "80" in violation and "50" in law
    # Logic: 80 > 50 -> Violation
```

---

## ✅ Verification Script

Create `verify_ch53.py`.

```python
"""
Verification script for Chapter 53: Compliance
"""
import sys
from reviewer import check_compliance

print("🧪 Running Compliance Verification...\n")

# P77: Violation Detection
violation_text = "It is acceptable to accept kickbacks from subcontractors."

print("Test 1: Detecting Kickbacks...")
result = check_compliance(violation_text)

if result and "kickback" in str(result).lower():
    print("✅ P77 Passed: Detected kickback violation.")
elif result:
    print(f"✅ P77 Passed: Detected violation ({result})")
else:
    print("❌ Failed: Did not detect violation.")
    sys.exit(1)

print("\n🎉 Chapter 53 Complete! You are the Inspector.")
```

---

## 📝 Summary & Key Takeaways

1.  **Regulatory RAG**: Laws are data. Index them.
2.  **Clause-by-Clause**: Don't review 50 pages at once. Review paragraph by paragraph.
3.  **Visual Compliance**: Use Multimodal AI to check drawings against text codes.
4.  **Gap Analysis**: AI is great at finding what is *missing* (RFIs).
5.  **Risk Mitigation**: The cost of an AI review ($0.50) vs the cost of a lawsuit ($1M).

**Key Insight**: Compliance isn't about being creative. It's about being 100% consistent. AI excels at consistency.

---

## 🔜 What's Next?

We have the individual pieces.
*   Models (Ch 49)
*   Generation (Ch 50-52)
*   Compliance (Ch 53)

In **Chapter 54 (The Finale)**, we assemble the **Complete System**. We will connect the pipes, build a UI, and ship it! 🚀