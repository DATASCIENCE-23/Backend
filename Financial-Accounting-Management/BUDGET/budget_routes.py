from fastapi import APIRouter
from BUDGET.budget_controller import router as budget_controller

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

router.include_router(budget_controller)
