from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from Waiting_List.Waiting_List_config import get_db
from Waiting_List.Waiting_List_service import WaitingListService
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/waiting-list",
    tags=["Waiting List"]
)

# ================= Pydantic Schemas =================

class WaitingListCreate(BaseModel):
    patient_id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Doctor ID")
    preferred_date: str = Field(..., description="Preferred date (YYYY-MM-DD)")
    preferred_time_start: str = Field(..., description="Preferred start time (HH:MM:SS)")
    preferred_time_end: str = Field(..., description="Preferred end time (HH:MM:SS)")
    reason: Optional[str] = Field(None, description="Reason for waiting list")
    expiry_days: Optional[int] = Field(7, ge=1, le=30)


class WaitingListUpdate(BaseModel):
    preferred_date: Optional[str] = None
    preferred_time_start: Optional[str] = None
    preferred_time_end: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None


class BulkCancel(BaseModel):
    waiting_ids: List[int]


# ================= CREATE =================

@router.post("/", status_code=201)
def create_waiting_entry(
    payload: WaitingListCreate,
    db: Session = Depends(get_db)
):
    try:
        entry = WaitingListService.create_waiting_entry(db, payload.dict())
        return {
            "message": "Waiting list entry created successfully",
            "waiting_id": entry.waiting_id,
            "waiting_entry": entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================= READ =================

@router.get("/{waiting_id}")
def get_waiting_entry(waiting_id: int, db: Session = Depends(get_db)):
    try:
        return WaitingListService.get_waiting_entry(db, waiting_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_waiting_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    entries = WaitingListService.list_waiting_entries(db, skip, limit)
    return {
        "count": len(entries),
        "waiting_entries": entries
    }


@router.get("/patient/{patient_id}")
def get_patient_waiting_entries(patient_id: int, db: Session = Depends(get_db)):
    entries = WaitingListService.get_patient_waiting_entries(db, patient_id)
    return {
        "patient_id": patient_id,
        "count": len(entries),
        "waiting_entries": entries
    }


@router.get("/patient/{patient_id}/active-count")
def get_patient_active_count(patient_id: int, db: Session = Depends(get_db)):
    count = WaitingListService.get_patient_active_count(db, patient_id)
    return {
        "patient_id": patient_id,
        "active_count": count
    }


@router.get("/doctor/{doctor_id}")
def get_doctor_waiting_entries(doctor_id: int, db: Session = Depends(get_db)):
    entries = WaitingListService.get_doctor_waiting_entries(db, doctor_id)
    return {
        "doctor_id": doctor_id,
        "count": len(entries),
        "waiting_entries": entries
    }


@router.get("/doctor/{doctor_id}/active")
def get_doctor_active_entries(doctor_id: int, db: Session = Depends(get_db)):
    entries = WaitingListService.get_active_entries(db, doctor_id)
    return {
        "doctor_id": doctor_id,
        "count": len(entries),
        "waiting_entries": entries
    }


@router.get("/doctor/{doctor_id}/notified")
def get_doctor_notified_entries(doctor_id: int, db: Session = Depends(get_db)):
    entries = WaitingListService.get_notified_entries(db, doctor_id)
    return {
        "doctor_id": doctor_id,
        "count": len(entries),
        "waiting_entries": entries
    }


@router.get("/doctor/{doctor_id}/statistics")
def get_doctor_waiting_statistics(doctor_id: int, db: Session = Depends(get_db)):
    return WaitingListService.get_waiting_statistics(db, doctor_id)


@router.get("/doctor/{doctor_id}/date/{preferred_date}")
def get_entries_by_date(
    doctor_id: int,
    preferred_date: str,
    db: Session = Depends(get_db)
):
    try:
        date_obj = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        entries = WaitingListService.get_entries_by_date(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "preferred_date": preferred_date,
            "count": len(entries),
            "waiting_entries": entries
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


@router.get("/doctor/{doctor_id}/date/{preferred_date}/priority")
def get_priority_entries_by_date(
    doctor_id: int,
    preferred_date: str,
    db: Session = Depends(get_db)
):
    try:
        date_obj = datetime.strptime(preferred_date, "%Y-%m-%d").date()
        entries = WaitingListService.get_priority_entries(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "preferred_date": preferred_date,
            "count": len(entries),
            "waiting_entries": entries
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")


@router.get("/doctor/{doctor_id}/date-range")
def get_entries_by_date_range(
    doctor_id: int,
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        entries = WaitingListService.get_entries_by_date_range(db, doctor_id, start, end)
        return {
            "doctor_id": doctor_id,
            "start_date": start_date,
            "end_date": end_date,
            "count": len(entries),
            "waiting_entries": entries
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/active")
def get_all_active_entries(
    doctor_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    entries = WaitingListService.get_active_entries(db, doctor_id)
    return {
        "doctor_id": doctor_id,
        "count": len(entries),
        "waiting_entries": entries
    }


# ================= UPDATE / STATUS =================

@router.put("/{waiting_id}")
def update_waiting_entry(
    waiting_id: int,
    payload: WaitingListUpdate,
    db: Session = Depends(get_db)
):
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        entry = WaitingListService.update_waiting_entry(db, waiting_id, update_data)
        return {
            "message": "Waiting list entry updated successfully",
            "waiting_entry": entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{waiting_id}/notify")
def notify_patient(waiting_id: int, db: Session = Depends(get_db)):
    try:
        entry = WaitingListService.notify_patient(db, waiting_id)
        return {
            "message": "Patient notified successfully",
            "waiting_entry": entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{waiting_id}/accept")
def accept_entry(waiting_id: int, db: Session = Depends(get_db)):
    try:
        entry = WaitingListService.accept_entry(db, waiting_id)
        return {
            "message": "Waiting list entry accepted",
            "waiting_entry": entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{waiting_id}/decline")
def decline_entry(waiting_id: int, db: Session = Depends(get_db)):
    try:
        entry = WaitingListService.decline_entry(db, waiting_id)
        return {
            "message": "Waiting list entry declined",
            "waiting_entry": entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{waiting_id}/cancel")
def cancel_entry(waiting_id: int, db: Session = Depends(get_db)):
    try:
        entry = WaitingListService.cancel_entry(db, waiting_id)
        return {
            "message": "Waiting list entry cancelled",
            "waiting_entry": entry
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================= BULK / MAINTENANCE =================

@router.post("/bulk-cancel")
def bulk_cancel_entries(payload: BulkCancel, db: Session = Depends(get_db)):
    count = WaitingListService.bulk_cancel_entries(db, payload.waiting_ids)
    return {
        "message": f"Cancelled {count} waiting list entries",
        "count": count
    }


@router.post("/expire-old-entries")
def expire_old_entries(db: Session = Depends(get_db)):
    count = WaitingListService.expire_old_entries(db)
    return {
        "message": f"Expired {count} waiting list entries",
        "count": count
    }


@router.delete("/{waiting_id}")
def delete_waiting_entry(waiting_id: int, db: Session = Depends(get_db)):
    try:
        WaitingListService.delete_waiting_entry(db, waiting_id)
        return {"message": "Waiting list entry deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
