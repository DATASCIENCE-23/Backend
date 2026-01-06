from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from Appointment_History.Appointment_History_config import get_db
from Appointment_History.Appointment_History_service import AppointmentHistoryService
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/appointment-history",
    tags=["Appointment History"]
)

# ================= Pydantic Schemas =================

class HistoryCreate(BaseModel):
    appointment_id: int
    changed_by: int
    change_type: str
    old_date: Optional[str] = None
    new_date: Optional[str] = None
    old_time: Optional[str] = None
    new_time: Optional[str] = None
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    change_reason: Optional[str] = None


# ================= CREATE =================

@router.post("/", status_code=201)
def create_history_record(
    payload: HistoryCreate,
    db: Session = Depends(get_db)
):
    try:
        history = AppointmentHistoryService.create_history_record(
            db, payload.dict()
        )
        return {
            "message": "History record created successfully",
            "history_id": history.history_id,
            "history": history
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================= READ =================

@router.get("/{history_id}")
def get_history_record(history_id: int, db: Session = Depends(get_db)):
    try:
        return AppointmentHistoryService.get_history_record(db, history_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_history_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    records = AppointmentHistoryService.list_history_records(db, skip, limit)
    return {
        "count": len(records),
        "records": records
    }


@router.get("/appointment/{appointment_id}")
def get_appointment_history(appointment_id: int, db: Session = Depends(get_db)):
    records = AppointmentHistoryService.get_appointment_history(
        db, appointment_id
    )
    return {
        "appointment_id": appointment_id,
        "count": len(records),
        "records": records
    }


@router.get("/appointment/{appointment_id}/timeline")
def get_appointment_timeline(appointment_id: int, db: Session = Depends(get_db)):
    return {
        "appointment_id": appointment_id,
        "timeline": AppointmentHistoryService.get_appointment_timeline(
            db, appointment_id
        )
    }


@router.get("/appointment/{appointment_id}/summary")
def get_appointment_summary(appointment_id: int, db: Session = Depends(get_db)):
    return AppointmentHistoryService.get_appointment_summary(
        db, appointment_id
    )


@router.get("/appointment/{appointment_id}/reschedules")
def get_reschedule_history(appointment_id: int, db: Session = Depends(get_db)):
    return {
        "appointment_id": appointment_id,
        "reschedules": AppointmentHistoryService.get_reschedule_history(
            db, appointment_id
        )
    }


@router.get("/change-type/{change_type}")
def get_by_change_type(change_type: str, db: Session = Depends(get_db)):
    try:
        records = AppointmentHistoryService.get_by_change_type(
            db, change_type
        )
        return {
            "change_type": change_type,
            "count": len(records),
            "records": records
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}")
def get_by_user(user_id: int, db: Session = Depends(get_db)):
    records = AppointmentHistoryService.get_by_user(db, user_id)
    return {
        "user_id": user_id,
        "count": len(records),
        "records": records
    }


@router.get("/recent")
def get_recent_changes(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    records = AppointmentHistoryService.get_recent_changes(db, limit)
    return {
        "count": len(records),
        "records": records
    }


@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    return AppointmentHistoryService.get_statistics(db)


# ================= DELETE / MAINTENANCE =================

@router.delete("/{history_id}")
def delete_history_record(history_id: int, db: Session = Depends(get_db)):
    try:
        AppointmentHistoryService.delete_history_record(db, history_id)
        return {"message": "History record deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/cleanup")
def cleanup_old_records(
    days_to_keep: int = Query(1825, ge=1),
    db: Session = Depends(get_db)
):
    count = AppointmentHistoryService.cleanup_old_records(
        db, days_to_keep
    )
    return {
        "message": f"Cleaned up {count} old records",
        "count": count
    }
