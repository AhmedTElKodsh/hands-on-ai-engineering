# Chapter 10: Rich Terminal UI

**Difficulty:** Beginner  
**Time:** 1.5 hours  
**Prerequisites:** Chapter 9  
**AITEA Component:** `src/cli/formatting.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create formatted tables with Rich
2. Display styled panels and text
3. Add progress bars for long operations
4. Use colors and emoji effectively
5. Build a consistent CLI visual style

## 10.1 Why Rich?

Rich transforms plain terminal output into beautiful, readable displays:

**Before (plain):**

```
Feature: CRUD
Team: backend
Hours: 4.0
Confidence: medium
```

**After (Rich):**

```
┌─────────────────────────────────────┐
│         📊 Feature Estimate         │
├─────────────────────────────────────┤
│ Feature:    CRUD                    │
│ Team:       backend                 │
│ Hours:      4.0                     │
│ Confidence: MEDIUM ⚡               │
└─────────────────────────────────────┘
```

## 10.2 Getting Started with Rich

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

# Simple styled output
console.print("Hello, [bold green]World[/bold green]!")
console.print("[red]Error:[/red] Something went wrong", style="bold")
```

## 10.3 Creating Tables

Tables are perfect for listing features:

```python
from rich.table import Table
from rich.console import Console

def display_features_table(features: list) -> None:
    """Display features in a formatted table."""
    console = Console()

    table = Table(title="📚 Feature Library")

    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Team", style="yellow")
    table.add_column("Process")
    table.add_column("Seed Hours", justify="right", style="magenta")

    # Add rows
    for feature in features:
        table.add_row(
            feature.id,
            feature.name,
            feature.team.value,
            feature.process,
            f"{feature.seed_time_hours:.1f}h"
        )

    console.print(table)
```

**Output:**

```
                    📚 Feature Library
┏━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID    ┃ Name           ┃ Team     ┃ Process        ┃ Seed Hours ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ f1    │ CRUD API       │ backend  │ Data Operations│       4.0h │
│ f2    │ Authentication │ backend  │ Auth           │       8.0h │
│ f3    │ Dashboard      │ frontend │ Content        │      12.0h │
└───────┴────────────────┴──────────┴────────────────┴────────────┘
```

### Your Turn: Exercise 10.1

Create a table for tracked time entries:

```python
def display_time_entries_table(entries: list) -> None:
    """Display time entries in a formatted table."""
    console = Console()

    table = Table(title="⏱️ Tracked Time")

    # TODO: Add columns for ID, Feature, Member, Hours, Date
    # TODO: Add rows from entries

    console.print(table)
```

## 10.4 Panels for Estimates

Panels highlight important information:

```python
from rich.panel import Panel
from rich.text import Text

def display_estimate_panel(estimate: ProjectEstimate) -> None:
    """Display project estimate in a styled panel."""
    console = Console()

    # Build content
    content = Text()
    content.append(f"Total Hours: ", style="bold")
    content.append(f"{estimate.total_hours:.1f}\n", style="cyan bold")
    content.append(f"Confidence:  ", style="bold")

    # Color-code confidence
    conf_style = {
        "low": "red",
        "medium": "yellow",
        "high": "green"
    }[estimate.confidence.value]
    content.append(f"{estimate.confidence.value.upper()}", style=f"{conf_style} bold")

    # Create panel
    panel = Panel(
        content,
        title="📊 Project Estimate",
        border_style="blue"
    )

    console.print(panel)
```

## 10.5 Feature Breakdown Table

Combine panels and tables for detailed estimates:

```python
def display_full_estimate(estimate: ProjectEstimate) -> None:
    """Display complete estimate with breakdown."""
    console = Console()

    # Summary panel
    display_estimate_panel(estimate)

    # Breakdown table
    table = Table(title="📋 Feature Breakdown")
    table.add_column("Feature", style="cyan")
    table.add_column("Hours", justify="right")
    table.add_column("Confidence")
    table.add_column("Source")

    for fe in estimate.features:
        # Confidence emoji
        conf_emoji = {"low": "🔴", "medium": "🟡", "high": "🟢"}[fe.confidence.value]

        # Source indicator
        source = "📌 seed" if fe.used_seed_time else "📊 stats"

        table.add_row(
            fe.feature_name,
            f"{fe.estimated_hours:.1f}h",
            f"{conf_emoji} {fe.confidence.value}",
            source
        )

    console.print(table)
```

## 10.6 Progress Bars

For long operations like CSV import:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

def import_with_progress(file_path: Path, entries: list) -> None:
    """Import entries with progress bar."""
    console = Console()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("Importing entries...", total=len(entries))

        for entry in entries:
            # Process entry
            time_service.add_entry(entry)
            progress.update(task, advance=1)

    console.print("[green]✅ Import complete![/green]")
```

### Indeterminate Progress

For operations with unknown duration:

```python
with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
    task = progress.add_task("Processing...", total=None)

    # Do work
    result = long_running_operation()

    progress.update(task, description="[green]Done!")
```

## 10.7 Status Messages

Consistent status indicators:

```python
def print_success(message: str) -> None:
    """Print success message."""
    console = Console()
    console.print(f"[green]✅ {message}[/green]")

def print_error(message: str) -> None:
    """Print error message."""
    console = Console()
    console.print(f"[red]❌ {message}[/red]")

def print_warning(message: str) -> None:
    """Print warning message."""
    console = Console()
    console.print(f"[yellow]⚠️  {message}[/yellow]")

def print_info(message: str) -> None:
    """Print info message."""
    console = Console()
    console.print(f"[blue]ℹ️  {message}[/blue]")
```

## 10.8 Complete Formatting Module

Create `src/cli/formatting.py`:

```python
"""Rich formatting utilities for AITEA CLI."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from typing import List

from models import Feature, TrackedTimeEntry, ProjectEstimate, FeatureEstimate


console = Console()


def print_success(message: str) -> None:
    console.print(f"[green]✅ {message}[/green]")


def print_error(message: str) -> None:
    console.print(f"[red]❌ {message}[/red]")


def print_warning(message: str) -> None:
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def display_features(features: List[Feature]) -> None:
    """Display features in a table."""
    if not features:
        console.print("[dim]No features found.[/dim]")
        return

    table = Table(title="📚 Feature Library")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Team", style="yellow")
    table.add_column("Hours", justify="right", style="magenta")

    for f in features:
        table.add_row(f.id, f.name, f.team.value, f"{f.seed_time_hours:.1f}h")

    console.print(table)


def display_estimate(estimate: ProjectEstimate, verbose: bool = False) -> None:
    """Display project estimate."""
    # Confidence styling
    conf_colors = {"low": "red", "medium": "yellow", "high": "green"}
    conf_emoji = {"low": "🔴", "medium": "🟡", "high": "🟢"}

    color = conf_colors[estimate.confidence.value]
    emoji = conf_emoji[estimate.confidence.value]

    # Summary
    content = Text()
    content.append(f"Total Hours: ", style="bold")
    content.append(f"{estimate.total_hours:.1f}h\n", style="cyan bold")
    content.append(f"Confidence:  ", style="bold")
    content.append(f"{emoji} {estimate.confidence.value.upper()}", style=f"{color} bold")

    panel = Panel(content, title="📊 Project Estimate", border_style="blue")
    console.print(panel)

    # Breakdown
    if verbose:
        table = Table(title="📋 Breakdown")
        table.add_column("Feature", style="cyan")
        table.add_column("Hours", justify="right")
        table.add_column("Confidence")
        table.add_column("Source")

        for fe in estimate.features:
            e = conf_emoji[fe.confidence.value]
            src = "📌 seed" if fe.used_seed_time else "📊 stats"
            table.add_row(fe.feature_name, f"{fe.estimated_hours:.1f}h", f"{e} {fe.confidence.value}", src)

        console.print(table)


def create_progress() -> Progress:
    """Create a progress bar instance."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    )
```

## 10.9 Integrating with CLI

Update the CLI commands to use formatting:

```python
from cli.formatting import display_features, display_estimate, print_success, print_error

@feature_app.command("list")
def feature_list(team: Optional[TeamType] = None):
    """List all features."""
    features = feature_service.list_features(team)
    display_features(features)


@app.command()
def estimate(features: str, verbose: bool = typer.Option(False, "-v")):
    """Estimate project time."""
    feature_list = [f.strip() for f in features.split(",")]
    result = estimation_service.estimate_project(feature_list)

    if result.is_err():
        print_error(str(result.unwrap_err()))
        raise typer.Exit(1)

    display_estimate(result.unwrap(), verbose=verbose)
```

## 10.10 Debugging Scenario

**The Bug:** Colors don't show in Windows CMD.

**The Fix:** Rich auto-detects terminal capabilities, but you can force it:

```python
# Force color output
console = Console(force_terminal=True)

# Or check if colors are supported
if console.is_terminal:
    console.print("[green]Colored output[/green]")
else:
    print("Plain output")
```

## 10.11 Quick Check Questions

1. How do you add a column to a Rich table?
2. What's the syntax for inline styling?
3. How do you create an indeterminate progress bar?
4. What does `justify="right"` do for a column?
5. How do you create a panel with a title?

<details>
<summary>Answers</summary>

1. `table.add_column("Name", style="green")`
2. `[bold green]text[/bold green]`
3. Set `total=None` in `add_task()`
4. Right-aligns the column content
5. `Panel(content, title="My Title")`

</details>

## 10.12 Mini-Project: Dashboard View

Create a dashboard that shows system status:

```python
from rich.layout import Layout
from rich.live import Live

def display_dashboard():
    """Display AITEA dashboard."""
    console = Console()

    # Feature count
    features = feature_service.list_features()

    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body")
    )

    layout["header"].update(
        Panel("[bold blue]AITEA Dashboard[/bold blue]", style="blue")
    )

    # Stats panel
    stats = Text()
    stats.append(f"Features: {len(features)}\n", style="cyan")
    stats.append(f"Time Entries: {len(time_service._entries)}\n", style="green")

    layout["body"].update(Panel(stats, title="📈 Statistics"))

    console.print(layout)
```

## 10.13 AITEA Integration

This chapter implements:

- **Requirement 2.2**: Rich-formatted terminal output with tables, panels, and progress bars

**Verification:**

```bash
# Test formatted output
aitea feature list
aitea estimate "CRUD,Auth" --verbose
```

## What's Next

In Chapter 11, we'll implement JSON persistence to save and load data. You'll learn:

- Persisting features and time entries to JSON files
- Loading data on CLI startup
- Handling file I/O errors

**Before proceeding:**

- Ensure all CLI output uses Rich formatting
- Test on different terminals
- Try the dashboard view
