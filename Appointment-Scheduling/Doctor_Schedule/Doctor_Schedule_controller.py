from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import date
from Doctor_Schedule_config import get_db
from Doctor_Schedule.Doctor_Schedule_service import DoctorScheduleService
from pydantic import BaseModel, Field

router = APIRouter()

# Pydantic models for request validation
class DoctorScheduleCreate(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    day_of_week: str = Field(..., description="Day of week (MONDAY, TUESDAY, etc.)")
    start_time: str = Field(..., description="Start time (HH:MM:SS)")
    end_time: str = Field(..., description="End time (HH:MM:SS)")
    slot_duration: int = Field(..., description="Slot duration in minutes", ge=1, le=480)
    max_patients_per_slot: int = Field(default=1, description="Maximum patients per slot", ge=1, le=50)
    effective_from: str = Field(..., description="Effective from date (YYYY-MM-DD)")
    effective_to: Optional[str] = Field(None, description="Effective to date (YYYY-MM-DD)")
    is_active: bool = Field(default=True, description="Is schedule active")

class DoctorScheduleUpdate(BaseModel):
    day_of_week: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    slot_duration: Optional[int] = Field(None, ge=1, le=480)
    max_patients_per_slot: Optional[int] = Field(None, ge=1, le=50)
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None
    is_active: Optional[bool] = None

class WeeklyScheduleDay(BaseModel):
    start_time: str = Field(..., description="Start time (HH:MM:SS)")
    end_time: str = Field(..., description="End time (HH:MM:SS)")
    slot_duration: int = Field(..., description="Slot duration in minutes", ge=1, le=480)
    max_patients_per_slot: int = Field(default=1, description="Maximum patients per slot", ge=1, le=50)

class BulkWeeklyScheduleCreate(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    effective_from: str = Field(..., description="Effective from date (YYYY-MM-DD)")
    effective_to: Optional[str] = Field(None, description="Effective to date (YYYY-MM-DD)")
    MONDAY: Optional[WeeklyScheduleDay] = None
    TUESDAY: Optional[WeeklyScheduleDay] = None
    WEDNESDAY: Optional[WeeklyScheduleDay] = None
    THURSDAY: Optional[WeeklyScheduleDay] = None
    FRIDAY: Optional[WeeklyScheduleDay] = None
    SATURDAY: Optional[WeeklyScheduleDay] = None
    SUNDAY: Optional[WeeklyScheduleDay] = None


@router.post("/", status_code=201)
def create_schedule(payload: DoctorScheduleCreate, db: Session = Depends(get_db)):
    """
    Create a new doctor schedule
    """
    try:
        schedule = DoctorScheduleService.create_schedule(db, payload.dict())
        return {
            "message": "Doctor schedule created successfully",
            "schedule_id": schedule.schedule_id,
            "schedule": schedule
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/bulk-weekly", status_code=201)
def create_bulk_weekly_schedule(payload: BulkWeeklyScheduleCreate, db: Session = Depends(get_db)):
    """
    Create schedules for multiple days of the week at once
    """
    try:
        from datetime import datetime
        
        effective_from = datetime.strptime(payload.effective_from, "%Y-%m-%d").date()
        effective_to = None
        if payload.effective_to:
            effective_to = datetime.strptime(payload.effective_to, "%Y-%m-%d").date()
        
        weekly_schedule = {}
        for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]:
            day_data = getattr(payload, day, None)
            if day_data:
                weekly_schedule[day] = day_data.dict()
        
        schedules = DoctorScheduleService.bulk_create_weekly_schedule(
            db, payload.doctor_id, weekly_schedule, effective_from, effective_to
        )
        
        return {
            "message": f"Created {len(schedules)} schedules successfully",
            "count": len(schedules),
            "schedules": schedules
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{schedule_id}")
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """
    Get schedule by ID
    """
    try:
        schedule = DoctorScheduleService.get_schedule(db, schedule_id)
        return schedule
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
def list_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List all schedules with pagination
    """
    try:
        schedules = DoctorScheduleService.list_schedules(db, skip, limit)
        return {
            "count": len(schedules),
            "schedules": schedules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}")
def get_doctor_schedules(
    doctor_id: int,
    active_only: bool = Query(False, description="Show only active schedules"),
    db: Session = Depends(get_db)
):
    """
    Get all schedules for a specific doctor
    """
    try:
        schedules = DoctorScheduleService.get_doctor_schedules(db, doctor_id, active_only)
        return {
            "doctor_id": doctor_id,
            "count": len(schedules),
            "schedules": schedules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/weekly")
def get_doctor_weekly_schedule(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get doctor's schedule organized by day of week
    """
    try:
        weekly_schedule = DoctorScheduleService.get_doctor_weekly_schedule(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "weekly_schedule": weekly_schedule
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/day/{day_of_week}")
def get_doctor_schedule_by_day(
    doctor_id: int,
    day_of_week: str,
    db: Session = Depends(get_db)
):
    """
    Get doctor's schedule for a specific day of week
    """
    try:
        schedules = DoctorScheduleService.get_doctor_schedule_by_day(db, doctor_id, day_of_week)
        return {
            "doctor_id": doctor_id,
            "day_of_week": day_of_week.upper(),
            "count": len(schedules),
            "schedules": schedules
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/day/{day_of_week}")
def get_schedules_by_day(day_of_week: str, db: Session = Depends(get_db)):
    """
    Get all schedules for a specific day of week
    """
    try:
        schedules = DoctorScheduleService.get_schedules_by_day(db, day_of_week)
        return {
            "day_of_week": day_of_week.upper(),
            "count": len(schedules),
            "schedules": schedules
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date/{check_date}")
def get_effective_schedule_for_date(
    doctor_id: int,
    check_date: str,
    db: Session = Depends(get_db)
):
    """
    Get doctor's schedule effective for a specific date (YYYY-MM-DD)
    """
    try:
        from datetime import datetime
        date_obj = datetime.strptime(check_date, "%Y-%m-%d").date()
        schedules = DoctorScheduleService.get_effective_schedule_for_date(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "date": check_date,
            "day_of_week": date_obj.strftime("%A"),
            "count": len(schedules),
            "schedules": schedules
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/slots/{check_date}")
def get_available_time_slots(
    doctor_id: int,
    check_date: str,
    db: Session = Depends(get_db)
):
    """
    Get available time slots for a doctor on a specific date
    """
    try:
        from datetime import datetime
        date_obj = datetime.strptime(check_date, "%Y-%m-%d").date()
        slots = DoctorScheduleService.get_available_time_slots(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "date": check_date,
            "day_of_week": date_obj.strftime("%A"),
            "total_slots": len(slots),
            "slots": slots
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date-range")
def get_schedules_by_date_range(
    doctor_id: int,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get schedules within a date range
    """
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        schedules = DoctorScheduleService.get_schedules_by_date_range(db, doctor_id, start, end)
        return {
            "doctor_id": doctor_id,
            "start_date": start_date,
            "end_date": end_date,
            "count": len(schedules),
            "schedules": schedules
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/upcoming")
def get_upcoming_schedules(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get upcoming schedules for a doctor (effective_from is in the future)
    """
    try:
        schedules = DoctorScheduleService.get_upcoming_schedules(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "count": len(schedules),
            "schedules": schedules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{schedule_id}")
def update_schedule(
    schedule_id: int,
    payload: DoctorScheduleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing schedule
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        schedule = DoctorScheduleService.update_schedule(db, schedule_id, update_data)
        return {
            "message": "Schedule updated successfully",
            "schedule": schedule
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{schedule_id}/activate")
def activate_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """
    Activate a deactivated schedule
    """
    try:
        schedule = DoctorScheduleService.activate_schedule(db, schedule_id)
        return {
            "message": "Schedule activated successfully",
            "schedule": schedule
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{schedule_id}/deactivate")
def deactivate_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """
    Deactivate an active schedule
    """
    try:
        schedule = DoctorScheduleService.deactivate_schedule(db, schedule_id)
        return {
            "message": "Schedule deactivated successfully",
            "schedule": schedule
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    soft_delete: bool = Query(True, description="Soft delete (deactivate) or hard delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a schedule (soft delete by default)
    """
    try:
        DoctorScheduleService.delete_schedule(db, schedule_id, soft_delete)
        return {
            "message": f"Schedule {'deactivated' if soft_delete else 'deleted'} successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/expire-old-schedules")
def expire_old_schedules(db: Session = Depends(get_db)):
    """
    Deactivate expired schedules (maintenance endpoint)
    """
    try:
        count = DoctorScheduleService.expire_old_schedules(db)
        return {
            "message": f"Expired {count} schedules successfully",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
