from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, time, timedelta


# ================= SETTINGS =================

class AppointmentHistorySettings(BaseSettings):
    """Appointment History entity settings"""

    DATABASE_URL: str = "postgresql://postgres:root@localhost:5432/hospitalmanagement"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # History retention
    RETENTION_DAYS: int = 1825  # 5 years
    AUTO_CLEANUP_ENABLED: bool = True
    MAX_HISTORY_PER_APPOINTMENT: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_history_settings() -> AppointmentHistorySettings:
    return AppointmentHistorySettings()


# ================= DATABASE =================

Base = declarative_base()

engine = create_engine(
    get_history_settings().DATABASE_URL,
    pool_size=get_history_settings().DATABASE_POOL_SIZE,
    max_overflow=get_history_settings().DATABASE_MAX_OVERFLOW,
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

class AppointmentHistoryException(Exception):
    pass


class HistoryNotFoundException(AppointmentHistoryException):
    pass


class MaxHistoryExceededException(AppointmentHistoryException):
    pass


# ================= CONSTANTS =================

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
