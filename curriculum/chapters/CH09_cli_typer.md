# Chapter 9: CLI with Typer

**Difficulty:** Intermediate  
**Time:** 2 hours  
**Prerequisites:** Chapters 1-8  
**AITEA Component:** `src/cli/__init__.py`, `src/cli/__main__.py`

## Learning Objectives

By the end of this chapter, you will be able to:

1. Create CLI applications using Typer
2. Define commands with arguments and options
3. Organize commands into groups
4. Handle user input validation
5. Connect CLI commands to AITEA services

## 9.1 Why Typer?

Typer builds on Python type hints to create CLIs with minimal code:

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """Say hello to someone."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

**Run it:**

```bash
python hello.py World
# Output: Hello, World!

python hello.py --help
# Output: Usage: hello.py [OPTIONS] NAME
#         Say hello to someone.
```

## 9.2 Arguments vs Options

**Arguments** are positional and required:

```python
@app.command()
def greet(name: str):  # Required argument
    print(f"Hello, {name}")

# Usage: python app.py greet Alice
```

**Options** use flags and can have defaults:

```python
@app.command()
def greet(
    name: str,
    greeting: str = typer.Option("Hello", "--greeting", "-g")
):
    print(f"{greeting}, {name}")

# Usage: python app.py greet Alice --greeting Hi
```

## 9.3 AITEA CLI Structure

Let's build the AITEA CLI with command groups:

```python
import typer
from typing import Optional
from pathlib import Path

# Main app
app = typer.Typer(
    name="aitea",
    help="AI Time Estimation Agent - Estimate software development time"
)

# Command groups
feature_app = typer.Typer(help="Manage features in the library")
time_app = typer.Typer(help="Manage tracked time entries")

app.add_typer(feature_app, name="feature")
app.add_typer(time_app, name="time")
```

This creates a hierarchy:

```
aitea
├── feature
│   ├── add
│   ├── list
│   └── search
├── time
│   ├── add
│   └── import
└── estimate
```

## 9.4 Feature Commands

### Add Feature

```python
from models import Feature, TeamType

@feature_app.command("add")
def feature_add(
    id: str = typer.Argument(..., help="Unique feature ID"),
    name: str = typer.Argument(..., help="Feature name"),
    team: TeamType = typer.Option(..., "--team", "-t", help="Team type"),
    process: str = typer.Option(..., "--process", "-p", help="Process type"),
    seed_hours: float = typer.Option(..., "--hours", "-h", help="Seed time in hours"),
    synonyms: Optional[str] = typer.Option(None, "--synonyms", "-s", help="Comma-separated synonyms"),
    notes: str = typer.Option("", "--notes", "-n", help="Additional notes")
):
    """Add a new feature to the library."""
    # Parse synonyms
    synonym_list = [s.strip() for s in synonyms.split(",")] if synonyms else []

    # Create feature
    feature = Feature(
        id=id,
        name=name,
        team=team,
        process=process,
        seed_time_hours=seed_hours,
        synonyms=synonym_list,
        notes=notes
    )

    # Add to service
    result = feature_service.add_feature(feature)

    if result.is_ok():
        typer.echo(f"✅ Added feature: {name}")
    else:
        typer.echo(f"❌ Error: {result.unwrap_err()}", err=True)
        raise typer.Exit(1)
```

**Usage:**

```bash
aitea feature add f1 "CRUD API" -t backend -p "Data Operations" -h 4.0 -s "crud,rest-api"
```

### List Features

```python
@feature_app.command("list")
def feature_list(
    team: Optional[TeamType] = typer.Option(None, "--team", "-t", help="Filter by team")
):
    """List all features in the library."""
    features = feature_service.list_features(team)

    if not features:
        typer.echo("No features found.")
        return

    for f in features:
        typer.echo(f"[{f.id}] {f.name} ({f.team.value}) - {f.seed_time_hours}h")
```

### Your Turn: Exercise 9.1

Implement the `feature search` command:

```python
@feature_app.command("search")
def feature_search(
    query: str = typer.Argument(..., help="Search query")
):
    """Search for features by name or synonym."""
    # TODO: Call feature_service.search_features(query)
    # TODO: Display results or "No matches found"
    pass
```

## 9.5 Time Tracking Commands

### Add Time Entry

```python
from datetime import date

@time_app.command("add")
def time_add(
    id: str = typer.Argument(..., help="Entry ID"),
    feature: str = typer.Argument(..., help="Feature name"),
    hours: float = typer.Argument(..., help="Hours spent"),
    team: TeamType = typer.Option(..., "--team", "-t"),
    member: str = typer.Option(..., "--member", "-m", help="Team member name"),
    process: str = typer.Option(..., "--process", "-p"),
    entry_date: str = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD)")
):
    """Add a tracked time entry."""
    # Parse date or use today
    if entry_date:
        parsed_date = date.fromisoformat(entry_date)
    else:
        parsed_date = date.today()

    entry = TrackedTimeEntry(
        id=id,
        team=team,
        member_name=member,
        feature=feature,
        tracked_time_hours=hours,
        process=process,
        date=parsed_date
    )

    result = time_service.add_entry(entry)

    if result.is_ok():
        typer.echo(f"✅ Added time entry: {hours}h for {feature}")
    else:
        typer.echo(f"❌ Error: {result.unwrap_err()}", err=True)
        raise typer.Exit(1)
```

### Import CSV

```python
@time_app.command("import")
def time_import(
    file: Path = typer.Argument(..., help="Path to CSV file", exists=True)
):
    """Import tracked time entries from CSV."""
    result = time_service.import_csv(file)

    if result.is_ok():
        import_result = result.unwrap()
        typer.echo(f"✅ Imported {import_result.successful_count}/{import_result.total_count} entries")
        if import_result.failed_count > 0:
            typer.echo(f"⚠️  {import_result.failed_count} entries failed")
    else:
        typer.echo(f"❌ Import failed: {result.unwrap_err()}", err=True)
        raise typer.Exit(1)
```

## 9.6 Estimate Command

```python
@app.command()
def estimate(
    features: str = typer.Argument(..., help="Comma-separated feature names"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed breakdown")
):
    """Estimate time for a project."""
    feature_list = [f.strip() for f in features.split(",")]

    result = estimation_service.estimate_project(feature_list)

    if result.is_err():
        typer.echo(f"❌ Error: {result.unwrap_err()}", err=True)
        raise typer.Exit(1)

    estimate = result.unwrap()

    typer.echo(f"\n📊 Project Estimate")
    typer.echo(f"{'=' * 40}")
    typer.echo(f"Total Hours: {estimate.total_hours:.1f}")
    typer.echo(f"Confidence:  {estimate.confidence.value.upper()}")

    if verbose:
        typer.echo(f"\n📋 Feature Breakdown:")
        for fe in estimate.features:
            seed_marker = " (seed)" if fe.used_seed_time else ""
            typer.echo(f"  • {fe.feature_name}: {fe.estimated_hours:.1f}h [{fe.confidence.value}]{seed_marker}")
```

**Usage:**

```bash
aitea estimate "CRUD,Authentication,Dashboard" --verbose
```

## 9.7 Service Initialization

Create a module to initialize services:

```python
# src/cli/__init__.py
from services import FeatureLibraryService, TimeTrackingService, EstimationService

# Global service instances
feature_service = FeatureLibraryService()
time_service = TimeTrackingService()
estimation_service = EstimationService(feature_service, time_service)
```

## 9.8 Entry Point

Create `src/cli/__main__.py`:

```python
"""AITEA CLI entry point."""

from . import app

if __name__ == "__main__":
    app()
```

And configure in `pyproject.toml`:

```toml
[project.scripts]
aitea = "cli:app"
```

Now you can run:

```bash
# After pip install -e .
aitea --help
aitea feature list
aitea estimate "CRUD,Auth"
```

## 9.9 Debugging Scenario

**The Bug:** Enum option doesn't work.

```python
@app.command()
def test(team: TeamType):  # ❌ Typer doesn't know how to parse this!
    print(team)
```

**The Fix:** Typer automatically handles Enum types, but you need to use the string values:

```bash
# This works:
aitea feature add f1 "Test" --team backend  # Use "backend", not "TeamType.BACKEND"
```

If you need custom parsing:

```python
def parse_team(value: str) -> TeamType:
    try:
        return TeamType(value.lower())
    except ValueError:
        raise typer.BadParameter(f"Invalid team: {value}")

@app.command()
def test(team: str = typer.Option(..., callback=parse_team)):
    print(team)
```

## 9.10 Quick Check Questions

1. What's the difference between `typer.Argument` and `typer.Option`?
2. How do you create command groups?
3. How do you exit with an error code?
4. What does `exists=True` do for a Path argument?
5. How do you make an option required?

<details>
<summary>Answers</summary>

1. Arguments are positional; Options use flags (--name)
2. Create sub-Typer apps and use `app.add_typer()`
3. `raise typer.Exit(1)`
4. Validates the file exists before running the command
5. Use `...` as the default: `typer.Option(..., "--name")`

</details>

## 9.11 Mini-Project: Interactive Mode

Add an interactive mode that prompts for input:

```python
@app.command()
def interactive():
    """Interactive mode for adding features."""
    typer.echo("🎯 AITEA Interactive Mode")
    typer.echo("=" * 40)

    # Prompt for each field
    id = typer.prompt("Feature ID")
    name = typer.prompt("Feature name")

    # Show team options
    typer.echo("\nTeam options: " + ", ".join(t.value for t in TeamType))
    team_str = typer.prompt("Team")
    team = TeamType(team_str)

    process = typer.prompt("Process type")
    seed_hours = typer.prompt("Seed time (hours)", type=float)

    # Confirm
    typer.echo(f"\n📝 Creating feature:")
    typer.echo(f"   ID: {id}")
    typer.echo(f"   Name: {name}")
    typer.echo(f"   Team: {team.value}")
    typer.echo(f"   Hours: {seed_hours}")

    if typer.confirm("Create this feature?"):
        feature = Feature(id, name, team, process, seed_hours)
        result = feature_service.add_feature(feature)
        if result.is_ok():
            typer.echo("✅ Feature created!")
        else:
            typer.echo(f"❌ Error: {result.unwrap_err()}")
    else:
        typer.echo("Cancelled.")
```

## 9.12 AITEA Integration

This chapter implements:

- **Requirement 2.1**: Typer-based CLI with feature, time, and estimate commands

**Verification:**

```bash
# Test the CLI
aitea --help
aitea feature --help
aitea feature add f1 "CRUD" -t backend -p "Data Ops" -h 4.0
aitea feature list
aitea estimate "CRUD"
```

## What's Next

In Chapter 10, we'll add beautiful terminal output using Rich. You'll learn:

- Creating formatted tables
- Progress bars for long operations
- Styled panels and text

**Before proceeding:**

- Ensure all CLI commands work
- Test error handling paths
- Try the interactive mode
