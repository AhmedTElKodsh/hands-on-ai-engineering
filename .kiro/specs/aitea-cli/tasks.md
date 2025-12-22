# Implementation Plan: AITEA CLI

## Prerequisites

- aitea-core package must be installed

## 1. Project Setup

- [ ] 1.1 Initialize CLI package structure
  - Create pyproject.toml with package metadata (name: aitea-cli)
  - Add dependency on aitea-core
  - Create src/aitea_cli/ directory structure
  - Create cli/, services/, templates/ subdirectories
  - Add **init**.py files to all packages
  - Create requirements.txt (typer[all], rich, aitea-core)
  - _Requirements: 1.1_

## 2. Persistence Service

- [ ] 2.1 Implement JSON Persistence Service

  - Create src/aitea_cli/services/persistence.py
  - Implement save_feature_library, load_feature_library
  - Implement save_tracked_time, load_tracked_time
  - Implement save_config, load_config
  - Handle file not found (return defaults)
  - Validate JSON integrity on load
  - _Requirements: 6.1-6.4_

- [ ]\* 2.2 Write tests for persistence round-trip
  - Test save then load produces equivalent data

## 3. CLI Framework

- [ ] 3.1 Create main CLI entry point
  - Create src/aitea_cli/cli/main.py with Typer app
  - Add --version command
  - Register sub-command groups (feature, tracked, estimate, config, quality, report, template, scenario)
  - Create src/aitea_cli/**main**.py for `python -m aitea_cli`
  - _Requirements: 1.1-1.3_

## 4. Feature Commands

- [ ] 4.1 Implement feature commands

  - Create src/aitea_cli/cli/feature.py
  - Implement `feature add` with name, team, process, seed-hours options
  - Implement `feature list` with table/json format option
  - Implement `feature search` with query argument
  - Implement `feature update` with id and optional fields
  - Implement `feature delete` with confirmation prompt
  - Use Rich tables for display
  - _Requirements: 2.1-2.5_

- [ ]\* 4.2 Write CLI tests for feature commands
  - Use typer.testing.CliRunner

## 5. Time Tracking Commands

- [ ] 5.1 Implement import command

  - Create src/aitea_cli/cli/tracked.py
  - Implement `import` command with file path argument
  - Add --dry-run option for preview
  - Display import results with Rich
  - _Requirements: 3.1-3.2_

- [ ] 5.2 Implement tracked data commands
  - Implement `tracked list` with optional feature filter
  - Implement `tracked stats` showing statistics per feature
  - _Requirements: 3.3-3.4_

## 6. Estimation Commands

- [ ] 6.1 Implement estimation commands
  - Create src/aitea_cli/cli/estimate.py
  - Implement `estimate brd` reading file and parsing
  - Implement `estimate features` with comma-separated list
  - Implement `estimate table` showing full estimation table
  - Implement `estimate export` with format and output options
  - _Requirements: 4.1-4.4_

## 7. Configuration Commands

- [ ] 7.1 Implement config commands
  - Create src/aitea_cli/cli/config.py
  - Implement `config show` displaying current config
  - Implement `config set` for key-value updates
  - Implement `config reset` restoring defaults
  - _Requirements: 5.1-5.3_

## 8. Data Quality Service & Commands

- [ ] 8.1 Implement Data Quality Service

  - Create src/aitea_cli/services/data_quality.py
  - Implement compute_quality_score (completeness, consistency)
  - Implement detect_duplicates (same feature, member, date)
  - Implement detect_anomalies (variance > 200% median)
  - _Requirements: 7.1-7.3_

- [ ] 8.2 Implement quality commands
  - Create src/aitea_cli/cli/quality.py
  - Implement `quality check` showing quality score
  - Implement `quality duplicates` listing duplicates
  - Implement `quality anomalies` listing anomalies
  - _Requirements: 7.1-7.3_

## 9. Reporting Service & Commands

- [ ] 9.1 Implement Reporting Service

  - Create src/aitea_cli/services/reporting.py
  - Implement generate_time_distribution
  - Implement generate_estimation_comparison
  - Implement generate_team_productivity
  - Implement render_bar_chart using Rich
  - _Requirements: 8.1-8.3_

- [ ] 9.2 Implement report commands
  - Create src/aitea_cli/cli/report.py
  - Implement `report distribution` with chart display
  - Implement `report comparison` showing seed vs tracked
  - Implement `report productivity` showing team stats
  - _Requirements: 8.1-8.3_

## 10. Template Service & Commands

- [ ] 10.1 Create built-in templates

  - Create src/aitea_cli/templates/ directory
  - Create ecommerce.json, saas.json, cms.json, mobile_app.json, api_only.json
  - Each template: 10-15 features with process assignments
  - _Requirements: 9.1_

- [ ] 10.2 Implement Template Service

  - Create src/aitea_cli/services/template.py
  - Implement list_templates
  - Implement apply_template
  - Implement export_as_template
  - _Requirements: 9.1-9.3_

- [ ] 10.3 Implement template commands
  - Create src/aitea_cli/cli/template.py
  - Implement `template list`
  - Implement `template apply <type>`
  - Implement `template export`
  - _Requirements: 9.1-9.3_

## 11. Scenario Service & Commands

- [ ] 11.1 Implement Scenario Service

  - Create src/aitea_cli/services/scenario.py
  - Implement create_scenario with best/likely/worst cases
  - Implement what_if_analysis with team composition changes
  - Implement compare_scenarios side-by-side
  - Implement save/load scenarios to JSON
  - _Requirements: 10.1-10.3_

- [ ] 11.2 Implement scenario commands
  - Create src/aitea_cli/cli/scenario.py
  - Implement `scenario create`
  - Implement `scenario list`
  - Implement `scenario what-if`
  - Implement `scenario compare`
  - _Requirements: 10.1-10.3_

## 12. Integration & Finalization

- [ ] 12.1 Wire services together

  - Create src/aitea_cli/container.py for dependency injection
  - Initialize all services with shared persistence
  - Update CLI commands to use container
  - _Requirements: All_

- [ ] 12.2 Create package entry point

  - Update pyproject.toml with entry point: `aitea = "aitea_cli.cli.main:app"`
  - Test installation with `pip install -e .`
  - _Requirements: All_

- [ ] 12.3 Checkpoint - Ensure all tests pass
  - Run pytest
  - Verify CLI commands work end-to-end
