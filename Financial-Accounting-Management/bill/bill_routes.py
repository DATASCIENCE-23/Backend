from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from bill.bill_schema import BillCreate, BillResponse
from bill.bill_service import BillService

router = APIRouter(prefix="/bills", tags=["Bill"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BillResponse)
def create_bill(data: BillCreate, db: Session = Depends(get_db)):
    return BillService.create_bill(db, data)

@router.get("/{bill_id}", response_model=BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    return BillService.get_bill(db, bill_id)

@router.get("/", response_model=list[BillResponse])
def get_all_bills(db: Session = Depends(get_db)):
    return BillService.get_all_bills(db)

@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(bill_id: int, data: dict, db: Session = Depends(get_db)):
    return BillService.update_bill(db, bill_id, data)

@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    BillService.delete_bill(db, bill_id)
    return {"message": "Bill deleted successfully"}
