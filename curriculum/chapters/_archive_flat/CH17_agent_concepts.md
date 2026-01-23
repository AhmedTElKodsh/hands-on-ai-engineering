# Chapter 17: What Are Agents?

**Difficulty:** Intermediate  
**Time:** 1 hour  
**Prerequisites:** Chapters 13-16  
**AITEA Component:** Conceptual foundation for `src/agents/`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Define what an AI agent is and isn't
2. Distinguish agents from chatbots and workflows
3. Understand the core components of an agent
4. Identify when to use agents vs simpler approaches
5. Describe the agent landscape (frameworks and patterns)

## 17.1 Agents vs Chatbots vs Workflows

**Chatbot**: Responds to messages, no persistent state or actions

```
User: "What's the weather?"
Bot: "I don't have access to weather data."
```

**Workflow**: Fixed sequence of steps, deterministic

```
1. Parse input → 2. Query database → 3. Format response
```

**Agent**: Autonomous decision-making, can use tools, adapts to context

```
User: "What's the weather?"
Agent: [Thinks] I need weather data. I'll use the weather_api tool.
       [Acts] weather_api(location="user_location")
       [Observes] Result: 72°F, sunny
       [Responds] "It's 72°F and sunny!"
```

## 17.2 The Agent Definition

An **agent** is a system that:

1. **Perceives** its environment (user input, tool results, context)
2. **Reasons** about what to do next
3. **Acts** by calling tools or generating responses
4. **Learns** from feedback (within session or across sessions)

```
┌─────────────────────────────────────────────────────┐
│                      AGENT                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐        │
│  │ Observe │ → │  Think  │ → │   Act   │         │
│  └─────────┘    └─────────┘    └─────────┘        │
│       ↑                              │             │
│       └──────────────────────────────┘             │
│                   Reflect                          │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │                  MEMORY                      │  │
│  │  Short-term │ Long-term │ Summarization     │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │                  TOOLS                       │  │
│  │  search │ calculate │ api_call │ database   │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 17.3 Core Agent Components

### 1. The Brain (LLM)

The reasoning engine that decides what to do:

```python
# The LLM analyzes the situation and decides
response = await llm.complete("""
Given the user's request and available tools,
what should I do next?

User request: {request}
Available tools: {tools}
Previous actions: {history}
""")
```

### 2. Tools

Functions the agent can call:

```python
tools = {
    "search_features": search_features_tool,
    "add_feature": add_feature_tool,
    "estimate_project": estimate_project_tool,
}
```

### 3. Memory

Context retention across interactions:

```python
# Short-term: Recent conversation
short_term = ["User asked about CRUD", "I searched features", "Found 3 matches"]

# Long-term: Persistent knowledge
long_term = {"user_preferences": {"team": "backend"}}
```

### 4. Planning

Strategy for achieving goals:

```python
# ReAct pattern: Reason → Act → Observe
plan = [
    "1. Search for similar features",
    "2. Get historical time data",
    "3. Calculate estimate",
    "4. Present results with confidence"
]
```

## 17.4 When to Use Agents

**Use agents when:**

- Tasks require multiple steps with decisions
- The path to solution isn't predetermined
- Tools need to be selected dynamically
- Context from previous steps affects next steps

**Use simpler approaches when:**

- Task is straightforward (single API call)
- Steps are always the same (workflow)
- No tool selection needed (chatbot)
- Latency is critical (agents are slower)

| Scenario                                 | Best Approach       |
| ---------------------------------------- | ------------------- |
| "What's 2+2?"                            | Direct LLM response |
| "Summarize this document"                | Single LLM call     |
| "Process these 100 invoices"             | Workflow/pipeline   |
| "Research competitors and create report" | Agent               |
| "Help me debug this code"                | Agent with tools    |

## 17.5 The Agent Landscape

### From-Scratch (This Course)

Build agents to understand fundamentals:

- SimpleAgent with OTAR loop
- ToolRegistry for tool management
- Memory classes for context

### LangChain/LangGraph

Agent engineering platform:

- High-level agent APIs
- LangGraph for orchestration
- LangSmith for observability

### LlamaIndex

Knowledge-powered agents:

- Agents with RAG as tools
- Event-driven workflows
- Production deployment

### Other Frameworks

- **CrewAI**: Multi-agent teams
- **AutoGen**: Conversational agents
- **Strands**: AWS Bedrock integration

## 17.6 AITEA Agent Use Cases

AITEA uses agents for:

1. **BRD Parsing Agent**

   - Reads business requirements document
   - Extracts features iteratively
   - Asks clarifying questions
   - Produces structured feature list

2. **Estimation Agent**

   - Searches feature library
   - Retrieves historical data
   - Calculates statistics
   - Provides confidence-rated estimates

3. **Project Planning Agent**
   - Analyzes project scope
   - Identifies dependencies
   - Suggests team allocation
   - Creates timeline

## 17.7 Your Turn: Exercise 17.1

Identify whether each scenario needs an agent:

1. "Convert this CSV to JSON" → \_\_\_
2. "Find all bugs in this codebase and fix them" → \_\_\_
3. "What's the capital of France?" → \_\_\_
4. "Help me plan a 2-week sprint" → \_\_\_
5. "Send an email to the team" → \_\_\_

<details>
<summary>Answers</summary>

1. **Workflow** - Fixed transformation, no decisions
2. **Agent** - Multiple steps, tool use, decisions about fixes
3. **Direct response** - Simple factual question
4. **Agent** - Requires analysis, multiple tools, iterative refinement
5. **Workflow** - Single action, no decisions (unless composing the email)

</details>

## 17.8 Quick Check Questions

1. What distinguishes an agent from a chatbot?
2. Name the four core components of an agent.
3. When should you NOT use an agent?
4. What is the OTAR loop?
5. Why do agents need memory?

<details>
<summary>Answers</summary>

1. Agents can use tools, make decisions, and take actions; chatbots just respond
2. Brain (LLM), Tools, Memory, Planning
3. When tasks are simple, deterministic, or latency-critical
4. Observe-Think-Act-Reflect - the agent's decision loop
5. To maintain context across steps and learn from previous interactions

</details>

## 17.9 The Agent Mental Model

Think of an agent like a skilled employee:

```
┌─────────────────────────────────────────────────────┐
│                 SKILLED EMPLOYEE                    │
│                                                     │
│  📋 Task: "Estimate the new project"               │
│                                                     │
│  🧠 Thinks: "I need to check similar past projects" │
│                                                     │
│  🔧 Uses tools:                                     │
│     - Searches project database                     │
│     - Pulls historical time data                    │
│     - Runs calculations                             │
│                                                     │
│  📝 Remembers:                                      │
│     - Client preferences                            │
│     - Past estimation accuracy                      │
│     - Team capabilities                             │
│                                                     │
│  ✅ Delivers: Detailed estimate with confidence    │
└─────────────────────────────────────────────────────┘
```

The agent does the same thing, but with:

- LLM as the "brain"
- Tool definitions as "skills"
- Memory systems as "experience"
- Prompts as "instructions"

## 17.10 AITEA Integration

This chapter provides the conceptual foundation for:

- **Requirement 5.1**: Understanding agent architecture
- **Phase 4**: Building agents from scratch

**Key Takeaways:**

- Agents are autonomous systems that perceive, reason, act, and learn
- They're more powerful than chatbots but more complex
- Use agents when tasks require dynamic decision-making
- AITEA uses agents for BRD parsing, estimation, and planning

## What's Next

In Chapter 18, you'll implement your first agent from scratch—a SimpleAgent with the Observe-Think-Act-Reflect loop.

**Before proceeding:**

- Review the agent components diagram
- Think about where agents fit in your projects
- Consider what tools your agents might need
