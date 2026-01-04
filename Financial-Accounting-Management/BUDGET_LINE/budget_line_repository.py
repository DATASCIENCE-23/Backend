from sqlalchemy.orm import Session
from sqlalchemy import func
from .budget_line_model import BudgetLine

class BudgetLineRepository:

    @staticmethod
    def get_by_id(db: Session, budget_line_id: int):
        return db.query(BudgetLine).filter(
            BudgetLine.budget_line_id == budget_line_id
        ).first()

    @staticmethod
    def get_by_budget_id(db: Session, budget_id: int):
        return db.query(BudgetLine).filter(
            BudgetLine.budget_id == budget_id
        ).all()

    @staticmethod
    def get_total_allocated(db: Session, budget_id: int):
        total = db.query(
            func.coalesce(func.sum(BudgetLine.allocated_amount), 0)
        ).filter(
            BudgetLine.budget_id == budget_id
        ).scalar()
        return total

    @staticmethod
    def get_all(db: Session):
        return db.query(BudgetLine).all()

    @staticmethod
    def create(db: Session, line: BudgetLine):
        db.add(line)
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def update(db: Session, line: BudgetLine):
        db.commit()
        db.refresh(line)
        return line

    @staticmethod
    def delete(db: Session, line: BudgetLine):
        db.delete(line)
        db.commit()
