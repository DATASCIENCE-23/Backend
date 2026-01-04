from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 CHANGE THIS ACCORDING TO YOUR SYSTEM
DATABASE_URL = "postgresql://postgres:sutharsan@localhost:5432/hospitalmanagement"



# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=True  # set False in production
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
