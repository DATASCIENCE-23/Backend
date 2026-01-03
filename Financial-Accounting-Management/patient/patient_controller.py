from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from PATIENT.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_patient(payload: dict, db: Session = Depends(get_db)):
    try:
        return PatientService.register_patient(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{patient_id}")
def get_patient_details(patient_id: int, db: Session = Depends(get_db)):
    """
    Fetch patient details by ID
    """
    try:
        return PatientService.get_patient_details(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_patients(db: Session = Depends(get_db)):
    """
    List all patients
    """
    return PatientService.list_patients(db)


@router.get("/search/")
def search_patients(
    name: str | None = Query(None, description="Search by patient name"),
    contact: str | None = Query(None, description="Search by contact details"),
    db: Session = Depends(get_db)
):
    """
    Search patients by name or contact details
    """
    return PatientService.search_patients(db, name, contact)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient
    """
    try:
        PatientService.delete_patient(db, patient_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
