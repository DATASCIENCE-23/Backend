from sqlalchemy.orm import Session
from expense.expense_models import Expense
from expense.expense_repository import ExpenseRepository
from expense.expense_schema import ExpenseCreate

class ExpenseService:

    @staticmethod
    def create_expense(db: Session, data: ExpenseCreate):
        if data.amount <= 0:
            raise ValueError("Expense amount must be positive")

        expense = Expense(**data.dict())
        return ExpenseRepository.create(db, expense)

    @staticmethod
    def get_expense(db: Session, expense_id: int):
        return ExpenseRepository.get_by_id(db, expense_id)

    @staticmethod
    def get_all_expenses(db: Session):
        return ExpenseRepository.get_all(db)

    @staticmethod
    def get_expenses_by_department(db: Session, department_id: int):
        return ExpenseRepository.get_by_department(db, department_id)

    @staticmethod
    def update_expense(db: Session, expense_id: int, data: dict):
        expense = ExpenseRepository.get_by_id(db, expense_id)
        if not expense:
            raise ValueError("Expense not found")

        return ExpenseRepository.update(db, expense, data)

    @staticmethod
    def delete_expense(db: Session, expense_id: int):
        expense = ExpenseRepository.get_by_id(db, expense_id)
        if not expense:
            raise ValueError("Expense not found")

        return ExpenseRepository.delete(db, expense)
