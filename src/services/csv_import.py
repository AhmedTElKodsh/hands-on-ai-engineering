"""CSV import functionality for AITEA time tracking data.

This module provides CSV import capabilities using pandas with validation
and error collection for invalid rows.
"""

import uuid
from datetime import date
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from ..models import (
    TrackedTimeEntry,
    TeamType,
    ValidationError,
    ImportError,
)
from .interfaces import ImportResult


# Expected CSV columns
REQUIRED_COLUMNS = ['team', 'member_name', 'feature', 'tracked_time_hours', 'process', 'date']


def validate_row(row: pd.Series, row_number: int) -> Tuple[TrackedTimeEntry | None, List[ValidationError]]:
    """Validate a single CSV row and convert to TrackedTimeEntry.
    
    Args:
        row: A pandas Series representing a CSV row
        row_number: The 1-indexed row number for error reporting
        
    Returns:
        Tuple of (TrackedTimeEntry or None, list of ValidationErrors)
    """
    errors: List[ValidationError] = []
    
    # Validate team
    team_value = row.get('team')
    team: TeamType | None = None
    if pd.isna(team_value) or str(team_value).strip() == '':
        errors.append(ValidationError(
            field='team',
            message='Team is required',
            value=team_value
        ))
    else:
        team_str = str(team_value).strip().lower()
        try:
            team = TeamType(team_str)
        except ValueError:
            valid_teams = [t.value for t in TeamType]
            errors.append(ValidationError(
                field='team',
                message=f'Invalid team. Must be one of: {", ".join(valid_teams)}',
                value=team_value
            ))
    
    # Validate member_name
    member_name = row.get('member_name')
    if pd.isna(member_name) or str(member_name).strip() == '':
        errors.append(ValidationError(
            field='member_name',
            message='Member name is required',
            value=member_name
        ))
    else:
        member_name = str(member_name).strip()
    
    # Validate feature
    feature = row.get('feature')
    if pd.isna(feature) or str(feature).strip() == '':
        errors.append(ValidationError(
            field='feature',
            message='Feature is required',
            value=feature
        ))
    else:
        feature = str(feature).strip()
    
    # Validate tracked_time_hours
    tracked_time_hours = row.get('tracked_time_hours')
    hours_value: float | None = None
    if pd.isna(tracked_time_hours):
        errors.append(ValidationError(
            field='tracked_time_hours',
            message='Tracked time hours is required',
            value=tracked_time_hours
        ))
    else:
        try:
            hours_value = float(tracked_time_hours)
            if hours_value <= 0:
                errors.append(ValidationError(
                    field='tracked_time_hours',
                    message='Tracked time hours must be positive',
                    value=tracked_time_hours
                ))
        except (ValueError, TypeError):
            errors.append(ValidationError(
                field='tracked_time_hours',
                message='Tracked time hours must be a number',
                value=tracked_time_hours
            ))
    
    # Validate process
    process = row.get('process')
    if pd.isna(process) or str(process).strip() == '':
        errors.append(ValidationError(
            field='process',
            message='Process is required',
            value=process
        ))
    else:
        process = str(process).strip()
    
    # Validate date
    date_value = row.get('date')
    parsed_date: date | None = None
    if pd.isna(date_value):
        errors.append(ValidationError(
            field='date',
            message='Date is required',
            value=date_value
        ))
    else:
        try:
            # Handle various date formats
            if isinstance(date_value, date):
                parsed_date = date_value
            elif isinstance(date_value, pd.Timestamp):
                parsed_date = date_value.date()
            else:
                # Try parsing as ISO format string
                parsed_date = date.fromisoformat(str(date_value).strip())
        except (ValueError, TypeError):
            errors.append(ValidationError(
                field='date',
                message='Invalid date format. Use YYYY-MM-DD',
                value=date_value
            ))
    
    # If there are errors, return None with the errors
    if errors:
        return None, errors
    
    # Create the TrackedTimeEntry
    entry = TrackedTimeEntry(
        id=f"track_{uuid.uuid4().hex[:8]}",
        team=team,  # type: ignore
        member_name=member_name,  # type: ignore
        feature=feature,  # type: ignore
        tracked_time_hours=hours_value,  # type: ignore
        process=process,  # type: ignore
        date=parsed_date,  # type: ignore
    )
    
    return entry, []


def import_csv_file(path: Path) -> Tuple[List[TrackedTimeEntry], ImportResult]:
    """Import tracked time entries from a CSV file.
    
    Args:
        path: Path to the CSV file to import
        
    Returns:
        Tuple of (list of valid TrackedTimeEntry objects, ImportResult with statistics)
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the CSV is missing required columns
    """
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    
    # Read CSV file
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")
    
    # Check for required columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}")
    
    # Process each row
    valid_entries: List[TrackedTimeEntry] = []
    import_errors: List[ImportError] = []
    
    for idx, row in df.iterrows():
        # Row numbers are 1-indexed, plus 1 for header row
        row_number = int(idx) + 2  # type: ignore
        
        entry, errors = validate_row(row, row_number)
        
        if entry is not None:
            valid_entries.append(entry)
        else:
            import_errors.append(ImportError(
                row_number=row_number,
                errors=errors,
                source=str(path)
            ))
    
    # Create import result
    total_count = len(df)
    successful_count = len(valid_entries)
    failed_count = len(import_errors)
    
    result = ImportResult(
        successful_count=successful_count,
        failed_count=failed_count,
        total_count=total_count,
        errors=import_errors
    )
    
    return valid_entries, result
