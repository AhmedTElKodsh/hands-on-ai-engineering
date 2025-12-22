"""Document ingestion module for AITEA.

This module provides document loading and processing capabilities
for various file formats including PDF, DOCX, HTML, and Markdown.
It also provides chunking strategies for splitting documents into
smaller pieces suitable for embedding and retrieval.

Additionally, it provides the ParentDocumentRetriever for implementing
the parent document retrieval pattern where small chunks are used for
search but larger parent chunks are retrieved for context.

The metadata module provides extractors for enriching documents and
chunks with additional metadata such as source information, page numbers,
sections, titles, and headings.
"""

from .models import Document, DocumentMetadata, Chunk, ChunkMetadata
from .loaders import (
    DocumentLoader,
    PDFLoader,
    DOCXLoader,
    HTMLLoader,
    MarkdownLoader,
)
from .chunkers import (
    ChunkingStrategy,
    FixedSizeChunker,
    RecursiveChunker,
    SemanticChunker,
    SentenceChunker,
)
from .retriever import (
    ParentChunk,
    ChunkMapping,
    ParentDocumentRetriever,
)
from .metadata import (
    MetadataExtractor,
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
from .tables import (
    TableExtractionMethod,
    TableToTextFormat,
    TableCell,
    ExtractedTable,
    TableExtractor,
    CamelotTableExtractor,
    TabulaTableExtractor,
    PDFTableExtractor,
    TableToTextConverter,
    MarkdownTableConverter,
    CSVTableConverter,
    PlainTextTableConverter,
    HTMLTableConverter,
    JSONTableConverter,
    get_converter,
    convert_table,
    StructuredTableData,
    TableDataHandler,
    TableCollection,
    extract_tables_from_pdf,
)

__all__ = [
    # Models
    "Document",
    "DocumentMetadata",
    "Chunk",
    "ChunkMetadata",
    # Loaders
    "DocumentLoader",
    "PDFLoader",
    "DOCXLoader",
    "HTMLLoader",
    "MarkdownLoader",
    # Chunkers
    "ChunkingStrategy",
    "FixedSizeChunker",
    "RecursiveChunker",
    "SemanticChunker",
    "SentenceChunker",
    # Retriever
    "ParentChunk",
    "ChunkMapping",
    "ParentDocumentRetriever",
    # Metadata Extractors
    "MetadataExtractor",
    "SourceExtractor",
    "SourceInfo",
    "PageExtractor",
    "PageInfo",
    "SectionExtractor",
    "SectionInfo",
    "TitleExtractor",
    "TitleInfo",
    "HeadingExtractor",
    "HeadingInfo",
    "MetadataEnrichmentPipeline",
    "create_default_pipeline",
    "create_minimal_pipeline",
    "create_full_pipeline",
    # Table Extraction
    "TableExtractionMethod",
    "TableToTextFormat",
    "TableCell",
    "ExtractedTable",
    "TableExtractor",
    "CamelotTableExtractor",
    "TabulaTableExtractor",
    "PDFTableExtractor",
    "TableToTextConverter",
    "MarkdownTableConverter",
    "CSVTableConverter",
    "PlainTextTableConverter",
    "HTMLTableConverter",
    "JSONTableConverter",
    "get_converter",
    "convert_table",
    "StructuredTableData",
    "TableDataHandler",
    "TableCollection",
    "extract_tables_from_pdf",
]
