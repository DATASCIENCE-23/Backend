"""
Test CRUD operations for Appointment entity
"""
from datetime import date, time, datetime
from Appointment.Appointment_service import AppointmentService
from Appointment.Appointment_config import get_db

def test_appointment_crud():
    """Test Create, Read, Update, Delete for Appointment"""
    print("=" * 50)
    print("🧪 TESTING APPOINTMENT CRUD")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # TEST 1: CREATE APPOINTMENT
        print("\n1️⃣ Testing CREATE Appointment...")
        
        appointment_data = {
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_date": "2026-02-10",
            "start_time": "10:00:00",
            "end_time": "10:30:00",
            "appointment_type": "opd",
            "reason_for_visit": "Regular checkup",
            "consultation_fee": 500.00
        }
        
        appointment = AppointmentService.create_appointment(db, appointment_data)
        print(f"✅ Appointment created successfully!")
        print(f"   ID: {appointment.appointment_id}")
        print(f"   Date: {appointment.appointment_date}")
        print(f"   Time: {appointment.start_time} - {appointment.end_time}")
        print(f"   Type: {appointment.appointment_type.value}")
        print(f"   Status: {appointment.status.value}")
        
        appointment_id = appointment.appointment_id
        
        # TEST 2: READ APPOINTMENT
        print("\n2️⃣ Testing READ Appointment...")
        
        read_appointment = AppointmentService.get_appointment(db, appointment_id)
        print(f"✅ Appointment retrieved successfully!")
        print(f"   Patient ID: {read_appointment.patient_id}")
        print(f"   Doctor ID: {read_appointment.doctor_id}")
        print(f"   Status: {read_appointment.status.value}")
        
        # TEST 3: UPDATE APPOINTMENT
        print("\n3️⃣ Testing UPDATE Appointment...")
        
        update_data = {
            "reason_for_visit": "Updated: Follow-up consultation",
            "consultation_fee": 750.00
        }
        
        updated_appointment = AppointmentService.update_appointment(db, appointment_id, update_data)
        print(f"✅ Appointment updated successfully!")
        print(f"   New Reason: {updated_appointment.reason_for_visit}")
        print(f"   New Fee: {updated_appointment.consultation_fee}")
        
        # TEST 4: COMPLETE APPOINTMENT
        print("\n4️⃣ Testing COMPLETE Appointment...")
        
        completed = AppointmentService.complete_appointment(db, appointment_id)
        print(f"✅ Appointment marked as completed!")
        print(f"   Status: {completed.status.value}")
        
        # TEST 5: DELETE APPOINTMENT
        print("\n5️⃣ Testing DELETE Appointment...")
        
        AppointmentService.delete_appointment(db, appointment_id)
        print(f"✅ Appointment deleted successfully!")
        
        print("\n" + "=" * 50)
        print("✅ ALL APPOINTMENT TESTS PASSED!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_appointment_crud()