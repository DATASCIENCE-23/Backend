from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from Waiting_List_config import get_db
from Waiting_List.Waiting_List_service import WaitingListService
from pydantic import BaseModel, Field

router = APIRouter()

# Pydantic models for request validation
class WaitingListCreate(BaseModel):
    patient_id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Doctor ID")
    preferred_date: str = Field(..., description="Preferred date (YYYY-MM-DD)")
    preferred_time_start: str = Field(..., description="Preferred start time (HH:MM:SS)")
    preferred_time_end: str = Field(..., description="Preferred end time (HH:MM:SS)")
    reason: Optional[str] = Field(None, description="Reason for waiting list")
    expiry_days: Optional[int] = Field(7, description="Days until entry expires", ge=1, le=30)

class WaitingListUpdate(BaseModel):
    preferred_date: Optional[str] = None
    preferred_time_start: Optional[str] = None
    preferred_time_end: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None

class BulkCancel(BaseModel):
    waiting_ids: List[int] = Field(..., description="List of waiting IDs to cancel")


@router.post("/", status_code=201)
def create_waiting_entry(payload: WaitingListCreate, db: Session = Depends(get_db)):
    """
    Create a new waiting list entry
    """
    try:
        waiting_entry = WaitingListService.create_waiting_entry(db, payload.dict())
        return {
            "message": "Waiting list entry created successfully",
            "waiting_id": waiting_entry.waiting_id,
            "waiting_entry": waiting_entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{waiting_id}")
def get_waiting_entry(waiting_id: int, db: Session = Depends(get_db)):
    """
    Get waiting list entry by ID
    """
    try:
        waiting_entry = WaitingListService.get_waiting_entry(db, waiting_id)
        return waiting_entry
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
def list_waiting_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List all waiting list entries with pagination
    """
    try:
        waiting_entries = WaitingListService.list_waiting_entries(db, skip, limit)
        return {
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/patient/{patient_id}")
def get_patient_waiting_entries(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all waiting list entries for a specific patient
    """
    try:
        waiting_entries = WaitingListService.get_patient_waiting_entries(db, patient_id)
        return {
            "patient_id": patient_id,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/patient/{patient_id}/active-count")
def get_patient_active_count(patient_id: int, db: Session = Depends(get_db)):
    """
    Get count of active waiting list entries for a patient
    """
    try:
        count = WaitingListService.get_patient_active_count(db, patient_id)
        return {
            "patient_id": patient_id,
            "active_count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}")
def get_doctor_waiting_entries(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get all waiting list entries for a specific doctor
    """
    try:
        waiting_entries = WaitingListService.get_doctor_waiting_entries(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/active")
def get_doctor_active_entries(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get all active waiting list entries for a doctor
    """
    try:
        waiting_entries = WaitingListService.get_active_entries(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/notified")
def get_doctor_notified_entries(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get all notified waiting list entries for a doctor
    """
    try:
        waiting_entries = WaitingListService.get_notified_entries(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/statistics")
def get_doctor_waiting_statistics(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get waiting list statistics for a doctor
    """
    try:
        statistics = WaitingListService.get_waiting_statistics(db, doctor_id)
        return statistics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date/{preferred_date}")
def get_entries_by_date(
    doctor_id: int,
    preferred_date: str,
    db: Session = Depends(get_db)
):
    """
    Get waiting list entries for a doctor on a specific date (YYYY-MM-DD)
    """
    try:
        from datetime import datetime
        date_obj = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        waiting_entries = WaitingListService.get_entries_by_date(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "preferred_date": preferred_date,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date/{preferred_date}/priority")
def get_priority_entries_by_date(
    doctor_id: int,
    preferred_date: str,
    db: Session = Depends(get_db)
):
    """
    Get waiting list entries sorted by priority for a specific date
    """
    try:
        from datetime import datetime
        date_obj = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        waiting_entries = WaitingListService.get_priority_entries(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "preferred_date": preferred_date,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date-range")
def get_entries_by_date_range(
    doctor_id: int,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get waiting list entries for a doctor within a date range
    """
    try:
        from datetime import datetime
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        waiting_entries = WaitingListService.get_entries_by_date_range(db, doctor_id, start, end)
        return {
            "doctor_id": doctor_id,
            "start_date": start_date,
            "end_date": end_date,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/active")
def get_all_active_entries(
    doctor_id: Optional[int] = Query(None, description="Filter by doctor ID"),
    db: Session = Depends(get_db)
):
    """
    Get all active waiting list entries (optionally filtered by doctor)
    """
    try:
        waiting_entries = WaitingListService.get_active_entries(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "count": len(waiting_entries),
            "waiting_entries": waiting_entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{waiting_id}")
def update_waiting_entry(
    waiting_id: int,
    payload: WaitingListUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing waiting list entry
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        waiting_entry = WaitingListService.update_waiting_entry(db, waiting_id, update_data)
        return {
            "message": "Waiting list entry updated successfully",
            "waiting_entry": waiting_entry
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{waiting_id}/notify")
def notify_patient(waiting_id: int, db: Session = Depends(get_db)):
    """
    Mark waiting list entry as notified
    """
    try:
        waiting_entry = WaitingListService.notify_patient(db, waiting_id)
        return {
            "message": "Patient notified successfully",
            "waiting_entry": waiting_entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{waiting_id}/accept")
def accept_entry(waiting_id: int, db: Session = Depends(get_db)):
    """
    Mark waiting list entry as accepted
    """
    try:
        waiting_entry = WaitingListService.accept_entry(db, waiting_id)
        return {
            "message": "Waiting list entry accepted",
            "waiting_entry": waiting_entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{waiting_id}/decline")
def decline_entry(waiting_id: int, db: Session = Depends(get_db)):
    """
    Mark waiting list entry as declined
    """
    try:
        waiting_entry = WaitingListService.decline_entry(db, waiting_id)
        return {
            "message": "Waiting list entry declined",
            "waiting_entry": waiting_entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{waiting_id}/cancel")
def cancel_entry(waiting_id: int, db: Session = Depends(get_db)):
    """
    Cancel a waiting list entry
    """
    try:
        waiting_entry = WaitingListService.cancel_entry(db, waiting_id)
        return {
            "message": "Waiting list entry cancelled",
            "waiting_entry": waiting_entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/bulk-cancel")
def bulk_cancel_entries(payload: BulkCancel, db: Session = Depends(get_db)):
    """
    Cancel multiple waiting list entries at once
    """
    try:
        count = WaitingListService.bulk_cancel_entries(db, payload.waiting_ids)
        return {
            "message": f"Cancelled {count} waiting list entries",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{waiting_id}")
def delete_waiting_entry(waiting_id: int, db: Session = Depends(get_db)):
    """
    Delete a waiting list entry
    """
    try:
        WaitingListService.delete_waiting_entry(db, waiting_id)
        return {"message": "Waiting list entry deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/expire-old-entries")
def expire_old_entries(db: Session = Depends(get_db)):
    """
    Mark expired waiting list entries as EXPIRED (maintenance endpoint)
    """
    try:
        count = WaitingListService.expire_old_entries(db)
        return {
            "message": f"Expired {count} waiting list entries",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")