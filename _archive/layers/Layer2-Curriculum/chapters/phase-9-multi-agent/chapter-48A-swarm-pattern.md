# Chapter 48A: The Swarm Pattern — Self-Organizing Teams

<!--
METADATA
Phase: Phase 9: Multi-Agent Systems
Time: 1.5 hours (30 minutes reading + 60 minutes hands-on)
Difficulty: ⭐⭐⭐
Type: Concept + Implementation
Prerequisites: Chapter 43 (Multi-Agent Fundamentals)
Builds Toward: Chapter 54 (Complete System)
Correctness Properties: P86 (Handoff accuracy), P87 (Agent reachability)
-->

## ☕ Coffee Shop Intro: The Ant Colony

**Hierarchical Teams (Boss-Worker)**:
Like a construction site. The Foreman (Supervisor) tells Worker A to dig, Worker B to pour. If the Foreman gets sick, nothing happens.

**Swarm Teams (Peer-to-Peer)**:
Like an ant colony.
Ant A finds food. It doesn't call a manager. It just signals Ant B: "Help me carry this."
Ant B helps, then signals Ant C.

**The Swarm Pattern** is about agents handing off tasks to each other directly, without a central router. It's lightweight, fast, and great for educational prototyping.

---

## 🔍 The 3-Layer Dive

### Layer 1: The Monolith
One Agent with 50 tools.
*   **Problem**: Confused agent. "Should I search or calculate?"

### Layer 2: The Supervisor (Star Topology)
Supervisor decides who acts.
*   **Problem**: The Supervisor becomes a bottleneck.

### Layer 3: The Swarm (Mesh Topology)
Agent A does its job, then *returns* Agent B as the next step.
*   **Benefit**: Simple logic. "I'm done, over to you."
*   **Drawback**: Hard to visualize (Spaghetti logic).

---

## 🛠️ Implementation Guide: The Handoff

OpenAI released an educational library called `swarm`. We will implement the core pattern from scratch so you understand it (it's very simple!).

### Step 1: The Core Logic

The "Magic" of Swarm is that a function can return an `Agent`.

```python
# simple_swarm.py

class Agent:
    def __init__(self, name, instructions, functions):
        self.name = name
        self.instructions = instructions
        self.functions = functions

def run_swarm(starting_agent, user_query):
    current_agent = starting_agent
    messages = [{"role": "user", "content": user_query}]
    
    print(f"--- Starting with {current_agent.name} ---")
    
    while True:
        # In a real swarm, you'd call the LLM here.
        # The LLM would decide to call a 'handoff' function.
        # We will simulate the decision logic for clarity.
        
        print(f"🤖 {current_agent.name} is thinking...")
        
        # Simulated Logic:
        if current_agent.name == "Receptionist":
            print("   -> Handing off to TechSupport")
            current_agent = tech_agent
        elif current_agent.name == "TechSupport":
            print("   -> Solved the problem.")
            return "Issue Resolved"
            
        # Break infinite loops for safety
        break
```

### Step 2: Using the Real `swarm` Library (Conceptual)

If you install `pip install git+https://github.com/openai/swarm.git`, the code looks like this:

```python
from swarm import Swarm, Agent

client = Swarm()

def transfer_to_agent_b():
    return agent_b

agent_a = Agent(
    name="Agent A",
    instructions="You are a greeter. If the user asks for help, transfer to Agent B.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="You are a helper. Answer the question.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I need help!"}],
)

print(response.messages[-1]["content"])
```

### Step 3: A CE Application (The Document Pipeline)

Let's build a swarm for Civil Engineering:
1.  **Extractor**: Pulls data.
2.  **Analyzer**: Checks compliance.
3.  **Reporter**: Writes summary.

#### 🔬 Try This! (Hands-On Practice #1)

**Create `ce_swarm.py`**:

```python
# We will build a functional mini-swarm without external deps
# using the "Function returns Agent" pattern.

class Agent:
    def __init__(self, name, logic_func):
        self.name = name
        self.logic_func = logic_func

# 1. Define Agents
def extractor_logic(query):
    if "extract" in query:
        return "Extracted Data: [Bridge length 50m]", analyzer_agent
    return "I only extract.", None

def analyzer_logic(query):
    if "Bridge" in query:
        return "Analysis: Length 50m is compliant.", reporter_agent
    return "Analysis Failed.", None

def reporter_logic(query):
    return f"REPORT: {query}", None # None means done

# 2. Wire them up
# (Note: In Python, we can define the variable first then assign logic, 
# or use a class structure to handle forward references)
# We'll use a simple registry approach here.

extractor_agent = Agent("Extractor", extractor_logic)
analyzer_agent = Agent("Analyzer", analyzer_logic)
reporter_agent = Agent("Reporter", reporter_logic)

# 3. The Loop
def run_loop(agent, initial_data):
    current_agent = agent
    data = initial_data
    
    steps = 0
    while current_agent and steps < 5:
        print(f"👉 {current_agent.name} active with data: '{data}'")
        
        # Run agent logic
        result, next_agent = current_agent.logic_func(data)
        print(f"   Output: {result}")
        
        # Update state
        data = result
        current_agent = next_agent
        steps += 1
        
    print("✅ Done.")

# Run it
run_loop(extractor_agent, "Please extract data.")
```

**Run it**. Watch the baton pass from Extractor -> Analyzer -> Reporter.

---

## 🧪 Correctness Properties (Testing Handoffs)

| Property | Description |
|----------|-------------|
| **P86: Handoff Accuracy** | If Agent A calls `transfer_to_B`, the next active agent MUST be B. |
| **P87: Agent Reachability** | From the Entry Agent, there must be a path to the Termination Agent. |

### Hypothesis Test Example

```python
from hypothesis import given, strategies as st

def test_p86_handoff():
    """P86: Verify function return updates current_agent."""
    # Setup
    agent_a = "A"
    agent_b = "B"
    
    def handoff_func():
        return agent_b
        
    # Execution
    next_agent = handoff_func()
    
    # Verify
    assert next_agent == agent_b
```

---

## ✍️ Try This! (Hands-On Exercises)

### Exercise 1: The Router
Create a `Triage` agent that looks at keywords.
*   "Sales" -> Handoff to `SalesAgent`
*   "Support" -> Handoff to `SupportAgent`
*   Verify the routing works.

### Exercise 2: The Loop
Create two agents, `Ping` and `Pong`.
`Ping` hands off to `Pong`. `Pong` hands off to `Ping`.
Run the loop and ensure your runner has a `max_turns` limit to prevent infinite loops!

---

## ✅ Verification Script

Create `verify_ch48a.py`.

```python
"""
Verification script for Chapter 48A: Swarm Pattern
"""
import sys

print("🧪 Running Swarm Verification...\n")

# Mock Agent Class
class Agent:
    def __init__(self, name):
        self.name = name

# P86: Handoff Accuracy
print("Test 1: Handoff Mechanics...")
agent_b = Agent("B")

def handoff_tool():
    return agent_b

result = handoff_tool()

if result.name == "B":
    print("✅ P86 Passed: Handoff returned correct agent.")
else:
    print(f"❌ Failed: Expected B, got {result.name}")
    sys.exit(1)

# P87: Reachability (Simple simulation)
print("Test 2: Path Simulation...")
agent_a = Agent("A")
# Map: A -> B -> End
handoffs = {
    "A": agent_b,
    "B": None # End
}

current = agent_a
steps = 0
while current and steps < 5:
    current = handoffs.get(current.name)
    steps += 1

if current is None:
    print("✅ P87 Passed: Reached termination state.")
else:
    print("❌ Failed: Stuck in loop.")
    sys.exit(1)

print("\n🎉 Chapter 48A Complete! You have built a Swarm.")
```

---

## 📝 Summary & Key Takeaways

1.  **Swarm Pattern**: Agents hand off tasks directly to other agents.
2.  **No Central Router**: Unlike the Supervisor pattern, logic is distributed.
3.  **Functions return Agents**: The core mechanism is a tool that returns the next `Agent` object.
4.  **Simplicity**: Great for prototyping and learning agent interactions.
5.  **Production Caution**: Swarms are hard to debug (spaghetti flow). For production, prefer **LangGraph** (State Machines) where flows are explicit.

**Key Insight**: In a Swarm, the "State" is just the conversation history, and the "Router" is the current agent's tool choices.

---

## 🔜 What's Next?

We've covered Multi-Agent systems deeply. Now it's time to apply everything to the real world.
In **Chapter 49**, we begin the final phase: **Civil Engineering Application**. We will define the data models for Contracts and Reports.
