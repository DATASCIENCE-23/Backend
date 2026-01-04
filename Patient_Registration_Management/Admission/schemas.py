from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AdmissionBase(BaseModel):
    appointment_id: int = Field(..., description="ID of the appointment")
    ward: Optional[str] = None
    bed_number: Optional[str] = None
    admission_reason: Optional[str] = None
    discharge_summary: Optional[str] = None
    status: Optional[str] = None

class AdmissionCreate(BaseModel):
    appointment_id: int
    ward: str
    bed_number: str
    admission_reason: str

class AdmissionUpdate(BaseModel):
    ward: Optional[str] = None
    bed_number: Optional[str] = None
    admission_reason: Optional[str] = None
    discharge_summary: Optional[str] = None
    status: Optional[str] = None

class AdmissionResponse(AdmissionBase):
    admission_id: int
    admission_datetime: datetime
    discharge_datetime: Optional[datetime] = None

    class Config:
        orm_mode = True
