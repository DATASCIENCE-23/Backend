from sqlalchemy.orm import Session

from BUDGET_LINE.budget_line_model import BudgetLine
from BUDGET_LINE.budget_line_repository import BudgetLineRepository

from BUDGET.budget_repository import BudgetRepository

class BudgetLineService:

    @staticmethod
    def create_budget_line(db: Session, data: dict):
        budget = BudgetRepository.get_by_id(db, data["budget_id"])
        if not budget:
            raise ValueError("Budget not found")

        allocated = BudgetLineRepository.get_total_allocated(db, data["budget_id"])
        if allocated + data["allocated_amount"] > budget.total_amount:
            raise ValueError("Allocated amount exceeds total budget")

        line = BudgetLine(**data)
        return BudgetLineRepository.create(db, line)

    @staticmethod
    def get_budget_line(db: Session, budget_line_id: int):
        line = BudgetLineRepository.get_by_id(db, budget_line_id)
        if not line:
            raise ValueError("Budget line not found")
        return line

    @staticmethod
    def list_budget_lines(db: Session):
        return BudgetLineRepository.get_all(db)

    @staticmethod
    def update_budget_line(db: Session, budget_line_id: int, data: dict):
        line = BudgetLineRepository.get_by_id(db, budget_line_id)
        if not line:
            raise ValueError("Budget line not found")

        budget = BudgetRepository.get_by_id(db, line.budget_id)
        current_allocated = BudgetLineRepository.get_total_allocated(db, budget.budget_id)
        new_amount = data.get("allocated_amount", line.allocated_amount)

        if current_allocated - line.allocated_amount + new_amount > budget.total_amount:
            raise ValueError("Allocated amount exceeds total budget")

        for key, value in data.items():
            setattr(line, key, value)

        return BudgetLineRepository.update(db, line)

    @staticmethod
    def delete_budget_line(db: Session, budget_line_id: int):
        line = BudgetLineRepository.get_by_id(db, budget_line_id)
        if not line:
            raise ValueError("Budget line not found")

        BudgetLineRepository.delete(db, line)
