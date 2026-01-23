"""
Scaffolding and hint data models.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Hint:
    """
    A strategic hint for guiding student implementation.
    
    Attributes:
        category: Hint category ('conceptual', 'approach', 'implementation', 'resource')
        content: The hint text
        tier_specific: Whether this hint is specific to a particular tier level
    """
    category: str
    content: str
    tier_specific: bool


@dataclass
class ScaffoldedCode:
    """
    Scaffolded code structure with guidance.
    
    Represents a complete implementation converted to educational scaffolding
    with function signatures, type hints, TODO markers, and strategic hints.
    
    Attributes:
        signature: Function or class signature
        docstring: Documentation string
        type_hints: Mapping of parameter names to type hint strings
        todo_markers: List of TODO comments for implementation steps
        hints: List of strategic hints
        preserved_code: Code to preserve (imports, constants, etc.)
    """
    signature: str
    docstring: str
    type_hints: Dict[str, str] = field(default_factory=dict)
    todo_markers: List[str] = field(default_factory=list)
    hints: List[Hint] = field(default_factory=list)
    preserved_code: str = ""
