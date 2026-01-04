from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .Payment_controller import PaymentController
from .Payment_model import PaymentCreate, PaymentResponse
from database import get_db

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentController(db).create(data)


@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return PaymentController(db).get_all()


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return PaymentController(db).get_by_id(payment_id)


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentController(db).update(payment_id, data)


@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return PaymentController(db).delete(payment_id)
