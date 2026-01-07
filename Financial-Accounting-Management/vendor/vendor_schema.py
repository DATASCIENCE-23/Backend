from pydantic import BaseModel
from typing import Optional

class VendorCreate(BaseModel):
    vendor_name: str
    contact_info: Optional[str] = None
    gst_number: Optional[str] = None

class VendorResponse(VendorCreate):
    vendor_id: int
    is_active: bool

    class Config:
        orm_mode = True
