from sqlalchemy.orm import Session
from bill.bill_models import Bill
from bill.bill_repository import BillRepository
from bill.bill_schema import BillCreate

class BillService:

    @staticmethod
    def create_bill(db: Session, data: BillCreate):
        if data.total_amount < 0:
            raise ValueError("Bill amount cannot be negative")

        bill = Bill(**data.dict())
        return BillRepository.create(db, bill)

    @staticmethod
    def get_bill(db: Session, bill_id: int):
        return BillRepository.get_by_id(db, bill_id)

    @staticmethod
    def get_all_bills(db: Session):
        return BillRepository.get_all(db)

    @staticmethod
    def update_bill(db: Session, bill_id: int, data: dict):
        bill = BillRepository.get_by_id(db, bill_id)
        if not bill:
            raise ValueError("Bill not found")

        return BillRepository.update(db, bill, data)

    @staticmethod
    def delete_bill(db: Session, bill_id: int):
        bill = BillRepository.get_by_id(db, bill_id)
        if not bill:
            raise ValueError("Bill not found")

        return BillRepository.delete(db, bill)
