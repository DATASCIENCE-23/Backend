from pydantic import BaseModel
from datetime import date
from typing import Optional

class JournalEntryCreate(BaseModel):
    journal_date: date
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    description: Optional[str] = None

class JournalEntryResponse(JournalEntryCreate):
    journal_id: int
    posted_status: bool

    class Config:
        orm_mode = True
