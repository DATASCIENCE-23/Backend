from pydantic import BaseModel

class BudgetCreate(BaseModel):
    financial_year: str
    department_id: int
    total_amount: float

class BudgetResponse(BudgetCreate):
    budget_id: int

    class Config:
        orm_mode = True
