"""
Database configuration for Pharmacy module (PostgreSQL)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------------------
# DATABASE URL (PostgreSQL)
# -------------------------------------------------------------------
# Format: postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DB_NAME
SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:preethi@localhost:5432/cloudHospital"
)
# ↑ adjust user, password, host, port, db name to your setup

# -------------------------------------------------------------------
# ENGINE & SESSION
# -------------------------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency for DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
