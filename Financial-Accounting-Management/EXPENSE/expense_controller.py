# EXPENSE/expense_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from EXPENSE.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_expense(payload: dict, db: Session = Depends(get_db)):
    try:
        return ExpenseService.create_expense(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    try:
        return ExpenseService.get_expense(db, expense_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_all_expenses(db: Session = Depends(get_db)):
    return ExpenseService.list_all_expenses(db)


@router.get("/account/{account_id}")
def list_expenses_by_account(account_id: int, db: Session = Depends(get_db)):
    return ExpenseService.list_expenses_by_account(db, account_id)


@router.get("/department/{department}")
def list_expenses_by_department(department: str, db: Session = Depends(get_db)):
    return ExpenseService.list_expenses_by_department(db, department)


@router.get("/date-range/")
def list_expenses_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    return ExpenseService.list_expenses_by_date_range(db, start_date, end_date)


@router.put("/{expense_id}")
def update_expense(expense_id: int, payload: dict, db: Session = Depends(get_db)):
    try:
        return ExpenseService.update_expense(db, expense_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    try:
        ExpenseService.delete_expense(db, expense_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))