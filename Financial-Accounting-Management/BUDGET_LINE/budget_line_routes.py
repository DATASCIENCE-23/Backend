from fastapi import APIRouter
from BUDGET_LINE.budget_line_controller import router as budget_line_controller

router = APIRouter(
    prefix="/budget-lines",
    tags=["Budget Lines"]
)

router.include_router(budget_line_controller)
