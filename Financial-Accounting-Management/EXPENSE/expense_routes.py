from fastapi import APIRouter
from EXPENSE.expense_controller import router as expense_controller

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

router.include_router(expense_controller)