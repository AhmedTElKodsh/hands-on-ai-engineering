"""
Quality verification and reporting data models.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from src.curriculum_converter.models.scaffolding import Hint
from src.curriculum_converter.models.enums import TierLevel


@dataclass
class SolutionViolation:
    """
    A detected complete solution that should have been scaffolded.
    
    Attributes:
        line_number: Line number where violation was found
        code_snippet: The problematic code snippet
        violation_type: Type of violation (e.g., 'complete_function', 'full_algorithm')
        severity: Severity level ('critical', 'warning', 'info')
        description: Optional description of the violation
    """
    line_number: int
    code_snippet: str
    violation_type: str
    severity: str
    description: str = ""


@dataclass
class TypeHintReport:
    """
    Report on type hint completeness.
    
    Attributes:
        total_functions: Total number of functions analyzed
        functions_with_hints: Number of functions with complete type hints
        missing_parameter_hints: List of function names missing parameter hints
        missing_return_hints: List of function names missing return hints
        coverage_percentage: Percentage of functions with complete type hints
        issues: List of specific type hint issues found
    """
    total_functions: int
    functions_with_hints: int
    missing_parameter_hints: List[str] = field(default_factory=list)
    missing_return_hints: List[str] = field(default_factory=list)
    coverage_percentage: float = 0.0
    issues: List[str] = field(default_factory=list)


@dataclass
class HintQualityReport:
    """
    Report on hint quality assessment.
    
    Attributes:
        total_hints: Total number of hints analyzed
        hints_with_code: Hints that contain copy-paste-ready code
        vague_hints: Hints that are too vague to be actionable
        tier_mismatches: Hints that don't match expected tier level
        quality_score: Overall quality score (0.0-1.0)
        issues: List of specific quality issues found
    """
    total_hints: int
    hints_with_code: List[Hint] = field(default_factory=list)
    vague_hints: List[Hint] = field(default_factory=list)
    tier_mismatches: List[Hint] = field(default_factory=list)
    quality_score: float = 0.0
    issues: List[str] = field(default_factory=list)


@dataclass
class ConsistencyReport:
    """
    Report on tier consistency validation.
    
    Attributes:
        expected_tier: The tier level expected for the chapter
        detected_tier: The tier level detected from scaffolding analysis
        matches: Whether expected and detected tiers match
        issues: List of consistency issues found
    """
    expected_tier: TierLevel
    detected_tier: TierLevel
    matches: bool
    issues: List[str] = field(default_factory=list)
