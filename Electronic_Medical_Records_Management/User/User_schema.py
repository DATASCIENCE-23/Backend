from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    department_id: Optional[int] = None


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: Optional[str]
    status: str

    class Config:
        from_attributes = True
