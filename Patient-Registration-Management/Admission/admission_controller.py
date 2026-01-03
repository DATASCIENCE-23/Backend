from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .admission_configuration import get_db
from .admission_service import AdmissionService

router = APIRouter()

@router.post("/admit")
def admit_patient(
    appointment_id: int,
    ward: str,
    bed_number: str,
    reason: str,
    db: Session = Depends(get_db)
):
    try:
        return AdmissionService.admit_patient(db, appointment_id, ward, bed_number, reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/discharge/{admission_id}")
def discharge_patient(
    admission_id: int,
    summary: str,
    db: Session = Depends(get_db)
):
    try:
        return AdmissionService.discharge_patient(db, admission_id, summary)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{admission_id}")
def get_admission(admission_id: int, db: Session = Depends(get_db)):
    try:
        return AdmissionService.get_admission(db, admission_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/active")
def list_active_admissions(db: Session = Depends(get_db)):
    return AdmissionService.list_active_admissions(db)

@router.put("/{admission_id}/transfer")
def transfer_bed(
    admission_id: int,
    ward: str,
    bed_number: str,
    db: Session = Depends(get_db)
):
    try:
        return AdmissionService.transfer_bed(db, admission_id, ward, bed_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{admission_id}")
def delete_admission(admission_id: int, db: Session = Depends(get_db)):
    try:
        return AdmissionService.delete_admission(db, admission_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
