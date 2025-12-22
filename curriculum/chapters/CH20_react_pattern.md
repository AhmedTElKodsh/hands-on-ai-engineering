# Chapter 20: Planning Patterns (ReAct)

**Difficulty:** Advanced  
**Time:** 2.5 hours  
**Prerequisites:** Chapters 18-19  
**AITEA Component:** `src/agents/react_agent.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Understand the ReAct (Reasoning + Acting) pattern
2. Implement a ReAct agent from scratch
3. Parse and execute tool calls from LLM output
4. Handle multi-step reasoning chains
5. Compare ReAct with other planning patterns

## 20.1 What Is ReAct?

ReAct combines **Rea**soning and **Act**ing in an interleaved manner:

```
Question: What's the estimated time for a CRUD API?

Thought 1: I need to search for CRUD features in the library.
Action 1: search_features(query="CRUD")
Observation 1: Found: CRUD API (4h seed time, 3 historical entries)

Thought 2: I have historical data. Let me get the statistics.
Action 2: estimate_feature(feature_name="CRUD API")
Observation 2: Mean: 4.2h, Median: 4.0h, P80: 5.5h

Thought 3: I have enough data to provide an estimate.
Answer: The CRUD API is estimated at 4-5.5 hours (medium confidence).
```

## 20.2 ReAct vs Other Patterns

| Pattern               | Description                    | Best For                 |
| --------------------- | ------------------------------ | ------------------------ |
| **ReAct**             | Interleaved reasoning + action | General tasks, debugging |
| **Plan-then-Execute** | Create full plan, then execute | Well-defined tasks       |
| **Chain-of-Thought**  | Reasoning only, no actions     | Pure reasoning tasks     |
| **Tree-of-Thought**   | Explore multiple paths         | Complex decisions        |

## 20.3 The ReAct Prompt

```python
REACT_SYSTEM_PROMPT = """You are an AI assistant that solves tasks using the ReAct pattern.

For each step, you must output in this exact format:
Thought: [Your reasoning about what to do next]
Action: [tool_name(param1="value1", param2="value2")]

After receiving an observation, continue with another Thought/Action pair.
When you have enough information to answer, output:
Thought: [Final reasoning]
Answer: [Your final answer]

Available tools:
{tools}

Rules:
1. Always start with a Thought
2. Only call one Action per step
3. Wait for Observation before next Thought
4. Use Answer only when you're confident in the result
"""
```

## 20.4 Implementing ReAct Agent

```python
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from src.services.llm import LLMProvider, ChatMessage
from src.services.tools import ToolRegistry


@dataclass
class ReActStep:
    """A single step in the ReAct chain."""
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    is_final: bool = False
    answer: Optional[str] = None


class ReActAgent:
    """Agent implementing the ReAct pattern.

    Example:
        >>> agent = ReActAgent(llm=MockLLM(), registry=create_aitea_registry())
        >>> result = await agent.run("Estimate time for user authentication")
        >>> print(result.answer)
    """

    def __init__(
        self,
        llm: LLMProvider,
        registry: ToolRegistry,
        max_steps: int = 10,
    ):
        self.llm = llm
        self.registry = registry
        self.max_steps = max_steps
        self.steps: List[ReActStep] = []

    def _build_system_prompt(self) -> str:
        """Build system prompt with tool descriptions."""
        tools_desc = self.registry.get_tool_descriptions()
        return REACT_SYSTEM_PROMPT.format(tools=tools_desc)

    def _build_conversation(self, question: str) -> List[ChatMessage]:
        """Build conversation history."""
        messages = [
            ChatMessage(role="system", content=self._build_system_prompt()),
            ChatMessage(role="user", content=f"Question: {question}"),
        ]

        # Add previous steps
        for step in self.steps:
            # Add assistant's thought/action
            content = f"Thought: {step.thought}"
            if step.action:
                content += f"\nAction: {step.action}({self._format_args(step.action_input)})"
            if step.is_final:
                content += f"\nAnswer: {step.answer}"
            messages.append(ChatMessage(role="assistant", content=content))

            # Add observation
            if step.observation:
                messages.append(ChatMessage(
                    role="user",
                    content=f"Observation: {step.observation}"
                ))

        return messages

    def _format_args(self, args: Optional[Dict[str, Any]]) -> str:
        """Format arguments for display."""
        if not args:
            return ""
        return ", ".join(f'{k}="{v}"' for k, v in args.items())

    def _parse_response(self, response: str) -> ReActStep:
        """Parse LLM response into a ReActStep."""
        step = ReActStep(thought="")

        # Extract Thought
        thought_match = re.search(r'Thought:\s*(.+?)(?=Action:|Answer:|$)', response, re.DOTALL)
        if thought_match:
            step.thought = thought_match.group(1).strip()

        # Check for Answer (final step)
        answer_match = re.search(r'Answer:\s*(.+?)$', response, re.DOTALL)
        if answer_match:
            step.is_final = True
            step.answer = answer_match.group(1).strip()
            return step

        # Extract Action
        action_match = re.search(r'Action:\s*(\w+)\(([^)]*)\)', response)
        if action_match:
            step.action = action_match.group(1)
            args_str = action_match.group(2)
            step.action_input = self._parse_args(args_str)

        return step

    def _parse_args(self, args_str: str) -> Dict[str, Any]:
        """Parse action arguments."""
        args = {}
        if not args_str.strip():
            return args

        # Match key="value" or key=value patterns
        pattern = r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
        for match in re.finditer(pattern, args_str):
            key = match.group(1)
            value = match.group(2) or match.group(3) or match.group(4)

            # Try to convert to appropriate type
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass

            args[key] = value

        return args

    async def _execute_action(self, action: str, args: Dict[str, Any]) -> str:
        """Execute a tool action."""
        # Validate
        errors = self.registry.validate_tool_call(action, args)
        if errors:
            return f"Error: {', '.join(errors)}"

        # Get tool
        tool = self.registry.get(action)
        if not tool:
            return f"Error: Unknown tool '{action}'"

        # Execute handler if available
        if tool.handler:
            try:
                result = tool.handler(**args)
                if hasattr(result, '__await__'):
                    result = await result
                return str(result)
            except Exception as e:
                return f"Error executing {action}: {e}"

        # Mock execution for tools without handlers
        return f"Executed {action} with {args}"

    async def run(self, question: str) -> ReActStep:
        """Run the ReAct loop until answer or max steps."""
        self.steps = []

        for step_num in range(self.max_steps):
            # Build conversation and get response
            messages = self._build_conversation(question)
            response = await self.llm.chat(messages)

            # Parse response
            step = self._parse_response(response)

            # If final answer, we're done
            if step.is_final:
                self.steps.append(step)
                return step

            # Execute action if present
            if step.action:
                observation = await self._execute_action(
                    step.action,
                    step.action_input or {}
                )
                step.observation = observation

            self.steps.append(step)

        # Max steps reached
        final_step = ReActStep(
            thought="Maximum steps reached",
            is_final=True,
            answer="Could not complete task within step limit"
        )
        self.steps.append(final_step)
        return final_step

    def get_trace(self) -> str:
        """Get formatted trace of all steps."""
        lines = []
        for i, step in enumerate(self.steps, 1):
            lines.append(f"Step {i}:")
            lines.append(f"  Thought: {step.thought}")
            if step.action:
                lines.append(f"  Action: {step.action}({self._format_args(step.action_input)})")
            if step.observation:
                lines.append(f"  Observation: {step.observation}")
            if step.is_final:
                lines.append(f"  Answer: {step.answer}")
            lines.append("")
        return "\n".join(lines)
```

## 20.5 Using the ReAct Agent

```python
import asyncio
from src.services.llm import get_llm_provider
from src.services.tools import create_aitea_registry


async def main():
    llm = get_llm_provider()
    registry = create_aitea_registry()

    agent = ReActAgent(llm=llm, registry=registry, max_steps=5)

    result = await agent.run("What's the estimated time for a CRUD API feature?")

    print("=== ReAct Trace ===")
    print(agent.get_trace())

    print("=== Final Answer ===")
    print(result.answer)


asyncio.run(main())
```

## 20.6 Your Turn: Exercise 20.1

Add step-by-step streaming to the ReAct agent:

```python
class StreamingReActAgent(ReActAgent):
    """ReAct agent with streaming output."""

    async def run_streaming(self, question: str):
        """Yield steps as they happen."""
        self.steps = []

        for step_num in range(self.max_steps):
            yield {"type": "thinking", "step": step_num + 1}

            messages = self._build_conversation(question)
            response = await self.llm.chat(messages)
            step = self._parse_response(response)

            yield {"type": "thought", "content": step.thought}

            if step.is_final:
                yield {"type": "answer", "content": step.answer}
                self.steps.append(step)
                return

            if step.action:
                yield {"type": "action", "tool": step.action, "args": step.action_input}

                observation = await self._execute_action(step.action, step.action_input or {})
                step.observation = observation

                yield {"type": "observation", "content": observation}

            self.steps.append(step)

        yield {"type": "error", "content": "Max steps reached"}


# Usage
async def demo():
    agent = StreamingReActAgent(llm=MockLLM(), registry=create_aitea_registry())

    async for event in agent.run_streaming("Estimate CRUD feature"):
        if event["type"] == "thought":
            print(f"💭 {event['content']}")
        elif event["type"] == "action":
            print(f"🔧 {event['tool']}({event['args']})")
        elif event["type"] == "observation":
            print(f"👁️ {event['content']}")
        elif event["type"] == "answer":
            print(f"✅ {event['content']}")
```

## 20.7 Debugging Scenario

**The Bug:** Agent loops without making progress.

```
Step 1: Thought: I need to search for features
        Action: search_features(query="CRUD")
        Observation: Found 3 features

Step 2: Thought: I need to search for features  # Same thought!
        Action: search_features(query="CRUD")   # Same action!
        ...
```

**The Problem:** LLM isn't seeing previous observations properly.

**The Fix:** Ensure conversation history includes observations:

```python
def _build_conversation(self, question: str) -> List[ChatMessage]:
    messages = [...]

    for step in self.steps:
        # Include the full step including observation
        content = f"Thought: {step.thought}"
        if step.action:
            content += f"\nAction: {step.action}(...)"
        messages.append(ChatMessage(role="assistant", content=content))

        # CRITICAL: Include observation as user message
        if step.observation:
            messages.append(ChatMessage(
                role="user",
                content=f"Observation: {step.observation}\n\nContinue with your next thought."
            ))

    return messages
```

## 20.8 Quick Check Questions

1. What does ReAct stand for?
2. What's the format of a ReAct step?
3. When does the ReAct loop terminate?
4. How is ReAct different from Plan-then-Execute?
5. Why include observations in conversation history?

<details>
<summary>Answers</summary>

1. Reasoning + Acting
2. Thought → Action → Observation (or Thought → Answer for final step)
3. When the LLM outputs an Answer or max_steps is reached
4. ReAct interleaves reasoning and acting; Plan-then-Execute creates full plan first
5. So the LLM knows what happened and can reason about next steps

</details>

## 20.9 Mini-Project: ReAct with Backtracking

Add ability to reconsider previous decisions:

```python
class BacktrackingReActAgent(ReActAgent):
    """ReAct agent that can backtrack on errors."""

    async def run(self, question: str) -> ReActStep:
        self.steps = []
        backtrack_count = 0
        max_backtracks = 2

        for step_num in range(self.max_steps):
            messages = self._build_conversation(question)
            response = await self.llm.chat(messages)
            step = self._parse_response(response)

            if step.is_final:
                self.steps.append(step)
                return step

            if step.action:
                observation = await self._execute_action(
                    step.action, step.action_input or {}
                )

                # Check for errors
                if observation.startswith("Error:") and backtrack_count < max_backtracks:
                    # Add error context and let agent reconsider
                    step.observation = f"{observation}\n\nPlease reconsider your approach."
                    backtrack_count += 1
                else:
                    step.observation = observation

            self.steps.append(step)

        return ReActStep(
            thought="Max steps reached",
            is_final=True,
            answer="Could not complete"
        )
```

## 20.10 AITEA Integration

This chapter implements:

- **Requirement 5.4**: ReActAgent implementing reasoning and acting
- ReAct pattern for AITEA estimation tasks

**Verification:**

```python
import asyncio
from src.services.llm import get_llm_provider
from src.services.tools import create_aitea_registry


async def test_react():
    llm = get_llm_provider("mock", show_warning=False)
    registry = create_aitea_registry()

    # Add mock handlers
    def mock_search(query, **kwargs):
        return f"Found features matching '{query}': CRUD API (4h), Auth (8h)"

    def mock_estimate(feature_name, **kwargs):
        return f"Estimate for {feature_name}: 4-6 hours (medium confidence)"

    registry.get("search_features").handler = mock_search
    registry.get("estimate_feature").handler = mock_estimate

    agent = ReActAgent(llm=llm, registry=registry, max_steps=5)
    result = await agent.run("Estimate time for CRUD API")

    print("Trace:")
    print(agent.get_trace())

    print(f"Steps taken: {len(agent.steps)}")
    print(f"Final answer: {result.answer}")


asyncio.run(test_react())
```

## What's Next

In Chapter 21, you'll implement memory patterns—short-term, long-term, and summarization memory for agents.

**Before proceeding:**

- Run the ReAct agent with different questions
- Experiment with max_steps
- Try the streaming and backtracking extensions
