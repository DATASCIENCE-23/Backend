from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from Blocked_Slots.Blocked_Slots_config import get_db
from Blocked_Slots.Blocked_Slots_service import BlockedSlotService
from pydantic import BaseModel, Field

router = APIRouter()

# Pydantic models for request validation
class BlockedSlotCreate(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    blocked_date: str = Field(..., description="Blocked date (YYYY-MM-DD)")
    start_time: str = Field(..., description="Start time (HH:MM:SS)")
    end_time: str = Field(..., description="End time (HH:MM:SS)")
    reason: str = Field(..., description="Reason for blocking")
    created_by: int = Field(..., description="User ID who is creating the block")

class BlockedSlotUpdate(BaseModel):
    blocked_date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    reason: Optional[str] = None

class FullDayBlock(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    blocked_date: str = Field(..., description="Date to block (YYYY-MM-DD)")
    reason: str = Field(..., description="Reason for blocking")
    created_by: int = Field(..., description="User ID who is creating the block")

class MultipleDaysBlock(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    reason: str = Field(..., description="Reason for blocking (e.g., Vacation)")
    created_by: int = Field(..., description="User ID who is creating the block")

class TimeSlotCheck(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    check_date: str = Field(..., description="Date to check (YYYY-MM-DD)")
    start_time: str = Field(..., description="Start time (HH:MM:SS)")
    end_time: str = Field(..., description="End time (HH:MM:SS)")


@router.post("/", status_code=201)
def create_blocked_slot(payload: BlockedSlotCreate, db: Session = Depends(get_db)):
    try:
        blocked_slot = BlockedSlotService.create_blocked_slot(db, payload.dict())
        return {
            "message": "Blocked slot created successfully",
            "blocked_slot_id": blocked_slot.blocked_slot_id,
            "blocked_slot": blocked_slot
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/block-full-day", status_code=201)
def block_full_day(payload: FullDayBlock, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        blocked_date = datetime.strptime(payload.blocked_date, "%Y-%m-%d").date()
        blocked_slot = BlockedSlotService.block_full_day(
            db, payload.doctor_id, blocked_date, payload.reason, payload.created_by
        )
        return {
            "message": "Full day blocked successfully",
            "blocked_slot_id": blocked_slot.blocked_slot_id,
            "blocked_slot": blocked_slot
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/block-multiple-days", status_code=201)
def block_multiple_days(payload: MultipleDaysBlock, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        start_date = datetime.strptime(payload.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(payload.end_date, "%Y-%m-%d").date()
        blocked_slots = BlockedSlotService.block_multiple_days(
            db, payload.doctor_id, start_date, end_date, payload.reason, payload.created_by
        )
        return {
            "message": f"Blocked {len(blocked_slots)} days successfully",
            "count": len(blocked_slots),
            "blocked_slots": blocked_slots
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{blocked_slot_id}")
def get_blocked_slot(blocked_slot_id: int, db: Session = Depends(get_db)):
    try:
        return BlockedSlotService.get_blocked_slot(db, blocked_slot_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
def list_blocked_slots(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        blocked_slots = BlockedSlotService.list_blocked_slots(db, skip, limit)
        return {"count": len(blocked_slots), "blocked_slots": blocked_slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}")
def get_doctor_blocked_slots(doctor_id: int, db: Session = Depends(get_db)):
    try:
        blocked_slots = BlockedSlotService.get_doctor_blocked_slots(db, doctor_id)
        return {"doctor_id": doctor_id, "count": len(blocked_slots), "blocked_slots": blocked_slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/upcoming")
def get_upcoming_blocked_slots(doctor_id: int, db: Session = Depends(get_db)):
    try:
        blocked_slots = BlockedSlotService.get_upcoming_blocked_slots(db, doctor_id)
        return {"doctor_id": doctor_id, "count": len(blocked_slots), "blocked_slots": blocked_slots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/summary")
def get_blocked_slots_summary(doctor_id: int, db: Session = Depends(get_db)):
    try:
        return BlockedSlotService.get_blocked_slots_summary(db, doctor_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date/{blocked_date}")
def get_doctor_blocked_slots_by_date(doctor_id: int, blocked_date: str, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        date_obj = datetime.strptime(blocked_date, "%Y-%m-%d").date()
        blocked_slots = BlockedSlotService.get_doctor_blocked_slots_by_date(db, doctor_id, date_obj)
        return {"doctor_id": doctor_id, "date": blocked_date, "count": len(blocked_slots), "blocked_slots": blocked_slots}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/date/{blocked_date}")
def get_blocked_slots_by_date(blocked_date: str, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        date_obj = datetime.strptime(blocked_date, "%Y-%m-%d").date()
        blocked_slots = BlockedSlotService.get_blocked_slots_by_date(db, date_obj)
        return {"date": blocked_date, "count": len(blocked_slots), "blocked_slots": blocked_slots}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date-range")
def get_blocked_slots_by_date_range(
    doctor_id: int,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        blocked_slots = BlockedSlotService.get_blocked_slots_by_date_range(db, doctor_id, start, end)
        return {"doctor_id": doctor_id, "start_date": start_date, "end_date": end_date,
                "count": len(blocked_slots), "blocked_slots": blocked_slots}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/blocked-dates")
def get_blocked_dates_in_range(
    doctor_id: int,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        blocked_dates = BlockedSlotService.get_blocked_dates_in_range(db, doctor_id, start, end)
        return {"doctor_id": doctor_id, "start_date": start_date, "end_date": end_date,
                "count": len(blocked_dates), "blocked_dates": blocked_dates}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ✅ FIXED FUNCTION — year & month are PATH params (not Query)
@router.get("/doctor/{doctor_id}/month/{year}/{month}")
def get_doctor_availability_for_month(
    doctor_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    try:
        availability = BlockedSlotService.get_doctor_availability_for_month(db, doctor_id, year, month)
        return availability
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/check-blocked")
def check_time_slot_blocked(payload: TimeSlotCheck, db: Session = Depends(get_db)):
    try:
        from datetime import datetime
        check_date = datetime.strptime(payload.check_date, "%Y-%m-%d").date()
        start_time = datetime.strptime(payload.start_time, "%H:%M:%S").time()
        end_time = datetime.strptime(payload.end_time, "%H:%M:%S").time()
        return BlockedSlotService.is_time_slot_blocked(
            db, payload.doctor_id, check_date, start_time, end_time
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{blocked_slot_id}")
def update_blocked_slot(blocked_slot_id: int, payload: BlockedSlotUpdate, db: Session = Depends(get_db)):
    try:
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        blocked_slot = BlockedSlotService.update_blocked_slot(db, blocked_slot_id, update_data)
        return {"message": "Blocked slot updated successfully", "blocked_slot": blocked_slot}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{blocked_slot_id}")
def delete_blocked_slot(blocked_slot_id: int, db: Session = Depends(get_db)):
    try:
        BlockedSlotService.delete_blocked_slot(db, blocked_slot_id)
        return {"message": "Blocked slot deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/doctor/{doctor_id}/cancel-range")
def cancel_blocked_slots_in_range(
    doctor_id: int,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        count = BlockedSlotService.cancel_blocked_slots_in_range(db, doctor_id, start, end)
        return {"message": f"Cancelled {count} blocked slot(s) successfully", "count": count}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/cleanup-old-slots")
def cleanup_old_blocked_slots(
    days_to_keep: int = Query(90, ge=1, le=365, description="Number of days to keep"),
    db: Session = Depends(get_db)
):
    try:
        count = BlockedSlotService.delete_past_blocked_slots(db, days_to_keep)
        return {"message": f"Cleaned up {count} old blocked slot(s)", "count": count, "days_kept": days_to_keep}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
