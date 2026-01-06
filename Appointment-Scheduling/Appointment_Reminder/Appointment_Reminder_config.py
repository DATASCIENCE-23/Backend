from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta


# ================= SETTINGS =================

class AppointmentReminderSettings(BaseSettings):
    """Appointment Reminder entity settings"""

    DATABASE_URL: str = "postgresql://postgres:root@localhost:5432/hospitalmanagement"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    DEFAULT_REMINDER_HOURS_BEFORE: int = 24
    ENABLE_AUTO_REMINDERS: bool = True
    MAX_REMINDERS_PER_APPOINTMENT: int = 3
    RETRY_FAILED_REMINDERS: bool = True
    FAILED_REMINDER_RETRY_HOURS: int = 2

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_reminder_settings() -> AppointmentReminderSettings:
    return AppointmentReminderSettings()


# ================= DATABASE =================

Base = declarative_base()

engine = create_engine(
    get_reminder_settings().DATABASE_URL,
    pool_size=get_reminder_settings().DATABASE_POOL_SIZE,
    max_overflow=get_reminder_settings().DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= EXCEPTIONS =================

class ReminderException(Exception):
    pass


class ReminderNotFoundException(ReminderException):
    pass


class MaxRemindersExceededException(ReminderException):
    pass


# ================= CONSTANTS =================

REMINDER_TYPES = [
    "EMAIL",
    "SMS",
    "PUSH_NOTIFICATION",
    "WHATSAPP"
]

REMINDER_STATUSES = [
    "PENDING",
    "SENT",
    "FAILED",
    "CANCELLED"
]


# ================= UTILITIES =================

def calculate_reminder_time(
    appointment_datetime: datetime,
    hours_before: int
) -> datetime:
    return appointment_datetime - timedelta(hours=hours_before)


def is_reminder_due(reminder_time: datetime) -> bool:
    return datetime.now() >= reminder_time


def format_reminder_message(
    patient_name: str,
    doctor_name: str,
    appointment_date: date,
    appointment_time: time
) -> str:
    return (
        f"Reminder: {patient_name}, you have an appointment with "
        f"Dr. {doctor_name} on "
        f"{appointment_date.strftime('%B %d, %Y')} at "
        f"{appointment_time.strftime('%I:%M %p')}."
    )
