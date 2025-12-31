from sqlalchemy.orm import Session
from .payment_model import Payment


class PaymentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, payment: Payment):
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_by_id(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.payment_id == payment_id).first()

    def get_all(self):
        return self.db.query(Payment).all()

    def update(self, payment: Payment):
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def delete(self, payment: Payment):
        self.db.delete(payment)
        self.db.commit()
