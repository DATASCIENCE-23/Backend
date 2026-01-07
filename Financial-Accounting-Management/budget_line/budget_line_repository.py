from sqlalchemy.orm import Session
from budget_line.budget_line_models import BudgetLine

class BudgetLineRepository:

    @staticmethod
    def create(db: Session, budget_line: BudgetLine):
        db.add(budget_line)
        db.commit()
        db.refresh(budget_line)
        return budget_line

    @staticmethod
    def get_by_id(db: Session, budget_line_id: int):
        return db.query(BudgetLine).filter(
            BudgetLine.budget_line_id == budget_line_id
        ).first()

    @staticmethod
    def get_by_budget(db: Session, budget_id: int):
        return db.query(BudgetLine).filter(
            BudgetLine.budget_id == budget_id
        ).all()

    @staticmethod
    def update(db: Session, budget_line: BudgetLine, data: dict):
        for key, value in data.items():
            setattr(budget_line, key, value)
        db.commit()
        db.refresh(budget_line)
        return budget_line

    @staticmethod
    def delete(db: Session, budget_line: BudgetLine):
        db.delete(budget_line)
        db.commit()
