"""
Appointment Entity - Configuration
Contains settings, database setup, exceptions, and utilities specific to Appointment
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta
import os


# ============ CONFIGURATION ============

class AppointmentSettings(BaseSettings):
    """Appointment entity settings"""

    # Database
    DATABASE_URL: str = "postgresql://postgres:sql12345678@localhost:5432/hospitalmanagement"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Appointment Settings
    MIN_APPOINTMENT_DURATION_MINUTES: int = 15
    MAX_APPOINTMENT_DURATION_MINUTES: int = 480  # 8 hours
    DEFAULT_APPOINTMENT_DURATION_MINUTES: int = 30
    ALLOW_PAST_DATE_BOOKING: bool = False
    ALLOW_SAME_DAY_BOOKING: bool = True
    MAX_APPOINTMENTS_PER_DAY_PER_DOCTOR: int = 50
    BOOKING_ADVANCE_DAYS: int = 90  # Can book up to 90 days in advance

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_appointment_settings() -> AppointmentSettings:
    """Get cached appointment settings instance"""
    return AppointmentSettings()


# ============ DATABASE SETUP ============

Base = declarative_base()

# Create database engine
engine = create_engine(
    get_appointment_settings().DATABASE_URL,
    pool_size=get_appointment_settings().DATABASE_POOL_SIZE,
    max_overflow=get_appointment_settings().DATABASE_MAX_OVERFLOW,
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

class AppointmentException(Exception):
    """Base exception for appointment"""
    pass


class AppointmentNotFoundException(AppointmentException):
    """Raised when an appointment is not found"""
    pass


class TimeSlotConflictException(AppointmentException):
    """Raised when there's a time slot conflict"""
    pass


class PastDateException(AppointmentException):
    """Raised when trying to book past dates"""
    pass


class InvalidTimeRangeException(AppointmentException):
    """Raised when start time is after end time"""
    pass


class AppointmentStatusException(AppointmentException):
    """Raised when appointment status transition is invalid"""
    pass


# ============ CONSTANTS ============

APPOINTMENT_TYPES = [
    "CONSULTATION",
    "FOLLOWUP", 
    "EMERGENCY",
    "ROUTINE_CHECKUP"
]

APPOINTMENT_STATUSES = [
    "SCHEDULED",
    "CONFIRMED",
    "CANCELLED",
    "COMPLETED",
    "NO_SHOW",
    "RESCHEDULED"
]


# ============ UTILITY FUNCTIONS ============

def is_valid_time_range(start_time: time, end_time: time) -> bool:
    """Check if start time is before end time"""
    return start_time < end_time


def is_past_date(check_date: date) -> bool:
    """Check if date is in the past"""
    return check_date < date.today()


def calculate_duration_minutes(start_time: time, end_time: time) -> int:
    """Calculate duration in minutes between two times"""
    start_datetime = datetime.combine(date.today(), start_time)
    end_datetime = datetime.combine(date.today(), end_time)
    duration = (end_datetime - start_datetime).total_seconds() / 60
    return int(duration)


def is_within_booking_window(appointment_date: date) -> bool:
    """Check if appointment date is within allowed booking window"""
    settings = get_appointment_settings()
    max_date = date.today() + timedelta(days=settings.BOOKING_ADVANCE_DAYS)
    return date.today() <= appointment_date <= max_date


def can_book_appointment(appointment_date: date) -> tuple:
    """
    Check if appointment can be booked for the date
    Returns (can_book: bool, reason: str)
    """
    settings = get_appointment_settings()
    
    # Check if past date
    if is_past_date(appointment_date) and not settings.ALLOW_PAST_DATE_BOOKING:
        return (False, "Cannot book appointments for past dates")
    
    # Check if same day
    if appointment_date == date.today() and not settings.ALLOW_SAME_DAY_BOOKING:
        return (False, "Same day booking is not allowed")
    
    # Check booking window
    if not is_within_booking_window(appointment_date):
        return (False, f"Appointments can only be booked up to {settings.BOOKING_ADVANCE_DAYS} days in advance")
    
    return (True, "Can book appointment")


def validate_appointment_duration(duration_minutes: int) -> bool:
    """Validate if appointment duration is within allowed range"""
    settings = get_appointment_settings()
    return (settings.MIN_APPOINTMENT_DURATION_MINUTES <= 
            duration_minutes <= 
            settings.MAX_APPOINTMENT_DURATION_MINUTES)
