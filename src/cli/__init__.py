"""Command-line interface for AITEA.

This module provides a Typer-based CLI application with commands for:
- Feature management (add, list, search)
- Time tracking (add, list)
- Project estimation
"""

import uuid
from datetime import date
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console

from ..models import (
    Feature,
    TrackedTimeEntry,
    TeamType,
)
from ..services.implementations import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)
from .formatting import (
    create_feature_table,
    create_feature_search_table,
    create_time_entries_table,
    create_project_estimate_table,
    create_project_summary_panel,
    create_progress_context,
    print_success,
    print_error,
    print_warning,
)

# Create console for rich output
console = Console()

# Create main app
app = typer.Typer(
    name="aitea",
    help="AI Time Estimation Agent - Estimate software development time using historical data.",
    no_args_is_help=True,
)

# Create subcommand groups
feature_app = typer.Typer(
    name="feature",
    help="Manage the feature library.",
    no_args_is_help=True,
)
time_app = typer.Typer(
    name="time",
    help="Manage tracked time entries.",
    no_args_is_help=True,
)

# Register subcommand groups
app.add_typer(feature_app, name="feature")
app.add_typer(time_app, name="time")

# Global service instances (in-memory for now)
_feature_service: Optional[FeatureLibraryService] = None
_time_service: Optional[TimeTrackingService] = None
_estimation_service: Optional[EstimationService] = None


def get_feature_service() -> FeatureLibraryService:
    """Get or create the feature library service."""
    global _feature_service
    if _feature_service is None:
        _feature_service = FeatureLibraryService()
    return _feature_service


def get_time_service() -> TimeTrackingService:
    """Get or create the time tracking service."""
    global _time_service
    if _time_service is None:
        _time_service = TimeTrackingService()
    return _time_service


def get_estimation_service() -> EstimationService:
    """Get or create the estimation service."""
    global _estimation_service
    if _estimation_service is None:
        _estimation_service = EstimationService(
            feature_library=get_feature_service(),
            time_tracking=get_time_service(),
        )
    return _estimation_service


# ============================================================================
# Feature Commands
# ============================================================================

@feature_app.command("add")
def feature_add(
    name: str = typer.Argument(..., help="Name of the feature"),
    team: TeamType = typer.Option(..., "--team", "-t", help="Team responsible for the feature"),
    seed_hours: float = typer.Option(..., "--seed-hours", "-s", help="Initial time estimate in hours"),
    process: str = typer.Option("Data Operations", "--process", "-p", help="Process type"),
    synonyms: Optional[str] = typer.Option(None, "--synonyms", help="Comma-separated list of synonyms"),
    notes: str = typer.Option("", "--notes", "-n", help="Additional notes"),
) -> None:
    """Add a new feature to the library."""
    service = get_feature_service()
    
    # Generate unique ID
    feature_id = f"feat_{uuid.uuid4().hex[:8]}"
    
    # Parse synonyms
    synonym_list: List[str] = []
    if synonyms:
        synonym_list = [s.strip() for s in synonyms.split(",") if s.strip()]
    
    # Create feature
    feature = Feature(
        id=feature_id,
        name=name,
        team=team,
        process=process,
        seed_time_hours=seed_hours,
        synonyms=synonym_list,
        notes=notes,
    )
    
    result = service.add_feature(feature)
    
    if result.is_ok():
        print_success(console, f"Feature '{name}' added with ID: {feature_id}")
    else:
        error = result.unwrap_err()
        print_error(console, f"Failed to add feature: {error.message}")
        raise typer.Exit(code=1)


@feature_app.command("list")
def feature_list(
    team: Optional[TeamType] = typer.Option(None, "--team", "-t", help="Filter by team"),
    show_notes: bool = typer.Option(False, "--notes", "-n", help="Show notes column"),
) -> None:
    """List all features in the library."""
    service = get_feature_service()
    features = service.list_features(team=team)
    
    if not features:
        print_warning(console, "No features found.")
        return
    
    title = "Feature Library"
    if team:
        title = f"Feature Library ({team.value} team)"
    
    table = create_feature_table(features, title=title, show_notes=show_notes)
    console.print(table)


@feature_app.command("search")
def feature_search(
    query: str = typer.Argument(..., help="Search query"),
) -> None:
    """Search for features by name or synonym."""
    service = get_feature_service()
    features = service.search_features(query)
    
    if not features:
        print_warning(console, f"No features found matching '{query}'.")
        return
    
    table = create_feature_search_table(features, query)
    console.print(table)



# ============================================================================
# Time Tracking Commands
# ============================================================================

@time_app.command("add")
def time_add(
    feature: str = typer.Argument(..., help="Name of the feature worked on"),
    hours: float = typer.Option(..., "--hours", "-h", help="Time spent in hours"),
    team: TeamType = typer.Option(..., "--team", "-t", help="Team that performed the work"),
    member: str = typer.Option(..., "--member", "-m", help="Team member name/identifier"),
    process: str = typer.Option("Data Operations", "--process", "-p", help="Process type"),
    entry_date: Optional[str] = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD), defaults to today"),
) -> None:
    """Add a tracked time entry."""
    service = get_time_service()
    
    # Generate unique ID
    entry_id = f"track_{uuid.uuid4().hex[:8]}"
    
    # Parse date
    if entry_date:
        try:
            parsed_date = date.fromisoformat(entry_date)
        except ValueError:
            console.print(f"[red]✗[/red] Invalid date format. Use YYYY-MM-DD.")
            raise typer.Exit(code=1)
    else:
        parsed_date = date.today()
    
    # Create entry
    entry = TrackedTimeEntry(
        id=entry_id,
        team=team,
        member_name=member,
        feature=feature,
        tracked_time_hours=hours,
        process=process,
        date=parsed_date,
    )
    
    result = service.add_entry(entry)
    
    if result.is_ok():
        print_success(console, f"Time entry added: {hours}h for '{feature}' by {member}")
    else:
        error = result.unwrap_err()
        print_error(console, f"Failed to add entry: {error.message}")
        raise typer.Exit(code=1)


@time_app.command("list")
def time_list(
    feature: Optional[str] = typer.Option(None, "--feature", "-f", help="Filter by feature name"),
) -> None:
    """List tracked time entries."""
    service = get_time_service()
    
    if feature:
        entries = service.get_entries_for_feature(feature)
        title = f"Time Entries for '{feature}'"
    else:
        # Get all entries (access internal storage for listing all)
        entries = list(service._entries.values())
        title = "All Time Entries"
    
    if not entries:
        print_warning(console, "No time entries found.")
        return
    
    table = create_time_entries_table(entries, title=title)
    console.print(table)


@time_app.command("import")
def time_import(
    csv_path: Path = typer.Argument(..., help="Path to CSV file to import"),
    show_errors: bool = typer.Option(True, "--show-errors/--hide-errors", help="Show detailed error messages"),
) -> None:
    """Import tracked time entries from a CSV file.
    
    The CSV file must have the following columns:
    - team: Team type (backend, frontend, fullstack, design, qa, devops)
    - member_name: Name/identifier of the team member
    - feature: Name of the feature worked on
    - tracked_time_hours: Time spent in hours (positive number)
    - process: Process type (e.g., "Data Operations")
    - date: Date in YYYY-MM-DD format
    """
    service = get_time_service()
    
    result = service.import_csv(csv_path)
    
    if result.is_err():
        error = result.unwrap_err()
        print_error(console, f"Import failed: {error}")
        raise typer.Exit(code=1)
    
    import_result = result.unwrap()
    
    # Display summary
    if import_result.successful_count > 0:
        print_success(
            console,
            f"Successfully imported {import_result.successful_count} of {import_result.total_count} entries"
        )
    
    if import_result.failed_count > 0:
        print_warning(
            console,
            f"Failed to import {import_result.failed_count} entries"
        )
        
        if show_errors and import_result.errors:
            console.print()
            console.print("[bold red]Import Errors:[/bold red]")
            for error in import_result.errors:
                console.print(f"  Row {error.row_number}:")
                for validation_error in error.errors:
                    console.print(f"    - {validation_error.field}: {validation_error.message}")
    
    if import_result.successful_count == 0 and import_result.failed_count == 0:
        print_warning(console, "CSV file was empty or contained no data rows")



# ============================================================================
# Estimation Commands
# ============================================================================

@app.command("estimate")
def estimate(
    features: List[str] = typer.Argument(..., help="Feature names to estimate"),
    summary_only: bool = typer.Option(False, "--summary", "-s", help="Show summary only"),
    show_progress: bool = typer.Option(False, "--progress", "-p", help="Show progress bar"),
) -> None:
    """Estimate time for a project consisting of multiple features."""
    service = get_estimation_service()
    
    if show_progress and len(features) > 1:
        # Use progress bar for multiple features
        from ..models import FeatureEstimate, ProjectEstimate, ConfidenceLevel
        
        feature_estimates: List[FeatureEstimate] = []
        errors: List[str] = []
        
        with create_progress_context() as progress:
            task = progress.add_task("Estimating features...", total=len(features))
            
            for feature_name in features:
                result = service.estimate_feature(feature_name)
                if result.is_err():
                    errors.append(f"{feature_name}: {result.unwrap_err().reason}")
                else:
                    feature_estimates.append(result.unwrap())
                progress.update(task, advance=1)
        
        if errors:
            for error in errors:
                print_error(console, error)
            raise typer.Exit(code=1)
        
        # Build project estimate from individual estimates
        total_hours = sum(fe.estimated_hours for fe in feature_estimates)
        confidence_order = [ConfidenceLevel.LOW, ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]
        overall_confidence = ConfidenceLevel.HIGH
        for fe in feature_estimates:
            if confidence_order.index(fe.confidence) < confidence_order.index(overall_confidence):
                overall_confidence = fe.confidence
        
        estimate_result = ProjectEstimate(
            features=feature_estimates,
            total_hours=total_hours,
            confidence=overall_confidence,
        )
    else:
        # Standard estimation without progress bar
        result = service.estimate_project(features)
        
        if result.is_err():
            error = result.unwrap_err()
            print_error(console, f"Estimation failed: {error.reason}")
            raise typer.Exit(code=1)
        
        estimate_result = result.unwrap()
    
    # Display feature breakdown table (unless summary only)
    if not summary_only:
        table = create_project_estimate_table(estimate_result)
        console.print(table)
        console.print()
    
    # Display summary panel
    summary_panel = create_project_summary_panel(estimate_result)
    console.print(summary_panel)


# ============================================================================
# Main Entry Point
# ============================================================================

def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
