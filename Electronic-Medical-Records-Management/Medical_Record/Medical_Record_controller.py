from fastapi import APIRouter, Depends
from typing import List

from .Medical_Record_schema import (
    MedicalRecordCreate,
    MedicalRecordUpdate,
    MedicalRecordResponse,
)
from .Medical_Record_service import MedicalRecordService
from .Medical_Record_configuration import get_medical_record_service
from auth.dependencies import get_current_user

router = APIRouter(
    prefix="/medical-records",
    tags=["EMR - Medical Records"]
)

# CREATE
@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(
    payload: MedicalRecordCreate,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user),
):
    return service.create_record(
        doctor_id=current_user["doctor_id"],
        payload=payload.dict()
    )

# READ (single)
@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user),
):
    return service.get_record(record_id)

# READ (by patient)
@router.get(
    "/patient/{patient_id}",
    response_model=List[MedicalRecordResponse]
)
def get_patient_medical_history(
    patient_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user),
):
    return service.get_patient_history(patient_id)

# UPDATE
@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: int,
    payload: MedicalRecordUpdate,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user),
):
    return service.update_record(
        record_id,
        payload.dict(exclude_unset=True)
    )

# DELETE
@router.delete("/{record_id}")
def delete_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
    current_user: dict = Depends(get_current_user),
):
    service.delete_record(record_id)
    return {"message": "Medical record deleted successfully"}
