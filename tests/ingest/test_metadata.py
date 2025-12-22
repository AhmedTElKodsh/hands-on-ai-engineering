"""Tests for metadata extraction functionality.

This module tests the metadata extractors and enrichment pipeline
for document processing.
"""

import pytest
from pathlib import Path
from datetime import datetime

from src.ingest.models import Document, DocumentMetadata, Chunk, ChunkMetadata
from src.ingest.metadata import (
    SourceExtractor,
    SourceInfo,
    PageExtractor,
    PageInfo,
    SectionExtractor,
    SectionInfo,
    TitleExtractor,
    TitleInfo,
    HeadingExtractor,
    HeadingInfo,
    MetadataEnrichmentPipeline,
    create_default_pipeline,
    create_minimal_pipeline,
    create_full_pipeline,
)


class TestSourceExtractor:
    """Tests for SourceExtractor."""
    
    def test_extract_from_path_basic(self):
        """Test basic path extraction."""
        extractor = SourceExtractor(include_timestamps=False, include_size=False)
        info = extractor.extract_from_path("documents/test.pdf")
        
        assert info.filename == "test.pdf"
        assert info.extension == ".pdf"
        assert info.directory == "documents"
    
    def test_extract_from_metadata(self):
        """Test extraction from existing metadata."""
        extractor = SourceExtractor(include_timestamps=False, include_size=False)
        result = extractor.extract("", {"source": "path/to/file.docx"})
        
        assert "source_info" in result
        assert result["source_info"]["filename"] == "file.docx"
        assert result["source_info"]["extension"] == ".docx"
    
    def test_extract_without_source(self):
        """Test extraction without source in metadata."""
        extractor = SourceExtractor()
        result = extractor.extract("", {})
        
        assert result == {}
    
    def test_source_info_to_dict(self):
        """Test SourceInfo serialization."""
        info = SourceInfo(
            path="/path/to/file.pdf",
            filename="file.pdf",
            extension=".pdf",
            directory="/path/to",
            file_size=1024,
        )
        
        d = info.to_dict()
        assert d["path"] == "/path/to/file.pdf"
        assert d["filename"] == "file.pdf"
        assert d["file_size"] == 1024


class TestPageExtractor:
    """Tests for PageExtractor."""
    
    def test_extract_page_info(self):
        """Test page info extraction."""
        extractor = PageExtractor()
        info = extractor.extract_page_info(page_number=3, total_pages=10)
        
        assert info.page_number == 3
        assert info.total_pages == 10
        assert info.is_first_page is False
        assert info.is_last_page is False
        assert info.page_range == "1-10"
    
    def test_first_page_detection(self):
        """Test first page detection."""
        extractor = PageExtractor()
        info = extractor.extract_page_info(page_number=1, total_pages=5)
        
        assert info.is_first_page is True
        assert info.is_last_page is False
    
    def test_last_page_detection(self):
        """Test last page detection."""
        extractor = PageExtractor()
        info = extractor.extract_page_info(page_number=5, total_pages=5)
        
        assert info.is_first_page is False
        assert info.is_last_page is True
    
    def test_extract_from_metadata(self):
        """Test extraction from metadata dict."""
        extractor = PageExtractor()
        result = extractor.extract("", {"page_number": 2, "total_pages": 8})
        
        assert "page_info" in result
        assert result["page_info"]["page_number"] == 2
        assert result["page_info"]["total_pages"] == 8


class TestSectionExtractor:
    """Tests for SectionExtractor."""
    
    def test_extract_markdown_atx_heading(self):
        """Test extraction of markdown ATX-style heading."""
        extractor = SectionExtractor()
        content = "# Introduction\n\nThis is the introduction."
        
        info = extractor.extract_section_from_content(content)
        
        assert info.section_title == "Introduction"
        assert info.section_level == 1
    
    def test_extract_markdown_h2(self):
        """Test extraction of H2 heading."""
        extractor = SectionExtractor()
        content = "## Getting Started\n\nLet's begin."
        
        info = extractor.extract_section_from_content(content)
        
        assert info.section_title == "Getting Started"
        assert info.section_level == 2
    
    def test_extract_setext_h1(self):
        """Test extraction of Setext-style H1."""
        extractor = SectionExtractor()
        content = "Main Title\n==========\n\nContent here."
        
        info = extractor.extract_section_from_content(content)
        
        assert info.section_title == "Main Title"
        assert info.section_level == 1
    
    def test_extract_setext_h2(self):
        """Test extraction of Setext-style H2."""
        extractor = SectionExtractor()
        content = "Subtitle\n--------\n\nMore content."
        
        info = extractor.extract_section_from_content(content)
        
        assert info.section_title == "Subtitle"
        assert info.section_level == 2
    
    def test_extract_html_heading(self):
        """Test extraction of HTML heading."""
        extractor = SectionExtractor()
        content = "<h1>Welcome</h1>\n<p>Hello world</p>"
        
        info = extractor.extract_section_from_content(content)
        
        assert info.section_title == "Welcome"
        assert info.section_level == 1
    
    def test_extract_all_sections(self):
        """Test extraction of all sections with hierarchy."""
        extractor = SectionExtractor(use_hierarchy=True)
        content = """# Chapter 1

## Section 1.1

### Subsection 1.1.1

## Section 1.2

# Chapter 2
"""
        
        sections = extractor.extract_all_sections(content)
        
        assert len(sections) == 5
        assert sections[0].section_title == "Chapter 1"
        assert sections[0].section_level == 1
        assert sections[1].section_title == "Section 1.1"
        assert sections[1].parent_sections == ["Chapter 1"]
        assert sections[2].section_title == "Subsection 1.1.1"
        assert sections[2].parent_sections == ["Chapter 1", "Section 1.1"]
    
    def test_no_heading_found(self):
        """Test when no heading is found."""
        extractor = SectionExtractor()
        content = "Just some plain text without any headings."
        
        info = extractor.extract_section_from_content(content)
        
        assert info.section_title is None
        assert info.section_level is None


class TestTitleExtractor:
    """Tests for TitleExtractor."""
    
    def test_extract_from_metadata(self):
        """Test title extraction from existing metadata."""
        extractor = TitleExtractor()
        result = extractor.extract("", {"title": "My Document"})
        
        assert result["title_info"]["title"] == "My Document"
        assert result["title_info"]["title_source"] == "metadata"
        assert result["title_info"]["confidence"] == "high"
    
    def test_extract_from_h1(self):
        """Test title extraction from H1 heading."""
        extractor = TitleExtractor()
        content = "# Document Title\n\nSome content here."
        
        result = extractor.extract(content, {})
        
        assert result["title_info"]["title"] == "Document Title"
        assert result["title_info"]["title_source"] == "h1_heading"
        assert result["title_info"]["confidence"] == "high"
    
    def test_extract_from_first_heading(self):
        """Test title extraction from first heading (not H1)."""
        extractor = TitleExtractor()
        content = "## Section Title\n\nContent."
        
        result = extractor.extract(content, {})
        
        assert result["title_info"]["title"] == "Section Title"
        assert result["title_info"]["title_source"] == "first_heading"
        assert result["title_info"]["confidence"] == "medium"
    
    def test_extract_from_filename(self):
        """Test title extraction from filename."""
        extractor = TitleExtractor(fallback_to_filename=True, clean_filename=True)
        content = "No headings here."
        
        result = extractor.extract(content, {"source": "my_document_file.pdf"})
        
        assert result["title_info"]["title"] == "My Document File"
        assert result["title_info"]["title_source"] == "filename"
        assert result["title_info"]["confidence"] == "low"
    
    def test_no_title_found(self):
        """Test when no title can be extracted."""
        extractor = TitleExtractor(fallback_to_filename=False)
        content = "Plain text without headings."
        
        result = extractor.extract(content, {})
        
        assert result["title_info"]["title"] is None


class TestHeadingExtractor:
    """Tests for HeadingExtractor."""
    
    def test_extract_all_headings(self):
        """Test extraction of all headings."""
        extractor = HeadingExtractor()
        content = """# Main Title

## Section 1

### Subsection 1.1

## Section 2

### Subsection 2.1
"""
        
        result = extractor.extract(content, {})
        
        assert result["heading_count"] == 5
        headings = result["headings"]
        assert headings[0]["text"] == "Main Title"
        assert headings[0]["level"] == 1
        assert headings[1]["text"] == "Section 1"
        assert headings[1]["level"] == 2
    
    def test_filter_by_level(self):
        """Test filtering headings by level."""
        extractor = HeadingExtractor(min_level=2, max_level=3)
        content = """# Title

## Section

### Subsection

#### Deep Section
"""
        
        result = extractor.extract(content, {})
        
        # Should only include H2 and H3
        assert result["heading_count"] == 2
        headings = result["headings"]
        assert all(2 <= h["level"] <= 3 for h in headings)
    
    def test_line_numbers(self):
        """Test line number extraction."""
        extractor = HeadingExtractor(include_line_numbers=True)
        content = "Line 1\n# Heading\nLine 3"
        
        result = extractor.extract(content, {})
        
        assert result["heading_count"] == 1
        assert result["headings"][0]["line_number"] is not None
    
    def test_table_of_contents(self):
        """Test table of contents generation."""
        extractor = HeadingExtractor()
        content = """# Chapter 1

## Section 1.1

## Section 1.2

# Chapter 2
"""
        
        toc = extractor.get_table_of_contents(content)
        
        assert len(toc) == 4
        assert toc[0]["text"] == "Chapter 1"
        assert toc[0]["level"] == 1
        assert toc[1]["indent"] == "  "  # H2 indented


class TestMetadataEnrichmentPipeline:
    """Tests for MetadataEnrichmentPipeline."""
    
    def test_enrich_document(self):
        """Test document enrichment."""
        pipeline = create_default_pipeline()
        
        doc = Document(
            content="# My Document\n\nThis is the content.",
            metadata=DocumentMetadata(
                source="test.md",
                file_type="markdown",
            )
        )
        
        enriched = pipeline.enrich_document(doc)
        
        assert enriched.metadata.title == "My Document"
        assert "title_info" in enriched.metadata.extra
        assert "headings" in enriched.metadata.extra
    
    def test_enrich_chunk(self):
        """Test chunk enrichment."""
        pipeline = create_default_pipeline()
        
        chunk = Chunk(
            content="## Section Title\n\nChunk content here.",
            metadata=ChunkMetadata(
                source="test.md",
                chunk_index=0,
            )
        )
        
        enriched = pipeline.enrich_chunk(chunk)
        
        assert enriched.metadata.section == "Section Title"
        assert "section_info" in enriched.metadata.extra
    
    def test_enrich_multiple_documents(self):
        """Test enriching multiple documents."""
        pipeline = create_minimal_pipeline()
        
        docs = [
            Document(
                content="# Doc 1\n\nContent 1",
                metadata=DocumentMetadata(source="doc1.md")
            ),
            Document(
                content="# Doc 2\n\nContent 2",
                metadata=DocumentMetadata(source="doc2.md")
            ),
        ]
        
        enriched = pipeline.enrich_documents(docs)
        
        assert len(enriched) == 2
        assert enriched[0].metadata.title == "Doc 1"
        assert enriched[1].metadata.title == "Doc 2"
    
    def test_add_extractor(self):
        """Test adding an extractor to pipeline."""
        pipeline = MetadataEnrichmentPipeline(extractors=[])
        
        assert len(pipeline.extractors) == 0
        
        pipeline.add_extractor(TitleExtractor())
        
        assert len(pipeline.extractors) == 1
    
    def test_remove_extractor(self):
        """Test removing extractors by type."""
        pipeline = create_default_pipeline()
        initial_count = len(pipeline.extractors)
        
        removed = pipeline.remove_extractor(HeadingExtractor)
        
        assert removed is True
        assert len(pipeline.extractors) == initial_count - 1
    
    def test_merge_strategy_first(self):
        """Test 'first' merge strategy."""
        pipeline = MetadataEnrichmentPipeline(
            extractors=[TitleExtractor()],
            merge_strategy="first"
        )
        
        base = {"title_info": {"title": "First"}}
        new = {"title_info": {"title": "Second"}}
        
        result = pipeline._merge_metadata(base, new)
        
        # First value should be kept
        assert result["title_info"]["title"] == "First"
    
    def test_merge_strategy_last(self):
        """Test 'last' merge strategy."""
        pipeline = MetadataEnrichmentPipeline(
            extractors=[TitleExtractor()],
            merge_strategy="last"
        )
        
        base = {"title_info": {"title": "First"}}
        new = {"title_info": {"title": "Second"}}
        
        result = pipeline._merge_metadata(base, new)
        
        # Last value should be kept
        assert result["title_info"]["title"] == "Second"


class TestPipelineFactories:
    """Tests for pipeline factory functions."""
    
    def test_create_default_pipeline(self):
        """Test default pipeline creation."""
        pipeline = create_default_pipeline()
        
        assert len(pipeline.extractors) == 5
        assert pipeline.merge_strategy == "merge"
    
    def test_create_minimal_pipeline(self):
        """Test minimal pipeline creation."""
        pipeline = create_minimal_pipeline()
        
        assert len(pipeline.extractors) == 2
    
    def test_create_full_pipeline(self):
        """Test full pipeline creation."""
        pipeline = create_full_pipeline()
        
        assert len(pipeline.extractors) == 5
