from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from patient_service import PatientService
from patient_repository import PatientRepository
from Patient_Registration_Management.database import get_db


router = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return PatientService(PatientRepository(db))


@router.post("/")
def create_patient(data: dict, service: PatientService = Depends(get_service)):
    return service.create_patient(data)


@router.get("/")
def get_all_patients(service: PatientService = Depends(get_service)):
    return service.get_all_patients()


@router.get("/{patient_id}")
def get_patient(patient_id: int, service: PatientService = Depends(get_service)):
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    data: dict,
    service: PatientService = Depends(get_service)
):
    patient = service.update_patient(patient_id, data)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, service: PatientService = Depends(get_service)):
    return service.delete_patient(patient_id)
