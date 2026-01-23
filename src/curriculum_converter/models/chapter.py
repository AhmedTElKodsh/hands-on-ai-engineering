"""
Chapter and content analysis data models.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from src.curriculum_converter.models.enums import TierLevel, ConversionStatus


@dataclass
class ChapterFile:
    """
    Metadata about a curriculum chapter file.
    
    Attributes:
        path: Path to the chapter markdown file
        phase: Phase name (e.g., 'phase-0-foundations')
        chapter_number: Chapter identifier (e.g., '06B')
        title: Chapter title
        tier: Difficulty tier level for scaffolding
        has_complete_solutions: Whether chapter contains complete implementations
        status: Current conversion status
    """
    path: Path
    phase: str
    chapter_number: str
    title: str
    tier: TierLevel
    has_complete_solutions: bool
    status: ConversionStatus = ConversionStatus.NOT_STARTED


@dataclass
class CodeBlock:
    """
    A code block extracted from a chapter.
    
    Attributes:
        content: The code content
        language: Programming language (e.g., 'python')
        start_line: Starting line number in the chapter
        end_line: Ending line number in the chapter
        block_type: Type of code ('function', 'class', 'algorithm', 'test')
    """
    content: str
    language: str
    start_line: int
    end_line: int
    block_type: str


@dataclass
class ContentAnalysis:
    """
    Analysis of chapter content structure.
    
    Attributes:
        function_count: Number of function implementations found
        class_count: Number of class implementations found
        algorithm_count: Number of algorithm implementations found
        test_count: Number of test implementations found
        educational_sections: List of educational section titles
        code_blocks: List of all code blocks in the chapter
    """
    function_count: int
    class_count: int
    algorithm_count: int
    test_count: int
    educational_sections: List[str] = field(default_factory=list)
    code_blocks: List[CodeBlock] = field(default_factory=list)
