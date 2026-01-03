from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from BILL.bill_model import Bill


class BillRepository:

    @staticmethod
    def get_by_id(db: Session, bill_id: int) -> Optional[Bill]:
        return db.query(Bill).filter(Bill.bill_id == bill_id).first()

    @staticmethod
    def get_all(db: Session) -> List[Bill]:
        return db.query(Bill).all()

    @staticmethod
    def get_by_vendor(db: Session, vendor_id: int) -> List[Bill]:
        return db.query(Bill).filter(Bill.vendor_id == vendor_id).all()

    @staticmethod
    def get_by_status(db: Session, status: str) -> List[Bill]:
        return db.query(Bill).filter(Bill.status == status).all()

    @staticmethod
    def get_by_date_range(
        db: Session, start_date: date, end_date: date
    ) -> List[Bill]:
        return db.query(Bill).filter(
            Bill.bill_date.between(start_date, end_date)
        ).all()

    @staticmethod
    def create(db: Session, bill: Bill) -> Bill:
        db.add(bill)
        db.commit()
        db.refresh(bill)
        return bill

    @staticmethod
    def update(db: Session, bill: Bill) -> Bill:
        db.commit()
        db.refresh(bill)
        return bill

    @staticmethod
    def delete(db: Session, bill: Bill) -> None:
        db.delete(bill)
        db.commit()