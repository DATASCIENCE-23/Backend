from sqlalchemy.orm import Session
from payment.payment_service import PaymentService
from payment.payment_schema import PaymentCreate

class PaymentController:

    @staticmethod
    def create(db: Session, data: PaymentCreate):
        return PaymentService.create_payment(db, data)

    @staticmethod
    def get(db: Session, payment_id: int):
        return PaymentService.get_payment(db, payment_id)

    @staticmethod
    def get_by_invoice(db: Session, invoice_id: int):
        return PaymentService.get_payments_by_invoice(db, invoice_id)

    @staticmethod
    def update(db: Session, payment_id: int, data: dict):
        return PaymentService.update_payment(db, payment_id, data)

    @staticmethod
    def delete(db: Session, payment_id: int):
        return PaymentService.delete_payment(db, payment_id)
