"""
Test database connection for all entities
"""

from sqlalchemy import text

from Appointment.Appointment_config import (
    get_db as get_appointment_db,
    Base as AppointmentBase,
    engine as appointment_engine
)

from Doctor_Schedule.Doctor_Schedule_config import (
    get_db as get_schedule_db,
    Base as ScheduleBase,
    engine as schedule_engine
)

from Blocked_Slots.Blocked_Slots_config import (
    get_db as get_blocked_db,
    Base as BlockedBase,
    engine as blocked_engine
)


def test_database_connection():
    """Test if database connection works"""
    print("=" * 50)
    print("🔍 TESTING DATABASE CONNECTIONS")
    print("=" * 50)

    # ---------------- Appointment DB ----------------
    try:
        db = next(get_appointment_db())
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Appointment Database: CONNECTED")
    except Exception as e:
        print("❌ Appointment Database: FAILED")
        print(f"   Error: {str(e)}")
        return False

    # ---------------- Doctor Schedule DB ----------------
    try:
        db = next(get_schedule_db())
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Doctor Schedule Database: CONNECTED")
    except Exception as e:
        print("❌ Doctor Schedule Database: FAILED")
        print(f"   Error: {str(e)}")
        return False

    # ---------------- Blocked Slots DB ----------------
    try:
        db = next(get_blocked_db())
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Blocked Slots Database: CONNECTED")
    except Exception as e:
        print("❌ Blocked Slots Database: FAILED")
        print(f"   Error: {str(e)}")
        return False

    print("=" * 50)
    print("🎉 ALL DATABASE CONNECTIONS SUCCESSFUL!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    test_database_connection()
