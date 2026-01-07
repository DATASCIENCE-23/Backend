from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from budget.budget_schema import BudgetCreate, BudgetResponse
from budget.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["Budget"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BudgetResponse)
def create_budget(data: BudgetCreate, db: Session = Depends(get_db)):
    return BudgetService.create_budget(db, data)

@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    return BudgetService.get_budget(db, budget_id)

@router.get("/", response_model=list[BudgetResponse])
def get_all_budgets(db: Session = Depends(get_db)):
    return BudgetService.get_all_budgets(db)

@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(budget_id: int, data: dict, db: Session = Depends(get_db)):
    return BudgetService.update_budget(db, budget_id, data)

@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    BudgetService.delete_budget(db, budget_id)
    return {"message": "Budget deleted successfully"}
