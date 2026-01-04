from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .service import DoctorService
from .repository import DoctorRepository
from .schemas import DoctorCreate, DoctorUpdate, DoctorResponse
from Patient_Registration_Management.database import get_db

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

# Dependency to get DoctorService
def get_service(db: Session = Depends(get_db)):
    return DoctorService(DoctorRepository(db))


# ---------------------------
# CREATE Doctor
# ---------------------------
@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
    data: DoctorCreate,
    service: DoctorService = Depends(get_service)
):
    try:
        return service.create_doctor(data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------------------------
# GET all Doctors
# ---------------------------
@router.get("/", response_model=List[DoctorResponse])
def get_all_doctors(service: DoctorService = Depends(get_service)):
    return service.get_all_doctors()


# ---------------------------
# GET Doctor by ID
# ---------------------------
@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    service: DoctorService = Depends(get_service)
):
    doctor = service.get_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doctor


# ---------------------------
# UPDATE Doctor
# ---------------------------
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    data: DoctorUpdate,
    service: DoctorService = Depends(get_service)
):
    try:
        doctor = service.update_doctor(doctor_id, data.dict(exclude_unset=True))
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------------------------
# DELETE Doctor
# ---------------------------
@router.delete("/{doctor_id}", response_model=dict)
def delete_doctor(
    doctor_id: int,
    service: DoctorService = Depends(get_service)
):
    try:
        doctor = service.delete_doctor(doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return {"message": "Doctor deleted successfully", "doctor_id": doctor_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
