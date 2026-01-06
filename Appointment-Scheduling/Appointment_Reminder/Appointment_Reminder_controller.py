from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from Appointment_Reminder.Appointment_Reminder_config import get_db
from Appointment_Reminder.Appointment_Reminder_service import AppointmentReminderService
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/appointment-reminders",
    tags=["Appointment Reminders"]
)

# ================= Pydantic Schemas =================

class ReminderCreate(BaseModel):
    appointment_id: int
    reminder_type: str
    reminder_time: str
    message_content: Optional[str] = None


class ReminderUpdate(BaseModel):
    reminder_type: Optional[str] = None
    reminder_time: Optional[str] = None
    message_content: Optional[str] = None


# ================= CREATE =================

@router.post("/", status_code=201)
def create_reminder(
    payload: ReminderCreate,
    db: Session = Depends(get_db)
):
    try:
        reminder = AppointmentReminderService.create_reminder(
            db, payload.dict()
        )
        return {
            "message": "Reminder created successfully",
            "reminder_id": reminder.reminder_id,
            "reminder": reminder
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================= READ =================

@router.get("/{reminder_id}")
def get_reminder(reminder_id: int, db: Session = Depends(get_db)):
    try:
        return AppointmentReminderService.get_reminder(db, reminder_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_reminders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    reminders = AppointmentReminderService.list_reminders(
        db, skip, limit
    )
    return {
        "count": len(reminders),
        "reminders": reminders
    }


@router.get("/appointment/{appointment_id}")
def get_appointment_reminders(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    reminders = AppointmentReminderService.get_appointment_reminders(
        db, appointment_id
    )
    return {
        "appointment_id": appointment_id,
        "count": len(reminders),
        "reminders": reminders
    }


@router.get("/pending")
def get_pending_reminders(db: Session = Depends(get_db)):
    reminders = AppointmentReminderService.get_pending_reminders(db)
    return {
        "count": len(reminders),
        "reminders": reminders
    }


@router.get("/due")
def get_due_reminders(db: Session = Depends(get_db)):
    reminders = AppointmentReminderService.get_due_reminders(db)
    return {
        "count": len(reminders),
        "reminders": reminders
    }


@router.get("/failed")
def get_failed_reminders(db: Session = Depends(get_db)):
    reminders = AppointmentReminderService.get_failed_reminders(db)
    return {
        "count": len(reminders),
        "reminders": reminders
    }


@router.get("/statistics")
def get_reminder_statistics(db: Session = Depends(get_db)):
    return AppointmentReminderService.get_reminder_statistics(db)


# ================= STATUS =================

@router.patch("/{reminder_id}/send")
def mark_as_sent(reminder_id: int, db: Session = Depends(get_db)):
    try:
        reminder = AppointmentReminderService.mark_as_sent(
            db, reminder_id
        )
        return {
            "message": "Reminder marked as sent",
            "reminder": reminder
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{reminder_id}/fail")
def mark_as_failed(
    reminder_id: int,
    reason: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        reminder = AppointmentReminderService.mark_as_failed(
            db, reminder_id, reason
        )
        return {
            "message": "Reminder marked as failed",
            "reminder": reminder
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{reminder_id}/cancel")
def cancel_reminder(reminder_id: int, db: Session = Depends(get_db)):
    try:
        reminder = AppointmentReminderService.cancel_reminder(
            db, reminder_id
        )
        return {
            "message": "Reminder cancelled",
            "reminder": reminder
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================= UPDATE / DELETE =================

@router.put("/{reminder_id}")
def update_reminder(
    reminder_id: int,
    payload: ReminderUpdate,
    db: Session = Depends(get_db)
):
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        reminder = AppointmentReminderService.update_reminder(
            db, reminder_id, update_data
        )
        return {
            "message": "Reminder updated successfully",
            "reminder": reminder
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    try:
        AppointmentReminderService.delete_reminder(db, reminder_id)
        return {"message": "Reminder deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ================= APPOINTMENT LEVEL =================

@router.post("/appointment/{appointment_id}/cancel-all")
def cancel_appointment_reminders(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    count = AppointmentReminderService.cancel_appointment_reminders(
        db, appointment_id
    )
    return {
        "message": f"Cancelled {count} reminder(s)",
        "count": count
    }


@router.post("/process-due")
def process_due_reminders(db: Session = Depends(get_db)):
    return AppointmentReminderService.process_due_reminders(db)
