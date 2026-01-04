"""
Pharmacy Module - Configuration and Setup
Contains application configuration, database setup, and utility functions
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
import os


# ============ CONFIGURATION ============

class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Hospital Pharmacy Module"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hospital_pharmacy"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Stock Management
    LOW_STOCK_THRESHOLD_PERCENT: int = 20  # Alert when stock is 20% of reorder level
    EXPIRY_WARNING_DAYS: int = 30  # Warn when medicines expire in 30 days

    # Integration APIs (for other modules)
    DOCTOR_MODULE_API_URL: str = "http://localhost:8001/api/doctor"
    BILLING_MODULE_API_URL: str = "http://localhost:8002/api/billing"
    INVENTORY_MODULE_API_URL: str = "http://localhost:8003/api/inventory"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# ============ DATABASE SETUP ============

Base = declarative_base()


def get_database_url() -> str:
    """Get database URL from environment or config"""
    settings = get_settings()
    return settings.DATABASE_URL


# Create database engine
engine = create_engine(
    get_database_url(),
    pool_size=get_settings().DATABASE_POOL_SIZE,
    max_overflow=get_settings().DATABASE_MAX_OVERFLOW,
    echo=get_settings().DEBUG,
    pool_pre_ping=True  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency for getting database session
    Used in FastAPI endpoints with Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


# ============ CUSTOM EXCEPTIONS ============

class PharmacyException(Exception):
    """Base exception for pharmacy module"""
    pass


class NotFoundException(PharmacyException):
    """Raised when a requested resource is not found"""
    pass


class DuplicateRecordException(PharmacyException):
    """Raised when trying to create a duplicate record"""
    pass


class InsufficientStockException(PharmacyException):
    """Raised when there is insufficient stock for dispensing"""
    pass


class ValidationException(PharmacyException):
    """Raised when validation fails"""
    pass


class UnauthorizedException(PharmacyException):
    """Raised when user is not authorized"""
    pass


# ============ LOGGING CONFIGURATION ============

import logging
from logging.handlers import RotatingFileHandler
import sys


def setup_logging():
    """Configure application logging"""
    settings = get_settings()

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Configure logging format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/pharmacy.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Error file handler
    error_handler = RotatingFileHandler(
        'logs/pharmacy_errors.log',
        maxBytes=10485760,
        backupCount=5
    )
    error_handler.setFormatter(log_format)
    error_handler.setLevel(logging.ERROR)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    return root_logger


# ============ AUTHENTICATION UTILITIES ============

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode JWT access token"""
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Get current authenticated user from JWT token
    Use as dependency in protected endpoints
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return {
        "user_id": user_id,
        "username": payload.get("username"),
        "roles": payload.get("roles", [])
    }


def require_role(allowed_roles: list):
    """
    Dependency factory for role-based access control
    Usage: current_user = Depends(require_role(["pharmacist", "admin"]))
    """

    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_roles = current_user.get("roles", [])
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(allowed_roles)}"
            )
        return current_user

    return role_checker


# ============ MIDDLEWARE & CORS ============

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def configure_middleware(app: FastAPI):
    """Configure application middleware"""
    settings = get_settings()

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host (optional - for production)
    # app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])


# ============ UTILITY FUNCTIONS ============

def calculate_deficit(available: int, reorder_level: int) -> int:
    """Calculate stock deficit"""
    return max(0, reorder_level - available)


def is_near_expiry(expiry_date, days: int = 30) -> bool:
    """Check if medicine is near expiry"""
    from datetime import date, timedelta
    return expiry_date <= date.today() + timedelta(days=days)


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"₹{amount:,.2f}"


# ============ CONSTANTS ============

MEDICINE_FORMS = [
    "Tablet", "Capsule", "Syrup", "Suspension", "Injection",
    "Cream", "Ointment", "Drops", "Inhaler", "Powder"
]

PRESCRIPTION_STATUS = [
    "pending", "in_progress", "completed", "partially_completed", "cancelled"
]

DISPENSE_STATUS = [
    "pending", "completed", "billed"
]

USER_ROLES = [
    "pharmacist", "doctor", "admin", "inventory_manager", "billing"
]