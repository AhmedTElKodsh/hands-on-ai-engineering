"""
Data models for the curriculum scaffolding conversion system.

This module defines all core data structures used throughout the conversion
process, including enums, dataclasses for chapters, code blocks, scaffolding,
quality reports, and progress tracking.
"""

from src.curriculum_converter.models.enums import TierLevel, ConversionStatus
from src.curriculum_converter.models.chapter import ChapterFile, CodeBlock, ContentAnalysis
from src.curriculum_converter.models.scaffolding import ScaffoldedCode, Hint
from src.curriculum_converter.models.quality import (
    SolutionViolation,
    TypeHintReport,
    HintQualityReport,
    ConsistencyReport,
)
from src.curriculum_converter.models.preservation import Section, PreservationReport
from src.curriculum_converter.models.tracking import PhaseReport, FinalReport
from src.curriculum_converter.models.config import ConversionConfig, ConversionError, ErrorReport

__all__ = [
    # Enums
    "TierLevel",
    "ConversionStatus",
    # Chapter models
    "ChapterFile",
    "CodeBlock",
    "ContentAnalysis",
    # Scaffolding models
    "ScaffoldedCode",
    "Hint",
    # Quality models
    "SolutionViolation",
    "TypeHintReport",
    "HintQualityReport",
    "ConsistencyReport",
    # Preservation models
    "Section",
    "PreservationReport",
    # Tracking models
    "PhaseReport",
    "FinalReport",
    # Config models
    "ConversionConfig",
    "ConversionError",
    "ErrorReport",
]
