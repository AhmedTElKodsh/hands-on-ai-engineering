"""
Enumerations for the curriculum scaffolding conversion system.
"""

from enum import Enum


class TierLevel(Enum):
    """
    Difficulty tier levels for scaffolding.
    
    Determines the amount of guidance and detail provided in scaffolding:
    - TIER_1: Foundations level with detailed hints and step-by-step guidance
    - TIER_2: Intermediate level with moderate hints and balanced scaffolding
    - TIER_3: Advanced level with minimal hints and basic signatures only
    """
    TIER_1 = "foundations"
    TIER_2 = "intermediate"
    TIER_3 = "advanced"


class ConversionStatus(Enum):
    """
    Status of chapter conversion process.
    
    Tracks the progress of converting a chapter from complete solutions
    to educational scaffolding.
    """
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NEEDS_REVIEW = "needs_review"
    VERIFIED = "verified"
