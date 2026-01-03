"""
Blocked_Slots Entity - Configuration
Contains settings, database setup, exceptions, and utilities specific to Blocked Slots
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta
import os


# ============ CONFIGURATION ============

class BlockedSlotsSettings(BaseSettings):
    """Blocked Slots entity settings"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hospital_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Blocked Slots Settings
    MAX_DAYS_BLOCK_AT_ONCE: int = 365
    AUTO_CLEANUP_OLD_BLOCKS_DAYS: int = 90  # Keep only last 90 days
    ALLOW_PAST_DATE_BLOCKING: bool = False
    REQUIRE_REASON: bool = True
    MIN_REASON_LENGTH: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_blocked_slots_settings() -> BlockedSlotsSettings:
    """Get cached blocked slots settings instance"""
    return BlockedSlotsSettings()


# ============ DATABASE SETUP ============

Base = declarative_base()

# Create database engine
engine = create_engine(
    get_blocked_slots_settings().DATABASE_URL,
    pool_size=get_blocked_slots_settings().DATABASE_POOL_SIZE,
    max_overflow=get_blocked_slots_settings().DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============ CUSTOM EXCEPTIONS ============

class BlockedSlotException(Exception):
    """Base exception for blocked slots"""
    pass


class BlockedSlotNotFoundException(BlockedSlotException):
    """Raised when a blocked slot is not found"""
    pass


class TimeSlotConflictException(BlockedSlotException):
    """Raised when there's a time slot conflict"""
    pass


class PastDateException(BlockedSlotException):
    """Raised when trying to block past dates"""
    pass


class InvalidTimeRangeException(BlockedSlotException):
    """Raised when start time is after end time"""
    pass


class MaxDaysExceededException(BlockedSlotException):
    """Raised when trying to block more days than allowed"""
    pass


class InvalidReasonException(BlockedSlotException):
    """Raised when reason is invalid or too short"""
    pass


# ============ CONSTANTS ============

COMMON_BLOCK_REASONS = [
    "Vacation",
    "Personal leave",
    "Medical leave",
    "Conference",
    "Training",
    "Meeting",
    "Emergency",
    "Holiday",
    "Surgery",
    "Other"
]


# ============ UTILITY FUNCTIONS ============

def is_valid_time_range(start_time: time, end_time: time) -> bool:
    """Check if start time is before end time"""
    return start_time < end_time


def is_past_date(check_date: date) -> bool:
    """Check if date is in the past"""
    return check_date < date.today()


def is_time_overlap(start1: time, end1: time, start2: time, end2: time) -> bool:
    """
    Check if two time ranges overlap
    Returns True if there's overlap, False otherwise
    """
    return not (end1 <= start2 or start1 >= end2)


def calculate_days_to_block(start_date: date, end_date: date) -> int:
    """Calculate number of days to block"""
    return (end_date - start_date).days + 1


def validate_block_duration(start_date: date, end_date: date) -> bool:
    """Validate if block duration is within allowed range"""
    settings = get_blocked_slots_settings()
    days = calculate_days_to_block(start_date, end_date)
    return days <= settings.MAX_DAYS_BLOCK_AT_ONCE


def validate_reason(reason: str) -> bool:
    """Validate if reason is valid"""
    settings = get_blocked_slots_settings()
    
    if not settings.REQUIRE_REASON:
        return True
    
    if not reason or len(reason.strip()) < settings.MIN_REASON_LENGTH:
        return False
    
    return True


def can_block_date(blocked_date: date) -> tuple:
    """
    Check if date can be blocked
    Returns (can_block: bool, reason: str)
    """
    settings = get_blocked_slots_settings()
    
    # Check if past date
    if is_past_date(blocked_date) and not settings.ALLOW_PAST_DATE_BLOCKING:
        return (False, "Cannot block past dates")
    
    return (True, "Can block date")


def get_month_date_range(year: int, month: int) -> tuple:
    """
    Get first and last date of a month
    Returns (first_date, last_date)
    """
    from calendar import monthrange
    
    first_date = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    last_date = date(year, month, last_day)
    
    return (first_date, last_date)


def format_date(check_date: date) -> str:
    """Format date for display (e.g., 'Monday, January 15, 2024')"""
    return check_date.strftime("%A, %B %d, %Y")


def days_until(target_date: date) -> int:
    """Calculate number of days until target date"""
    return (target_date - date.today()).days


def is_within_cleanup_period(blocked_date: date) -> bool:
    """Check if blocked date is old enough to be cleaned up"""
    settings = get_blocked_slots_settings()
    cutoff_date = date.today() - timedelta(days=settings.AUTO_CLEANUP_OLD_BLOCKS_DAYS)
    return blocked_date < cutoff_date


def generate_date_range(start_date: date, end_date: date) -> list:
    """Generate list of dates between start and end date (inclusive)"""
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates


def is_full_day_block(start_time: time, end_time: time) -> bool:
    """Check if blocked slot covers the full day"""
    return start_time == time(0, 0, 0) and end_time == time(23, 59, 59)
