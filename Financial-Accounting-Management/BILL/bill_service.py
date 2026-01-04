from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from BILL.bill_model import Bill
from BILL.bill_repository import BillRepository


class BillService:
    @staticmethod
    def get_bill(db: Session, bill_id: int) -> Optional[Bill]:
        bill = BillRepository.get_by_id(db, bill_id)
        if not bill:
            raise ValueError("Bill not found")
        return bill

    @staticmethod
    def list_all_bills(db: Session) -> List[Bill]:
        return BillRepository.get_all(db)

    @staticmethod
    def list_bills_by_vendor(db: Session, vendor_id: int) -> List[Bill]:
        return BillRepository.get_by_vendor(db, vendor_id)

    @staticmethod
    def list_bills_by_status(db: Session, status: str) -> List[Bill]:
        return BillRepository.get_by_status(db, status)

    @staticmethod
    def list_bills_by_date_range(
        db: Session, start_date: date, end_date: date
    ) -> List[Bill]:
        return BillRepository.get_by_date_range(db, start_date, end_date)

    @staticmethod
    def create_bill(db: Session, data: dict) -> Bill:
        bill = Bill(**data)
        return BillRepository.create(db, bill)

    @staticmethod
    def update_bill(db: Session, bill_id: int, data: dict) -> Bill:
        bill = BillRepository.get_by_id(db, bill_id)
        if not bill:
            raise ValueError("Bill not found")

        for key, value in data.items():
            if hasattr(bill, key):
                setattr(bill, key, value)

        return BillRepository.update(db, bill)

    @staticmethod
    def delete_bill(db: Session, bill_id: int) -> None:
        bill = BillRepository.get_by_id(db, bill_id)
        if not bill:
            raise ValueError("Bill not found")

        BillRepository.delete(db, bill)