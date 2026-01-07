from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from invoice.invoice_schema import InvoiceCreate, InvoiceResponse
from invoice.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["Invoice"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    return InvoiceService.create_invoice(db, data)

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return InvoiceService.get_invoice(db, invoice_id)

@router.get("/", response_model=list[InvoiceResponse])
def get_all_invoices(db: Session = Depends(get_db)):
    return InvoiceService.get_all_invoices(db)

@router.get("/by-patient/{patient_id}", response_model=list[InvoiceResponse])
def get_invoices_by_patient(patient_id: int, db: Session = Depends(get_db)):
    return InvoiceService.get_invoices_by_patient(db, patient_id)

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(invoice_id: int, data: dict, db: Session = Depends(get_db)):
    return InvoiceService.update_invoice(db, invoice_id, data)

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    InvoiceService.delete_invoice(db, invoice_id)
    return {"message": "Invoice deleted successfully"}
