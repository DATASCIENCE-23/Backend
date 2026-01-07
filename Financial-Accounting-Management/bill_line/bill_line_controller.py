from sqlalchemy.orm import Session
from bill_line.bill_line_service import BillLineService
from bill_line.bill_line_schema import BillLineCreate

class BillLineController:

    @staticmethod
    def create(db: Session, data: BillLineCreate):
        return BillLineService.create_bill_line(db, data)

    @staticmethod
    def get(db: Session, bill_line_id: int):
        return BillLineService.get_bill_line(db, bill_line_id)

    @staticmethod
    def get_by_bill(db: Session, bill_id: int):
        return BillLineService.get_bill_lines_by_bill(db, bill_id)

    @staticmethod
    def update(db: Session, bill_line_id: int, data: dict):
        return BillLineService.update_bill_line(db, bill_line_id, data)

    @staticmethod
    def delete(db: Session, bill_line_id: int):
        return BillLineService.delete_bill_line(db, bill_line_id)
