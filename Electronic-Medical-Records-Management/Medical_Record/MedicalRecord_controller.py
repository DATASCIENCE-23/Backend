from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .MedicalRecord_model import MedicalRecord
from .MedicalRecord_service import MedicalRecordService
from ..database import get_db
from .MedicalRecord_configuration import get_medical_record_service
from ..auth.dependencies import get_current_user  # Adjust path if your auth is elsewhere

router = APIRouter(
    prefix="/medical-records",
    tags=["EMR - Medical Records"]
)

@router.post("/", response_model=dict)
def create_medical_record(
    payload: dict,
    patient_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new medical record for a patient.
    Typically used by Doctor or Nurse during/afer a visit.
    """
    try:
        record = service.create_record(
            current_user_id=current_user["user_id"],
            patient_id=patient_id,
            payload=payload
        )
        return record.__dict__  # or use a Pydantic schema later
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{record_id}", response_model=dict)
def get_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve a single medical record by ID"""
    try:
        record = service.get_record(record_id)
        return record.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[dict])
def get_patient_medical_history(
    patient_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Get complete medical history for a patient (chronological).
    Key feature for Doctors to make informed decisions.
    """
    records = service.get_patient_history(patient_id)
    return [record.__dict__ for record in records]


@router.get("/", response_model=List[dict])
def get_all_medical_records(
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    """List all medical records - mainly for Admin reporting"""
    records = service.list_all_records()
    return [record.__dict__ for record in records]


@router.put("/{record_id}", response_model=dict)
def update_medical_record(
    record_id: int,
    payload: dict,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Update clinical notes, diagnosis, treatment plan, vitals, etc.
    Used by Doctors and Nurses.
    """
    try:
        updated_record = service.update_record(record_id, payload)
        return updated_record.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{record_id}", response_model=dict)
def delete_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    """Delete a medical record (Admin or correction use case)"""
    try:
        service.delete_record(record_id)
        return {"message": "Medical record deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))