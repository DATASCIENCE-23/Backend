"""
Shared Database Configuration
This file provides database connection for all modules in the Appointment Scheduling system
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ============ DATABASE CONFIGURATION ============

# Database URL - Update with your credentials
DATABASE_URL = "postgresql://postgres:sql12345678@localhost:5432/hospitalmanagement"

# Create engine with hms schema
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-csearch_path=hms"},  # Set default schema to hms
    pool_size=10,          # Number of connections in the pool
    max_overflow=20,       # Maximum number of connections that can be created beyond pool_size
    pool_pre_ping=True,    # Verify connections before using them
    echo=False             # Set to True to see SQL queries (useful for debugging)
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for models
Base = declarative_base()


# ============ DATABASE DEPENDENCY ============

def get_db() -> Session:
    """
    Database dependency for FastAPI endpoints
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============ DATABASE UTILITIES ============

def init_db():
    """
    Initialize database - create all tables
    Note: Only call this if you want SQLAlchemy to create tables
    In your case, tables already exist from the SQL schema file
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def check_db_connection():
    """
    Check if database connection is working
    Returns True if connected, False otherwise
    """
    try:
        db = SessionLocal()
        # Try to execute a simple query
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False


# ============ TEST CONNECTION ON IMPORT ============

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 TESTING DATABASE CONNECTION")
    print("=" * 50)
    check_db_connection()