"""
Progress tracking and reporting data models.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PhaseReport:
    """
    Conversion report for a single phase.
    
    Attributes:
        phase_name: Name of the phase (e.g., 'phase-0-foundations')
        total_chapters: Total number of chapters in the phase
        completed_chapters: Number of chapters successfully converted
        chapters_needing_review: Number of chapters flagged for review
        conversion_rate: Percentage of chapters completed (0.0-1.0)
        quality_metrics: Dictionary of quality metric names to values
    """
    phase_name: str
    total_chapters: int
    completed_chapters: int
    chapters_needing_review: int
    conversion_rate: float
    quality_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class FinalReport:
    """
    Overall conversion report across all phases.
    
    Attributes:
        total_chapters: Total number of chapters across all phases
        completed_chapters: Total number of chapters successfully converted
        total_functions_converted: Total number of functions converted
        total_classes_converted: Total number of classes converted
        total_algorithms_converted: Total number of algorithms converted
        total_tests_converted: Total number of tests converted
        phase_reports: List of individual phase reports
        overall_quality_score: Overall quality score across all conversions (0.0-1.0)
    """
    total_chapters: int
    completed_chapters: int
    total_functions_converted: int
    total_classes_converted: int
    total_algorithms_converted: int
    total_tests_converted: int
    phase_reports: List[PhaseReport] = field(default_factory=list)
    overall_quality_score: float = 0.0
