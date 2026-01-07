from sqlalchemy.orm import Session
from expense.expense_models import Expense

class ExpenseRepository:

    @staticmethod
    def create(db: Session, expense: Expense):
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def get_by_id(db: Session, expense_id: int):
        return db.query(Expense).filter(
            Expense.expense_id == expense_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Expense).all()

    @staticmethod
    def get_by_department(db: Session, department_id: int):
        return db.query(Expense).filter(
            Expense.department_id == department_id
        ).all()

    @staticmethod
    def update(db: Session, expense: Expense, data: dict):
        for key, value in data.items():
            setattr(expense, key, value)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def delete(db: Session, expense: Expense):
        db.delete(expense)
        db.commit()
