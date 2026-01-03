from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .Payment_service import PaymentService
from .Payment_model import PaymentCreate, PaymentResponse
from database import get_db


class PaymentController:

    def __init__(self, db: Session = Depends(get_db)):
        self.service = PaymentService(db)

    def create(self, data: PaymentCreate):
        return self.service.create_payment(data)

    def get_by_id(self, payment_id: int):
        payment = self.service.get_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

    def get_all(self):
        return self.service.get_all_payments()

    def update(self, payment_id: int, data: PaymentCreate):
        payment = self.service.update_payment(payment_id, data)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

    def delete(self, payment_id: int):
        success = self.service.delete_payment(payment_id)
        if not success:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"message": "Payment deleted successfully"}
