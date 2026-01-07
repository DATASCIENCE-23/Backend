from sqlalchemy.orm import Session
from budget_line.budget_line_models import BudgetLine
from budget_line.budget_line_repository import BudgetLineRepository
from budget_line.budget_line_schema import BudgetLineCreate

class BudgetLineService:

    @staticmethod
    def create_budget_line(db: Session, data: BudgetLineCreate):
        if data.allocated_amount <= 0:
            raise ValueError("Allocated amount must be positive")

        budget_line = BudgetLine(**data.dict())
        return BudgetLineRepository.create(db, budget_line)

    @staticmethod
    def get_budget_line(db: Session, budget_line_id: int):
        return BudgetLineRepository.get_by_id(db, budget_line_id)

    @staticmethod
    def get_budget_lines_by_budget(db: Session, budget_id: int):
        return BudgetLineRepository.get_by_budget(db, budget_id)

    @staticmethod
    def update_budget_line(db: Session, budget_line_id: int, data: dict):
        budget_line = BudgetLineRepository.get_by_id(db, budget_line_id)
        if not budget_line:
            raise ValueError("Budget line not found")

        return BudgetLineRepository.update(db, budget_line, data)

    @staticmethod
    def delete_budget_line(db: Session, budget_line_id: int):
        budget_line = BudgetLineRepository.get_by_id(db, budget_line_id)
        if not budget_line:
            raise ValueError("Budget line not found")

        return BudgetLineRepository.delete(db, budget_line)
