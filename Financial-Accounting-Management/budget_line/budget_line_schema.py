from pydantic import BaseModel

class BudgetLineCreate(BaseModel):
    budget_id: int
    account_id: int
    allocated_amount: float

class BudgetLineResponse(BudgetLineCreate):
    budget_line_id: int

    class Config:
        orm_mode = True
