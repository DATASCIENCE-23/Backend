from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from PAYMENT.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def record_payment(payload: dict, db: Session = Depends(get_db)):
    """
    Record a payment against an invoice
    """
    try:
        return PaymentService.record_payment(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoice/{invoice_id}")
def list_payments(invoice_id: int, db: Session = Depends(get_db)):
    """
    List all payments for an invoice
    """
    return PaymentService.list_payments_for_invoice(db, invoice_id)


@router.get("/balance/{invoice_id}")
def calculate_balance(invoice_id: int, db: Session = Depends(get_db)):
    """
    Calculate outstanding balance for an invoice
    """
    try:
        return PaymentService.calculate_balance(db, invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/reconcile/{invoice_id}")
def reconcile_payment(invoice_id: int, db: Session = Depends(get_db)):
    """
    Reconcile invoice payment status (PAID / PARTIALLY_PAID)
    """
    try:
        return PaymentService.reconcile_payment(db, invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
