from fastapi import APIRouter
from JOURNAL_ENTRY.journal_entry_controller import router as journal_entry_controller

router = APIRouter(
    prefix="/journal-entries",
    tags=["Journal Entries"]
)

router.include_router(journal_entry_controller)
