from fastapi import APIRouter, Depends, HTTPException
from .Prescription_service import PrescriptionService
from .Prescription_configuration import get_prescription_service
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/prescriptions", tags=["EMR - Prescriptions"])

@router.post("/")
def create_prescription(
    record_id: int,
    patient_id: int,
    payload: dict,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        return service.create_prescription(current_user["user_id"], record_id, patient_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/record/{record_id}")
def get_by_record(record_id: int, service: PrescriptionService = Depends(get_prescription_service)):
    return service.get_prescriptions_for_record(record_id)

@router.get("/patient/{patient_id}")
def get_by_patient(patient_id: int, service: PrescriptionService = Depends(get_prescription_service)):
    return service.get_patient_prescriptions(patient_id)