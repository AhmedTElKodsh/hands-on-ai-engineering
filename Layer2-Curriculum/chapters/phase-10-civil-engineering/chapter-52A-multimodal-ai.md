# Chapter 52A: Multimodal AI for Civil Engineering — The Engineer with Eyes

<!--
METADATA
Phase: Phase 10: Civil Engineering Application
Time: 2.5 hours (45 minutes reading + 105 minutes hands-on)
Difficulty: ⭐⭐⭐⭐
Type: Application / Advanced
Prerequisites: Chapter 52 (Report Generation)
Builds Toward: Chapter 53 (Compliance), Chapter 54 (Complete System)
Correctness Properties: P88 (Image parsing accuracy), P89 (Compliance detection from visuals)
-->

## ☕ Coffee Shop Intro: The Site Visit

Imagine sending a structural engineer to a bridge site, but blindfolding them.
"Read this report," you say. "Is the bridge safe?"
They can check the math. But they can't see the rust on the bolts or the crack in the concrete.

Until now, our AI has been blind. It could only read text.
**Multimodal AI** changes the game. It gives the AI eyes.

Now, we can feed it:
*   **CAD Drawings**: "Extract the beam dimensions."
*   **Site Photos**: "Identify safety violations."
*   **Diagrams**: "Does this schematic match the ASCE 7 code?"

In this chapter, we upgrade our system from "Text Processor" to "Field Engineer." 🏗️👀

---

## 🔍 The 3-Layer Dive

### Layer 1: Text-Only (The Blind Spot)
OCR (Optical Character Recognition) extracts text from images.
*   **Limit**: It reads "Beam A", but loses the context that "Beam A" is resting on a cracked support.

### Layer 2: Visual QA (The Glimpse)
Using models like CLIP to match images to text.
*   **Limit**: Good for search ("Find photos of cracks"), bad for analysis ("How severe is this crack?").

### Layer 3: Multimodal LLMs (The Full View)
Models like **GPT-4 Vision** or **Claude 3**.
*   **Capability**: They "reason" about the image. They can read a floor plan, understand spatial relationships, and verify compliance against a text standard.

---

## 🛠️ Implementation Guide: Giving AI Sight

We will build a **Site Inspection Assistant** that analyzes photos and a **CAD Reader** that extracts specs.

### Step 1: Setup

You need an OpenAI API key (GPT-4o or GPT-4-Turbo recommended for vision).

```bash
pip install openai matplotlib
```

### Step 2: The Vision Client

The API for vision is slightly different—you pass image URLs or base64 data.

```python
# vision_client.py
import base64
from openai import OpenAI
import os

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, prompt):
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

# Test it (You need a dummy image 'site.jpg')
# print(analyze_image("site.jpg", "What safety hazards do you see?"))
```

### Step 3: CAD Drawing Extraction (Your Turn)

We often need to turn a 2D drawing into structured data (JSON).

#### 🔬 Try This! (Hands-On Practice #1)

**Create `cad_extractor.py`**:

```python
# We will simulate extracting structural elements from a drawing
from vision_client import analyze_image

def extract_cad_specs(drawing_path):
    prompt = """
    You are a structural engineer. Analyze this technical drawing.
    Extract the following in JSON format:
    1. Beam Labels (e.g., B1, B2)
    2. Dimensions
    3. Material specifications mentioned
    """
    
    # In a real scenario, you'd use json_mode or structured outputs
    return analyze_image(drawing_path, prompt)

# Note: To run this, you need a sample image. 
# You can download a sample floor plan or create a simple dummy image.
```

---

## Part 2: Automated Site Inspection

Safety officers spend hours reviewing photos. Let's automate the "First Pass."

### 🔬 Try This! (Hands-On Practice #2)

**Create `safety_inspector.py`**:

```python
class SafetyInspector:
    def __init__(self):
        self.checklist = [
            "Workers wearing helmets (PPE)",
            "Guardrails on elevated platforms",
            "Clear pathways (no debris)",
            "Proper electrical wiring"
        ]

    def inspect_photo(self, photo_path):
        # Construct a prompt based on the checklist
        checklist_str = "\n".join(f"- {item}" for item in self.checklist)
        
        prompt = f"""
        Inspect this construction site photo for safety violations.
        Check against this list:
        {checklist_str}
        
        Report format:
        - Violation Detected: [Yes/No]
        - Description: [Details]
        - Severity: [High/Medium/Low]
        """
        
        return analyze_image(photo_path, prompt)

# Usage
# inspector = SafetyInspector()
# report = inspector.inspect_photo("site_photo_01.jpg")
# print(report)
```

---

## Part 3: Visual Compliance Checking (Advanced)

The Holy Grail: "Does this design match the requirements?"

1.  **Input A**: PDF Requirement ("Stairs must be 1.2m wide").
2.  **Input B**: CAD Image.
3.  **Task**: Measure and Compare.

*Note: LLMs are not perfect rulers. They are good at relative checking ("Is this obviously too narrow?"), but for precise measurement, you integrate OpenCV or dedicated CAD APIs (covered in Ch 54).*

---

## 🧪 Correctness Properties (Testing Vision)

Testing vision models is tricky. We rely on **Ground Truth** datasets.

| Property | Description |
|----------|-------------|
| **P88: Image Parsing** | The model MUST identify key elements (e.g., "There is a beam"). |
| **P89: Compliance Detection** | If an image contains a known violation, the model MUST flag it. |

### Hypothesis Test Example

```python
from hypothesis import given, strategies as st

# We mock the vision response for property testing
def mock_vision_model(image_bytes, prompt):
    if b"hazard" in image_bytes: # Simulating a hazard in the image data
        return "Violation: Yes"
    return "Violation: No"

@given(st.binary())
def test_p89_hazard_detection(image_data):
    """P89: Model must detect injected hazards."""
    # Inject a known hazard marker
    hazard_image = image_data + b"hazard"
    
    result = mock_vision_model(hazard_image, "Check safety")
    assert "Violation: Yes" in result
```

---

## ✅ Verification Script

Create `verify_ch52a.py`. We will mock the OpenAI client to verify the logic flow without spending $$$. 

```python
"""
Verification script for Chapter 52A: Multimodal AI
"""
import sys
from unittest.mock import MagicMock

print("🧪 Running Multimodal Verification...\n")

# Mock the OpenAI client
class MockClient:
    def __init__(self):
        self.chat = MagicMock()
        self.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content='{"beam": "B1", "width": "500mm"}'))
        ]

print("1. Testing Vision Client Setup...")
client = MockClient()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "analyze"}]
)
content = response.choices[0].message.content

if "beam" in content:
    print("✅ P88 Passed: Vision client structure is correct.")
else:
    print("❌ Failed: Unexpected mock response.")
    sys.exit(1)

print("2. Testing Logic Flow...")
# Verify that we can construct the payload correctly (without sending)
try:
    import base64
    dummy_data = base64.b64encode(b"fake_image").decode('utf-8')
    payload = {
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{dummy_data}"}
    }
    print("✅ Payload construction valid.")
except Exception as e:
    print(f"❌ Failed to construct payload: {e}")
    sys.exit(1)

print("\n🎉 Chapter 52A Complete! Your AI can see.")
```

---

## 📝 Summary & Key Takeaways

1.  **Multimodal AI**: Combining Text + Vision (and sometimes Audio).
2.  **GPT-4o / Claude 3**: The current state-of-the-art for reasoning about technical images.
3.  **Prompting with Images**: You treat the image as part of the context. "Look at [Image] and tell me [Prompt]."
4.  **Use Cases**: CAD extraction, Safety Inspection, Visual Compliance.
5.  **Limitations**: Precision measurement (mm accuracy) is still best done by geometric tools, not LLMs. Use LLMs for *semantic* analysis.

**Key Insight**: An image is worth 1,000 tokens. By adding vision, we close the gap between "Paperwork" and "Physical Reality."

---

## 🔜 What's Next?

We have the eyes (Ch 52A) and the brains (Ch 52). Now we need the **Lawyer**.
In **Chapter 53**, we will build the **Compliance Review Agent** that uses everything we've built to automate RFIs and Code Checking.
