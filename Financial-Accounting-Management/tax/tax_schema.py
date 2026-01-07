from pydantic import BaseModel

class TaxCreate(BaseModel):
    tax_name: str
    tax_rate: float
    account_id: int

class TaxResponse(TaxCreate):
    tax_id: int
    is_active: bool

    class Config:
        orm_mode = True
