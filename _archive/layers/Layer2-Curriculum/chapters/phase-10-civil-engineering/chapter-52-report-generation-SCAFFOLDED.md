# Chapter 52: Technical Report Generation System — The Calculator

<!--
METADATA
Phase: 10 - Civil Engineering Application
Time: 1.5 hours (30 min reading + 60 min hands-on)
Difficulty: ⭐⭐⭐
Type: Application
Prerequisites: Chapter 49 (Models), Chapter 29 (Tools)
Builds Toward: Complete System (Ch 54)
Correctness Properties: P74 (Calculation Accuracy), P75 (Visualization Correctness)
Project Thread: Analysis

NAVIGATION
→ Quick Reference: #quick-reference-card
→ Verification: #verification-required-section
→ What's Next: #whats-next
-->

---

## ☕ Coffee Shop Intro

**Imagine this**: You ask a calculator, "What is 55 \* 142?" It gives you the exact answer.
You ask a poet the same question. They might say, "A lot. Like, thousands. Maybe a million?"

LLMs are poets. They are terrible at math.
If you ask an AI to "Calculate the structural load," it will confidently hallucinate a number that causes your bridge to collapse.

**Technical Reports** require precision.
To build them, we need to force the Poet to use a Calculator.
We will give our AI tools to run Python code, generate real charts, and crunch real data.

**By the end of this chapter**, you will generate a report with charts and tables that are mathematically perfect. 📊

---

## Prerequisites Check

We need data science tools.

```bash
pip install pandas matplotlib
```

Ensure you have `domain_models.py` from Chapter 49.

---

## The Story: The "Hallucinated" Graph

### The Problem (Fake Data)

You ask GPT-4: "Draw a graph of the stress test."
It outputs text: `[Chart showing curve going up]`.
Or it generates SVG code that looks like a squiggly line but matches no real data.
It looks scientific, but it's fiction.

### The Solution (Code Interpreter)

We don't ask the AI to _draw_. We ask it to _write Python code that draws_.

1.  **Reason**: "I need a graph of Load vs Deflection."
2.  **Act**: Write `matplotlib` code.
3.  **Execute**: Run code -> Save `graph.png`.
4.  **Report**: Embed `![Graph](graph.png)` in the document.

---

## Part 1: The Calculation Tool

Never let an LLM do math in its head.

### 🔬 Try This! (Hands-On Practice #1)

**Create `calc_tools.py`**:

```python
from langchain_core.tools import tool
import math
```

@tool
def calculate_beam_load(length: float, load_per_meter: float) -> float:
"""
Calculates total load on a beam.

    This tool provides precise mathematical calculations that LLMs cannot
    reliably perform. It implements the formula: length * load_per_meter

    TODO: Implement this function
    HINT: Use the @tool decorator from langchain_core.tools (already applied)
    HINT: Print a calculation message: f"🧮 Calculating: {length}m * {load_per_meter}kg/m"
    HINT: Return the result of length * load_per_meter
    HINT: This is a simple multiplication, but the tool pattern makes it reliable

    Args:
        length: Length of the beam in meters
        load_per_meter: Load per meter in kg/m

    Returns:
        float: Total load on the beam in kg

    Example:
        >>> result = calculate_beam_load.invoke({"length": 10, "load_per_meter": 500})
        >>> print(result)
        5000.0
    """
    pass  # Your code here

@tool
def calculate_safety_factor(max_load: float, actual_load: float) -> float:
"""
Calculates safety factor for structural analysis.

    Safety factor is the ratio of maximum capacity to actual load.
    A factor > 1.0 indicates the structure is safe.

    TODO: Implement this function
    HINT: Check if actual_load == 0 to avoid division by zero
    HINT: If actual_load is 0, return 0.0 as a safe default
    HINT: Otherwise, return max_load / actual_load
    HINT: Formula: safety_factor = max_capacity / actual_load

    Args:
        max_load: Maximum load capacity in kg
        actual_load: Actual load applied in kg

    Returns:
        float: Safety factor (ratio). Values > 1.0 indicate safety margin.

    Example:
        >>> result = calculate_safety_factor.invoke({"max_load": 15000, "actual_load": 10000})
        >>> print(result)
        1.5
    """
    pass  # Your code here

# Test execution

if **name** == "**main**":
print("Testing calculation tools...")
print(calculate_beam_load.invoke({"length": 10, "load_per_meter": 500}))
print(calculate_safety_factor.invoke({"max_load": 15000, "actual_load": 10000}))

````

<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
from langchain_core.tools import tool
import math

@tool
def calculate_beam_load(length: float, load_per_meter: float) -> float:
    """
    Calculates total load on a beam.
    Formula: length * load_per_meter
    """
    print(f"🧮 Calculating: {length}m * {load_per_meter}kg/m")
    return length * load_per_meter

@tool
def calculate_safety_factor(max_load: float, actual_load: float) -> float:
    """
    Calculates safety factor.
    Formula: max_load / actual_load
    """
    if actual_load == 0:
        return 0.0
    return max_load / actual_load

# Test
if __name__ == "__main__":
    print("Testing calculation tools...")
    print(calculate_beam_load.invoke({"length": 10, "load_per_meter": 500}))
    print(calculate_safety_factor.invoke({"max_load": 15000, "actual_load": 10000}))
````

**Why this implementation works**:

1. **@tool Decorator**: LangChain's `@tool` decorator automatically converts Python functions into tools that agents can call. The decorator handles argument parsing and result formatting.

2. **Precise Calculations**: By implementing calculations as tools, we guarantee mathematical accuracy. LLMs are probabilistic and can hallucinate numbers, but Python's arithmetic is deterministic.

3. **Error Handling**: The safety factor function checks for division by zero, preventing runtime errors when actual_load is 0.

4. **Tool Invocation Pattern**: Tools are called using `.invoke({"param": value})` syntax, which LangChain agents use automatically during execution.

**Key Pattern**: Tool-Based Computation - Never let LLMs do math in their "head". Always delegate to deterministic code.

**Real-World Application**: In engineering, financial, or scientific applications, calculation errors can have serious consequences. Tools ensure 100% accuracy.

</details>

**Run it**.
We now have trusted functions that provide mathematical precision.

---

## Part 2: The Visualization Tool

Now, let's generate a chart using matplotlib.

### 🔬 Try This! (Hands-On Practice #2)

**Create `chart_tools.py`**:

```python
from langchain_core.tools import tool
import matplotlib.pyplot as plt
import os
from typing import List

@tool
def generate_load_chart(loads: List[float], spans: List[float]) -> str:
    """
    Generates a Load vs Span chart and saves it to 'load_chart.png'.

    This tool creates real data visualizations that LLMs cannot generate
    reliably. It uses matplotlib to create publication-quality charts.

    TODO: Implement this function
    HINT: Print a status message: "📊 Generating Chart..."
    HINT: Create a figure with plt.figure(figsize=(10, 6))
    HINT: Plot data with plt.plot(spans, loads, marker='o', linestyle='-')
    HINT: Add title: plt.title('Beam Load Distribution')
    HINT: Add labels: plt.xlabel('Span (m)'), plt.ylabel('Load (kg)')
    HINT: Add grid: plt.grid(True)
    HINT: Save with plt.savefig("load_chart.png")
    HINT: Close figure with plt.close() to free memory
    HINT: Return the filename string: "load_chart.png"

    Args:
        loads: List of load values in kg
        spans: List of span positions in meters

    Returns:
        str: Filename of the generated chart

    Raises:
        ValueError: If loads and spans have different lengths

    Example:
        >>> filename = generate_load_chart.invoke({
        ...     "loads": [100, 200, 150],
        ...     "spans": [0, 5, 10]
        ... })
        >>> print(filename)
        'load_chart.png'
    """
    pass  # Your code here


# Test execution
if __name__ == "__main__":
    print("Testing chart generation...")
    result = generate_load_chart.invoke({
        "loads": [100, 200, 150],
        "spans": [0, 5, 10]
    })
    print(f"Chart saved to: {result}")
```

<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
from langchain_core.tools import tool
import matplotlib.pyplot as plt
import os
from typing import List

@tool
def generate_load_chart(loads: List[float], spans: List[float]) -> str:
    """
    Generates a Load vs Span chart and saves it to 'load_chart.png'.
    Returns the filename.
    """
    print("📊 Generating Chart...")
    plt.figure(figsize=(10, 6))
    plt.plot(spans, loads, marker='o', linestyle='-')
    plt.title('Beam Load Distribution')
    plt.xlabel('Span (m)')
    plt.ylabel('Load (kg)')
    plt.grid(True)

    filename = "load_chart.png"
    plt.savefig(filename)
    plt.close()

    return filename

# Test
if __name__ == "__main__":
    print("Testing chart generation...")
    result = generate_load_chart.invoke({
        "loads": [100, 200, 150],
        "spans": [0, 5, 10]
    })
    print(f"Chart saved to: {result}")
```

**Why this implementation works**:

1. **Matplotlib Integration**: We use matplotlib's pyplot API to create professional charts. The `figsize=(10, 6)` creates a readable 10x6 inch figure.

2. **Data Visualization**: The `plot()` function with `marker='o'` and `linestyle='-'` creates a line chart with visible data points, making trends clear.

3. **File Persistence**: `plt.savefig()` writes the chart to disk as a PNG file. This file can be embedded in reports, emails, or presentations.

4. **Memory Management**: `plt.close()` releases the figure from memory, preventing memory leaks when generating multiple charts.

5. **Return Value**: Returning the filename allows the agent to reference the chart in its report text.

**Key Pattern**: File-Based Artifacts - Generate real files (images, PDFs, CSVs) that can be verified, shared, and archived.

**Performance Note**: For production systems, use unique filenames (e.g., `chart_{uuid}.png`) to avoid overwriting charts when generating multiple reports concurrently.

</details>

**Run it**.
Check your folder. Do you see `load_chart.png`? Open it. That's a real graph with actual data!

---

## Part 3: The Report Generator Agent

Now we put the Poet in charge of the Calculator and the Artist.

### 🔬 Try This! (Hands-On Practice #3)

**Create `report_gen.py`**:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from calc_tools import calculate_beam_load, calculate_safety_factor
from chart_tools import generate_load_chart
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def create_report_agent() -> AgentExecutor:
    """
    Creates an agent that can generate technical reports using calculation
    and visualization tools.

    This agent orchestrates multiple tools to produce accurate, data-driven
    reports with embedded visualizations.

    TODO: Implement this function
    HINT 1: Create tools list: [calculate_beam_load, calculate_safety_factor, generate_load_chart]
    HINT 2: Initialize model: ChatOpenAI(model="gpt-4o-mini", temperature=0)
    HINT 3: Temperature=0 ensures deterministic, factual responses
    HINT 4: Create prompt with ChatPromptTemplate.from_messages([...])
    HINT 4a: Message structure: [("system", "system_text"), ("human", "{input}"), ("placeholder", "{agent_scratchpad}")]
    HINT 4b: System message: "You are a Structural Engineer. Create a technical report."
    HINT 4c: Human message uses {input} placeholder for user's task
    HINT 4d: Placeholder {agent_scratchpad} stores tool execution history (required for agents)
    HINT 5: Create agent: create_tool_calling_agent(model, tools, prompt)
    HINT 6: Create executor: AgentExecutor(agent=agent, tools=tools, verbose=True)
    HINT 7: Return the executor

    Returns:
        AgentExecutor: Configured agent that can generate reports

    Example:
        >>> executor = create_report_agent()
        >>> result = executor.invoke({"input": "Calculate load for 10m beam at 500kg/m"})
        >>> print(result["output"])
    """
    pass  # Your code here


def generate_structural_report(executor: AgentExecutor, task: str) -> Dict[str, Any]:
    """
    Generates a structural analysis report using the agent.

    The agent will automatically call calculation and visualization tools
    as needed to complete the task.

    TODO: Implement this function
    HINT: Print a header: "--- Generating Report ---"
    HINT: Call executor.invoke({"input": task})
    HINT: Store the result (it's a dictionary with "output" key)
    HINT: Print another header: "\n--- FINAL REPORT ---\n"
    HINT: Print result["output"] to show the generated report
    HINT: Return the full result dictionary

    Args:
        executor: The agent executor
        task: Task description for the report

    Returns:
        Dict containing "input" and "output" keys

    Example:
        >>> executor = create_report_agent()
        >>> result = generate_structural_report(executor, "Analyze 20m beam...")
        >>> print(result["output"])
    """
    pass  # Your code here


# Main execution
if __name__ == "__main__":
    # Create the agent
    executor = create_report_agent()

    # Define the analysis task
    task = """
We have a 20m beam. The load is 500kg/m.
The max capacity is 15,000kg.

1. Calculate the total load.
2. Calculate the safety factor.
3. Generate a chart assuming load increases linearly from 0 to Total over the 20m span.
4. Write a brief report summarizing the findings. Include the chart.
"""

    # Generate the report
    result = generate_structural_report(executor, task)
```

<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from calc_tools import calculate_beam_load, calculate_safety_factor
from chart_tools import generate_load_chart
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def create_report_agent() -> AgentExecutor:
    """Creates an agent that can generate technical reports."""
    # 1. Setup tools
    tools = [calculate_beam_load, calculate_safety_factor, generate_load_chart]
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 2. Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Structural Engineer. Create a technical report."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 3. Create agent and executor
    agent = create_tool_calling_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return executor


def generate_structural_report(executor: AgentExecutor, task: str) -> Dict[str, Any]:
    """Generates a structural analysis report using the agent."""
    print("--- Generating Report ---")
    result = executor.invoke({"input": task})
    print("\n--- FINAL REPORT ---\n")
    print(result["output"])
    return result


# Main execution
if __name__ == "__main__":
    executor = create_report_agent()

    task = """
We have a 20m beam. The load is 500kg/m.
The max capacity is 15,000kg.

1. Calculate the total load.
2. Calculate the safety factor.
3. Generate a chart assuming load increases linearly from 0 to Total over the 20m span.
4. Write a brief report summarizing the findings. Include the chart.
"""

    result = generate_structural_report(executor, task)
```

**Why this implementation works**:

1. **Tool Calling Agent**: `create_tool_calling_agent()` creates an agent that can automatically decide which tools to call based on the task. It uses the LLM's function calling capability.

2. **Temperature=0**: Setting temperature to 0 makes the LLM deterministic and factual, which is critical for technical reports. Higher temperatures add creativity but reduce reliability.

3. **Agent Scratchpad**: The `{agent_scratchpad}` placeholder stores the history of tool calls and results, allowing the agent to reason about previous actions.

4. **Verbose Mode**: `verbose=True` prints the agent's reasoning process, showing which tools it calls and why. This is invaluable for debugging and understanding agent behavior.

5. **Multi-Step Orchestration**: The agent breaks down the complex task into steps:
   - Call `calculate_beam_load` for total load
   - Call `calculate_safety_factor` for safety analysis
   - Call `generate_load_chart` for visualization
   - Synthesize results into a coherent report

**Key Pattern**: Agent Orchestration - The LLM acts as a coordinator, delegating precise tasks to specialized tools while maintaining narrative coherence.

**Execution Flow**:

1. Agent reads the task
2. Agent decides to call `calculate_beam_load(20, 500)`
3. Tool returns `10000.0`
4. Agent decides to call `calculate_safety_factor(15000, 10000)`
5. Tool returns `1.5`
6. Agent decides to call `generate_load_chart([0, 5000, 10000], [0, 10, 20])`
7. Tool returns `"load_chart.png"`
8. Agent synthesizes all results into a report mentioning the numbers and referencing the chart

This report is **grounded in math** and **backed by real visualizations**.

</details>

**Run it**.
Watch the trace in verbose mode. You'll see:

1. It calculates `20 * 500 = 10,000` (precise)
2. It calculates `15,000 / 10,000 = 1.5` (precise)
3. It calls the chart tool (real file created)
4. It writes text referencing the numbers and the image (coherent narrative)

---

## Part 4: Integration with Pydantic

We can parse the final text into our `TechnicalReport` model for structured storage.

### 🔬 Try This! (Hands-On Practice #4)

**Create `structured_report.py`**:

```python
from domain_models import TechnicalReport, Calculation
from langchain_core.output_parsers import PydanticOutputParser
from typing import List

def create_structured_report(
    report_id: str,
    title: str,
    calculations: List[Calculation],
    conclusion: str,
    approved_by: str
) -> TechnicalReport:
    """
    Creates a structured technical report using Pydantic models.

    This function demonstrates how to convert agent-generated data
    into validated, type-safe data structures.

    TODO: Implement this function
    HINT: Create a TechnicalReport instance with all parameters
    HINT: Pass report_id, title, calculations, conclusion, approved_by as keyword arguments
    HINT: Pydantic will automatically validate all fields
    HINT: Return the TechnicalReport instance

    Args:
        report_id: Unique identifier for the report
        title: Report title
        calculations: List of Calculation objects
        conclusion: Summary conclusion
        approved_by: Name of approver

    Returns:
        TechnicalReport: Validated report object

    Example:
        >>> calcs = [
        ...     Calculation(name="Total Load", formula="20*500", result=10000, units="kg")
        ... ]
        >>> report = create_structured_report(
        ...     "RPT-001", "Structural Analysis", calcs, "Safe", "Engineer"
        ... )
        >>> print(report.report_id)
        'RPT-001'
    """
    pass  # Your code here


# Example usage
if __name__ == "__main__":
    # Mock data from agent execution
    calculations = [
        Calculation(
            name="Total Load",
            formula="20 * 500",
            result=10000,
            units="kg"
        ),
        Calculation(
            name="Safety Factor",
            formula="15000 / 10000",
            result=1.5,
            units="ratio"
        )
    ]

    report = create_structured_report(
        report_id="RPT-001",
        title="Structural Analysis",
        calculations=calculations,
        conclusion="The beam is safe with a safety factor of 1.5.",
        approved_by="AI Engineer"
    )

    print(f"Report ID: {report.report_id}")
    print(f"Title: {report.title}")
    print(f"Calculations: {len(report.calculations)}")
    print(f"Conclusion: {report.conclusion}")
```

<details>
<summary>💡 Click to reveal complete implementation (try on your own first!)</summary>

```python
from domain_models import TechnicalReport, Calculation
from langchain_core.output_parsers import PydanticOutputParser
from typing import List

def create_structured_report(
    report_id: str,
    title: str,
    calculations: List[Calculation],
    conclusion: str,
    approved_by: str
) -> TechnicalReport:
    """Creates a structured technical report using Pydantic models."""
    report = TechnicalReport(
        report_id=report_id,
        title=title,
        calculations=calculations,
        conclusion=conclusion,
        approved_by=approved_by
    )
    return report


# Example usage
if __name__ == "__main__":
    calculations = [
        Calculation(
            name="Total Load",
            formula="20 * 500",
            result=10000,
            units="kg"
        ),
        Calculation(
            name="Safety Factor",
            formula="15000 / 10000",
            result=1.5,
            units="ratio"
        )
    ]

    report = create_structured_report(
        report_id="RPT-001",
        title="Structural Analysis",
        calculations=calculations,
        conclusion="The beam is safe with a safety factor of 1.5.",
        approved_by="AI Engineer"
    )

    print(f"Report ID: {report.report_id}")
    print(f"Title: {report.title}")
    print(f"Calculations: {len(report.calculations)}")
    print(f"Conclusion: {report.conclusion}")
```

**Why this implementation works**:

1. **Pydantic Validation**: The `TechnicalReport` model automatically validates all fields. If you pass invalid data (e.g., wrong type), Pydantic raises a clear error.

2. **Type Safety**: By using Pydantic models, we get IDE autocomplete, type checking, and runtime validation. This prevents bugs from invalid data.

3. **Structured Storage**: The report can be easily serialized to JSON, stored in databases, or transmitted over APIs using `report.model_dump()` or `report.model_dump_json()`.

4. **Domain Models**: The `Calculation` and `TechnicalReport` models from Chapter 49 provide a consistent schema across the entire application.

**Key Pattern**: Structured Output - Convert unstructured agent text into validated data structures for reliable storage and processing.

**Integration Strategy**: In a production system, you would:

1. Run the agent to generate the report text
2. Use an extraction chain (Chapter 11) to parse the text into structured data
3. Validate with Pydantic models
4. Store in database
5. Generate PDF/DOCX from the structured data

</details>

---

## Common Mistakes

### Mistake #1: Using `eval()`

**The Mistake**: Letting the LLM write arbitrary Python code and running it with `eval()`.
**Why it fails**: Security risk! The LLM could generate code that deletes files, accesses sensitive data, or crashes your system.
**The Fix**: Define specific tools (`calculate_load`) or use a sandboxed environment (Docker, E2B) if using generic code execution.

### Mistake #2: Hallucinated Units

**The Mistake**: LLM calculates "100". Is it kg? lbs? meters?
**Why it fails**: Ambiguous units lead to catastrophic errors (Mars Climate Orbiter crashed due to unit confusion).
**The Fix**: Tools should return strings with units ("100 kg") or Pydantic models with explicit unit fields.

### Mistake #3: Overwriting Charts

**The Mistake**: Running the report twice overwrites `load_chart.png`.
**Why it fails**: Concurrent report generation or historical analysis becomes impossible.
**The Fix**: Generate unique filenames using UUIDs: `chart_{uuid.uuid4()}.png`.

---

## Quick Reference Card

### Plotting with Matplotlib

```python
import matplotlib.pyplot as plt

# Create figure
plt.figure(figsize=(10, 6))

# Plot data
plt.plot(x_values, y_values, marker='o', linestyle='-')

# Add labels and title
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Chart Title')
plt.grid(True)

# Save and close
plt.savefig("chart.png")
plt.close()
```

### Markdown Images

To embed an image in a markdown report:

```markdown
![Chart Description](filename.png)
```

### Tool Pattern

```python
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description for the LLM."""
    # Implementation
    return result
```

---

## Verification (REQUIRED SECTION)

We need to verify **P74 (Calculation Accuracy)** and **P75 (Visualization Correctness)**.

**The verification script is provided complete** (you don't need to implement this - it's for testing your tools):

**Create `verify_report.py`**:

```python
"""
Verification script for Chapter 52.
Properties: P74 (Calculation Accuracy), P75 (Visualization Correctness).

P74 ensures that mathematical calculations are precise and deterministic.
P75 ensures that visualization files are created and contain valid data.
"""
from calc_tools import calculate_beam_load, calculate_safety_factor
from chart_tools import generate_load_chart
import os
import sys

print("🧪 Running Report Verification...\n")

# P74: Calculation Accuracy
print("Test 1: Mathematical Precision...")
res = calculate_beam_load.invoke({"length": 10, "load_per_meter": 5})
if res == 50.0:
    print("✅ P74 Passed: 10 * 5 = 50 (exact).")
else:
    print(f"❌ Failed: Math error. Expected 50.0, got {res}")
    sys.exit(1)

# Test safety factor calculation
sf_res = calculate_safety_factor.invoke({"max_load": 100, "actual_load": 50})
if sf_res == 2.0:
    print("✅ P74 Passed: 100 / 50 = 2.0 (exact).")
else:
    print(f"❌ Failed: Safety factor error. Expected 2.0, got {sf_res}")
    sys.exit(1)

# P75: Visualization Correctness
print("\nTest 2: Chart Generation...")
chart_file = "load_chart.png"

# Cleanup old chart
if os.path.exists(chart_file):
    os.remove(chart_file)

# Generate new chart
generate_load_chart.invoke({"loads": [1, 2, 3], "spans": [1, 2, 3]})

# Verify file exists and has content
if os.path.exists(chart_file):
    size = os.path.getsize(chart_file)
    if size > 0:
        print(f"✅ P75 Passed: Chart created ({size} bytes).")
    else:
        print("❌ Failed: Chart file is empty.")
        sys.exit(1)
else:
    print("❌ Failed: Chart file not created.")
    sys.exit(1)

print("\n🎉 Chapter 52 Complete! You are a Data Scientist with AI superpowers.")
```

**Run it:** `python verify_report.py`

---

## Summary

**What you learned:**

1. ✅ **Tools over Thoughts**: Using Python for math is 100% accurate; using LLM "thoughts" is risky.
2. ✅ **Visuals**: Generating real image files from data using matplotlib.
3. ✅ **Integration**: Combining text generation with data processing.
4. ✅ **Structured Output**: Fitting analysis into the `TechnicalReport` schema.
5. ✅ **Sandboxing**: Why specific tools are safer than generic `exec()`.

**Key Takeaway**: The LLM is not the calculator. The LLM is the _operator_ of the calculator. It orchestrates tools but delegates precision tasks to deterministic code.

**Skills unlocked**: 🎯

- Data Visualization with matplotlib
- Computational Tools with LangChain
- Report Automation with Agents
- Multi-Tool Orchestration

**Looking ahead**: We have contracts, proposals, and reports.
But are they legal? Are they compliant?
In **Chapter 53**, we will build the **Compliance Review Agent** to check our work against regulations.

---

**Next**: [Chapter 53: Compliance Review Agent →](chapter-53-compliance-review.md)
