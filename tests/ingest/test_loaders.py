"""Tests for document loaders."""

import pytest
from pathlib import Path
import tempfile
import os

from src.ingest.models import Document, DocumentMetadata
from src.ingest.loaders import (
    DocumentLoader,
    PDFLoader,
    DOCXLoader,
    HTMLLoader,
    MarkdownLoader,
)


class TestDocumentMetadata:
    """Tests for DocumentMetadata dataclass."""
    
    def test_create_minimal_metadata(self):
        """Test creating metadata with only required fields."""
        metadata = DocumentMetadata(source="/path/to/file.txt")
        assert metadata.source == "/path/to/file.txt"
        assert metadata.page_number is None
        assert metadata.title is None
    
    def test_create_full_metadata(self):
        """Test creating metadata with all fields."""
        metadata = DocumentMetadata(
            source="/path/to/file.pdf",
            page_number=1,
            total_pages=10,
            title="Test Document",
            author="Test Author",
            file_type="pdf",
        )
        assert metadata.source == "/path/to/file.pdf"
        assert metadata.page_number == 1
        assert metadata.total_pages == 10
        assert metadata.title == "Test Document"
        assert metadata.author == "Test Author"
    
    def test_metadata_to_dict(self):
        """Test serializing metadata to dictionary."""
        metadata = DocumentMetadata(
            source="/path/to/file.txt",
            title="Test",
            file_type="txt",
        )
        data = metadata.to_dict()
        assert data["source"] == "/path/to/file.txt"
        assert data["title"] == "Test"
        assert data["file_type"] == "txt"



class TestDocument:
    """Tests for Document dataclass."""
    
    def test_create_document(self):
        """Test creating a document."""
        metadata = DocumentMetadata(source="/path/to/file.txt")
        doc = Document(content="Hello, world!", metadata=metadata)
        assert doc.content == "Hello, world!"
        assert doc.metadata.source == "/path/to/file.txt"
    
    def test_document_length(self):
        """Test document length."""
        metadata = DocumentMetadata(source="test.txt")
        doc = Document(content="Hello", metadata=metadata)
        assert len(doc) == 5
    
    def test_document_str(self):
        """Test document string representation."""
        metadata = DocumentMetadata(source="test.txt")
        doc = Document(content="Short content", metadata=metadata)
        assert "test.txt" in str(doc)
        assert "Short content" in str(doc)
    
    def test_document_validation(self):
        """Test document validation."""
        metadata = DocumentMetadata(source="test.txt")
        # Content cannot be None
        with pytest.raises(ValueError):
            Document(content=None, metadata=metadata)  # type: ignore
    
    def test_document_to_dict(self):
        """Test serializing document to dictionary."""
        metadata = DocumentMetadata(source="test.txt", title="Test")
        doc = Document(content="Content", metadata=metadata)
        data = doc.to_dict()
        assert data["content"] == "Content"
        assert data["metadata"]["source"] == "test.txt"
        assert data["metadata"]["title"] == "Test"


class TestMarkdownLoader:
    """Tests for MarkdownLoader."""
    
    def test_supported_extensions(self):
        """Test that MarkdownLoader supports correct extensions."""
        loader = MarkdownLoader()
        assert ".md" in loader.supported_extensions
        assert ".markdown" in loader.supported_extensions
    
    def test_can_load(self):
        """Test can_load method."""
        loader = MarkdownLoader()
        assert loader.can_load(Path("test.md"))
        assert loader.can_load(Path("test.markdown"))
        assert not loader.can_load(Path("test.txt"))
    
    def test_load_simple_markdown(self):
        """Test loading a simple markdown file."""
        loader = MarkdownLoader()
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Hello World\n\nThis is a test.")
            temp_path = f.name
        
        try:
            docs = loader.load(Path(temp_path))
            assert len(docs) == 1
            assert "Hello World" in docs[0].content
            assert "This is a test" in docs[0].content
            assert docs[0].metadata.file_type == "markdown"
            assert docs[0].metadata.title == "Hello World"
        finally:
            os.unlink(temp_path)
    
    def test_load_markdown_with_frontmatter(self):
        """Test loading markdown with YAML frontmatter."""
        loader = MarkdownLoader()
        
        content = """---
title: My Document
author: Test Author
date: 2025-01-15
---

# Content

This is the body.
"""
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            docs = loader.load(Path(temp_path))
            assert len(docs) == 1
            assert docs[0].metadata.title == "My Document"
            assert docs[0].metadata.author == "Test Author"
            # Frontmatter should be removed from content
            assert "---" not in docs[0].content
            assert "Content" in docs[0].content
        finally:
            os.unlink(temp_path)
    
    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        loader = MarkdownLoader()
        with pytest.raises(FileNotFoundError):
            loader.load(Path("/nonexistent/file.md"))
    
    def test_unsupported_extension(self):
        """Test that ValueError is raised for unsupported extensions."""
        loader = MarkdownLoader()
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("test")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError):
                loader.load(Path(temp_path))
        finally:
            os.unlink(temp_path)


class TestHTMLLoader:
    """Tests for HTMLLoader."""
    
    def test_supported_extensions(self):
        """Test that HTMLLoader supports correct extensions."""
        loader = HTMLLoader()
        assert ".html" in loader.supported_extensions
        assert ".htm" in loader.supported_extensions
    
    def test_load_simple_html(self):
        """Test loading a simple HTML file."""
        loader = HTMLLoader()
        
        html_content = """<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
<h1>Hello World</h1>
<p>This is a test paragraph.</p>
</body>
</html>"""
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            # Skip if beautifulsoup4 is not installed
            pytest.importorskip("bs4")
            
            docs = loader.load(Path(temp_path))
            assert len(docs) == 1
            assert "Hello World" in docs[0].content
            assert "test paragraph" in docs[0].content
            assert docs[0].metadata.title == "Test Page"
            assert docs[0].metadata.file_type == "html"
        finally:
            os.unlink(temp_path)
    
    def test_html_removes_scripts(self):
        """Test that scripts are removed from HTML."""
        loader = HTMLLoader(remove_scripts=True)
        
        html_content = """<html>
<head><script>alert('test');</script></head>
<body><p>Content</p></body>
</html>"""
        
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            pytest.importorskip("bs4")
            
            docs = loader.load(Path(temp_path))
            assert "alert" not in docs[0].content
            assert "Content" in docs[0].content
        finally:
            os.unlink(temp_path)


class TestPDFLoader:
    """Tests for PDFLoader."""
    
    def test_supported_extensions(self):
        """Test that PDFLoader supports correct extensions."""
        loader = PDFLoader()
        assert ".pdf" in loader.supported_extensions
    
    def test_can_load(self):
        """Test can_load method."""
        loader = PDFLoader()
        assert loader.can_load(Path("test.pdf"))
        assert not loader.can_load(Path("test.txt"))
    
    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        loader = PDFLoader()
        with pytest.raises(FileNotFoundError):
            loader.load(Path("/nonexistent/file.pdf"))


class TestDOCXLoader:
    """Tests for DOCXLoader."""
    
    def test_supported_extensions(self):
        """Test that DOCXLoader supports correct extensions."""
        loader = DOCXLoader()
        assert ".docx" in loader.supported_extensions
    
    def test_can_load(self):
        """Test can_load method."""
        loader = DOCXLoader()
        assert loader.can_load(Path("test.docx"))
        assert not loader.can_load(Path("test.doc"))
        assert not loader.can_load(Path("test.txt"))
    
    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        loader = DOCXLoader()
        with pytest.raises(FileNotFoundError):
            loader.load(Path("/nonexistent/file.docx"))
