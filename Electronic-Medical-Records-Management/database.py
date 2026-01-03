from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Update these credentials according to your PostgreSQL setup
DATABASE_URL = "postgresql://postgres:Password@localhost:5432/hospitalmanagement"

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-csearch_path=hms"}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()