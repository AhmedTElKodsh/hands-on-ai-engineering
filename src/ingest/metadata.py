"""Metadata extraction for document processing.

This module provides metadata extractors for enriching documents and chunks
with additional information such as source details, page numbers, sections,
titles, and headings.

Extractors:
- SourceExtractor: Extract source file information
- PageExtractor: Extract page-related metadata
- SectionExtractor: Extract section/heading information
- TitleExtractor: Extract document titles
- HeadingExtractor: Extract all headings from content
- MetadataEnrichmentPipeline: Combine multiple extractors
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import os
import re

from .models import Document, DocumentMetadata, Chunk, ChunkMetadata


class MetadataExtractor(ABC):
    """Abstract base class for metadata extractors.
    
    Metadata extractors analyze documents or chunks and extract
    specific types of metadata to enrich the data models.
    
    Subclasses must implement the extract() method to handle
    their specific extraction logic.
    """
    
    @abstractmethod
    def extract(self, content: str, existing_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract metadata from content.
        
        Args:
            content: The text content to analyze
            existing_metadata: Any existing metadata to consider
            
        Returns:
            Dictionary of extracted metadata
        """
        ...
    
    def extract_from_document(self, document: Document) -> Dict[str, Any]:
        """Extract metadata from a Document object.
        
        Args:
            document: The document to extract metadata from
            
        Returns:
            Dictionary of extracted metadata
        """
        existing = document.metadata.to_dict() if document.metadata else {}
        return self.extract(document.content, existing)
    
    def extract_from_chunk(self, chunk: Chunk) -> Dict[str, Any]:
        """Extract metadata from a Chunk object.
        
        Args:
            chunk: The chunk to extract metadata from
            
        Returns:
            Dictionary of extracted metadata
        """
        existing = chunk.metadata.to_dict() if chunk.metadata else {}
        return self.extract(chunk.content, existing)


@dataclass
class SourceInfo:
    """Information about a document source.
    
    Attributes:
        path: Full path to the source file
        filename: Name of the file without directory
        extension: File extension (e.g., '.pdf')
        directory: Parent directory path
        file_size: Size of the file in bytes
        created_time: File creation timestamp
        modified_time: File modification timestamp
    """
    path: str
    filename: str
    extension: str
    directory: str
    file_size: Optional[int] = None
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "path": self.path,
            "filename": self.filename,
            "extension": self.extension,
            "directory": self.directory,
            "file_size": self.file_size,
        }
        if self.created_time:
            result["created_time"] = self.created_time.isoformat()
        if self.modified_time:
            result["modified_time"] = self.modified_time.isoformat()
        return result


class SourceExtractor(MetadataExtractor):
    """Extract source file information.
    
    Extracts metadata about the source file including path components,
    file size, and timestamps.
    
    Attributes:
        include_timestamps: Whether to include file timestamps
        include_size: Whether to include file size
    """
    
    def __init__(
        self,
        include_timestamps: bool = True,
        include_size: bool = True,
    ) -> None:
        """Initialize the source extractor.
        
        Args:
            include_timestamps: Whether to extract file timestamps
            include_size: Whether to extract file size
        """
        self.include_timestamps = include_timestamps
        self.include_size = include_size
    
    def extract(self, content: str, existing_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract source metadata.
        
        Args:
            content: The text content (not used for source extraction)
            existing_metadata: Must contain 'source' key with file path
            
        Returns:
            Dictionary with source information
        """
        if not existing_metadata or "source" not in existing_metadata:
            return {}
        
        source_path = existing_metadata["source"]
        source_info = self.extract_from_path(source_path)
        
        return {"source_info": source_info.to_dict()}
    
    def extract_from_path(self, path: str) -> SourceInfo:
        """Extract source information from a file path.
        
        Args:
            path: Path to the source file
            
        Returns:
            SourceInfo object with extracted information
        """
        path_obj = Path(path)
        
        file_size = None
        created_time = None
        modified_time = None
        
        # Try to get file stats if the file exists
        if path_obj.exists():
            stat = path_obj.stat()
            
            if self.include_size:
                file_size = stat.st_size
            
            if self.include_timestamps:
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                # st_ctime is creation time on Windows, change time on Unix
                created_time = datetime.fromtimestamp(stat.st_ctime)
        
        return SourceInfo(
            path=str(path_obj.absolute()) if path_obj.exists() else path,
            filename=path_obj.name,
            extension=path_obj.suffix.lower(),
            directory=str(path_obj.parent),
            file_size=file_size,
            created_time=created_time,
            modified_time=modified_time,
        )


@dataclass
class PageInfo:
    """Information about a page within a document.
    
    Attributes:
        page_number: Current page number (1-indexed)
        total_pages: Total number of pages in the document
        is_first_page: Whether this is the first page
        is_last_page: Whether this is the last page
        page_range: String representation of page range (e.g., "1-10")
    """
    page_number: Optional[int] = None
    total_pages: Optional[int] = None
    is_first_page: bool = False
    is_last_page: bool = False
    page_range: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "page_number": self.page_number,
            "total_pages": self.total_pages,
            "is_first_page": self.is_first_page,
            "is_last_page": self.is_last_page,
            "page_range": self.page_range,
        }


class PageExtractor(MetadataExtractor):
    """Extract page-related metadata.
    
    Extracts information about page numbers and positions within
    multi-page documents.
    """
    
    def extract(self, content: str, existing_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract page metadata.
        
        Args:
            content: The text content (not used for page extraction)
            existing_metadata: Should contain page_number and total_pages
            
        Returns:
            Dictionary with page information
        """
        if not existing_metadata:
            return {}
        
        page_number = existing_metadata.get("page_number")
        total_pages = existing_metadata.get("total_pages")
        
        page_info = self.extract_page_info(page_number, total_pages)
        
        return {"page_info": page_info.to_dict()}
    
    def extract_page_info(
        self,
        page_number: Optional[int],
        total_pages: Optional[int],
    ) -> PageInfo:
        """Extract page information from page numbers.
        
        Args:
            page_number: Current page number
            total_pages: Total number of pages
            
        Returns:
            PageInfo object with extracted information
        """
        is_first = page_number == 1 if page_number else False
        is_last = (page_number == total_pages) if (page_number and total_pages) else False
        
        page_range = None
        if total_pages:
            page_range = f"1-{total_pages}"
        
        return PageInfo(
            page_number=page_number,
            total_pages=total_pages,
            is_first_page=is_first,
            is_last_page=is_last,
            page_range=page_range,
        )


@dataclass
class SectionInfo:
    """Information about a section within a document.
    
    Attributes:
        section_title: Title of the current section
        section_level: Heading level (1-6 for markdown-style)
        parent_sections: List of parent section titles (hierarchy)
        section_path: Full path like "Chapter 1 > Section 1.1 > Subsection"
        section_index: Index of this section within the document
    """
    section_title: Optional[str] = None
    section_level: Optional[int] = None
    parent_sections: List[str] = field(default_factory=list)
    section_path: Optional[str] = None
    section_index: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "section_title": self.section_title,
            "section_level": self.section_level,
            "parent_sections": self.parent_sections,
            "section_path": self.section_path,
            "section_index": self.section_index,
        }


class SectionExtractor(MetadataExtractor):
    """Extract section/heading information from content.
    
    Identifies the section a piece of content belongs to by analyzing
    headings in the content or using existing section metadata.
    
    Supports:
    - Markdown-style headings (# Heading)
    - HTML-style headings (<h1>Heading</h1>)
    - Underline-style headings (Heading followed by === or ---)
    
    Attributes:
        heading_patterns: List of regex patterns for heading detection
    """
    
    # Markdown ATX-style headings: # Heading
    MARKDOWN_ATX_PATTERN = re.compile(r'^(#{1,6})\s+(.+?)(?:\s*#*)?$', re.MULTILINE)
    
    # Markdown Setext-style headings: Heading followed by === or ---
    MARKDOWN_SETEXT_H1_PATTERN = re.compile(r'^(.+)\n={3,}\s*$', re.MULTILINE)
    MARKDOWN_SETEXT_H2_PATTERN = re.compile(r'^(.+)\n-{3,}\s*$', re.MULTILINE)
    
    # HTML headings: <h1>Heading</h1>
    HTML_HEADING_PATTERN = re.compile(r'<h([1-6])[^>]*>(.+?)</h\1>', re.IGNORECASE | re.DOTALL)
    
    def __init__(self, use_hierarchy: bool = True) -> None:
        """Initialize the section extractor.
        
        Args:
            use_hierarchy: Whether to track section hierarchy
        """
        self.use_hierarchy = use_hierarchy
    
    def extract(self, content: str, existing_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract section metadata from content.
        
        Args:
            content: The text content to analyze
            existing_metadata: Any existing metadata (may contain 'section')
            
        Returns:
            Dictionary with section information
        """
        # Check if section is already provided
        if existing_metadata and existing_metadata.get("section"):
            section_info = SectionInfo(
                section_title=existing_metadata["section"],
                section_level=existing_metadata.get("section_level"),
            )
            return {"section_info": section_info.to_dict()}
        
        # Extract section from content
        section_info = self.extract_section_from_content(content)
        
        return {"section_info": section_info.to_dict()}
    
    def extract_section_from_content(self, content: str) -> SectionInfo:
        """Extract section information from content.
        
        Finds the first heading in the content and uses it as the section.
        
        Args:
            content: Text content to analyze
            
        Returns:
            SectionInfo with extracted information
        """
        # Try markdown ATX-style first
        match = self.MARKDOWN_ATX_PATTERN.search(content)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            return SectionInfo(
                section_title=title,
                section_level=level,
            )
        
        # Try markdown Setext-style H1
        match = self.MARKDOWN_SETEXT_H1_PATTERN.search(content)
        if match:
            title = match.group(1).strip()
            return SectionInfo(
                section_title=title,
                section_level=1,
            )
        
        # Try markdown Setext-style H2
        match = self.MARKDOWN_SETEXT_H2_PATTERN.search(content)
        if match:
            title = match.group(1).strip()
            return SectionInfo(
                section_title=title,
                section_level=2,
            )
        
        # Try HTML headings
        match = self.HTML_HEADING_PATTERN.search(content)
        if match:
            level = int(match.group(1))
            title = match.group(2).strip()
            # Remove any nested HTML tags
            title = re.sub(r'<[^>]+>', '', title)
            return SectionInfo(
                section_title=title,
                section_level=level,
            )
        
        return SectionInfo()
    
    def extract_all_sections(self, content: str) -> List[SectionInfo]:
        """Extract all sections from content with hierarchy.
        
        Args:
            content: Text content to analyze
            
        Returns:
            List of SectionInfo objects for all sections found
        """
        sections: List[SectionInfo] = []
        parent_stack: List[Tuple[int, str]] = []  # (level, title)
        section_index = 0
        
        # Find all headings
        headings = self._find_all_headings(content)
        
        for level, title, _ in headings:
            # Update parent stack
            while parent_stack and parent_stack[-1][0] >= level:
                parent_stack.pop()
            
            parent_sections = [p[1] for p in parent_stack]
            section_path = " > ".join(parent_sections + [title]) if parent_sections else title
            
            section_info = SectionInfo(
                section_title=title,
                section_level=level,
                parent_sections=parent_sections.copy(),
                section_path=section_path,
                section_index=section_index,
            )
            sections.append(section_info)
            
            # Add to parent stack for hierarchy tracking
            if self.use_hierarchy:
                parent_stack.append((level, title))
            
            section_index += 1
        
        return sections
    
    def _find_all_headings(self, content: str) -> List[Tuple[int, str, int]]:
        """Find all headings in content with their positions.
        
        Args:
            content: Text content to analyze
            
        Returns:
            List of (level, title, position) tuples
        """
        headings: List[Tuple[int, str, int]] = []
        
        # Find markdown ATX-style headings
        for match in self.MARKDOWN_ATX_PATTERN.finditer(content):
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title, match.start()))
        
        # Find markdown Setext-style H1
        for match in self.MARKDOWN_SETEXT_H1_PATTERN.finditer(content):
            title = match.group(1).strip()
            headings.append((1, title, match.start()))
        
        # Find markdown Setext-style H2
        for match in self.MARKDOWN_SETEXT_H2_PATTERN.finditer(content):
            title = match.group(1).strip()
            headings.append((2, title, match.start()))
        
        # Find HTML headings
        for match in self.HTML_HEADING_PATTERN.finditer(content):
            level = int(match.group(1))
            title = re.sub(r'<[^>]+>', '', match.group(2).strip())
            headings.append((level, title, match.start()))
        
        # Sort by position
        headings.sort(key=lambda x: x[2])
        
        return headings



@dataclass
class TitleInfo:
    """Information about a document title.
    
    Attributes:
        title: The extracted title
        title_source: Where the title was extracted from (metadata, heading, filename)
        confidence: Confidence level of the extraction (high, medium, low)
    """
    title: Optional[str] = None
    title_source: Optional[str] = None
    confidence: str = "low"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "title_source": self.title_source,
            "confidence": self.confidence,
        }


class TitleExtractor(MetadataExtractor):
    """Extract document title using multiple strategies.
    
    Attempts to extract the document title from:
    1. Existing metadata (highest confidence)
    2. First H1 heading in content
    3. First heading of any level
    4. Filename (lowest confidence)
    
    Attributes:
        fallback_to_filename: Whether to use filename as fallback
        clean_filename: Whether to clean up filename (remove extension, underscores)
    """
    
    def __init__(
        self,
        fallback_to_filename: bool = True,
        clean_filename: bool = True,
    ) -> None:
        """Initialize the title extractor.
        
        Args:
            fallback_to_filename: Whether to use filename as last resort
            clean_filename: Whether to clean up the filename for display
        """
        self.fallback_to_filename = fallback_to_filename
        self.clean_filename = clean_filename
    
    def extract(self, content: str, existing_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract title from content and metadata.
        
        Args:
            content: The text content to analyze
            existing_metadata: Any existing metadata
            
        Returns:
            Dictionary with title information
        """
        title_info = self.extract_title(content, existing_metadata)
        return {"title_info": title_info.to_dict()}
    
    def extract_title(
        self,
        content: str,
        existing_metadata: Optional[Dict[str, Any]] = None,
    ) -> TitleInfo:
        """Extract title using multiple strategies.
        
        Args:
            content: Text content to analyze
            existing_metadata: Existing metadata dictionary
            
        Returns:
            TitleInfo with extracted title
        """
        # Strategy 1: Check existing metadata
        if existing_metadata and existing_metadata.get("title"):
            return TitleInfo(
                title=existing_metadata["title"],
                title_source="metadata",
                confidence="high",
            )
        
        # Strategy 2: Look for first H1 heading
        h1_title = self._extract_h1_title(content)
        if h1_title:
            return TitleInfo(
                title=h1_title,
                title_source="h1_heading",
                confidence="high",
            )
        
        # Strategy 3: Look for any first heading
        first_heading = self._extract_first_heading(content)
        if first_heading:
            return TitleInfo(
                title=first_heading,
                title_source="first_heading",
                confidence="medium",
            )
        
        # Strategy 4: Use filename as fallback
        if self.fallback_to_filename and existing_metadata:
            source = existing_metadata.get("source", "")
            if source:
                filename_title = self._extract_from_filename(source)
                if filename_title:
                    return TitleInfo(
                        title=filename_title,
                        title_source="filename",
                        confidence="low",
                    )
        
        return TitleInfo()
    
    def _extract_h1_title(self, content: str) -> Optional[str]:
        """Extract title from H1 heading.
        
        Args:
            content: Text content
            
        Returns:
            H1 title or None
        """
        # Markdown ATX H1
        match = re.search(r'^#\s+(.+?)(?:\s*#*)?$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Markdown Setext H1
        match = re.search(r'^(.+)\n={3,}\s*$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # HTML H1
        match = re.search(r'<h1[^>]*>(.+?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if match:
            title = re.sub(r'<[^>]+>', '', match.group(1))
            return title.strip()
        
        return None
    
    def _extract_first_heading(self, content: str) -> Optional[str]:
        """Extract the first heading of any level.
        
        Args:
            content: Text content
            
        Returns:
            First heading or None
        """
        # Markdown ATX any level
        match = re.search(r'^#{1,6}\s+(.+?)(?:\s*#*)?$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # HTML any heading level
        match = re.search(r'<h[1-6][^>]*>(.+?)</h[1-6]>', content, re.IGNORECASE | re.DOTALL)
        if match:
            title = re.sub(r'<[^>]+>', '', match.group(1))
            return title.strip()
        
        return None
    
    def _extract_from_filename(self, source: str) -> Optional[str]:
        """Extract title from filename.
        
        Args:
            source: Source file path
            
        Returns:
            Cleaned filename as title
        """
        path = Path(source)
        filename = path.stem  # Filename without extension
        
        if not filename:
            return None
        
        if self.clean_filename:
            # Replace underscores and hyphens with spaces
            filename = re.sub(r'[_-]+', ' ', filename)
            # Remove multiple spaces
            filename = re.sub(r'\s+', ' ', filename)
            # Title case
            filename = filename.strip().title()
        
        return filename if filename else None


@dataclass
class HeadingInfo:
    """Information about a heading in a document.
    
    Attributes:
        text: The heading text
        level: Heading level (1-6)
        position: Character position in the document
        line_number: Line number in the document
    """
    text: str
    level: int
    position: int = 0
    line_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "level": self.level,
            "position": self.position,
            "line_number": self.line_number,
        }


class HeadingExtractor(MetadataExtractor):
    """Extract all headings from document content.
    
    Identifies and extracts all headings from a document, supporting
    multiple heading formats (Markdown, HTML).
    
    Attributes:
        include_line_numbers: Whether to include line numbers
        min_level: Minimum heading level to extract (1-6)
        max_level: Maximum heading level to extract (1-6)
    """
    
    def __init__(
        self,
        include_line_numbers: bool = True,
        min_level: int = 1,
        max_level: int = 6,
    ) -> None:
        """Initialize the heading extractor.
        
        Args:
            include_line_numbers: Whether to calculate line numbers
            min_level: Minimum heading level to include
            max_level: Maximum heading level to include
        """
        self.include_line_numbers = include_line_numbers
        self.min_level = min_level
        self.max_level = max_level
    
    def extract(self, content: str, existing_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract all headings from content.
        
        Args:
            content: The text content to analyze
            existing_metadata: Any existing metadata (not used)
            
        Returns:
            Dictionary with list of headings
        """
        headings = self.extract_headings(content)
        return {
            "headings": [h.to_dict() for h in headings],
            "heading_count": len(headings),
        }
    
    def extract_headings(self, content: str) -> List[HeadingInfo]:
        """Extract all headings from content.
        
        Args:
            content: Text content to analyze
            
        Returns:
            List of HeadingInfo objects
        """
        headings: List[HeadingInfo] = []
        
        # Build line number lookup if needed
        line_starts: List[int] = []
        if self.include_line_numbers:
            line_starts = [0]
            for i, char in enumerate(content):
                if char == '\n':
                    line_starts.append(i + 1)
        
        # Extract markdown ATX headings
        for match in re.finditer(r'^(#{1,6})\s+(.+?)(?:\s*#*)?$', content, re.MULTILINE):
            level = len(match.group(1))
            if self.min_level <= level <= self.max_level:
                text = match.group(2).strip()
                position = match.start()
                line_number = self._get_line_number(position, line_starts) if self.include_line_numbers else None
                headings.append(HeadingInfo(
                    text=text,
                    level=level,
                    position=position,
                    line_number=line_number,
                ))
        
        # Extract markdown Setext H1
        if self.min_level <= 1 <= self.max_level:
            for match in re.finditer(r'^(.+)\n={3,}\s*$', content, re.MULTILINE):
                text = match.group(1).strip()
                position = match.start()
                line_number = self._get_line_number(position, line_starts) if self.include_line_numbers else None
                headings.append(HeadingInfo(
                    text=text,
                    level=1,
                    position=position,
                    line_number=line_number,
                ))
        
        # Extract markdown Setext H2
        if self.min_level <= 2 <= self.max_level:
            for match in re.finditer(r'^(.+)\n-{3,}\s*$', content, re.MULTILINE):
                text = match.group(1).strip()
                position = match.start()
                line_number = self._get_line_number(position, line_starts) if self.include_line_numbers else None
                headings.append(HeadingInfo(
                    text=text,
                    level=2,
                    position=position,
                    line_number=line_number,
                ))
        
        # Extract HTML headings
        for match in re.finditer(r'<h([1-6])[^>]*>(.+?)</h\1>', content, re.IGNORECASE | re.DOTALL):
            level = int(match.group(1))
            if self.min_level <= level <= self.max_level:
                text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
                position = match.start()
                line_number = self._get_line_number(position, line_starts) if self.include_line_numbers else None
                headings.append(HeadingInfo(
                    text=text,
                    level=level,
                    position=position,
                    line_number=line_number,
                ))
        
        # Sort by position
        headings.sort(key=lambda h: h.position)
        
        return headings
    
    def _get_line_number(self, position: int, line_starts: List[int]) -> int:
        """Get line number for a character position.
        
        Args:
            position: Character position
            line_starts: List of line start positions
            
        Returns:
            Line number (1-indexed)
        """
        for i, start in enumerate(line_starts):
            if start > position:
                return i  # Previous line (1-indexed)
        return len(line_starts)  # Last line
    
    def get_table_of_contents(self, content: str) -> List[Dict[str, Any]]:
        """Generate a table of contents from headings.
        
        Args:
            content: Text content to analyze
            
        Returns:
            List of TOC entries with text, level, and indent
        """
        headings = self.extract_headings(content)
        toc: List[Dict[str, Any]] = []
        
        for heading in headings:
            indent = "  " * (heading.level - 1)
            toc.append({
                "text": heading.text,
                "level": heading.level,
                "indent": indent,
                "formatted": f"{indent}- {heading.text}",
            })
        
        return toc



class MetadataEnrichmentPipeline:
    """Pipeline for enriching documents and chunks with metadata.
    
    Combines multiple metadata extractors to enrich documents and chunks
    with comprehensive metadata. Extractors are run in sequence and their
    results are merged.
    
    Attributes:
        extractors: List of metadata extractors to apply
        merge_strategy: How to handle conflicting metadata ('first', 'last', 'merge')
    """
    
    def __init__(
        self,
        extractors: Optional[List[MetadataExtractor]] = None,
        merge_strategy: str = "merge",
    ) -> None:
        """Initialize the enrichment pipeline.
        
        Args:
            extractors: List of extractors to use (default: all standard extractors)
            merge_strategy: How to merge conflicting values
                - 'first': Keep first non-None value
                - 'last': Keep last non-None value
                - 'merge': Merge dictionaries, last value wins for conflicts
        """
        if extractors is None:
            # Default set of extractors
            extractors = [
                SourceExtractor(),
                PageExtractor(),
                SectionExtractor(),
                TitleExtractor(),
                HeadingExtractor(),
            ]
        
        self.extractors = extractors
        self.merge_strategy = merge_strategy
    
    def enrich_document(self, document: Document) -> Document:
        """Enrich a document with additional metadata.
        
        Args:
            document: The document to enrich
            
        Returns:
            New Document with enriched metadata
        """
        # Start with existing metadata
        existing_metadata = document.metadata.to_dict()
        
        # Run all extractors
        enriched = self._run_extractors(document.content, existing_metadata)
        
        # Merge enriched metadata into extra field
        new_extra = document.metadata.extra.copy()
        new_extra.update(enriched)
        
        # Create new metadata with enriched extra
        new_metadata = DocumentMetadata(
            source=document.metadata.source,
            page_number=document.metadata.page_number,
            total_pages=document.metadata.total_pages,
            title=enriched.get("title_info", {}).get("title") or document.metadata.title,
            author=document.metadata.author,
            created_date=document.metadata.created_date,
            modified_date=document.metadata.modified_date,
            file_type=document.metadata.file_type,
            extra=new_extra,
        )
        
        return Document(content=document.content, metadata=new_metadata)
    
    def enrich_chunk(self, chunk: Chunk, document: Optional[Document] = None) -> Chunk:
        """Enrich a chunk with additional metadata.
        
        Args:
            chunk: The chunk to enrich
            document: Optional parent document for context
            
        Returns:
            New Chunk with enriched metadata
        """
        # Start with existing metadata
        existing_metadata = chunk.metadata.to_dict()
        
        # Add document metadata if available
        if document:
            doc_meta = document.metadata.to_dict()
            existing_metadata.update({
                "doc_title": doc_meta.get("title"),
                "doc_author": doc_meta.get("author"),
                "total_pages": doc_meta.get("total_pages"),
            })
        
        # Run all extractors
        enriched = self._run_extractors(chunk.content, existing_metadata)
        
        # Merge enriched metadata into extra field
        new_extra = chunk.metadata.extra.copy()
        new_extra.update(enriched)
        
        # Update section if extracted
        section = chunk.metadata.section
        if "section_info" in enriched and enriched["section_info"].get("section_title"):
            section = enriched["section_info"]["section_title"]
        
        # Create new metadata with enriched extra
        new_metadata = ChunkMetadata(
            source=chunk.metadata.source,
            chunk_index=chunk.metadata.chunk_index,
            total_chunks=chunk.metadata.total_chunks,
            start_char=chunk.metadata.start_char,
            end_char=chunk.metadata.end_char,
            page_number=chunk.metadata.page_number,
            section=section,
            parent_id=chunk.metadata.parent_id,
            extra=new_extra,
        )
        
        return Chunk(content=chunk.content, metadata=new_metadata, id=chunk.id)
    
    def enrich_documents(self, documents: List[Document]) -> List[Document]:
        """Enrich multiple documents.
        
        Args:
            documents: List of documents to enrich
            
        Returns:
            List of enriched documents
        """
        return [self.enrich_document(doc) for doc in documents]
    
    def enrich_chunks(
        self,
        chunks: List[Chunk],
        document: Optional[Document] = None,
    ) -> List[Chunk]:
        """Enrich multiple chunks.
        
        Args:
            chunks: List of chunks to enrich
            document: Optional parent document for context
            
        Returns:
            List of enriched chunks
        """
        return [self.enrich_chunk(chunk, document) for chunk in chunks]
    
    def _run_extractors(
        self,
        content: str,
        existing_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Run all extractors and merge results.
        
        Args:
            content: Text content to analyze
            existing_metadata: Existing metadata dictionary
            
        Returns:
            Merged extraction results
        """
        result: Dict[str, Any] = {}
        
        for extractor in self.extractors:
            try:
                extracted = extractor.extract(content, existing_metadata)
                result = self._merge_metadata(result, extracted)
            except Exception:
                # Skip failed extractors
                continue
        
        return result
    
    def _merge_metadata(
        self,
        base: Dict[str, Any],
        new: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Merge two metadata dictionaries.
        
        Args:
            base: Base metadata dictionary
            new: New metadata to merge in
            
        Returns:
            Merged dictionary
        """
        if self.merge_strategy == "first":
            # Keep first non-None values
            result = base.copy()
            for key, value in new.items():
                if key not in result or result[key] is None:
                    result[key] = value
            return result
        
        elif self.merge_strategy == "last":
            # Keep last non-None values
            result = base.copy()
            for key, value in new.items():
                if value is not None:
                    result[key] = value
            return result
        
        else:  # merge
            # Deep merge dictionaries
            result = base.copy()
            for key, value in new.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_metadata(result[key], value)
                elif value is not None:
                    result[key] = value
            return result
    
    def add_extractor(self, extractor: MetadataExtractor) -> None:
        """Add an extractor to the pipeline.
        
        Args:
            extractor: Extractor to add
        """
        self.extractors.append(extractor)
    
    def remove_extractor(self, extractor_type: type) -> bool:
        """Remove extractors of a specific type.
        
        Args:
            extractor_type: Type of extractor to remove
            
        Returns:
            True if any extractors were removed
        """
        original_count = len(self.extractors)
        self.extractors = [e for e in self.extractors if not isinstance(e, extractor_type)]
        return len(self.extractors) < original_count


def create_default_pipeline() -> MetadataEnrichmentPipeline:
    """Create a default metadata enrichment pipeline.
    
    Returns:
        MetadataEnrichmentPipeline with standard extractors
    """
    return MetadataEnrichmentPipeline()


def create_minimal_pipeline() -> MetadataEnrichmentPipeline:
    """Create a minimal metadata enrichment pipeline.
    
    Only includes source and title extraction for performance.
    
    Returns:
        MetadataEnrichmentPipeline with minimal extractors
    """
    return MetadataEnrichmentPipeline(
        extractors=[
            SourceExtractor(include_timestamps=False, include_size=False),
            TitleExtractor(fallback_to_filename=True),
        ]
    )


def create_full_pipeline() -> MetadataEnrichmentPipeline:
    """Create a full metadata enrichment pipeline.
    
    Includes all extractors with full options enabled.
    
    Returns:
        MetadataEnrichmentPipeline with all extractors
    """
    return MetadataEnrichmentPipeline(
        extractors=[
            SourceExtractor(include_timestamps=True, include_size=True),
            PageExtractor(),
            SectionExtractor(use_hierarchy=True),
            TitleExtractor(fallback_to_filename=True, clean_filename=True),
            HeadingExtractor(include_line_numbers=True, min_level=1, max_level=6),
        ]
    )
