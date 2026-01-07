from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from bill_line.bill_line_schema import BillLineCreate, BillLineResponse
from bill_line.bill_line_service import BillLineService

router = APIRouter(prefix="/bill-lines", tags=["Bill Line"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BillLineResponse)
def create_bill_line(data: BillLineCreate, db: Session = Depends(get_db)):
    return BillLineService.create_bill_line(db, data)

@router.get("/{bill_line_id}", response_model=BillLineResponse)
def get_bill_line(bill_line_id: int, db: Session = Depends(get_db)):
    return BillLineService.get_bill_line(db, bill_line_id)

@router.get("/by-bill/{bill_id}", response_model=list[BillLineResponse])
def get_bill_lines_by_bill(bill_id: int, db: Session = Depends(get_db)):
    return BillLineService.get_bill_lines_by_bill(db, bill_id)

@router.put("/{bill_line_id}", response_model=BillLineResponse)
def update_bill_line(bill_line_id: int, data: dict, db: Session = Depends(get_db)):
    return BillLineService.update_bill_line(db, bill_line_id, data)

@router.delete("/{bill_line_id}")
def delete_bill_line(bill_line_id: int, db: Session = Depends(get_db)):
    BillLineService.delete_bill_line(db, bill_line_id)
    return {"message": "Bill line deleted successfully"}
