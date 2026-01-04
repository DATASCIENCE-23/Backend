from pydantic import BaseModel
from typing import Optional

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    pincode: str
    country: str
    patient_id: int

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None

class AddressResponse(BaseModel):
    address_id: int
    street: str
    city: str
    state: str
    pincode: str
    country: str
    patient_id: int

    class Config:
        orm_mode = True
