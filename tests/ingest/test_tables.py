"""Tests for table extraction module."""

import pytest
from pathlib import Path
from src.ingest.tables import (
    TableExtractionMethod,
    TableToTextFormat,
    TableCell,
    ExtractedTable,
    CamelotTableExtractor,
    TabulaTableExtractor,
    PDFTableExtractor,
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
)


class TestExtractedTable:
    """Tests for ExtractedTable dataclass."""

    def test_create_table(self):
        """Test creating an ExtractedTable."""
        data = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
        table = ExtractedTable(data=data, page_number=1)
        assert table.num_rows == 3
        assert table.num_cols == 2
        assert not table.is_empty

    def test_empty_table(self):
        """Test empty table detection."""
        table = ExtractedTable(data=[])
        assert table.is_empty
        assert table.num_rows == 0
        assert table.num_cols == 0

    def test_whitespace_only_table(self):
        """Test table with only whitespace is considered empty."""
        table = ExtractedTable(data=[["  ", ""], [" ", "  "]])
        assert table.is_empty

    def test_get_cell(self):
        """Test getting individual cells."""
        data = [["A", "B"], ["C", "D"]]
        table = ExtractedTable(data=data)
        assert table.get_cell(0, 0) == "A"
        assert table.get_cell(1, 1) == "D"
        assert table.get_cell(5, 5) == ""  # Out of bounds

    def test_get_row(self):
        """Test getting rows."""
        data = [["A", "B"], ["C", "D"]]
        table = ExtractedTable(data=data)
        assert table.get_row(0) == ["A", "B"]
        assert table.get_row(5) == []  # Out of bounds

    def test_get_column(self):
        """Test getting columns."""
        data = [["A", "B"], ["C", "D"]]
        table = ExtractedTable(data=data)
        assert table.get_column(0) == ["A", "C"]
        assert table.get_column(1) == ["B", "D"]

    def test_to_dict_from_dict(self):
        """Test serialization round-trip."""
        data = [["Name", "Age"], ["Alice", "30"]]
        table = ExtractedTable(
            data=data, page_number=2, table_index=1,
            accuracy=95.5, extraction_method="test"
        )
        d = table.to_dict()
        restored = ExtractedTable.from_dict(d)
        assert restored.data == table.data
        assert restored.page_number == table.page_number
        assert restored.accuracy == table.accuracy


class TestTableToTextConverters:
    """Tests for table-to-text converters."""

    @pytest.fixture
    def sample_table(self):
        """Create a sample table for testing."""
        return ExtractedTable(
            data=[["Name", "Age", "City"], ["Alice", "30", "NYC"], ["Bob", "25", "LA"]]
        )

    def test_markdown_converter(self, sample_table):
        """Test Markdown conversion."""
        converter = MarkdownTableConverter()
        result = converter.convert(sample_table)
        assert "| Name" in result
        assert "| Alice" in result
        assert "---" in result

    def test_csv_converter(self, sample_table):
        """Test CSV conversion."""
        converter = CSVTableConverter()
        result = converter.convert(sample_table)
        lines = result.split("\n")
        assert len(lines) == 3
        assert "Name,Age,City" in lines[0]

    def test_csv_quoting(self):
        """Test CSV quoting for special characters."""
        table = ExtractedTable(data=[["Hello, World", "Test"]])
        converter = CSVTableConverter()
        result = converter.convert(table)
        assert '"Hello, World"' in result

    def test_plain_text_converter(self, sample_table):
        """Test plain text conversion."""
        converter = PlainTextTableConverter()
        result = converter.convert(sample_table)
        assert "Name" in result
        assert "Alice" in result

    def test_html_converter(self, sample_table):
        """Test HTML conversion."""
        converter = HTMLTableConverter()
        result = converter.convert(sample_table)
        assert "<table>" in result
        assert "<th>Name</th>" in result
        assert "<td>Alice</td>" in result
        assert "</table>" in result

    def test_html_escaping(self):
        """Test HTML escaping."""
        table = ExtractedTable(data=[["<script>", "&test"]])
        converter = HTMLTableConverter(include_header=False)
        result = converter.convert(table)
        assert "&lt;script&gt;" in result
        assert "&amp;test" in result

    def test_json_converter(self, sample_table):
        """Test JSON conversion."""
        converter = JSONTableConverter()
        result = converter.convert(sample_table)
        import json
        parsed = json.loads(result)
        assert len(parsed) == 2  # 2 data rows (header used as keys)
        assert parsed[0]["Name"] == "Alice"

    def test_json_converter_no_header(self, sample_table):
        """Test JSON conversion without header as keys."""
        converter = JSONTableConverter(use_header_as_keys=False)
        result = converter.convert(sample_table)
        import json
        parsed = json.loads(result)
        assert len(parsed) == 3  # All rows as arrays
        assert parsed[0] == ["Name", "Age", "City"]

    def test_get_converter(self):
        """Test get_converter factory function."""
        for fmt in TableToTextFormat:
            converter = get_converter(fmt)
            assert converter is not None

    def test_convert_table_function(self, sample_table):
        """Test convert_table convenience function."""
        result = convert_table(sample_table, TableToTextFormat.CSV)
        assert "Name,Age,City" in result

    def test_empty_table_conversion(self):
        """Test converting empty tables."""
        table = ExtractedTable(data=[])
        for fmt in TableToTextFormat:
            converter = get_converter(fmt)
            result = converter.convert(table)
            assert result == "" or result == "[]"


class TestStructuredTableData:
    """Tests for StructuredTableData."""

    def test_create_structured_data(self):
        """Test creating structured table data."""
        data = StructuredTableData(
            headers=["name", "age"],
            rows=[{"name": "Alice", "age": 30}],
            column_types={"name": "string", "age": "integer"}
        )
        assert data.num_rows == 1
        assert data.num_columns == 2

    def test_get_column(self):
        """Test getting column values."""
        data = StructuredTableData(
            headers=["name", "age"],
            rows=[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}],
            column_types={"name": "string", "age": "integer"}
        )
        names = data.get_column("name")
        assert names == ["Alice", "Bob"]

    def test_filter_rows(self):
        """Test filtering rows."""
        data = StructuredTableData(
            headers=["name", "age"],
            rows=[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}],
            column_types={"name": "string", "age": "integer"}
        )
        filtered = data.filter_rows(lambda r: r["age"] > 26)
        assert filtered.num_rows == 1
        assert filtered.rows[0]["name"] == "Alice"

    def test_select_columns(self):
        """Test selecting columns."""
        data = StructuredTableData(
            headers=["name", "age", "city"],
            rows=[{"name": "Alice", "age": 30, "city": "NYC"}],
            column_types={"name": "string", "age": "integer", "city": "string"}
        )
        selected = data.select_columns(["name", "city"])
        assert selected.num_columns == 2
        assert "age" not in selected.rows[0]

    def test_to_dict_from_dict(self):
        """Test serialization round-trip."""
        data = StructuredTableData(
            headers=["name"], rows=[{"name": "Alice"}],
            column_types={"name": "string"}
        )
        d = data.to_dict()
        restored = StructuredTableData.from_dict(d)
        assert restored.headers == data.headers
        assert restored.rows == data.rows


class TestTableDataHandler:
    """Tests for TableDataHandler."""

    def test_process_table(self):
        """Test processing a table into structured data."""
        table = ExtractedTable(
            data=[["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
        )
        handler = TableDataHandler()
        result = handler.process(table)
        assert result.num_rows == 2
        assert "name" in result.headers  # Normalized
        assert result.column_types["age"] == "integer"

    def test_header_normalization(self):
        """Test header normalization."""
        table = ExtractedTable(
            data=[["First Name", "Age (Years)"], ["Alice", "30"]]
        )
        handler = TableDataHandler(normalize_headers=True)
        result = handler.process(table)
        assert "first_name" in result.headers
        assert "age_years" in result.headers

    def test_unique_headers(self):
        """Test handling duplicate headers."""
        table = ExtractedTable(
            data=[["Name", "Name", "Name"], ["A", "B", "C"]]
        )
        handler = TableDataHandler()
        result = handler.process(table)
        assert len(set(result.headers)) == 3  # All unique

    def test_type_inference_integer(self):
        """Test integer type inference."""
        table = ExtractedTable(data=[["Count"], ["100"], ["200"], ["300"]])
        handler = TableDataHandler()
        result = handler.process(table)
        assert result.column_types["count"] == "integer"
        assert result.rows[0]["count"] == 100

    def test_type_inference_float(self):
        """Test float type inference."""
        table = ExtractedTable(data=[["Price"], ["10.5"], ["20.75"]])
        handler = TableDataHandler()
        result = handler.process(table)
        assert result.column_types["price"] == "float"
        assert result.rows[0]["price"] == 10.5

    def test_type_inference_boolean(self):
        """Test boolean type inference."""
        table = ExtractedTable(data=[["Active"], ["true"], ["false"]])
        handler = TableDataHandler()
        result = handler.process(table)
        assert result.column_types["active"] == "boolean"
        assert result.rows[0]["active"] is True

    def test_no_type_inference(self):
        """Test disabling type inference."""
        table = ExtractedTable(data=[["Count"], ["100"]])
        handler = TableDataHandler(infer_types=False)
        result = handler.process(table)
        assert result.column_types["count"] == "string"
        assert result.rows[0]["count"] == "100"

    def test_empty_table(self):
        """Test processing empty table."""
        table = ExtractedTable(data=[])
        handler = TableDataHandler()
        result = handler.process(table)
        assert result.num_rows == 0
        assert result.num_columns == 0


class TestTableCollection:
    """Tests for TableCollection."""

    def test_create_collection(self):
        """Test creating a table collection."""
        tables = [
            ExtractedTable(data=[["A"]], page_number=1),
            ExtractedTable(data=[["B"]], page_number=2),
        ]
        collection = TableCollection(tables=tables)
        assert len(collection) == 2

    def test_iteration(self):
        """Test iterating over collection."""
        tables = [ExtractedTable(data=[["A"]]), ExtractedTable(data=[["B"]])]
        collection = TableCollection(tables=tables)
        items = list(collection)
        assert len(items) == 2

    def test_indexing(self):
        """Test indexing collection."""
        tables = [ExtractedTable(data=[["A"]]), ExtractedTable(data=[["B"]])]
        collection = TableCollection(tables=tables)
        assert collection[0].data == [["A"]]

    def test_add_table(self):
        """Test adding tables to collection."""
        collection = TableCollection()
        collection.add(ExtractedTable(data=[["A"]]))
        assert len(collection) == 1

    def test_get_by_page(self):
        """Test filtering by page number."""
        tables = [
            ExtractedTable(data=[["A"]], page_number=1),
            ExtractedTable(data=[["B"]], page_number=1),
            ExtractedTable(data=[["C"]], page_number=2),
        ]
        collection = TableCollection(tables=tables)
        page1 = collection.get_by_page(1)
        assert len(page1) == 2

    def test_get_non_empty(self):
        """Test filtering non-empty tables."""
        tables = [
            ExtractedTable(data=[["A"]]),
            ExtractedTable(data=[]),
            ExtractedTable(data=[["  ", ""]]),
        ]
        collection = TableCollection(tables=tables)
        non_empty = collection.get_non_empty()
        assert len(non_empty) == 1

    def test_filter_by_size(self):
        """Test filtering by size."""
        tables = [
            ExtractedTable(data=[["A"]]),  # 1x1
            ExtractedTable(data=[["A", "B"], ["C", "D"]]),  # 2x2
        ]
        collection = TableCollection(tables=tables)
        large = collection.filter_by_size(min_rows=2, min_cols=2)
        assert len(large) == 1

    def test_to_structured(self):
        """Test converting to structured data."""
        tables = [ExtractedTable(data=[["Name"], ["Alice"]])]
        collection = TableCollection(tables=tables)
        structured = collection.to_structured()
        assert len(structured) == 1
        assert structured[0].num_rows == 1

    def test_to_text(self):
        """Test converting to text."""
        tables = [
            ExtractedTable(data=[["A", "B"]]),
            ExtractedTable(data=[["C", "D"]]),
        ]
        collection = TableCollection(tables=tables)
        text = collection.to_text(TableToTextFormat.CSV)
        assert "A,B" in text
        assert "C,D" in text

    def test_to_dict_from_dict(self):
        """Test serialization round-trip."""
        tables = [ExtractedTable(data=[["A"]])]
        collection = TableCollection(tables=tables, source_path=Path("test.pdf"))
        d = collection.to_dict()
        restored = TableCollection.from_dict(d)
        assert len(restored) == 1
        assert restored.source_path == Path("test.pdf")


class TestTableExtractors:
    """Tests for table extractor classes."""

    def test_camelot_availability(self):
        """Test Camelot availability check."""
        extractor = CamelotTableExtractor()
        # Just check it doesn't crash
        _ = extractor.is_available()

    def test_tabula_availability(self):
        """Test Tabula availability check."""
        extractor = TabulaTableExtractor()
        # Just check it doesn't crash
        _ = extractor.is_available()

    def test_pdf_extractor_file_not_found(self):
        """Test error handling for missing files."""
        extractor = PDFTableExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.extract(Path("nonexistent.pdf"))

    def test_pdf_extractor_wrong_format(self, tmp_path):
        """Test error handling for wrong file format."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("hello")
        extractor = PDFTableExtractor()
        with pytest.raises(ValueError):
            extractor.extract(txt_file)

    def test_get_available_methods(self):
        """Test getting available extraction methods."""
        extractor = PDFTableExtractor()
        methods = extractor.get_available_methods()
        # Should return a list (may be empty if no libraries installed)
        assert isinstance(methods, list)
