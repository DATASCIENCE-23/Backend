"""
Test CRUD operations for Blocked_Slots entity
"""
from datetime import date, time, datetime
from Blocked_Slots.Blocked_Slots_service import BlockedSlotService
from Blocked_Slots.Blocked_Slots_config import get_db

def test_blocked_slots_crud():
    """Test Create, Read, Update, Delete for Blocked Slots"""
    print("=" * 50)
    print("🧪 TESTING BLOCKED SLOTS CRUD")
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
        
        # TEST 1: CREATE BLOCKED SLOT
        print("\n1️⃣ Testing CREATE Blocked Slot...")
        
        blocked_data = {
            "doctor_id": 1,
            "blocked_date": "2026-02-15",
            "start_time": "14:00:00",
            "end_time": "16:00:00",
            "reason": "Medical conference",
            "created_by": 2  # Changed from 1 to 2 (doctor's user_id)
        }
        
        blocked_slot = BlockedSlotService.create_blocked_slot(db, blocked_data)
        print(f"✅ Blocked slot created successfully!")
        print(f"   ID: {blocked_slot.blocked_slot_id}")
        print(f"   Doctor ID: {blocked_slot.doctor_id}")
        print(f"   Date: {blocked_slot.blocked_date}")
        print(f"   Time: {blocked_slot.start_time} - {blocked_slot.end_time}")
        print(f"   Reason: {blocked_slot.reason}")
        
        blocked_slot_id = blocked_slot.blocked_slot_id
        
        # TEST 2: READ BLOCKED SLOT
        print("\n2️⃣ Testing READ Blocked Slot...")
        
        read_slot = BlockedSlotService.get_blocked_slot(db, blocked_slot_id)
        print(f"✅ Blocked slot retrieved successfully!")
        print(f"   Created At: {read_slot.created_at}")
        print(f"   Created By: {read_slot.created_by}")
        
        # TEST 3: BLOCK FULL DAY
        print("\n3️⃣ Testing BLOCK FULL DAY...")
        
        full_day_slot = BlockedSlotService.block_full_day(
            db, 1, date(2026, 2, 20), "Doctor's day off", 2  # Changed to user_id=2
        )
        print(f"✅ Full day blocked successfully!")
        print(f"   ID: {full_day_slot.blocked_slot_id}")
        print(f"   Date: {full_day_slot.blocked_date}")
        print(f"   Time: {full_day_slot.start_time} - {full_day_slot.end_time}")
        
        # TEST 4: CHECK IF TIME SLOT IS BLOCKED
        print("\n4️⃣ Testing CHECK If Time Slot Is Blocked...")
        
        check_result = BlockedSlotService.is_time_slot_blocked(
            db, 1, date(2026, 2, 15), time(14, 30), time(15, 30)
        )
        print(f"✅ Time slot check completed!")
        print(f"   Is Blocked: {check_result['is_blocked']}")
        if check_result['is_blocked']:
            print(f"   Reasons: {', '.join(check_result['reasons'])}")
        
        # TEST 5: GET DOCTOR'S BLOCKED SLOTS
        print("\n5️⃣ Testing GET Doctor's Blocked Slots...")
        
        all_blocked = BlockedSlotService.get_doctor_blocked_slots(db, 1)
        print(f"✅ Retrieved {len(all_blocked)} blocked slots for doctor")
        
        # TEST 6: GET UPCOMING BLOCKED SLOTS
        print("\n6️⃣ Testing GET Upcoming Blocked Slots...")
        
        upcoming = BlockedSlotService.get_upcoming_blocked_slots(db, 1)
        print(f"✅ Retrieved {len(upcoming)} upcoming blocked slots")
        
        # TEST 7: UPDATE BLOCKED SLOT
        print("\n7️⃣ Testing UPDATE Blocked Slot...")
        
        update_data = {
            "reason": "Updated: Important medical seminar",
            "end_time": "17:00:00"
        }
        
        updated_slot = BlockedSlotService.update_blocked_slot(db, blocked_slot_id, update_data)
        print(f"✅ Blocked slot updated successfully!")
        print(f"   New Reason: {updated_slot.reason}")
        print(f"   New End Time: {updated_slot.end_time}")
        
        # TEST 8: GET SUMMARY
        print("\n8️⃣ Testing GET Blocked Slots Summary...")
        
        summary = BlockedSlotService.get_blocked_slots_summary(db, 1)
        print(f"✅ Summary retrieved successfully!")
        print(f"   Total Blocked Slots: {summary['total_blocked_slots']}")
        print(f"   Upcoming Blocked Slots: {summary['upcoming_blocked_slots']}")
        print(f"   Next Blocked Date: {summary['next_blocked_date']}")
        
        # TEST 9: GET MONTH AVAILABILITY
        print("\n9️⃣ Testing GET Month Availability...")
        
        month_data = BlockedSlotService.get_doctor_availability_for_month(db, 1, 2026, 2)
        print(f"✅ Month availability retrieved!")
        print(f"   Year/Month: {month_data['year']}/{month_data['month']}")
        print(f"   Total Blocked Slots: {month_data['total_blocked_slots']}")
        print(f"   Blocked Dates: {len(month_data['blocked_dates'])} days")
        
        # TEST 10: DELETE BLOCKED SLOTS
        print("\n🔟 Testing DELETE Blocked Slots...")
        
        # Delete the full day block first
        BlockedSlotService.delete_blocked_slot(db, full_day_slot.blocked_slot_id)
        print(f"✅ Full day block deleted!")
        
        # Delete the main test slot
        BlockedSlotService.delete_blocked_slot(db, blocked_slot_id)
        print(f"✅ Blocked slot deleted successfully!")
        
        print("\n" + "=" * 50)
        print("✅ ALL BLOCKED SLOTS TESTS PASSED!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_blocked_slots_crud()