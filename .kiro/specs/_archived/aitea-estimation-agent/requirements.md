# Requirements Document

## Introduction

AITEA (AI Time Estimation Agent for Web Projects) is a practical estimation workflow system that improves web project time estimates by learning from real time-tracking data at the feature/micro-step level. The system supports frontend frameworks (React, Next.js, Nuxt.js) and backend frameworks (Node.js, Django, Laravel), enabling Project Owners/Managers to seed feature libraries, update estimates from tracked data, and estimate new projects from BRDs/User Stories.

## Glossary

- **Feature**: A development building block or micro-step (e.g., ui-Page, tables, forms, CRUD, websocket, file-upload)
- **Process**: Middle-level functional area grouping related features (e.g., User Management, Content Management, Communication, Data Operations, Media Handling, Integration, Real-time, Background Processing)
- **Category/Project Type**: High-level product domain (e.g., Ecommerce, ERP, LMS, CMS, Marketplace, SaaS Dashboard)
- **Team**: Top-level grouping (Frontend, Backend)
- **Tracked Time**: Actual time logged by team members while implementing a feature
- **Seed Time**: Initial arbitrary time used only when tracked data is missing
- **Feature Library**: A structured collection of features with baseline time estimates organized by Team → Process → Feature
- **Estimation Table**: Computed statistics (mean, median, P80) derived from tracked time data
- **BRD**: Business Requirements Document describing project needs
- **P80**: 80th percentile value, representing a conservative estimate

## Feature Hierarchy

The system uses a three-tier hierarchy for organizing features:

```
Team (Category) → Process → Feature (with seed time)
```

### Frontend Features

| Process | Feature | Seed Time (hours) |
|---------|---------|-------------------|
| User Management | RBAC | 12 |
| Content Management | ui-Page | 6 |
| Content Management | tables | 5 |
| Content Management | forms | 3 |
| Content Management | filtering | 4 |
| Communication | messaging | 12 |
| Communication | notifications | 12 |
| Data Operations | CRUD | 4 |
| Data Operations | analytics | 8 |
| Media Handling | file-upload | 6 |
| Media Handling | streaming | 12 |
| Integration | 3rd-party-integration | 8 |
| Visual Enhancement | animations | 6 |

### Backend Features

| Process | Feature | Seed Time (hours) |
|---------|---------|-------------------|
| User Management | RBAC | 8 |
| Data Operations | CRUD | 4 |
| Data Operations | filtering | 4 |
| Data Operations | caching | 1 |
| Data Operations | statistics-and-charts | 8 |
| Communication | emails | 2 |
| Communication | push-notifications | 12 |
| Media Handling | file-upload | 4 |
| Media Handling | streaming | 12 |
| Media Handling | video-handling | 20 |
| Integration | 3rd-party-integration | 8 |
| Integration | payment | 8 |
| Real-time | websocket | 12 |
| Background Processing | background-tasks | 12 |

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

### Requirement 1: Feature Library Management

**User Story:** As a Project Manager, I want to create and maintain a feature library with baseline times organized by process, so that I can have a foundation for project estimation even without historical data.

#### Acceptance Criteria

1. WHEN a user creates a new feature library, THE System SHALL generate a structured table containing feature name, process, team assignment (frontend/backend/both), seed time hours per team, notes, and synonyms fields
2. WHEN a user adds a feature to the library, THE System SHALL validate that required fields (feature name, process, team, seed_time_hours) are provided and store the feature record
3. WHEN a user searches for a feature, THE System SHALL match against both feature names and defined synonyms using case-insensitive comparison
4. WHEN a user updates a feature's seed time, THE System SHALL preserve the previous value in history and apply the new seed time for future estimates
5. WHEN the System displays the feature library, THE System SHALL present features grouped by process and sorted alphabetically with all fields visible in tabular format
6. WHEN a user lists processes, THE System SHALL display all available processes (User Management, Content Management, Communication, Data Operations, Media Handling, Integration, Real-time, Background Processing, Visual Enhancement)

### Requirement 2: Time Tracking Data Import

**User Story:** As a Project Manager, I want to import time-tracking CSV data with process categorization, so that the system can learn from actual implementation times organized by functional area.

#### Acceptance Criteria

1. WHEN a user uploads a CSV file, THE System SHALL validate the schema contains required columns: team, member_name, feature, tracked_time_hours
2. WHEN a CSV contains optional columns (process, category, date), THE System SHALL parse and store these fields for enhanced analysis and hierarchical organization
3. WHEN tracked_time_hours values are in minutes or days, THE System SHALL convert them to hours using configurable conversion factors (60 minutes/hour, 8 hours/day)
4. WHEN a CSV row contains invalid data, THE System SHALL log the error with row number and continue processing remaining rows
5. WHEN import completes, THE System SHALL report total rows processed, successful imports, and failed imports with error details
6. WHEN a process column is provided, THE System SHALL validate it against known processes (User Management, Content Management, Communication, Data Operations, Media Handling, Integration, Real-time, Background Processing, Visual Enhancement)

### Requirement 3: Category Mapping Management

**User Story:** As a Project Manager, I want to map features to project categories, so that I can quickly identify relevant features for different project types.

#### Acceptance Criteria

1. WHEN a user creates a category mapping, THE System SHALL store the relationship between category, feature, and priority level (core/common/optional)
2. WHEN a feature is assigned to multiple categories, THE System SHALL maintain all category associations without duplication
3. WHEN a user queries features by category, THE System SHALL return all mapped features sorted by priority level (core first, then common, then optional)
4. WHEN a user adds a new category, THE System SHALL validate the category name is unique and create the category record
5. WHEN displaying category mappings, THE System SHALL present a table with category, feature, priority, and notes columns

### Requirement 4: Estimation Table Computation

**User Story:** As a Project Manager, I want the system to compute learned estimates from tracked time data, so that estimates improve based on real implementation experience.

#### Acceptance Criteria

1. WHEN tracked time data exists for a feature, THE System SHALL compute count_entries, mean_hours, median_hours, p80_hours, and std_dev statistics
2. WHEN computing statistics, THE System SHALL normalize feature names by trimming whitespace, converting to lowercase, and matching against synonyms
3. WHEN a tracked time entry exceeds 3x the median for that feature, THE System SHALL flag the entry as a potential outlier and provide both raw and robust (outlier-excluded) statistics
4. WHEN a feature has no tracked data, THE System SHALL fall back to seed time and mark the basis as "seed"
5. WHEN displaying the estimation table, THE System SHALL show team, feature, all computed statistics, and data_coverage indicator (tracked/seed fallback)

### Requirement 5: Project Estimation from BRD

**User Story:** As a Project Manager, I want to estimate a new project from a BRD or user story, so that I can quickly generate time estimates for project planning.

#### Acceptance Criteria

1. WHEN a user provides a BRD or user story, THE System SHALL extract candidate features by parsing requirements text and matching against the feature library
2. WHEN extracted features match existing library entries, THE System SHALL use synonym matching with case-insensitive comparison
3. WHEN requirements imply features absent from the library, THE System SHALL propose new features marked with new_feature=true and basis=seed
4. WHEN generating estimates, THE System SHALL produce a breakdown table with feature, team, category, estimated_hours, basis, confidence, and notes columns
5. WHEN requirements are ambiguous, THE System SHALL ask a maximum of 3 targeted clarifying questions before proceeding with stated assumptions

### Requirement 6: Estimation Output Generation

**User Story:** As a Project Manager, I want clear estimation outputs with confidence levels, so that I can make informed planning decisions.

#### Acceptance Criteria

1. WHEN generating project estimates, THE System SHALL calculate totals for frontend hours, backend hours, and grand total hours
2. WHEN assigning confidence levels, THE System SHALL use "high" for features with 5+ tracked entries and std_dev < 20% of mean, "medium" for 2-4 entries, and "low" for seed-based or single-entry estimates
3. WHEN features potentially overlap (e.g., Auth vs Login page), THE System SHALL detect and flag the overlap, suggesting merge or separate tracking
4. WHEN displaying estimates, THE System SHALL clearly show the basis (tracked_mean, tracked_median, tracked_p80, or seed) for each line item
5. WHEN a user requests buffer suggestions, THE System SHALL provide buffer amounts clearly labeled as buffer separate from core estimates

### Requirement 7: Data Persistence and Export

**User Story:** As a Project Manager, I want to save and export estimation data, so that I can maintain historical records and share estimates with stakeholders.

#### Acceptance Criteria

1. WHEN a user saves the feature library, THE System SHALL persist all features, synonyms, and seed times to a JSON file
2. WHEN a user saves tracked time data, THE System SHALL persist all imported records with computed statistics to a JSON file
3. WHEN a user exports an estimation breakdown, THE System SHALL generate a formatted table in both JSON and CSV formats
4. WHEN loading saved data, THE System SHALL validate file integrity and report any corruption or missing required fields
5. WHEN a user requests the estimation table, THE System SHALL serialize the table with all computed fields preserving numeric precision to 2 decimal places

### Requirement 8: Estimation Style Configuration

**User Story:** As a Project Manager, I want to configure estimation preferences, so that estimates match my team's working conventions.

#### Acceptance Criteria

1. WHEN a user sets estimation style, THE System SHALL apply the selected method (mean, median, or P80) as the default for all estimates
2. WHEN a user configures working hours per day, THE System SHALL use the configured value (6 or 8 hours) for day-based conversions and reporting
3. WHEN a user sets team composition factors, THE System SHALL apply multipliers for junior (1.5x), mid (1.0x), and senior (0.8x) experience levels
4. WHEN a user configures buffer percentage, THE System SHALL calculate and display buffer amounts separately from base estimates
5. WHEN configuration changes occur, THE System SHALL recalculate all derived estimates using the new settings

### Requirement 9: Data Validation and Quality

**User Story:** As a Project Manager, I want the system to validate and score data quality, so that I can trust the accuracy of my estimates.

#### Acceptance Criteria

1. WHEN importing CSV data, THE System SHALL compute a data quality score based on completeness (all fields filled), consistency (valid values), and format compliance
2. WHEN duplicate entries are detected (same feature, team member, and date), THE System SHALL flag duplicates and offer merge or skip options
3. WHEN the same feature has time entries with variance exceeding 200% of the median, THE System SHALL generate an anomaly alert for user review
4. WHEN displaying import results, THE System SHALL show quality metrics including completeness percentage, duplicate count, and anomaly count
5. WHEN data quality score falls below 70%, THE System SHALL warn the user that estimates may be unreliable

### Requirement 10: Reporting and Visualization

**User Story:** As a Project Manager, I want visual reports and summaries, so that I can quickly understand estimation data and team performance.

#### Acceptance Criteria

1. WHEN a user requests a time distribution report, THE System SHALL display a CLI-based bar chart showing hours distribution across features
2. WHEN a user requests an estimation comparison report, THE System SHALL show seed times versus tracked times with variance percentages
3. WHEN a user requests a team productivity summary, THE System SHALL display average hours per feature by team member
4. WHEN generating reports, THE System SHALL support output formats including terminal display, JSON, and CSV
5. WHEN displaying charts in terminal, THE System SHALL use Rich library formatting with color-coded bars and legends

### Requirement 11: Feature Library Templates

**User Story:** As a Project Manager, I want pre-built feature library templates, so that I can quickly start estimating common project types.

#### Acceptance Criteria

1. WHEN a user requests available templates, THE System SHALL list built-in templates for Ecommerce, SaaS, CMS, Mobile App, and API-only projects
2. WHEN a user selects a template, THE System SHALL create a new feature library pre-populated with common features for that project type
3. WHEN a user exports a feature library as template, THE System SHALL save the library structure without tracked time data for sharing
4. WHEN a user imports a template, THE System SHALL merge template features with existing library, preserving user customizations
5. WHEN templates are updated in future versions, THE System SHALL offer to update user libraries with new template features

### Requirement 12: Estimation Scenarios

**User Story:** As a Project Manager, I want to create multiple estimation scenarios, so that I can plan for different outcomes and team compositions.

#### Acceptance Criteria

1. WHEN a user creates an estimation scenario, THE System SHALL generate best-case (P20), likely-case (median), and worst-case (P80) estimates
2. WHEN a user runs a "what-if" analysis, THE System SHALL recalculate estimates based on hypothetical team composition changes
3. WHEN comparing scenarios, THE System SHALL display side-by-side comparison of hours, costs, and timelines
4. WHEN a user saves a scenario, THE System SHALL persist scenario parameters and results for future reference
5. WHEN team composition changes in a scenario, THE System SHALL apply experience multipliers and show impact on total hours

### Requirement 13: Streamlit GUI (Optional)

**User Story:** As a Project Manager, I want a visual web interface for the estimation system, so that I can interact with features more intuitively than command line.

#### Acceptance Criteria

1. WHEN a user launches the Streamlit app, THE System SHALL display a dashboard with summary statistics including total features, tracked entries, and recent activity
2. WHEN viewing the feature library page, THE System SHALL present an interactive table with sorting, filtering, and inline add/edit/delete capabilities
3. WHEN importing CSV data, THE System SHALL provide drag-and-drop file upload with progress indication, validation feedback, and quality score display
4. WHEN generating estimates, THE System SHALL display an estimation interface with BRD text input, feature selection, and formatted results table with export buttons
5. WHEN viewing reports, THE System SHALL display interactive charts for time distribution, estimation comparison, and team productivity with date range filters
6. WHEN configuring settings, THE System SHALL provide a settings page with all configuration options (estimation style, working hours, experience multipliers, buffer percentage)

