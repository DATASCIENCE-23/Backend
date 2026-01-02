from fastapi import APIRouter, Depends, HTTPException
from .Medical_Record_service import MedicalRecordService
from .Medical_Record_configuration import get_medical_record_service

router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)

@router.post("/")
def create_medical_record(
    patient_id: int,
    payload: dict,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    # TEMP: until auth is added
    user_id = 1

    return service.create_record(
        user_id=user_id,
        patient_id=patient_id,
        payload=payload
    )



@router.get("/")
def list_all_records(
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    return service.list_all_records()


@router.get("/{record_id}")
def get_medical_record(
    record_id: int,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    record = service.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
@router.put("/{record_id}")
def update_medical_record(
    record_id: int,
    payload: dict,
    service: MedicalRecordService = Depends(get_medical_record_service),
):
    try:
        return service.update_record(record_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
