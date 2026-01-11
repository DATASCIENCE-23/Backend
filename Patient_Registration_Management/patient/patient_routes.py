from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Patient_Registration_Management.patient.patient_service import PatientService
from Patient_Registration_Management.patient.patient_repository import PatientRepository
from Patient_Registration_Management.patient.schemas import PatientCreate, PatientUpdate, PatientResponse
from Patient_Registration_Management.database import get_db

router = APIRouter()


def get_service(db: Session = Depends(get_db)):
    return PatientService(PatientRepository(db))


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(data: PatientCreate, service: PatientService = Depends(get_service)):
    return service.create_patient(data.dict())


@router.get("/", response_model=list[PatientResponse])
def get_all_patients(service: PatientService = Depends(get_service)):
    return service.get_all_patients()


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, service: PatientService = Depends(get_service)):
    patient = service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, data: PatientUpdate, service: PatientService = Depends(get_service)):
    patient = service.update_patient(patient_id, data.dict(exclude_unset=True))
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_200_OK)
def delete_patient(patient_id: int, service: PatientService = Depends(get_service)):
    patient = service.delete_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully", "patient_id": patient_id}
