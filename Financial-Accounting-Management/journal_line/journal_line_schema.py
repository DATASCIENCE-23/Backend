from pydantic import BaseModel

class JournalLineCreate(BaseModel):
    journal_id: int
    account_id: int
    debit_amount: float = 0
    credit_amount: float = 0

class JournalLineResponse(JournalLineCreate):
    journal_line_id: int

    class Config:
        orm_mode = True
