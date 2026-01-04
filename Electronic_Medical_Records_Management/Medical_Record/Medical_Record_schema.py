from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalRecordCreate(BaseModel):
    patient_id: int
    visit_id: Optional[int] = None
    chief_complaint: Optional[str] = None
    history_of_present_illness: Optional[str] = None
    past_medical_history: Optional[str] = None
    physical_examination: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordUpdate(BaseModel):
    chief_complaint: Optional[str] = None
    history_of_present_illness: Optional[str] = None
    past_medical_history: Optional[str] = None
    physical_examination: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_plan: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordResponse(BaseModel):
    record_id: int
    patient_id: int
    doctor_id: int
    visit_id: Optional[int]
    record_date: datetime

    class Config:
        from_attributes = True
