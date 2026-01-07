from sqlalchemy.orm import Session
from bill_line.bill_line_models import BillLine
from bill_line.bill_line_repository import BillLineRepository
from bill_line.bill_line_schema import BillLineCreate

class BillLineService:

    @staticmethod
    def create_bill_line(db: Session, data: BillLineCreate):
        if data.amount <= 0:
            raise ValueError("Bill line amount must be positive")

        bill_line = BillLine(**data.dict())
        return BillLineRepository.create(db, bill_line)

    @staticmethod
    def get_bill_line(db: Session, bill_line_id: int):
        return BillLineRepository.get_by_id(db, bill_line_id)

    @staticmethod
    def get_bill_lines_by_bill(db: Session, bill_id: int):
        return BillLineRepository.get_by_bill(db, bill_id)

    @staticmethod
    def update_bill_line(db: Session, bill_line_id: int, data: dict):
        bill_line = BillLineRepository.get_by_id(db, bill_line_id)
        if not bill_line:
            raise ValueError("Bill line not found")

        return BillLineRepository.update(db, bill_line, data)

    @staticmethod
    def delete_bill_line(db: Session, bill_line_id: int):
        bill_line = BillLineRepository.get_by_id(db, bill_line_id)
        if not bill_line:
            raise ValueError("Bill line not found")

        return BillLineRepository.delete(db, bill_line)
