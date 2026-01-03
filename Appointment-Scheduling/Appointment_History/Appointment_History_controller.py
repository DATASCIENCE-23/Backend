from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from Appointment_History_config import get_db
from Appointment_History.Appointment_History_service import AppointmentHistoryService
from pydantic import BaseModel, Field

router = APIRouter()

# Pydantic models
class HistoryCreate(BaseModel):
    appointment_id: int = Field(..., description="Appointment ID")
    changed_by: int = Field(..., description="User ID who made the change")
    change_type: str = Field(..., description="Type of change")
    old_date: Optional[str] = Field(None, description="Old date (YYYY-MM-DD)")
    new_date: Optional[str] = Field(None, description="New date (YYYY-MM-DD)")
    old_time: Optional[str] = Field(None, description="Old time (HH:MM:SS)")
    new_time: Optional[str] = Field(None, description="New time (HH:MM:SS)")
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    change_reason: Optional[str] = None


@router.post("/", status_code=201)
def create_history_record(payload: HistoryCreate, db: Session = Depends(get_db)):
    """Create a new history record"""
    try:
        history = AppointmentHistoryService.create_history_record(db, payload.dict())
        return {
            "message": "History record created successfully",
            "history_id": history.history_id,
            "history": history
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{history_id}")
def get_history_record(history_id: int, db: Session = Depends(get_db)):
    """Get history record by ID"""
    try:
        history = AppointmentHistoryService.get_history_record(db, history_id)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
def list_history_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all history records"""
    try:
        records = AppointmentHistoryService.list_history_records(db, skip, limit)
        return {"count": len(records), "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/appointment/{appointment_id}")
def get_appointment_history(appointment_id: int, db: Session = Depends(get_db)):
    """Get all history records for an appointment"""
    try:
        records = AppointmentHistoryService.get_appointment_history(db, appointment_id)
        return {"appointment_id": appointment_id, "count": len(records), "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/appointment/{appointment_id}/timeline")
def get_appointment_timeline(appointment_id: int, db: Session = Depends(get_db)):
    """Get chronological timeline for an appointment"""
    try:
        timeline = AppointmentHistoryService.get_appointment_timeline(db, appointment_id)
        return {"appointment_id": appointment_id, "timeline": timeline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/appointment/{appointment_id}/summary")
def get_appointment_summary(appointment_id: int, db: Session = Depends(get_db)):
    """Get summary of changes for an appointment"""
    try:
        summary = AppointmentHistoryService.get_appointment_summary(db, appointment_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/appointment/{appointment_id}/reschedules")
def get_reschedule_history(appointment_id: int, db: Session = Depends(get_db)):
    """Get all reschedule records"""
    try:
        records = AppointmentHistoryService.get_reschedule_history(db, appointment_id)
        return {"appointment_id": appointment_id, "reschedules": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/change-type/{change_type}")
def get_by_change_type(change_type: str, db: Session = Depends(get_db)):
    """Get history records by change type"""
    try:
        records = AppointmentHistoryService.get_by_change_type(db, change_type)
        return {"change_type": change_type, "count": len(records), "records": records}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/user/{user_id}")
def get_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all changes made by a user"""
    try:
        records = AppointmentHistoryService.get_by_user(db, user_id)
        return {"user_id": user_id, "count": len(records), "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/recent")
def get_recent_changes(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get recent history records"""
    try:
        records = AppointmentHistoryService.get_recent_changes(db, limit)
        return {"count": len(records), "records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """Get overall history statistics"""
    try:
        stats = AppointmentHistoryService.get_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{history_id}")
def delete_history_record(history_id: int, db: Session = Depends(get_db)):
    """Delete a history record"""
    try:
        AppointmentHistoryService.delete_history_record(db, history_id)
        return {"message": "History record deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/cleanup")
def cleanup_old_records(
    days_to_keep: int = Query(1825, ge=1, description="Days to keep"),
    db: Session = Depends(get_db)
):
    """Cleanup old history records"""
    try:
        count = AppointmentHistoryService.cleanup_old_records(db, days_to_keep)
        return {"message": f"Cleaned up {count} old records", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")