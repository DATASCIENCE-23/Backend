from sqlalchemy.orm import Session
from expense.expense_service import ExpenseService
from expense.expense_schema import ExpenseCreate

class ExpenseController:

    @staticmethod
    def create(db: Session, data: ExpenseCreate):
        return ExpenseService.create_expense(db, data)

    @staticmethod
    def get(db: Session, expense_id: int):
        return ExpenseService.get_expense(db, expense_id)

    @staticmethod
    def get_all(db: Session):
        return ExpenseService.get_all_expenses(db)

    @staticmethod
    def get_by_department(db: Session, department_id: int):
        return ExpenseService.get_expenses_by_department(db, department_id)

    @staticmethod
    def update(db: Session, expense_id: int, data: dict):
        return ExpenseService.update_expense(db, expense_id, data)

    @staticmethod
    def delete(db: Session, expense_id: int):
        return ExpenseService.delete_expense(db, expense_id)
