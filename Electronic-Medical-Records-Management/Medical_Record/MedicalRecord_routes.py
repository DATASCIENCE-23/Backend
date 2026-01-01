from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .MedicalRecord_service import MedicalRecordService
from .MedicalRecord_configuration import get_medical_record_service
from ..auth.dependencies import get_current_user  # Assuming you have auth

router = APIRouter(prefix="/medical-records", tags=["EMR - Medical Records"])

# POST /medical-records/ - Create new record (Doctor/Nurse)
@router.post("/")
def create_medical_record(
    payload: dict,
    patient_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        return service.create_record(current_user["user_id"], patient_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# GET /medical-records/{record_id} - View single record
@router.get("/{record_id}")
def get_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        return service.get_record(record_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# GET /medical-records/patient/{patient_id} - Patient's full history (key doctor story)
@router.get("/patient/{patient_id}")
def get_patient_medical_history(
    patient_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    return service.get_patient_history(patient_id)

# GET /medical-records/ - List all (Admin or reporting)
@router.get("/")
def list_all_records(
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    return service.list_all_records()

# PUT /medical-records/{record_id} - Update notes, diagnosis, treatment plan, vitals, etc.
@router.put("/{record_id}")
def update_medical_record(
    record_id: int,
    payload: dict,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        return service.update_record(record_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# DELETE /medical-records/{record_id} - Soft delete or admin only
@router.delete("/{record_id}")
def delete_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        service.delete_record(record_id)
        return {"message": "Medical record deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))