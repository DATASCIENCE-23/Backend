"""
Doctor_Schedule Entity - Configuration
Contains settings, database setup, exceptions, and utilities specific to Doctor Schedule
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta
import os


# ============ CONFIGURATION ============

class DoctorScheduleSettings(BaseSettings):
    """Doctor Schedule entity settings"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hospital_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Doctor Schedule Settings
    MIN_SLOT_DURATION_MINUTES: int = 15
    MAX_SLOT_DURATION_MINUTES: int = 480  # 8 hours
    DEFAULT_SLOT_DURATION_MINUTES: int = 30
    MAX_PATIENTS_PER_SLOT: int = 5
    MIN_PATIENTS_PER_SLOT: int = 1
    SCHEDULE_EFFECTIVE_DAYS: int = 365  # Default validity period

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_schedule_settings() -> DoctorScheduleSettings:
    """Get cached schedule settings instance"""
    return DoctorScheduleSettings()


# ============ DATABASE SETUP ============

Base = declarative_base()

# Create database engine
engine = create_engine(
    get_schedule_settings().DATABASE_URL,
    pool_size=get_schedule_settings().DATABASE_POOL_SIZE,
    max_overflow=get_schedule_settings().DATABASE_MAX_OVERFLOW,
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

class DoctorScheduleException(Exception):
    """Base exception for doctor schedule"""
    pass


class DoctorScheduleNotFoundException(DoctorScheduleException):
    """Raised when a doctor schedule is not found"""
    pass


class ScheduleOverlapException(DoctorScheduleException):
    """Raised when schedules overlap"""
    pass


class InvalidTimeRangeException(DoctorScheduleException):
    """Raised when start time is after end time"""
    pass


class InvalidSlotDurationException(DoctorScheduleException):
    """Raised when slot duration is invalid"""
    pass


class InvalidDateRangeException(DoctorScheduleException):
    """Raised when date range is invalid"""
    pass


# ============ CONSTANTS ============

DAYS_OF_WEEK = [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY"
]


# ============ UTILITY FUNCTIONS ============

def is_valid_time_range(start_time: time, end_time: time) -> bool:
    """Check if start time is before end time"""
    return start_time < end_time


def is_valid_date_range(start_date: date, end_date: date) -> bool:
    """Check if start date is before or equal to end date"""
    return start_date <= end_date


def calculate_duration_minutes(start_time: time, end_time: time) -> int:
    """Calculate duration in minutes between two times"""
    start_datetime = datetime.combine(date.today(), start_time)
    end_datetime = datetime.combine(date.today(), end_time)
    duration = (end_datetime - start_datetime).total_seconds() / 60
    return int(duration)


def generate_time_slots(start_time: time, end_time: time, slot_duration: int) -> list:
    """
    Generate time slots between start and end time
    Returns list of (start_time, end_time) tuples
    """
    slots = []
    current_datetime = datetime.combine(date.today(), start_time)
    end_datetime = datetime.combine(date.today(), end_time)
    slot_delta = timedelta(minutes=slot_duration)
    
    while current_datetime + slot_delta <= end_datetime:
        slot_end = current_datetime + slot_delta
        slots.append((current_datetime.time(), slot_end.time()))
        current_datetime = slot_end
    
    return slots


def get_day_of_week(check_date: date) -> str:
    """Get day of week name from date (e.g., 'MONDAY')"""
    return check_date.strftime("%A").upper()


def format_time_slot(start_time: time, end_time: time) -> str:
    """Format time slot for display (e.g., '09:00 AM - 10:00 AM')"""
    start_str = start_time.strftime("%I:%M %p")
    end_str = end_time.strftime("%I:%M %p")
    return f"{start_str} - {end_str}"


def validate_slot_duration(duration_minutes: int) -> bool:
    """Validate if slot duration is within allowed range"""
    settings = get_schedule_settings()
    return (settings.MIN_SLOT_DURATION_MINUTES <= 
            duration_minutes <= 
            settings.MAX_SLOT_DURATION_MINUTES)


def validate_patients_per_slot(num_patients: int) -> bool:
    """Validate if number of patients per slot is within allowed range"""
    settings = get_schedule_settings()
    return (settings.MIN_PATIENTS_PER_SLOT <= 
            num_patients <= 
            settings.MAX_PATIENTS_PER_SLOT)


def is_time_overlap(start1: time, end1: time, start2: time, end2: time) -> bool:
    """
    Check if two time ranges overlap
    Returns True if there's overlap, False otherwise
    """
    return not (end1 <= start2 or start1 >= end2)


def get_week_date_range(reference_date: date = None) -> tuple:
    """
    Get start and end date of the week for a reference date
    Returns (monday_date, sunday_date)
    """
    if reference_date is None:
        reference_date = date.today()
    
    # Get Monday of the week
    days_since_monday = reference_date.weekday()
    monday = reference_date - timedelta(days=days_since_monday)
    
    # Get Sunday of the week
    sunday = monday + timedelta(days=6)
    
    return (monday, sunday)
