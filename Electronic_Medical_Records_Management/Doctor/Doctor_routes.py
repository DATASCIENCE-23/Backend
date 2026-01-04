from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .Doctor_service import DoctorService
from .Doctor_repository import DoctorRepository
from database import get_db
from fastapi import APIRouter

router = APIRouter()



def get_service(db: Session = Depends(get_db)):
    return DoctorService(DoctorRepository(db))


@router.post("/")
def create_doctor(data: dict, service: DoctorService = Depends(get_service)):
    return service.create_doctor(data)


@router.get("/")
def get_all_doctors(service: DoctorService = Depends(get_service)):
    return service.get_all_doctors()


@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, service: DoctorService = Depends(get_service)):
    doctor = service.get_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, data: dict, service: DoctorService = Depends(get_service)):
    doctor = service.update_doctor(doctor_id, data)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, service: DoctorService = Depends(get_service)):
    return service.delete_doctor(doctor_id)
