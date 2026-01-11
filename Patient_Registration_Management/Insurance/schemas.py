from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class InsuranceBase(BaseModel):
    patient_id: int = Field(..., description="ID of the patient")
    provider_name: Optional[str] = None
    policy_number: str = Field(..., description="Unique policy number")
    coverage_type: Optional[str] = None
    coverage_percent: Optional[float] = Field(None, ge=0, le=100)
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: Optional[bool] = True

class InsuranceCreate(InsuranceBase):
    pass

class InsuranceUpdate(BaseModel):
    provider_name: Optional[str] = None
    policy_number: Optional[str] = None
    coverage_type: Optional[str] = None
    coverage_percent: Optional[float] = Field(None, ge=0, le=100)
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: Optional[bool] = None

class InsuranceResponse(InsuranceBase):
    insurance_id: int

    class Config:
        orm_mode = True
