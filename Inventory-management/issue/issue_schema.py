from pydantic import BaseModel, Field
from typing import List

class IssueItem(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)

class IssueCreate(BaseModel):
    department_id: int
    items: List[IssueItem]
