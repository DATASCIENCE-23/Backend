from sqlalchemy.orm import Session
from bill_line.bill_line_models import BillLine

class BillLineRepository:

    @staticmethod
    def create(db: Session, bill_line: BillLine):
        db.add(bill_line)
        db.commit()
        db.refresh(bill_line)
        return bill_line

    @staticmethod
    def get_by_id(db: Session, bill_line_id: int):
        return db.query(BillLine).filter(
            BillLine.bill_line_id == bill_line_id
        ).first()

    @staticmethod
    def get_by_bill(db: Session, bill_id: int):
        return db.query(BillLine).filter(
            BillLine.bill_id == bill_id
        ).all()

    @staticmethod
    def update(db: Session, bill_line: BillLine, data: dict):
        for key, value in data.items():
            setattr(bill_line, key, value)
        db.commit()
        db.refresh(bill_line)
        return bill_line

    @staticmethod
    def delete(db: Session, bill_line: BillLine):
        db.delete(bill_line)
        db.commit()
