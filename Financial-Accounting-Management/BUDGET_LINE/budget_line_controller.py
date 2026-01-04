from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from BUDGET_LINE.database import get_db
from BUDGET_LINE.budget_line_service import BudgetLineService


router = APIRouter()

@router.post("/")
def create_budget_line(payload: dict, db: Session = Depends(get_db)):
    try:
        return BudgetLineService.create_budget_line(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{budget_line_id}")
def get_budget_line(budget_line_id: int, db: Session = Depends(get_db)):
    try:
        return BudgetLineService.get_budget_line(db, budget_line_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_budget_lines(db: Session = Depends(get_db)):
    return BudgetLineService.list_budget_lines(db)


@router.put("/{budget_line_id}")
def update_budget_line(budget_line_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return BudgetLineService.update_budget_line(db, budget_line_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{budget_line_id}")
def delete_budget_line(budget_line_id: int, db: Session = Depends(get_db)):
    try:
        BudgetLineService.delete_budget_line(db, budget_line_id)
        return {"message": "Budget line deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
