"""
Test if all tables exist in database
"""
from sqlalchemy import inspect, text
from Appointment.Appointment_config import engine

def test_tables_exist():
    """Check if all required tables exist"""
    print("=" * 50)
    print("🔍 CHECKING DATABASE TABLES")
    print("=" * 50)
    
    # Expected tables for Appointment Scheduling Module
    expected_tables = [
        'appointment',
        'doctor_schedule',
        'blocked_slots',
        'appointment_reminder',
        'appointment_history',
        'waiting_list',
        'doctor',
        'patient',
        'users'  # For foreign keys
    ]
    
    inspector = inspect(engine)
    
    # Check in hms schema
    existing_tables = inspector.get_table_names(schema='hms')
    
    print(f"\n📊 Found {len(existing_tables)} tables in 'hms' schema\n")
    
    for table in expected_tables:
        if table in existing_tables:
            print(f"✅ Table '{table}' EXISTS")
            
            # Get columns
            columns = inspector.get_columns(table, schema='hms')
            print(f"   Columns: {len(columns)}")
            
            # Show first 3 columns
            for col in columns[:3]:
                print(f"      - {col['name']}: {col['type']}")
            if len(columns) > 3:
                print(f"      ... and {len(columns) - 3} more columns")
            print()
        else:
            print(f"❌ Table '{table}' MISSING")
            print()
    
    print("=" * 50)

if __name__ == "__main__":
    test_tables_exist()