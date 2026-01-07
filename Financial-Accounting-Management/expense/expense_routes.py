from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from expense.expense_schema import ExpenseCreate, ExpenseResponse
from expense.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expense"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ExpenseResponse)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    return ExpenseService.create_expense(db, data)

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return ExpenseService.get_expense(db, expense_id)

@router.get("/", response_model=list[ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return ExpenseService.get_all_expenses(db)

@router.get("/by-department/{department_id}", response_model=list[ExpenseResponse])
def get_expenses_by_department(department_id: int, db: Session = Depends(get_db)):
    return ExpenseService.get_expenses_by_department(db, department_id)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, data: dict, db: Session = Depends(get_db)):
    return ExpenseService.update_expense(db, expense_id, data)

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    ExpenseService.delete_expense(db, expense_id)
    return {"message": "Expense deleted successfully"}
