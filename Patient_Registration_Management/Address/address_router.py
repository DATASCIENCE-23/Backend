from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .address_service import AddressService
from .schemas import AddressCreate, AddressUpdate, AddressResponse
from Patient_Registration_Management.database import get_db

router = APIRouter(
    prefix="/addresses",
    tags=["Address"]
)

def get_service(db: Session = Depends(get_db)):
    return AddressService(db)

# Create address
@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(data: AddressCreate, service: AddressService = Depends(get_service)):
    return service.create_address(data.dict())

# Get single address
@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, service: AddressService = Depends(get_service)):
    address = service.get_address(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

# Get all addresses of a patient
@router.get("/patient/{patient_id}", response_model=List[AddressResponse])
def get_patient_addresses(patient_id: int, service: AddressService = Depends(get_service)):
    return service.get_addresses_by_patient(patient_id)

# ✅ Update address
@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    data: AddressUpdate,
    service: AddressService = Depends(get_service)
):
    updated = service.update_address(address_id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated

# Delete address
@router.delete("/{address_id}")
def delete_address(address_id: int, service: AddressService = Depends(get_service)):
    deleted = service.delete_address(address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully", "address_id": address_id}
