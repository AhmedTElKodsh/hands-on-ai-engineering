"""Table extraction from PDF documents.

This module provides functionality for detecting and extracting tables
from PDF documents using camelot-py and tabula-py libraries, with
fallback support when libraries are not available.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import re


class TableExtractionMethod(str, Enum):
    """Methods for extracting tables from PDFs."""
    CAMELOT_LATTICE = "camelot_lattice"
    CAMELOT_STREAM = "camelot_stream"
    TABULA = "tabula"
    AUTO = "auto"


class TableToTextFormat(str, Enum):
    """Output formats for table-to-text conversion."""
    MARKDOWN = "markdown"
    CSV = "csv"
    PLAIN = "plain"
    HTML = "html"
    JSON = "json"


@dataclass
class TableCell:
    """Represents a single cell in a table."""
    value: str
    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1

    def __str__(self) -> str:
        return self.value


@dataclass
class ExtractedTable:
    """Represents a table extracted from a document."""
    data: List[List[str]]
    page_number: int = 1
    table_index: int = 0
    bbox: Optional[tuple] = None
    accuracy: float = 0.0
    extraction_method: str = ""
    headers: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


    @property
    def num_rows(self) -> int:
        return len(self.data)

    @property
    def num_cols(self) -> int:
        if not self.data:
            return 0
        return max(len(row) for row in self.data)

    @property
    def is_empty(self) -> bool:
        return self.num_rows == 0 or all(
            all(not cell.strip() for cell in row) for row in self.data
        )

    def get_cell(self, row: int, col: int) -> str:
        if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
            return self.data[row][col]
        return ""

    def get_row(self, row: int) -> List[str]:
        if 0 <= row < len(self.data):
            return self.data[row]
        return []

    def get_column(self, col: int) -> List[str]:
        return [row[col] if col < len(row) else "" for row in self.data]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "page_number": self.page_number,
            "table_index": self.table_index,
            "bbox": self.bbox,
            "accuracy": self.accuracy,
            "extraction_method": self.extraction_method,
            "headers": self.headers,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractedTable":
        return cls(
            data=data["data"],
            page_number=data.get("page_number", 1),
            table_index=data.get("table_index", 0),
            bbox=tuple(data["bbox"]) if data.get("bbox") else None,
            accuracy=data.get("accuracy", 0.0),
            extraction_method=data.get("extraction_method", ""),
            headers=data.get("headers"),
            metadata=data.get("metadata", {}),
        )


class TableExtractor(ABC):
    """Abstract base class for table extractors."""

    @abstractmethod
    def extract(self, path: Path, pages: Optional[str] = None) -> List[ExtractedTable]:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...


class CamelotTableExtractor(TableExtractor):
    """Table extractor using camelot-py library."""

    def __init__(self, flavor: str = "lattice", line_scale: int = 15, row_tol: int = 2):
        self.flavor = flavor
        self.line_scale = line_scale
        self.row_tol = row_tol

    def is_available(self) -> bool:
        try:
            import camelot
            return True
        except ImportError:
            return False

    def extract(self, path: Path, pages: Optional[str] = None) -> List[ExtractedTable]:
        if not self.is_available():
            raise ImportError("camelot-py is required. Install with: pip install camelot-py[cv]")
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Camelot only supports PDF files, got: {path.suffix}")

        import camelot
        pages = pages or "all"
        kwargs: Dict[str, Any] = {"flavor": self.flavor, "pages": pages}
        if self.flavor == "lattice":
            kwargs["line_scale"] = self.line_scale
        else:
            kwargs["row_tol"] = self.row_tol

        tables = camelot.read_pdf(str(path), **kwargs)
        extracted: List[ExtractedTable] = []
        for idx, table in enumerate(tables):
            data = table.df.values.tolist()
            bbox = table._bbox if hasattr(table, "_bbox") else None
            extracted.append(ExtractedTable(
                data=data,
                page_number=table.page,
                table_index=idx,
                bbox=bbox,
                accuracy=table.accuracy if hasattr(table, "accuracy") else 0.0,
                extraction_method=f"camelot_{self.flavor}",
                metadata={"flavor": self.flavor, "shape": table.shape},
            ))
        return extracted


class TabulaTableExtractor(TableExtractor):
    """Table extractor using tabula-py library."""

    def __init__(self, lattice: bool = False, stream: bool = False, guess: bool = True):
        self.lattice = lattice
        self.stream = stream
        self.guess = guess

    def is_available(self) -> bool:
        try:
            import tabula
            return True
        except ImportError:
            return False

    def extract(self, path: Path, pages: Optional[str] = None) -> List[ExtractedTable]:
        if not self.is_available():
            raise ImportError("tabula-py is required. Install with: pip install tabula-py")
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Tabula only supports PDF files, got: {path.suffix}")

        import tabula
        pages = pages or "all"
        dfs = tabula.read_pdf(
            str(path), pages=pages, lattice=self.lattice,
            stream=self.stream, guess=self.guess, pandas_options={"header": None}
        )
        extracted: List[ExtractedTable] = []
        for idx, df in enumerate(dfs):
            data = df.fillna("").astype(str).values.tolist()
            extracted.append(ExtractedTable(
                data=data, page_number=1, table_index=idx,
                extraction_method="tabula",
                metadata={"lattice": self.lattice, "stream": self.stream, "shape": df.shape},
            ))
        return extracted



class PDFTableExtractor:
    """High-level PDF table extractor with automatic method selection."""

    def __init__(
        self,
        preferred_method: TableExtractionMethod = TableExtractionMethod.AUTO,
        fallback_enabled: bool = True,
    ):
        self.preferred_method = preferred_method
        self.fallback_enabled = fallback_enabled
        self._camelot_lattice = CamelotTableExtractor(flavor="lattice")
        self._camelot_stream = CamelotTableExtractor(flavor="stream")
        self._tabula = TabulaTableExtractor()

    def get_available_methods(self) -> List[TableExtractionMethod]:
        available = []
        if self._camelot_lattice.is_available():
            available.extend([TableExtractionMethod.CAMELOT_LATTICE, TableExtractionMethod.CAMELOT_STREAM])
        if self._tabula.is_available():
            available.append(TableExtractionMethod.TABULA)
        return available

    def extract(
        self, path: Path, pages: Optional[str] = None,
        method: Optional[TableExtractionMethod] = None
    ) -> List[ExtractedTable]:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Only PDF files are supported, got: {path.suffix}")

        method = method or self.preferred_method
        extractors = self._get_extractor_order(method)
        if not extractors:
            raise ImportError("No table extraction library available. Install camelot-py or tabula-py")

        last_error: Optional[Exception] = None
        for extractor in extractors:
            try:
                tables = extractor.extract(path, pages)
                if tables:
                    return tables
            except Exception as e:
                last_error = e
                if not self.fallback_enabled:
                    raise
        return []

    def _get_extractor_order(self, method: TableExtractionMethod) -> List[TableExtractor]:
        extractors: List[TableExtractor] = []
        if method == TableExtractionMethod.CAMELOT_LATTICE:
            if self._camelot_lattice.is_available():
                extractors.append(self._camelot_lattice)
            if self.fallback_enabled and self._camelot_stream.is_available():
                extractors.append(self._camelot_stream)
            if self.fallback_enabled and self._tabula.is_available():
                extractors.append(self._tabula)
        elif method == TableExtractionMethod.CAMELOT_STREAM:
            if self._camelot_stream.is_available():
                extractors.append(self._camelot_stream)
            if self.fallback_enabled and self._camelot_lattice.is_available():
                extractors.append(self._camelot_lattice)
            if self.fallback_enabled and self._tabula.is_available():
                extractors.append(self._tabula)
        elif method == TableExtractionMethod.TABULA:
            if self._tabula.is_available():
                extractors.append(self._tabula)
            if self.fallback_enabled and self._camelot_lattice.is_available():
                extractors.append(self._camelot_lattice)
            if self.fallback_enabled and self._camelot_stream.is_available():
                extractors.append(self._camelot_stream)
        else:  # AUTO
            if self._camelot_lattice.is_available():
                extractors.append(self._camelot_lattice)
            if self._tabula.is_available():
                extractors.append(self._tabula)
            if self._camelot_stream.is_available():
                extractors.append(self._camelot_stream)
        return extractors



# Table-to-Text Converters

class TableToTextConverter(ABC):
    """Abstract base class for table-to-text converters."""

    @abstractmethod
    def convert(self, table: ExtractedTable) -> str:
        ...

    @property
    @abstractmethod
    def format_name(self) -> str:
        ...


class MarkdownTableConverter(TableToTextConverter):
    """Convert tables to Markdown format."""

    def __init__(self, include_header_row: bool = True, align: str = "left"):
        self.include_header_row = include_header_row
        self.align = align

    @property
    def format_name(self) -> str:
        return "markdown"

    def convert(self, table: ExtractedTable) -> str:
        if table.is_empty:
            return ""
        data = table.data
        num_cols = table.num_cols
        col_widths = [max(3, max(len(str(row[i])) if i < len(row) else 0 for row in data)) for i in range(num_cols)]

        lines: List[str] = []
        if self.include_header_row and data:
            header = data[0]
            header_cells = [str(header[i] if i < len(header) else "").ljust(col_widths[i]) for i in range(num_cols)]
            lines.append("| " + " | ".join(header_cells) + " |")
            sep = ["-" * w for w in col_widths]
            lines.append("| " + " | ".join(sep) + " |")
            for row in data[1:]:
                cells = [str(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(num_cols)]
                lines.append("| " + " | ".join(cells) + " |")
        else:
            for row in data:
                cells = [str(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(num_cols)]
                lines.append("| " + " | ".join(cells) + " |")
        return "\n".join(lines)


class CSVTableConverter(TableToTextConverter):
    """Convert tables to CSV format."""

    def __init__(self, delimiter: str = ",", quote_char: str = '"'):
        self.delimiter = delimiter
        self.quote_char = quote_char

    @property
    def format_name(self) -> str:
        return "csv"

    def convert(self, table: ExtractedTable) -> str:
        if table.is_empty:
            return ""
        lines = []
        for row in table.data:
            cells = [self._quote_cell(str(cell)) for cell in row]
            lines.append(self.delimiter.join(cells))
        return "\n".join(lines)

    def _quote_cell(self, value: str) -> str:
        if self.delimiter in value or self.quote_char in value or "\n" in value:
            escaped = value.replace(self.quote_char, self.quote_char + self.quote_char)
            return f"{self.quote_char}{escaped}{self.quote_char}"
        return value


class PlainTextTableConverter(TableToTextConverter):
    """Convert tables to plain text format."""

    def __init__(self, column_separator: str = "  ", pad_columns: bool = True):
        self.column_separator = column_separator
        self.pad_columns = pad_columns

    @property
    def format_name(self) -> str:
        return "plain"

    def convert(self, table: ExtractedTable) -> str:
        if table.is_empty:
            return ""
        data = table.data
        if self.pad_columns:
            num_cols = table.num_cols
            col_widths = [max(len(str(row[i])) if i < len(row) else 0 for row in data) for i in range(num_cols)]
            lines = []
            for row in data:
                cells = [str(row[i] if i < len(row) else "").ljust(col_widths[i]) for i in range(num_cols)]
                lines.append(self.column_separator.join(cells))
            return "\n".join(lines)
        return "\n".join(self.column_separator.join(str(c) for c in row) for row in data)


class HTMLTableConverter(TableToTextConverter):
    """Convert tables to HTML format."""

    def __init__(self, include_header: bool = True, table_class: str = ""):
        self.include_header = include_header
        self.table_class = table_class

    @property
    def format_name(self) -> str:
        return "html"

    def convert(self, table: ExtractedTable) -> str:
        if table.is_empty:
            return ""
        data = table.data
        attrs = f' class="{self.table_class}"' if self.table_class else ""
        lines = [f"<table{attrs}>"]
        if self.include_header and data:
            lines.append("  <thead><tr>")
            for cell in data[0]:
                lines.append(f"    <th>{self._escape(str(cell))}</th>")
            lines.append("  </tr></thead>")
            data_rows = data[1:]
        else:
            data_rows = data
        if data_rows:
            lines.append("  <tbody>")
            for row in data_rows:
                lines.append("    <tr>")
                for cell in row:
                    lines.append(f"      <td>{self._escape(str(cell))}</td>")
                lines.append("    </tr>")
            lines.append("  </tbody>")
        lines.append("</table>")
        return "\n".join(lines)

    def _escape(self, text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class JSONTableConverter(TableToTextConverter):
    """Convert tables to JSON format."""

    def __init__(self, use_header_as_keys: bool = True, indent: int = 2):
        self.use_header_as_keys = use_header_as_keys
        self.indent = indent

    @property
    def format_name(self) -> str:
        return "json"

    def convert(self, table: ExtractedTable) -> str:
        import json
        if table.is_empty:
            return "[]"
        data = table.data
        if self.use_header_as_keys and len(data) > 1:
            headers = [str(h) for h in data[0]]
            rows = []
            for row in data[1:]:
                row_dict = {headers[i] if i < len(headers) else f"col_{i}": str(cell) for i, cell in enumerate(row)}
                rows.append(row_dict)
            return json.dumps(rows, indent=self.indent, ensure_ascii=False)
        return json.dumps(data, indent=self.indent, ensure_ascii=False)


def get_converter(format: TableToTextFormat) -> TableToTextConverter:
    """Get a converter for the specified format."""
    converters = {
        TableToTextFormat.MARKDOWN: MarkdownTableConverter,
        TableToTextFormat.CSV: CSVTableConverter,
        TableToTextFormat.PLAIN: PlainTextTableConverter,
        TableToTextFormat.HTML: HTMLTableConverter,
        TableToTextFormat.JSON: JSONTableConverter,
    }
    return converters[format]()


def convert_table(table: ExtractedTable, format: TableToTextFormat = TableToTextFormat.MARKDOWN) -> str:
    """Convert a table to the specified text format."""
    return get_converter(format).convert(table)



# Structured Data Handling

@dataclass
class StructuredTableData:
    """Structured representation of table data with type inference."""
    headers: List[str]
    rows: List[Dict[str, Any]]
    column_types: Dict[str, str]
    source_table: Optional[ExtractedTable] = None

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_columns(self) -> int:
        return len(self.headers)

    def get_column(self, name: str) -> List[Any]:
        return [row.get(name) for row in self.rows]

    def filter_rows(self, predicate: callable) -> "StructuredTableData":
        filtered = [row for row in self.rows if predicate(row)]
        return StructuredTableData(
            headers=self.headers.copy(), rows=filtered,
            column_types=self.column_types.copy(), source_table=self.source_table
        )

    def select_columns(self, columns: List[str]) -> "StructuredTableData":
        new_rows = [{k: v for k, v in row.items() if k in columns} for row in self.rows]
        new_types = {k: v for k, v in self.column_types.items() if k in columns}
        return StructuredTableData(
            headers=[h for h in self.headers if h in columns],
            rows=new_rows, column_types=new_types, source_table=self.source_table
        )

    def to_dataframe(self) -> Any:
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required. Install with: pip install pandas")
        return pd.DataFrame(self.rows, columns=self.headers)

    def to_dict(self) -> Dict[str, Any]:
        return {"headers": self.headers, "rows": self.rows, "column_types": self.column_types}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructuredTableData":
        return cls(headers=data["headers"], rows=data["rows"], column_types=data["column_types"])


class TableDataHandler:
    """Handler for structured table data operations."""

    def __init__(self, infer_types: bool = True, normalize_headers: bool = True, strip_whitespace: bool = True):
        self.infer_types = infer_types
        self.normalize_headers = normalize_headers
        self.strip_whitespace = strip_whitespace

    def process(self, table: ExtractedTable) -> StructuredTableData:
        if table.is_empty:
            return StructuredTableData(headers=[], rows=[], column_types={}, source_table=table)

        data = table.data
        raw_headers = [str(h) for h in data[0]] if data else []
        headers = [self._normalize_header(h) for h in raw_headers] if self.normalize_headers else raw_headers
        headers = self._ensure_unique_headers(headers)

        rows: List[Dict[str, Any]] = []
        for row_data in data[1:]:
            row_dict: Dict[str, Any] = {}
            for i, cell in enumerate(row_data):
                if i < len(headers):
                    value = str(cell).strip() if self.strip_whitespace else str(cell)
                    row_dict[headers[i]] = value
            rows.append(row_dict)

        column_types: Dict[str, str] = {}
        if self.infer_types:
            for header in headers:
                values = [row.get(header, "") for row in rows]
                column_types[header] = self._infer_column_type(values)
            rows = self._convert_values(rows, column_types)
        else:
            column_types = {h: "string" for h in headers}

        return StructuredTableData(headers=headers, rows=rows, column_types=column_types, source_table=table)

    def _normalize_header(self, header: str) -> str:
        header = header.strip()
        header = re.sub(r"[^\w\s]", "", header)
        header = re.sub(r"\s+", "_", header).lower()
        if header and not header[0].isalpha() and header[0] != "_":
            header = "_" + header
        return header or "column"

    def _ensure_unique_headers(self, headers: List[str]) -> List[str]:
        seen: Dict[str, int] = {}
        unique: List[str] = []
        for h in headers:
            if h in seen:
                seen[h] += 1
                unique.append(f"{h}_{seen[h]}")
            else:
                seen[h] = 0
                unique.append(h)
        return unique

    def _infer_column_type(self, values: List[str]) -> str:
        non_empty = [v for v in values if v.strip()]
        if not non_empty:
            return "string"
        # Check integer
        if all(self._is_int(v) for v in non_empty):
            return "integer"
        # Check float
        if all(self._is_float(v) for v in non_empty):
            return "float"
        # Check boolean
        bool_vals = {"true", "false", "yes", "no", "1", "0"}
        if all(v.lower() in bool_vals for v in non_empty):
            return "boolean"
        return "string"

    def _is_int(self, v: str) -> bool:
        try:
            int(v.replace(",", "").replace(" ", ""))
            return True
        except ValueError:
            return False

    def _is_float(self, v: str) -> bool:
        try:
            float(v.replace(",", "").replace(" ", ""))
            return True
        except ValueError:
            return False

    def _convert_values(self, rows: List[Dict[str, Any]], column_types: Dict[str, str]) -> List[Dict[str, Any]]:
        converted = []
        for row in rows:
            new_row = {}
            for key, value in row.items():
                col_type = column_types.get(key, "string")
                new_row[key] = self._convert_value(value, col_type)
            converted.append(new_row)
        return converted

    def _convert_value(self, value: str, col_type: str) -> Any:
        if not value.strip():
            return None
        try:
            if col_type == "integer":
                return int(value.replace(",", "").replace(" ", ""))
            elif col_type == "float":
                return float(value.replace(",", "").replace(" ", ""))
            elif col_type == "boolean":
                return value.lower() in {"true", "yes", "1"}
        except (ValueError, TypeError):
            pass
        return value



class TableCollection:
    """Collection of extracted tables from a document."""

    def __init__(self, tables: Optional[List[ExtractedTable]] = None, source_path: Optional[Path] = None):
        self.tables = tables or []
        self.source_path = source_path

    def __len__(self) -> int:
        return len(self.tables)

    def __iter__(self):
        return iter(self.tables)

    def __getitem__(self, index: int) -> ExtractedTable:
        return self.tables[index]

    def add(self, table: ExtractedTable) -> None:
        self.tables.append(table)

    def get_by_page(self, page_number: int) -> List[ExtractedTable]:
        return [t for t in self.tables if t.page_number == page_number]

    def get_non_empty(self) -> List[ExtractedTable]:
        return [t for t in self.tables if not t.is_empty]

    def filter_by_size(self, min_rows: int = 0, min_cols: int = 0) -> List[ExtractedTable]:
        return [t for t in self.tables if t.num_rows >= min_rows and t.num_cols >= min_cols]

    def to_structured(self, handler: Optional[TableDataHandler] = None) -> List[StructuredTableData]:
        handler = handler or TableDataHandler()
        return [handler.process(t) for t in self.tables]

    def to_text(self, format: TableToTextFormat = TableToTextFormat.MARKDOWN, separator: str = "\n\n") -> str:
        converter = get_converter(format)
        texts = [converter.convert(t) for t in self.tables if not t.is_empty]
        return separator.join(texts)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_path": str(self.source_path) if self.source_path else None,
            "tables": [t.to_dict() for t in self.tables],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TableCollection":
        tables = [ExtractedTable.from_dict(t) for t in data.get("tables", [])]
        source_path = Path(data["source_path"]) if data.get("source_path") else None
        return cls(tables=tables, source_path=source_path)


def extract_tables_from_pdf(
    path: Path,
    pages: Optional[str] = None,
    method: TableExtractionMethod = TableExtractionMethod.AUTO,
) -> TableCollection:
    """Extract all tables from a PDF file."""
    extractor = PDFTableExtractor(preferred_method=method)
    tables = extractor.extract(path, pages)
    return TableCollection(tables=tables, source_path=path)
