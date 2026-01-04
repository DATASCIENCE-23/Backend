from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from EXPENSE.expense_model import Expense
from EXPENSE.expense_repository import ExpenseRepository


class ExpenseService:
    @staticmethod
    def get_expense(db: Session, expense_id: int) -> Optional[Expense]:
        expense = ExpenseRepository.get_by_id(db, expense_id)
        if not expense:
            raise ValueError("Expense not found")
        return expense

    @staticmethod
    def list_all_expenses(db: Session) -> List[Expense]:
        return ExpenseRepository.get_all(db)

    @staticmethod
    def list_expenses_by_account(db: Session, account_id: int) -> List[Expense]:
        return ExpenseRepository.get_by_account(db, account_id)

    @staticmethod
    def list_expenses_by_department(db: Session, department: str) -> List[Expense]:
        return ExpenseRepository.get_by_department(db, department)

    @staticmethod
    def list_expenses_by_date_range(
        db: Session, start_date: date, end_date: date
    ) -> List[Expense]:
        return ExpenseRepository.get_by_date_range(db, start_date, end_date)

    @staticmethod
    def create_expense(db: Session, data: dict) -> Expense:
        expense = Expense(**data)
        return ExpenseRepository.create(db, expense)

    @staticmethod
    def update_expense(db: Session, expense_id: int, data: dict) -> Expense:
        expense = ExpenseRepository.get_by_id(db, expense_id)
        if not expense:
            raise ValueError("Expense not found")

        for key, value in data.items():
            if hasattr(expense, key):
                setattr(expense, key, value)

        return ExpenseRepository.update(db, expense)

    @staticmethod
    def delete_expense(db: Session, expense_id: int) -> None:
        expense = ExpenseRepository.get_by_id(db, expense_id)
        if not expense:
            raise ValueError("Expense not found")

        ExpenseRepository.delete(db, expense)