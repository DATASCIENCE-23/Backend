"""
Test CRUD operations for Doctor_Schedule entity
"""
from datetime import date, time, datetime
from Doctor_Schedule.Doctor_Schedule_service import DoctorScheduleService
from Doctor_Schedule.Doctor_Schedule_config import get_db

def test_doctor_schedule_crud():
    """Test Create, Read, Update, Delete for Doctor Schedule"""
    print("=" * 50)
    print("🧪 TESTING DOCTOR SCHEDULE CRUD")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        # STEP 0: Check if doctor_id=1 exists
        print("\n0️⃣ Checking if test doctor exists...")
        from sqlalchemy import text
        result = db.execute(text("SELECT COUNT(*) FROM hms.doctor WHERE doctor_id = 1"))
        doctor_count = result.scalar()
        print(f"   Doctors with ID 1: {doctor_count}")
        
        if doctor_count == 0:
            print("\n⚠️  WARNING: You need doctor_id=1 in database!")
            print("   Please insert test data first or run insert_test_data.py")
            return
        
        # TEST 1: CREATE SCHEDULE
        print("\n1️⃣ Testing CREATE Doctor Schedule...")
        
        schedule_data = {
            "doctor_id": 1,
            "day_of_week": "mon",  # Match DB enum: mon, tue, wed, thu, fri, sat, sun
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "slot_duration": 30,  # minutes
            "max_patients_per_slot": 2,
            "effective_from": "2026-01-01"
        }
        
        schedule = DoctorScheduleService.create_schedule(db, schedule_data)
        print(f"✅ Schedule created successfully!")
        print(f"   ID: {schedule.schedule_id}")
        print(f"   Doctor ID: {schedule.doctor_id}")
        print(f"   Day: {schedule.day_of_week.value}")
        print(f"   Time: {schedule.start_time} - {schedule.end_time}")
        print(f"   Slot Duration: {schedule.slot_duration} minutes")
        print(f"   Max Patients: {schedule.max_patients_per_slot}")
        print(f"   Active: {schedule.is_active}")
        
        schedule_id = schedule.schedule_id
        
        # TEST 2: READ SCHEDULE
        print("\n2️⃣ Testing READ Doctor Schedule...")
        
        read_schedule = DoctorScheduleService.get_schedule(db, schedule_id)
        print(f"✅ Schedule retrieved successfully!")
        print(f"   Doctor ID: {read_schedule.doctor_id}")
        print(f"   Day: {read_schedule.day_of_week.value}")
        print(f"   Effective From: {read_schedule.effective_from}")
        
        # TEST 3: GET DOCTOR'S ALL SCHEDULES
        print("\n3️⃣ Testing GET ALL Doctor's Schedules...")
        
        all_schedules = DoctorScheduleService.get_doctor_schedules(db, 1)
        print(f"✅ Retrieved {len(all_schedules)} schedules for doctor")
        
        # TEST 4: GET SCHEDULES BY DAY
        print("\n4️⃣ Testing GET Schedules by Day...")
        
        monday_schedules = DoctorScheduleService.get_schedules_by_day(db, 1, "mon")
        print(f"✅ Retrieved {len(monday_schedules)} Monday schedules")
        
        # TEST 5: UPDATE SCHEDULE
        print("\n5️⃣ Testing UPDATE Doctor Schedule...")
        
        update_data = {
            "slot_duration": 45,
            "max_patients_per_slot": 3
        }
        
        updated_schedule = DoctorScheduleService.update_schedule(db, schedule_id, update_data)
        print(f"✅ Schedule updated successfully!")
        print(f"   New Slot Duration: {updated_schedule.slot_duration} minutes")
        print(f"   New Max Patients: {updated_schedule.max_patients_per_slot}")
        
        # TEST 6: GET SUMMARY
        print("\n6️⃣ Testing GET Doctor Schedule Summary...")
        
        summary = DoctorScheduleService.get_doctor_schedule_summary(db, 1)
        print(f"✅ Summary retrieved successfully!")
        print(f"   Total Active Schedules: {summary['total_schedules']}")
        print(f"   Monday Schedules: {summary['schedules_by_day']['mon']}")
        
        # TEST 7: DEACTIVATE SCHEDULE
        print("\n7️⃣ Testing DEACTIVATE Schedule...")
        
        deactivated = DoctorScheduleService.deactivate_schedule(db, schedule_id)
        print(f"✅ Schedule deactivated!")
        print(f"   Active: {deactivated.is_active}")
        
        # TEST 8: DELETE SCHEDULE
        print("\n8️⃣ Testing DELETE Schedule...")
        
        DoctorScheduleService.delete_schedule(db, schedule_id)
        print(f"✅ Schedule deleted successfully!")
        
        print("\n" + "=" * 50)
        print("✅ ALL DOCTOR SCHEDULE TESTS PASSED!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_doctor_schedule_crud()