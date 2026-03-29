from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from INVOICE.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_invoice(payload: dict, db: Session = Depends(get_db)):
    """
    Generate a new invoice for a patient
    """
    try:
        return InvoiceService.generate_invoice(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{invoice_id}")
def view_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    View invoice details
    """
    try:
        return InvoiceService.get_invoice(db, invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/patient/{patient_id}")
def list_invoices_by_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    List invoices for a patient
    """
    return InvoiceService.list_invoices_by_patient(db, patient_id)


@router.get("/status/{status}")
def list_invoices_by_status(status: str, db: Session = Depends(get_db)):
    """
    List PAID or UNPAID invoices
    """
    try:
        return InvoiceService.list_invoices_by_status(db, status.upper())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{invoice_id}/close")
def close_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Close (mark as PAID) an invoice
    """
    try:
        return InvoiceService.close_invoice(db, invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
