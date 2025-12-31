from sqlalchemy.orm import Session
from .payment_repository import PaymentRepository
from .payment_model import Payment, PaymentCreate


class PaymentService:

    def __init__(self, db: Session):
        self.repo = PaymentRepository(db)

    def create_payment(self, data: PaymentCreate):
        payment = Payment(**data.dict())
        return self.repo.create(payment)

    def get_payment(self, payment_id: int):
        return self.repo.get_by_id(payment_id)

    def get_all_payments(self):
        return self.repo.get_all()

    def update_payment(self, payment_id: int, data: PaymentCreate):
        payment = self.repo.get_by_id(payment_id)
        if not payment:
            return None

        for key, value in data.dict().items():
            setattr(payment, key, value)

        return self.repo.update(payment)

    def delete_payment(self, payment_id: int):
        payment = self.repo.get_by_id(payment_id)
        if not payment:
            return False

        self.repo.delete(payment)
        return True
