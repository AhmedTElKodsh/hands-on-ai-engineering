# Chapter 18: Agent Loop from Scratch

**Difficulty:** Advanced  
**Time:** 3 hours  
**Prerequisites:** Chapters 13-17  
**AITEA Component:** `src/agents/simple_agent.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Implement the Observe-Think-Act-Reflect (OTAR) loop
2. Create a state machine for agent execution
3. Track state transitions for debugging
4. Build an AgentContext for maintaining state
5. Handle errors and termination conditions

## 18.1 The OTAR Loop

Every agent iteration follows four phases:

```
┌─────────────────────────────────────────────────────┐
│                    OTAR LOOP                        │
│                                                     │
│    ┌──────────┐                                    │
│    │  OBSERVE │ ← Gather information               │
│    └────┬─────┘                                    │
│         ↓                                          │
│    ┌──────────┐                                    │
│    │  THINK   │ ← Analyze and plan                 │
│    └────┬─────┘                                    │
│         ↓                                          │
│    ┌──────────┐                                    │
│    │   ACT    │ ← Execute action                   │
│    └────┬─────┘                                    │
│         ↓                                          │
│    ┌──────────┐                                    │
│    │ REFLECT  │ ← Evaluate outcome                 │
│    └────┬─────┘                                    │
│         │                                          │
│         ↓                                          │
│    Continue? ──Yes──→ Back to OBSERVE              │
│         │                                          │
│         No                                         │
│         ↓                                          │
│    ┌──────────┐                                    │
│    │ COMPLETE │                                    │
│    └──────────┘                                    │
└─────────────────────────────────────────────────────┘
```

## 18.2 Agent States

Define the possible states:

```python
from enum import Enum, auto


class AgentState(Enum):
    """States in the OTAR loop."""
    IDLE = auto()      # Initial state
    OBSERVE = auto()   # Gathering information
    THINK = auto()     # Analyzing and planning
    ACT = auto()       # Executing action
    REFLECT = auto()   # Evaluating outcome
    COMPLETE = auto()  # Task finished
    ERROR = auto()     # Error occurred
```

## 18.3 State Transitions

Define valid transitions:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class AgentTransition:
    """Record of a state transition."""
    from_state: AgentState
    to_state: AgentState
    timestamp: datetime = field(default_factory=datetime.now)
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

    def __str__(self) -> str:
        msg = f"{self.from_state.name} → {self.to_state.name}"
        if self.message:
            msg += f": {self.message}"
        return msg


# Valid state transitions
VALID_TRANSITIONS: Dict[AgentState, List[AgentState]] = {
    AgentState.IDLE: [AgentState.OBSERVE, AgentState.ERROR],
    AgentState.OBSERVE: [AgentState.THINK, AgentState.ERROR],
    AgentState.THINK: [AgentState.ACT, AgentState.ERROR],
    AgentState.ACT: [AgentState.REFLECT, AgentState.ERROR],
    AgentState.REFLECT: [AgentState.OBSERVE, AgentState.COMPLETE, AgentState.ERROR],
    AgentState.COMPLETE: [],  # Terminal
    AgentState.ERROR: [],     # Terminal
}
```

## 18.4 Agent Context

Maintain state across the loop:

```python
@dataclass
class AgentContext:
    """Context maintained throughout agent execution."""
    task: str
    observations: List[str] = field(default_factory=list)
    thoughts: List[str] = field(default_factory=list)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)
    iteration: int = 0
    max_iterations: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_observation(self, observation: str) -> None:
        self.observations.append(observation)

    def add_thought(self, thought: str) -> None:
        self.thoughts.append(thought)

    def add_action(self, action: Dict[str, Any]) -> None:
        self.actions.append(action)

    def add_reflection(self, reflection: str) -> None:
        self.reflections.append(reflection)

    def increment_iteration(self) -> None:
        self.iteration += 1

    def should_continue(self) -> bool:
        return self.iteration < self.max_iterations
```

## 18.5 The SimpleAgent Class

```python
import logging
from typing import Callable, Optional

from src.services.llm import LLMProvider


logger = logging.getLogger(__name__)


class SimpleAgent:
    """Agent implementing the OTAR loop.

    Example:
        >>> from src.services.llm import MockLLM
        >>> agent = SimpleAgent(llm=MockLLM())
        >>> result = await agent.run("Estimate time for CRUD API")
        >>> print(agent.transitions)  # See state history
    """

    def __init__(
        self,
        llm: LLMProvider,
        max_iterations: int = 5,
        on_transition: Optional[Callable[[AgentTransition], None]] = None,
    ) -> None:
        self.llm = llm
        self.max_iterations = max_iterations
        self.on_transition = on_transition

        self._state = AgentState.IDLE
        self._transitions: List[AgentTransition] = []
        self._context: Optional[AgentContext] = None

    @property
    def state(self) -> AgentState:
        return self._state

    @property
    def transitions(self) -> List[AgentTransition]:
        return self._transitions.copy()

    @property
    def context(self) -> Optional[AgentContext]:
        return self._context

    def _transition_to(
        self,
        new_state: AgentState,
        data: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
    ) -> None:
        """Transition to a new state with validation."""
        valid_next = VALID_TRANSITIONS.get(self._state, [])

        if new_state not in valid_next:
            raise ValueError(
                f"Invalid transition: {self._state.name} → {new_state.name}. "
                f"Valid: {[s.name for s in valid_next]}"
            )

        transition = AgentTransition(
            from_state=self._state,
            to_state=new_state,
            data=data,
            message=message,
        )

        logger.info(f"Agent transition: {transition}")

        self._state = new_state
        self._transitions.append(transition)

        if self.on_transition:
            self.on_transition(transition)

    async def _observe(self) -> str:
        """OBSERVE: Gather information."""
        self._transition_to(AgentState.OBSERVE, message="Gathering information")

        prompt = f"""You are in the OBSERVE phase.
Task: {self._context.task}
Iteration: {self._context.iteration + 1}/{self._context.max_iterations}
Previous observations: {self._context.observations or 'None'}
Previous actions: {self._context.actions or 'None'}

What do you observe about this task?"""

        observation = await self.llm.complete(prompt)
        self._context.add_observation(observation)
        return observation

    async def _think(self) -> str:
        """THINK: Analyze and plan."""
        self._transition_to(AgentState.THINK, message="Analyzing and planning")

        latest_obs = self._context.observations[-1] if self._context.observations else "None"

        prompt = f"""You are in the THINK phase.
Task: {self._context.task}
Latest observation: {latest_obs}

Analyze the situation and decide what action to take."""

        thought = await self.llm.complete(prompt)
        self._context.add_thought(thought)
        return thought

    async def _act(self) -> Dict[str, Any]:
        """ACT: Execute the planned action."""
        self._transition_to(AgentState.ACT, message="Executing action")

        latest_thought = self._context.thoughts[-1] if self._context.thoughts else "None"

        prompt = f"""You are in the ACT phase.
Task: {self._context.task}
Your plan: {latest_thought}

Execute the action and provide the result."""

        result = await self.llm.complete(prompt)

        action = {
            "iteration": self._context.iteration,
            "plan": latest_thought,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }
        self._context.add_action(action)
        return action

    async def _reflect(self) -> tuple[str, bool]:
        """REFLECT: Evaluate outcome and decide to continue."""
        self._transition_to(AgentState.REFLECT, message="Evaluating outcome")

        latest_action = self._context.actions[-1] if self._context.actions else {}

        prompt = f"""You are in the REFLECT phase.
Task: {self._context.task}
Action result: {latest_action.get('result', 'None')}

Evaluate:
1. Was the action successful?
2. Is the task complete?
3. Should we continue?

End with "CONTINUE" or "COMPLETE"."""

        reflection = await self.llm.complete(prompt)
        self._context.add_reflection(reflection)

        should_complete = (
            "COMPLETE" in reflection.upper() or
            not self._context.should_continue()
        )

        return reflection, should_complete

    async def run(self, task: str) -> str:
        """Run the agent on a task."""
        # Initialize
        self._context = AgentContext(task=task, max_iterations=self.max_iterations)
        self._state = AgentState.IDLE
        self._transitions = []

        logger.info(f"Starting agent with task: {task}")

        try:
            while True:
                await self._observe()
                await self._think()
                await self._act()
                _, should_complete = await self._reflect()

                self._context.increment_iteration()

                if should_complete:
                    self._transition_to(AgentState.COMPLETE, message="Task completed")
                    break

            # Return final result
            if self._context.actions:
                return self._context.actions[-1].get("result", "No result")
            return "No actions taken"

        except Exception as e:
            logger.error(f"Agent error: {e}")
            self._transition_to(AgentState.ERROR, data={"error": str(e)})
            raise

    def get_state_history(self) -> List[AgentState]:
        """Get sequence of states."""
        states = [AgentState.IDLE]
        for t in self._transitions:
            states.append(t.to_state)
        return states

    def reset(self) -> None:
        """Reset agent to initial state."""
        self._state = AgentState.IDLE
        self._transitions = []
        self._context = None
```

## 18.6 Using the SimpleAgent

```python
import asyncio
from src.services.llm import get_llm_provider
from src.agents.simple_agent import SimpleAgent, AgentTransition


def on_transition(t: AgentTransition):
    """Callback for state transitions."""
    print(f"  [{t.from_state.name}] → [{t.to_state.name}]: {t.message}")


async def main():
    llm = get_llm_provider("mock", show_warning=False)

    agent = SimpleAgent(
        llm=llm,
        max_iterations=3,
        on_transition=on_transition
    )

    print("Starting agent...")
    result = await agent.run("Estimate time for a user authentication feature")

    print(f"\nFinal result: {result}")
    print(f"\nState history: {[s.name for s in agent.get_state_history()]}")
    print(f"Total iterations: {agent.context.iteration}")


asyncio.run(main())
```

## 18.7 Your Turn: Exercise 18.1

Add a `pause` capability to the agent:

```python
class PausableAgent(SimpleAgent):
    """Agent that can be paused and resumed."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._paused = False
        self._pause_after_state: Optional[AgentState] = None

    def pause_after(self, state: AgentState) -> None:
        """Pause after reaching the specified state."""
        self._pause_after_state = state

    def resume(self) -> None:
        """Resume execution."""
        self._paused = False

    def _transition_to(self, new_state: AgentState, **kwargs) -> None:
        super()._transition_to(new_state, **kwargs)

        if new_state == self._pause_after_state:
            self._paused = True
            # TODO: Implement pause logic
```

## 18.8 Debugging Scenario

**The Bug:** Agent loops forever without completing.

```python
agent = SimpleAgent(llm=MockLLM(), max_iterations=10)
result = await agent.run("Simple task")
# Never completes, hits max_iterations
```

**The Problem:** The LLM never outputs "COMPLETE" in reflections.

**The Fix:** Improve the reflection prompt or add explicit completion detection:

```python
async def _reflect(self) -> tuple[str, bool]:
    # ... existing code ...

    # Add explicit completion check
    task_keywords = ["done", "finished", "complete", "success"]
    reflection_lower = reflection.lower()

    explicit_complete = any(kw in reflection_lower for kw in task_keywords)
    max_reached = not self._context.should_continue()

    should_complete = explicit_complete or max_reached or "COMPLETE" in reflection.upper()

    return reflection, should_complete
```

## 18.9 Quick Check Questions

1. What are the four phases of the OTAR loop?
2. Why validate state transitions?
3. What does AgentContext store?
4. How does the agent decide to stop?
5. Why track transitions?

<details>
<summary>Answers</summary>

1. Observe, Think, Act, Reflect
2. To ensure the agent follows a valid execution path and catch bugs early
3. Task, observations, thoughts, actions, reflections, iteration count
4. When reflection contains "COMPLETE" or max_iterations is reached
5. For debugging, logging, and understanding agent behavior

</details>

## 18.10 Mini-Project: Streaming Agent

Create an agent that streams its thinking:

```python
class StreamingAgent(SimpleAgent):
    """Agent that streams its thought process."""

    async def run_streaming(self, task: str):
        """Run with streaming output."""
        self._context = AgentContext(task=task, max_iterations=self.max_iterations)
        self._state = AgentState.IDLE
        self._transitions = []

        while True:
            # Stream observe
            yield {"phase": "observe", "status": "starting"}
            observation = await self._observe()
            yield {"phase": "observe", "content": observation}

            # Stream think
            yield {"phase": "think", "status": "starting"}
            thought = await self._think()
            yield {"phase": "think", "content": thought}

            # Stream act
            yield {"phase": "act", "status": "starting"}
            action = await self._act()
            yield {"phase": "act", "content": action}

            # Stream reflect
            yield {"phase": "reflect", "status": "starting"}
            reflection, should_complete = await self._reflect()
            yield {"phase": "reflect", "content": reflection}

            self._context.increment_iteration()

            if should_complete:
                self._transition_to(AgentState.COMPLETE)
                yield {"phase": "complete", "result": action.get("result")}
                break


# Usage
async def main():
    agent = StreamingAgent(llm=MockLLM())

    async for event in agent.run_streaming("Estimate CRUD feature"):
        print(f"[{event['phase']}] {event.get('content', event.get('status', ''))[:50]}...")
```

## 18.11 AITEA Integration

This chapter implements:

- **Requirement 5.2**: SimpleAgent with OTAR loop
- **Property 8**: Agent Loop State Transitions

**Verification:**

```python
import asyncio
from src.agents.simple_agent import SimpleAgent, AgentState
from src.services.llm import get_llm_provider


async def test_agent():
    llm = get_llm_provider("mock", show_warning=False)
    agent = SimpleAgent(llm=llm, max_iterations=2)

    result = await agent.run("Test task")

    # Verify state transitions
    history = agent.get_state_history()
    print(f"State history: {[s.name for s in history]}")

    # Should follow: IDLE → OBSERVE → THINK → ACT → REFLECT → ...
    assert history[0] == AgentState.IDLE
    assert history[1] == AgentState.OBSERVE
    assert history[2] == AgentState.THINK
    assert history[3] == AgentState.ACT
    assert history[4] == AgentState.REFLECT

    print("✅ Agent loop verified")
    print(f"Iterations: {agent.context.iteration}")
    print(f"Observations: {len(agent.context.observations)}")


asyncio.run(test_agent())
```

## What's Next

In Chapter 19, you'll build a ToolRegistry that lets agents discover and use tools dynamically.

**Before proceeding:**

- Run the SimpleAgent with different tasks
- Experiment with max_iterations
- Try the streaming agent mini-project
