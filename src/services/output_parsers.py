"""Output parsers for extracting structured data from LLM responses.

This module provides output parsers that extract structured JSON from LLM
responses using Pydantic validation. The parsers ensure type safety and
provide detailed error messages when parsing fails.

The main components are:
- OutputParserError: Base exception for parsing errors
- JsonOutputParser: Generic parser for JSON to Pydantic models
- Predefined parsers for common AITEA response types
"""

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, ValidationError as PydanticValidationError


# Type variable for generic parser
T = TypeVar('T', bound=BaseModel)


class OutputParserError(Exception):
    """Base exception for output parser errors."""
    pass


class JsonParseError(OutputParserError):
    """Raised when JSON parsing fails."""
    
    def __init__(self, message: str, raw_output: str, position: Optional[int] = None):
        self.raw_output = raw_output
        self.position = position
        super().__init__(message)


class ValidationParseError(OutputParserError):
    """Raised when Pydantic validation fails."""
    
    def __init__(
        self,
        message: str,
        errors: List[Dict[str, Any]],
        raw_output: str
    ):
        self.errors = errors
        self.raw_output = raw_output
        super().__init__(message)


class OutputParser(ABC, Generic[T]):
    """Abstract base class for output parsers.
    
    Output parsers transform raw LLM text output into structured data.
    Subclasses must implement the parse() method.
    """
    
    @abstractmethod
    def parse(self, text: str) -> T:
        """Parse the raw text output into structured data.
        
        Args:
            text: Raw text output from an LLM
            
        Returns:
            Parsed and validated data of type T
            
        Raises:
            OutputParserError: If parsing fails
        """
        ...
    
    @abstractmethod
    def get_format_instructions(self) -> str:
        """Get instructions for the LLM on how to format output.
        
        Returns:
            A string describing the expected output format
        """
        ...



class JsonOutputParser(OutputParser[T]):
    """Parser that extracts JSON from LLM output and validates with Pydantic.
    
    JsonOutputParser handles common LLM output patterns including:
    - Pure JSON responses
    - JSON wrapped in markdown code blocks (```json ... ```)
    - JSON with surrounding text
    
    The parser validates the extracted JSON against a Pydantic model,
    providing detailed error messages when validation fails.
    
    Attributes:
        pydantic_model: The Pydantic model class to validate against
        
    Example:
        >>> from pydantic import BaseModel
        >>> class Feature(BaseModel):
        ...     name: str
        ...     hours: float
        >>> parser = JsonOutputParser(Feature)
        >>> result = parser.parse('{"name": "Login", "hours": 8.0}')
        >>> print(result.name)
        Login
        
        >>> # Also handles markdown code blocks
        >>> result = parser.parse('```json\\n{"name": "Login", "hours": 8.0}\\n```')
        >>> print(result.hours)
        8.0
    """
    
    def __init__(self, pydantic_model: Type[T]) -> None:
        """Initialize the parser with a Pydantic model.
        
        Args:
            pydantic_model: The Pydantic model class to use for validation
        """
        self.pydantic_model = pydantic_model
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text, handling various formats.
        
        Handles:
        - Pure JSON
        - JSON in markdown code blocks (```json ... ``` or ``` ... ```)
        - JSON with surrounding text
        
        Args:
            text: Raw text that may contain JSON
            
        Returns:
            Extracted JSON string
            
        Raises:
            JsonParseError: If no valid JSON can be found
        """
        text = text.strip()
        
        # Try to extract from markdown code blocks first
        # Pattern matches ```json ... ``` or ``` ... ```
        code_block_pattern = r'```(?:json)?\s*\n?([\s\S]*?)\n?```'
        matches = re.findall(code_block_pattern, text)
        if matches:
            # Return the first code block that looks like JSON
            for match in matches:
                match = match.strip()
                if match.startswith('{') or match.startswith('['):
                    return match
        
        # If text itself looks like JSON, return it directly
        if text.startswith('{') or text.startswith('['):
            return text
        
        # Try to find JSON by matching balanced brackets
        json_str = self._find_balanced_json(text)
        if json_str:
            return json_str
        
        raise JsonParseError(
            "Could not find valid JSON in the output. "
            "Expected JSON object ({...}) or array ([...]).",
            raw_output=text
        )
    
    def _find_balanced_json(self, text: str) -> Optional[str]:
        """Find JSON with balanced brackets in text.
        
        Args:
            text: Text that may contain JSON
            
        Returns:
            Extracted JSON string or None if not found
        """
        # Find the first { or [
        start_chars = {'{': '}', '[': ']'}
        
        for i, char in enumerate(text):
            if char in start_chars:
                end_char = start_chars[char]
                depth = 0
                in_string = False
                escape_next = False
                
                for j in range(i, len(text)):
                    c = text[j]
                    
                    if escape_next:
                        escape_next = False
                        continue
                    
                    if c == '\\' and in_string:
                        escape_next = True
                        continue
                    
                    if c == '"' and not escape_next:
                        in_string = not in_string
                        continue
                    
                    if in_string:
                        continue
                    
                    if c == char:
                        depth += 1
                    elif c == end_char:
                        depth -= 1
                        if depth == 0:
                            return text[i:j+1]
        
        return None
    
    def parse(self, text: str) -> T:
        """Parse text output into a validated Pydantic model instance.
        
        Args:
            text: Raw text output from an LLM
            
        Returns:
            Validated Pydantic model instance
            
        Raises:
            JsonParseError: If JSON extraction or parsing fails
            ValidationParseError: If Pydantic validation fails
        """
        # Extract JSON from the text
        json_str = self._extract_json(text)
        
        # Parse JSON
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise JsonParseError(
                f"Invalid JSON: {e.msg}",
                raw_output=text,
                position=e.pos
            )
        
        # Validate with Pydantic
        try:
            return self.pydantic_model.model_validate(data)
        except PydanticValidationError as e:
            errors = e.errors()
            error_messages = []
            for err in errors:
                loc = ".".join(str(x) for x in err["loc"])
                msg = err["msg"]
                error_messages.append(f"  - {loc}: {msg}")
            
            raise ValidationParseError(
                f"Validation failed for {self.pydantic_model.__name__}:\n" +
                "\n".join(error_messages),
                errors=errors,
                raw_output=text
            )
    
    def parse_safe(self, text: str) -> Union[T, OutputParserError]:
        """Parse text without raising exceptions.
        
        Args:
            text: Raw text output from an LLM
            
        Returns:
            Either the validated model instance or an OutputParserError
        """
        try:
            return self.parse(text)
        except OutputParserError as e:
            return e
    
    def get_format_instructions(self) -> str:
        """Get instructions for the LLM on how to format output.
        
        Returns:
            A string describing the expected JSON format based on the Pydantic model
        """
        schema = self.pydantic_model.model_json_schema()
        schema_str = json.dumps(schema, indent=2)
        
        return (
            f"Your response must be valid JSON that conforms to this schema:\n"
            f"```json\n{schema_str}\n```\n\n"
            f"Respond with only the JSON object, no additional text."
        )



class ListOutputParser(OutputParser[List[T]]):
    """Parser for JSON arrays of Pydantic models.
    
    ListOutputParser extracts a JSON array from LLM output and validates
    each element against a Pydantic model.
    
    Example:
        >>> class Feature(BaseModel):
        ...     name: str
        >>> parser = ListOutputParser(Feature)
        >>> result = parser.parse('[{"name": "Login"}, {"name": "Logout"}]')
        >>> len(result)
        2
    """
    
    def __init__(self, item_model: Type[T]) -> None:
        """Initialize the parser with a Pydantic model for list items.
        
        Args:
            item_model: The Pydantic model class for each list item
        """
        self.item_model = item_model
        self._json_parser = JsonOutputParser(item_model)
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON array from text."""
        return self._json_parser._extract_json(text)
    
    def parse(self, text: str) -> List[T]:
        """Parse text output into a list of validated Pydantic model instances.
        
        Args:
            text: Raw text output from an LLM
            
        Returns:
            List of validated Pydantic model instances
            
        Raises:
            JsonParseError: If JSON extraction or parsing fails
            ValidationParseError: If Pydantic validation fails for any item
        """
        json_str = self._extract_json(text)
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise JsonParseError(
                f"Invalid JSON: {e.msg}",
                raw_output=text,
                position=e.pos
            )
        
        if not isinstance(data, list):
            raise JsonParseError(
                f"Expected JSON array, got {type(data).__name__}",
                raw_output=text
            )
        
        results = []
        all_errors = []
        
        for i, item in enumerate(data):
            try:
                validated = self.item_model.model_validate(item)
                results.append(validated)
            except PydanticValidationError as e:
                for err in e.errors():
                    err_copy = err.copy()
                    err_copy["loc"] = (i,) + err["loc"]
                    all_errors.append(err_copy)
        
        if all_errors:
            error_messages = []
            for err in all_errors:
                loc = ".".join(str(x) for x in err["loc"])
                msg = err["msg"]
                error_messages.append(f"  - [{loc}]: {msg}")
            
            raise ValidationParseError(
                f"Validation failed for list of {self.item_model.__name__}:\n" +
                "\n".join(error_messages),
                errors=all_errors,
                raw_output=text
            )
        
        return results
    
    def get_format_instructions(self) -> str:
        """Get instructions for the LLM on how to format output."""
        schema = self.item_model.model_json_schema()
        schema_str = json.dumps(schema, indent=2)
        
        return (
            f"Your response must be a JSON array where each item conforms to this schema:\n"
            f"```json\n{schema_str}\n```\n\n"
            f"Respond with only the JSON array, no additional text."
        )


# =============================================================================
# Predefined Pydantic Models for AITEA
# =============================================================================

class ExtractedFeature(BaseModel):
    """A feature extracted from a project description."""
    name: str = Field(description="Concise feature name")
    team: str = Field(description="Team responsible: backend, frontend, fullstack, design, qa, devops")
    estimated_hours: float = Field(description="Initial time estimate in hours", gt=0)
    description: Optional[str] = Field(default=None, description="Brief description of the feature")


class FeatureExtractionResponse(BaseModel):
    """Response from feature extraction."""
    features: List[ExtractedFeature] = Field(description="List of extracted features")


class EstimationResponse(BaseModel):
    """Response from feature estimation."""
    estimated_hours: float = Field(description="Estimated time in hours", gt=0)
    confidence: str = Field(description="Confidence level: low, medium, or high")
    reasoning: Optional[str] = Field(default=None, description="Explanation of the estimate")


class ProjectEstimationResponse(BaseModel):
    """Response from project estimation."""
    total_hours: float = Field(description="Total estimated hours", ge=0)
    confidence: str = Field(description="Overall confidence level")
    breakdown: List[Dict[str, Any]] = Field(description="Feature-by-feature breakdown")
    risks: Optional[List[str]] = Field(default=None, description="Potential risks")


class BRDFeature(BaseModel):
    """A feature extracted from a BRD."""
    id: str = Field(description="Unique feature identifier (e.g., F001)")
    name: str = Field(description="Feature name")
    priority: str = Field(description="Priority: high, medium, or low")
    description: str = Field(description="Feature description")
    acceptance_criteria: Optional[List[str]] = Field(default=None, description="Acceptance criteria")


class BRDParseResponse(BaseModel):
    """Response from BRD parsing."""
    title: str = Field(description="Project title")
    description: str = Field(description="Project summary")
    features: List[BRDFeature] = Field(description="Extracted features")
    requirements: Optional[List[str]] = Field(default=None, description="Functional requirements")
    non_functional: Optional[List[str]] = Field(default=None, description="Non-functional requirements")
    constraints: Optional[List[str]] = Field(default=None, description="Project constraints")
    assumptions: Optional[List[str]] = Field(default=None, description="Project assumptions")


# =============================================================================
# Predefined Parsers
# =============================================================================

# Parser for feature extraction responses
feature_extraction_parser = JsonOutputParser(FeatureExtractionResponse)

# Parser for single feature estimation
estimation_parser = JsonOutputParser(EstimationResponse)

# Parser for project estimation
project_estimation_parser = JsonOutputParser(ProjectEstimationResponse)

# Parser for BRD parsing
brd_parser = JsonOutputParser(BRDParseResponse)

# Parser for list of features (alternative format)
feature_list_parser = ListOutputParser(ExtractedFeature)


def get_parser(name: str) -> OutputParser:
    """Get a predefined parser by name.
    
    Args:
        name: Parser name (feature_extraction, estimation, project_estimation, brd)
        
    Returns:
        The requested parser
        
    Raises:
        KeyError: If the parser name is not found
    """
    parsers = {
        "feature_extraction": feature_extraction_parser,
        "estimation": estimation_parser,
        "project_estimation": project_estimation_parser,
        "brd": brd_parser,
        "feature_list": feature_list_parser,
    }
    
    if name not in parsers:
        available = ", ".join(sorted(parsers.keys()))
        raise KeyError(f"Parser '{name}' not found. Available parsers: {available}")
    
    return parsers[name]


def list_parsers() -> List[str]:
    """List all available parser names.
    
    Returns:
        List of parser names
    """
    return ["feature_extraction", "estimation", "project_estimation", "brd", "feature_list"]
