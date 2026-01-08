from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.utcnow()


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input data",
                    "details": "Field 'patient_id' is required"
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = 0
    limit: int = 100
    
    class Config:
        schema_extra = {
            "example": {
                "skip": 0,
                "limit": 50
            }
        }


class PaginatedResponse(BaseResponse):
    """Paginated response model"""
    total: int
    skip: int
    limit: int
    has_more: bool