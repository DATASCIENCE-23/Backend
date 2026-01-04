from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from EXPENSE.expense_model import Expense


class ExpenseRepository:
    @staticmethod
    def get_by_id(db: Session, expense_id: int) -> Optional[Expense]:
        return db.query(Expense).filter(Expense.expense_id == expense_id).first()

    @staticmethod
    def get_all(db: Session) -> List[Expense]:
        return db.query(Expense).all()

    @staticmethod
    def get_by_account(db: Session, account_id: int) -> List[Expense]:
        return db.query(Expense).filter(Expense.account_id == account_id).all()

    @staticmethod
    def get_by_department(db: Session, department: str) -> List[Expense]:
        return db.query(Expense).filter(Expense.department == department).all()

    @staticmethod
    def get_by_date_range(db: Session, start_date: date, end_date: date) -> List[Expense]:
        return db.query(Expense).filter(
            Expense.expense_date.between(start_date, end_date)
        ).all()

    @staticmethod
    def create(db: Session, expense: Expense) -> Expense:
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def update(db: Session, expense: Expense) -> Expense:
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def delete(db: Session, expense: Expense) -> None:
        db.delete(expense)
        db.commit()