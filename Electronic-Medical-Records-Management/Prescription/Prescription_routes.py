# Prescription/Prescription_routes.py
from fastapi import APIRouter, Depends, HTTPException
from .Prescription_service import PrescriptionService
from .Prescription_configuration import get_prescription_service

router = APIRouter(
    prefix="/prescriptions",
    tags=["EMR - Prescriptions"]
)

@router.post("/")
def create_prescription(
    doctor_id: int,
    record_id: int,
    patient_id: int,
    payload: dict,
    service: PrescriptionService = Depends(get_prescription_service)
):
    return service.create_prescription(doctor_id, record_id, patient_id, payload)

from fastapi import HTTPException

@router.get("/{prescription_id}")
def get_prescription(
    prescription_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
):
    try:
        return service.get_prescription(prescription_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/patient/{patient_id}")
def get_by_patient(
    patient_id: int,
    service: PrescriptionService = Depends(get_prescription_service)
):
    return service.get_patient_prescriptions(patient_id)

@router.get("/record/{record_id}")
def get_by_record(
    record_id: int,
    service: PrescriptionService = Depends(get_prescription_service)
):
    return service.get_record_prescriptions(record_id)

@router.patch("/{prescription_id}/cancel")
def cancel_prescription(
    prescription_id: int,
    service: PrescriptionService = Depends(get_prescription_service)
):
    return service.cancel_prescription(prescription_id)

@router.put("/{prescription_id}")
def update_prescription(
    prescription_id: int,
    payload: dict,
    service: PrescriptionService = Depends(get_prescription_service),
):
    try:
        return service.update_prescription(prescription_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.delete("/{prescription_id}")
def delete_prescription(
    prescription_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
):
    try:
        service.delete_prescription(prescription_id)
        return {"message": "Prescription deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))