from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .Insurance_service import InsuranceService
from .schemas import InsuranceCreate, InsuranceUpdate, InsuranceResponse
from Patient_Registration_Management.database import get_db

router = APIRouter(
    prefix="/insurance",
    tags=["Insurance"]
)

def get_service(db: Session = Depends(get_db)):
    return InsuranceService(db)

# Create insurance
@router.post("/", response_model=InsuranceResponse, status_code=status.HTTP_201_CREATED)
def create_insurance(data: InsuranceCreate, service: InsuranceService = Depends(get_service)):
    try:
        return service.create_insurance(data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get insurance by ID
@router.get("/{insurance_id}", response_model=InsuranceResponse)
def get_insurance(insurance_id: int, service: InsuranceService = Depends(get_service)):
    try:
        return service.get_insurance(insurance_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Get all insurances
@router.get("/", response_model=List[InsuranceResponse])
def list_insurances(service: InsuranceService = Depends(get_service)):
    return service.list_insurances()

# Update insurance
@router.put("/{insurance_id}", response_model=InsuranceResponse)
def update_insurance(insurance_id: int, data: InsuranceUpdate, service: InsuranceService = Depends(get_service)):
    try:
        return service.update_insurance(insurance_id, data.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Delete insurance
@router.delete("/{insurance_id}")
def delete_insurance(insurance_id: int, service: InsuranceService = Depends(get_service)):
    try:
        service.delete_insurance(insurance_id)
        return {"message": "Insurance deleted successfully", "insurance_id": insurance_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
