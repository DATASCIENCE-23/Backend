"""
Shared Database Configuration
This file provides database connection for all modules in the Appointment Scheduling system
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import ProgrammingError

# ============ DATABASE CONFIGURATION ============

# Database URL - Update with your credentials
DATABASE_URL = "postgresql://postgres:root@localhost:5432/hospitalmanagement"

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


# ============ DATABASE INITIALIZATION ============

def init_db():
    """
    Initialize database - create all tables from SQLAlchemy models
    
    IMPORTANT: This is safe to call even if tables already exist!
    SQLAlchemy will NOT recreate existing tables.
    
    As per project lead requirements, this ensures all teams use
    Base.metadata.create_all(bind=engine) for consistency.
    """
    try:
        # Import all models so they're registered with Base
        from Appointment.Appointment_model import Appointment
        from Doctor_Schedule.Doctor_Schedule_model import DoctorSchedule
        from Blocked_Slots.Blocked_Slots_model import BlockedSlot

        from Appointment_History.Appointment_History_model import AppointmentHistory
        from Appointment_Reminder.Appointment_Reminder_model import AppointmentReminder
        from Waiting_List.Waiting_List_model import WaitingList

        from Doctor.models import Doctor
        from Patient.models import Patient
        from Specialization.models import Specialization

        
        # Create all tables (safe - won't recreate existing ones)
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database initialization completed!")
        print("   Tables checked/created from SQLAlchemy models")
        
    except Exception as e:
        print(f"⚠️  Database initialization warning: {str(e)}")
        print("   This is usually fine if tables already exist from SQL file")


# ============ DATABASE UTILITIES ============

def check_db_connection():
    """
    Check if database connection is working
    Returns True if connected, False otherwise
    """
    try:
        db = SessionLocal()
        # Try to execute a simple query
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False


def check_tables_exist():
    """
    Check if required tables exist in the database
    """
    try:
        db = SessionLocal()
        
        tables_to_check = [
            "hms.appointment",
            "hms.doctor_schedule", 
            "hms.blocked_slots"
        ]
        
        print("\n🔍 Checking database tables:")
        all_exist = True
        
        for table in tables_to_check:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table} LIMIT 1"))
                print(f"   ✅ {table} - EXISTS")
            except ProgrammingError:
                print(f"   ❌ {table} - MISSING")
                all_exist = False
        
        db.close()
        
        if all_exist:
            print("\n✅ All required tables exist!")
        else:
            print("\n⚠️  Some tables are missing. Run init_db() to create them.")
        
        return all_exist
        
    except Exception as e:
        print(f"❌ Error checking tables: {str(e)}")
        return False


# ============ STARTUP FUNCTION ============

def startup_db():
    """
    Complete database startup routine
    Call this when your FastAPI app starts
    """
    print("=" * 60)
    print("🚀 STARTING DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Step 1: Check connection
    print("\n1️⃣ Checking database connection...")
    if not check_db_connection():
        print("❌ Cannot proceed without database connection!")
        return False
    
    # Step 2: Initialize tables (safe - won't recreate)
    print("\n2️⃣ Initializing database tables...")
    init_db()
    
    # Step 3: Verify tables exist
    print("\n3️⃣ Verifying tables...")
    check_tables_exist()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE READY!")
    print("=" * 60)
    return True


# ============ TEST CONNECTION ON IMPORT ============

if __name__ == "__main__":
    startup_db()
