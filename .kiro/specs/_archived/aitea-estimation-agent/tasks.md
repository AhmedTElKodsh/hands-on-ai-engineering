# Implementation Plan

## 1. Project Setup and Core Infrastructure

- [x] 1.1 Initialize Python project with pytest and Hypothesis
  - Create pyproject.toml with project metadata and dependencies (typer, rich, pandas, numpy, pydantic, pytest, hypothesis)
  - Create requirements.txt for pip installation
  - Set up pytest configuration in pytest.ini with Hypothesis settings (min_examples=100)
  - Create src/ directory structure: src/models/, src/services/, src/cli/, src/utils/
  - Create tests/ directory structure mirroring src/
  - Add __init__.py files to make packages importable
  - Create .gitignore for Python projects
  - Create README.md with project overview and setup instructions
  - _Requirements: All_

- [ ] 1.2 Create core data models and types in src/models/
  - Create src/models/__init__.py
  - Create src/models/enums.py with: Team, Process, Priority, Basis, Confidence, EstimationStyle, TimeUnit, ExperienceLevel, ProjectType
    - Process enum values: USER_MANAGEMENT, CONTENT_MANAGEMENT, COMMUNICATION, DATA_OPERATIONS, MEDIA_HANDLING, INTEGRATION, REAL_TIME, BACKGROUND_PROCESSING, VISUAL_ENHANCEMENT
  - Create src/models/feature.py with: Feature (including process field), FeatureLibrary, SeedTimeHistoryEntry dataclasses
  - Create src/models/tracking.py with: TrackedTimeEntry dataclass (including optional process field)
  - Create src/models/category.py with: Category, CategoryMapping dataclasses
  - Create src/models/statistics.py with: FeatureStatistics, OutlierFlag, RobustStatistics dataclasses
  - Create src/models/estimation.py with: ProjectEstimate, EstimateLineItem (including process field), OverlapWarning dataclasses
  - Create src/models/config.py with: EstimationConfig, ExperienceMultipliers, TimeConversion dataclasses
  - Create src/models/import_result.py with: ImportResult, ImportError dataclasses
  - Create src/models/brd.py with: ExtractedFeature (including process field), ParseResult, Ambiguity, MatchResult dataclasses
  - Create src/models/quality.py with: DataQualityScore, DuplicateEntry, AnomalyAlert dataclasses
  - Create src/models/reporting.py with: TimeDistributionReport, EstimationComparisonReport, TeamProductivityReport, ProcessSummaryReport dataclasses
  - Create src/models/template.py with: FeatureTemplate dataclass
  - Create src/models/scenario.py with: TeamComposition, ScenarioEstimate, Scenario, ScenarioComparison dataclasses
  - Create src/models/errors.py with: ValidationError exception and Result[T, E] generic type
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.4, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1, 12.1_

## 2. Feature Library Service

- [ ] 2.1 Implement Feature Library Service interface and core functionality
  - Create src/services/__init__.py
  - Create IFeatureLibraryService abstract base class in src/services/feature_library.py
  - Implement FeatureLibraryService class with in-memory storage (dictionary of features by ID)
  - Implement create_library() to generate empty FeatureLibrary with unique ID (use uuid.uuid4())
  - Implement add_feature() with validation for required fields (name, process, team, seed_time_hours) - return Result[Feature, ValidationError]
  - Implement update_feature() with seed time history preservation (append SeedTimeHistoryEntry to seed_time_history when seed_time_hours changes)
  - Implement delete_feature() to remove feature by ID - return Result[None, Exception]
  - Implement list_features() returning features grouped by process and sorted alphabetically by name
  - Implement list_processes() returning all available Process enum values
  - Implement get_features_by_process(process: Process) returning features filtered by process
  - _Requirements: 1.1, 1.2, 1.4, 1.5, 1.6_

- [ ]* 2.2 Write property test for feature validation
  - **Property 1: Feature validation rejects incomplete inputs**
  - **Validates: Requirements 1.2**
  - Create test_feature_library_props.py with Hypothesis strategies
  - Test that add_feature rejects inputs missing name, team, or seed_time_hours

- [ ]* 2.3 Write property test for seed time history
  - **Property 3: Seed time history preservation**
  - **Validates: Requirements 1.4**
  - Test that updating seed_time_hours preserves previous value in history array

- [ ]* 2.4 Write property test for alphabetical sorting
  - **Property 4: Feature library alphabetical sorting**
  - **Validates: Requirements 1.5**
  - Test that list_features() returns features in alphabetical order by name

- [ ] 2.5 Implement feature search with synonym matching
  - Implement search_features(query: str) with case-insensitive name and synonym matching
  - Implement get_feature_by_name_or_synonym(name: str) for exact matching (returns Optional[Feature])
  - Normalize search queries: strip whitespace, convert to lowercase
  - Search should check both feature.name and all items in feature.synonyms list
  - _Requirements: 1.3, 5.2_

- [ ]* 2.6 Write property test for case-insensitive synonym search
  - **Property 2: Feature search is case-insensitive and synonym-aware**
  - **Validates: Requirements 1.3, 5.2**
  - Test that search matches features regardless of case in name or synonyms

## 3. Time Tracking Service

- [ ] 3.1 Implement Time Tracking Service interface and CSV import
  - Create ITimeTrackingService abstract base class in src/services/time_tracking.py
  - Implement TimeTrackingService class with in-memory storage (list of TrackedTimeEntry)
  - Implement validate_schema(headers: List[str]) checking for required columns: team, member_name, feature, tracked_time_hours
  - Implement import_csv(file_path: str) using pandas.read_csv() with row-by-row validation
  - Handle optional columns (process, category, date) when present - parse date strings to datetime objects
  - Validate team values are in ["frontend", "backend"]
  - Validate process values against Process enum (User Management, Content Management, Communication, Data Operations, Media Handling, Integration, Real-time, Background Processing, Visual Enhancement)
  - Validate tracked_time_hours is a positive number
  - Return ImportResult with total_rows, successful_imports, failed_imports counts and error details
  - _Requirements: 2.1, 2.2, 2.4, 2.6_

- [ ]* 3.2 Write property test for CSV schema validation
  - **Property 5: CSV schema validation**
  - **Validates: Requirements 2.1**
  - Test that schemas with all required columns pass, missing columns fail

- [ ] 3.3 Implement time unit conversion utilities
  - Create src/utils/__init__.py
  - Create src/utils/time_conversion.py
  - Implement convert_to_hours(value: float, unit: TimeUnit, config: EstimationConfig) -> float
  - Support TimeUnit.HOURS (return value unchanged), TimeUnit.MINUTES (value ÷ config.time_conversion.minutes_per_hour), TimeUnit.DAYS (value × config.time_conversion.hours_per_day)
  - Use configurable conversion factors from EstimationConfig.time_conversion
  - _Requirements: 2.3_

- [ ]* 3.4 Write property test for time conversion round-trip
  - **Property 6: Time unit conversion round-trip**
  - **Validates: Requirements 2.3**
  - Test that hours -> minutes -> hours preserves value (within floating-point precision)

- [ ] 3.5 Implement import result reporting
  - Track total_rows, successful_imports, failed_imports in ImportResult
  - Generate ImportError objects with row_number, field, message, raw_value
  - Collect all errors during import and return in ImportResult.errors list
  - _Requirements: 2.5_

- [ ]* 3.6 Write property test for import count consistency
  - **Property 7: Import count consistency**
  - **Validates: Requirements 2.5**
  - Test that successful_imports + failed_imports == total_rows

## 4. Category Mapping Service

- [ ] 4.1 Implement Category Mapping Service interface and category management
  - Create ICategoryMappingService abstract base class in src/services/category_mapping.py
  - Implement CategoryMappingService class with in-memory storage (dictionary of categories by ID, list of mappings)
  - Implement create_category(name: str) with uniqueness validation (check existing category names, case-insensitive)
  - Return Result[Category, ValidationError] - error if duplicate name exists
  - Implement list_categories() returning all Category objects sorted by name
  - _Requirements: 3.4_

- [ ]* 4.2 Write property test for category uniqueness
  - **Property 8: Category uniqueness**
  - **Validates: Requirements 3.4**
  - Test that creating a category with duplicate name returns error

- [ ] 4.3 Implement feature-to-category mapping
  - Implement map_feature_to_category(feature_id: str, category_id: str, priority: Priority) -> Result[None, Exception]
  - Store CategoryMapping objects with priority (CORE/COMMON/OPTIONAL)
  - Implement get_features_by_category(category_id: str) returning features sorted by priority (CORE first, then COMMON, then OPTIONAL)
  - Implement get_categories_for_feature(feature_id: str) for reverse lookup
  - Prevent duplicate mappings (same feature_id + category_id combination) - return error if duplicate exists
  - Validate that feature_id and category_id exist before creating mapping
  - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [ ]* 4.4 Write property test for priority sorting
  - **Property 9: Category feature priority sorting**
  - **Validates: Requirements 3.3**
  - Test that get_features_by_category returns features in order: CORE, COMMON, OPTIONAL

## 5. Statistics and Estimation Computation

- [ ] 5.1 Implement statistical computation utilities
  - Create src/utils/statistics.py
  - Implement compute_mean(values: List[float]) -> float using numpy.mean()
  - Implement compute_median(values: List[float]) -> float using numpy.median()
  - Implement compute_p80(values: List[float]) -> float using numpy.percentile(values, 80)
  - Implement compute_p20(values: List[float]) -> float using numpy.percentile(values, 20) for best-case scenarios
  - Implement compute_std_dev(values: List[float]) -> float using numpy.std()
  - Handle edge cases: return 0.0 for empty arrays, return single value for single-element arrays
  - _Requirements: 4.1, 12.1_

- [ ]* 5.2 Write property test for statistics correctness
  - **Property 10: Statistics computation correctness**
  - **Validates: Requirements 4.1**
  - Test that mean equals sum/count, median is middle value when sorted

- [ ] 5.3 Implement feature name normalization utilities
  - Create src/utils/normalization.py
  - Implement normalize_feature_name(name: str) -> str: strip whitespace, convert to lowercase
  - Implement match_feature_with_synonyms(name: str, features: List[Feature]) -> Optional[Feature]
  - Match against both feature.name and feature.synonyms (all normalized)
  - Use normalization for grouping tracked time entries by feature
  - _Requirements: 4.2_

- [ ]* 5.4 Write property test for feature name normalization
  - **Property 11: Feature name normalization**
  - **Validates: Requirements 4.2**
  - Test that names differing only in whitespace/case are grouped together

- [ ] 5.5 Implement outlier detection
  - Create src/utils/outlier_detection.py
  - Implement detect_outliers(values: List[float], threshold: float = 3.0) -> List[int]
  - Flag entries where value > threshold × median (return list of indices)
  - Implement compute_robust_statistics(values: List[float], outlier_indices: List[int]) -> RobustStatistics
  - Compute statistics excluding outlier indices
  - Return RobustStatistics with mean_hours, median_hours, p80_hours, std_dev (all computed without outliers)
  - _Requirements: 4.3_

- [ ]* 5.6 Write property test for outlier detection
  - **Property 12: Outlier detection threshold**
  - **Validates: Requirements 4.3**
  - Test that entries exceeding 3x median are flagged as outliers

- [ ] 5.7 Implement Estimation Computation Service
  - Create IEstimationComputationService in src/services/estimation_computation.py
  - Implement EstimationComputationService class
  - Inject dependencies: FeatureLibraryService, TimeTrackingService, ConfigurationService
  - Implement compute_statistics(feature_name: str) -> FeatureStatistics
  - Use normalization to match feature names from tracked data
  - For features with tracked data: compute mean, median, p80, std_dev, mark data_coverage="tracked"
  - For features without tracked data: use seed_time_hours, mark data_coverage="seed"
  - Implement compute_estimation_table() -> List[FeatureStatistics] for all features
  - _Requirements: 4.4_

- [ ]* 5.8 Write property test for seed fallback
  - **Property 13: Seed fallback for missing data**
  - **Validates: Requirements 4.4**
  - Test that features with no tracked data use seed time and mark basis as "seed"

- [ ] 5.9 Checkpoint - Ensure all tests pass
  - Run pytest to verify all implemented tests pass
  - Ensure all tests pass, ask the user if questions arise.

## 6. Project Estimation Service

- [ ] 6.1 Implement confidence level assignment logic
  - Create src/utils/confidence.py
  - Implement assign_confidence(count: int, std_dev: float, mean: float, data_coverage: str) -> Confidence
  - Return Confidence.HIGH for count >= 5 and std_dev < 0.2 × mean and data_coverage == "tracked"
  - Return Confidence.MEDIUM for 2 <= count <= 4 and data_coverage == "tracked"
  - Return Confidence.LOW for seed-based (data_coverage == "seed") or single-entry (count == 1)
  - _Requirements: 6.2_

- [ ]* 6.2 Write property test for confidence level assignment
  - **Property 14: Confidence level assignment**
  - **Validates: Requirements 6.2**
  - Test confidence levels match the specified criteria

- [ ] 6.3 Implement project estimate generation
  - Extend EstimationComputationService with generate_project_estimate(features: List[ExtractedFeature]) -> ProjectEstimate
  - Create EstimateLineItem for each feature with: feature name, team, estimated_hours, basis, confidence, category, notes, is_new_feature
  - Use ConfigurationService.estimation_style to determine which statistic to use (mean/median/p80)
  - Set basis field to Basis.TRACKED_MEAN, TRACKED_MEDIAN, TRACKED_P80, or SEED based on data source and estimation style
  - Calculate frontend_total_hours (sum of frontend team + half of both team estimates)
  - Calculate backend_total_hours (sum of backend team + half of both team estimates)
  - Calculate grand_total_hours (sum of all estimates)
  - Generate unique ID for ProjectEstimate using uuid.uuid4()
  - _Requirements: 6.1, 6.4_

- [ ]* 6.4 Write property test for estimate totals consistency
  - **Property 15: Estimate totals consistency**
  - **Validates: Requirements 6.1**
  - Test that grand_total equals sum of all line items, frontend/backend totals match their respective items

- [ ] 6.5 Implement overlap detection
  - Implement detect_overlaps(features: List[str]) -> List[OverlapWarning] in EstimationComputationService
  - Use simple keyword detection: extract common keywords (auth, login, user, payment, etc.)
  - Check if multiple features contain the same keyword
  - Generate OverlapWarning with features list and suggestion text (e.g., "Consider merging or clarifying scope")
  - _Requirements: 6.3_

- [ ] 6.6 Implement buffer calculation
  - Add calculate_buffer(base_hours: float) -> float to EstimationComputationService
  - Use ConfigurationService.buffer_percentage to calculate buffer
  - Formula: buffer_hours = base_hours × (buffer_percentage / 100)
  - Store buffer_hours separately in ProjectEstimate (not added to grand_total_hours)
  - Ensure buffer is clearly labeled and not included in base totals
  - _Requirements: 6.5_

- [ ]* 6.7 Write property test for buffer separation
  - **Property 16: Buffer separation**
  - **Validates: Requirements 6.5**
  - Test that buffer is calculated separately and not included in base estimates

## 7. BRD Parser Service

- [ ] 7.1 Implement BRD Parser Service interface and text parsing
  - Create IBRDParserService abstract base class in src/services/brd_parser.py
  - Implement BRDParserService class
  - Implement parse_requirements(text: str) -> ParseResult
  - Implement extract_features(text: str) -> List[ExtractedFeature]
  - Use simple keyword extraction (look for common feature terms: "login", "auth", "dashboard", "payment", etc.)
  - Match extracted features against library using get_feature_by_name_or_synonym()
  - _Requirements: 5.1, 5.2_

- [ ] 7.2 Implement new feature proposal
  - In extract_features(), mark unmatched features with is_new_feature=True
  - Set matched_library_feature=None for new features
  - Suggest using seed time for new features (basis will be "seed")
  - _Requirements: 5.3_

- [ ] 7.3 Implement clarifying questions generation
  - Implement generate_clarifying_questions(ambiguities: List[Ambiguity]) -> List[str]
  - Detect ambiguous requirements (vague terms, missing details)
  - Generate targeted questions to resolve ambiguities
  - Limit output to maximum 3 questions (sort by importance, take top 3)
  - _Requirements: 5.5_

- [ ]* 7.4 Write property test for clarifying questions limit
  - **Property 21: Clarifying questions limit**
  - **Validates: Requirements 5.5**
  - Test that generate_clarifying_questions returns at most 3 questions

## 8. Configuration Service

- [ ] 8.1 Implement Configuration Service interface and management
  - Create IConfigurationService abstract base class in src/services/configuration.py
  - Implement ConfigurationService class with in-memory EstimationConfig
  - Implement get_config() -> EstimationConfig
  - Implement set_estimation_style(style: EstimationStyle)
  - Implement set_working_hours_per_day(hours: Literal[6, 8])
  - Implement set_experience_multipliers(multipliers: ExperienceMultipliers)
  - Implement set_buffer_percentage(percentage: float)
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ]* 8.2 Write property test for configuration application
  - **Property 19: Configuration application**
  - **Validates: Requirements 8.1**
  - Test that changing estimation style affects subsequent estimates

- [ ] 8.3 Implement experience multiplier application
  - Add apply_experience_multiplier(hours: float, level: ExperienceLevel) -> float to EstimationComputationService
  - Multiply base hours by multiplier from config (junior: 1.5, mid: 1.0, senior: 0.8)
  - _Requirements: 8.3_

- [ ]* 8.4 Write property test for experience multiplier
  - **Property 20: Experience multiplier application**
  - **Validates: Requirements 8.3**
  - Test that estimates are multiplied by correct experience level factor

- [ ] 8.5 Implement configuration change propagation
  - Add on_config_change(callback: Callable[[EstimationConfig], None]) to ConfigurationService
  - Implement invalidate_cached_estimates() to clear any cached computation results
  - Trigger recalculation when config changes (call registered callbacks)
  - _Requirements: 8.5_

- [ ]* 8.6 Write property test for config change recalculation
  - **Property 22: Configuration change triggers recalculation**
  - **Validates: Requirements 8.5**
  - Test that config changes result in different estimate values

## 9. Persistence Service

- [ ] 9.1 Implement Persistence Service interface and JSON persistence for feature library
  - Create IPersistenceService abstract base class in src/services/persistence.py
  - Implement PersistenceService class using JSON files
  - Implement save_feature_library(library: FeatureLibrary) -> Result[None, Exception]
  - Implement load_feature_library() -> Result[FeatureLibrary, Exception]
  - Use json.dump() with dataclasses.asdict() for serialization
  - Store in data/feature_library.json (create data/ directory if needed)
  - Implement validate_file_integrity(content: str) -> ValidationResult
  - _Requirements: 7.1, 7.4_

- [ ] 9.2 Implement JSON persistence for tracked time data
  - Implement save_tracked_time(data: TrackedTimeData) -> Result[None, Exception]
  - Implement load_tracked_time() -> Result[TrackedTimeData, Exception]
  - Store in data/tracked_time.json
  - Include all imported records and computed statistics
  - _Requirements: 7.2, 7.4_

- [ ]* 9.3 Write property test for data persistence round-trip
  - **Property 17: Data persistence round-trip**
  - **Validates: Requirements 7.1, 7.2**
  - Test that save then load produces equivalent data structures

- [ ] 9.4 Implement estimation export (JSON and CSV)
  - Implement export_estimation(estimate: ProjectEstimate, format: ExportFormat) -> str
  - For JSON: use json.dumps() with indent=2, round floats to 2 decimal places
  - For CSV: use pandas.DataFrame.to_csv() with float_format='%.2f'
  - Return formatted string ready for file writing
  - _Requirements: 7.3, 7.5_

- [ ]* 9.5 Write property test for numeric precision
  - **Property 18: Numeric precision preservation**
  - **Validates: Requirements 7.5**
  - Test that exported values have exactly 2 decimal places

## 10. CLI Interface

- [ ] 10.1 Implement CLI entry point and base structure
  - Create src/cli/main.py with Typer app
  - Set up Rich Console for formatted output
  - Add app.command() for --version showing package version
  - Configure help text and command descriptions
  - Initialize service instances (feature library, time tracking, etc.)
  - _Requirements: All_

- [ ] 10.2 Implement Feature Library CLI commands
  - `aitea feature add <name> --team <team> --seed-hours <hours> [--synonyms <list>]`
  - `aitea feature list [--format table|json]` - Use Rich Table for table format
  - `aitea feature search <query>` - Display matching features
  - `aitea feature update <id> [--name] [--team] [--seed-hours] [--synonyms]`
  - `aitea feature delete <id>` - Confirm before deletion
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 10.3 Implement Time Tracking CLI commands
  - `aitea import <csv_file> [--dry-run]` - Show preview without saving if dry-run
  - `aitea tracked list [--feature <name>] [--team <team>]` - Filter and display entries
  - `aitea tracked stats [--feature <name>]` - Show statistics for feature(s)
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 10.4 Implement Category CLI commands
  - `aitea category add <name>` - Create new category
  - `aitea category list` - Display all categories
  - `aitea category map <feature_id> <category_id> --priority <core|common|optional>`
  - `aitea category features <category_id>` - Show features in category
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 10.5 Implement Estimation CLI commands
  - `aitea estimate --brd <file>` - Read BRD file, parse, and estimate
  - `aitea estimate --features <list>` - Estimate comma-separated feature list
  - `aitea estimate table` - Display full estimation table with Rich Table
  - `aitea estimate export --format <json|csv> --output <file>` - Export to file
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 10.6 Implement Configuration CLI commands
  - `aitea config show` - Display current configuration in table format
  - `aitea config set <key> <value>` - Set config option (estimation_style, working_hours, etc.)
  - `aitea config reset` - Reset to default EstimationConfig values
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 10.7 Write CLI integration tests
  - Create tests/test_cli.py
  - Use typer.testing.CliRunner to test commands
  - Test all CLI commands with various inputs
  - Test error handling and user feedback messages
  - Test output formatting (table, JSON)
  - _Requirements: All_

## 11. Data Quality Service

- [ ] 11.1 Implement Data Quality Service interface and scoring
  - Create IDataQualityService abstract base class in src/services/data_quality.py
  - Implement DataQualityService class
  - Implement compute_quality_score(entries: List[TrackedTimeEntry]) -> DataQualityScore
  - Calculate completeness: percentage of non-null optional fields (category, date)
  - Calculate consistency: percentage of valid values (team in [frontend, backend], hours > 0)
  - Calculate overall score as weighted average: 0.6 × completeness + 0.4 × consistency
  - _Requirements: 9.1_

- [ ]* 11.2 Write property test for quality score calculation
  - **Property 23: Data quality score calculation**
  - **Validates: Requirements 9.1**
  - Test that overall score is weighted average of completeness and consistency

- [ ] 11.3 Implement duplicate detection
  - Implement detect_duplicates(entries: List[TrackedTimeEntry]) -> List[DuplicateEntry]
  - Detect entries with identical feature, member_name, and date
  - Return DuplicateEntry objects with original_id and duplicate_id
  - Implement merge_duplicates(original_id, duplicate_id) to combine entries
  - _Requirements: 9.2_

- [ ]* 11.4 Write property test for duplicate detection
  - **Property 24: Duplicate detection accuracy**
  - **Validates: Requirements 9.2**
  - Test that entries with same feature, member_name, date are flagged as duplicates

- [ ] 11.5 Implement anomaly detection
  - Implement detect_anomalies(entries: List[TrackedTimeEntry]) -> List[AnomalyAlert]
  - Group entries by feature, compute median for each feature
  - Flag entries where variance > 200% of median (value > 3 × median)
  - Generate AnomalyAlert with feature, entry_id, value, median, variance_percentage
  - _Requirements: 9.3_

- [ ]* 11.6 Write property test for anomaly detection
  - **Property 25: Anomaly detection threshold**
  - **Validates: Requirements 9.3**
  - Test that entries with variance > 200% of median generate anomaly alerts

- [ ] 11.7 Implement quality metrics display utilities
  - Create src/utils/quality_display.py
  - Format quality metrics: completeness %, duplicate count, anomaly count
  - Generate warning message when overall score < 70%
  - _Requirements: 9.4, 9.5_

- [ ] 11.8 Implement Data Quality CLI commands
  - `aitea quality check` - Run compute_quality_score and display results
  - `aitea quality duplicates [--merge|--skip]` - Show duplicates, handle based on flag
  - `aitea quality anomalies` - Display anomaly alerts in table format
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

## 12. Reporting Service

- [ ] 12.1 Implement Reporting Service interface and time distribution report
  - Create IReportingService abstract base class in src/services/reporting.py
  - Implement ReportingService class
  - Implement generate_time_distribution() -> TimeDistributionReport
  - Calculate total hours per feature from tracked time entries
  - Generate chart_data as List[Tuple[str, float]] for visualization
  - _Requirements: 10.1_

- [ ] 12.2 Implement estimation comparison report
  - Implement generate_estimation_comparison() -> EstimationComparisonReport
  - Compare seed_time_hours vs actual tracked mean/median for each feature
  - Calculate variance_percentage: ((tracked - seed) / seed) × 100
  - Return list of comparisons with feature, seed_hours, tracked_hours, variance_pct
  - _Requirements: 10.2_

- [ ] 12.3 Implement team productivity report
  - Implement generate_team_productivity() -> TeamProductivityReport
  - Group tracked entries by member_name
  - Calculate avg_hours, total_features, total_hours for each member
  - Return member_stats dictionary
  - _Requirements: 10.3_

- [ ] 12.4 Implement CLI bar chart rendering
  - Implement render_bar_chart(data: List[Tuple[str, float]], title: str) using Rich
  - Use Rich's BarChart or create custom bar visualization with colored blocks
  - Support color-coding by team (frontend=blue, backend=green)
  - Add legend for colors
  - _Requirements: 10.5_

- [ ] 12.5 Implement report export
  - Implement export_report(report: Any, format: str) -> str
  - Support format="json": json.dumps(report)
  - Support format="csv": convert to pandas DataFrame, then to_csv()
  - Support format="terminal": use Rich tables for display
  - _Requirements: 10.4_

- [ ] 12.6 Implement Reporting CLI commands
  - `aitea report distribution [--format table|chart|json]` - Generate and display time distribution
  - `aitea report comparison` - Show seed vs tracked comparison table
  - `aitea report productivity [--team <team>]` - Filter by team if specified
  - `aitea report export --type <type> --format <format> --output <file>` - Export report to file
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

## 13. Template Service

- [ ] 13.1 Create Template Service interface and built-in templates
  - Create ITemplateService abstract base class in src/services/template.py
  - Implement TemplateService class
  - Create src/templates/ directory with JSON template files
  - Create ecommerce.json: cart, checkout, payments, products, search, reviews (10-15 features)
  - Create saas.json: auth, dashboard, billing, settings, user management, notifications (10-15 features)
  - Create cms.json: content editor, media library, users, permissions, workflows (10-15 features)
  - Create mobile_app.json: navigation, push notifications, offline sync, camera, location (10-15 features)
  - Create api_only.json: REST endpoints, auth, rate limiting, logging, webhooks (10-15 features)
  - _Requirements: 11.1_

- [ ] 13.2 Implement template application
  - Implement list_templates() -> List[FeatureTemplate]
  - Implement get_template(project_type: ProjectType) -> FeatureTemplate
  - Implement apply_template(project_type: ProjectType) -> FeatureLibrary
  - Load template JSON, create FeatureLibrary with all template features
  - Assign unique IDs to features, set created_at timestamps
  - _Requirements: 11.2_

- [ ]* 13.3 Write property test for template application
  - **Property 26: Template application preserves structure**
  - **Validates: Requirements 11.2**
  - Test that all template features appear in resulting library with identical properties

- [ ] 13.4 Implement template export
  - Implement export_as_template(library: FeatureLibrary, name: str) -> FeatureTemplate
  - Create FeatureTemplate from library (exclude tracked time data)
  - Save as JSON file in templates/ directory
  - _Requirements: 11.3_

- [ ] 13.5 Implement template import and merge
  - Implement import_template(template: FeatureTemplate, merge: bool = True) -> FeatureLibrary
  - If merge=False: replace current library with template
  - If merge=True: add template features to existing library, skip duplicates by name
  - Preserve user customizations (notes, synonyms) for existing features
  - _Requirements: 11.4_

- [ ] 13.6 Implement Template CLI commands
  - `aitea template list` - Display available templates with descriptions
  - `aitea template apply <type>` - Apply template (ecommerce, saas, cms, mobile_app, api_only)
  - `aitea template export --output <file>` - Export current library as template JSON
  - `aitea template import <file> [--merge]` - Import template, merge if flag set
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

## 14. Scenario Service

- [ ] 14.1 Implement Scenario Service interface and scenario creation
  - Create IScenarioService abstract base class in src/services/scenario.py
  - Implement ScenarioService class with in-memory storage
  - Implement create_scenario(name: str, features: List[str], team: TeamComposition) -> Scenario
  - Store scenario with unique ID, feature list, and team composition
  - _Requirements: 12.1_

- [ ] 14.2 Implement multi-case estimation
  - Implement compute_scenario_estimate(scenario: Scenario) -> ScenarioEstimate
  - Calculate best_case_hours using P20 (20th percentile) from tracked data
  - Calculate likely_case_hours using median from tracked data
  - Calculate worst_case_hours using P80 (80th percentile) from tracked data
  - Apply experience multipliers based on team composition
  - _Requirements: 12.1_

- [ ]* 14.3 Write property test for scenario estimate consistency
  - **Property 27: Scenario estimate consistency**
  - **Validates: Requirements 12.1**
  - Test that best_case_hours <= likely_case_hours <= worst_case_hours

- [ ] 14.4 Implement what-if analysis
  - Implement what_if_analysis(base_scenario: Scenario, new_team: TeamComposition) -> Scenario
  - Create new scenario with same features but different team composition
  - Recalculate estimates with new experience multipliers
  - Show delta between base and new scenario
  - _Requirements: 12.2_

- [ ]* 14.5 Write property test for what-if team impact
  - **Property 28: What-if team composition impact**
  - **Validates: Requirements 12.2**
  - Test that changing team composition changes estimates proportionally to multipliers

- [ ] 14.6 Implement scenario comparison
  - Implement compare_scenarios(scenario_ids: List[str]) -> ScenarioComparison
  - Generate side-by-side comparison table with hours, costs (hours × hourly rate), timelines
  - Calculate differences and percentages between scenarios
  - _Requirements: 12.3_

- [ ] 14.7 Implement scenario persistence
  - Implement save_scenario(scenario: Scenario) -> Result[None, Exception]
  - Implement list_scenarios() -> List[Scenario]
  - Store scenarios in data/scenarios.json
  - _Requirements: 12.4_

- [ ] 14.8 Implement Scenario CLI commands
  - `aitea scenario create <name> --features <list>` - Create scenario with comma-separated features
  - `aitea scenario list` - Display all saved scenarios
  - `aitea scenario show <name>` - Show scenario details with best/likely/worst estimates
  - `aitea scenario what-if <name> --junior <n> --mid <n> --senior <n>` - Run what-if analysis
  - `aitea scenario compare <name1> <name2> [<name3>...]` - Compare multiple scenarios
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

## 15. Streamlit GUI (Optional)

- [ ]* 15.1 Set up Streamlit application structure
  - Add streamlit, plotly dependencies to requirements.txt
  - Create src/gui/ directory structure (app.py, pages/, components/, utils/)
  - Configure Streamlit page settings and navigation
  - _Requirements: 13.1_

- [ ]* 15.2 Implement Dashboard page
  - Display summary metrics (total features, tracked entries, quality score, avg confidence)
  - Show recent activity feed
  - Add quick action buttons
  - _Requirements: 13.1_

- [ ]* 15.3 Implement Feature Library page
  - Create interactive feature table with sorting and filtering
  - Implement add feature form with validation
  - Implement inline edit and delete functionality
  - Add search functionality
  - _Requirements: 13.2_

- [ ]* 15.4 Implement Import Data page
  - Create drag-and-drop file uploader for CSV
  - Display data preview with first 10 rows
  - Show quality metrics (total rows, quality score, duplicates)
  - Implement import with progress bar
  - Display import results and errors
  - _Requirements: 13.3_

- [ ]* 15.5 Implement Estimation page
  - Create BRD text input tab with analyze button
  - Create feature selection tab with multiselect
  - Display extracted features table
  - Display estimation results table
  - Add export buttons (JSON, CSV, PDF)
  - _Requirements: 13.4_

- [ ]* 15.6 Implement Reports page
  - Add date range filter
  - Create time distribution bar chart (Plotly)
  - Create seed vs tracked scatter plot with trendline
  - Create team productivity chart
  - Add export functionality for reports
  - _Requirements: 13.5_

- [ ]* 15.7 Implement Settings page
  - Create estimation style selector (mean/median/P80)
  - Create working hours radio buttons (6/8)
  - Create experience multiplier inputs (junior/mid/senior)
  - Create buffer percentage slider
  - Implement save settings functionality
  - _Requirements: 13.6_

- [ ]* 15.8 Implement session state management
  - Manage service instances across pages
  - Handle data persistence between page navigations
  - Implement caching for performance
  - _Requirements: 13.1-13.6_

## 16. Integration and Final Validation

- [ ] 16.1 Wire all services together
  - Create src/container.py for service container/dependency injection
  - Initialize all services: FeatureLibraryService, TimeTrackingService, EstimationComputationService, etc.
  - Share PersistenceService instance across all services
  - Share ConfigurationService instance for consistent config access
  - Update CLI main.py to use service container
  - _Requirements: All_

- [ ] 16.2 Create main entry point and package setup
  - Create src/__main__.py to enable `python -m aitea` execution
  - Update pyproject.toml with entry point: `aitea = "src.cli.main:app"`
  - Add package metadata: version, description, authors
  - Test installation with `pip install -e .`
  - _Requirements: All_

- [ ] 16.3 Checkpoint - Ensure all tests pass
  - Run `pytest tests/` to verify all implemented tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ]* 16.4 Write integration tests for end-to-end workflows
  - Create tests/integration/ directory
  - Test complete workflow: create library → import CSV → generate estimate
  - Test BRD parsing → feature extraction → estimation output
  - Test CLI end-to-end: run commands via CliRunner, verify outputs
  - Test data quality workflow: import → detect duplicates/anomalies → fix
  - Test reporting workflow: import data → generate reports → export
  - Test template workflow: apply template → customize → export
  - Test scenario workflow: create → what-if → compare
  - _Requirements: All_

- [ ] 16.5 Final Checkpoint - Ensure all tests pass
  - Run full test suite: `pytest tests/ -v --cov=src`
  - Verify test coverage is adequate (aim for >80%)
  - Ensure all tests pass, ask the user if questions arise.
