"""
Waiting_List Entity - Configuration
Contains settings, database setup, exceptions, and utilities specific to Waiting List
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta
import os


# ============ CONFIGURATION ============

class WaitingListSettings(BaseSettings):
    """Waiting List entity settings"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hospital_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Waiting List Settings
    DEFAULT_EXPIRY_DAYS: int = 7  # Default expiry period for waiting list entries
    MAX_WAITING_DAYS: int = 30  # Maximum days a patient can be on waiting list
    AUTO_NOTIFICATION_ENABLED: bool = True
    NOTIFICATION_ADVANCE_HOURS: int = 24  # Notify 24 hours before slot becomes available
    MAX_ACTIVE_WAITING_ENTRIES_PER_PATIENT: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_waiting_list_settings() -> WaitingListSettings:
    """Get cached waiting list settings instance"""
    return WaitingListSettings()


# ============ DATABASE SETUP ============

Base = declarative_base()

# Create database engine
engine = create_engine(
    get_waiting_list_settings().DATABASE_URL,
    pool_size=get_waiting_list_settings().DATABASE_POOL_SIZE,
    max_overflow=get_waiting_list_settings().DATABASE_MAX_OVERFLOW,
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

class WaitingListException(Exception):
    """Base exception for waiting list"""
    pass


class WaitingListNotFoundException(WaitingListException):
    """Raised when a waiting list entry is not found"""
    pass


class DuplicateWaitingListException(WaitingListException):
    """Raised when trying to add duplicate waiting list entry"""
    pass


class WaitingListExpiredException(WaitingListException):
    """Raised when waiting list entry has expired"""
    pass


class MaxWaitingEntriesException(WaitingListException):
    """Raised when patient exceeds max waiting entries"""
    pass


class InvalidTimeRangeException(WaitingListException):
    """Raised when start time is after end time"""
    pass


# ============ CONSTANTS ============

WAITING_LIST_STATUSES = [
    "ACTIVE",
    "NOTIFIED",
    "ACCEPTED",
    "DECLINED",
    "EXPIRED",
    "CANCELLED"
]


# ============ UTILITY FUNCTIONS ============

def is_valid_time_range(start_time: time, end_time: time) -> bool:
    """Check if start time is before end time"""
    return start_time < end_time


def calculate_expiry_date(added_at: datetime, expiry_days: int = None) -> datetime:
    """Calculate expiry date for waiting list entry"""
    settings = get_waiting_list_settings()
    days = expiry_days if expiry_days else settings.DEFAULT_EXPIRY_DAYS
    return added_at + timedelta(days=days)


def is_expired(expires_at: datetime) -> bool:
    """Check if waiting list entry has expired"""
    return datetime.now() >= expires_at


def days_until_expiry(expires_at: datetime) -> int:
    """Calculate days until expiry"""
    delta = expires_at - datetime.now()
    return max(0, delta.days)


def is_within_max_waiting_period(preferred_date: date) -> bool:
    """Check if preferred date is within maximum waiting period"""
    settings = get_waiting_list_settings()
    max_date = date.today() + timedelta(days=settings.MAX_WAITING_DAYS)
    return preferred_date <= max_date


def format_time_preference(start_time: time, end_time: time) -> str:
    """Format time preference for display"""
    start_str = start_time.strftime("%I:%M %p")
    end_str = end_time.strftime("%I:%M %p")
    return f"{start_str} - {end_str}"


def get_priority_score(added_at: datetime, preferred_date: date) -> int:
    """
    Calculate priority score for waiting list entry
    Earlier additions and earlier preferred dates get higher scores
    """
    days_waiting = (datetime.now() - added_at).days
    days_to_preferred = (preferred_date - date.today()).days
    
    # Higher score for longer waiting time, lower score for far future dates
    return (days_waiting * 10) - days_to_preferred


def should_send_notification(expires_at: datetime) -> bool:
    """Check if notification should be sent based on expiry time"""
    settings = get_waiting_list_settings()
    if not settings.AUTO_NOTIFICATION_ENABLED:
        return False
    
    hours_until_expiry = (expires_at - datetime.now()).total_seconds() / 3600
    return 0 < hours_until_expiry <= settings.NOTIFICATION_ADVANCE_HOURS


def validate_preferred_date(preferred_date: date) -> tuple:
    """
    Validate preferred date for waiting list
    Returns (is_valid: bool, reason: str)
    """
    if preferred_date < date.today():
        return (False, "Preferred date cannot be in the past")
    
    if not is_within_max_waiting_period(preferred_date):
        settings = get_waiting_list_settings()
        return (False, f"Preferred date must be within {settings.MAX_WAITING_DAYS} days")
    
    return (True, "Valid preferred date")


def get_waiting_duration(added_at: datetime) -> dict:
    """Get waiting duration in a readable format"""
    duration = datetime.now() - added_at
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "total_hours": days * 24 + hours
    }


def is_time_overlap(start1: time, end1: time, start2: time, end2: time) -> bool:
    """Check if two time ranges overlap"""
    return not (end1 <= start2 or start1 >= end2)


def format_waiting_status(status: str) -> str:
    """Format waiting list status for display"""
    status_display = {
        "ACTIVE": "Active - Waiting",
        "NOTIFIED": "Notified - Pending Response",
        "ACCEPTED": "Accepted - Slot Reserved",
        "DECLINED": "Declined",
        "EXPIRED": "Expired",
        "CANCELLED": "Cancelled"
    }
    return status_display.get(status, status)