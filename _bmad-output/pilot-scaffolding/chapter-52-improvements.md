# Chapter 52 Improvements: Error Handling, Testing, & Debugging

**Date**: 2026-01-23
**Task**: Improve Chapter 52 with error handling hints, test execution guidance, and debugging notes
**Status**: ✅ COMPLETE

---

## Part 1: Error Handling Hints for Complex Functions

### Improvement 1: Add Error Handling to `calculate_beam_load()`

**Location**: After existing hints in calc_tools.py

**Add these additional hints**:

```python
@tool
def calculate_beam_load(length: float, load_per_meter: float) -> float:
    """
    Calculates total load on a beam.

    TODO: Implement this function
    HINT: Use the @tool decorator from langchain_core.tools (already applied)
    HINT: Print a calculation message: f"🧮 Calculating: {length}m * {load_per_meter}kg/m"
    HINT: Return the result of length * load_per_meter
    HINT: This is a simple multiplication, but the tool pattern makes it reliable

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Validate inputs before calculation: check length > 0 and load_per_meter >= 0
    HINT (Error Handling): If invalid, raise ValueError(f"Invalid inputs: length={length}, load={load_per_meter}")
    HINT (Error Handling): The @tool decorator will catch and format this error for the agent
    HINT (Error Handling): Add type checking: isinstance(length, (int, float)) to prevent string inputs

    Args:
        length: Length of the beam in meters (must be > 0)
        load_per_meter: Load per meter in kg/m (must be >= 0)

    Returns:
        float: Total load in kg

    Raises:
        ValueError: If length <= 0 or load_per_meter < 0
    """
    pass  # Your code here
```

**Rationale**: Tools are called by LLMs - they may pass invalid arguments. Validation prevents garbage calculations.

---

### Improvement 2: Add Error Handling to `create_load_chart()`

**Location**: After existing hints in viz_tools.py

**Add these additional hints**:

```python
@tool
def create_load_chart(loads: list[float], labels: list[str], output_path: str = "load_chart.png") -> str:
    """
    Create a bar chart showing loads.

    TODO: Implement this function
    HINT: Use matplotlib.pyplot.bar() to create bar chart
    HINT: Pass labels as x-axis and loads as heights
    HINT: Add xlabel="Beam Sections", ylabel="Load (kg)", title="Structural Load Analysis"
    HINT: Use plt.xticks(rotation=45) if labels are long
    HINT: Use plt.tight_layout() before saving to prevent label cutoff
    HINT: Save with plt.savefig(output_path, dpi=300) for high-quality output
    HINT: Close the figure with plt.close() to free memory
    HINT: Return the output_path so agent knows where file was saved

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Validate input lengths match: len(loads) == len(labels)
    HINT (Error Handling): If mismatch, raise ValueError(f"Loads ({len(loads)}) and labels ({len(labels)}) must match")
    HINT (Error Handling): Wrap plt.savefig() in try/except to catch IOError (permissions, disk space)
    HINT (Error Handling): If save fails, return f"Error: Could not save chart to {output_path}: {error}"
    HINT (Error Handling): Validate output_path directory exists: Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    HINT (Error Handling): Check for empty data: if not loads: raise ValueError("Cannot create chart with empty data")

    Args:
        loads: List of load values in kg
        labels: List of labels for each bar (must match loads length)
        output_path: Where to save the chart PNG file (default: "load_chart.png")

    Returns:
        str: Path to saved chart file, or error message if save failed

    Raises:
        ValueError: If loads and labels have different lengths or data is empty
    """
    pass  # Your code here
```

**Rationale**: Visualization tools can fail in many ways (mismatched data, file system issues, empty data). Validate early.

---

### Improvement 3: Add Error Handling to `create_report_agent()`

**Location**: After existing hints in report_agent.py

**Add these additional hints**:

```python
def create_report_agent(llm, tools: list, verbose: bool = True):
    """
    Creates an agent that can generate technical reports using provided tools.

    TODO: Implement this function
    HINT: Import from langchain.agents: initialize_agent, AgentType
    HINT: Use initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=verbose)
    HINT: The ZERO_SHOT_REACT_DESCRIPTION type lets agent decide which tools to use
    HINT: Setting verbose=True shows agent's reasoning process (helpful for debugging)
    HINT: Return the initialized agent object
    HINT: Agent will use tools like calculate_beam_load and create_load_chart automatically

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Validate tools list is not empty: if not tools: raise ValueError("Must provide at least one tool")
    HINT (Error Handling): Wrap initialize_agent() in try/except to catch langchain.schema.exceptions.OutputParserException
    HINT (Error Handling): If agent creation fails, log error and return None: print(f"⚠️  Agent creation failed: {error}")
    HINT (Error Handling): Validate llm is callable: if not hasattr(llm, 'invoke'): raise TypeError("LLM must be LangChain-compatible")
    HINT (Error Handling): Check for tool name conflicts: tool_names = [t.name for t in tools]; if len(tool_names) != len(set(tool_names)): raise ValueError("Duplicate tool names found")

    Args:
        llm: Language model to power the agent (must be LangChain-compatible)
        tools: List of tool functions decorated with @tool
        verbose: Whether to print agent's reasoning steps (default: True)

    Returns:
        Agent object capable of using tools, or None if creation failed

    Raises:
        ValueError: If tools list is empty or has duplicate names
        TypeError: If llm is not LangChain-compatible
    """
    pass  # Your code here
```

**Rationale**: Agent creation can fail for many subtle reasons (incompatible LLM, bad tools, parser issues). Validate inputs.

---

### Improvement 4: Add Error Handling to `generate_report()`

**Location**: After existing hints in report_agent.py

**Add these additional hints**:

```python
def generate_report(agent, requirements: str, output_file: str = "structural_report.md") -> dict:
    """
    Generate a technical report using the agent.

    TODO: Implement this function
    HINT: Call agent.invoke({"input": requirements}) to start agent execution
    HINT: Agent will decide which tools to call based on requirements
    HINT: Extract output from result["output"] (agent returns a dict)
    HINT: Write report content to output_file using Path().write_text()
    HINT: Return a dict with {"report_path": output_file, "content": result["output"], "success": True}

    # NEW ERROR HANDLING HINTS:
    HINT (Error Handling): Wrap agent.invoke() in try/except to catch AgentExecutionError
    HINT (Error Handling): If agent fails, return {"error": str(error), "success": False}
    HINT (Error Handling): Add timeout protection: Use signal.alarm(300) for 5-minute timeout (Unix) or threading.Timer (Windows)
    HINT (Error Handling): If timeout, return {"error": "Report generation timed out after 5 minutes", "success": False}
    HINT (Error Handling): Wrap file write in try/except to catch IOError
    HINT (Error Handling): If write fails, return success=False but include content in response
    HINT (Error Handling): Validate agent is not None: if agent is None: raise ValueError("Agent not initialized")
    HINT (Error Handling): Validate requirements is not empty: if not requirements.strip(): raise ValueError("Requirements cannot be empty")

    Args:
        agent: Initialized agent from create_report_agent()
        requirements: Natural language description of what report should contain
        output_file: Path where report should be saved (default: "structural_report.md")

    Returns:
        dict: Report generation results with keys:
            - success (bool): Whether generation succeeded
            - report_path (str): Where report was saved (if successful)
            - content (str): Report content
            - error (str): Error message (if failed)

    Raises:
        ValueError: If agent is None or requirements are empty
    """
    pass  # Your code here
```

**Rationale**: Agent execution is the most failure-prone part (LLM errors, tool errors, timeouts). Comprehensive error handling is critical.

---

## Part 2: Test Execution Guidance

### New Section: Add After "Common Mistakes" (Before Verification Section)

**Insert this complete section**:

---

## 🧪 Running Your Tests

After implementing your report generation system, verify your work with the comprehensive test suite.

### Prerequisites

Ensure you have all testing dependencies:

```bash
pip install pytest pytest-asyncio matplotlib pandas
```

### Running All Tests

Execute the full test suite for Chapter 52:

```bash
pytest tests/test_chapter_52.py -v
```

**Expected Output** (when fully implemented):

```
tests/test_chapter_52.py::TestCalculationTools::test_calculate_beam_load_exists PASSED
tests/test_chapter_52.py::TestCalculationTools::test_calculate_beam_load_accuracy PASSED
tests/test_chapter_52.py::TestCalculationTools::test_calculate_safety_factor_exists PASSED
tests/test_chapter_52.py::TestCalculationTools::test_calculate_safety_factor_accuracy PASSED
tests/test_chapter_52.py::TestVisualizationTools::test_create_load_chart_exists PASSED
tests/test_chapter_52.py::TestVisualizationTools::test_create_load_chart_creates_file PASSED
tests/test_chapter_52.py::TestVisualizationTools::test_create_stress_diagram_exists PASSED
tests/test_chapter_52.py::TestAgentOrchestration::test_create_report_agent_exists PASSED
tests/test_chapter_52.py::TestAgentOrchestration::test_generate_report_exists PASSED
tests/test_chapter_52.py::TestReportStructure::test_report_contains_calculations PASSED
tests/test_chapter_52.py::TestReportStructure::test_report_contains_visualizations PASSED
tests/test_chapter_52.py::TestPropertyP74::test_p74_calculation_accuracy PASSED
tests/test_chapter_52.py::TestPropertyP74::test_p74_calculation_precision PASSED
tests/test_chapter_52.py::TestPropertyP75::test_p75_visualization_file_exists PASSED
tests/test_chapter_52.py::TestPropertyP75::test_p75_chart_has_correct_data PASSED
tests/test_chapter_52.py::TestIntegration::test_full_report_generation_pipeline PASSED

========================= 16 passed in 12.54s =========================
```

### Running Specific Test Categories

**Test only calculation tools**:
```bash
pytest tests/test_chapter_52.py::TestCalculationTools -v
```

**Test only visualization tools**:
```bash
pytest tests/test_chapter_52.py::TestVisualizationTools -v
```

**Test only agent orchestration**:
```bash
pytest tests/test_chapter_52.py::TestAgentOrchestration -v
```

**Test only properties P74 & P75 (correctness)**:
```bash
pytest tests/test_chapter_52.py::TestPropertyP74 -v
pytest tests/test_chapter_52.py::TestPropertyP75 -v
```

### Understanding Test Results

#### ✅ When Tests Pass

```
tests/test_chapter_52.py::TestPropertyP74::test_p74_calculation_accuracy PASSED
```

**Meaning**: Your calculation tool returns mathematically correct results (10m * 500kg/m = 5000kg).

---

#### ⏭️ When Tests Skip

```
tests/test_chapter_52.py::TestVisualizationTools::test_create_load_chart_creates_file SKIPPED
```

**Meaning**: Test was skipped because:
- Tool function doesn't exist yet (`pass` still in place)
- matplotlib not installed
- File creation not implemented

**Action**: Implement the tool and rerun tests.

---

#### ❌ When Tests Fail

```
tests/test_chapter_52.py::TestPropertyP74::test_p74_calculation_accuracy FAILED

E AssertionError: Calculation inaccurate!
E Expected: 5000.0
E Got: 5000.125 (LLM hallucinated the calculation)
```

**Meaning**: Your implementation has a bug. The assertion message explains what went wrong.

**Action**:
- Check if you're using the tool pattern correctly (`@tool` decorator)
- Verify LLM is calling the tool, not doing math in its head
- Print agent's reasoning: set `verbose=True`

---

### Test-Driven Development (TDD) Workflow

**Step 1**: Run tests before implementing (they should skip):
```bash
pytest tests/test_chapter_52.py::TestCalculationTools -v
```

**Step 2**: Implement the first tool (e.g., `calculate_beam_load()`)

**Step 3**: Run tests again:
```bash
pytest tests/test_chapter_52.py::TestCalculationTools::test_calculate_beam_load_accuracy -v
```

**Step 4**: Fix any failures based on assertion messages

**Step 5**: Move to next tool, repeat until all tests pass ✅

---

### Running the Verification Script

After all implementation tests pass, run the correctness verification:

```bash
python verify_report.py
```

**Expected Output**:
```
Testing Properties P74 (Calculation Accuracy) & P75 (Visualization Correctness)
===============================================================================

Property P74: Testing Calculation Accuracy
Test: 10m beam * 500 kg/m = ?
Agent Result: 5000.0 kg
Expected: 5000.0 kg
✅ PASS: P74 - Calculation is mathematically correct

Property P75: Testing Visualization Correctness
Test: Chart saved to load_chart_test.png
File exists: True
Chart dimensions: 1200x800 pixels
Data points: 4 bars
✅ PASS: P75 - Visualization generated correctly

===============================================================================
✅ ALL PROPERTIES VERIFIED
```

**If verification fails**:
```
❌ FAIL: P74 - Agent calculated 5125.0 instead of 5000.0
→ Agent is doing math in its head instead of using the tool!
```

**Fix**: Check that agent has access to tools and is actually calling them (set `verbose=True`).

---

### Debugging Failed Tests

**Problem**: `test_calculate_beam_load_accuracy` fails

**Common Causes**:
1. Forgot `@tool` decorator
2. Tool not added to agent's tool list
3. Function does wrong calculation
4. Returns wrong type (string instead of float)

**Debug Steps**:
1. Test tool directly: `result = calculate_beam_load.invoke({"length": 10, "load_per_meter": 500})`
2. Print result type: `print(type(result), result)`
3. Verify it's a tool: `print(calculate_beam_load.name)` should print function name
4. Check if agent has it: `print([t.name for t in agent.tools])`

---

**Problem**: `test_create_load_chart_creates_file` fails

**Common Causes**:
1. File not actually saved (forgot `plt.savefig()`)
2. Wrong file path (check current directory)
3. Permissions issue (can't write to path)
4. Matplotlib backend issue (can't render in headless mode)

**Debug Steps**:
1. Print current directory: `print(Path.cwd())`
2. List files after save: `print(list(Path('.').glob('*.png')))`
3. Check file exists: `print(Path('load_chart.png').exists())`
4. Try absolute path: `output_path = str(Path.cwd() / 'load_chart.png')`

**Fix for headless environments** (CI/CD, Docker):
```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
```

---

**Problem**: `test_p74_calculation_accuracy` fails (LLM does math wrong)

**Common Causes**:
1. Agent not actually calling the tool
2. Tool not in agent's tool list
3. LLM hallucinating answer instead of using tool
4. Agent type doesn't support tools

**Debug Steps**:
1. Set verbose=True: `agent = create_report_agent(llm, tools, verbose=True)`
2. Look for tool calls in output: Should see "Using tool: calculate_beam_load"
3. Check agent type: Should be ZERO_SHOT_REACT_DESCRIPTION or STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
4. Print agent's tool list: `print([t.name for t in agent.tools])`

**If agent still won't use tools**:
```python
# Force tool usage in prompt
requirements = """
Calculate the beam load for a 10-meter beam with 500 kg/m load.
YOU MUST use the calculate_beam_load tool. DO NOT do the math yourself.
Call: calculate_beam_load(length=10, load_per_meter=500)
"""
```

---

**Problem**: `test_full_report_generation_pipeline` times out

**Common Causes**:
1. Agent stuck in reasoning loop
2. LLM API slow/unavailable
3. Too many tool calls
4. Infinite loop in agent logic

**Debug Steps**:
1. Set max_iterations: `agent = initialize_agent(..., max_iterations=10)`
2. Monitor tool calls: Set `verbose=True` to see agent's reasoning
3. Test tools individually: Ensure each tool works before testing agent
4. Simplify requirements: Start with simple report, add complexity gradually

**Emergency timeout**:
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Agent execution exceeded time limit")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)  # 60 second timeout

try:
    result = agent.invoke(requirements)
finally:
    signal.alarm(0)  # Cancel alarm
```

---

### Performance Notes

**Test Suite Runtime**: ~10-15 seconds (with tool/agent execution)

**If tests are very slow** (>2 minutes):
- LLM API latency (switch to faster model: gpt-3.5-turbo vs gpt-4)
- Too many agent iterations (set max_iterations=5)
- Large file I/O (use smaller test data)
- Matplotlib rendering slow (use 'Agg' backend)

**If tests fail intermittently**:
- LLM non-determinism (set temperature=0 for consistency)
- API rate limits (add retry logic)
- File system race conditions (use unique file names per test)

---

## Part 3: Common Errors & Debugging

### New Section: Add After "🧪 Running Your Tests" (Before Verification Section)

**Insert this complete section**:

---

## 🐛 Common Errors & How to Fix Them

### Error 1: `ModuleNotFoundError: No module named 'matplotlib'`

**Symptom**:
```python
Traceback (most recent call last):
  File "viz_tools.py", line 1, in <module>
    import matplotlib.pyplot as plt
ModuleNotFoundError: No module named 'matplotlib'
```

**Cause**: Matplotlib not installed

**Fix**:
```bash
pip install matplotlib pandas
```

**Verify**:
```bash
python -c "import matplotlib; print('Matplotlib:', matplotlib.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
```

---

### Error 2: `langchain.schema.exceptions.OutputParserException`

**Symptom**:
```
langchain.schema.exceptions.OutputParserException: Could not parse LLM output
```

**Cause**:
- LLM didn't follow expected output format
- Agent type incompatible with tools
- LLM output too verbose or malformed

**Fix**:

**Step 1**: Check agent type - use one that supports tools:
```python
# GOOD - Supports tools:
AgentType.ZERO_SHOT_REACT_DESCRIPTION
AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION

# BAD - No tool support:
AgentType.CONVERSATIONAL
```

**Step 2**: Add error handling:
```python
from langchain.schema.exceptions import OutputParserException

try:
    result = agent.invoke(requirements)
except OutputParserException as e:
    print(f"⚠️  Agent output parsing failed: {e}")
    print("Retrying with simpler prompt...")
    # Retry with more specific instructions
```

**Step 3**: Simplify requirements if complex:
```python
# TOO COMPLEX (agent gets confused):
requirements = "Analyze all beams, calculate safety factors, generate 5 charts, write detailed report with executive summary..."

# SIMPLE (clear steps):
requirements = "Calculate load for 10m beam at 500kg/m. Create one bar chart showing this result."
```

---

### Error 3: Agent Won't Use Tools (Does Math in Its Head)

**Symptom**:
```python
# You ask: "Calculate 55 * 142"
# Agent responds: "The answer is approximately 7810"  ← WRONG! (hallucinated)
# Should have called calculate_beam_load tool
```

**Cause**:
- Tools not passed to agent
- LLM thinks it can do math itself
- Tool names/descriptions unclear

**Fix**:

**Step 1**: Verify tools are passed:
```python
agent = create_report_agent(llm, tools=[calculate_beam_load, create_load_chart])
print(f"Agent has {len(agent.tools)} tools: {[t.name for t in agent.tools]}")
# Should print: Agent has 2 tools: ['calculate_beam_load', 'create_load_chart']
```

**Step 2**: Make tool descriptions explicit:
```python
@tool
def calculate_beam_load(length: float, load_per_meter: float) -> float:
    """
    Calculates total load on a beam. USE THIS TOOL FOR ALL CALCULATIONS.
    DO NOT attempt to do math yourself - you will get it wrong.

    Args:
        length: Beam length in meters
        load_per_meter: Load per meter in kg/m

    Returns:
        Exact total load in kg
    """
    return length * load_per_meter
```

**Step 3**: Force tool usage in prompt:
```python
requirements = """
IMPORTANT: You MUST use tools for all calculations. DO NOT do math yourself.

Task: Calculate the load for a 10-meter beam with 500 kg/m load.
Use the calculate_beam_load tool with these exact parameters.
"""
```

**Step 4**: Set verbose=True to debug:
```python
agent = create_report_agent(llm, tools, verbose=True)
result = agent.invoke(requirements)
# Watch for: "Action: calculate_beam_load" (good) vs "Final Answer: 5000" (bad, no tool used)
```

---

### Error 4: `FileNotFoundError: [Errno 2] No such file or directory: 'load_chart.png'`

**Symptom**:
```python
FileNotFoundError: [Errno 2] No such file or directory: 'load_chart.png'
```

**Cause**:
- Chart not actually saved (forgot plt.savefig)
- Saved to wrong directory
- Filename has spaces/special characters

**Debug Steps**:

**Step 1**: Check where file was saved:
```python
import os
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
```

**Step 2**: Use absolute path:
```python
from pathlib import Path

output_path = Path.cwd() / "load_chart.png"
plt.savefig(str(output_path))
print(f"Saved to: {output_path}")
print(f"File exists: {output_path.exists()}")
```

**Step 3**: Ensure directory exists:
```python
output_path = Path("reports") / "load_chart.png"
output_path.parent.mkdir(parents=True, exist_ok=True)  # Create reports/ if missing
plt.savefig(str(output_path))
```

---

### Error 5: Matplotlib Shows Error: `_tkinter.TclError: no display name`

**Symptom** (Linux/Docker/CI):
```
_tkinter.TclError: no display name and no $DISPLAY environment variable
```

**Cause**: Matplotlib trying to use GUI backend in headless environment

**Fix**:

**Add at top of viz_tools.py** (before importing pyplot):
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
```

**Or set via environment**:
```bash
export MPLBACKEND=Agg
python viz_tools.py
```

---

### Error 6: Agent Timeout / Hangs Forever

**Symptom**:
```python
# Agent starts processing...
# Never returns (stuck in infinite loop)
```

**Cause**:
- Agent stuck in reasoning loop
- Waiting for slow API
- Tool calls failing silently
- max_iterations not set

**Fix**:

**Step 1**: Set max_iterations:
```python
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=10  # Stop after 10 steps
)
```

**Step 2**: Add timeout:
```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

def generate_with_timeout(agent, requirements, timeout_seconds=60):
    """Run agent with timeout protection."""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(agent.invoke, {"input": requirements})
        try:
            result = future.result(timeout=timeout_seconds)
            return result
        except TimeoutError:
            return {"error": f"Agent timed out after {timeout_seconds}s"}

result = generate_with_timeout(agent, requirements, timeout_seconds=120)
```

**Step 3**: Debug with verbose=True:
```python
# Watch agent's reasoning in real-time
agent = create_report_agent(llm, tools, verbose=True)
# If you see repeated actions, agent is stuck
```

---

### Error 7: Calculation Results Are Wrong (P74 Fails)

**Symptom**:
```
Expected: 5000.0
Got: 5125.3
```

**Cause**:
- LLM did math itself (didn't use tool)
- Tool has bug in calculation
- Wrong parameters passed to tool
- Floating-point precision issue

**Debug Steps**:

**Step 1**: Test tool directly:
```python
result = calculate_beam_load.invoke({"length": 10, "load_per_meter": 500})
print(f"Tool result: {result}")
assert result == 5000.0, f"Tool calculation wrong: {result}"
```

**Step 2**: Check if agent called tool:
```python
agent = create_report_agent(llm, tools, verbose=True)
result = agent.invoke("Calculate load: 10m beam, 500kg/m")

# Look for in output:
# "Action: calculate_beam_load"  ← Good, tool used
# "Action Input: {length: 10, load_per_meter: 500}"

# If you see:
# "Final Answer: The load is approximately 5000kg"  ← Bad, LLM guessed
```

**Step 3**: Force tool usage:
```python
requirements = """
You MUST use the calculate_beam_load tool for this calculation.
DO NOT estimate. Use exact parameters: length=10, load_per_meter=500.
"""
```

---

### Error 8: Chart Looks Wrong (P75 Fails)

**Symptom**:
- Chart file exists but has wrong data
- Bars are different heights than expected
- Labels don't match data
- Chart is blank/corrupted

**Debug Steps**:

**Step 1**: Verify data before plotting:
```python
def create_load_chart(loads, labels, output_path):
    print(f"📊 Creating chart with {len(loads)} data points")
    print(f"   Loads: {loads}")
    print(f"   Labels: {labels}")

    assert len(loads) == len(labels), "Data length mismatch!"

    plt.figure(figsize=(10, 6))
    plt.bar(labels, loads)
    # ... rest of plotting
```

**Step 2**: Open and inspect chart:
```python
from PIL import Image
img = Image.open('load_chart.png')
print(f"Chart size: {img.size}")  # Should be reasonable (e.g., 1000x600)
print(f"Chart mode: {img.mode}")  # Should be 'RGB' or 'RGBA'
img.show()  # Opens in system image viewer
```

**Step 3**: Check matplotlib wasn't corrupted:
```python
# Ensure figure was closed properly
plt.close('all')

# Create new chart
fig, ax = plt.subplots()
ax.bar(['A', 'B'], [1, 2])
plt.savefig('test.png')
plt.close()

# Verify test chart
assert Path('test.png').exists(), "Chart creation completely broken"
```

---

### Debugging Checklist

When your report generation system isn't working, check these in order:

**1. Dependencies**
- [ ] Matplotlib installed: `pip install matplotlib`
- [ ] Pandas installed: `pip install pandas`
- [ ] LangChain installed: `pip install langchain langchain-openai`
- [ ] OpenAI key set: `echo $OPENAI_API_KEY`

**2. Tools**
- [ ] Tools decorated with @tool
- [ ] Tool names are descriptive
- [ ] Tools added to agent's tool list
- [ ] Tools return correct types (float, str, etc.)

**3. Agent**
- [ ] Agent type supports tools (ZERO_SHOT_REACT_DESCRIPTION)
- [ ] Tools passed in tools parameter
- [ ] max_iterations set (prevent infinite loops)
- [ ] verbose=True for debugging

**4. Calculations (P74)**
- [ ] Agent calls calculation tools (not doing math itself)
- [ ] Tool calculations are correct (test directly)
- [ ] Parameters passed correctly
- [ ] Results are exact (not approximations)

**5. Visualizations (P75)**
- [ ] Files are actually saved
- [ ] Paths are correct (absolute if needed)
- [ ] Data lengths match (loads vs labels)
- [ ] Matplotlib backend set ('Agg' for headless)

---

### Getting Help

If you're still stuck after debugging:

**1. Check test assertion messages** - They explain what's wrong:
```
AssertionError: Expected 5000.0, got 5125.3 (agent didn't use tool)
```

**2. Use verbose=True** - See agent's reasoning:
```python
agent = create_report_agent(llm, tools, verbose=True)
# Watch for "Action: calculate_beam_load" (good)
# vs "Final Answer: 5000" (bad, guessed)
```

**3. Test components separately**:
- Test each tool individually
- Test agent with one tool at a time
- Test full workflow only after parts work

**4. Compare with solution code** (in `<details>` sections):
- How does your tool differ?
- Is your agent type correct?
- Are tool descriptions clear enough?

---

## Summary of Improvements

**Added to Chapter 52**:

1. ✅ **Error Handling Hints**: 4 functions enhanced with 18 additional hints
   - `calculate_beam_load()`: Input validation and type checking
   - `create_load_chart()`: Data validation, file system error handling
   - `create_report_agent()`: Tool validation, agent creation error handling
   - `generate_report()`: Timeout protection, execution error handling

2. ✅ **Test Execution Guidance**: Complete "🧪 Running Your Tests" section
   - How to run all tests and specific categories
   - Understanding PASSED/SKIPPED/FAILED results
   - TDD workflow for capstone projects
   - Debugging complex agent failures
   - Performance notes for agent execution

3. ✅ **Common Errors & Debugging**: Complete "🐛 Common Errors" section
   - 8 common error scenarios with fixes
   - Agent-specific debugging (tool usage, timeouts, parsing)
   - Visualization debugging (file I/O, matplotlib backend)
   - Property testing failures (P74 calculations, P75 charts)
   - Comprehensive debugging checklists

**Total New Content**: ~2000 words of practical guidance

---

## Insertion Points in Chapter 52

**Error Handling Hints**: Update the four scaffolded functions directly with new hints

**Test Execution Section**: Insert after "Common Mistakes" section, before "Verification (REQUIRED SECTION)"

**Debugging Section**: Insert after "🧪 Running Your Tests", before "Verification (REQUIRED SECTION)"

**Final Structure**:
1. Coffee Shop Intro
2. Prerequisites
3. Calculator Story
4. Part 1: calc_tools.py (with error hints)
5. Part 2: viz_tools.py (with error hints)
6. Part 3: report_agent.py (with error hints)
7. Common Mistakes
8. **🧪 Running Your Tests** ← NEW
9. **🐛 Common Errors & Debugging** ← NEW
10. Verification (P74, P75)
11. Summary
12. What's Next

---

**Status**: ✅ COMPLETE - Ready to merge into Chapter 52
