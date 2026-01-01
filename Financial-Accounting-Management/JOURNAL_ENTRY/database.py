from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common_base import Base

DATABASE_URL = "postgresql://hms_user:CloudComputing@localhost/hospitalmanagement"

engine = create_engine(DATABASE_URL)

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
