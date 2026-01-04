from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Patient.database import get_db
from Patient.Patient_service import PatientService

router = APIRouter()

@router.post("/")
def create_patient(payload: dict, db: Session = Depends(get_db)):
    try:
        return PatientService.create_patient(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        return PatientService.get_patient(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_patients(db: Session = Depends(get_db)):
    return PatientService.list_patients(db)

@router.put("/{patient_id}")
def update_patient(patient_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return PatientService.update_patient(db, patient_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    try:
        PatientService.delete_patient(db, patient_id)
        return {"message": "Patient deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
