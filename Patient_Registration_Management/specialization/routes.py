from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import SpecializationCreate, SpecializationUpdate, SpecializationResponse
from .service import SpecializationService
from .repository import SpecializationRepository
from Patient_Registration_Management.database import get_db

router = APIRouter()

def get_service(db: Session = Depends(get_db)):
    repository = SpecializationRepository(db)
    return SpecializationService(repository)

# Create
@router.post("/", response_model=SpecializationResponse)
def create_specialization(data: SpecializationCreate, service: SpecializationService = Depends(get_service)):
    return service.create_specialization(data)

# Read all
@router.get("/", response_model=list[SpecializationResponse])
def get_all_specializations(service: SpecializationService = Depends(get_service)):
    return service.get_all_specializations()

# Read one
@router.get("/{specialization_id}", response_model=SpecializationResponse)
def get_specialization(specialization_id: int, service: SpecializationService = Depends(get_service)):
    specialization = service.get_specialization(specialization_id)
    if not specialization:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return specialization

# Update
@router.put("/{specialization_id}", response_model=SpecializationResponse)
def update_specialization(specialization_id: int, data: SpecializationUpdate, service: SpecializationService = Depends(get_service)):
    specialization = service.update_specialization(specialization_id, data)
    if not specialization:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return specialization

# Delete
@router.delete("/{specialization_id}")
def delete_specialization(specialization_id: int, service: SpecializationService = Depends(get_service)):
    specialization = service.delete_specialization(specialization_id)
    if not specialization:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return {"message": "Specialization deleted successfully"}
