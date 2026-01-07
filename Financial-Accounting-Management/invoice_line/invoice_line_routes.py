from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from invoice_line.invoice_line_schema import InvoiceLineCreate, InvoiceLineResponse
from invoice_line.invoice_line_service import InvoiceLineService

router = APIRouter(prefix="/invoice-lines", tags=["Invoice Line"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InvoiceLineResponse)
def create_invoice_line(data: InvoiceLineCreate, db: Session = Depends(get_db)):
    return InvoiceLineService.create_invoice_line(db, data)

@router.get("/{invoice_line_id}", response_model=InvoiceLineResponse)
def get_invoice_line(invoice_line_id: int, db: Session = Depends(get_db)):
    return InvoiceLineService.get_invoice_line(db, invoice_line_id)

@router.get("/by-invoice/{invoice_id}", response_model=list[InvoiceLineResponse])
def get_invoice_lines_by_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return InvoiceLineService.get_invoice_lines_by_invoice(db, invoice_id)

@router.put("/{invoice_line_id}", response_model=InvoiceLineResponse)
def update_invoice_line(invoice_line_id: int, data: dict, db: Session = Depends(get_db)):
    return InvoiceLineService.update_invoice_line(db, invoice_line_id, data)

@router.delete("/{invoice_line_id}")
def delete_invoice_line(invoice_line_id: int, db: Session = Depends(get_db)):
    InvoiceLineService.delete_invoice_line(db, invoice_line_id)
    return {"message": "Invoice line deleted successfully"}
