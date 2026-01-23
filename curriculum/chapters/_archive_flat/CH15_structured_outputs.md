# Chapter 15: Structured Outputs

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 13-14  
**AITEA Component:** `src/services/output_parsers.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Parse JSON from LLM responses reliably
2. Validate outputs using Pydantic models
3. Handle common parsing errors gracefully
4. Create custom output parsers for different formats
5. Generate format instructions for LLMs

## 15.1 The Challenge of LLM Outputs

LLMs return unstructured text, but applications need structured data:

````python
# LLM might return any of these:
response1 = '{"name": "Login", "hours": 8}'
response2 = 'Here is the JSON:\n```json\n{"name": "Login", "hours": 8}\n```'
response3 = 'The feature is Login and it takes 8 hours.'
````

Output parsers solve this by:

1. Extracting JSON from various formats
2. Validating against a schema
3. Providing clear error messages

## 15.2 The OutputParser Base Class

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class OutputParserError(Exception):
    """Base exception for parsing errors."""
    pass


class JsonParseError(OutputParserError):
    """Raised when JSON parsing fails."""
    def __init__(self, message: str, raw_output: str, position: int = None):
        self.raw_output = raw_output
        self.position = position
        super().__init__(message)


class ValidationParseError(OutputParserError):
    """Raised when Pydantic validation fails."""
    def __init__(self, message: str, errors: list, raw_output: str):
        self.errors = errors
        self.raw_output = raw_output
        super().__init__(message)


class OutputParser(ABC, Generic[T]):
    """Abstract base class for output parsers."""

    @abstractmethod
    def parse(self, text: str) -> T:
        """Parse raw text into structured data."""
        ...

    @abstractmethod
    def get_format_instructions(self) -> str:
        """Get instructions for the LLM on output format."""
        ...
```

## 15.3 The JsonOutputParser

````python
import json
import re
from typing import Any, Dict, Type, Union
from pydantic import BaseModel, ValidationError as PydanticValidationError


class JsonOutputParser(OutputParser[T]):
    """Parser that extracts JSON and validates with Pydantic.

    Handles common LLM output patterns:
    - Pure JSON responses
    - JSON in markdown code blocks (```json ... ```)
    - JSON with surrounding text

    Example:
        >>> from pydantic import BaseModel
        >>> class Feature(BaseModel):
        ...     name: str
        ...     hours: float
        >>> parser = JsonOutputParser(Feature)
        >>> result = parser.parse('{"name": "Login", "hours": 8.0}')
        >>> print(result.name)
        Login
    """

    def __init__(self, pydantic_model: Type[T]) -> None:
        self.pydantic_model = pydantic_model

    def _extract_json(self, text: str) -> str:
        """Extract JSON from text, handling various formats."""
        text = text.strip()

        # Try markdown code blocks first
        code_block_pattern = r'```(?:json)?\s*\n?([\s\S]*?)\n?```'
        matches = re.findall(code_block_pattern, text)
        if matches:
            for match in matches:
                match = match.strip()
                if match.startswith('{') or match.startswith('['):
                    return match

        # If text looks like JSON, return directly
        if text.startswith('{') or text.startswith('['):
            return text

        # Try to find balanced JSON
        json_str = self._find_balanced_json(text)
        if json_str:
            return json_str

        raise JsonParseError(
            "Could not find valid JSON in output",
            raw_output=text
        )

    def _find_balanced_json(self, text: str) -> str | None:
        """Find JSON with balanced brackets."""
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
        """Parse text into validated Pydantic model."""
        # Extract JSON
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
            error_msgs = [
                f"  - {'.'.join(str(x) for x in err['loc'])}: {err['msg']}"
                for err in errors
            ]
            raise ValidationParseError(
                f"Validation failed:\n" + "\n".join(error_msgs),
                errors=errors,
                raw_output=text
            )

    def parse_safe(self, text: str) -> Union[T, OutputParserError]:
        """Parse without raising exceptions."""
        try:
            return self.parse(text)
        except OutputParserError as e:
            return e

    def get_format_instructions(self) -> str:
        """Get LLM instructions based on Pydantic schema."""
        schema = self.pydantic_model.model_json_schema()
        schema_str = json.dumps(schema, indent=2)

        return (
            f"Your response must be valid JSON matching this schema:\n"
            f"```json\n{schema_str}\n```\n\n"
            f"Respond with only the JSON object, no additional text."
        )
````

## 15.4 Pydantic Models for AITEA

Define structured response types:

```python
from pydantic import BaseModel, Field
from typing import List, Optional


class ExtractedFeature(BaseModel):
    """A feature extracted from a project description."""
    name: str = Field(description="Concise feature name")
    team: str = Field(description="Team: backend, frontend, fullstack, etc.")
    estimated_hours: float = Field(description="Time estimate in hours", gt=0)
    description: Optional[str] = Field(default=None)


class FeatureExtractionResponse(BaseModel):
    """Response from feature extraction."""
    features: List[ExtractedFeature]


class EstimationResponse(BaseModel):
    """Response from feature estimation."""
    estimated_hours: float = Field(gt=0)
    confidence: str = Field(description="low, medium, or high")
    reasoning: Optional[str] = None


class BRDFeature(BaseModel):
    """A feature from a BRD."""
    id: str = Field(description="Unique ID like F001")
    name: str
    priority: str = Field(description="high, medium, or low")
    description: str


class BRDParseResponse(BaseModel):
    """Response from BRD parsing."""
    title: str
    description: str
    features: List[BRDFeature]
    requirements: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
```

## 15.5 Using Output Parsers

```python
import asyncio
from src.services.llm import get_llm_provider
from src.services.prompts import get_template
from src.services.output_parsers import (
    JsonOutputParser,
    FeatureExtractionResponse,
    EstimationResponse
)


async def extract_features(description: str) -> FeatureExtractionResponse:
    """Extract features from a description."""
    llm = get_llm_provider()
    parser = JsonOutputParser(FeatureExtractionResponse)

    # Get template and format
    template = get_template("feature_extraction")
    messages = template.format_messages(description=description)

    # Add format instructions to system message
    messages[0]["content"] += "\n\n" + parser.get_format_instructions()

    # Get LLM response
    from src.services.llm import ChatMessage
    chat_messages = [ChatMessage(**m) for m in messages]
    response = await llm.chat(chat_messages)

    # Parse and validate
    return parser.parse(response)


async def main():
    result = await extract_features("Build a user login system with OAuth")

    print(f"Found {len(result.features)} features:")
    for feature in result.features:
        print(f"  - {feature.name}: {feature.estimated_hours}h ({feature.team})")


asyncio.run(main())
```

## 15.6 List Output Parser

For responses that are JSON arrays:

````python
class ListOutputParser(OutputParser[List[T]]):
    """Parser for JSON arrays of Pydantic models."""

    def __init__(self, item_model: Type[T]) -> None:
        self.item_model = item_model
        self._json_parser = JsonOutputParser(item_model)

    def parse(self, text: str) -> List[T]:
        """Parse text into list of validated models."""
        json_str = self._json_parser._extract_json(text)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise JsonParseError(f"Invalid JSON: {e.msg}", text, e.pos)

        if not isinstance(data, list):
            raise JsonParseError(
                f"Expected array, got {type(data).__name__}",
                text
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
            raise ValidationParseError(
                f"Validation failed for {len(all_errors)} items",
                errors=all_errors,
                raw_output=text
            )

        return results

    def get_format_instructions(self) -> str:
        schema = self.item_model.model_json_schema()
        return (
            f"Respond with a JSON array where each item matches:\n"
            f"```json\n{json.dumps(schema, indent=2)}\n```"
        )
````

## 15.7 Your Turn: Exercise 15.1

Create a parser for code review responses:

````python
class CodeIssue(BaseModel):
    """A code review issue."""
    line: int = Field(description="Line number")
    severity: str = Field(description="error, warning, or info")
    message: str = Field(description="Description of the issue")
    suggestion: Optional[str] = Field(default=None)


class CodeReviewResponse(BaseModel):
    """Response from code review."""
    issues: List[CodeIssue]
    overall_quality: str = Field(description="good, acceptable, or needs_work")
    summary: str


# Create parser and test
parser = JsonOutputParser(CodeReviewResponse)

test_response = '''```json
{
  "issues": [
    {"line": 5, "severity": "warning", "message": "Missing type hint"}
  ],
  "overall_quality": "acceptable",
  "summary": "Code is functional but needs type hints"
}
```'''

result = parser.parse(test_response)
print(f"Quality: {result.overall_quality}")
print(f"Issues: {len(result.issues)}")
````

## 15.8 Debugging Scenario

**The Bug:** Parser fails on valid-looking JSON.

```python
response = '{"name": "Test", "hours": 8}'
parser = JsonOutputParser(EstimationResponse)
result = parser.parse(response)
# ValidationParseError: estimated_hours: Field required
```

**The Problem:** Field name mismatch—model expects `estimated_hours`, JSON has `hours`.

**The Fix:** Either:

1. Update the Pydantic model to accept aliases:

```python
class EstimationResponse(BaseModel):
    estimated_hours: float = Field(alias="hours", gt=0)

    model_config = {"populate_by_name": True}
```

2. Or update the prompt to request the correct field name.

## 15.9 Quick Check Questions

1. Why extract JSON instead of parsing the whole response?
2. What does `model_validate()` do?
3. How do you handle optional fields in Pydantic?
4. What's the purpose of `get_format_instructions()`?
5. When would you use `parse_safe()` instead of `parse()`?

<details>
<summary>Answers</summary>

1. LLMs often add explanatory text around JSON; extraction handles this
2. Validates a dictionary against the Pydantic model and returns an instance
3. Use `Optional[Type]` with `default=None` or `Field(default=None)`
4. To tell the LLM exactly what JSON structure to produce
5. When you want to handle errors without try/except (returns error object)

</details>

## 15.10 Mini-Project: Retry Parser

Create a parser that retries with feedback on failure:

```python
class RetryParser(OutputParser[T]):
    """Parser that retries with error feedback."""

    def __init__(
        self,
        parser: JsonOutputParser[T],
        llm: LLMProvider,
        max_retries: int = 2
    ):
        self.parser = parser
        self.llm = llm
        self.max_retries = max_retries

    async def parse_with_retry(self, text: str, original_prompt: str) -> T:
        """Parse with automatic retry on failure."""
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                return self.parser.parse(text)
            except OutputParserError as e:
                last_error = e

                if attempt < self.max_retries:
                    # Ask LLM to fix the output
                    fix_prompt = f"""Your previous response had an error:
{str(e)}

Original request: {original_prompt}

Please provide a corrected response that matches the required format:
{self.parser.get_format_instructions()}"""

                    text = await self.llm.complete(fix_prompt)

        raise last_error

    def parse(self, text: str) -> T:
        return self.parser.parse(text)

    def get_format_instructions(self) -> str:
        return self.parser.get_format_instructions()
```

## 15.11 AITEA Integration

This chapter implements:

- **Requirement 3.3**: JSON output parser with Pydantic validation
- **Property 7**: Output Parser Round-Trip (parse → serialize → parse)

**Verification:**

````python
from src.services.output_parsers import (
    JsonOutputParser,
    ListOutputParser,
    FeatureExtractionResponse,
    ExtractedFeature,
    get_parser
)

# Test JSON extraction from code blocks
parser = JsonOutputParser(FeatureExtractionResponse)
response = '''Here are the features:
```json
{
  "features": [
    {"name": "Login", "team": "backend", "estimated_hours": 8}
  ]
}
````

'''
result = parser.parse(response)
print(f"✅ Parsed {len(result.features)} features")

# Test list parser

list_parser = ListOutputParser(ExtractedFeature)
array_response = '[{"name": "A", "team": "backend", "estimated_hours": 4}]'
features = list_parser.parse(array_response)
print(f"✅ Parsed list of {len(features)} features")

# Test format instructions

instructions = parser.get_format_instructions()
print("Format instructions generated:", len(instructions), "chars")

# Test predefined parsers

estimation_parser = get_parser("estimation")
print(f"✅ Got estimation parser: {type(estimation_parser)}")

```

## What's Next

In Chapter 16, you'll learn about tool calling patterns—how to define tools that LLMs can invoke to interact with external systems.

**Before proceeding:**
- Create parsers for your own response types
- Test with various LLM output formats
- Try the RetryParser mini-project
```
