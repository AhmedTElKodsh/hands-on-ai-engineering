"""
Property-based tests for AITEA models.
"""
from datetime import date
from hypothesis import given, strategies as st, assume
import pytest

from src.models.enums import TeamType, ProcessType, ConfidenceLevel
from src.models.dataclasses import (
    Feature,
    TrackedTimeEntry,
    ProjectEstimate,
    EstimationConfig,
    FeatureEstimate,
    FeatureStatistics,
)
from src.models.result import Result, UnwrapError
from src.models.errors import ValidationError, NotFoundError, ImportError, EstimationError


class TestEnumProperties:
    """Property tests for enum completeness and type safety."""

    def test_enum_completeness_and_type_safety(self) -> None:
        """
        **Feature: curriculum, Property 1: Enum Completeness and Type Safety**
        **Validates: Requirements 1.2**
        
        For any TeamType, ProcessType, or ConfidenceLevel enum, all defined members
        SHALL be accessible by name and value, and mypy SHALL report no type errors
        when using these enums.
        """
        # Test TeamType enum
        team_members = ["BACKEND", "FRONTEND", "FULLSTACK", "DESIGN", "QA", "DEVOPS"]
        team_values = ["backend", "frontend", "fullstack", "design", "qa", "devops"]
        
        # Verify all members are accessible by name
        for member_name in team_members:
            assert hasattr(TeamType, member_name), f"TeamType missing member: {member_name}"
            member = getattr(TeamType, member_name)
            assert isinstance(member, TeamType), f"TeamType.{member_name} is not a TeamType instance"
        
        # Verify all members are accessible by value
        for value in team_values:
            member = TeamType(value)
            assert member.value == value, f"TeamType value mismatch for {value}"
        
        # Verify count matches expected
        assert len(TeamType) == len(team_members), f"TeamType has unexpected member count"
        
        # Test ProcessType enum
        process_members = ["DATA_OPERATIONS", "CONTENT_MANAGEMENT", "REAL_TIME", "AUTHENTICATION", "INTEGRATION"]
        process_values = ["Data Operations", "Content Management", "Real-time", "Authentication", "Integration"]
        
        # Verify all members are accessible by name
        for member_name in process_members:
            assert hasattr(ProcessType, member_name), f"ProcessType missing member: {member_name}"
            member = getattr(ProcessType, member_name)
            assert isinstance(member, ProcessType), f"ProcessType.{member_name} is not a ProcessType instance"
        
        # Verify all members are accessible by value
        for value in process_values:
            member = ProcessType(value)
            assert member.value == value, f"ProcessType value mismatch for {value}"
        
        # Verify count matches expected
        assert len(ProcessType) == len(process_members), f"ProcessType has unexpected member count"
        
        # Test ConfidenceLevel enum
        confidence_members = ["LOW", "MEDIUM", "HIGH"]
        confidence_values = ["low", "medium", "high"]
        
        # Verify all members are accessible by name
        for member_name in confidence_members:
            assert hasattr(ConfidenceLevel, member_name), f"ConfidenceLevel missing member: {member_name}"
            member = getattr(ConfidenceLevel, member_name)
            assert isinstance(member, ConfidenceLevel), f"ConfidenceLevel.{member_name} is not a ConfidenceLevel instance"
        
        # Verify all members are accessible by value
        for value in confidence_values:
            member = ConfidenceLevel(value)
            assert member.value == value, f"ConfidenceLevel value mismatch for {value}"
        
        # Verify count matches expected
        assert len(ConfidenceLevel) == len(confidence_members), f"ConfidenceLevel has unexpected member count"

    @given(st.sampled_from(TeamType))
    def test_team_type_string_inheritance(self, team: TeamType) -> None:
        """
        **Feature: curriculum, Property 1: Enum Completeness and Type Safety**
        **Validates: Requirements 1.2**
        
        For any TeamType member, it SHALL be a string instance (str inheritance)
        for JSON serialization compatibility.
        """
        # Verify string inheritance
        assert isinstance(team.value, str), f"TeamType.{team.name} value is not a string"
        
        # Verify it can be used in string operations
        assert len(team.value) > 0, f"TeamType.{team.name} has empty value"
        
        # Verify JSON serialization compatibility
        assert team.value == str(team.value), f"TeamType.{team.name} value is not JSON serializable"

    @given(st.sampled_from(ProcessType))
    def test_process_type_string_inheritance(self, process: ProcessType) -> None:
        """
        **Feature: curriculum, Property 1: Enum Completeness and Type Safety**
        **Validates: Requirements 1.2**
        
        For any ProcessType member, it SHALL be a string instance (str inheritance)
        for JSON serialization compatibility.
        """
        # Verify string inheritance
        assert isinstance(process.value, str), f"ProcessType.{process.name} value is not a string"
        
        # Verify it can be used in string operations
        assert len(process.value) > 0, f"ProcessType.{process.name} has empty value"
        
        # Verify JSON serialization compatibility
        assert process.value == str(process.value), f"ProcessType.{process.name} value is not JSON serializable"

    @given(st.sampled_from(ConfidenceLevel))
    def test_confidence_level_string_inheritance(self, confidence: ConfidenceLevel) -> None:
        """
        **Feature: curriculum, Property 1: Enum Completeness and Type Safety**
        **Validates: Requirements 1.2**
        
        For any ConfidenceLevel member, it SHALL be a string instance (str inheritance)
        for JSON serialization compatibility.
        """
        # Verify string inheritance
        assert isinstance(confidence.value, str), f"ConfidenceLevel.{confidence.name} value is not a string"
        
        # Verify it can be used in string operations
        assert len(confidence.value) > 0, f"ConfidenceLevel.{confidence.name} has empty value"
        
        # Verify JSON serialization compatibility
        assert confidence.value == str(confidence.value), f"ConfidenceLevel.{confidence.name} value is not JSON serializable"

    def test_enum_uniqueness(self) -> None:
        """
        **Feature: curriculum, Property 1: Enum Completeness and Type Safety**
        **Validates: Requirements 1.2**
        
        For any enum, all member values SHALL be unique (no duplicates).
        """
        # Test TeamType uniqueness
        team_values = [member.value for member in TeamType]
        assert len(team_values) == len(set(team_values)), "TeamType has duplicate values"
        
        # Test ProcessType uniqueness
        process_values = [member.value for member in ProcessType]
        assert len(process_values) == len(set(process_values)), "ProcessType has duplicate values"
        
        # Test ConfidenceLevel uniqueness
        confidence_values = [member.value for member in ConfidenceLevel]
        assert len(confidence_values) == len(set(confidence_values)), "ConfidenceLevel has duplicate values"


# Hypothesis strategies for generating valid dataclass instances
valid_id_strategy = st.text(min_size=1, max_size=50).filter(lambda x: x.strip())
valid_name_strategy = st.text(min_size=1, max_size=100).filter(lambda x: x.strip())
positive_float_strategy = st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False)
non_negative_float_strategy = st.floats(min_value=0.0, max_value=10000.0, allow_nan=False, allow_infinity=False)
positive_int_strategy = st.integers(min_value=1, max_value=10000)
non_negative_int_strategy = st.integers(min_value=0, max_value=10000)
date_strategy = st.dates(min_value=date(2000, 1, 1), max_value=date(2100, 12, 31))


class TestDataclassInstantiationValidity:
    """
    Property tests for dataclass instantiation validity.
    
    **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
    **Validates: Requirements 1.3**
    """

    @given(
        id=valid_id_strategy,
        name=valid_name_strategy,
        team=st.sampled_from(TeamType),
        process=st.text(min_size=1, max_size=50),
        seed_time_hours=positive_float_strategy,
        synonyms=st.lists(st.text(max_size=30), max_size=5),
        notes=st.text(max_size=200),
    )
    def test_feature_instantiation_validity(
        self,
        id: str,
        name: str,
        team: TeamType,
        process: str,
        seed_time_hours: float,
        synonyms: list,
        notes: str,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for Feature, the dataclass
        SHALL instantiate without error and all fields SHALL be accessible
        with correct types.
        """
        # Instantiate Feature with valid values
        feature = Feature(
            id=id,
            name=name,
            team=team,
            process=process,
            seed_time_hours=seed_time_hours,
            synonyms=synonyms,
            notes=notes,
        )
        
        # Verify all fields are accessible with correct types
        assert feature.id == id
        assert feature.name == name
        assert feature.team == team
        assert isinstance(feature.team, TeamType)
        assert feature.process == process
        assert feature.seed_time_hours == seed_time_hours
        assert isinstance(feature.seed_time_hours, float)
        assert feature.synonyms == synonyms
        assert isinstance(feature.synonyms, list)
        assert feature.notes == notes

    @given(
        id=valid_id_strategy,
        team=st.sampled_from(TeamType),
        member_name=valid_name_strategy,
        feature=valid_name_strategy,
        tracked_time_hours=positive_float_strategy,
        process=st.text(min_size=1, max_size=50),
        entry_date=date_strategy,
    )
    def test_tracked_time_entry_instantiation_validity(
        self,
        id: str,
        team: TeamType,
        member_name: str,
        feature: str,
        tracked_time_hours: float,
        process: str,
        entry_date: date,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for TrackedTimeEntry, the dataclass
        SHALL instantiate without error and all fields SHALL be accessible
        with correct types.
        """
        # Instantiate TrackedTimeEntry with valid values
        entry = TrackedTimeEntry(
            id=id,
            team=team,
            member_name=member_name,
            feature=feature,
            tracked_time_hours=tracked_time_hours,
            process=process,
            date=entry_date,
        )
        
        # Verify all fields are accessible with correct types
        assert entry.id == id
        assert entry.team == team
        assert isinstance(entry.team, TeamType)
        assert entry.member_name == member_name
        assert entry.feature == feature
        assert entry.tracked_time_hours == tracked_time_hours
        assert isinstance(entry.tracked_time_hours, float)
        assert entry.process == process
        assert entry.date == entry_date
        assert isinstance(entry.date, date)

    @given(
        mean=non_negative_float_strategy,
        median=non_negative_float_strategy,
        std_dev=non_negative_float_strategy,
        p80=non_negative_float_strategy,
        data_point_count=non_negative_int_strategy,
    )
    def test_feature_statistics_instantiation_validity(
        self,
        mean: float,
        median: float,
        std_dev: float,
        p80: float,
        data_point_count: int,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for FeatureStatistics, the dataclass
        SHALL instantiate without error and all fields SHALL be accessible
        with correct types.
        """
        # Instantiate FeatureStatistics with valid values
        stats = FeatureStatistics(
            mean=mean,
            median=median,
            std_dev=std_dev,
            p80=p80,
            data_point_count=data_point_count,
        )
        
        # Verify all fields are accessible with correct types
        assert stats.mean == mean
        assert isinstance(stats.mean, float)
        assert stats.median == median
        assert isinstance(stats.median, float)
        assert stats.std_dev == std_dev
        assert isinstance(stats.std_dev, float)
        assert stats.p80 == p80
        assert isinstance(stats.p80, float)
        assert stats.data_point_count == data_point_count
        assert isinstance(stats.data_point_count, int)

    @given(
        feature_name=valid_name_strategy,
        estimated_hours=positive_float_strategy,
        confidence=st.sampled_from(ConfidenceLevel),
        used_seed_time=st.booleans(),
    )
    def test_feature_estimate_instantiation_validity(
        self,
        feature_name: str,
        estimated_hours: float,
        confidence: ConfidenceLevel,
        used_seed_time: bool,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for FeatureEstimate, the dataclass
        SHALL instantiate without error and all fields SHALL be accessible
        with correct types.
        """
        # Instantiate FeatureEstimate with valid values (without statistics)
        estimate = FeatureEstimate(
            feature_name=feature_name,
            estimated_hours=estimated_hours,
            confidence=confidence,
            statistics=None,
            used_seed_time=used_seed_time,
        )
        
        # Verify all fields are accessible with correct types
        assert estimate.feature_name == feature_name
        assert estimate.estimated_hours == estimated_hours
        assert isinstance(estimate.estimated_hours, float)
        assert estimate.confidence == confidence
        assert isinstance(estimate.confidence, ConfidenceLevel)
        assert estimate.statistics is None
        assert estimate.used_seed_time == used_seed_time
        assert isinstance(estimate.used_seed_time, bool)

    @given(
        feature_name=valid_name_strategy,
        estimated_hours=positive_float_strategy,
        confidence=st.sampled_from(ConfidenceLevel),
        mean=non_negative_float_strategy,
        median=non_negative_float_strategy,
        std_dev=non_negative_float_strategy,
        p80=non_negative_float_strategy,
        data_point_count=non_negative_int_strategy,
        used_seed_time=st.booleans(),
    )
    def test_feature_estimate_with_statistics_instantiation_validity(
        self,
        feature_name: str,
        estimated_hours: float,
        confidence: ConfidenceLevel,
        mean: float,
        median: float,
        std_dev: float,
        p80: float,
        data_point_count: int,
        used_seed_time: bool,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for FeatureEstimate with nested
        FeatureStatistics, the dataclass SHALL instantiate without error and all
        fields SHALL be accessible with correct types.
        """
        # Create nested FeatureStatistics
        stats = FeatureStatistics(
            mean=mean,
            median=median,
            std_dev=std_dev,
            p80=p80,
            data_point_count=data_point_count,
        )
        
        # Instantiate FeatureEstimate with statistics
        estimate = FeatureEstimate(
            feature_name=feature_name,
            estimated_hours=estimated_hours,
            confidence=confidence,
            statistics=stats,
            used_seed_time=used_seed_time,
        )
        
        # Verify all fields are accessible with correct types
        assert estimate.feature_name == feature_name
        assert estimate.estimated_hours == estimated_hours
        assert estimate.confidence == confidence
        assert estimate.statistics is not None
        assert isinstance(estimate.statistics, FeatureStatistics)
        assert estimate.statistics.mean == mean
        assert estimate.statistics.median == median
        assert estimate.statistics.std_dev == std_dev
        assert estimate.statistics.p80 == p80
        assert estimate.statistics.data_point_count == data_point_count
        assert estimate.used_seed_time == used_seed_time

    @given(
        feature_name=valid_name_strategy,
        estimated_hours=positive_float_strategy,
        confidence=st.sampled_from(ConfidenceLevel),
        total_hours=non_negative_float_strategy,
        project_confidence=st.sampled_from(ConfidenceLevel),
    )
    def test_project_estimate_instantiation_validity(
        self,
        feature_name: str,
        estimated_hours: float,
        confidence: ConfidenceLevel,
        total_hours: float,
        project_confidence: ConfidenceLevel,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for ProjectEstimate, the dataclass
        SHALL instantiate without error and all fields SHALL be accessible
        with correct types.
        """
        # Create a feature estimate for the project
        feature_estimate = FeatureEstimate(
            feature_name=feature_name,
            estimated_hours=estimated_hours,
            confidence=confidence,
        )
        
        # Instantiate ProjectEstimate with valid values
        project = ProjectEstimate(
            features=[feature_estimate],
            total_hours=total_hours,
            confidence=project_confidence,
        )
        
        # Verify all fields are accessible with correct types
        assert len(project.features) == 1
        assert isinstance(project.features, list)
        assert project.features[0] == feature_estimate
        assert isinstance(project.features[0], FeatureEstimate)
        assert project.total_hours == total_hours
        assert isinstance(project.total_hours, float)
        assert project.confidence == project_confidence
        assert isinstance(project.confidence, ConfidenceLevel)

    @given(
        use_outlier_detection=st.booleans(),
        outlier_threshold_std=st.floats(min_value=0.01, max_value=10.0, allow_nan=False, allow_infinity=False),
        min_data_points_for_stats=positive_int_strategy,
    )
    def test_estimation_config_instantiation_validity(
        self,
        use_outlier_detection: bool,
        outlier_threshold_std: float,
        min_data_points_for_stats: int,
    ) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        For any valid combination of field values for EstimationConfig, the dataclass
        SHALL instantiate without error and all fields SHALL be accessible
        with correct types.
        """
        # Instantiate EstimationConfig with valid values
        config = EstimationConfig(
            use_outlier_detection=use_outlier_detection,
            outlier_threshold_std=outlier_threshold_std,
            min_data_points_for_stats=min_data_points_for_stats,
        )
        
        # Verify all fields are accessible with correct types
        assert config.use_outlier_detection == use_outlier_detection
        assert isinstance(config.use_outlier_detection, bool)
        assert config.outlier_threshold_std == outlier_threshold_std
        assert isinstance(config.outlier_threshold_std, float)
        assert config.min_data_points_for_stats == min_data_points_for_stats
        assert isinstance(config.min_data_points_for_stats, int)

    def test_estimation_config_default_values(self) -> None:
        """
        **Feature: curriculum, Property 2: Dataclass Instantiation Validity**
        **Validates: Requirements 1.3**
        
        EstimationConfig SHALL instantiate with sensible default values when
        no arguments are provided.
        """
        # Instantiate with defaults
        config = EstimationConfig()
        
        # Verify default values
        assert config.use_outlier_detection is True
        assert config.outlier_threshold_std == 2.0
        assert config.min_data_points_for_stats == 3


# Strategies for generating error types
validation_error_strategy = st.builds(
    ValidationError,
    field=st.text(min_size=1, max_size=30).filter(lambda x: x.strip()),
    message=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
    value=st.one_of(st.none(), st.integers(), st.text(max_size=50), st.floats(allow_nan=False)),
)

not_found_error_strategy = st.builds(
    NotFoundError,
    resource_type=st.sampled_from(["Feature", "TrackedTimeEntry", "User", "Project"]),
    identifier=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    message=st.one_of(st.none(), st.text(max_size=100)),
)

estimation_error_strategy = st.builds(
    EstimationError,
    feature_name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
    reason=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
    details=st.one_of(st.none(), st.text(max_size=50)),
)

# Strategy for any error type
any_error_strategy = st.one_of(
    validation_error_strategy,
    not_found_error_strategy,
    estimation_error_strategy,
)

# Strategy for success values
any_value_strategy = st.one_of(
    st.integers(),
    st.text(max_size=50),
    st.floats(allow_nan=False, allow_infinity=False),
    st.booleans(),
    st.lists(st.integers(), max_size=5),
)


class TestResultPatternConsistency:
    """
    Property tests for Result pattern consistency.
    
    **Feature: curriculum, Property 3: Service Result Pattern Consistency**
    **Validates: Requirements 1.5, 1.8**
    """

    @given(value=any_value_strategy)
    def test_ok_result_is_ok(self, value) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any value wrapped in Result.ok(), is_ok() SHALL return True
        and is_err() SHALL return False.
        """
        result = Result.ok(value)
        
        assert result.is_ok() is True, "Result.ok() should return is_ok() == True"
        assert result.is_err() is False, "Result.ok() should return is_err() == False"

    @given(error=any_error_strategy)
    def test_err_result_is_err(self, error) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any error wrapped in Result.err(), is_err() SHALL return True
        and is_ok() SHALL return False.
        """
        result = Result.err(error)
        
        assert result.is_err() is True, "Result.err() should return is_err() == True"
        assert result.is_ok() is False, "Result.err() should return is_ok() == False"

    @given(value=any_value_strategy)
    def test_ok_result_unwrap_returns_value(self, value) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.ok(value), unwrap() SHALL return the original value.
        """
        result = Result.ok(value)
        
        unwrapped = result.unwrap()
        assert unwrapped == value, "unwrap() should return the original value"

    @given(error=any_error_strategy)
    def test_err_result_unwrap_err_returns_error(self, error) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.err(error), unwrap_err() SHALL return the original error.
        """
        result = Result.err(error)
        
        unwrapped_error = result.unwrap_err()
        assert unwrapped_error == error, "unwrap_err() should return the original error"

    @given(error=any_error_strategy)
    def test_err_result_unwrap_raises(self, error) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.err(error), calling unwrap() SHALL raise UnwrapError.
        """
        result = Result.err(error)
        
        with pytest.raises(UnwrapError):
            result.unwrap()

    @given(value=any_value_strategy)
    def test_ok_result_unwrap_err_raises(self, value) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.ok(value), calling unwrap_err() SHALL raise UnwrapError.
        """
        result = Result.ok(value)
        
        with pytest.raises(UnwrapError):
            result.unwrap_err()

    @given(value=any_value_strategy)
    def test_is_ok_and_is_err_mutually_exclusive(self, value) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result, is_ok() and is_err() SHALL be mutually exclusive
        (exactly one is True).
        """
        ok_result = Result.ok(value)
        
        # XOR: exactly one should be True
        assert ok_result.is_ok() != ok_result.is_err(), \
            "is_ok() and is_err() must be mutually exclusive"

    @given(error=any_error_strategy)
    def test_is_ok_and_is_err_mutually_exclusive_for_err(self, error) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.err(), is_ok() and is_err() SHALL be mutually exclusive
        (exactly one is True).
        """
        err_result = Result.err(error)
        
        # XOR: exactly one should be True
        assert err_result.is_ok() != err_result.is_err(), \
            "is_ok() and is_err() must be mutually exclusive"

    @given(value=any_value_strategy, default=any_value_strategy)
    def test_ok_result_unwrap_or_returns_value(self, value, default) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.ok(value), unwrap_or(default) SHALL return the original value,
        not the default.
        """
        result = Result.ok(value)
        
        unwrapped = result.unwrap_or(default)
        assert unwrapped == value, "unwrap_or() should return the value for Ok results"

    @given(error=any_error_strategy, default=any_value_strategy)
    def test_err_result_unwrap_or_returns_default(self, error, default) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.err(error), unwrap_or(default) SHALL return the default value.
        """
        result = Result.err(error)
        
        unwrapped = result.unwrap_or(default)
        assert unwrapped == default, "unwrap_or() should return the default for Err results"

    @given(value=st.integers())
    def test_ok_result_map_transforms_value(self, value: int) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.ok(value), map(f) SHALL return Result.ok(f(value)).
        """
        result = Result.ok(value)
        
        mapped = result.map(lambda x: x * 2)
        
        assert mapped.is_ok(), "map() on Ok should return Ok"
        assert mapped.unwrap() == value * 2, "map() should transform the value"

    @given(error=validation_error_strategy)
    def test_err_result_map_preserves_error(self, error: ValidationError) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For any Result.err(error), map(f) SHALL return the original error unchanged.
        """
        result: Result[int, ValidationError] = Result.err(error)
        
        mapped = result.map(lambda x: x * 2)
        
        assert mapped.is_err(), "map() on Err should return Err"
        assert mapped.unwrap_err() == error, "map() should preserve the error"

    @given(value=any_value_strategy)
    def test_result_equality_for_ok(self, value) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        Two Result.ok() with the same value SHALL be equal.
        """
        result1 = Result.ok(value)
        result2 = Result.ok(value)
        
        assert result1 == result2, "Two Ok results with same value should be equal"

    @given(error=validation_error_strategy)
    def test_result_equality_for_err(self, error: ValidationError) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        Two Result.err() with the same error SHALL be equal.
        """
        result1 = Result.err(error)
        result2 = Result.err(error)
        
        assert result1 == result2, "Two Err results with same error should be equal"

    @given(value=any_value_strategy, error=any_error_strategy)
    def test_ok_and_err_not_equal(self, value, error) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        Result.ok(value) and Result.err(error) SHALL never be equal.
        """
        ok_result = Result.ok(value)
        err_result = Result.err(error)
        
        assert ok_result != err_result, "Ok and Err results should never be equal"

    @given(value=st.integers())
    def test_and_then_chains_on_ok(self, value: int) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For Result.ok(value), and_then(f) SHALL call f with the value and return its result.
        """
        result = Result.ok(value)
        
        chained = result.and_then(lambda x: Result.ok(x * 2))
        
        assert chained.is_ok(), "and_then() on Ok should propagate Ok"
        assert chained.unwrap() == value * 2, "and_then() should chain the operation"

    @given(error=validation_error_strategy)
    def test_and_then_short_circuits_on_err(self, error: ValidationError) -> None:
        """
        **Feature: curriculum, Property 3: Service Result Pattern Consistency**
        **Validates: Requirements 1.5, 1.8**
        
        For Result.err(error), and_then(f) SHALL return the original error without calling f.
        """
        result: Result[int, ValidationError] = Result.err(error)
        called = [False]
        
        def should_not_be_called(x: int) -> Result[int, ValidationError]:
            called[0] = True
            return Result.ok(x * 2)
        
        chained = result.and_then(should_not_be_called)
        
        assert chained.is_err(), "and_then() on Err should return Err"
        assert chained.unwrap_err() == error, "and_then() should preserve the error"
        assert not called[0], "and_then() should not call f on Err"


# Import statistics utility functions
from src.utils import calculate_mean, calculate_median, calculate_std_dev, calculate_p80


class TestStatisticsMathematicalCorrectness:
    """
    Property tests for statistics mathematical correctness.
    
    **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
    **Validates: Requirements 1.6, 9.1**
    """

    # Strategy for generating non-empty lists of positive floats
    non_empty_float_list_strategy = st.lists(
        st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=100,
    )

    @given(values=non_empty_float_list_strategy)
    def test_mean_equals_sum_divided_by_count(self, values: list) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For any non-empty list of tracked time entries, mean SHALL equal
        sum of values divided by count.
        """
        calculated_mean = calculate_mean(values)
        expected_mean = sum(values) / len(values)
        
        # Use approximate equality due to floating point precision
        assert abs(calculated_mean - expected_mean) < 1e-9, \
            f"Mean {calculated_mean} should equal sum/count {expected_mean}"

    @given(values=non_empty_float_list_strategy)
    def test_median_is_middle_value(self, values: list) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For any non-empty list of tracked time entries, median SHALL equal
        the middle value (or average of two middle values for even-length lists).
        """
        calculated_median = calculate_median(values)
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        
        if n % 2 == 0:
            expected_median = (sorted_values[mid - 1] + sorted_values[mid]) / 2
        else:
            expected_median = sorted_values[mid]
        
        # Use approximate equality due to floating point precision
        assert abs(calculated_median - expected_median) < 1e-9, \
            f"Median {calculated_median} should equal middle value {expected_median}"

    @given(values=non_empty_float_list_strategy)
    def test_p80_greater_than_or_equal_to_median(self, values: list) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For any non-empty list of tracked time entries, P80 SHALL be
        greater than or equal to median.
        """
        calculated_p80 = calculate_p80(values)
        calculated_median = calculate_median(values)
        
        # P80 (80th percentile) should always be >= median (50th percentile)
        assert calculated_p80 >= calculated_median - 1e-9, \
            f"P80 {calculated_p80} should be >= median {calculated_median}"

    @given(values=non_empty_float_list_strategy)
    def test_std_dev_is_non_negative(self, values: list) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For any non-empty list of tracked time entries, standard deviation
        SHALL be non-negative.
        """
        calculated_std_dev = calculate_std_dev(values)
        
        assert calculated_std_dev >= 0, \
            f"Standard deviation {calculated_std_dev} should be non-negative"

    @given(values=non_empty_float_list_strategy)
    def test_std_dev_mathematical_correctness(self, values: list) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For any non-empty list of tracked time entries, standard deviation
        SHALL equal the square root of the variance (population std dev).
        """
        calculated_std_dev = calculate_std_dev(values)
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        expected_std_dev = variance ** 0.5
        
        # Use approximate equality due to floating point precision
        assert abs(calculated_std_dev - expected_std_dev) < 1e-9, \
            f"Std dev {calculated_std_dev} should equal sqrt(variance) {expected_std_dev}"

    @given(value=st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False))
    def test_single_value_statistics(self, value: float) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For a single-value list, mean, median, and P80 SHALL all equal that value,
        and standard deviation SHALL be zero.
        """
        values = [value]
        
        assert abs(calculate_mean(values) - value) < 1e-9, \
            "Mean of single value should equal that value"
        assert abs(calculate_median(values) - value) < 1e-9, \
            "Median of single value should equal that value"
        assert abs(calculate_p80(values) - value) < 1e-9, \
            "P80 of single value should equal that value"
        assert abs(calculate_std_dev(values)) < 1e-9, \
            "Std dev of single value should be zero"

    @given(
        value=st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False),
        count=st.integers(min_value=2, max_value=50),
    )
    def test_identical_values_statistics(self, value: float, count: int) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For a list of identical values, mean, median, and P80 SHALL all equal
        that value, and standard deviation SHALL be zero.
        """
        values = [value] * count
        
        assert abs(calculate_mean(values) - value) < 1e-9, \
            "Mean of identical values should equal that value"
        assert abs(calculate_median(values) - value) < 1e-9, \
            "Median of identical values should equal that value"
        assert abs(calculate_p80(values) - value) < 1e-9, \
            "P80 of identical values should equal that value"
        assert abs(calculate_std_dev(values)) < 1e-9, \
            "Std dev of identical values should be zero"

    def test_empty_list_raises_error(self) -> None:
        """
        **Feature: curriculum, Property 4: Statistics Mathematical Correctness**
        **Validates: Requirements 1.6, 9.1**
        
        For an empty list, all statistics functions SHALL raise ValueError.
        """
        with pytest.raises(ValueError):
            calculate_mean([])
        
        with pytest.raises(ValueError):
            calculate_median([])
        
        with pytest.raises(ValueError):
            calculate_std_dev([])
        
        with pytest.raises(ValueError):
            calculate_p80([])


# Import outlier detection function
from src.utils import detect_outliers


class TestOutlierDetectionAccuracy:
    """
    Property tests for outlier detection accuracy.
    
    **Feature: curriculum, Property 19: Outlier Detection Accuracy**
    **Validates: Requirements 9.3**
    """

    def test_outliers_exceeding_2_std_are_flagged(self) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For any set of tracked time entries, entries with values exceeding
        2 standard deviations from the mean SHALL be flagged as outliers.
        """
        # Create a list with a clear outlier
        # Values: 10, 10, 10, 10, 10, 100 (100 is clearly an outlier)
        values = [10.0, 10.0, 10.0, 10.0, 10.0, 100.0]
        
        # Calculate mean and std_dev of the full list
        mean = calculate_mean(values)  # (50 + 100) / 6 = 25
        std_dev = calculate_std_dev(values)
        
        # Verify 100.0 exceeds 2 std devs from mean
        distance = abs(100.0 - mean)
        assert distance > 2.0 * std_dev, \
            f"Test setup error: 100.0 should exceed 2 std devs from mean {mean}"
        
        # Detect outliers with default threshold of 2.0
        outliers = detect_outliers(values, threshold_std=2.0)
        
        # The outlier (100.0 at index 5) should be detected
        outlier_indices = [idx for idx, _ in outliers]
        outlier_values = [val for _, val in outliers]
        
        # Verify the outlier is flagged
        assert 5 in outlier_indices, \
            f"Outlier at index 5 should be flagged, but got indices {outlier_indices}"
        assert 100.0 in outlier_values, \
            f"Outlier value 100.0 should be in detected outliers {outlier_values}"

    @given(
        base_value=st.floats(min_value=10.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        count=st.integers(min_value=10, max_value=50),
    )
    def test_extreme_outliers_are_flagged(
        self, base_value: float, count: int
    ) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For any set of tracked time entries with an extreme outlier (10x the base value),
        that outlier SHALL be flagged.
        """
        # Create a list of similar values
        values = [base_value] * count
        
        # Add an extreme outlier (10x the base value)
        extreme_outlier = base_value * 10.0
        values_with_outlier = values + [extreme_outlier]
        
        # Calculate mean and std_dev of the full list
        mean = calculate_mean(values_with_outlier)
        std_dev = calculate_std_dev(values_with_outlier)
        
        # Verify the extreme outlier exceeds 2 std devs
        distance = abs(extreme_outlier - mean)
        
        # Only test if the outlier actually exceeds 2 std devs
        if std_dev > 0 and distance > 2.0 * std_dev:
            outliers = detect_outliers(values_with_outlier, threshold_std=2.0)
            outlier_indices = [idx for idx, _ in outliers]
            
            # The extreme outlier should be detected
            assert len(values_with_outlier) - 1 in outlier_indices, \
                f"Extreme outlier at index {len(values_with_outlier) - 1} should be flagged"

    @given(
        values=st.lists(
            st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
            min_size=3,
            max_size=50,
        )
    )
    def test_values_within_2_std_not_flagged(self, values: list) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For any set of tracked time entries, entries with values within
        2 standard deviations from the mean SHALL NOT be flagged as outliers.
        """
        mean = calculate_mean(values)
        std_dev = calculate_std_dev(values)
        
        # Detect outliers
        outliers = detect_outliers(values, threshold_std=2.0)
        outlier_indices = set(idx for idx, _ in outliers)
        
        # Verify that values within 2 std devs are not flagged
        for idx, value in enumerate(values):
            if std_dev > 0:
                distance_from_mean = abs(value - mean)
                within_threshold = distance_from_mean <= 2.0 * std_dev
                
                if within_threshold:
                    assert idx not in outlier_indices, \
                        f"Value {value} at index {idx} is within 2 std devs and should not be flagged"

    @given(
        values=st.lists(
            st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
            min_size=3,
            max_size=50,
        )
    )
    def test_outlier_detection_correctness(self, values: list) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For any set of tracked time entries, the detect_outliers function
        SHALL correctly identify all and only values exceeding 2 standard
        deviations from the mean.
        """
        mean = calculate_mean(values)
        std_dev = calculate_std_dev(values)
        
        # Detect outliers
        outliers = detect_outliers(values, threshold_std=2.0)
        detected_indices = set(idx for idx, _ in outliers)
        
        # Manually compute expected outliers
        expected_outliers = set()
        if std_dev > 0:
            for idx, value in enumerate(values):
                if abs(value - mean) > 2.0 * std_dev:
                    expected_outliers.add(idx)
        
        # Verify exact match
        assert detected_indices == expected_outliers, \
            f"Detected outliers {detected_indices} should match expected {expected_outliers}"

    @given(
        value=st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        count=st.integers(min_value=2, max_value=50),
    )
    def test_identical_values_no_outliers(self, value: float, count: int) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For a list of identical values (std dev = 0), no values SHALL be
        flagged as outliers.
        """
        values = [value] * count
        
        outliers = detect_outliers(values, threshold_std=2.0)
        
        assert len(outliers) == 0, \
            f"Identical values should have no outliers, but found {outliers}"

    def test_single_value_no_outliers(self) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For a single-value list, no outliers SHALL be detected.
        """
        outliers = detect_outliers([42.0], threshold_std=2.0)
        
        assert len(outliers) == 0, \
            "Single value should have no outliers"

    def test_empty_list_no_outliers(self) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For an empty list, no outliers SHALL be detected.
        """
        outliers = detect_outliers([], threshold_std=2.0)
        
        assert len(outliers) == 0, \
            "Empty list should have no outliers"

    @given(
        threshold=st.floats(min_value=0.5, max_value=5.0, allow_nan=False, allow_infinity=False)
    )
    def test_custom_threshold_respected(self, threshold: float) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For any custom threshold, the detect_outliers function SHALL use
        that threshold instead of the default 2.0.
        """
        # Create values with known distribution
        values = [10.0, 10.0, 10.0, 10.0, 10.0, 50.0]  # 50.0 is an outlier
        
        mean = calculate_mean(values)
        std_dev = calculate_std_dev(values)
        
        outliers = detect_outliers(values, threshold_std=threshold)
        detected_indices = set(idx for idx, _ in outliers)
        
        # Manually compute expected outliers with custom threshold
        expected_outliers = set()
        if std_dev > 0:
            for idx, value in enumerate(values):
                if abs(value - mean) > threshold * std_dev:
                    expected_outliers.add(idx)
        
        assert detected_indices == expected_outliers, \
            f"With threshold {threshold}, detected {detected_indices} should match expected {expected_outliers}"

    @given(
        values=st.lists(
            st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
            min_size=3,
            max_size=50,
        )
    )
    def test_outlier_returns_correct_index_value_pairs(self, values: list) -> None:
        """
        **Feature: curriculum, Property 19: Outlier Detection Accuracy**
        **Validates: Requirements 9.3**
        
        For any detected outlier, the returned tuple SHALL contain the
        correct index and the actual value at that index.
        """
        outliers = detect_outliers(values, threshold_std=2.0)
        
        for idx, value in outliers:
            assert 0 <= idx < len(values), \
                f"Outlier index {idx} should be within bounds [0, {len(values)})"
            assert values[idx] == value, \
                f"Outlier value {value} should match values[{idx}] = {values[idx]}"


# Import services for estimation testing
from src.services.implementations import (
    FeatureLibraryService,
    TimeTrackingService,
    EstimationService,
)


class TestLowDataPointFallback:
    """
    Property tests for low data point fallback behavior.
    
    **Feature: curriculum, Property 18: Low Data Point Fallback**
    **Validates: Requirements 9.2**
    """

    @given(
        feature_id=valid_id_strategy,
        feature_name=valid_name_strategy,
        team=st.sampled_from(TeamType),
        process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        seed_time_hours=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
    )
    def test_zero_data_points_uses_seed_time_with_low_confidence(
        self,
        feature_id: str,
        feature_name: str,
        team: TeamType,
        process: str,
        seed_time_hours: float,
    ) -> None:
        """
        **Feature: curriculum, Property 18: Low Data Point Fallback**
        **Validates: Requirements 9.2**
        
        For any feature with zero tracked time entries, the estimation SHALL
        use the seed time and return ConfidenceLevel.LOW.
        """
        # Set up services
        feature_library = FeatureLibraryService()
        time_tracking = TimeTrackingService()
        estimation_service = EstimationService(feature_library, time_tracking)
        
        # Create and add a feature
        feature = Feature(
            id=feature_id,
            name=feature_name,
            team=team,
            process=process,
            seed_time_hours=seed_time_hours,
        )
        feature_library.add_feature(feature)
        
        # Estimate the feature (no tracked time entries)
        result = estimation_service.estimate_feature(feature_name)
        
        # Verify the result
        assert result.is_ok(), f"Estimation should succeed, got error: {result.unwrap_err() if result.is_err() else 'N/A'}"
        estimate = result.unwrap()
        
        # Verify seed time is used
        assert estimate.used_seed_time is True, \
            "With 0 data points, used_seed_time should be True"
        assert abs(estimate.estimated_hours - seed_time_hours) < 1e-9, \
            f"With 0 data points, estimated_hours {estimate.estimated_hours} should equal seed_time {seed_time_hours}"
        
        # Verify confidence is LOW
        assert estimate.confidence == ConfidenceLevel.LOW, \
            f"With 0 data points, confidence should be LOW, got {estimate.confidence}"
        
        # Verify no statistics are provided
        assert estimate.statistics is None, \
            "With 0 data points, statistics should be None"

    @given(
        feature_id=valid_id_strategy,
        feature_name=valid_name_strategy,
        team=st.sampled_from(TeamType),
        process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        seed_time_hours=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
        tracked_time=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
        entry_date=date_strategy,
    )
    def test_one_data_point_uses_seed_time_with_low_confidence(
        self,
        feature_id: str,
        feature_name: str,
        team: TeamType,
        process: str,
        seed_time_hours: float,
        tracked_time: float,
        entry_date: date,
    ) -> None:
        """
        **Feature: curriculum, Property 18: Low Data Point Fallback**
        **Validates: Requirements 9.2**
        
        For any feature with exactly 1 tracked time entry, the estimation SHALL
        use the seed time and return ConfidenceLevel.LOW.
        """
        # Set up services
        feature_library = FeatureLibraryService()
        time_tracking = TimeTrackingService()
        estimation_service = EstimationService(feature_library, time_tracking)
        
        # Create and add a feature
        feature = Feature(
            id=feature_id,
            name=feature_name,
            team=team,
            process=process,
            seed_time_hours=seed_time_hours,
        )
        feature_library.add_feature(feature)
        
        # Add exactly 1 tracked time entry
        entry = TrackedTimeEntry(
            id="entry_1",
            team=team,
            member_name="Developer",
            feature=feature_name,
            tracked_time_hours=tracked_time,
            process=process,
            date=entry_date,
        )
        time_tracking.add_entry(entry)
        
        # Estimate the feature
        result = estimation_service.estimate_feature(feature_name)
        
        # Verify the result
        assert result.is_ok(), f"Estimation should succeed, got error: {result.unwrap_err() if result.is_err() else 'N/A'}"
        estimate = result.unwrap()
        
        # Verify seed time is used (fewer than 3 data points)
        assert estimate.used_seed_time is True, \
            "With 1 data point, used_seed_time should be True"
        assert abs(estimate.estimated_hours - seed_time_hours) < 1e-9, \
            f"With 1 data point, estimated_hours {estimate.estimated_hours} should equal seed_time {seed_time_hours}"
        
        # Verify confidence is LOW
        assert estimate.confidence == ConfidenceLevel.LOW, \
            f"With 1 data point, confidence should be LOW, got {estimate.confidence}"
        
        # Verify no statistics are provided
        assert estimate.statistics is None, \
            "With 1 data point, statistics should be None"

    @given(
        feature_id=valid_id_strategy,
        feature_name=valid_name_strategy,
        team=st.sampled_from(TeamType),
        process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        seed_time_hours=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
        tracked_times=st.lists(
            st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
            min_size=2,
            max_size=2,
        ),
        entry_date=date_strategy,
    )
    def test_two_data_points_uses_seed_time_with_low_confidence(
        self,
        feature_id: str,
        feature_name: str,
        team: TeamType,
        process: str,
        seed_time_hours: float,
        tracked_times: list,
        entry_date: date,
    ) -> None:
        """
        **Feature: curriculum, Property 18: Low Data Point Fallback**
        **Validates: Requirements 9.2**
        
        For any feature with exactly 2 tracked time entries, the estimation SHALL
        use the seed time and return ConfidenceLevel.LOW.
        """
        # Set up services
        feature_library = FeatureLibraryService()
        time_tracking = TimeTrackingService()
        estimation_service = EstimationService(feature_library, time_tracking)
        
        # Create and add a feature
        feature = Feature(
            id=feature_id,
            name=feature_name,
            team=team,
            process=process,
            seed_time_hours=seed_time_hours,
        )
        feature_library.add_feature(feature)
        
        # Add exactly 2 tracked time entries
        for i, tracked_time in enumerate(tracked_times):
            entry = TrackedTimeEntry(
                id=f"entry_{i}",
                team=team,
                member_name=f"Developer_{i}",
                feature=feature_name,
                tracked_time_hours=tracked_time,
                process=process,
                date=entry_date,
            )
            time_tracking.add_entry(entry)
        
        # Estimate the feature
        result = estimation_service.estimate_feature(feature_name)
        
        # Verify the result
        assert result.is_ok(), f"Estimation should succeed, got error: {result.unwrap_err() if result.is_err() else 'N/A'}"
        estimate = result.unwrap()
        
        # Verify seed time is used (fewer than 3 data points)
        assert estimate.used_seed_time is True, \
            "With 2 data points, used_seed_time should be True"
        assert abs(estimate.estimated_hours - seed_time_hours) < 1e-9, \
            f"With 2 data points, estimated_hours {estimate.estimated_hours} should equal seed_time {seed_time_hours}"
        
        # Verify confidence is LOW
        assert estimate.confidence == ConfidenceLevel.LOW, \
            f"With 2 data points, confidence should be LOW, got {estimate.confidence}"
        
        # Verify no statistics are provided
        assert estimate.statistics is None, \
            "With 2 data points, statistics should be None"

    @given(
        feature_id=valid_id_strategy,
        feature_name=valid_name_strategy,
        team=st.sampled_from(TeamType),
        process=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()),
        seed_time_hours=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
        tracked_times=st.lists(
            st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
            min_size=3,
            max_size=9,
        ),
        entry_date=date_strategy,
    )
    def test_three_or_more_data_points_uses_statistics_not_seed_time(
        self,
        feature_id: str,
        feature_name: str,
        team: TeamType,
        process: str,
        seed_time_hours: float,
        tracked_times: list,
        entry_date: date,
    ) -> None:
        """
        **Feature: curriculum, Property 18: Low Data Point Fallback**
        **Validates: Requirements 9.2**
        
        For any feature with 3 or more tracked time entries, the estimation SHALL
        use statistics (not seed time) and return ConfidenceLevel.MEDIUM or higher.
        """
        # Set up services
        feature_library = FeatureLibraryService()
        time_tracking = TimeTrackingService()
        estimation_service = EstimationService(feature_library, time_tracking)
        
        # Create and add a feature
        feature = Feature(
            id=feature_id,
            name=feature_name,
            team=team,
            process=process,
            seed_time_hours=seed_time_hours,
        )
        feature_library.add_feature(feature)
        
        # Add 3 or more tracked time entries
        for i, tracked_time in enumerate(tracked_times):
            entry = TrackedTimeEntry(
                id=f"entry_{i}",
                team=team,
                member_name=f"Developer_{i}",
                feature=feature_name,
                tracked_time_hours=tracked_time,
                process=process,
                date=entry_date,
            )
            time_tracking.add_entry(entry)
        
        # Estimate the feature
        result = estimation_service.estimate_feature(feature_name)
        
        # Verify the result
        assert result.is_ok(), f"Estimation should succeed, got error: {result.unwrap_err() if result.is_err() else 'N/A'}"
        estimate = result.unwrap()
        
        # Verify statistics are used (not seed time)
        assert estimate.used_seed_time is False, \
            f"With {len(tracked_times)} data points (>= 3), used_seed_time should be False"
        
        # Verify statistics are provided
        assert estimate.statistics is not None, \
            f"With {len(tracked_times)} data points (>= 3), statistics should be provided"
        
        # Verify confidence is MEDIUM or HIGH (not LOW)
        assert estimate.confidence in [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH], \
            f"With {len(tracked_times)} data points (>= 3), confidence should be MEDIUM or HIGH, got {estimate.confidence}"
        
        # Verify estimated hours equals P80 from statistics
        assert abs(estimate.estimated_hours - estimate.statistics.p80) < 1e-9, \
            f"With statistics, estimated_hours {estimate.estimated_hours} should equal P80 {estimate.statistics.p80}"

    @given(
        data_point_count=st.integers(min_value=0, max_value=2),
    )
    def test_fewer_than_3_data_points_always_low_confidence(
        self,
        data_point_count: int,
    ) -> None:
        """
        **Feature: curriculum, Property 18: Low Data Point Fallback**
        **Validates: Requirements 9.2**
        
        For any feature with fewer than 3 tracked time entries (0, 1, or 2),
        the estimation SHALL return ConfidenceLevel.LOW.
        """
        # Set up services
        feature_library = FeatureLibraryService()
        time_tracking = TimeTrackingService()
        estimation_service = EstimationService(feature_library, time_tracking)
        
        # Create and add a feature with fixed values for simplicity
        feature = Feature(
            id="test_feature",
            name="Test Feature",
            team=TeamType.BACKEND,
            process="Data Operations",
            seed_time_hours=8.0,
        )
        feature_library.add_feature(feature)
        
        # Add the specified number of tracked time entries
        for i in range(data_point_count):
            entry = TrackedTimeEntry(
                id=f"entry_{i}",
                team=TeamType.BACKEND,
                member_name=f"Developer_{i}",
                feature="Test Feature",
                tracked_time_hours=4.0 + i,  # Varying times
                process="Data Operations",
                date=date(2025, 1, 15),
            )
            time_tracking.add_entry(entry)
        
        # Estimate the feature
        result = estimation_service.estimate_feature("Test Feature")
        
        # Verify the result
        assert result.is_ok(), f"Estimation should succeed"
        estimate = result.unwrap()
        
        # Verify confidence is LOW
        assert estimate.confidence == ConfidenceLevel.LOW, \
            f"With {data_point_count} data points (< 3), confidence should be LOW, got {estimate.confidence}"
        
        # Verify seed time is used
        assert estimate.used_seed_time is True, \
            f"With {data_point_count} data points (< 3), used_seed_time should be True"
        
        # Verify estimated hours equals seed time
        assert abs(estimate.estimated_hours - 8.0) < 1e-9, \
            f"With {data_point_count} data points (< 3), estimated_hours should equal seed_time 8.0"
