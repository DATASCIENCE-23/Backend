from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from BILL.bill_service import BillService

router = APIRouter(prefix="/bills", tags=["Bills"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_bill(payload: dict, db: Session = Depends(get_db)):
    try:
        return BillService.create_bill(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{bill_id}")
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    try:
        return BillService.get_bill(db, bill_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_all_bills(db: Session = Depends(get_db)):
    return BillService.list_all_bills(db)


@router.get("/vendor/{vendor_id}")
def list_bills_by_vendor(vendor_id: int, db: Session = Depends(get_db)):
    return BillService.list_bills_by_vendor(db, vendor_id)


@router.get("/status/{status}")
def list_bills_by_status(status: str, db: Session = Depends(get_db)):
    return BillService.list_bills_by_status(db, status)


@router.get("/date-range/")
def list_bills_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    return BillService.list_bills_by_date_range(db, start_date, end_date)


@router.put("/{bill_id}")
def update_bill(bill_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return BillService.update_bill(db, bill_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    try:
        BillService.delete_bill(db, bill_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))