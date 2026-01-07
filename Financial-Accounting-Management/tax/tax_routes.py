from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from tax.tax_schema import TaxCreate, TaxResponse
from tax.tax_service import TaxService

router = APIRouter(prefix="/taxes", tags=["Tax"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaxResponse)
def create_tax(data: TaxCreate, db: Session = Depends(get_db)):
    return TaxService.create_tax(db, data)

@router.get("/{tax_id}", response_model=TaxResponse)
def get_tax(tax_id: int, db: Session = Depends(get_db)):
    return TaxService.get_tax(db, tax_id)

@router.get("/", response_model=list[TaxResponse])
def get_all_taxes(db: Session = Depends(get_db)):
    return TaxService.get_all_taxes(db)

@router.put("/{tax_id}", response_model=TaxResponse)
def update_tax(tax_id: int, data: dict, db: Session = Depends(get_db)):
    return TaxService.update_tax(db, tax_id, data)

@router.delete("/{tax_id}")
def delete_tax(tax_id: int, db: Session = Depends(get_db)):
    TaxService.delete_tax(db, tax_id)
    return {"message": "Tax deleted successfully"}
