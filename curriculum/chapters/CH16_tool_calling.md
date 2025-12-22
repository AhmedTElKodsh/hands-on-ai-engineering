# Chapter 16: Tool Calling Patterns

**Difficulty:** Intermediate  
**Time:** 2.5 hours  
**Prerequisites:** Chapters 13-15  
**AITEA Component:** `src/services/tools.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Define tools using JSON Schema format
2. Create a ToolRegistry for managing tool definitions
3. Validate tool arguments against schemas
4. Convert tools to OpenAI and Anthropic formats
5. Implement AITEA tools for feature management

## 16.1 What Is Tool Calling?

Tool calling (function calling) lets LLMs invoke external functions:

```
User: "Add a CRUD feature to the library"
     ↓
LLM: "I'll call add_feature with these arguments..."
     ↓
Tool: add_feature(name="CRUD", team="backend", hours=4)
     ↓
Result: Feature added successfully
```

**Why tools matter:**

- LLMs can't access databases, APIs, or files directly
- Tools bridge the gap between language and action
- Enables agents to interact with the real world

## 16.2 Tool Definition Schema

Tools are defined using JSON Schema:

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolParameter:
    """Definition of a single tool parameter."""
    name: str
    type: str  # string, number, integer, boolean, array, object
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    items: Optional[Dict[str, Any]] = None  # For array types
    default: Optional[Any] = None

    def to_schema(self) -> Dict[str, Any]:
        """Convert to JSON Schema format."""
        schema: Dict[str, Any] = {
            "type": self.type,
            "description": self.description,
        }

        if self.enum is not None:
            schema["enum"] = self.enum
        if self.items is not None:
            schema["items"] = self.items
        if self.default is not None:
            schema["default"] = self.default

        return schema


@dataclass
class ToolDefinition:
    """Definition of a tool for LLM function calling.

    Example:
        >>> tool = ToolDefinition(
        ...     name="search_features",
        ...     description="Search for features in the library",
        ...     parameters=[
        ...         ToolParameter(name="query", type="string",
        ...                       description="Search query")
        ...     ]
        ... )
    """
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    handler: Optional[Callable[..., Any]] = None

    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format."""
        properties = {}
        required = []

        for param in self.parameters:
            properties[param.name] = param.to_schema()
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

    def to_anthropic_schema(self) -> Dict[str, Any]:
        """Convert to Anthropic tool use format."""
        properties = {}
        required = []

        for param in self.parameters:
            properties[param.name] = param.to_schema()
            if param.required:
                required.append(param.name)

        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }
```

## 16.3 JSON Schema Validation

Validate tool arguments before execution:

```python
import re
from typing import Any, Dict, List


class JsonSchemaValidationError:
    """Represents a validation error."""
    def __init__(self, path: str, message: str, value: Any = None):
        self.path = path
        self.message = message
        self.value = value

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


class JsonSchemaValidator:
    """Validates data against JSON Schema.

    Supports: type, required, properties, items, enum,
    minimum/maximum, minLength/maxLength, pattern
    """

    TYPE_MAP = {
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None),
    }

    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def validate(self, data: Any) -> List[JsonSchemaValidationError]:
        """Validate data against schema."""
        return self._validate_value(data, self.schema, "$")

    def is_valid(self, data: Any) -> bool:
        """Check if data is valid."""
        return len(self.validate(data)) == 0

    def _validate_value(
        self, value: Any, schema: Dict[str, Any], path: str
    ) -> List[JsonSchemaValidationError]:
        errors = []

        # Type validation
        if "type" in schema:
            type_errors = self._validate_type(value, schema["type"], path)
            errors.extend(type_errors)
            if type_errors:
                return errors  # Skip other validations if type is wrong

        # Enum validation
        if "enum" in schema and value not in schema["enum"]:
            errors.append(JsonSchemaValidationError(
                path, f"Must be one of {schema['enum']}", value
            ))

        # String validations
        if isinstance(value, str):
            if "minLength" in schema and len(value) < schema["minLength"]:
                errors.append(JsonSchemaValidationError(
                    path, f"Length < minimum {schema['minLength']}", value
                ))
            if "maxLength" in schema and len(value) > schema["maxLength"]:
                errors.append(JsonSchemaValidationError(
                    path, f"Length > maximum {schema['maxLength']}", value
                ))
            if "pattern" in schema and not re.search(schema["pattern"], value):
                errors.append(JsonSchemaValidationError(
                    path, f"Doesn't match pattern '{schema['pattern']}'", value
                ))

        # Number validations
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(JsonSchemaValidationError(
                    path, f"Value < minimum {schema['minimum']}", value
                ))
            if "maximum" in schema and value > schema["maximum"]:
                errors.append(JsonSchemaValidationError(
                    path, f"Value > maximum {schema['maximum']}", value
                ))

        # Array validations
        if isinstance(value, list):
            if "minItems" in schema and len(value) < schema["minItems"]:
                errors.append(JsonSchemaValidationError(
                    path, f"Array length < minimum {schema['minItems']}", value
                ))
            if "items" in schema:
                for i, item in enumerate(value):
                    errors.extend(self._validate_value(
                        item, schema["items"], f"{path}[{i}]"
                    ))

        # Object validations
        if isinstance(value, dict):
            props = schema.get("properties", {})
            required = schema.get("required", [])

            # Check required properties
            for prop in required:
                if prop not in value:
                    errors.append(JsonSchemaValidationError(
                        f"{path}.{prop}", "Missing required property"
                    ))

            # Validate each property
            for prop_name, prop_value in value.items():
                if prop_name in props:
                    errors.extend(self._validate_value(
                        prop_value, props[prop_name], f"{path}.{prop_name}"
                    ))

        return errors

    def _validate_type(
        self, value: Any, expected: str, path: str
    ) -> List[JsonSchemaValidationError]:
        python_type = self.TYPE_MAP.get(expected)

        if expected == "number" and isinstance(value, (int, float)):
            return []
        if expected == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return []
        if expected == "null" and value is None:
            return []
        if isinstance(value, python_type):
            return []

        return [JsonSchemaValidationError(
            path, f"Expected {expected}, got {type(value).__name__}", value
        )]
```

## 16.4 The ToolRegistry

Manage multiple tools:

```python
class ToolRegistry:
    """Registry for managing tool definitions.

    Example:
        >>> registry = ToolRegistry()
        >>> registry.register(add_feature_tool)
        >>> registry.register(search_features_tool)
        >>>
        >>> tool = registry.get("add_feature")
        >>> schemas = registry.to_openai_schemas()
    """

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool definition."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

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
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def to_anthropic_schemas(self) -> List[Dict[str, Any]]:
        """Export all tools in Anthropic format."""
        return [tool.to_anthropic_schema() for tool in self._tools.values()]

    def validate_tool_call(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> List[str]:
        """Validate a tool call."""
        tool = self.get(tool_name)
        if tool is None:
            return [f"Unknown tool: {tool_name}"]

        return tool.validate_arguments(arguments)
```

## 16.5 AITEA Tool Definitions

```python
# Add Feature Tool
add_feature_tool = ToolDefinition(
    name="add_feature",
    description="Add a new feature to the feature library",
    parameters=[
        ToolParameter(
            name="name",
            type="string",
            description="Feature name (e.g., 'CRUD API', 'User Authentication')"
        ),
        ToolParameter(
            name="team",
            type="string",
            description="Team responsible for the feature",
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"]
        ),
        ToolParameter(
            name="seed_time_hours",
            type="number",
            description="Initial time estimate in hours"
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
            description="Alternative names for the feature",
            required=False,
            items={"type": "string"}
        ),
        ToolParameter(
            name="notes",
            type="string",
            description="Additional notes about the feature",
            required=False
        ),
    ]
)


# Search Features Tool
search_features_tool = ToolDefinition(
    name="search_features",
    description="Search for features in the library by name or keyword",
    parameters=[
        ToolParameter(
            name="query",
            type="string",
            description="Search query (feature name or keyword)"
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
            description="Maximum results to return",
            required=False,
            default=10
        ),
    ]
)


# Estimate Feature Tool
estimate_feature_tool = ToolDefinition(
    name="estimate_feature",
    description="Get time estimate for a feature based on historical data",
    parameters=[
        ToolParameter(
            name="feature_name",
            type="string",
            description="Name of the feature to estimate"
        ),
        ToolParameter(
            name="include_statistics",
            type="boolean",
            description="Include detailed statistics (mean, median, p80)",
            required=False,
            default=True
        ),
    ]
)


# Create default registry with AITEA tools
def create_aitea_registry() -> ToolRegistry:
    """Create a registry with all AITEA tools."""
    registry = ToolRegistry()
    registry.register(add_feature_tool)
    registry.register(search_features_tool)
    registry.register(estimate_feature_tool)
    return registry
```

## 16.6 Using Tools with LLMs

````python
import json
from src.services.llm import get_llm_provider, ChatMessage
from src.services.tools import create_aitea_registry


async def process_with_tools(user_message: str):
    """Process a message with tool calling."""
    llm = get_llm_provider()
    registry = create_aitea_registry()

    # Build messages with tool definitions
    messages = [
        ChatMessage(
            role="system",
            content=f"""You are an AITEA assistant. You have access to these tools:

{json.dumps(registry.to_openai_schemas(), indent=2)}

When you need to use a tool, respond with:
```json
{{"tool": "tool_name", "arguments": {{...}}}}
```"""
        ),
        ChatMessage(role="user", content=user_message)
    ]

    response = await llm.chat(messages)

    # Check if response contains a tool call
    try:
        data = json.loads(response)
        if "tool" in data:
            tool_name = data["tool"]
            arguments = data.get("arguments", {})

            # Validate arguments
            errors = registry.validate_tool_call(tool_name, arguments)
            if errors:
                return f"Invalid tool call: {errors}"

            # Execute tool (in real implementation)
            return f"Would execute: {tool_name}({arguments})"
    except json.JSONDecodeError:
        pass

    return response
````

## 16.7 Your Turn: Exercise 16.1

Create a tool for importing CSV data:

```python
import_csv_tool = ToolDefinition(
    name="import_csv",
    description="Import tracked time entries from a CSV file",
    parameters=[
        ToolParameter(
            name="file_path",
            type="string",
            description="Path to the CSV file"
        ),
        ToolParameter(
            name="validate_only",
            type="boolean",
            description="Only validate without importing",
            required=False,
            default=False
        ),
        # TODO: Add more parameters:
        # - skip_errors: boolean - continue on row errors
        # - date_format: string - expected date format
    ]
)

# Test validation
errors = import_csv_tool.validate_arguments({
    "file_path": "data/time.csv",
    "validate_only": True
})
print(f"Validation errors: {errors}")
```

## 16.8 Debugging Scenario

**The Bug:** Tool validation passes but execution fails.

```python
tool = ToolDefinition(
    name="test",
    parameters=[
        ToolParameter(name="count", type="integer", description="Count")
    ]
)

# This passes validation
errors = tool.validate_arguments({"count": 5.0})
print(errors)  # []

# But the handler expects int
def handler(count: int):
    return count + 1

handler(5.0)  # Works but might cause issues downstream
```

**The Problem:** JSON Schema `integer` accepts Python floats that are whole numbers.

**The Fix:** Add explicit type coercion in the handler or use stricter validation:

```python
def handler(count: int):
    if not isinstance(count, int):
        count = int(count)  # Coerce to int
    return count + 1
```

## 16.9 Quick Check Questions

1. What format do tool definitions use?
2. Why validate arguments before execution?
3. What's the difference between OpenAI and Anthropic tool formats?
4. How does ToolRegistry help manage tools?
5. What happens if a required parameter is missing?

<details>
<summary>Answers</summary>

1. JSON Schema format for parameter definitions
2. To catch errors early and provide clear feedback before executing potentially dangerous operations
3. OpenAI uses `function.parameters`, Anthropic uses `input_schema` - same structure, different keys
4. Centralizes registration, lookup, validation, and format conversion
5. Validation returns an error indicating the missing required property

</details>

## 16.10 Mini-Project: Tool Executor

Create a tool executor that handles the full lifecycle:

```python
from typing import Any, Callable, Dict


class ToolExecutor:
    """Executes tools with validation and error handling."""

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self._handlers: Dict[str, Callable] = {}

    def register_handler(self, tool_name: str, handler: Callable) -> None:
        """Register a handler function for a tool."""
        if tool_name not in self.registry.list_tool_names():
            raise ValueError(f"Unknown tool: {tool_name}")
        self._handlers[tool_name] = handler

    async def execute(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool with validation."""
        # Validate tool exists
        tool = self.registry.get(tool_name)
        if tool is None:
            return {"error": f"Unknown tool: {tool_name}"}

        # Validate arguments
        errors = tool.validate_arguments(arguments)
        if errors:
            return {"error": "Validation failed", "details": errors}

        # Get handler
        handler = self._handlers.get(tool_name)
        if handler is None:
            return {"error": f"No handler for tool: {tool_name}"}

        # Execute
        try:
            result = await handler(**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"error": str(e)}


# Usage
executor = ToolExecutor(create_aitea_registry())

async def add_feature_handler(name: str, team: str, seed_time_hours: float, **kwargs):
    # Implementation here
    return {"id": "feat_001", "name": name}

executor.register_handler("add_feature", add_feature_handler)
```

## 16.11 AITEA Integration

This chapter implements:

- **Requirement 3.4**: Tool definition schema structure
- **Requirement 3.4**: Tools for AITEA operations (add_feature, estimate, etc.)

**Verification:**

```python
from src.services.tools import (
    ToolRegistry,
    ToolDefinition,
    ToolParameter,
    create_aitea_registry
)

# Create registry
registry = create_aitea_registry()
print(f"Registered tools: {registry.list_tool_names()}")

# Test OpenAI format
schemas = registry.to_openai_schemas()
print(f"OpenAI schemas: {len(schemas)} tools")

# Test validation
errors = registry.validate_tool_call("add_feature", {
    "name": "CRUD",
    "team": "backend",
    "seed_time_hours": 4,
    "process": "Data Operations"
})
print(f"✅ Valid call, errors: {errors}")

# Test invalid call
errors = registry.validate_tool_call("add_feature", {
    "name": "CRUD",
    "team": "invalid_team"  # Not in enum
})
print(f"Invalid call errors: {errors}")
```

## What's Next

Phase 3 is complete! In Chapter 17, you'll start Phase 4: Agent Foundations, learning what agents are and how they differ from chatbots.

**Before proceeding:**

- Create tools for your own use cases
- Test validation with various inputs
- Try the ToolExecutor mini-project
