from sqlalchemy.orm import Session
from bill.bill_models import Bill

class BillRepository:

    @staticmethod
    def create(db: Session, bill: Bill):
        db.add(bill)
        db.commit()
        db.refresh(bill)
        return bill

    @staticmethod
    def get_by_id(db: Session, bill_id: int):
        return db.query(Bill).filter(Bill.bill_id == bill_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Bill).all()

    @staticmethod
    def update(db: Session, bill: Bill, data: dict):
        for key, value in data.items():
            setattr(bill, key, value)
        db.commit()
        db.refresh(bill)
        return bill

    @staticmethod
    def delete(db: Session, bill: Bill):
        db.delete(bill)
        db.commit()
