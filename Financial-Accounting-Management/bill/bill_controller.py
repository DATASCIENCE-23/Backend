from sqlalchemy.orm import Session
from bill.bill_service import BillService
from bill.bill_schema import BillCreate

class BillController:

    @staticmethod
    def create(db: Session, data: BillCreate):
        return BillService.create_bill(db, data)

    @staticmethod
    def get(db: Session, bill_id: int):
        return BillService.get_bill(db, bill_id)

    @staticmethod
    def get_all(db: Session):
        return BillService.get_all_bills(db)

    @staticmethod
    def update(db: Session, bill_id: int, data: dict):
        return BillService.update_bill(db, bill_id, data)

    @staticmethod
    def delete(db: Session, bill_id: int):
        return BillService.delete_bill(db, bill_id)
