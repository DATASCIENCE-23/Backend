from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from INVOICE_LINE.invoice_line_service import InvoiceLineService

router = APIRouter(prefix="/invoice-lines", tags=["Invoice Lines"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_invoice_line(payload: dict, db: Session = Depends(get_db)):
    """
    Add an invoice line (price calculation + revenue account mapping)
    """
    try:
        return InvoiceLineService.add_invoice_line(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoice/{invoice_id}")
def list_invoice_lines(invoice_id: int, db: Session = Depends(get_db)):
    """
    List all invoice lines for an invoice
    """
    return InvoiceLineService.list_invoice_lines(db, invoice_id)
