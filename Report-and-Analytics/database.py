from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
        "postgresql://neondb_owner:npg_ra5GlUMB6ZLX@"
        "ep-cool-hat-a4zpgn9g.us-east-1.aws.neon.tech/"
        "neondb?sslmode=require"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
