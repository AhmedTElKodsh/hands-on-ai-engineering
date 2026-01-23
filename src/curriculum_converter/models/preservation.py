"""
Content preservation data models.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Section:
    """
    A section of educational content in a chapter.
    
    Attributes:
        title: Section title
        content: Section content
        start_line: Starting line number in the chapter
        end_line: Ending line number in the chapter
        section_type: Type of section (e.g., 'learning_objectives', 'concepts', 'explanation')
    """
    title: str
    content: str
    start_line: int
    end_line: int
    section_type: str


@dataclass
class PreservationReport:
    """
    Report on educational content preservation.
    
    Attributes:
        preserved_sections: Sections that remained unchanged
        modified_sections: Sections that were modified
        preservation_rate: Percentage of content preserved (0.0-1.0)
        issues: List of preservation issues found
    """
    preserved_sections: List[Section] = field(default_factory=list)
    modified_sections: List[Section] = field(default_factory=list)
    preservation_rate: float = 0.0
    issues: List[str] = field(default_factory=list)
