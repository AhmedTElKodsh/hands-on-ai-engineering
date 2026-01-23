# Chapter 19: Tool Registry

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 16, 18  
**AITEA Component:** `src/services/tools.py` (ToolRegistry)

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create a centralized tool registry for agents
2. Register, retrieve, and list tools dynamically
3. Validate tool arguments using JSON Schema
4. Export tools in multiple formats (OpenAI, Anthropic)
5. Integrate the registry with SimpleAgent

## 19.1 Why a Tool Registry?

Without a registry, tools are scattered:

```python
# Bad: Tools defined everywhere
def search_features(query): ...
def add_feature(name, team): ...
# How does the agent know what's available?
```

With a registry, tools are centralized:

```python
# Good: Single source of truth
registry = ToolRegistry()
registry.register(search_features_tool)
registry.register(add_feature_tool)

# Agent can discover tools
available = registry.list_tool_names()  # ["search_features", "add_feature"]
```

## 19.2 The ToolRegistry Class

```python
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    items: Optional[Dict[str, Any]] = None
    default: Optional[Any] = None

    def to_schema(self) -> Dict[str, Any]:
        schema = {"type": self.type, "description": self.description}
        if self.enum:
            schema["enum"] = self.enum
        if self.items:
            schema["items"] = self.items
        if self.default is not None:
            schema["default"] = self.default
        return schema


@dataclass
class ToolDefinition:
    """Complete tool definition."""
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    handler: Optional[Callable[..., Any]] = None

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI format."""
        props = {p.name: p.to_schema() for p in self.parameters}
        required = [p.name for p in self.parameters if p.required]

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                },
            },
        }

    def to_anthropic_schema(self) -> Dict[str, Any]:
        """Convert to Anthropic format."""
        props = {p.name: p.to_schema() for p in self.parameters}
        required = [p.name for p in self.parameters if p.required]

        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        }

    def validate_arguments(self, args: Dict[str, Any]) -> List[str]:
        """Validate arguments against schema."""
        errors = []

        # Check required parameters
        for param in self.parameters:
            if param.required and param.name not in args:
                errors.append(f"Missing required parameter: {param.name}")

        # Check types and constraints
        for name, value in args.items():
            param = next((p for p in self.parameters if p.name == name), None)
            if param is None:
                errors.append(f"Unknown parameter: {name}")
                continue

            # Type checking
            if param.type == "string" and not isinstance(value, str):
                errors.append(f"{name}: expected string, got {type(value).__name__}")
            elif param.type == "number" and not isinstance(value, (int, float)):
                errors.append(f"{name}: expected number, got {type(value).__name__}")
            elif param.type == "integer" and not isinstance(value, int):
                errors.append(f"{name}: expected integer, got {type(value).__name__}")
            elif param.type == "boolean" and not isinstance(value, bool):
                errors.append(f"{name}: expected boolean, got {type(value).__name__}")
            elif param.type == "array" and not isinstance(value, list):
                errors.append(f"{name}: expected array, got {type(value).__name__}")

            # Enum checking
            if param.enum and value not in param.enum:
                errors.append(f"{name}: must be one of {param.enum}")

        return errors


class ToolRegistry:
    """Registry for managing tool definitions.

    Example:
        >>> registry = ToolRegistry()
        >>> registry.register(search_tool)
        >>> registry.register(add_tool)
        >>>
        >>> tool = registry.get("search_features")
        >>> errors = registry.validate_tool_call("search_features", {"query": "CRUD"})
    """

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def unregister(self, name: str) -> bool:
        """Unregister a tool. Returns True if found."""
        if name in self._tools:
            del self._tools[name]
            return True
        return False

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[ToolDefinition]:
        """List all registered tools."""
        return list(self._tools.values())

    def list_tool_names(self) -> List[str]:
        """List all tool names."""
        return list(self._tools.keys())

    def to_openai_schemas(self) -> List[Dict[str, Any]]:
        """Export all tools in OpenAI format."""
        return [t.to_openai_schema() for t in self._tools.values()]

    def to_anthropic_schemas(self) -> List[Dict[str, Any]]:
        """Export all tools in Anthropic format."""
        return [t.to_anthropic_schema() for t in self._tools.values()]

    def validate_tool_call(self, name: str, args: Dict[str, Any]) -> List[str]:
        """Validate a tool call."""
        tool = self.get(name)
        if tool is None:
            return [f"Unknown tool: {name}"]
        return tool.validate_arguments(args)

    def get_tool_descriptions(self) -> str:
        """Get formatted descriptions of all tools."""
        lines = []
        for tool in self._tools.values():
            params = ", ".join(
                f"{p.name}: {p.type}" + ("?" if not p.required else "")
                for p in tool.parameters
            )
            lines.append(f"- {tool.name}({params}): {tool.description}")
        return "\n".join(lines)
```

## 19.3 AITEA Tools

Define tools for AITEA operations:

```python
# Search Features Tool
search_features_tool = ToolDefinition(
    name="search_features",
    description="Search for features in the library by name or keyword",
    parameters=[
        ToolParameter(
            name="query",
            type="string",
            description="Search query"
        ),
        ToolParameter(
            name="team",
            type="string",
            description="Filter by team",
            required=False,
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"]
        ),
        ToolParameter(
            name="limit",
            type="integer",
            description="Max results",
            required=False,
            default=10
        ),
    ]
)


# Add Feature Tool
add_feature_tool = ToolDefinition(
    name="add_feature",
    description="Add a new feature to the library",
    parameters=[
        ToolParameter(name="name", type="string", description="Feature name"),
        ToolParameter(
            name="team",
            type="string",
            description="Responsible team",
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"]
        ),
        ToolParameter(
            name="seed_time_hours",
            type="number",
            description="Initial time estimate"
        ),
        ToolParameter(
            name="process",
            type="string",
            description="Process type",
            enum=["Data Operations", "Content Management", "Real-time",
                  "Authentication", "Integration"]
        ),
        ToolParameter(
            name="synonyms",
            type="array",
            description="Alternative names",
            required=False,
            items={"type": "string"}
        ),
    ]
)


# Estimate Feature Tool
estimate_feature_tool = ToolDefinition(
    name="estimate_feature",
    description="Get time estimate for a feature",
    parameters=[
        ToolParameter(
            name="feature_name",
            type="string",
            description="Feature to estimate"
        ),
        ToolParameter(
            name="include_statistics",
            type="boolean",
            description="Include detailed stats",
            required=False,
            default=True
        ),
    ]
)


def create_aitea_registry() -> ToolRegistry:
    """Create registry with all AITEA tools."""
    registry = ToolRegistry()
    registry.register(search_features_tool)
    registry.register(add_feature_tool)
    registry.register(estimate_feature_tool)
    return registry
```

## 19.4 Integrating with SimpleAgent

```python
from src.agents.simple_agent import SimpleAgent
from src.services.tools import ToolRegistry


class ToolAwareAgent(SimpleAgent):
    """Agent that can use tools from a registry."""

    def __init__(self, llm, registry: ToolRegistry, **kwargs):
        super().__init__(llm, **kwargs)
        self.registry = registry

    async def _think(self) -> str:
        """Think phase with tool awareness."""
        self._transition_to(AgentState.THINK, message="Planning with tools")

        tool_descriptions = self.registry.get_tool_descriptions()

        prompt = f"""You are in the THINK phase.
Task: {self._context.task}
Latest observation: {self._context.observations[-1] if self._context.observations else 'None'}

Available tools:
{tool_descriptions}

Decide what to do. If using a tool, specify:
TOOL: tool_name
ARGS: {{"param": "value"}}

Or respond directly if no tool is needed."""

        thought = await self.llm.complete(prompt)
        self._context.add_thought(thought)
        return thought

    async def _act(self) -> Dict[str, Any]:
        """Act phase with tool execution."""
        self._transition_to(AgentState.ACT, message="Executing")

        thought = self._context.thoughts[-1] if self._context.thoughts else ""

        # Parse tool call from thought
        tool_call = self._parse_tool_call(thought)

        if tool_call:
            tool_name, args = tool_call

            # Validate
            errors = self.registry.validate_tool_call(tool_name, args)
            if errors:
                result = f"Tool validation failed: {errors}"
            else:
                # Execute tool (simplified)
                tool = self.registry.get(tool_name)
                if tool and tool.handler:
                    result = await tool.handler(**args)
                else:
                    result = f"Would execute: {tool_name}({args})"
        else:
            # No tool call, use LLM response
            result = thought

        action = {
            "iteration": self._context.iteration,
            "tool_call": tool_call,
            "result": result,
        }
        self._context.add_action(action)
        return action

    def _parse_tool_call(self, text: str) -> Optional[tuple]:
        """Parse tool call from text."""
        import re
        import json

        tool_match = re.search(r'TOOL:\s*(\w+)', text)
        args_match = re.search(r'ARGS:\s*(\{[^}]+\})', text)

        if tool_match:
            tool_name = tool_match.group(1)
            args = {}
            if args_match:
                try:
                    args = json.loads(args_match.group(1))
                except json.JSONDecodeError:
                    pass
            return (tool_name, args)

        return None
```

## 19.5 Your Turn: Exercise 19.1

Add a tool for listing features:

```python
list_features_tool = ToolDefinition(
    name="list_features",
    description="List all features in the library",
    parameters=[
        ToolParameter(
            name="team",
            type="string",
            description="Filter by team",
            required=False,
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"]
        ),
        ToolParameter(
            name="sort_by",
            type="string",
            description="Sort field",
            required=False,
            enum=["name", "seed_time_hours", "created_at"],
            default="name"
        ),
        # TODO: Add pagination parameters
        # - offset: integer
        # - limit: integer (default 20)
    ]
)
```

## 19.6 Debugging Scenario

**The Bug:** Tool validation passes but execution fails.

```python
registry = ToolRegistry()
registry.register(add_feature_tool)

# This passes validation
errors = registry.validate_tool_call("add_feature", {
    "name": "Test",
    "team": "backend",
    "seed_time_hours": "4",  # String instead of number!
    "process": "Data Operations"
})
print(errors)  # [] - No errors!
```

**The Problem:** JSON from LLM might have strings for numbers.

**The Fix:** Add type coercion or stricter validation:

```python
def validate_arguments(self, args: Dict[str, Any]) -> List[str]:
    errors = []

    for name, value in args.items():
        param = next((p for p in self.parameters if p.name == name), None)
        if param is None:
            continue

        # Try to coerce types
        if param.type == "number" and isinstance(value, str):
            try:
                args[name] = float(value)  # Coerce in place
            except ValueError:
                errors.append(f"{name}: cannot convert '{value}' to number")
        elif param.type == "integer" and isinstance(value, str):
            try:
                args[name] = int(value)
            except ValueError:
                errors.append(f"{name}: cannot convert '{value}' to integer")

    return errors
```

## 19.7 Quick Check Questions

1. What problem does ToolRegistry solve?
2. How do you add a new tool to the registry?
3. What's the difference between OpenAI and Anthropic tool formats?
4. Why validate tool arguments before execution?
5. How does an agent discover available tools?

<details>
<summary>Answers</summary>

1. Centralizes tool management, discovery, and validation
2. `registry.register(tool_definition)`
3. OpenAI uses `function.parameters`, Anthropic uses `input_schema`
4. To catch errors early and provide clear feedback
5. By calling `registry.list_tools()` or `registry.get_tool_descriptions()`

</details>

## 19.8 Mini-Project: Tool Decorator

Create a decorator for easy tool registration:

```python
def tool(
    name: str,
    description: str,
    registry: Optional[ToolRegistry] = None
):
    """Decorator to register a function as a tool.

    Example:
        >>> @tool("greet", "Greet a user")
        ... def greet(name: str) -> str:
        ...     return f"Hello, {name}!"
    """
    def decorator(func: Callable) -> Callable:
        import inspect

        # Extract parameters from function signature
        sig = inspect.signature(func)
        parameters = []

        for param_name, param in sig.parameters.items():
            # Infer type from annotation
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"

            required = param.default == inspect.Parameter.empty

            parameters.append(ToolParameter(
                name=param_name,
                type=param_type,
                description=f"Parameter: {param_name}",
                required=required,
                default=None if required else param.default
            ))

        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            handler=func
        )

        if registry:
            registry.register(tool_def)

        func._tool_definition = tool_def
        return func

    return decorator


# Usage
my_registry = ToolRegistry()

@tool("calculate_sum", "Add two numbers", registry=my_registry)
def calculate_sum(a: float, b: float) -> float:
    return a + b

print(my_registry.list_tool_names())  # ["calculate_sum"]
```

## 19.9 AITEA Integration

This chapter implements:

- **Requirement 5.3**: ToolRegistry with register, get, list methods
- **Property 9**: Tool Registry Operations

**Verification:**

```python
from src.services.tools import create_aitea_registry

# Create registry
registry = create_aitea_registry()

# Test registration
print(f"Tools: {registry.list_tool_names()}")
assert "search_features" in registry.list_tool_names()
assert "add_feature" in registry.list_tool_names()

# Test retrieval
tool = registry.get("search_features")
assert tool is not None
assert tool.name == "search_features"

# Test validation
errors = registry.validate_tool_call("search_features", {"query": "CRUD"})
assert len(errors) == 0, f"Unexpected errors: {errors}"

errors = registry.validate_tool_call("search_features", {})  # Missing query
assert len(errors) > 0

# Test export
openai_schemas = registry.to_openai_schemas()
assert len(openai_schemas) == 3

print("✅ ToolRegistry verified")
```

## What's Next

In Chapter 20, you'll implement the ReAct pattern—a powerful approach that combines reasoning and acting.

**Before proceeding:**

- Create your own tools and register them
- Test validation with various inputs
- Try the tool decorator mini-project
