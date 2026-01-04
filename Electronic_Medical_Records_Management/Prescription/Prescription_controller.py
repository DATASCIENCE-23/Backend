from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .Prescription_model import Prescription
from .Prescription_service import PrescriptionService
from .Prescription_configuration import get_prescription_service
from ..auth.dependencies import get_current_user  # Adjust path as needed

router = APIRouter(
    prefix="/prescriptions",
    tags=["EMR - Prescriptions"]
)

@router.post("/", response_model=dict)
def create_prescription(
    record_id: int,
    patient_id: int,
    payload: dict,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    """Doctor creates electronic prescription linked to a medical record"""
    try:
        prescription = service.create_prescription(
            current_user_id=current_user["user_id"],
            record_id=record_id,
            patient_id=patient_id,
            payload=payload
        )
        return prescription.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{prescription_id}", response_model=dict)
def get_prescription(
    prescription_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        prescription = service.get_prescription(prescription_id)
        return prescription.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/patient/{patient_id}", response_model=List[dict])
def get_patient_prescriptions(
    patient_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    """View all prescriptions for a patient (Doctor, Nurse, Patient optional)"""
    prescriptions = service.get_patient_prescriptions(patient_id)
    return [p.__dict__ for p in prescriptions]


@router.get("/record/{record_id}", response_model=List[dict])
def get_prescriptions_by_record(
    record_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    prescriptions = service.get_prescriptions_for_record(record_id)
    return [p.__dict__ for p in prescriptions]


@router.put("/{prescription_id}", response_model=dict)
def update_prescription(
    prescription_id: int,
    payload: dict,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        updated = service.update_prescription(prescription_id, payload)
        return updated.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{prescription_id}/cancel", response_model=dict)
def cancel_prescription(
    prescription_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        cancelled = service.cancel_prescription(prescription_id)
        return cancelled.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{prescription_id}", response_model=dict)
def delete_prescription(
    prescription_id: int,
    service: PrescriptionService = Depends(get_prescription_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        service.delete_prescription(prescription_id)
        return {"message": "Prescription deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))