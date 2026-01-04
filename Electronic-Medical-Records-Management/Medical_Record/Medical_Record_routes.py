from fastapi import APIRouter, Depends, HTTPException
from typing import List

from .Medical_Record_schema import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
)
from .Medical_Record_service import MedicalRecordService
from .Medical_Record_configuration import get_medical_record_service

router = APIRouter(
    prefix="/medical-records",
    tags=["EMR - Medical Records"]
)

# CREATE
@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(
    payload: MedicalRecordCreate,
    doctor_id: int,   # ✅ explicitly passed
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    return service.create_record(
        doctor_id=doctor_id,
        data=payload.dict()
    )

# READ (single)
@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    record = service.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

# READ (by patient)
@router.get(
    "/patient/{patient_id}",
    response_model=List[MedicalRecordResponse]
)
def get_patient_medical_history(
    patient_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    return service.get_patient_history(patient_id)

# UPDATE
@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    payload: MedicalRecordUpdate,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    record = service.update_record(
        record_id,
        payload.dict(exclude_unset=True)
    )
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

# DELETE
@router.delete("/{record_id}")
def delete_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    service.delete_record(record_id)
    return {"message": "Medical record deleted successfully"}

@router.get("/", response_model=List[MedicalRecordResponse])
def get_all_medical_records(
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    return service.get_all_records()
