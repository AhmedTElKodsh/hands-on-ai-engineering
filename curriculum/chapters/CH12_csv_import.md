# Chapter 12: CSV Import Pipeline

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 9-11  
**AITEA Component:** `src/services/csv_import.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Parse CSV files using pandas
2. Validate and transform imported data
3. Collect errors without stopping the import
4. Generate detailed import reports
5. Handle common CSV issues (encoding, missing columns)

## 12.1 CSV Import Requirements

AITEA needs to import tracked time from CSV files like:

```csv
team,member_name,feature,tracked_time_hours,process,date
backend,BE-1,CRUD,4.5,Data Operations,2025-01-15
backend,BE-2,CRUD,3.5,Data Operations,2025-01-16
frontend,FE-1,Dashboard,6.0,Content Management,2025-01-15
```

**Requirements:**

- Validate all required columns exist
- Validate each row's data types
- Continue importing valid rows even if some fail
- Report all errors at the end

## 12.2 Basic CSV Reading with Pandas

```python
import pandas as pd
from pathlib import Path

def read_csv_file(path: Path) -> pd.DataFrame:
    """Read CSV file into DataFrame."""
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Empty CSV file: {path}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Invalid CSV format: {e}")
```

## 12.3 Column Validation

```python
REQUIRED_COLUMNS = [
    "team",
    "member_name",
    "feature",
    "tracked_time_hours",
    "process",
    "date"
]

def validate_columns(df: pd.DataFrame) -> list:
    """Check for required columns.

    Returns:
        List of missing column names.
    """
    missing = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)
    return missing
```

## 12.4 Row Validation

```python
from datetime import date
from typing import Tuple, List, Optional
from models import TrackedTimeEntry, TeamType, ValidationError

def validate_row(
    row: pd.Series,
    row_number: int
) -> Tuple[Optional[TrackedTimeEntry], List[ValidationError]]:
    """Validate a single row and create entry if valid.

    Args:
        row: DataFrame row
        row_number: 1-indexed row number for error reporting

    Returns:
        Tuple of (entry or None, list of errors)
    """
    errors = []

    # Validate team
    team_str = str(row.get("team", "")).strip().lower()
    try:
        team = TeamType(team_str)
    except ValueError:
        errors.append(ValidationError(
            field="team",
            message=f"Invalid team type. Valid: {[t.value for t in TeamType]}",
            value=team_str
        ))
        team = None

    # Validate member_name
    member_name = str(row.get("member_name", "")).strip()
    if not member_name:
        errors.append(ValidationError(
            field="member_name",
            message="Cannot be empty",
            value=member_name
        ))

    # Validate feature
    feature = str(row.get("feature", "")).strip()
    if not feature:
        errors.append(ValidationError(
            field="feature",
            message="Cannot be empty",
            value=feature
        ))

    # Validate tracked_time_hours
    try:
        hours = float(row.get("tracked_time_hours", 0))
        if hours <= 0:
            errors.append(ValidationError(
                field="tracked_time_hours",
                message="Must be positive",
                value=hours
            ))
    except (ValueError, TypeError):
        errors.append(ValidationError(
            field="tracked_time_hours",
            message="Must be a number",
            value=row.get("tracked_time_hours")
        ))
        hours = None

    # Validate process
    process = str(row.get("process", "")).strip()
    if not process:
        errors.append(ValidationError(
            field="process",
            message="Cannot be empty",
            value=process
        ))

    # Validate date
    date_str = str(row.get("date", "")).strip()
    try:
        entry_date = date.fromisoformat(date_str)
    except ValueError:
        errors.append(ValidationError(
            field="date",
            message="Invalid date format. Use YYYY-MM-DD",
            value=date_str
        ))
        entry_date = None

    # If any errors, return None entry
    if errors:
        return None, errors

    # Create entry
    entry = TrackedTimeEntry(
        id=f"import_{row_number}_{date_str}",
        team=team,
        member_name=member_name,
        feature=feature,
        tracked_time_hours=hours,
        process=process,
        date=entry_date
    )

    return entry, []
```

## 12.5 Complete Import Function

```python
from dataclasses import dataclass
from typing import List, Tuple
from services.interfaces import ImportResult
from models import TrackedTimeEntry, ImportError, ValidationError

def import_csv_file(
    path: Path
) -> Tuple[List[TrackedTimeEntry], ImportResult]:
    """Import tracked time entries from CSV.

    Args:
        path: Path to CSV file

    Returns:
        Tuple of (valid entries, import result with statistics)

    Raises:
        ValueError: If file cannot be read or has invalid structure
    """
    # Read file
    df = read_csv_file(path)

    # Validate columns
    missing = validate_columns(df)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Process rows
    valid_entries: List[TrackedTimeEntry] = []
    import_errors: List[ImportError] = []

    for idx, row in df.iterrows():
        row_number = idx + 2  # +2 for 1-indexing and header row

        entry, errors = validate_row(row, row_number)

        if entry:
            valid_entries.append(entry)
        else:
            import_errors.append(ImportError(
                row_number=row_number,
                errors=errors,
                source=str(path)
            ))

    # Create result
    result = ImportResult(
        successful_count=len(valid_entries),
        failed_count=len(import_errors),
        total_count=len(df),
        errors=import_errors
    )

    return valid_entries, result
```

## 12.6 CLI Integration

```python
from rich.table import Table
from cli.formatting import console, print_success, print_error, print_warning

@time_app.command("import")
def time_import(
    file: Path = typer.Argument(..., help="CSV file path", exists=True),
    verbose: bool = typer.Option(False, "-v", help="Show error details")
):
    """Import tracked time entries from CSV."""
    try:
        entries, result = import_csv_file(file)
    except ValueError as e:
        print_error(str(e))
        raise typer.Exit(1)

    # Add entries to service
    for entry in entries:
        time_service.add_entry(entry)

    # Save to persistence
    time_persistence.save()

    # Report results
    if result.failed_count == 0:
        print_success(f"Imported {result.successful_count} entries")
    else:
        print_warning(
            f"Imported {result.successful_count}/{result.total_count} entries "
            f"({result.failed_count} failed)"
        )

        if verbose and result.errors:
            display_import_errors(result.errors)


def display_import_errors(errors: List[ImportError]) -> None:
    """Display import errors in a table."""
    table = Table(title="❌ Import Errors")
    table.add_column("Row", style="cyan")
    table.add_column("Field", style="yellow")
    table.add_column("Error", style="red")
    table.add_column("Value")

    for err in errors[:20]:  # Limit to first 20
        for val_err in err.errors:
            table.add_row(
                str(err.row_number),
                val_err.field,
                val_err.message,
                str(val_err.value)[:30]  # Truncate long values
            )

    console.print(table)

    if len(errors) > 20:
        console.print(f"[dim]... and {len(errors) - 20} more errors[/dim]")
```

## 12.7 Handling Common Issues

### Encoding Issues

```python
def read_csv_file(path: Path) -> pd.DataFrame:
    """Read CSV with encoding detection."""
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Cannot decode {path}. Try saving as UTF-8.")
```

### Flexible Column Names

```python
COLUMN_ALIASES = {
    "team": ["team", "team_name", "department"],
    "member_name": ["member_name", "member", "name", "developer"],
    "feature": ["feature", "feature_name", "task"],
    "tracked_time_hours": ["tracked_time_hours", "hours", "time", "duration"],
    "process": ["process", "process_type", "category"],
    "date": ["date", "entry_date", "work_date"]
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to standard names."""
    rename_map = {}

    for standard, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in df.columns and standard not in df.columns:
                rename_map[alias] = standard
                break

    return df.rename(columns=rename_map)
```

## 12.8 Your Turn: Exercise 12.1

Add support for optional columns:

```python
OPTIONAL_COLUMNS = {
    "notes": "",  # Default value
    "confidence": "medium"
}

def add_optional_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add optional columns with defaults if missing."""
    # TODO: For each optional column, add it with default if missing
    pass
```

## 12.9 Debugging Scenario

**The Bug:** Import fails silently with 0 entries.

```python
df = pd.read_csv("data.csv")
print(len(df))  # 100
# But import returns 0 valid entries!
```

**The Problem:** Column names have extra whitespace.

```python
print(df.columns.tolist())
# ['team ', ' member_name', 'feature', ...]  # Note the spaces!
```

**The Fix:** Strip column names:

```python
def read_csv_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()  # Remove whitespace
    return df
```

## 12.10 Quick Check Questions

1. Why continue importing after row errors instead of stopping?
2. How do you handle different date formats?
3. What's the purpose of row_number in error reporting?
4. Why try multiple encodings when reading CSV?
5. How do you handle columns with different names?

<details>
<summary>Answers</summary>

1. To maximize data import - one bad row shouldn't block 99 good ones
2. Use `pd.to_datetime()` with `format` parameter or try multiple formats
3. So users can find and fix the problematic row in their spreadsheet
4. Different systems export CSV with different encodings (Excel uses cp1252)
5. Use column aliases to map common variations to standard names

</details>

## 12.11 Mini-Project: Export to CSV

Create the reverse operation - export time entries to CSV:

```python
@time_app.command("export")
def time_export(
    output: Path = typer.Argument(..., help="Output CSV path"),
    feature: Optional[str] = typer.Option(None, "-f", help="Filter by feature")
):
    """Export tracked time entries to CSV."""
    # Get entries
    if feature:
        entries = time_service.get_entries_for_feature(feature)
    else:
        entries = list(time_service._entries.values())

    if not entries:
        print_warning("No entries to export")
        return

    # Convert to DataFrame
    data = [
        {
            "team": e.team.value,
            "member_name": e.member_name,
            "feature": e.feature,
            "tracked_time_hours": e.tracked_time_hours,
            "process": e.process,
            "date": e.date.isoformat()
        }
        for e in entries
    ]

    df = pd.DataFrame(data)
    df.to_csv(output, index=False)

    print_success(f"Exported {len(entries)} entries to {output}")
```

## 12.12 AITEA Integration

This chapter implements:

- **Requirement 2.4**: CSV import pipeline with validation and error collection
- **Property 6**: CSV Import Validation

**Verification:**

```bash
# Create test CSV
echo "team,member_name,feature,tracked_time_hours,process,date
backend,BE-1,CRUD,4.5,Data Operations,2025-01-15
backend,BE-2,CRUD,3.5,Data Operations,2025-01-16
invalid,,Missing,bad,Test,not-a-date" > test_import.csv

# Import with verbose errors
aitea time import test_import.csv -v

# Verify imported entries
aitea time list
```

## What's Next

Phase 2 is complete! In Chapter 13, we'll start Phase 3: LLM Fundamentals. You'll learn:

- How LLMs work (tokens, temperature, context)
- Creating a MockLLM for learning without API keys
- Basic prompt engineering

**Before proceeding:**

- Test CSV import with various edge cases
- Ensure error reporting is clear and helpful
- Try the export functionality
