from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta
import os


# ============ CONFIGURATION ============

class AppointmentHistorySettings(BaseSettings):
    """Appointment History entity settings"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hospital_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # History Settings
    RETENTION_DAYS: int = 1825  # Keep history for 5 years (1825 days)
    AUTO_CLEANUP_ENABLED: bool = True
    MAX_HISTORY_PER_APPOINTMENT: int = 100  # Maximum history records per appointment

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_history_settings() -> AppointmentHistorySettings:
    """Get cached appointment history settings instance"""
    return AppointmentHistorySettings()


# ============ DATABASE SETUP ============

Base = declarative_base()

# Create database engine
engine = create_engine(
    get_history_settings().DATABASE_URL,
    pool_size=get_history_settings().DATABASE_POOL_SIZE,
    max_overflow=get_history_settings().DATABASE_MAX_OVERFLOW,
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

class AppointmentHistoryException(Exception):
    """Base exception for appointment history"""
    pass


class HistoryNotFoundException(AppointmentHistoryException):
    """Raised when a history record is not found"""
    pass


class MaxHistoryExceededException(AppointmentHistoryException):
    """Raised when max history records exceeded"""
    pass


# ============ CONSTANTS ============

CHANGE_TYPES = [
    "CREATED",
    "UPDATED",
    "RESCHEDULED",
    "CANCELLED",
    "CONFIRMED",
    "COMPLETED",
    "NO_SHOW",
    "STATUS_CHANGED"
]


# ============ UTILITY FUNCTIONS ============

def format_change_summary(change_type: str, old_value: any, new_value: any) -> str:
    """Format a human-readable change summary"""
    if change_type == "CREATED":
        return "Appointment created"
    elif change_type == "CANCELLED":
        return "Appointment cancelled"
    elif change_type == "CONFIRMED":
        return "Appointment confirmed"
    elif change_type == "COMPLETED":
        return "Appointment completed"
    elif change_type == "NO_SHOW":
        return "Marked as no-show"
    elif change_type == "RESCHEDULED":
        return f"Rescheduled from {old_value} to {new_value}"
    elif change_type == "STATUS_CHANGED":
        return f"Status changed from {old_value} to {new_value}"
    elif change_type == "UPDATED":
        return "Appointment details updated"
    else:
        return f"Changed: {change_type}"


def get_change_category(change_type: str) -> str:
    """Categorize change types"""
    status_changes = ["CONFIRMED", "CANCELLED", "COMPLETED", "NO_SHOW", "STATUS_CHANGED"]
    time_changes = ["RESCHEDULED"]
    
    if change_type in status_changes:
        return "STATUS"
    elif change_type in time_changes:
        return "SCHEDULE"
    elif change_type == "CREATED":
        return "CREATION"
    elif change_type == "UPDATED":
        return "MODIFICATION"
    else:
        return "OTHER"


def is_significant_change(change_type: str) -> bool:
    """Determine if a change is significant (affects patient/doctor directly)"""
    significant_changes = ["CREATED", "RESCHEDULED", "CANCELLED", "CONFIRMED"]
    return change_type in significant_changes


def format_date_change(old_date: date, new_date: date) -> str:
    """Format date change for display"""
    if not old_date and new_date:
        return f"Set to {new_date.strftime('%B %d, %Y')}"
    elif old_date and new_date:
        return f"Changed from {old_date.strftime('%B %d, %Y')} to {new_date.strftime('%B %d, %Y')}"
    else:
        return "Date cleared"


def format_time_change(old_time: time, new_time: time) -> str:
    """Format time change for display"""
    if not old_time and new_time:
        return f"Set to {new_time.strftime('%I:%M %p')}"
    elif old_time and new_time:
        return f"Changed from {old_time.strftime('%I:%M %p')} to {new_time.strftime('%I:%M %p')}"
    else:
        return "Time cleared"


def calculate_change_frequency(history_records: list) -> dict:
    """Calculate how frequently appointments are changed"""
    if not history_records:
        return {"total_changes": 0, "reschedules": 0, "cancellations": 0}
    
    reschedules = sum(1 for h in history_records if h.change_type == "RESCHEDULED")
    cancellations = sum(1 for h in history_records if h.change_type == "CANCELLED")
    
    return {
        "total_changes": len(history_records),
        "reschedules": reschedules,
        "cancellations": cancellations
    }


def get_audit_trail_summary(history_records: list) -> dict:
    """Get a summary of the audit trail"""
    if not history_records:
        return {
            "total_changes": 0,
            "first_change": None,
            "last_change": None,
            "change_types": {}
        }
    
    change_types = {}
    for record in history_records:
        change_type = record.change_type
        change_types[change_type] = change_types.get(change_type, 0) + 1
    
    sorted_records = sorted(history_records, key=lambda x: x.changed_at)
    
    return {
        "total_changes": len(history_records),
        "first_change": sorted_records[0].changed_at.isoformat() if sorted_records else None,
        "last_change": sorted_records[-1].changed_at.isoformat() if sorted_records else None,
        "change_types": change_types
    }


def is_within_retention_period(changed_at: datetime) -> bool:
    """Check if history record is within retention period"""
    settings = get_history_settings()
    cutoff_date = datetime.now() - timedelta(days=settings.RETENTION_DAYS)
    return changed_at >= cutoff_date


def get_time_since_change(changed_at: datetime) -> str:
    """Get human-readable time since change"""
    delta = datetime.now() - changed_at
    
    if delta.days > 365:
        years = delta.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif delta.days > 30:
        months = delta.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"


def group_by_date(history_records: list) -> dict:
    """Group history records by date"""
    grouped = {}
    for record in history_records:
        date_key = record.changed_at.date()
        if date_key not in grouped:
            grouped[date_key] = []
        grouped[date_key].append(record)
    return grouped