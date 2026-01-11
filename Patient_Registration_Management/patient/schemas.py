from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime


class PatientCreate(BaseModel):
    hospital_id: str
    first_name: str
    last_name: Optional[str] = None
    date_of_birth: date
    gender: str  # "Male", "Female", "Other"
    blood_group: Optional[str] = None
    phone_number: str
    email: Optional[EmailStr] = None
    marital_status: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    registration_date: Optional[datetime] = None
    patient_type: Optional[str] = None
    medical_record_number: str
    user_id: int
    is_active: Optional[bool] = True


class PatientUpdate(BaseModel):
    hospital_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    marital_status: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    registration_date: Optional[datetime] = None
    patient_type: Optional[str] = None
    medical_record_number: Optional[str] = None
    is_active: Optional[bool] = None


class PatientResponse(BaseModel):
    patient_id: int
    hospital_id: str
    first_name: str
    last_name: Optional[str]
    date_of_birth: date
    gender: str
    phone_number: str
    email: Optional[EmailStr]
    is_active: bool

    class Config:
        orm_mode = True
