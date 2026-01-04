"""
Insert test data for patient and doctor
Run this BEFORE running appointment tests
"""
from sqlalchemy import text
from Appointment.Appointment_config import get_db

def insert_test_data():
    """Insert test patient and doctor if they don't exist"""
    print("=" * 50)
    print("📝 INSERTING TEST DATA")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # Check if patient exists
        result = db.execute(text("SELECT COUNT(*) FROM hms.patient WHERE patient_id = 1"))
        patient_exists = result.scalar() > 0
        
        if not patient_exists:
            print("\n1️⃣ Inserting test patient...")
            
            # Insert patient (patient table doesn't require user_id to exist first)
            db.execute(text("""
                INSERT INTO hms.patient (
                    patient_id, hospital_id, first_name, last_name, 
                    date_of_birth, gender, phone_number, email
                )
                VALUES (
                    1, 'HP001', 'John', 'Doe', 
                    '1990-01-01', 'male', '1234567890', 'patient@test.com'
                )
                ON CONFLICT (patient_id) DO NOTHING
            """))
            db.commit()
            print("   ✅ Test patient inserted!")
        else:
            print("\n1️⃣ Test patient already exists ✅")
        
        # Check if doctor exists
        result = db.execute(text("SELECT COUNT(*) FROM hms.doctor WHERE doctor_id = 1"))
        doctor_exists = result.scalar() > 0
        
        if not doctor_exists:
            print("\n2️⃣ Inserting test doctor...")
            
            # First check if user_id = 2 exists for doctor
            result = db.execute(text("SELECT COUNT(*) FROM hms.users WHERE user_id = 2"))
            user_exists = result.scalar() > 0
            
            if not user_exists:
                # Insert user for doctor
                db.execute(text("""
                    INSERT INTO hms.users (
                        user_id, username, password_hash, email, full_name, status
                    )
                    VALUES (
                        2, 'testdoctor', 'hash123', 'doctor@test.com', 'Dr. Jane Smith', 'active'
                    )
                    ON CONFLICT (user_id) DO NOTHING
                """))
                db.commit()
            
            # Insert doctor
            db.execute(text("""
                INSERT INTO hms.doctor (
                    doctor_id, user_id, first_name, last_name, 
                    license_number, phone_number, email, is_active
                )
                VALUES (
                    1, 2, 'Jane', 'Smith', 
                    'LIC123', '0987654321', 'doctor@test.com', true
                )
                ON CONFLICT (doctor_id) DO NOTHING
            """))
            db.commit()
            print("   ✅ Test doctor inserted!")
        else:
            print("\n2️⃣ Test doctor already exists ✅")
        
        print("\n" + "=" * 50)
        print("✅ TEST DATA READY!")
        print("=" * 50)
        print("\nYou can now run: python test_appointment_crud.py")
        
    except Exception as e:
        print(f"\n❌ FAILED TO INSERT TEST DATA!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n⚠️  You may need to insert test data manually in the database.")
        print("\n💡 Manual SQL to run in psql:")
        print("""
-- Insert test patient
INSERT INTO hms.patient (patient_id, hospital_id, first_name, last_name, date_of_birth, gender, phone_number, email)
VALUES (1, 'HP001', 'John', 'Doe', '1990-01-01', 'male', '1234567890', 'patient@test.com')
ON CONFLICT (patient_id) DO NOTHING;

-- Insert test user for doctor
INSERT INTO hms.users (user_id, username, password_hash, email, full_name, status)
VALUES (2, 'testdoctor', 'hash123', 'doctor@test.com', 'Dr. Jane Smith', 'active')
ON CONFLICT (user_id) DO NOTHING;

-- Insert test doctor
INSERT INTO hms.doctor (doctor_id, user_id, first_name, last_name, license_number, phone_number, email, is_active)
VALUES (1, 2, 'Jane', 'Smith', 'LIC123', '0987654321', 'doctor@test.com', true)
ON CONFLICT (doctor_id) DO NOTHING;
        """)
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()