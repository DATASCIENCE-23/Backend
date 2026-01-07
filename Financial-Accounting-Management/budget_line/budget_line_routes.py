from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from budget_line.budget_line_schema import BudgetLineCreate, BudgetLineResponse
from budget_line.budget_line_service import BudgetLineService

router = APIRouter(prefix="/budget-lines", tags=["Budget Line"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BudgetLineResponse)
def create_budget_line(data: BudgetLineCreate, db: Session = Depends(get_db)):
    return BudgetLineService.create_budget_line(db, data)

@router.get("/{budget_line_id}", response_model=BudgetLineResponse)
def get_budget_line(budget_line_id: int, db: Session = Depends(get_db)):
    return BudgetLineService.get_budget_line(db, budget_line_id)

@router.get("/by-budget/{budget_id}", response_model=list[BudgetLineResponse])
def get_budget_lines_by_budget(budget_id: int, db: Session = Depends(get_db)):
    return BudgetLineService.get_budget_lines_by_budget(db, budget_id)

@router.put("/{budget_line_id}", response_model=BudgetLineResponse)
def update_budget_line(budget_line_id: int, data: dict, db: Session = Depends(get_db)):
    return BudgetLineService.update_budget_line(db, budget_line_id, data)

@router.delete("/{budget_line_id}")
def delete_budget_line(budget_line_id: int, db: Session = Depends(get_db)):
    BudgetLineService.delete_budget_line(db, budget_line_id)
    return {"message": "Budget line deleted successfully"}
