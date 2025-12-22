# Chapter 14: Prompt Engineering

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapter 13  
**AITEA Component:** `src/services/prompts.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create reusable prompt templates with variable substitution
2. Build chat-style prompts with system/user/assistant messages
3. Implement few-shot prompting with examples
4. Use chain-of-thought (CoT) patterns for complex reasoning
5. Design effective prompts for AITEA tasks

## 14.1 Why Prompt Templates?

Hardcoding prompts leads to:

- Duplicated text across your codebase
- Inconsistent formatting
- Difficult maintenance

Prompt templates solve this:

```python
# Bad: Hardcoded prompt
prompt = f"Extract features from: {description}"

# Good: Reusable template
template = PromptTemplate(
    template="Extract features from: {description}",
    name="feature_extraction"
)
prompt = template.format(description=description)
```

## 14.2 The PromptTemplate Class

```python
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


class MissingVariableError(Exception):
    """Raised when required variables are missing."""

    def __init__(self, missing_vars: Set[str], template_name: Optional[str] = None):
        self.missing_vars = missing_vars
        name_part = f" in template '{template_name}'" if template_name else ""
        super().__init__(
            f"Missing required variables{name_part}: {', '.join(sorted(missing_vars))}"
        )


@dataclass
class PromptTemplate:
    """A template for generating prompts with variable substitution.

    Uses {variable_name} syntax for placeholders.

    Example:
        >>> template = PromptTemplate(
        ...     template="Extract features from: {description}",
        ...     name="feature_extraction"
        ... )
        >>> result = template.format(description="User login system")
        >>> print(result)
        Extract features from: User login system
    """
    template: str
    name: Optional[str] = None
    description: Optional[str] = None
    input_variables: Set[str] = field(default_factory=set, init=False)

    _VAR_PATTERN: re.Pattern[str] = field(
        default=re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'),
        init=False,
        repr=False
    )

    def __post_init__(self) -> None:
        """Extract variables from template after initialization."""
        self.input_variables = set(self._VAR_PATTERN.findall(self.template))

    def format(self, **kwargs: Any) -> str:
        """Format the template with provided variables.

        Raises:
            MissingVariableError: If required variables are missing
        """
        provided = set(kwargs.keys())
        missing = self.input_variables - provided

        if missing:
            raise MissingVariableError(missing, self.name)

        return self.template.format(**kwargs)

    def validate(self, **kwargs: Any) -> bool:
        """Check if provided variables are sufficient."""
        return self.input_variables.issubset(set(kwargs.keys()))

    def partial(self, **kwargs: Any) -> "PromptTemplate":
        """Create a new template with some variables pre-filled."""
        new_template = self.template.format_map(_PartialFormatDict(kwargs))
        return PromptTemplate(
            template=new_template,
            name=self.name,
            description=self.description,
        )


class _PartialFormatDict(dict):
    """Dict that returns {key} for missing keys (for partial formatting)."""
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"
```

## 14.3 Chat Prompt Templates

For chat-style LLMs, we need system/user/assistant message sequences:

```python
@dataclass
class MessageTemplate:
    """A template for a single chat message."""
    role: str  # "system", "user", or "assistant"
    content: str

    def format(self, **kwargs: Any) -> Dict[str, str]:
        """Format the message with variables."""
        return {
            "role": self.role,
            "content": self.content.format(**kwargs)
        }

    def get_variables(self) -> Set[str]:
        """Extract variable names from content."""
        pattern = re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}')
        return set(pattern.findall(self.content))


@dataclass
class ChatPromptTemplate:
    """Template for multi-message chat prompts.

    Example:
        >>> template = ChatPromptTemplate.from_messages([
        ...     ("system", "You are a helpful assistant."),
        ...     ("user", "Extract features from: {description}")
        ... ])
        >>> messages = template.format_messages(description="Login system")
    """
    messages: List[MessageTemplate]
    name: Optional[str] = None

    @classmethod
    def from_messages(
        cls,
        messages: List[tuple],
        name: Optional[str] = None
    ) -> "ChatPromptTemplate":
        """Create from list of (role, content) tuples."""
        return cls(
            messages=[MessageTemplate(role=r, content=c) for r, c in messages],
            name=name
        )

    @property
    def input_variables(self) -> Set[str]:
        """Get all variables from all messages."""
        variables: Set[str] = set()
        for msg in self.messages:
            variables.update(msg.get_variables())
        return variables

    def format_messages(self, **kwargs: Any) -> List[Dict[str, str]]:
        """Format all messages with variables."""
        missing = self.input_variables - set(kwargs.keys())
        if missing:
            raise MissingVariableError(missing, self.name)

        return [msg.format(**kwargs) for msg in self.messages]
```

## 14.4 Few-Shot Prompting

Few-shot prompting provides examples to guide the LLM:

```python
@dataclass
class Example:
    """A few-shot example."""
    input: str
    output: str
    explanation: Optional[str] = None

    def format(self, input_label: str = "Input", output_label: str = "Output") -> str:
        parts = [f"{input_label}: {self.input}", f"{output_label}: {self.output}"]
        if self.explanation:
            parts.append(f"Explanation: {self.explanation}")
        return "\n".join(parts)


# Predefined examples for AITEA
FEATURE_EXTRACTION_EXAMPLES = [
    Example(
        input="Build a user authentication system with login and registration",
        output="""{
  "features": [
    {"name": "User Login", "team": "backend", "estimated_hours": 8},
    {"name": "User Registration", "team": "backend", "estimated_hours": 6}
  ]
}""",
        explanation="Authentication features are typically backend work"
    ),
    Example(
        input="Create a dashboard with sales charts",
        output="""{
  "features": [
    {"name": "Dashboard Layout", "team": "frontend", "estimated_hours": 6},
    {"name": "Sales Charts", "team": "frontend", "estimated_hours": 8}
  ]
}""",
        explanation="Dashboard features span frontend visualization"
    )
]


def create_few_shot_prompt(
    instruction: str,
    examples: List[Example],
    input_template: str = "{input}"
) -> PromptTemplate:
    """Create a few-shot prompt template."""
    parts = [instruction, ""]

    for i, example in enumerate(examples, 1):
        parts.append(f"Example {i}:")
        parts.append(example.format())
        parts.append("")

    parts.append("Now process this input:")
    parts.append(input_template)

    return PromptTemplate(template="\n".join(parts))
```

## 14.5 Chain-of-Thought Prompting

CoT prompting encourages step-by-step reasoning:

```python
def create_cot_prompt(
    task_description: str,
    steps: Optional[List[str]] = None,
    final_instruction: str = "Provide your final answer."
) -> PromptTemplate:
    """Create a chain-of-thought prompt template.

    Example:
        >>> template = create_cot_prompt(
        ...     task_description="Estimate time for: {feature}",
        ...     steps=["Identify similar features", "Check historical data"]
        ... )
    """
    parts = [task_description, "", "Let's think step by step:"]

    if steps:
        for i, step in enumerate(steps, 1):
            parts.append(f"{i}. {step}")
    else:
        parts.append("1. First, I'll analyze the problem.")
        parts.append("2. Then, I'll consider relevant factors.")
        parts.append("3. Finally, I'll synthesize my findings.")

    parts.extend(["", final_instruction])

    return PromptTemplate(
        template="\n".join(parts),
        name="chain_of_thought"
    )


# AITEA estimation with CoT
ESTIMATION_COT_TEMPLATE = PromptTemplate(
    template="""Estimate the time required for: {feature_name}

Let's think step by step:

1. **Identify the core components**: What are the main parts of this feature?
2. **Consider complexity factors**: What makes this simple or complex?
3. **Check for dependencies**: Does this depend on other features?
4. **Review historical data**: {historical_data}
5. **Account for unknowns**: What uncertainties exist?

Based on this analysis, provide your estimate:
- Estimated hours:
- Confidence level:
- Key assumptions: """,
    name="estimation_chain_of_thought"
)
```

## 14.6 AITEA Prompt Templates

AITEA includes predefined templates for common tasks:

```python
# Feature Extraction
FEATURE_EXTRACTION_SYSTEM = """You are a software project analyst.
Extract software features from project descriptions.

For each feature, provide:
- name: A concise feature name
- team: backend, frontend, fullstack, design, qa, devops
- estimated_hours: Initial time estimate
- description: Brief description

Output as valid JSON."""

FEATURE_EXTRACTION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", FEATURE_EXTRACTION_SYSTEM),
        ("user", "Extract features from:\n\n{description}")
    ],
    name="feature_extraction"
)


# Estimation
ESTIMATION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a senior developer with estimation expertise.
Provide accurate time estimates based on complexity and historical data.
Include confidence levels (low, medium, high)."""),
        ("user", """Estimate time for:

Feature: {feature_name}
Description: {feature_description}
Team: {team_type}

Historical context: {historical_context}

Respond in JSON with estimated_hours, confidence, and reasoning.""")
    ],
    name="feature_estimation"
)


# BRD Parsing
BRD_PARSING_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a business analyst expert at parsing BRDs.
Extract structured information including features, requirements, and constraints.
Output as valid JSON."""),
        ("user", """Parse this BRD and extract structured information:

{brd_content}

Provide: title, description, features, requirements, constraints.""")
    ],
    name="brd_parsing"
)


# Template Registry
TEMPLATES = {
    "feature_extraction": FEATURE_EXTRACTION_TEMPLATE,
    "feature_estimation": ESTIMATION_TEMPLATE,
    "brd_parsing": BRD_PARSING_TEMPLATE,
}


def get_template(name: str):
    """Get a predefined template by name."""
    if name not in TEMPLATES:
        available = ", ".join(sorted(TEMPLATES.keys()))
        raise KeyError(f"Template '{name}' not found. Available: {available}")
    return TEMPLATES[name]
```

## 14.7 Your Turn: Exercise 14.1

Create a prompt template for code review:

````python
CODE_REVIEW_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """You are a senior code reviewer.
Review code for:
- Bugs and potential issues
- Code style and best practices
- Performance concerns
- Security vulnerabilities

Provide specific, actionable feedback."""),
    ("user", """Review this {language} code:

```{language}
{code}
````

Focus on: {focus_areas}""")
])

# Test it

messages = CODE_REVIEW_TEMPLATE.format_messages(
language="python",
code="def add(a, b): return a + b",
focus_areas="type hints, error handling"
)

````

## 14.8 Debugging Scenario

**The Bug:** Template formatting fails with KeyError.

```python
template = PromptTemplate(template="Hello {name}, your score is {score}%")
result = template.format(name="Alice")
# KeyError: 'score'
````

**The Problem:** The `%` is being interpreted as a format specifier.

**The Fix:** Escape literal `%` with `%%`:

```python
template = PromptTemplate(template="Hello {name}, your score is {score}%%")
# Or use the validate method first:
if not template.validate(name="Alice"):
    print(f"Missing: {template.input_variables - {'name'}}")
```

## 14.9 Quick Check Questions

1. What syntax does PromptTemplate use for variables?
2. What's the difference between `format()` and `partial()`?
3. Why use ChatPromptTemplate instead of PromptTemplate?
4. What is few-shot prompting?
5. When should you use chain-of-thought prompting?

<details>
<summary>Answers</summary>

1. `{variable_name}` syntax (Python's str.format style)
2. `format()` requires all variables; `partial()` fills some and returns a new template
3. For chat-style LLMs that expect system/user/assistant message sequences
4. Providing examples in the prompt to guide the LLM's response format
5. For complex reasoning tasks where step-by-step thinking improves accuracy

</details>

## 14.10 Mini-Project: Dynamic Template Builder

Create a template builder that constructs prompts dynamically:

```python
class PromptBuilder:
    """Fluent interface for building prompts."""

    def __init__(self):
        self._system: Optional[str] = None
        self._examples: List[Example] = []
        self._instruction: str = ""
        self._output_format: Optional[str] = None

    def system(self, content: str) -> "PromptBuilder":
        self._system = content
        return self

    def add_example(self, input: str, output: str) -> "PromptBuilder":
        self._examples.append(Example(input=input, output=output))
        return self

    def instruction(self, content: str) -> "PromptBuilder":
        self._instruction = content
        return self

    def output_format(self, format: str) -> "PromptBuilder":
        self._output_format = format
        return self

    def build(self) -> ChatPromptTemplate:
        messages = []

        if self._system:
            messages.append(("system", self._system))

        user_content = []

        if self._examples:
            user_content.append("Examples:")
            for i, ex in enumerate(self._examples, 1):
                user_content.append(f"\nExample {i}:")
                user_content.append(f"Input: {ex.input}")
                user_content.append(f"Output: {ex.output}")
            user_content.append("\n")

        user_content.append(self._instruction)

        if self._output_format:
            user_content.append(f"\nOutput format: {self._output_format}")

        messages.append(("user", "\n".join(user_content)))

        return ChatPromptTemplate.from_messages(messages)


# Usage
template = (
    PromptBuilder()
    .system("You are a helpful assistant.")
    .add_example("2+2", "4")
    .add_example("3*3", "9")
    .instruction("Calculate: {expression}")
    .output_format("Just the number")
    .build()
)
```

## 14.11 AITEA Integration

This chapter implements:

- **Requirement 3.2**: PromptTemplate class with variable substitution
- **Requirement 3.2**: Templates for feature extraction, estimation, BRD parsing

**Verification:**

```python
from src.services.prompts import (
    get_template,
    create_cot_prompt,
    FEATURE_EXTRACTION_EXAMPLES
)

# Test feature extraction template
template = get_template("feature_extraction")
messages = template.format_messages(description="Build a shopping cart")
print("Messages:", messages)

# Test CoT template
cot = create_cot_prompt(
    task_description="Estimate: {feature}",
    steps=["Analyze complexity", "Check similar features"]
)
prompt = cot.format(feature="User authentication")
print("CoT prompt:", prompt)

# Test few-shot
from src.services.prompts import create_few_shot_prompt
few_shot = create_few_shot_prompt(
    instruction="Extract features from the description.",
    examples=FEATURE_EXTRACTION_EXAMPLES,
    input_template="{description}"
)
print("Few-shot template variables:", few_shot.input_variables)
```

## What's Next

In Chapter 15, you'll learn about structured outputs—how to parse LLM responses into validated Pydantic models.

**Before proceeding:**

- Create templates for your own use cases
- Experiment with few-shot examples
- Try the PromptBuilder mini-project
