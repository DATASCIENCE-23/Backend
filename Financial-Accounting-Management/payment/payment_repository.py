from sqlalchemy.orm import Session
from payment.payment_models import Payment

class PaymentRepository:

    @staticmethod
    def create(db: Session, payment: Payment):
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_by_id(db: Session, payment_id: int):
        return db.query(Payment).filter(
            Payment.payment_id == payment_id
        ).first()

    @staticmethod
    def get_by_invoice(db: Session, invoice_id: int):
        return db.query(Payment).filter(
            Payment.invoice_id == invoice_id
        ).all()

    @staticmethod
    def update(db: Session, payment: Payment, data: dict):
        for key, value in data.items():
            setattr(payment, key, value)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def delete(db: Session, payment: Payment):
        db.delete(payment)
        db.commit()
