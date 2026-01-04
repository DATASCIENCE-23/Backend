from sqlalchemy.orm import Session
from BUDGET.budget_model import Budget

class BudgetRepository:

    @staticmethod
    def get_by_id(db: Session, budget_id: int):
        return db.query(Budget).filter(Budget.budget_id == budget_id).first()

    @staticmethod
    def get_by_year_and_department(db: Session, financial_year: str, department: str):
        return db.query(Budget).filter(
            Budget.financial_year == financial_year,
            Budget.department == department
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Budget).all()

    @staticmethod
    def create(db: Session, budget: Budget):
        db.add(budget)
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def update(db: Session, budget: Budget):
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def delete(db: Session, budget: Budget):
        db.delete(budget)
        db.commit()
