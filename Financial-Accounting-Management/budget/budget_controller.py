from sqlalchemy.orm import Session
from budget.budget_service import BudgetService
from budget.budget_schema import BudgetCreate

class BudgetController:

    @staticmethod
    def create(db: Session, data: BudgetCreate):
        return BudgetService.create_budget(db, data)

    @staticmethod
    def get(db: Session, budget_id: int):
        return BudgetService.get_budget(db, budget_id)

    @staticmethod
    def get_all(db: Session):
        return BudgetService.get_all_budgets(db)

    @staticmethod
    def update(db: Session, budget_id: int, data: dict):
        return BudgetService.update_budget(db, budget_id, data)

    @staticmethod
    def delete(db: Session, budget_id: int):
        return BudgetService.delete_budget(db, budget_id)
