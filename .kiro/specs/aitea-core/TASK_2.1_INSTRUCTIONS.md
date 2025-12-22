# Task 2.1: Create Enum Definitions

## Objective
Create the `src/models/enums.py` file with all enum types needed for the AITEA Core library.

## Background
Enums provide type-safe constants throughout the application. Python's `Enum` class from the standard library allows us to define named constants with associated string values. Using string values (rather than auto-generated integers) makes the enums more readable in logs, databases, and API responses.

## Requirements Reference
This task implements data model requirements from Requirements 1.1-1.5 in the requirements document.

## Implementation Guide

### Step 1: Create the File
Create a new file at `src/models/enums.py`

### Step 2: Import Dependencies
You'll need:
```python
from enum import Enum
```

### Step 3: Implement the Enums
Create the following 8 enum classes. Each should:
- Inherit from `Enum`
- Use UPPERCASE names for enum members
- Use lowercase string values (e.g., `FRONTEND = "frontend"`)

#### Enums to Implement:

1. **Team** - Represents which team owns a feature
   - Members: FRONTEND, BACKEND, BOTH
   - Values: "frontend", "backend", "both"

2. **Process** - Represents functional areas (see Process Definitions table in requirements)
   - Members: USER_MANAGEMENT, CONTENT_MANAGEMENT, COMMUNICATION, DATA_OPERATIONS, MEDIA_HANDLING, INTEGRATION, REAL_TIME, BACKGROUND_PROCESSING, VISUAL_ENHANCEMENT
   - Values: Use the display names from the requirements (e.g., "User Management", "Real-time")

3. **Priority** - Indicates feature importance
   - Members: CORE, COMMON, OPTIONAL
   - Values: "core", "common", "optional"

4. **Basis** - Indicates how an estimate was calculated
   - Members: TRACKED_MEAN, TRACKED_MEDIAN, TRACKED_P80, SEED
   - Values: "tracked_mean", "tracked_median", "tracked_p80", "seed"

5. **Confidence** - Indicates estimate reliability
   - Members: HIGH, MEDIUM, LOW
   - Values: "high", "medium", "low"

6. **EstimationStyle** - User's preferred estimation method
   - Members: MEAN, MEDIAN, P80
   - Values: "mean", "median", "p80"

7. **TimeUnit** - Units for time conversion
   - Members: HOURS, MINUTES, DAYS
   - Values: "hours", "minutes", "days"

8. **ExperienceLevel** - Developer experience for multipliers
   - Members: JUNIOR, MID, SENIOR
   - Values: "junior", "mid", "senior"

### Step 4: Verify Your Implementation

After implementing, verify:
- [ ] All 8 enum classes are defined
- [ ] Each enum inherits from `Enum`
- [ ] Enum member names are UPPERCASE
- [ ] Enum values are lowercase strings (except Process which uses title case)
- [ ] Process enum has exactly 9 members matching the requirements table
- [ ] No syntax errors (run `python -m py_compile src/models/enums.py`)

## Example Pattern

Here's an example of the correct pattern for one enum:

```python
class Team(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    BOTH = "both"
```

## Acceptance Criteria
✅ File `src/models/enums.py` exists
✅ All 8 enums are implemented with correct members and values
✅ Code follows Python enum conventions
✅ No syntax errors

## Next Steps
After completing this task, let me know and I'll review your implementation before we proceed to task 2.2 (error types).
