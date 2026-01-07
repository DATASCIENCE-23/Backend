from sqlalchemy.orm import Session
from budget.budget_models import Budget

class BudgetRepository:

    @staticmethod
    def create(db: Session, budget: Budget):
        db.add(budget)
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def get_by_id(db: Session, budget_id: int):
        return db.query(Budget).filter(Budget.budget_id == budget_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Budget).all()

    @staticmethod
    def update(db: Session, budget: Budget, data: dict):
        for key, value in data.items():
            setattr(budget, key, value)
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def delete(db: Session, budget: Budget):
        db.delete(budget)
        db.commit()
