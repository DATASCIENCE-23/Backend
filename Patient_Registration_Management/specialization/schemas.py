from pydantic import BaseModel

class SpecializationCreate(BaseModel):
    specialization_name: str
    is_active: bool = True

class SpecializationUpdate(BaseModel):
    specialization_name: str | None = None
    is_active: bool | None = None

class SpecializationResponse(BaseModel):
    specialization_id: int
    specialization_name: str
    is_active: bool

    class Config:
        orm_mode = True
