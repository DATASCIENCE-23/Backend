from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from BUDGET.database import get_db
from BUDGET.budget_service import BudgetService


router = APIRouter()

@router.post("/")
def create_budget(payload: dict, db: Session = Depends(get_db)):
    try:
        return BudgetService.create_budget(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{budget_id}")
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    try:
        return BudgetService.get_budget(db, budget_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_budgets(db: Session = Depends(get_db)):
    return BudgetService.list_budgets(db)


@router.put("/{budget_id}")
def update_budget(budget_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return BudgetService.update_budget(db, budget_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    try:
        BudgetService.delete_budget(db, budget_id)
        return {"message": "Budget deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
