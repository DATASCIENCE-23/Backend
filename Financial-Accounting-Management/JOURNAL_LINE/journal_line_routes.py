from fastapi import APIRouter
from JOURNAL_LINE.journal_line_controller import router as journal_line_controller

router = APIRouter(
    prefix="/journal-lines",
    tags=["Journal Lines"]
)

router.include_router(journal_line_controller)
