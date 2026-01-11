from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Patient_Registration_Management.database import get_db
from .admission_service import AdmissionService
from .schemas import AdmissionCreate, AdmissionUpdate, AdmissionResponse

router = APIRouter(
    prefix="/admissions",
    tags=["Admission"]
)

def get_service(db: Session = Depends(get_db)):
    return AdmissionService(db)

# Create admission
@router.post("/", response_model=AdmissionResponse, status_code=status.HTTP_201_CREATED)
def create_admission(data: AdmissionCreate, service: AdmissionService = Depends(get_service)):
    try:
        return service.admit_patient(data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get admission by ID
@router.get("/{admission_id}", response_model=AdmissionResponse)
def get_admission(admission_id: int, service: AdmissionService = Depends(get_service)):
    try:
        return service.get_admission(admission_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# List all active admissions
@router.get("/active", response_model=List[AdmissionResponse])
def list_active_admissions(service: AdmissionService = Depends(get_service)):
    return service.list_active_admissions()

# Update admission
@router.put("/{admission_id}", response_model=AdmissionResponse)
def update_admission(admission_id: int, data: AdmissionUpdate, service: AdmissionService = Depends(get_service)):
    try:
        return service.update_admission(admission_id, data.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Discharge patient
@router.put("/{admission_id}/discharge", response_model=AdmissionResponse)
def discharge_admission(admission_id: int, summary: str, service: AdmissionService = Depends(get_service)):
    try:
        return service.discharge_patient(admission_id, summary)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Transfer bed
@router.put("/{admission_id}/transfer", response_model=AdmissionResponse)
def transfer_bed(admission_id: int, ward: str, bed_number: str, service: AdmissionService = Depends(get_service)):
    try:
        return service.transfer_bed(admission_id, ward, bed_number)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete admission
@router.delete("/{admission_id}", response_model=dict)
def delete_admission(admission_id: int, service: AdmissionService = Depends(get_service)):
    try:
        return service.delete_admission(admission_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
