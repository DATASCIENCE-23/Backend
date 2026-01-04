from sqlalchemy.orm import Session

from BUDGET.budget_model import Budget
from BUDGET.budget_repository import BudgetRepository

from BUDGET_LINE.budget_line_repository import BudgetLineRepository


class BudgetService:

    @staticmethod
    def create_budget(db: Session, data: dict):
        existing = BudgetRepository.get_by_year_and_department(
            db, data["financial_year"], data["department"]
        )
        if existing:
            raise ValueError("Budget already exists for this department and year")

        budget = Budget(**data)
        return BudgetRepository.create(db, budget)

    @staticmethod
    def get_budget(db: Session, budget_id: int):
        budget = BudgetRepository.get_by_id(db, budget_id)
        if not budget:
            raise ValueError("Budget not found")
        return budget

    @staticmethod
    def list_budgets(db: Session):
        return BudgetRepository.get_all(db)

    @staticmethod
    def update_budget(db: Session, budget_id: int, data: dict):
        budget = BudgetRepository.get_by_id(db, budget_id)
        if not budget:
            raise ValueError("Budget not found")

        allocated = BudgetLineRepository.get_total_allocated(db, budget_id)
        if "total_amount" in data and data["total_amount"] < allocated:
            raise ValueError("Total budget cannot be less than allocated amount")

        for key, value in data.items():
            setattr(budget, key, value)

        return BudgetRepository.update(db, budget)

    @staticmethod
    def delete_budget(db: Session, budget_id: int):
        budget = BudgetRepository.get_by_id(db, budget_id)
        if not budget:
            raise ValueError("Budget not found")

        BudgetRepository.delete(db, budget)
