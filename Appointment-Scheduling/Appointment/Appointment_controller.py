from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, time
from Appointment_config import get_db
from Appointment.Appointment_service import AppointmentService
from pydantic import BaseModel, Field

router = APIRouter()

# Pydantic models for request validation
class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Doctor ID")
    appointment_date: str = Field(..., description="Appointment date (YYYY-MM-DD)")
    start_time: str = Field(..., description="Start time (HH:MM:SS)")
    end_time: str = Field(..., description="End time (HH:MM:SS)")
    appointment_type: str = Field(default="CONSULTATION", description="Type of appointment")
    reason_for_visit: Optional[str] = Field(None, description="Reason for visit")
    symptoms: Optional[str] = Field(None, description="Symptoms")
    notes: Optional[str] = Field(None, description="Additional notes")
    consultation_fee: Optional[float] = Field(None, description="Consultation fee")

class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    appointment_type: Optional[str] = None
    reason_for_visit: Optional[str] = None
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    consultation_fee: Optional[float] = None
    status: Optional[str] = None

class AppointmentCancel(BaseModel):
    cancelled_by: int = Field(..., description="User ID who is cancelling")
    cancellation_reason: str = Field(..., description="Reason for cancellation")

class AppointmentReschedule(BaseModel):
    new_date: str = Field(..., description="New appointment date (YYYY-MM-DD)")
    new_start_time: str = Field(..., description="New start time (HH:MM:SS)")
    new_end_time: str = Field(..., description="New end time (HH:MM:SS)")

class AvailabilityCheck(BaseModel):
    doctor_id: int = Field(..., description="Doctor ID")
    appointment_date: str = Field(..., description="Date to check (YYYY-MM-DD)")
    start_time: str = Field(..., description="Start time (HH:MM:SS)")
    end_time: str = Field(..., description="End time (HH:MM:SS)")


@router.post("/", status_code=201)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    """
    Create a new appointment
    """
    try:
        appointment = AppointmentService.create_appointment(db, payload.dict())
        return {
            "message": "Appointment created successfully",
            "appointment_id": appointment.appointment_id,
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Get appointment by ID
    """
    try:
        appointment = AppointmentService.get_appointment(db, appointment_id)
        return appointment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
def list_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    List all appointments with pagination
    """
    try:
        appointments = AppointmentService.list_appointments(db, skip, limit)
        return {
            "count": len(appointments),
            "appointments": appointments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/patient/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    """
    Get all appointments for a specific patient
    """
    try:
        appointments = AppointmentService.get_patient_appointments(db, patient_id)
        return {
            "patient_id": patient_id,
            "count": len(appointments),
            "appointments": appointments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/patient/{patient_id}/upcoming")
def get_patient_upcoming_appointments(patient_id: int, db: Session = Depends(get_db)):
    """
    Get upcoming appointments for a patient
    """
    try:
        appointments = AppointmentService.get_upcoming_appointments_for_patient(db, patient_id)
        return {
            "patient_id": patient_id,
            "count": len(appointments),
            "appointments": appointments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/patient/{patient_id}/past")
def get_patient_past_appointments(patient_id: int, db: Session = Depends(get_db)):
    """
    Get past appointments for a patient
    """
    try:
        appointments = AppointmentService.get_past_appointments_for_patient(db, patient_id)
        return {
            "patient_id": patient_id,
            "count": len(appointments),
            "appointments": appointments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}")
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get all appointments for a specific doctor
    """
    try:
        appointments = AppointmentService.get_doctor_appointments(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "count": len(appointments),
            "appointments": appointments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/today")
def get_doctor_today_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get today's appointments for a doctor
    """
    try:
        appointments = AppointmentService.get_today_appointments_for_doctor(db, doctor_id)
        return {
            "doctor_id": doctor_id,
            "date": str(date.today()),
            "count": len(appointments),
            "appointments": appointments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/doctor/{doctor_id}/date/{appointment_date}")
def get_doctor_appointments_by_date(
    doctor_id: int, 
    appointment_date: str,
    db: Session = Depends(get_db)
):
    """
    Get doctor's appointments on a specific date (YYYY-MM-DD)
    """
    try:
        from datetime import datetime
        date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        appointments = AppointmentService.get_doctor_appointments_by_date(db, doctor_id, date_obj)
        return {
            "doctor_id": doctor_id,
            "date": appointment_date,
            "count": len(appointments),
            "appointments": appointments
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/date/{appointment_date}")
def get_appointments_by_date(appointment_date: str, db: Session = Depends(get_db)):
    """
    Get all appointments on a specific date (YYYY-MM-DD)
    """
    try:
        from datetime import datetime
        date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        appointments = AppointmentService.get_appointments_by_date(db, date_obj)
        return {
            "date": appointment_date,
            "count": len(appointments),
            "appointments": appointments
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format. Use YYYY-MM-DD: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{appointment_id}")
def update_appointment(
    appointment_id: int, 
    payload: AppointmentUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing appointment
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in payload.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        appointment = AppointmentService.update_appointment(db, appointment_id, update_data)
        return {
            "message": "Appointment updated successfully",
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int, 
    payload: AppointmentCancel, 
    db: Session = Depends(get_db)
):
    """
    Cancel an appointment
    """
    try:
        appointment = AppointmentService.cancel_appointment(
            db, 
            appointment_id, 
            payload.cancelled_by, 
            payload.cancellation_reason
        )
        return {
            "message": "Appointment cancelled successfully",
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{appointment_id}/confirm")
def confirm_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Confirm an appointment
    """
    try:
        appointment = AppointmentService.confirm_appointment(db, appointment_id)
        return {
            "message": "Appointment confirmed successfully",
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{appointment_id}/complete")
def complete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Mark an appointment as completed
    """
    try:
        appointment = AppointmentService.complete_appointment(db, appointment_id)
        return {
            "message": "Appointment marked as completed",
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{appointment_id}/no-show")
def mark_no_show(appointment_id: int, db: Session = Depends(get_db)):
    """
    Mark an appointment as no-show
    """
    try:
        appointment = AppointmentService.mark_no_show(db, appointment_id)
        return {
            "message": "Appointment marked as no-show",
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/{appointment_id}/reschedule")
def reschedule_appointment(
    appointment_id: int, 
    payload: AppointmentReschedule, 
    db: Session = Depends(get_db)
):
    """
    Reschedule an appointment to a new date and time
    """
    try:
        from datetime import datetime
        new_date = datetime.strptime(payload.new_date, "%Y-%m-%d").date()
        new_start_time = datetime.strptime(payload.new_start_time, "%H:%M:%S").time()
        new_end_time = datetime.strptime(payload.new_end_time, "%H:%M:%S").time()
        
        appointment = AppointmentService.reschedule_appointment(
            db, appointment_id, new_date, new_start_time, new_end_time
        )
        return {
            "message": "Appointment rescheduled successfully",
            "appointment": appointment
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Delete an appointment
    """
    try:
        AppointmentService.delete_appointment(db, appointment_id)
        return {"message": "Appointment deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/check-availability")
def check_availability(payload: AvailabilityCheck, db: Session = Depends(get_db)):
    """
    Check if a time slot is available for a doctor
    """
    try:
        from datetime import datetime
        check_date = datetime.strptime(payload.appointment_date, "%Y-%m-%d").date()
        start_time = datetime.strptime(payload.start_time, "%H:%M:%S").time()
        end_time = datetime.strptime(payload.end_time, "%H:%M:%S").time()
        
        result = AppointmentService.check_availability(
            db, payload.doctor_id, check_date, start_time, end_time
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
