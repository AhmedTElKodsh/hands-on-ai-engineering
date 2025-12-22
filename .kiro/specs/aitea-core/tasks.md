# Implementation Plan: AITEA Core

## 1. Project Setup

- [x] 1.1 Initialize Python package structure
  - Create pyproject.toml with package metadata (name: aitea-core)
  - Create src/aitea_core/ directory structure
  - Create src/aitea_core/**init**.py with version
  - Create src/aitea_core/models/, services/, utils/ directories
  - Add **init**.py files to all packages
  - Create requirements.txt with dependencies (numpy, pandas, pydantic)
  - Create pytest.ini with Hypothesis settings
  - Create tests/ directory structure mirroring src/
  - _Requirements: All_

## 2. Data Models

- [ ] 2.1 Create enum definitions

  - Create src/models/enums.py
  - Implement Team, Process, Priority, Basis, Confidence, EstimationStyle, TimeUnit, ExperienceLevel enums
  - Use string values for all enum members (e.g., FRONTEND = "frontend")
  - _Requirements: 1.1-1.5_

- [ ] 2.2 Create error types

  - Create src/models/errors.py
  - Implement ValidationError exception with field, message, and value attributes
  - Implement Result[T, E] generic type with value, error, is_ok property, and ok/err class methods
  - _Requirements: All_

- [ ] 2.3 Create feature models

  - Create src/models/feature.py
  - Implement SeedTimeHistoryEntry dataclass (previous_value, new_value, changed_at)
  - Implement Feature dataclass with all required fields including seed_time_history
  - Implement FeatureLibrary dataclass
  - Use field(default_factory=list) for list fields and field(default_factory=datetime.now) for timestamps
  - _Requirements: 1.1_

- [ ] 2.4 Create tracking models

  - Create src/models/tracking.py
  - Implement TrackedTimeEntry dataclass with team, member_name, feature, tracked_time_hours, and optional fields
  - Implement ImportError dataclass (row_number, field, message, raw_value)
  - Implement ImportResult dataclass (total_rows, successful_imports, failed_imports, errors)
  - _Requirements: 1.2_

- [ ] 2.5 Create estimation models

  - Create src/models/estimation.py
  - Implement OutlierFlag dataclass (entry_id, value, threshold)
  - Implement RobustStatistics dataclass (mean_hours, median_hours, p80_hours, std_dev)
  - Implement FeatureStatistics dataclass with all statistical fields
  - Implement EstimateLineItem dataclass
  - Implement OverlapWarning dataclass (features, suggestion)
  - Implement ProjectEstimate dataclass with breakdown and totals
  - _Requirements: 1.3, 1.4_

- [ ] 2.6 Create configuration models

  - Create src/models/config.py
  - Implement ExperienceMultipliers dataclass with defaults (junior=1.5, mid=1.0, senior=0.8)
  - Implement TimeConversion dataclass with defaults (minutes_per_hour=60, hours_per_day=8)
  - Implement EstimationConfig dataclass with all configuration fields
  - Use field(default_factory=...) for nested dataclass defaults
  - _Requirements: 1.5_

- [ ] 2.7 Create models package exports
  - Update src/models/**init**.py to export all models and enums
  - Ensure all classes are in **all** list for clean imports
  - _Requirements: All_

## 3. Utility Functions

- [ ] 3.1 Implement statistics utilities

  - Create src/utils/statistics.py
  - Implement compute_mean using numpy.mean
  - Implement compute_median using numpy.median
  - Implement compute_p80 using numpy.percentile(values, 80)
  - Implement compute_p20 using numpy.percentile(values, 20)
  - Implement compute_std_dev using numpy.std
  - Handle edge cases: return 0.0 for empty arrays, handle single values
  - _Requirements: 6.1, 4.1_

- [ ]\* 3.2 Write property test for statistics computation

  - **Property 8: Statistics computation correctness**
  - **Validates: Requirements 4.1**

- [ ] 3.3 Implement normalization utilities

  - Create src/utils/normalization.py
  - Implement normalize_feature_name (strip whitespace, convert to lowercase)
  - Implement match_feature_with_synonyms (search by name and synonyms, case-insensitive)
  - _Requirements: 6.1_

- [ ]\* 3.4 Write property test for feature name normalization

  - **Property 14: Feature name normalization**
  - **Validates: Requirements 6.1**

- [ ] 3.5 Implement outlier detection

  - Create src/utils/outlier_detection.py
  - Implement detect_outliers (return indices where value > 3 \* median)
  - Implement compute_robust_statistics (compute stats excluding outliers)
  - _Requirements: 6.2_

- [ ]\* 3.6 Write property test for outlier detection

  - **Property 15: Outlier detection threshold**
  - **Validates: Requirements 6.2**

- [ ] 3.7 Implement time conversion

  - Create src/utils/time_conversion.py
  - Implement convert_to_hours supporting TimeUnit.HOURS, MINUTES, DAYS
  - Use configurable conversion factors from TimeConversion config
  - _Requirements: 6.3_

- [ ]\* 3.8 Write property test for time conversion round-trip

  - **Property 16: Time conversion round-trip**
  - **Validates: Requirements 6.3**

- [ ] 3.9 Implement confidence assignment

  - Create src/utils/confidence.py
  - Implement assign_confidence logic:
    - HIGH: count >= 5 and coefficient of variation < 0.2
    - MEDIUM: 2 <= count <= 4
    - LOW: seed-based or count == 1
  - _Requirements: 4.3_

- [ ]\* 3.10 Write property test for confidence assignment

  - **Property 9: Confidence assignment based on data quality**
  - **Validates: Requirements 4.3**

- [ ] 3.11 Create utils package exports
  - Update src/utils/**init**.py to export all utility functions
  - _Requirements: All_

## 4. Feature Library Service

- [ ] 4.1 Implement Feature Library Service

  - Create src/services/feature_library.py
  - Implement IFeatureLibraryService abstract base class with all required methods
  - Implement FeatureLibraryService with in-memory storage (dict or list)
  - Implement create_library() -> FeatureLibrary
  - Implement add_feature() with validation (check required fields: name, team, process, seed_time_hours)
  - Return Result[Feature, ValidationError] for add_feature
  - Implement update_feature() with seed_time_history preservation
  - Implement delete_feature() -> Result[None, Exception]
  - Implement search_features() using case-insensitive matching on names and synonyms
  - Implement get_feature_by_name_or_synonym() using normalization utility
  - Implement list_features() returning features grouped by process and sorted alphabetically
  - Implement list_processes() -> List[Process]
  - Implement get_features_by_process(process: Process) -> List[Feature]
  - _Requirements: 2.1-2.4_

- [ ]\* 4.2 Write property test for feature validation

  - **Property 1: Feature validation rejects incomplete inputs**
  - **Validates: Requirements 2.1**

- [ ]\* 4.3 Write property test for feature search

  - **Property 2: Feature search is case-insensitive and synonym-aware**
  - **Validates: Requirements 2.2**

- [ ]\* 4.4 Write property test for seed time history preservation

  - **Property 3: Seed time history preservation**
  - **Validates: Requirements 2.3**

- [ ]\* 4.5 Write property test for feature listing
  - **Property 4: Feature listing is grouped and sorted**
  - **Validates: Requirements 2.4**

## 5. Time Tracking Service

- [ ] 5.1 Implement Time Tracking Service

  - Create src/services/time_tracking.py
  - Implement ITimeTrackingService abstract base class with all required methods
  - Implement TimeTrackingService with in-memory storage (list of TrackedTimeEntry)
  - Implement validate_schema(headers: List[str]) -> bool
    - Check for required columns: team, member_name, feature, tracked_time_hours
    - Return False if any required column is missing
  - Implement import_csv(file_path: str) -> ImportResult
    - Use pandas to read CSV file
    - Validate schema first
    - Process optional columns: process, category, date
    - Convert time values to hours using time_conversion utility
    - Collect errors for invalid rows but continue processing
    - Return ImportResult with counts and error details
  - Implement get_entries_by_feature(feature_name: str) -> List[TrackedTimeEntry]
  - Implement get_all_entries() -> List[TrackedTimeEntry]
  - Implement add_entry(entry: TrackedTimeEntry) -> Result[TrackedTimeEntry, Exception]
  - _Requirements: 3.1-3.4_

- [ ]\* 5.2 Write property test for CSV schema validation

  - **Property 5: CSV schema validation detects missing columns**
  - **Validates: Requirements 3.1**

- [ ]\* 5.3 Write property test for CSV optional columns

  - **Property 6: CSV import processes optional columns**
  - **Validates: Requirements 3.2**

- [ ]\* 5.4 Write property test for import error handling
  - **Property 7: Import error handling continues processing**
  - **Validates: Requirements 3.3, 3.4**

## 6. Estimation Service

- [ ] 6.1 Implement Estimation Service

  - Create src/services/estimation.py
  - Implement IEstimationService abstract base class with all required methods
  - Implement EstimationService (depends on FeatureLibraryService, TimeTrackingService, ConfigurationService)
  - Implement compute_statistics(feature_name: str) -> FeatureStatistics
    - Get tracked entries for feature from TimeTrackingService
    - If entries exist: compute mean, median, P80, std_dev using statistics utilities
    - If no entries: use seed time from FeatureLibrary, mark data_coverage as "seed"
    - Detect outliers using outlier_detection utility
    - Compute robust statistics if outliers exist
    - Assign confidence using confidence utility
  - Implement compute_estimation_table() -> List[FeatureStatistics]
    - Compute statistics for all features in library
  - Implement generate_estimate(features: List[str]) -> ProjectEstimate
    - Get statistics for each feature
    - Apply configured estimation style (mean/median/P80) to select hours
    - Create EstimateLineItem for each feature with basis and confidence
    - Calculate frontend_total_hours, backend_total_hours, grand_total_hours
    - Apply buffer_percentage if configured
  - Implement detect_overlaps(features: List[str]) -> List[OverlapWarning]
    - Check for potentially duplicate features
  - Implement apply_experience_multiplier(hours: float, level: ExperienceLevel) -> float
    - Apply multiplier from configuration (junior=1.5x, mid=1.0x, senior=0.8x)
  - _Requirements: 4.1-4.4_

- [ ]\* 6.2 Write property test for estimation style selection

  - **Property 10: Estimation style selection**
  - **Validates: Requirements 4.4**

- [ ]\* 6.3 Write unit test for seed fallback
  - Test that features with zero tracked entries use seed time and mark basis as "seed"
  - _Requirements: 4.2_

## 7. Configuration Service

- [ ] 7.1 Implement Configuration Service

  - Create src/services/configuration.py
  - Implement IConfigurationService abstract base class with all required methods
  - Implement ConfigurationService with in-memory EstimationConfig
  - Implement get_config() -> EstimationConfig
  - Implement set_estimation_style(style: EstimationStyle) -> None
    - Validate that style is one of: MEAN, MEDIAN, P80
    - Update config and trigger callbacks
  - Implement set_working_hours_per_day(hours: int) -> None
  - Implement set_experience_multipliers(multipliers: ExperienceMultipliers) -> None
    - Store multipliers (junior=1.5, mid=1.0, senior=0.8)
  - Implement set_buffer_percentage(percentage: float) -> None
  - Implement on_config_change(callback: Callable[[EstimationConfig], None]) -> None
    - Register callback function
    - Invoke all registered callbacks when any config changes
  - _Requirements: 5.1-5.3_

- [ ]\* 7.2 Write property test for configuration validation

  - **Property 11: Configuration validation**
  - **Validates: Requirements 5.1**

- [ ]\* 7.3 Write property test for experience multipliers

  - **Property 12: Experience multiplier application**
  - **Validates: Requirements 5.2**

- [ ]\* 7.4 Write property test for configuration change notifications
  - **Property 13: Configuration change notifications**
  - **Validates: Requirements 5.3**

## 8. Package Finalization

- [ ] 8.1 Create services package exports

  - Update src/services/**init**.py to export all service interfaces and implementations
  - Export: IFeatureLibraryService, FeatureLibraryService, ITimeTrackingService, TimeTrackingService, IEstimationService, EstimationService, IConfigurationService, ConfigurationService
  - _Requirements: All_

- [ ] 8.2 Create main package exports

  - Update src/**init**.py to export key models, services, and utilities
  - Make it easy to import: `from src import Feature, Team, FeatureLibraryService`
  - _Requirements: All_

- [ ] 8.3 Checkpoint - Ensure all tests pass
  - Run pytest to verify all implemented tests pass
  - Ask user if any questions arise
  - _Requirements: All_
