from sqlalchemy.orm import Session
from budget_line.budget_line_service import BudgetLineService
from budget_line.budget_line_schema import BudgetLineCreate

class BudgetLineController:

    @staticmethod
    def create(db: Session, data: BudgetLineCreate):
        return BudgetLineService.create_budget_line(db, data)

    @staticmethod
    def get(db: Session, budget_line_id: int):
        return BudgetLineService.get_budget_line(db, budget_line_id)

    @staticmethod
    def get_by_budget(db: Session, budget_id: int):
        return BudgetLineService.get_budget_lines_by_budget(db, budget_id)

    @staticmethod
    def update(db: Session, budget_line_id: int, data: dict):
        return BudgetLineService.update_budget_line(db, budget_line_id, data)

    @staticmethod
    def delete(db: Session, budget_line_id: int):
        return BudgetLineService.delete_budget_line(db, budget_line_id)
