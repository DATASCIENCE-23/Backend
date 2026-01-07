from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Tax.database import get_db
from Tax.Tax_service import TaxService

router = APIRouter()

@router.post("/")
def create_tax(payload: dict, db: Session = Depends(get_db)):
    try:
        return TaxService.create_tax(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tax_id}")
def get_tax(tax_id: int, db: Session = Depends(get_db)):
    try:
        return TaxService.get_tax(db, tax_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_taxes(db: Session = Depends(get_db)):
    return TaxService.list_taxes(db)

@router.put("/{tax_id}")
def update_tax(tax_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return TaxService.update_tax(db, tax_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{tax_id}")
def delete_tax(tax_id: int, db: Session = Depends(get_db)):
    try:
        TaxService.delete_tax(db, tax_id)
        return {"message": "Tax deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
