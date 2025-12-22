"""Tool definitions for LLM function calling patterns.

This module provides the tool definition schema structure and concrete tool
definitions for AITEA operations. Tools follow the JSON Schema format used
by OpenAI, Anthropic, and other LLM providers for function calling.

The tool definitions enable LLMs to:
- Add features to the feature library
- Search for existing features
- Estimate time for features and projects
- Import tracked time data

Example:
    >>> from src.services.tools import ToolRegistry, add_feature_tool
    >>> registry = ToolRegistry()
    >>> registry.register(add_feature_tool)
    >>> schema = registry.get_tool_schema("add_feature")
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
import json
import re


class JsonSchemaValidationError:
    """Represents a JSON Schema validation error.
    
    Attributes:
        path: JSON path to the invalid value (e.g., "$.features[0].name")
        message: Human-readable error message
        value: The invalid value
        schema_path: Path in the schema that was violated
    """
    
    def __init__(
        self,
        path: str,
        message: str,
        value: Any = None,
        schema_path: Optional[str] = None
    ) -> None:
        self.path = path
        self.message = message
        self.value = value
        self.schema_path = schema_path
    
    def __str__(self) -> str:
        return f"{self.path}: {self.message}"
    
    def __repr__(self) -> str:
        return f"JsonSchemaValidationError(path={self.path!r}, message={self.message!r})"


class JsonSchemaValidator:
    """Validates data against JSON Schema (draft-07 compatible).
    
    This validator supports the core JSON Schema validation keywords:
    - type: string, number, integer, boolean, array, object, null
    - required: list of required property names
    - properties: object property schemas
    - items: array item schema
    - enum: list of allowed values
    - minimum/maximum: numeric bounds
    - minLength/maxLength: string length bounds
    - minItems/maxItems: array length bounds
    - pattern: regex pattern for strings
    - additionalProperties: whether extra properties are allowed
    
    Example:
        >>> schema = {
        ...     "type": "object",
        ...     "properties": {
        ...         "name": {"type": "string"},
        ...         "age": {"type": "integer", "minimum": 0}
        ...     },
        ...     "required": ["name"]
        ... }
        >>> validator = JsonSchemaValidator(schema)
        >>> errors = validator.validate({"name": "Alice", "age": 30})
        >>> assert len(errors) == 0
    """
    
    # Mapping from JSON Schema types to Python types
    TYPE_MAP: Dict[str, type] = {
        "string": str,
        "number": (int, float),  # type: ignore
        "integer": int,
        "boolean": bool,
        "array": list,
        "object": dict,
        "null": type(None),
    }
    
    def __init__(self, schema: Dict[str, Any]) -> None:
        """Initialize the validator with a JSON Schema.
        
        Args:
            schema: The JSON Schema to validate against
        """
        self.schema = schema
    
    def validate(self, data: Any) -> List[JsonSchemaValidationError]:
        """Validate data against the schema.
        
        Args:
            data: The data to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        return self._validate_value(data, self.schema, "$")
    
    def is_valid(self, data: Any) -> bool:
        """Check if data is valid against the schema.
        
        Args:
            data: The data to validate
            
        Returns:
            True if valid, False otherwise
        """
        return len(self.validate(data)) == 0
    
    def _validate_value(
        self,
        value: Any,
        schema: Dict[str, Any],
        path: str
    ) -> List[JsonSchemaValidationError]:
        """Validate a value against a schema at a given path.
        
        Args:
            value: The value to validate
            schema: The schema to validate against
            path: The JSON path to the value
            
        Returns:
            List of validation errors
        """
        errors: List[JsonSchemaValidationError] = []
        
        # Handle empty schema (accepts anything)
        if not schema:
            return errors
        
        # Type validation
        if "type" in schema:
            type_errors = self._validate_type(value, schema["type"], path)
            errors.extend(type_errors)
            # If type is wrong, skip other validations
            if type_errors:
                return errors
        
        # Enum validation
        if "enum" in schema:
            if value not in schema["enum"]:
                errors.append(JsonSchemaValidationError(
                    path=path,
                    message=f"Value must be one of {schema['enum']}, got {value!r}",
                    value=value,
                    schema_path="enum"
                ))
        
        # String validations
        if isinstance(value, str):
            errors.extend(self._validate_string(value, schema, path))
        
        # Number validations
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            errors.extend(self._validate_number(value, schema, path))
        
        # Array validations
        if isinstance(value, list):
            errors.extend(self._validate_array(value, schema, path))
        
        # Object validations
        if isinstance(value, dict):
            errors.extend(self._validate_object(value, schema, path))
        
        return errors
    
    def _validate_type(
        self,
        value: Any,
        expected_type: Union[str, List[str]],
        path: str
    ) -> List[JsonSchemaValidationError]:
        """Validate the type of a value.
        
        Args:
            value: The value to validate
            expected_type: Expected type(s) from schema
            path: JSON path to the value
            
        Returns:
            List of validation errors
        """
        errors: List[JsonSchemaValidationError] = []
        
        # Handle multiple types
        if isinstance(expected_type, list):
            types = expected_type
        else:
            types = [expected_type]
        
        # Check if value matches any of the expected types
        for t in types:
            python_type = self.TYPE_MAP.get(t)
            if python_type is None:
                continue
            
            # Special handling for number type (accepts int and float)
            if t == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
                return errors
            
            # Special handling for integer (must be int, not float)
            if t == "integer" and isinstance(value, int) and not isinstance(value, bool):
                return errors
            
            # Special handling for null
            if t == "null" and value is None:
                return errors
            
            # General type check
            if isinstance(value, python_type) and not (t == "boolean" and isinstance(value, int)):
                return errors
        
        # No type matched
        actual_type = type(value).__name__
        if value is None:
            actual_type = "null"
        
        errors.append(JsonSchemaValidationError(
            path=path,
            message=f"Expected type {expected_type}, got {actual_type}",
            value=value,
            schema_path="type"
        ))
        
        return errors
    
    def _validate_string(
        self,
        value: str,
        schema: Dict[str, Any],
        path: str
    ) -> List[JsonSchemaValidationError]:
        """Validate string-specific constraints.
        
        Args:
            value: The string value
            schema: The schema with constraints
            path: JSON path to the value
            
        Returns:
            List of validation errors
        """
        errors: List[JsonSchemaValidationError] = []
        
        # minLength
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"String length {len(value)} is less than minimum {schema['minLength']}",
                value=value,
                schema_path="minLength"
            ))
        
        # maxLength
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"String length {len(value)} exceeds maximum {schema['maxLength']}",
                value=value,
                schema_path="maxLength"
            ))
        
        # pattern
        if "pattern" in schema:
            pattern = schema["pattern"]
            if not re.search(pattern, value):
                errors.append(JsonSchemaValidationError(
                    path=path,
                    message=f"String does not match pattern '{pattern}'",
                    value=value,
                    schema_path="pattern"
                ))
        
        return errors
    
    def _validate_number(
        self,
        value: Union[int, float],
        schema: Dict[str, Any],
        path: str
    ) -> List[JsonSchemaValidationError]:
        """Validate number-specific constraints.
        
        Args:
            value: The numeric value
            schema: The schema with constraints
            path: JSON path to the value
            
        Returns:
            List of validation errors
        """
        errors: List[JsonSchemaValidationError] = []
        
        # minimum
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Value {value} is less than minimum {schema['minimum']}",
                value=value,
                schema_path="minimum"
            ))
        
        # maximum
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Value {value} exceeds maximum {schema['maximum']}",
                value=value,
                schema_path="maximum"
            ))
        
        # exclusiveMinimum
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Value {value} must be greater than {schema['exclusiveMinimum']}",
                value=value,
                schema_path="exclusiveMinimum"
            ))
        
        # exclusiveMaximum
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Value {value} must be less than {schema['exclusiveMaximum']}",
                value=value,
                schema_path="exclusiveMaximum"
            ))
        
        # multipleOf
        if "multipleOf" in schema:
            multiple = schema["multipleOf"]
            if value % multiple != 0:
                errors.append(JsonSchemaValidationError(
                    path=path,
                    message=f"Value {value} is not a multiple of {multiple}",
                    value=value,
                    schema_path="multipleOf"
                ))
        
        return errors
    
    def _validate_array(
        self,
        value: List[Any],
        schema: Dict[str, Any],
        path: str
    ) -> List[JsonSchemaValidationError]:
        """Validate array-specific constraints.
        
        Args:
            value: The array value
            schema: The schema with constraints
            path: JSON path to the value
            
        Returns:
            List of validation errors
        """
        errors: List[JsonSchemaValidationError] = []
        
        # minItems
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Array length {len(value)} is less than minimum {schema['minItems']}",
                value=value,
                schema_path="minItems"
            ))
        
        # maxItems
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Array length {len(value)} exceeds maximum {schema['maxItems']}",
                value=value,
                schema_path="maxItems"
            ))
        
        # uniqueItems
        if schema.get("uniqueItems", False):
            # Check for duplicates (only works for hashable items)
            try:
                seen = set()
                for i, item in enumerate(value):
                    item_key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
                    if item_key in seen:
                        errors.append(JsonSchemaValidationError(
                            path=f"{path}[{i}]",
                            message=f"Duplicate item found at index {i}",
                            value=item,
                            schema_path="uniqueItems"
                        ))
                    seen.add(item_key)
            except (TypeError, ValueError):
                pass  # Skip uniqueness check for unhashable items
        
        # items - validate each item against the items schema
        if "items" in schema:
            items_schema = schema["items"]
            for i, item in enumerate(value):
                item_path = f"{path}[{i}]"
                errors.extend(self._validate_value(item, items_schema, item_path))
        
        return errors
    
    def _validate_object(
        self,
        value: Dict[str, Any],
        schema: Dict[str, Any],
        path: str
    ) -> List[JsonSchemaValidationError]:
        """Validate object-specific constraints.
        
        Args:
            value: The object value
            schema: The schema with constraints
            path: JSON path to the value
            
        Returns:
            List of validation errors
        """
        errors: List[JsonSchemaValidationError] = []
        
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        additional_properties = schema.get("additionalProperties", True)
        
        # Check required properties
        for prop_name in required:
            if prop_name not in value:
                errors.append(JsonSchemaValidationError(
                    path=f"{path}.{prop_name}",
                    message=f"Missing required property: {prop_name}",
                    value=None,
                    schema_path="required"
                ))
        
        # Validate each property
        for prop_name, prop_value in value.items():
            prop_path = f"{path}.{prop_name}"
            
            if prop_name in properties:
                # Validate against property schema
                prop_schema = properties[prop_name]
                errors.extend(self._validate_value(prop_value, prop_schema, prop_path))
            elif additional_properties is False:
                # Additional properties not allowed
                errors.append(JsonSchemaValidationError(
                    path=prop_path,
                    message=f"Additional property not allowed: {prop_name}",
                    value=prop_value,
                    schema_path="additionalProperties"
                ))
            elif isinstance(additional_properties, dict):
                # Validate against additionalProperties schema
                errors.extend(self._validate_value(prop_value, additional_properties, prop_path))
        
        # minProperties
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Object has {len(value)} properties, minimum is {schema['minProperties']}",
                value=value,
                schema_path="minProperties"
            ))
        
        # maxProperties
        if "maxProperties" in schema and len(value) > schema["maxProperties"]:
            errors.append(JsonSchemaValidationError(
                path=path,
                message=f"Object has {len(value)} properties, maximum is {schema['maxProperties']}",
                value=value,
                schema_path="maxProperties"
            ))
        
        return errors


def validate_json_schema(data: Any, schema: Dict[str, Any]) -> List[str]:
    """Validate data against a JSON Schema and return error messages.
    
    This is a convenience function that creates a validator and returns
    simple string error messages.
    
    Args:
        data: The data to validate
        schema: The JSON Schema to validate against
        
    Returns:
        List of error message strings (empty if valid)
        
    Example:
        >>> schema = {"type": "object", "required": ["name"]}
        >>> errors = validate_json_schema({}, schema)
        >>> assert "$.name: Missing required property: name" in errors
    """
    validator = JsonSchemaValidator(schema)
    validation_errors = validator.validate(data)
    return [str(error) for error in validation_errors]


@dataclass
class ToolParameter:
    """Definition of a single tool parameter.
    
    Attributes:
        name: The parameter name
        type: JSON Schema type (string, number, integer, boolean, array, object)
        description: Human-readable description of the parameter
        required: Whether the parameter is required
        enum: Optional list of allowed values
        items: For array types, the schema of array items
        default: Optional default value
    """
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    items: Optional[Dict[str, Any]] = None
    default: Optional[Any] = None
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert to JSON Schema format.
        
        Returns:
            Dictionary representing the parameter in JSON Schema format
        """
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
    
    A tool definition describes a function that an LLM can call,
    including its name, description, and parameter schema. This
    follows the OpenAI function calling format which is also
    compatible with Anthropic and other providers.
    
    Attributes:
        name: Unique identifier for the tool (snake_case)
        description: Human-readable description of what the tool does
        parameters: List of parameter definitions
        handler: Optional callable that implements the tool
        
    Example:
        >>> tool = ToolDefinition(
        ...     name="search_features",
        ...     description="Search for features in the library",
        ...     parameters=[
        ...         ToolParameter(
        ...             name="query",
        ...             type="string",
        ...             description="Search query string"
        ...         )
        ...     ]
        ... )
        >>> schema = tool.to_openai_schema()
    """
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    handler: Optional[Callable[..., Any]] = None
    
    def to_openai_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling schema format.
        
        Returns:
            Dictionary in OpenAI's function schema format
        """
        properties: Dict[str, Any] = {}
        required: List[str] = []
        
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
        """Convert to Anthropic tool use schema format.
        
        Returns:
            Dictionary in Anthropic's tool schema format
        """
        properties: Dict[str, Any] = {}
        required: List[str] = []
        
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
    
    def to_json_schema(self) -> Dict[str, Any]:
        """Convert to standard JSON Schema format.
        
        Returns:
            Dictionary in JSON Schema format
        """
        properties: Dict[str, Any] = {}
        required: List[str] = []
        
        for param in self.parameters:
            properties[param.name] = param.to_schema()
            if param.required:
                required.append(param.name)
        
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": self.name,
            "description": self.description,
            "type": "object",
            "properties": properties,
            "required": required,
        }
    
    def validate_arguments(self, arguments: Dict[str, Any]) -> List[str]:
        """Validate arguments against the tool's parameter schema using JSON Schema.
        
        This method uses the JsonSchemaValidator to perform comprehensive
        validation including:
        - Required parameter checking
        - Type validation (string, number, integer, boolean, array, object)
        - Enum validation
        - Nested object and array validation
        - String constraints (minLength, maxLength, pattern)
        - Number constraints (minimum, maximum)
        - Array constraints (minItems, maxItems, uniqueItems)
        
        Args:
            arguments: Dictionary of argument name to value
            
        Returns:
            List of validation error messages (empty if valid)
            
        Example:
            >>> tool = ToolDefinition(
            ...     name="test",
            ...     description="Test tool",
            ...     parameters=[
            ...         ToolParameter(name="name", type="string", description="Name", required=True),
            ...         ToolParameter(name="count", type="integer", description="Count", required=False)
            ...     ]
            ... )
            >>> errors = tool.validate_arguments({"name": "test", "count": 5})
            >>> assert len(errors) == 0
            >>> errors = tool.validate_arguments({})
            >>> assert "$.name: Missing required property: name" in errors
        """
        # Build JSON Schema from parameters
        schema = self.to_json_schema()
        
        # Extract just the properties schema for validation
        validation_schema = {
            "type": "object",
            "properties": schema.get("properties", {}),
            "required": schema.get("required", []),
            "additionalProperties": False,  # Don't allow unknown parameters
        }
        
        # Use the JsonSchemaValidator for comprehensive validation
        return validate_json_schema(arguments, validation_schema)
    
    def validate_arguments_detailed(
        self, 
        arguments: Dict[str, Any]
    ) -> List[JsonSchemaValidationError]:
        """Validate arguments and return detailed error objects.
        
        This method is similar to validate_arguments but returns
        JsonSchemaValidationError objects with full details including
        the path, value, and schema path.
        
        Args:
            arguments: Dictionary of argument name to value
            
        Returns:
            List of JsonSchemaValidationError objects (empty if valid)
        """
        schema = self.to_json_schema()
        validation_schema = {
            "type": "object",
            "properties": schema.get("properties", {}),
            "required": schema.get("required", []),
            "additionalProperties": False,
        }
        
        validator = JsonSchemaValidator(validation_schema)
        return validator.validate(arguments)


class ToolRegistry:
    """Registry for managing tool definitions.
    
    The ToolRegistry provides a central place to register, retrieve,
    and list tool definitions. It supports validation of tool arguments
    and can export tools in various schema formats.
    
    Example:
        >>> registry = ToolRegistry()
        >>> registry.register(add_feature_tool)
        >>> registry.register(search_features_tool)
        >>> 
        >>> # Get a specific tool
        >>> tool = registry.get("add_feature")
        >>> 
        >>> # List all tools
        >>> all_tools = registry.list_tools()
        >>> 
        >>> # Export for OpenAI
        >>> schemas = registry.to_openai_schemas()
    """
    
    def __init__(self) -> None:
        """Initialize an empty tool registry."""
        self._tools: Dict[str, ToolDefinition] = {}
    
    def register(self, tool: ToolDefinition) -> None:
        """Register a tool definition.
        
        Args:
            tool: The tool definition to register
            
        Raises:
            ValueError: If a tool with the same name is already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name.
        
        Args:
            name: The name of the tool to retrieve
            
        Returns:
            The tool definition, or None if not found
        """
        return self._tools.get(name)
    
    def list_tools(self) -> List[ToolDefinition]:
        """List all registered tools.
        
        Returns:
            List of all registered tool definitions
        """
        return list(self._tools.values())
    
    def list_tool_names(self) -> List[str]:
        """List names of all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())
    
    def to_openai_schemas(self) -> List[Dict[str, Any]]:
        """Export all tools in OpenAI function calling format.
        
        Returns:
            List of tool schemas in OpenAI format
        """
        return [tool.to_openai_schema() for tool in self._tools.values()]
    
    def to_anthropic_schemas(self) -> List[Dict[str, Any]]:
        """Export all tools in Anthropic tool use format.
        
        Returns:
            List of tool schemas in Anthropic format
        """
        return [tool.to_anthropic_schema() for tool in self._tools.values()]
    
    def validate_tool_call(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> List[str]:
        """Validate a tool call.
        
        Args:
            tool_name: Name of the tool being called
            arguments: Arguments passed to the tool
            
        Returns:
            List of validation error messages (empty if valid)
        """
        tool = self.get(tool_name)
        if tool is None:
            return [f"Unknown tool: {tool_name}"]
        
        return tool.validate_arguments(arguments)


# =============================================================================
# AITEA Tool Definitions
# =============================================================================
# These tools enable LLMs to interact with AITEA services for feature
# management, time tracking, and project estimation.


# Tool: add_feature
# Adds a new feature to the feature library
add_feature_tool = ToolDefinition(
    name="add_feature",
    description=(
        "Add a new feature to the AITEA feature library. "
        "Features represent software components or tasks that can be estimated. "
        "Each feature has a seed time estimate used when historical data is unavailable."
    ),
    parameters=[
        ToolParameter(
            name="name",
            type="string",
            description="The name of the feature (e.g., 'User Authentication', 'CRUD API')",
            required=True,
        ),
        ToolParameter(
            name="team",
            type="string",
            description="The team responsible for this feature",
            required=True,
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"],
        ),
        ToolParameter(
            name="seed_time_hours",
            type="number",
            description="Initial time estimate in hours (used when no historical data exists)",
            required=True,
        ),
        ToolParameter(
            name="process",
            type="string",
            description="The type of process this feature belongs to",
            required=False,
            default="Data Operations",
            enum=[
                "Data Operations",
                "Content Management",
                "Real-time",
                "Authentication",
                "Integration",
            ],
        ),
        ToolParameter(
            name="synonyms",
            type="array",
            description="Alternative names for this feature (for search matching)",
            required=False,
            items={"type": "string"},
            default=[],
        ),
        ToolParameter(
            name="notes",
            type="string",
            description="Additional notes or description for the feature",
            required=False,
            default="",
        ),
    ],
)


# Tool: search_features
# Searches for features in the library
search_features_tool = ToolDefinition(
    name="search_features",
    description=(
        "Search for features in the AITEA feature library. "
        "Searches feature names and synonyms for matches. "
        "Returns a list of matching features with their details."
    ),
    parameters=[
        ToolParameter(
            name="query",
            type="string",
            description="Search query to match against feature names and synonyms",
            required=True,
        ),
    ],
)


# Tool: list_features
# Lists all features, optionally filtered by team
list_features_tool = ToolDefinition(
    name="list_features",
    description=(
        "List all features in the AITEA feature library. "
        "Optionally filter by team to see only features assigned to a specific team."
    ),
    parameters=[
        ToolParameter(
            name="team",
            type="string",
            description="Filter features by team (optional)",
            required=False,
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"],
        ),
    ],
)


# Tool: get_feature
# Gets a specific feature by ID
get_feature_tool = ToolDefinition(
    name="get_feature",
    description=(
        "Get detailed information about a specific feature by its ID. "
        "Returns the feature's name, team, seed time, synonyms, and notes."
    ),
    parameters=[
        ToolParameter(
            name="feature_id",
            type="string",
            description="The unique identifier of the feature to retrieve",
            required=True,
        ),
    ],
)


# Tool: estimate_feature
# Estimates time for a single feature
estimate_feature_tool = ToolDefinition(
    name="estimate_feature",
    description=(
        "Estimate the time required for a single feature. "
        "Uses historical tracked time data if available (3+ data points), "
        "otherwise falls back to the feature's seed time estimate. "
        "Returns the estimate with confidence level and statistics."
    ),
    parameters=[
        ToolParameter(
            name="feature_name",
            type="string",
            description="Name of the feature to estimate",
            required=True,
        ),
    ],
)


# Tool: estimate_project
# Estimates time for a project with multiple features
estimate_project_tool = ToolDefinition(
    name="estimate_project",
    description=(
        "Estimate the total time required for a project consisting of multiple features. "
        "Aggregates individual feature estimates and provides total hours with "
        "overall confidence level (based on the lowest confidence among features)."
    ),
    parameters=[
        ToolParameter(
            name="features",
            type="array",
            description="List of feature names to include in the project estimate",
            required=True,
            items={"type": "string"},
        ),
    ],
)


# Tool: add_time_entry
# Adds a tracked time entry
add_time_entry_tool = ToolDefinition(
    name="add_time_entry",
    description=(
        "Record actual time spent on a feature by a team member. "
        "This data is used to improve estimation accuracy over time. "
        "More data points lead to higher confidence estimates."
    ),
    parameters=[
        ToolParameter(
            name="feature",
            type="string",
            description="Name of the feature the time was spent on",
            required=True,
        ),
        ToolParameter(
            name="tracked_time_hours",
            type="number",
            description="Actual time spent in hours",
            required=True,
        ),
        ToolParameter(
            name="team",
            type="string",
            description="The team of the person who tracked the time",
            required=True,
            enum=["backend", "frontend", "fullstack", "design", "qa", "devops"],
        ),
        ToolParameter(
            name="member_name",
            type="string",
            description="Name or identifier of the team member",
            required=True,
        ),
        ToolParameter(
            name="process",
            type="string",
            description="The type of process for this work",
            required=False,
            default="Data Operations",
            enum=[
                "Data Operations",
                "Content Management",
                "Real-time",
                "Authentication",
                "Integration",
            ],
        ),
        ToolParameter(
            name="date",
            type="string",
            description="Date when the work was done (ISO format: YYYY-MM-DD)",
            required=False,
        ),
    ],
)


# Tool: get_feature_statistics
# Gets statistics for a feature's tracked time
get_feature_statistics_tool = ToolDefinition(
    name="get_feature_statistics",
    description=(
        "Get statistical analysis of tracked time for a feature. "
        "Returns mean, median, standard deviation, and P80 (80th percentile) "
        "of all tracked time entries for the feature."
    ),
    parameters=[
        ToolParameter(
            name="feature_name",
            type="string",
            description="Name of the feature to get statistics for",
            required=True,
        ),
    ],
)


# Tool: import_time_csv
# Imports tracked time from a CSV file
import_time_csv_tool = ToolDefinition(
    name="import_time_csv",
    description=(
        "Import tracked time entries from a CSV file. "
        "The CSV should have columns: team, member_name, feature, "
        "tracked_time_hours, process, date. "
        "Returns count of successful and failed imports."
    ),
    parameters=[
        ToolParameter(
            name="file_path",
            type="string",
            description="Path to the CSV file to import",
            required=True,
        ),
    ],
)


def get_default_tool_registry() -> ToolRegistry:
    """Create a ToolRegistry with all default AITEA tools registered.
    
    Returns:
        A ToolRegistry containing all AITEA tool definitions
        
    Example:
        >>> registry = get_default_tool_registry()
        >>> print(registry.list_tool_names())
        ['add_feature', 'search_features', 'list_features', ...]
    """
    registry = ToolRegistry()
    
    # Register all AITEA tools
    registry.register(add_feature_tool)
    registry.register(search_features_tool)
    registry.register(list_features_tool)
    registry.register(get_feature_tool)
    registry.register(estimate_feature_tool)
    registry.register(estimate_project_tool)
    registry.register(add_time_entry_tool)
    registry.register(get_feature_statistics_tool)
    registry.register(import_time_csv_tool)
    
    return registry


# List of all AITEA tools for easy access
AITEA_TOOLS: List[ToolDefinition] = [
    add_feature_tool,
    search_features_tool,
    list_features_tool,
    get_feature_tool,
    estimate_feature_tool,
    estimate_project_tool,
    add_time_entry_tool,
    get_feature_statistics_tool,
    import_time_csv_tool,
]
