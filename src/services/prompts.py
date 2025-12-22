"""Prompt template system for LLM interactions.

This module provides a PromptTemplate class for creating and managing
prompt templates with variable substitution. It supports system/user
messages, few-shot examples, and chain-of-thought patterns.

The PromptTemplate class enables:
- Variable substitution using {variable_name} syntax
- Validation of required variables
- Few-shot example formatting
- Chain-of-thought prompt patterns
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


class PromptTemplateError(Exception):
    """Base exception for prompt template errors."""
    pass


class MissingVariableError(PromptTemplateError):
    """Raised when required variables are missing during formatting."""
    
    def __init__(self, missing_vars: Set[str], template_name: Optional[str] = None):
        self.missing_vars = missing_vars
        self.template_name = template_name
        name_part = f" in template '{template_name}'" if template_name else ""
        super().__init__(
            f"Missing required variables{name_part}: {', '.join(sorted(missing_vars))}"
        )


@dataclass
class Example:
    """A few-shot example for prompt templates.
    
    Attributes:
        input: The example input text
        output: The expected output text
        explanation: Optional explanation of the example
    """
    input: str
    output: str
    explanation: Optional[str] = None
    
    def format(self, input_label: str = "Input", output_label: str = "Output") -> str:
        """Format the example as a string.
        
        Args:
            input_label: Label for the input section
            output_label: Label for the output section
            
        Returns:
            Formatted example string
        """
        parts = [f"{input_label}: {self.input}", f"{output_label}: {self.output}"]
        if self.explanation:
            parts.append(f"Explanation: {self.explanation}")
        return "\n".join(parts)


@dataclass
class PromptTemplate:
    """A template for generating prompts with variable substitution.
    
    PromptTemplate supports variable substitution using {variable_name} syntax.
    Variables are validated during formatting to ensure all required variables
    are provided.
    
    Attributes:
        template: The template string with {variable} placeholders
        name: Optional name for the template (for error messages)
        description: Optional description of the template's purpose
        examples: Optional list of few-shot examples
        input_variables: Set of variable names extracted from the template
        
    Example:
        >>> template = PromptTemplate(
        ...     template="Extract features from: {description}",
        ...     name="feature_extraction"
        ... )
        >>> result = template.format(description="User login system")
        >>> print(result)
        Extract features from: User login system
        
        >>> # With few-shot examples
        >>> template = PromptTemplate(
        ...     template="Extract features from: {description}",
        ...     examples=[
        ...         Example(input="Shopping cart", output='["Cart", "Checkout"]')
        ...     ]
        ... )
    """
    template: str
    name: Optional[str] = None
    description: Optional[str] = None
    examples: List[Example] = field(default_factory=list)
    input_variables: Set[str] = field(default_factory=set, init=False)
    
    # Regex pattern to find {variable_name} placeholders
    _VAR_PATTERN: re.Pattern[str] = field(
        default=re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'),
        init=False,
        repr=False
    )
    
    def __post_init__(self) -> None:
        """Extract input variables from the template after initialization."""
        self.input_variables = self._extract_variables(self.template)
    
    def _extract_variables(self, text: str) -> Set[str]:
        """Extract variable names from a template string.
        
        Args:
            text: The template string to extract variables from
            
        Returns:
            Set of variable names found in the template
        """
        return set(self._VAR_PATTERN.findall(text))
    
    def format(self, **kwargs: Any) -> str:
        """Format the template with the provided variables.
        
        Args:
            **kwargs: Variable values to substitute into the template
            
        Returns:
            The formatted template string with all variables replaced
            
        Raises:
            MissingVariableError: If required variables are not provided
            
        Example:
            >>> template = PromptTemplate(template="Hello, {name}!")
            >>> template.format(name="World")
            'Hello, World!'
        """
        provided_vars = set(kwargs.keys())
        missing_vars = self.input_variables - provided_vars
        
        if missing_vars:
            raise MissingVariableError(missing_vars, self.template_name)
        
        return self.template.format(**kwargs)
    
    @property
    def template_name(self) -> Optional[str]:
        """Get the template name for error messages."""
        return self.name
    
    def format_with_examples(
        self,
        examples_header: str = "Examples:",
        input_label: str = "Input",
        output_label: str = "Output",
        **kwargs: Any
    ) -> str:
        """Format the template with examples prepended.
        
        This method formats the template and prepends any configured
        few-shot examples, creating a complete prompt with examples.
        
        Args:
            examples_header: Header text before examples section
            input_label: Label for example inputs
            output_label: Label for example outputs
            **kwargs: Variable values to substitute into the template
            
        Returns:
            The formatted template with examples prepended
            
        Example:
            >>> template = PromptTemplate(
            ...     template="Extract features: {description}",
            ...     examples=[Example(input="Cart", output='["Cart"]')]
            ... )
            >>> result = template.format_with_examples(description="Login")
        """
        parts = []
        
        if self.examples:
            parts.append(examples_header)
            for i, example in enumerate(self.examples, 1):
                parts.append(f"\nExample {i}:")
                parts.append(example.format(input_label, output_label))
            parts.append("\n")
        
        parts.append(self.format(**kwargs))
        return "\n".join(parts)
    
    def partial(self, **kwargs: Any) -> "PromptTemplate":
        """Create a new template with some variables pre-filled.
        
        Args:
            **kwargs: Variable values to pre-fill
            
        Returns:
            A new PromptTemplate with the specified variables substituted
            
        Example:
            >>> template = PromptTemplate(template="{greeting}, {name}!")
            >>> partial = template.partial(greeting="Hello")
            >>> partial.format(name="World")
            'Hello, World!'
        """
        new_template = self.template.format_map(
            _PartialFormatDict(kwargs)
        )
        return PromptTemplate(
            template=new_template,
            name=self.name,
            description=self.description,
            examples=self.examples.copy()
        )
    
    def add_example(self, example: Example) -> "PromptTemplate":
        """Add an example to the template and return a new template.
        
        Args:
            example: The example to add
            
        Returns:
            A new PromptTemplate with the example added
        """
        new_examples = self.examples.copy()
        new_examples.append(example)
        return PromptTemplate(
            template=self.template,
            name=self.name,
            description=self.description,
            examples=new_examples
        )
    
    def validate(self, **kwargs: Any) -> bool:
        """Check if the provided variables are sufficient for formatting.
        
        Args:
            **kwargs: Variable values to check
            
        Returns:
            True if all required variables are provided, False otherwise
        """
        provided_vars = set(kwargs.keys())
        return self.input_variables.issubset(provided_vars)


class _PartialFormatDict(dict):
    """A dict subclass that returns the key as {key} for missing keys.
    
    Used by PromptTemplate.partial() to allow partial formatting.
    """
    
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


@dataclass
class MessageTemplate:
    """A template for a single chat message.
    
    Attributes:
        role: The role of the message sender (system, user, assistant)
        content: The message content template with {variable} placeholders
    """
    role: str
    content: str
    
    def format(self, **kwargs: Any) -> Dict[str, str]:
        """Format the message template with variables.
        
        Args:
            **kwargs: Variable values to substitute
            
        Returns:
            Dictionary with 'role' and 'content' keys
        """
        return {
            "role": self.role,
            "content": self.content.format(**kwargs)
        }
    
    def get_variables(self) -> Set[str]:
        """Extract variable names from the content template."""
        pattern = re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}')
        return set(pattern.findall(self.content))


@dataclass
class ChatPromptTemplate:
    """A template for multi-message chat prompts.
    
    ChatPromptTemplate manages a sequence of message templates for
    creating chat-style prompts with system, user, and assistant messages.
    
    Attributes:
        messages: List of MessageTemplate objects
        name: Optional name for the template
        description: Optional description
        
    Example:
        >>> template = ChatPromptTemplate.from_messages([
        ...     ("system", "You are a helpful assistant."),
        ...     ("user", "Extract features from: {description}")
        ... ])
        >>> messages = template.format_messages(description="Login system")
        >>> print(messages[0])
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    """
    messages: List[MessageTemplate]
    name: Optional[str] = None
    description: Optional[str] = None
    
    @classmethod
    def from_messages(
        cls,
        messages: List[tuple],
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> "ChatPromptTemplate":
        """Create a ChatPromptTemplate from a list of (role, content) tuples.
        
        Args:
            messages: List of (role, content) tuples
            name: Optional template name
            description: Optional description
            
        Returns:
            A new ChatPromptTemplate instance
            
        Example:
            >>> template = ChatPromptTemplate.from_messages([
            ...     ("system", "You are an expert."),
            ...     ("user", "Analyze: {text}")
            ... ])
        """
        message_templates = [
            MessageTemplate(role=role, content=content)
            for role, content in messages
        ]
        return cls(messages=message_templates, name=name, description=description)
    
    @property
    def input_variables(self) -> Set[str]:
        """Get all input variables from all message templates."""
        variables: Set[str] = set()
        for msg in self.messages:
            variables.update(msg.get_variables())
        return variables
    
    def format_messages(self, **kwargs: Any) -> List[Dict[str, str]]:
        """Format all message templates with the provided variables.
        
        Args:
            **kwargs: Variable values to substitute
            
        Returns:
            List of formatted message dictionaries
            
        Raises:
            MissingVariableError: If required variables are not provided
        """
        provided_vars = set(kwargs.keys())
        missing_vars = self.input_variables - provided_vars
        
        if missing_vars:
            raise MissingVariableError(missing_vars, self.name)
        
        return [msg.format(**kwargs) for msg in self.messages]
    
    def format(self, **kwargs: Any) -> str:
        """Format all messages and join them as a single string.
        
        This is useful for non-chat LLM APIs that expect a single prompt.
        
        Args:
            **kwargs: Variable values to substitute
            
        Returns:
            All messages joined with newlines
        """
        messages = self.format_messages(**kwargs)
        parts = []
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"]
            parts.append(f"[{role}]\n{content}")
        return "\n\n".join(parts)
    
    def validate(self, **kwargs: Any) -> bool:
        """Check if the provided variables are sufficient for formatting.
        
        Args:
            **kwargs: Variable values to check
            
        Returns:
            True if all required variables are provided
        """
        provided_vars = set(kwargs.keys())
        return self.input_variables.issubset(provided_vars)


# Chain-of-thought prompt helpers

def create_cot_prompt(
    task_description: str,
    steps: Optional[List[str]] = None,
    final_instruction: str = "Provide your final answer."
) -> PromptTemplate:
    """Create a chain-of-thought prompt template.
    
    Chain-of-thought prompting encourages the LLM to break down
    complex problems into steps before providing a final answer.
    
    Args:
        task_description: Description of the task to perform
        steps: Optional list of reasoning steps to include
        final_instruction: Instruction for the final answer
        
    Returns:
        A PromptTemplate configured for chain-of-thought reasoning
        
    Example:
        >>> template = create_cot_prompt(
        ...     task_description="Estimate the time for: {feature}",
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
    
    parts.append("")
    parts.append(final_instruction)
    
    return PromptTemplate(
        template="\n".join(parts),
        name="chain_of_thought",
        description="Chain-of-thought reasoning prompt"
    )


def create_few_shot_prompt(
    instruction: str,
    examples: List[Example],
    input_template: str = "{input}",
    name: Optional[str] = None
) -> PromptTemplate:
    """Create a few-shot prompt template with examples.
    
    Few-shot prompting provides examples to guide the LLM's responses.
    
    Args:
        instruction: The main instruction for the task
        examples: List of Example objects to include
        input_template: Template for the actual input
        name: Optional template name
        
    Returns:
        A PromptTemplate with examples configured
        
    Example:
        >>> template = create_few_shot_prompt(
        ...     instruction="Extract features from the description.",
        ...     examples=[
        ...         Example(input="Shopping cart", output='["Cart", "Checkout"]'),
        ...         Example(input="User login", output='["Auth", "Session"]')
        ...     ],
        ...     input_template="{description}"
        ... )
    """
    return PromptTemplate(
        template=f"{instruction}\n\n{input_template}",
        name=name or "few_shot",
        description="Few-shot learning prompt",
        examples=examples
    )


# =============================================================================
# Predefined Templates for AITEA
# =============================================================================

# Feature Extraction Templates
# -----------------------------------------------------------------------------

FEATURE_EXTRACTION_SYSTEM = """You are a software project analyst specializing in feature extraction.
Your task is to identify and extract software features from project descriptions.

For each feature, provide:
- name: A concise feature name
- team: The team responsible (backend, frontend, fullstack, design, qa, devops)
- estimated_hours: Initial time estimate in hours
- description: Brief description of the feature

Output your response as valid JSON."""

FEATURE_EXTRACTION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", FEATURE_EXTRACTION_SYSTEM),
        ("user", "Extract features from the following project description:\n\n{description}")
    ],
    name="feature_extraction",
    description="Extract software features from project descriptions"
)

FEATURE_EXTRACTION_WITH_CONTEXT = ChatPromptTemplate.from_messages(
    [
        ("system", FEATURE_EXTRACTION_SYSTEM),
        ("user", """Context about the project:
Team size: {team_size}
Project type: {project_type}
Timeline: {timeline}

Extract features from the following description:

{description}""")
    ],
    name="feature_extraction_with_context",
    description="Extract features with additional project context"
)


# Estimation Templates
# -----------------------------------------------------------------------------

ESTIMATION_SYSTEM = """You are a senior software developer with extensive experience in project estimation.
Your task is to provide accurate time estimates for software features based on:
- Feature complexity
- Historical data when available
- Team composition and experience
- Technical requirements

Provide estimates in hours and include confidence levels (low, medium, high)."""

ESTIMATION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", ESTIMATION_SYSTEM),
        ("user", """Estimate the time required for the following feature:

Feature: {feature_name}
Description: {feature_description}
Team: {team_type}

{historical_context}

Provide your estimate in JSON format with:
- estimated_hours: number
- confidence: "low" | "medium" | "high"
- reasoning: brief explanation""")
    ],
    name="feature_estimation",
    description="Estimate time for a single feature"
)

PROJECT_ESTIMATION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", ESTIMATION_SYSTEM),
        ("user", """Estimate the total time for the following project:

Project: {project_name}
Features:
{features_list}

Team composition: {team_composition}

Provide your estimate in JSON format with:
- total_hours: number
- confidence: "low" | "medium" | "high"
- breakdown: list of feature estimates
- risks: potential risks that could affect the estimate""")
    ],
    name="project_estimation",
    description="Estimate time for an entire project"
)

ESTIMATION_COT_TEMPLATE = PromptTemplate(
    template="""Estimate the time required for: {feature_name}

Let's think step by step:

1. **Identify the core components**: What are the main parts of this feature?
2. **Consider complexity factors**: What makes this feature simple or complex?
3. **Check for dependencies**: Does this feature depend on other features?
4. **Review historical data**: {historical_data}
5. **Account for unknowns**: What uncertainties exist?

Based on this analysis, provide your estimate:
- Estimated hours: 
- Confidence level: 
- Key assumptions: """,
    name="estimation_chain_of_thought",
    description="Chain-of-thought estimation prompt"
)


# BRD Parsing Templates
# -----------------------------------------------------------------------------

BRD_PARSING_SYSTEM = """You are a business analyst expert at parsing Business Requirements Documents (BRDs).
Your task is to extract structured information from BRD documents including:
- Project title and description
- Functional requirements
- Non-functional requirements
- Features and user stories
- Constraints and assumptions
- Success criteria

Output your response as valid JSON."""

BRD_PARSING_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", BRD_PARSING_SYSTEM),
        ("user", """Parse the following Business Requirements Document and extract structured information:

{brd_content}

Provide your response in JSON format with:
- title: project title
- description: project summary
- features: list of features with name, priority, and description
- requirements: list of functional requirements
- non_functional: list of non-functional requirements
- constraints: list of constraints
- assumptions: list of assumptions""")
    ],
    name="brd_parsing",
    description="Parse Business Requirements Documents"
)

BRD_FEATURE_EXTRACTION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", BRD_PARSING_SYSTEM),
        ("user", """From the following BRD section, extract only the features:

{brd_section}

For each feature provide:
- id: unique identifier (F001, F002, etc.)
- name: feature name
- priority: high, medium, or low
- description: brief description
- acceptance_criteria: list of acceptance criteria""")
    ],
    name="brd_feature_extraction",
    description="Extract features from BRD sections"
)


# Few-Shot Examples for Templates
# -----------------------------------------------------------------------------

FEATURE_EXTRACTION_EXAMPLES = [
    Example(
        input="Build a user authentication system with login, registration, and password reset",
        output="""{
  "features": [
    {"name": "User Login", "team": "backend", "estimated_hours": 8, "description": "Implement secure login with session management"},
    {"name": "User Registration", "team": "backend", "estimated_hours": 6, "description": "Create registration flow with email verification"},
    {"name": "Password Reset", "team": "backend", "estimated_hours": 4, "description": "Implement password reset via email"}
  ]
}""",
        explanation="Authentication features typically involve backend work with security considerations"
    ),
    Example(
        input="Create a dashboard with charts showing sales data and user metrics",
        output="""{
  "features": [
    {"name": "Dashboard Layout", "team": "frontend", "estimated_hours": 6, "description": "Create responsive dashboard layout"},
    {"name": "Sales Charts", "team": "frontend", "estimated_hours": 8, "description": "Implement interactive sales visualization"},
    {"name": "User Metrics", "team": "fullstack", "estimated_hours": 10, "description": "Build user analytics with backend aggregation"}
  ]
}""",
        explanation="Dashboard features span frontend visualization and backend data processing"
    )
]

ESTIMATION_EXAMPLES = [
    Example(
        input="CRUD API for products",
        output="""{
  "estimated_hours": 4,
  "confidence": "high",
  "reasoning": "Standard CRUD operations with well-defined patterns"
}""",
        explanation="CRUD operations are well-understood with predictable effort"
    ),
    Example(
        input="Real-time collaborative editing",
        output="""{
  "estimated_hours": 40,
  "confidence": "low",
  "reasoning": "Complex feature requiring WebSocket implementation, conflict resolution, and extensive testing"
}""",
        explanation="Real-time features have high complexity and uncertainty"
    )
]


# Template Registry
# -----------------------------------------------------------------------------

TEMPLATES = {
    # Feature extraction
    "feature_extraction": FEATURE_EXTRACTION_TEMPLATE,
    "feature_extraction_with_context": FEATURE_EXTRACTION_WITH_CONTEXT,
    
    # Estimation
    "feature_estimation": ESTIMATION_TEMPLATE,
    "project_estimation": PROJECT_ESTIMATION_TEMPLATE,
    "estimation_cot": ESTIMATION_COT_TEMPLATE,
    
    # BRD parsing
    "brd_parsing": BRD_PARSING_TEMPLATE,
    "brd_feature_extraction": BRD_FEATURE_EXTRACTION_TEMPLATE,
}


def get_template(name: str) -> PromptTemplate | ChatPromptTemplate:
    """Get a predefined template by name.
    
    Args:
        name: The template name
        
    Returns:
        The requested template
        
    Raises:
        KeyError: If the template name is not found
        
    Example:
        >>> template = get_template("feature_extraction")
        >>> messages = template.format_messages(description="Build a login system")
    """
    if name not in TEMPLATES:
        available = ", ".join(sorted(TEMPLATES.keys()))
        raise KeyError(f"Template '{name}' not found. Available templates: {available}")
    return TEMPLATES[name]


def list_templates() -> List[str]:
    """List all available template names.
    
    Returns:
        List of template names
    """
    return list(TEMPLATES.keys())
