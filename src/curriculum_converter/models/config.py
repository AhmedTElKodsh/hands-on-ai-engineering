"""
Configuration and error handling data models.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from src.curriculum_converter.models.chapter import ChapterFile


@dataclass
class ConversionConfig:
    """
    Configuration for conversion behavior.
    
    Attributes:
        tier_1_hint_detail: Detail level for Tier 1 hints ('detailed', 'moderate', 'minimal')
        tier_2_hint_detail: Detail level for Tier 2 hints
        tier_3_hint_detail: Detail level for Tier 3 hints
        max_implementation_lines: Maximum lines of logic before flagging as solution
        min_type_hint_coverage: Minimum percentage of functions with type hints (0.0-1.0)
        min_quality_score: Minimum acceptable quality score (0.0-1.0)
        batch_size: Number of chapters to process before checkpoint
        auto_verify: Whether to run verification after each conversion
        create_backup: Whether to backup original before conversion
        output_suffix: Suffix for converted files
    """
    tier_1_hint_detail: str = "detailed"
    tier_2_hint_detail: str = "moderate"
    tier_3_hint_detail: str = "minimal"
    max_implementation_lines: int = 5
    min_type_hint_coverage: float = 0.95
    min_quality_score: float = 0.80
    batch_size: int = 5
    auto_verify: bool = True
    create_backup: bool = True
    output_suffix: str = "-SCAFFOLDED"


@dataclass
class ConversionError:
    """
    An error that occurred during conversion.
    
    Attributes:
        chapter: The chapter being converted when error occurred
        error_type: Type of error (e.g., 'parsing_error', 'validation_error')
        error_message: Detailed error message
        line_number: Line number where error occurred (if applicable)
        code_snippet: Code snippet related to the error (if applicable)
        severity: Severity level ('critical', 'warning', 'info')
        suggested_action: Suggested action to resolve the error
    """
    chapter: ChapterFile
    error_type: str
    error_message: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    severity: str = "critical"
    suggested_action: str = ""


@dataclass
class ErrorReport:
    """
    Report of errors encountered during batch conversion.
    
    Attributes:
        total_errors: Total number of errors encountered
        critical_errors: List of critical errors
        warnings: List of warnings
        chapters_affected: List of chapters that had errors
        recovery_suggestions: List of suggestions for recovering from errors
    """
    total_errors: int
    critical_errors: List[ConversionError] = field(default_factory=list)
    warnings: List[ConversionError] = field(default_factory=list)
    chapters_affected: List[ChapterFile] = field(default_factory=list)
    recovery_suggestions: List[str] = field(default_factory=list)
