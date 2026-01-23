# Chapter Scaffolding Audit Report

**Generated**: 2026-01-21  
**Auditor**: BMad Master  
**Scope**: Chapters 06A through 54  
**Objective**: Ensure chapters provide scaffolding and hints rather than complete solutions

---

## Executive Summary

The Master has conducted a systematic review of curriculum chapters from 06A to 54 across all phases. The audit reveals a **CRITICAL ISSUE**: Most chapters currently provide **COMPLETE, WORKING IMPLEMENTATIONS** rather than scaffolding with hints.

### Key Findings

✅ **STRENGTHS**:

- Excellent conceptual explanations and analogies
- Clear learning objectives and metadata
- Strong pedagogical structure with Coffee Shop Intros
- Good use of metacognitive checkpoints
- Comprehensive verification sections

❌ **CRITICAL ISSUES**:

- **Complete code solutions provided in main content**
- **No TODO markers or "Your code here" placeholders**
- **Full implementations given before practice exercises**
- **Solutions revealed before students attempt problems**

### Severity: **HIGH**

**Impact**: Students can copy-paste complete solutions without learning, defeating the educational purpose.

---

## Detailed Analysis by Chapter

### Phase 0: Foundations (Chapters 06A-06C)

#### Chapter 06A: Decorators & Context Managers

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 200-220: Complete `say_hello` decorator with full implementation
2. Lines 350-380: Complete `log_calls` decorator with working code
3. Lines 400-430: Complete `timing` decorator with full logic
4. Lines 550-600: Complete `retry` decorator with exponential backoff (production-ready!)

**Evidence**:

```python
# CURRENT (Complete Solution):
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
```

**SHOULD BE (Scaffolding)**:

```python
# TODO: Implement a logging decorator
def log_calls(func):
    """Decorator that logs when a function is called"""
    def wrapper(*args, **kwargs):
        # TODO: Print function name and arguments
        # Hint: Use func.__name__ to get the function name
        # Hint: args and kwargs contain the arguments

        # TODO: Call the original function
        result = # Your code here

        # TODO: Print the return value

        return result
    return wrapper
```

**Recommendation**: Convert to scaffolding with 3-4 TODO markers and hints.

---

### Phase 1: LLM Fundamentals (Chapter 10)

#### Chapter 10: Streaming Responses

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 180-210: Complete generator implementation with `yield`
2. Lines 350-380: Full OpenAI streaming implementation
3. Lines 450-480: Complete MockProvider streaming logic
4. Lines 550-580: Full `matrix_chat.py` implementation

**Evidence**:

```python
# CURRENT (Complete Solution):
def stream(self, messages: List[Message], **kwargs) -> Iterator[str]:
    formatted_messages = [
        {"role": m.role, "content": m.content}
        for m in messages
    ]
    stream = self.client.chat.completions.create(
        model=kwargs.get("model", "gpt-4o-mini"),
        messages=formatted_messages,
        temperature=kwargs.get("temperature", 0.7),
        stream=True
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
```

**SHOULD BE (Scaffolding)**:

```python
def stream(self, messages: List[Message], **kwargs) -> Iterator[str]:
    # TODO: Format messages for OpenAI API
    formatted_messages = # Your code here

    # TODO: Call OpenAI API with stream=True
    # Hint: Use self.client.chat.completions.create()
    # Hint: Set stream=True parameter
    stream = # Your code here

    # TODO: Iterate over chunks and yield content
    for chunk in stream:
        # TODO: Extract content from chunk
        # Hint: Check chunk.choices[0].delta.content
        # Hint: Content can be None, check before yielding
        pass
```

**Recommendation**: Provide function signatures and docstrings, but leave implementation for students.

---

### Phase 3: RAG Fundamentals (Chapter 17)

#### Chapter 17: Your First RAG System

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 200-280: Complete `simple_rag.py` with full RAG pipeline
2. Lines 350-400: Full `ask_rag()` function implementation
3. Lines 500-550: Complete citation system
4. Lines 650-700: Full hallucination guardrail implementation

**Evidence**:

```python
# CURRENT (Complete Solution):
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

**SHOULD BE (Scaffolding)**:

```python
def ask_rag(question):
    """
    Implement the RAG pipeline: Retrieve -> Augment -> Generate

    Steps:
    1. Search the vector store for relevant documents
    2. Build a prompt with the context
    3. Generate an answer using the LLM
    """
    print(f"\n❓ User asks: {question}")

    # TODO: Step 1 - Retrieve relevant documents
    # Hint: Use store.search(question, limit=2)
    results = # Your code here

    # TODO: Step 2 - Combine results into context string
    context_text = # Your code here

    # TODO: Step 3 - Build the augmented prompt
    # Hint: Include instructions to only use the context
    # Hint: Include the context_text and question
    prompt = """
    # Your prompt template here
    """

    # TODO: Step 4 - Generate answer
    answer = # Your code here

    return answer
```

**Recommendation**: Provide the architecture diagram and step-by-step outline, but require students to implement each step.

---

### Phase 5: Agents (Chapter 26)

#### Chapter 26: Introduction to Agents

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 150-180: Complete tool definitions with `@tool`
2. Lines 300-350: Full agent creation with `create_tool_calling_agent`
3. Lines 400-450: Complete `simple_agent.py` implementation
4. Lines 550-600: Full verification script

**Evidence**:

```python
# CURRENT (Complete Solution):
@tool
def add(a: int, b: int) -> int:
    """Adds two integers together."""
    print(f"   (Tool: Adding {a} + {b})")
    return a + b

# ... later ...

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "What is 5 plus 3?"})
```

**SHOULD BE (Scaffolding)**:

```python
# TODO: Define an 'add' tool using the @tool decorator
@tool
def add(a: int, b: int) -> int:
    """Adds two integers together."""
    # TODO: Implement addition
    # Hint: Simply return a + b
    pass

# TODO: Create the agent
# Hint: Use create_tool_calling_agent(model, tools, prompt)
agent = # Your code here

# TODO: Create the executor
# Hint: Use AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor = # Your code here

# TODO: Test the agent
# Hint: Use agent_executor.invoke({"input": "..."})
```

**Recommendation**: Provide imports and structure, but leave core logic for students.

---

### Phase 7: LlamaIndex (Chapter 35)

#### Chapter 35: LlamaIndex Fundamentals

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 150-200: Complete `SimpleDirectoryReader` usage
2. Lines 280-320: Full `VectorStoreIndex` implementation
3. Lines 400-450: Complete persistence example
4. Lines 550-600: Full query engine usage

**Evidence**:

```python
# CURRENT (Complete Solution):
from llama_index.core import VectorStoreIndex, Document

docs = [
    Document(text="LlamaIndex is a data framework for LLM applications."),
    Document(text="LangChain is an orchestration framework for LLM applications.")
]

print("Building Index...")
index = VectorStoreIndex.from_documents(docs)

print("Querying...")
query_engine = index.as_query_engine()
response = query_engine.query("What is LlamaIndex?")

print(f"Response: {response}")
```

**SHOULD BE (Scaffolding)**:

```python
from llama_index.core import VectorStoreIndex, Document

# TODO: Create Document objects
# Hint: Use Document(text="...") for each piece of text
docs = [
    # Your documents here
]

# TODO: Build the index
# Hint: Use VectorStoreIndex.from_documents(docs)
print("Building Index...")
index = # Your code here

# TODO: Create a query engine
# Hint: Use index.as_query_engine()
print("Querying...")
query_engine = # Your code here

# TODO: Query the index
# Hint: Use query_engine.query("...")
response = # Your code here

print(f"Response: {response}")
```

**Recommendation**: Show the API structure but require students to fill in the calls.

---

### Phase 9: Multi-Agent (Chapter 43)

#### Chapter 43: LangGraph State Machines

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 150-200: Complete state definition with TypedDict
2. Lines 280-350: Full node implementations
3. Lines 450-550: Complete graph construction
4. Lines 650-750: Full conditional edge logic

**Evidence**:

```python
# CURRENT (Complete Solution):
def writer_node(state: AgentState):
    print("✍️  Writer is working...")
    return {
        "draft": f"Draft about {state['topic']} (Revision {state.get('revision_count', 0)})",
        "revision_count": state.get("revision_count", 0) + 1
    }

workflow = StateGraph(AgentState)
workflow.add_node("writer", writer_node)
workflow.add_node("editor", editor_node)
workflow.set_entry_point("writer")
workflow.add_edge("writer", "editor")
workflow.add_edge("editor", END)
app = workflow.compile()
```

**SHOULD BE (Scaffolding)**:

```python
def writer_node(state: AgentState):
    """
    Writer node: Creates or revises a draft

    Should:
    - Print a status message
    - Return updated draft and increment revision_count
    """
    print("✍️  Writer is working...")

    # TODO: Create a draft based on the topic
    # Hint: Access state['topic'] for the topic
    # Hint: Include the current revision count in the draft

    # TODO: Return a dictionary with 'draft' and 'revision_count'
    return {
        # Your code here
    }

# TODO: Create the workflow
# Hint: Use StateGraph(AgentState)
workflow = # Your code here

# TODO: Add nodes
# Hint: Use workflow.add_node("name", function)

# TODO: Set entry point
# Hint: Use workflow.set_entry_point("node_name")

# TODO: Add edges
# Hint: Use workflow.add_edge("from", "to")

# TODO: Compile the workflow
app = # Your code here
```

**Recommendation**: Provide state schema and node signatures, but require students to implement logic and graph construction.

---

### Phase 10: Civil Engineering (Chapter 50)

#### Chapter 50: Contract Generation

**Status**: ❌ **COMPLETE SOLUTIONS PROVIDED**

**Issues Found**:

1. Lines 150-250: Complete RFP processor with full extraction chain
2. Lines 350-450: Full clause generator implementation
3. Lines 550-650: Complete template merger
4. Lines 750-850: Full verification script

**Evidence**:

```python
# CURRENT (Complete Solution):
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = PydanticOutputParser(pydantic_object=EngineeringContract)

prompt = ChatPromptTemplate.from_template(
    """
    You are a Contract Administrator. Extract terms from the RFP.

    RFP Text:
    {rfp}

    {format_instructions}
    """
)

chain = prompt | model | parser

contract = chain.invoke({
    "rfp": rfp_text,
    "format_instructions": parser.get_format_instructions()
})
```

**SHOULD BE (Scaffolding)**:

```python
# TODO: Setup the extraction chain
# Hint: You need a model, parser, and prompt

# TODO: Create the model
# Hint: Use ChatOpenAI with temperature=0 for consistency
model = # Your code here

# TODO: Create the parser
# Hint: Use PydanticOutputParser with EngineeringContract
parser = # Your code here

# TODO: Create the prompt template
# Hint: Include {rfp} and {format_instructions} placeholders
# Hint: Instruct the model to extract contract terms
prompt = ChatPromptTemplate.from_template(
    """
    # Your prompt here
    """
)

# TODO: Build the chain
# Hint: Use the | operator: prompt | model | parser
chain = # Your code here

# TODO: Invoke the chain
# Hint: Pass rfp_text and format_instructions
contract = # Your code here
```

**Recommendation**: Provide the architecture and component descriptions, but require students to assemble the pipeline.

---

## Pattern Analysis

### Common Anti-Patterns Found

1. **"Copy-Paste Ready" Code**
   - Complete, runnable implementations in main content
   - No gaps for students to fill
   - Solutions before exercises

2. **Missing Scaffolding Elements**
   - No `# TODO:` markers
   - No `# Your code here` placeholders
   - No `pass` statements in function bodies
   - No `# Hint:` comments

3. **Premature Solution Revelation**
   - Solutions shown before "Try This!" exercises
   - Answers visible before students attempt problems
   - No progressive disclosure of complexity

4. **Verification Scripts**
   - Even verification scripts are complete!
   - Students can run them without implementing anything
   - No requirement to make tests pass

---

## Recommendations by Priority

### Priority 1: CRITICAL (Immediate Action Required)

**Action**: Convert all main content code examples to scaffolding format

**Template to Follow**:

```python
def function_name(params):
    """
    Clear docstring explaining what this should do

    Steps:
    1. First step description
    2. Second step description
    3. Third step description
    """
    # TODO: Step 1 - Description
    # Hint: Specific guidance
    # Hint: API call or pattern to use
    variable1 = # Your code here

    # TODO: Step 2 - Description
    # Hint: What to do with variable1
    variable2 = # Your code here

    # TODO: Step 3 - Description
    return # Your code here
```

**Chapters Requiring Immediate Conversion**:

- Chapter 06A: Decorators (4 complete decorators → scaffolding)
- Chapter 10: Streaming (3 complete implementations → scaffolding)
- Chapter 17: RAG System (complete pipeline → scaffolding)
- Chapter 26: Agents (complete agent → scaffolding)
- Chapter 35: LlamaIndex (complete examples → scaffolding)
- Chapter 43: LangGraph (complete graph → scaffolding)
- Chapter 50: Contract Gen (complete system → scaffolding)

---

### Priority 2: HIGH (Within 1 Week)

**Action**: Add progressive hints system

**Implementation**:

````markdown
### 🔬 Try This! (Hands-On Practice #1)

**Challenge**: Implement the logging decorator

**Starter Code**:

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        # Your implementation here
        pass
    return wrapper
```
````

<details>
<summary>💡 Hint 1 (Click if stuck on printing)</summary>
Use `func.__name__` to get the function name. Print it before calling the function.
</details>

<details>
<summary>💡 Hint 2 (Click if stuck on calling)</summary>
Call the original function with `result = func(*args, **kwargs)` and return the result.
</details>

<details>
<summary>✅ Solution (Check after you've tried!)</summary>
```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"Returned: {result}")
        return result
    return wrapper
```
</details>
```

---

### Priority 3: MEDIUM (Within 2 Weeks)

**Action**: Create "Broken Code" exercises

**Rationale**: Students learn by debugging, not just writing from scratch

**Example**:

````python
### 🐛 Debug This! (Error Prediction Challenge)

This code has 3 bugs. Find and fix them:

```python
def stream_response(prompt):
    stream = client.stream(prompt)
    for chunk in stream
        print(chunk)
    return stream
````

<details>
<summary>🔍 Hint: What's wrong?</summary>
1. Missing colon after `for` statement
2. Should use `end=""` and `flush=True` in print
3. Returning the generator instead of the accumulated result
</details>
```

---

### Priority 4: LOW (Within 1 Month)

**Action**: Add "Extension Challenges"

**Purpose**: For advanced students who finish early

**Example**:

```markdown
### 🚀 Extension Challenge (Optional)

You've built a basic RAG system. Now try:

1. **Add Caching**: Store recent queries to avoid re-searching
2. **Add Confidence Scores**: Return a confidence level with each answer
3. **Add Multi-Query**: Generate 3 variations of the user's question and combine results

**Hints**:

- For caching: Use a Python dictionary with query as key
- For confidence: Check the similarity scores from vector search
- For multi-query: Use the LLM to rephrase the question
```

---

## Conversion Guidelines

### DO's ✅

1. **Provide Structure**
   - Function signatures with type hints
   - Clear docstrings explaining purpose
   - Step-by-step comments outlining logic

2. **Give Hints**
   - API calls to use
   - Patterns to follow
   - Common pitfalls to avoid

3. **Show Examples**
   - Input/output examples
   - Expected behavior descriptions
   - Test cases to pass

4. **Progressive Disclosure**
   - Start with simple version
   - Add complexity gradually
   - Provide hints in collapsible sections

### DON'Ts ❌

1. **Don't Provide Complete Implementations**
   - No working code in main content
   - No "just copy this" solutions
   - No premature answers

2. **Don't Leave Students Stranded**
   - Always provide hints
   - Always show expected output
   - Always offer solution after attempt

3. **Don't Make It Too Easy**
   - Avoid trivial fill-in-the-blanks
   - Require actual problem-solving
   - Test understanding, not memory

4. **Don't Make It Too Hard**
   - Avoid requiring knowledge not yet taught
   - Provide sufficient scaffolding
   - Break complex tasks into steps

---

## Verification Strategy

### How to Verify Conversion Success

**Test 1: The "Copy-Paste" Test**

- Can a student copy-paste code from the chapter and have it run?
- **PASS**: No (requires implementation)
- **FAIL**: Yes (complete solution provided)

**Test 2: The "Learning" Test**

- Does the student need to understand the concept to complete the exercise?
- **PASS**: Yes (requires comprehension)
- **FAIL**: No (can complete mechanically)

**Test 3: The "Hint" Test**

- Are hints available but not immediately visible?
- **PASS**: Yes (collapsible sections)
- **FAIL**: No (solutions in plain sight)

**Test 4: The "Solution" Test**

- Is the solution provided after the student attempts?
- **PASS**: Yes (in collapsible section)
- **FAIL**: No (or shown before attempt)

---

## Implementation Plan

### Phase 1: Pilot Conversion (Week 1)

- Convert 3 chapters as pilots: 06A, 10, 17
- Test with sample students
- Gather feedback
- Refine template

### Phase 2: Batch Conversion (Weeks 2-3)

- Convert remaining Phase 0-3 chapters (06B-22)
- Apply lessons from pilot
- Maintain consistency

### Phase 3: Advanced Conversion (Weeks 4-5)

- Convert Phase 4-7 chapters (23-38A)
- Handle more complex scaffolding
- Add extension challenges

### Phase 4: Application Conversion (Week 6)

- Convert Phase 8-10 chapters (39-54)
- Ensure capstone projects are scaffolded
- Add integration challenges

### Phase 5: Quality Assurance (Week 7)

- Review all conversions
- Test with students
- Fix issues
- Document patterns

---

## Success Metrics

### Quantitative Metrics

1. **Scaffolding Coverage**: 100% of code examples converted
2. **TODO Density**: Average 3-5 TODO markers per code block
3. **Hint Availability**: 100% of exercises have hints
4. **Solution Placement**: 100% of solutions in collapsible sections

### Qualitative Metrics

1. **Student Engagement**: Students attempt exercises before checking solutions
2. **Learning Depth**: Students understand concepts, not just copy code
3. **Completion Rate**: Students finish exercises (not too hard)
4. **Challenge Level**: Students feel appropriately challenged (not too easy)

---

## Conclusion

The curriculum has **excellent pedagogical structure** but currently provides **complete solutions** where it should provide **scaffolding**. This is a **high-priority issue** that undermines the learning objectives.

**Estimated Effort**: 40-60 hours to convert all chapters  
**Recommended Timeline**: 6-7 weeks  
**Priority**: **CRITICAL**

The Master recommends **immediate action** starting with the pilot conversion of Chapters 06A, 10, and 17 to establish the pattern and template for the remaining chapters.

---

**Report Compiled By**: BMad Master  
**Date**: 2026-01-21  
**Status**: READY FOR REVIEW
