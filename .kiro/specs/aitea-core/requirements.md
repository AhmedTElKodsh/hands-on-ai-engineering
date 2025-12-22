# Requirements Document: AITEA Core

## Introduction

AITEA Core is the shared foundation library for the AITEA (AI Time Estimation Agent) ecosystem. It provides data models, core services, and utilities that are used by both the CLI tool (Phase 1) and the Web application (Phase 2).

## Glossary

- **System**: The AITEA Core library including all models, services, and utilities
- **Service**: A component within the System that provides specific functionality (Feature Library Service, Time Tracking Service, Estimation Service, Configuration Service)
- **Utility**: A helper function within the System that performs common operations
- **Feature**: Atomic development task (e.g., ui-Page, tables, forms, CRUD, websocket, file-upload)
- **Process**: Middle-level functional area grouping related features (e.g., User Management, Content Management)
- **Team**: Top-level grouping (Frontend, Backend)
- **Tracked Time**: Actual time logged by team members while implementing a feature
- **Seed Time**: Initial arbitrary time used only when tracked data is missing
- **Feature Library**: Structured collection of features with baseline time estimates
- **Estimation Table**: Computed statistics (mean, median, P80) derived from tracked time data
- **P80**: 80th percentile value, representing a conservative estimate

## Feature Hierarchy

```
Team (Category) → Process → Feature (with seed time)
```

### Process Definitions

| Process | Description |
|---------|-------------|
| **User Management** | Authentication, authorization, user profiles, RBAC |
| **Content Management** | Pages, forms, tables, data display and manipulation |
| **Communication** | Messaging, notifications, emails, push notifications |
| **Data Operations** | CRUD operations, filtering, caching, analytics |
| **Media Handling** | File uploads, streaming, video/audio processing |
| **Integration** | Third-party APIs, payment gateways, webhooks |
| **Real-time** | WebSocket, live updates, streaming connections |
| **Background Processing** | Async tasks, scheduled jobs, queues |
| **Visual Enhancement** | Animations, transitions, UI polish |

## Requirements

### Requirement 1: Data Models

**User Story:** As a developer, I want well-defined data models, so that all AITEA components share consistent data structures.

#### Acceptance Criteria

1. WHEN defining a Feature, THE System SHALL include: id, name, team, process, seed_time_hours, notes, synonyms, seed_time_history, created_at, updated_at
2. WHEN defining a TrackedTimeEntry, THE System SHALL include: id, team, member_name, feature, tracked_time_hours, process (optional), category (optional), date (optional), imported_at
3. WHEN defining FeatureStatistics, THE System SHALL include: feature_name, team, count_entries, mean_hours, median_hours, p80_hours, std_dev, data_coverage, outlier_flags, robust_statistics
4. WHEN defining ProjectEstimate, THE System SHALL include: id, breakdown (list of EstimateLineItem), frontend_total_hours, backend_total_hours, grand_total_hours, buffer_hours, overlap_warnings, created_at
5. WHEN defining EstimationConfig, THE System SHALL include: estimation_style, working_hours_per_day, experience_multipliers, buffer_percentage, time_conversion

### Requirement 2: Feature Library Service

**User Story:** As a developer, I want a reusable feature library service, so that feature management is consistent across CLI and Web interfaces.

#### Acceptance Criteria

1. WHEN adding a feature with missing required fields (name, process, team, or seed_time_hours), THE Service SHALL reject the input and return a validation error identifying the missing field
2. WHEN searching features with a query string, THE Service SHALL match against both feature names and synonyms using case-insensitive comparison and return all matching features
3. WHEN updating seed time for a feature, THE Service SHALL preserve the previous value in the seed_time_history list before applying the new value
4. WHEN listing features, THE Service SHALL return all features grouped by process and sorted alphabetically by feature name within each process

### Requirement 3: Time Tracking Service

**User Story:** As a developer, I want a reusable time tracking service, so that time data import and retrieval is consistent.

#### Acceptance Criteria

1. WHEN validating CSV schema, THE Service SHALL verify the presence of required columns (team, member_name, feature, tracked_time_hours) and return false if any are missing
2. WHEN importing CSV data, THE Service SHALL process optional columns (process, category, date) when present and convert time values to hours using the configured time conversion settings
3. WHEN import fails for a row due to validation errors, THE Service SHALL record the error with row number and field details, then continue processing remaining rows
4. WHEN import completes, THE Service SHALL return an ImportResult containing total row count, successful import count, and failed import count with error details

### Requirement 4: Estimation Computation Service

**User Story:** As a developer, I want a reusable estimation service, so that statistical computations are consistent.

#### Acceptance Criteria

1. WHEN computing statistics for a feature with tracked time entries, THE Service SHALL calculate mean, median, P80, and standard deviation values using numpy functions
2. WHEN computing statistics for a feature with zero tracked time entries, THE Service SHALL use the feature seed time as the estimate and mark the basis field as "seed"
3. WHEN assigning confidence level, THE Service SHALL assign "high" for features with 5 or more entries and coefficient of variation below 0.2, "medium" for features with 2-4 entries, and "low" for features with seed-based estimates or single entries
4. WHEN generating project estimates, THE Service SHALL apply the configured estimation style (mean, median, or P80) to select the appropriate statistical value for each feature

### Requirement 5: Configuration Service

**User Story:** As a developer, I want a reusable configuration service, so that estimation preferences are managed consistently.

#### Acceptance Criteria

1. WHEN setting estimation style, THE Service SHALL accept and store one of three valid values: mean, median, or P80
2. WHEN setting experience multipliers, THE Service SHALL store and apply the multiplier factors: junior (1.5x), mid (1.0x), and senior (0.8x)
3. WHEN any configuration value changes, THE Service SHALL invoke all registered callback functions with the updated configuration object

### Requirement 6: Utility Functions

**User Story:** As a developer, I want shared utility functions, so that common operations are implemented once.

#### Acceptance Criteria

1. WHEN normalizing a feature name string, THE Utility SHALL remove leading and trailing whitespace and convert all characters to lowercase
2. WHEN detecting outliers in a set of time values, THE Utility SHALL flag and return the indices of entries that exceed 3 times the median value
3. WHEN converting time values between units, THE Utility SHALL support conversion between hours, minutes, and days using configurable conversion factors (default: 60 minutes per hour, 8 hours per day)
