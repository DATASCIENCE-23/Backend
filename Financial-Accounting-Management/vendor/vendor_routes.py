from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from vendor.vendor_schema import VendorCreate, VendorResponse
from vendor.vendor_service import VendorService

router = APIRouter(prefix="/vendors", tags=["Vendor"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=VendorResponse)
def create_vendor(data: VendorCreate, db: Session = Depends(get_db)):
    return VendorService.create_vendor(db, data)

@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    return VendorService.get_vendor(db, vendor_id)

@router.get("/", response_model=list[VendorResponse])
def get_all_vendors(db: Session = Depends(get_db)):
    return VendorService.get_all_vendors(db)

@router.put("/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, data: dict, db: Session = Depends(get_db)):
    return VendorService.update_vendor(db, vendor_id, data)

@router.delete("/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    VendorService.delete_vendor(db, vendor_id)
    return {"message": "Vendor deleted successfully"}
