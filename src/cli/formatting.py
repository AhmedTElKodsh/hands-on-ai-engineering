"""Rich output formatting utilities for AITEA CLI.

This module provides Rich-based formatting for:
- Feature listing tables with enhanced styling
- Estimation result panels with statistics
- Progress bars for long-running operations
"""

from typing import List, Optional, Iterator, Callable, TypeVar
from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.columns import Columns
from rich.box import ROUNDED, DOUBLE

from ..models import (
    Feature,
    TrackedTimeEntry,
    FeatureEstimate,
    ProjectEstimate,
    FeatureStatistics,
    ConfidenceLevel,
)

# Type variable for generic progress operations
T = TypeVar('T')


def get_confidence_style(confidence: ConfidenceLevel) -> str:
    """Get Rich style string for a confidence level.
    
    Args:
        confidence: The confidence level to style
        
    Returns:
        Rich style string (color name)
    """
    styles = {
        ConfidenceLevel.HIGH: "green",
        ConfidenceLevel.MEDIUM: "yellow",
        ConfidenceLevel.LOW: "red",
    }
    return styles.get(confidence, "white")


def get_confidence_icon(confidence: ConfidenceLevel) -> str:
    """Get an icon/emoji for a confidence level.
    
    Args:
        confidence: The confidence level
        
    Returns:
        Unicode icon representing the confidence
    """
    icons = {
        ConfidenceLevel.HIGH: "●●●",
        ConfidenceLevel.MEDIUM: "●●○",
        ConfidenceLevel.LOW: "●○○",
    }
    return icons.get(confidence, "○○○")


# ============================================================================
# Feature Tables (Task 13.1)
# ============================================================================

def create_feature_table(
    features: List[Feature],
    title: str = "Feature Library",
    show_notes: bool = False,
) -> Table:
    """Create a Rich table for displaying features.
    
    Args:
        features: List of features to display
        title: Table title
        show_notes: Whether to include the notes column
        
    Returns:
        Configured Rich Table object
    """
    table = Table(
        title=title,
        box=ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
        title_style="bold white",
    )
    
    # Add columns with styling
    table.add_column("ID", style="dim cyan", no_wrap=True)
    table.add_column("Name", style="bold green")
    table.add_column("Team", style="magenta")
    table.add_column("Process", style="white")
    table.add_column("Seed Hours", justify="right", style="yellow")
    table.add_column("Synonyms", style="dim")
    
    if show_notes:
        table.add_column("Notes", style="dim italic", max_width=30)
    
    for feature in features:
        synonyms_text = ", ".join(feature.synonyms) if feature.synonyms else "—"
        
        row = [
            feature.id,
            feature.name,
            feature.team.value,
            feature.process,
            f"{feature.seed_time_hours:.1f}h",
            synonyms_text,
        ]
        
        if show_notes:
            notes_text = feature.notes[:27] + "..." if len(feature.notes) > 30 else feature.notes
            row.append(notes_text or "—")
        
        table.add_row(*row)
    
    return table


def create_feature_search_table(
    features: List[Feature],
    query: str,
) -> Table:
    """Create a Rich table for feature search results.
    
    Args:
        features: List of matching features
        query: The search query used
        
    Returns:
        Configured Rich Table object
    """
    table = Table(
        title=f"Search Results for '[bold]{query}[/bold]'",
        box=ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="green",
        caption=f"{len(features)} feature(s) found",
    )
    
    table.add_column("ID", style="dim cyan", no_wrap=True)
    table.add_column("Name", style="bold green")
    table.add_column("Team", style="magenta")
    table.add_column("Process", style="white")
    table.add_column("Seed Hours", justify="right", style="yellow")
    
    for feature in features:
        table.add_row(
            feature.id,
            feature.name,
            feature.team.value,
            feature.process,
            f"{feature.seed_time_hours:.1f}h",
        )
    
    return table


# ============================================================================
# Time Entry Tables
# ============================================================================

def create_time_entries_table(
    entries: List[TrackedTimeEntry],
    title: str = "Time Entries",
) -> Table:
    """Create a Rich table for displaying time entries.
    
    Args:
        entries: List of time entries to display
        title: Table title
        
    Returns:
        Configured Rich Table object
    """
    table = Table(
        title=title,
        box=ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )
    
    table.add_column("ID", style="dim cyan", no_wrap=True)
    table.add_column("Feature", style="bold green")
    table.add_column("Member", style="magenta")
    table.add_column("Team", style="white")
    table.add_column("Hours", justify="right", style="yellow")
    table.add_column("Process", style="dim")
    table.add_column("Date", style="dim")
    
    for entry in entries:
        table.add_row(
            entry.id,
            entry.feature,
            entry.member_name,
            entry.team.value,
            f"{entry.tracked_time_hours:.1f}h",
            entry.process,
            entry.date.isoformat(),
        )
    
    return table


# ============================================================================
# Estimation Panels (Task 13.2)
# ============================================================================

def create_statistics_panel(statistics: FeatureStatistics) -> Panel:
    """Create a Rich panel displaying feature statistics.
    
    Args:
        statistics: The statistics to display
        
    Returns:
        Configured Rich Panel object
    """
    content = Text()
    content.append("Mean:      ", style="bold")
    content.append(f"{statistics.mean:.1f}h\n", style="cyan")
    content.append("Median:    ", style="bold")
    content.append(f"{statistics.median:.1f}h\n", style="cyan")
    content.append("Std Dev:   ", style="bold")
    content.append(f"{statistics.std_dev:.1f}h\n", style="cyan")
    content.append("P80:       ", style="bold")
    content.append(f"{statistics.p80:.1f}h\n", style="yellow bold")
    content.append("Data Pts:  ", style="bold")
    content.append(f"{statistics.data_point_count}", style="green")
    
    return Panel(
        content,
        title="[bold]Statistics[/bold]",
        border_style="blue",
        box=ROUNDED,
    )


def create_feature_estimate_panel(estimate: FeatureEstimate) -> Panel:
    """Create a Rich panel for a single feature estimate.
    
    Args:
        estimate: The feature estimate to display
        
    Returns:
        Configured Rich Panel object
    """
    confidence_style = get_confidence_style(estimate.confidence)
    confidence_icon = get_confidence_icon(estimate.confidence)
    
    content = Text()
    content.append("Estimated Hours: ", style="bold")
    content.append(f"{estimate.estimated_hours:.1f}h\n", style="yellow bold")
    content.append("Confidence:      ", style="bold")
    content.append(f"{confidence_icon} ", style=confidence_style)
    content.append(f"{estimate.confidence.value.upper()}\n", style=f"bold {confidence_style}")
    content.append("Source:          ", style="bold")
    source = "Seed Time" if estimate.used_seed_time else "Historical Data"
    source_style = "dim" if estimate.used_seed_time else "green"
    content.append(source, style=source_style)
    
    return Panel(
        content,
        title=f"[bold green]{estimate.feature_name}[/bold green]",
        border_style=confidence_style,
        box=ROUNDED,
    )


def create_project_estimate_table(estimate: ProjectEstimate) -> Table:
    """Create a Rich table for project estimate breakdown.
    
    Args:
        estimate: The project estimate to display
        
    Returns:
        Configured Rich Table object
    """
    table = Table(
        title="Feature Breakdown",
        box=ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
    )
    
    table.add_column("Feature", style="bold green")
    table.add_column("Hours", justify="right", style="yellow")
    table.add_column("Confidence", justify="center")
    table.add_column("Source", style="dim")
    
    for fe in estimate.features:
        confidence_style = get_confidence_style(fe.confidence)
        confidence_icon = get_confidence_icon(fe.confidence)
        source = "Seed Time" if fe.used_seed_time else "Historical"
        
        table.add_row(
            fe.feature_name,
            f"{fe.estimated_hours:.1f}h",
            Text(f"{confidence_icon} {fe.confidence.value}", style=confidence_style),
            source,
        )
    
    # Add total row
    table.add_section()
    overall_style = get_confidence_style(estimate.confidence)
    overall_icon = get_confidence_icon(estimate.confidence)
    table.add_row(
        Text("TOTAL", style="bold white"),
        Text(f"{estimate.total_hours:.1f}h", style="bold yellow"),
        Text(f"{overall_icon} {estimate.confidence.value}", style=f"bold {overall_style}"),
        "",
    )
    
    return table


def create_project_summary_panel(estimate: ProjectEstimate) -> Panel:
    """Create a Rich panel summarizing the project estimate.
    
    Args:
        estimate: The project estimate to summarize
        
    Returns:
        Configured Rich Panel object
    """
    confidence_style = get_confidence_style(estimate.confidence)
    confidence_icon = get_confidence_icon(estimate.confidence)
    
    # Count features by confidence
    high_count = sum(1 for fe in estimate.features if fe.confidence == ConfidenceLevel.HIGH)
    medium_count = sum(1 for fe in estimate.features if fe.confidence == ConfidenceLevel.MEDIUM)
    low_count = sum(1 for fe in estimate.features if fe.confidence == ConfidenceLevel.LOW)
    
    # Count seed time usage
    seed_count = sum(1 for fe in estimate.features if fe.used_seed_time)
    historical_count = len(estimate.features) - seed_count
    
    content = Text()
    content.append("╭─────────────────────────────────╮\n", style="dim")
    content.append("│  ", style="dim")
    content.append("Total Estimated Hours", style="bold")
    content.append("       │\n", style="dim")
    content.append("│         ", style="dim")
    content.append(f"{estimate.total_hours:.1f}h", style="bold yellow")
    content.append("                │\n", style="dim")
    content.append("╰─────────────────────────────────╯\n\n", style="dim")
    
    content.append("Overall Confidence: ", style="bold")
    content.append(f"{confidence_icon} ", style=confidence_style)
    content.append(f"{estimate.confidence.value.upper()}\n\n", style=f"bold {confidence_style}")
    
    content.append("Confidence Breakdown:\n", style="bold")
    content.append(f"  ●●● High:   {high_count} feature(s)\n", style="green")
    content.append(f"  ●●○ Medium: {medium_count} feature(s)\n", style="yellow")
    content.append(f"  ●○○ Low:    {low_count} feature(s)\n\n", style="red")
    
    content.append("Data Sources:\n", style="bold")
    content.append(f"  Historical: {historical_count} feature(s)\n", style="green")
    content.append(f"  Seed Time:  {seed_count} feature(s)", style="dim")
    
    return Panel(
        content,
        title="[bold white]Project Estimate Summary[/bold white]",
        border_style=confidence_style,
        box=DOUBLE,
        padding=(1, 2),
    )


# ============================================================================
# Progress Bars (Task 13.3)
# ============================================================================

def create_progress_context() -> Progress:
    """Create a Rich Progress context for long-running operations.
    
    Returns:
        Configured Rich Progress object
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )


def create_simple_progress() -> Progress:
    """Create a simple spinner-based progress indicator.
    
    Returns:
        Configured Rich Progress object with spinner only
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
    )


@contextmanager
def progress_operation(
    console: Console,
    description: str,
    total: Optional[int] = None,
) -> Iterator[Callable[[int], None]]:
    """Context manager for progress-tracked operations.
    
    Args:
        console: Rich Console instance
        description: Description of the operation
        total: Total number of steps (None for indeterminate)
        
    Yields:
        A function to call to advance progress
        
    Example:
        with progress_operation(console, "Processing files", total=10) as advance:
            for file in files:
                process(file)
                advance(1)
    """
    if total is not None:
        progress = create_progress_context()
    else:
        progress = create_simple_progress()
    
    with progress:
        task_id = progress.add_task(description, total=total)
        
        def advance(amount: int = 1) -> None:
            progress.update(task_id, advance=amount)
        
        yield advance


def process_with_progress(
    console: Console,
    items: List[T],
    processor: Callable[[T], None],
    description: str = "Processing",
) -> None:
    """Process a list of items with a progress bar.
    
    Args:
        console: Rich Console instance
        items: List of items to process
        processor: Function to call for each item
        description: Description of the operation
    """
    with create_progress_context() as progress:
        task = progress.add_task(description, total=len(items))
        
        for item in items:
            processor(item)
            progress.update(task, advance=1)


# ============================================================================
# Utility Functions
# ============================================================================

def print_success(console: Console, message: str) -> None:
    """Print a success message with green checkmark.
    
    Args:
        console: Rich Console instance
        message: Message to display
    """
    console.print(f"[green]✓[/green] {message}")


def print_error(console: Console, message: str) -> None:
    """Print an error message with red X.
    
    Args:
        console: Rich Console instance
        message: Message to display
    """
    console.print(f"[red]✗[/red] {message}")


def print_warning(console: Console, message: str) -> None:
    """Print a warning message with yellow exclamation.
    
    Args:
        console: Rich Console instance
        message: Message to display
    """
    console.print(f"[yellow]![/yellow] {message}")


def print_info(console: Console, message: str) -> None:
    """Print an info message with blue info icon.
    
    Args:
        console: Rich Console instance
        message: Message to display
    """
    console.print(f"[blue]ℹ[/blue] {message}")
