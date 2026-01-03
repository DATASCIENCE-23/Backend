from sqlalchemy.orm import Session
from sqlalchemy import func
from PAYMENT.payment_model import Payment


class PaymentRepository:

    @staticmethod
    def create(db: Session, payment: Payment) -> Payment:
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def list_by_invoice(db: Session, invoice_id: int):
        return (
            db.query(Payment)
            .filter(Payment.invoice_id == invoice_id)
            .all()
        )

    @staticmethod
    def total_paid_for_invoice(db: Session, invoice_id: int) -> float:
        return (
            db.query(func.coalesce(func.sum(Payment.amount_paid), 0))
            .filter(Payment.invoice_id == invoice_id)
            .scalar()
        )
