from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from payment.payment_schema import PaymentCreate, PaymentResponse
from payment.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payment"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PaymentResponse)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentService.create_payment(db, data)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return PaymentService.get_payment(db, payment_id)

@router.get("/by-invoice/{invoice_id}", response_model=list[PaymentResponse])
def get_payments_by_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return PaymentService.get_payments_by_invoice(db, invoice_id)

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, data: dict, db: Session = Depends(get_db)):
    return PaymentService.update_payment(db, payment_id, data)

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    PaymentService.delete_payment(db, payment_id)
    return {"message": "Payment deleted successfully"}
