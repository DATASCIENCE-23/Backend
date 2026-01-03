from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common_base import Base

DATABASE_URL = "postgresql://postgres:CHARLIEechoDELTA@localhost:5432/hms"


engine = create_engine(
    DATABASE_URL,
    echo=True
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
