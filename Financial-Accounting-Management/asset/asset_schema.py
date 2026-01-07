from pydantic import BaseModel
from datetime import date

class AssetCreate(BaseModel):
    asset_name: str
    purchase_date: date
    purchase_cost: float
    useful_life_years: int
    salvage_value: float = 0

class AssetResponse(AssetCreate):
    asset_id: int

    class Config:
        orm_mode = True
