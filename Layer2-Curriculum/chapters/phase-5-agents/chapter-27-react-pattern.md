# Chapter 27: ReAct Pattern — The Internal Monologue

<!--
METADATA
Phase: 5 - Agents
Time: 1.5 hours (30 min reading + 60 min hands-on)
Difficulty: ⭐⭐⭐
Type: Concept + Implementation
Prerequisites: Chapter 26 (Introduction to Agents)
Builds Toward: OTAR Loop (Ch 28), Multi-Agent Systems (Ch 35)
Correctness Properties: P36 (Reasoning Trace), P37 (Action Validity)
Project Thread: Cognitive Architecture

NAVIGATION
→ Quick Reference: #quick-reference-card
→ Verification: #verification-required-section
→ What's Next: #whats-next
-->

---

## ☕ Coffee Shop Intro

Let's talk about the difference between a genius who stays silent and a genius who explains their work.

Imagine you're watching a cooking competition.
**Chef A** works in total silence. They chop, sear, and plate. You have no idea _why_ they added vinegar to the sauce. It tastes good, but you can't learn from them, and if something burns, you don't know when things went wrong.
**Chef B** narrates everything. _"The pan is too hot, so I'm moving it off the heat. The sauce is too sweet, so I'm adding vinegar to balance it. Now I'm resting the meat so the juices redistribute."_

**ReAct (Reason + Act)** is the technique of forcing our AI Agents to be like **Chef B**.

Instead of just treating the AI like a magical black box that spits out answers, we force it to maintain an **Internal Monologue**. We make it "think out loud" before it touches any tools.

_"Thought: The user is asking about the weather. I should check the location first. Action: Use Location Tool."_

By the end of this chapter, you won't just be building agents; you'll be reading their minds. You'll see the exact moment they get confused, the moment they have an "Aha!" realization, and the logic behind every decision they make. It's like having a debugger for the AI's brain. 🧠

---

## Prerequisites Check

We're stepping into intermediate territory here. You need your LangChain environment ready.

✅ **LangChain Installation**:

```bash
pip install langchain langchain-openai langchain-community
```

✅ **API Keys**:
Ensure your `.env` file has your `OPENAI_API_KEY`.

✅ **Mental Model**:
You should remember from Chapter 26 that an Agent is just an LLM with access to Tools. Today, we change _how_ it uses those tools.

---

## The Story: The "Black Box" Problem

### The Problem: Invisible Logic

In the previous chapter, we built a simple agent that could call functions. It worked, but it felt a bit like magic. You asked a question, and _poof_, the answer appeared.

But what happens when it breaks?

Imagine you ask: _"Who is the CEO of the company that made the iPhone?"_
The agent fails. Why?

- Did it fail to search for "iPhone maker"?
- Did it find "Apple" but fail to search for "Apple CEO"?
- Did it find the CEO's name but fail to print it?

Without an internal monologue, you are flying blind. You have no idea where the chain of logic snapped.

### The Solution: The ReAct Trace

ReAct (Reasoning + Acting) imposes a strict structure on the AI's behavior. It forces the AI to follow this loop:

1.  **Thought**: Analyze the situation. _"I need to find out who made the iPhone."_
2.  **Action**: Choose a tool. _"Search: iPhone manufacturer."_
3.  **Observation**: Read the result. _"Result: Apple Inc."_
4.  **Thought**: Update the plan. _"Okay, now I need to find the CEO of Apple."_
5.  **Action**: Choose a tool. _"Search: Apple CEO."_
6.  **Observation**: Read the result. _"Result: Tim Cook."_
7.  **Final Answer**: deliver the result. _"The CEO is Tim Cook."_

This **Trace** tells you exactly what happened. If it fails at step 2, you know exactly why.

---

## Part 1: The ReAct Prompt 📜

The engine of a ReAct agent is the **Prompt**. It's not code; it's a set of English instructions that tells the LLM the rules of the game.

### 🔬 Try This! (Hands-On Practice #1)

Let's pull the actual prompt used by thousands of production agents and inspect it.

**Create `inspect_prompt.py`**:

```python
from langchain import hub

# 1. Pull the standard prompt from LangChain Hub
# "hwchase17/react" is the gold standard ReAct prompt
prompt = hub.pull("hwchase17/react")

# 2. Print it to the console
print("\n--- THE RE-ACT PROMPT ---\n")
print(prompt.template)
```

**Run it.** Read the output carefully. You'll see instructions like:

> "Answer the following questions as best you can. You have access to the following tools..."
> "Use the following format:"
> "Question: the input question you must answer"
> "Thought: you should always think about what to do"
> "Action: the action to take..."

**Key Insight**: We aren't programming the logic in Python. We are programming the logic in _English_, and the LLM is executing it. The `Thought:` keyword triggers the internal monologue.

---

## Part 2: Building a ReAct Agent 🤖

Now let's build an agent that uses this trace to solve a multi-step problem.

We'll give it a simple tool: a "Character Counter." Then we'll ask it a trick question that requires it to _think_ before it counts.

### 🔬 Try This! (Hands-On Practice #2)

**Create `react_agent.py`**:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain import hub
from dotenv import load_dotenv

load_dotenv()

# 1. Define our Tool
# The docstring is CRITICAL. The Agent reads this to know WHEN to use the tool.
@tool
def get_length(text: str) -> int:
    """Returns the length of a text string in characters."""
    print(f"   (🛠️ Tool called: Counting chars in '{text}')")
    # Clean the input to avoid invisible spaces affecting the count
    return len(text.strip())

# List of tools available to the agent
tools = [get_length]

# 2. Setup the Brain (LLM) + The Instructions (Prompt)
# We use temperature=0 to make the reasoning precise and consistent.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = hub.pull("hwchase17/react")

# 3. Construct the Agent
# This combines the Brain, the Tools, and the Instructions.
agent = create_react_agent(model, tools, prompt)

# 4. Create the Executor
# The Executor is the runtime loop that actually calls the agent,
# executes the tools, and feeds the output back to the agent.
# verbose=True is the key! It lets us see the ReAct trace.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Run the Scenario
print("--- 🕵️ Running ReAct Agent ---")
query = "How many characters are in the word 'Supercalifragilistic'?"
agent_executor.invoke({"input": query})
```

**Run it.**

Watch the output. It's mesmerizing.

```text
> Entering new AgentExecutor chain...
I need to count the characters in the word provided.
Action: get_length
Action Input: 'Supercalifragilistic'
   (🛠️ Tool called: Counting chars in 'Supercalifragilistic')
Observation: 20
I have the count.
Final Answer: 20
> Finished chain.
```

**What just happened?**

1.  **Thought**: It realized "I can't just guess. I have a tool."
2.  **Action**: It formulated the correct syntax to call `get_length`.
3.  **Observation**: It received `20` from our Python function.
4.  **Final Answer**: It translated that result back to the user.

---

## Part 3: Debugging Logic (Why did it do that?) 🐞

The real power of ReAct comes when things go wrong.

Imagine you ask: _"What is the weather?"_

If you ran this against our agent (which _only_ has a length-counting tool), here is what the trace would look like:

```text
Thought: I need to check the weather.
Action: WeatherTool ??
Observation: Tool 'WeatherTool' not found.
Thought: Oh, I don't have a weather tool. I only have get_length.
Final Answer: I apologize, but I cannot check the weather. I can only count characters.
```

**Without ReAct**, an LLM might simply hallucinate: _"It's 72 degrees and sunny!"_ because it wants to be helpful.
**With ReAct**, it looks for a tool, fails to find it, and honestly reports the limitation.

### 🔬 Try This! (Hands-On Practice #3)

Modify `react_agent.py` to ask a question it _can't_ answer.

```python
# Change the input
query = "What is the square root of 144?"
agent_executor.invoke({"input": query})
```

**Watch the struggle.**
It might try to use `get_length` on "144".
It might say "I don't have a math tool."
It might calculate it in its head (because LLMs know basic math).

Reading the trace tells you exactly _how_ it solved it. Did it cheat and do mental math? Or did it hallucinate a tool? **ReAct gives you visibility.**

---

## Common Mistakes to Avoid 🚫

### Mistake #1: Weak Tool Descriptions

**The Mistake**: `@tool def func(x): pass` without a docstring.
**Why it matters**: The agent reads the docstring to decide _if_ and _how_ to use the tool. If you don't describe it, the agent won't use it.
**The Fix**: Always write detailed docstrings: `"""Use this tool to calculate X given Y..."""`

### Mistake #2: Parsing Errors

**The Mistake**: The agent outputs `Action: ToolName` but forgets the `Action Input:`.
**Why it matters**: The `AgentExecutor` regex parser will fail and crash.
**The Fix**: Use robust models (GPT-3.5 or GPT-4). Smaller models (Llama-7b) often struggle to follow the strict formatting rules of ReAct.

### Mistake #3: Infinite Loops

**The Mistake**: The agent keeps trying the same failed action over and over.
**The Fix**: Set `max_iterations=5` in the `AgentExecutor`. This kills the process if it spins in circles too long.

---

## Quick Reference Card 🃏

### The 5 Steps of ReAct

1.  **Thought**: The internal monologue ("What do I do next?")
2.  **Action**: The decision to use a specific tool.
3.  **Action Input**: The arguments passed to that tool.
4.  **Observation**: The output returned by the tool (invisible to the user, visible to the agent).
5.  **Final Answer**: The response given to the human.

---

## Verification (REQUIRED SECTION) 🧪

We need to verify **Properties P36 (Trace Completeness)**. A working ReAct agent _must_ produce a thought before acting.

**Create `verify_react.py`**:

```python
"""
Verification script for Chapter 27.
Property P36: Reasoning Trace.
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain import hub
# We use this to intercept the log output programmatically
from langchain_core.callbacks import BaseCallbackHandler
import sys

print("🧪 Running ReAct Verification...\n")

# 1. Setup a dummy tool
@tool
def magic_number_tool(x: str) -> int:
    """Returns the magic number 42."""
    return 42

tools = [magic_number_tool]
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(model, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 2. Setup a Callback to capture the "Thoughts"
class TraceCallback(BaseCallbackHandler):
    def __init__(self):
        self.thoughts = []

    def on_agent_action(self, action, **kwargs):
        # This captures the "log" (the text generated by the agent)
        self.thoughts.append(action.log)

tracer = TraceCallback()

# 3. Run the Agent
print("Test 1: Analyzing Trace...")
res = executor.invoke(
    {"input": "What is the magic number?"},
    config={"callbacks": [tracer]}
)

# 4. Verify the Trace
trace_log = "".join(tracer.thoughts)
print(f"\nCaptured Trace Fragment: {trace_log[:50]}...")

if "Thought" in trace_log and "Action" in trace_log:
    print("✅ P36 Passed: Agent produced a reasoning trace.")
else:
    print(f"❌ Failed: No trace found. The agent acted without thinking!")
    sys.exit(1)

# 5. Verify the Result
if "42" in res['output']:
    print("✅ Result Correct.")
else:
    print(f"❌ Failed result: {res['output']}")
    sys.exit(1)

print("\n🎉 Chapter 27 Complete! You can see the matrix code.")
```

**Run it:** `python verify_react.py`

---

## Summary

We've fundamentally changed how we interact with AI.

- **Before ReAct**: Inputs went in, outputs came out. It was a black box.
- **After ReAct**: We see the _Thinking Process_. We see the _Action Selection_. We see the _Observations_.

**What you learned:**

1.  ✅ **ReAct**: The loop of Reasoning and Acting.
2.  ✅ **Transparency**: Why seeing the "Thought" is critical for debugging.
3.  ✅ **Model Agnostic**: How to make agents work with almost any model.
4.  ✅ **Tracing**: Catching the agent in the act.

**Looking ahead**:
We have an agent that can reason. But what if it makes a mistake? What if it tries a tool and fails? Right now, it might just give up.
In **Chapter 28**, we will upgrade loops to the **OTAR Pattern** (Observe, Think, Act, Reflect), teaching our agents to learn from their own mistakes in real-time! 🚀

---

**Next**: [Chapter 28: OTAR Loop Pattern →](chapter-28-otar-loop.md)
