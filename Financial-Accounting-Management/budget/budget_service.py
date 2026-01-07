from sqlalchemy.orm import Session
from budget.budget_models import Budget
from budget.budget_repository import BudgetRepository
from budget.budget_schema import BudgetCreate

class BudgetService:

    @staticmethod
    def create_budget(db: Session, data: BudgetCreate):
        if data.total_amount <= 0:
            raise ValueError("Budget amount must be positive")

        budget = Budget(**data.dict())
        return BudgetRepository.create(db, budget)

    @staticmethod
    def get_budget(db: Session, budget_id: int):
        return BudgetRepository.get_by_id(db, budget_id)

    @staticmethod
    def get_all_budgets(db: Session):
        return BudgetRepository.get_all(db)

    @staticmethod
    def update_budget(db: Session, budget_id: int, data: dict):
        budget = BudgetRepository.get_by_id(db, budget_id)
        if not budget:
            raise ValueError("Budget not found")

        return BudgetRepository.update(db, budget, data)

    @staticmethod
    def delete_budget(db: Session, budget_id: int):
        budget = BudgetRepository.get_by_id(db, budget_id)
        if not budget:
            raise ValueError("Budget not found")

        return BudgetRepository.delete(db, budget)
