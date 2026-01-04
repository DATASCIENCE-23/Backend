from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from decimal import Decimal


# ---------- CREATE ----------
class DoctorCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    specialization_id: Optional[int] = None
    qualification: Optional[str] = None
    license_number: str
    phone_number: str
    email: Optional[EmailStr] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[Decimal] = None
    date_joined: Optional[date] = None
    date_of_birth: Optional[date] = None
    is_active: Optional[bool] = True


# ---------- UPDATE ----------
class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization_id: Optional[int] = None
    qualification: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[Decimal] = None
    date_joined: Optional[date] = None
    date_of_birth: Optional[date] = None
    is_active: Optional[bool] = None


# ---------- RESPONSE ----------
class DoctorResponse(BaseModel):
    doctor_id: int
    user_id: int
    first_name: str
    last_name: str
    specialization_id: Optional[int]
    qualification: Optional[str]
    license_number: str
    phone_number: str
    email: Optional[EmailStr]
    experience_years: Optional[int]
    consultation_fee: Optional[Decimal]
    date_joined: Optional[date]
    date_of_birth: Optional[date]
    is_active: bool

    class Config:
        from_attributes = True
