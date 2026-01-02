from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controller import AddressController
from database import get_db

router = APIRouter(prefix="/addresses", tags=["Address"])
controller = AddressController()

@router.post("/")
def create_address(address_data: dict, db: Session = Depends(get_db)):
    return controller.create_address(db, address_data)

@router.get("/{address_id}")
def get_address(address_id: int, db: Session = Depends(get_db)):
    return controller.fetch_address(db, address_id)

@router.get("/patient/{patient_id}")
def get_patient_addresses(patient_id: int, db: Session = Depends(get_db)):
    return controller.fetch_addresses_by_patient(db, patient_id)

@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    return controller.delete_address(db, address_id)
