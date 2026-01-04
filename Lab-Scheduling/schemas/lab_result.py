"""
Lab Result Schemas
Pydantic models for lab result request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

from .base import BaseResponse


class ResultStatusEnum(str, Enum):
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    REJECTED = "rejected"


class LabResultCreate(BaseModel):
    """Request model for creating lab results"""
    order_id: int = Field(..., gt=0, description="Lab order identifier")
    test_id: int = Field(..., gt=0, description="Test identifier")
    result_value: str = Field(..., min_length=1, max_length=200, description="Result value")
    unit: Optional[str] = Field(None, max_length=50, description="Unit of measurement")
    reference_range_min: Optional[float] = Field(None, description="Reference range minimum")
    reference_range_max: Optional[float] = Field(None, description="Reference range maximum")
    test_name: Optional[str] = Field(None, max_length=200, description="Test name")
    notes: Optional[str] = Field(None, max_length=500, description="Result notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "test_id": 1,
                "result_value": "7.2",
                "unit": "g/dL",
                "reference_range_min": 6.0,
                "reference_range_max": 8.0,
                "test_name": "Hemoglobin",
                "notes": "Normal result within reference range"
            }
        }


class LabResultUpdate(BaseModel):
    """Request model for updating lab results"""
    result_value: Optional[str] = Field(None, min_length=1, max_length=200)
    unit: Optional[str] = Field(None, max_length=50)
    reference_range_min: Optional[float] = None
    reference_range_max: Optional[float] = None
    test_name: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "result_value": "7.5",
                "notes": "Updated result after re-analysis"
            }
        }


class LabResultVerification(BaseModel):
    """Request model for verifying lab results"""
    verified_by: int = Field(..., gt=0, description="Verifier user ID")
    verification_notes: Optional[str] = Field(None, max_length=500, description="Verification notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "verified_by": 1,
                "verification_notes": "Result verified and approved"
            }
        }


class LabResultResponse(BaseModel):
    """Response model for lab result data"""
    id: int
    order_id: int
    test_id: int
    result_value: str
    numeric_value: Optional[float]
    unit: Optional[str]
    reference_range_min: Optional[float]
    reference_range_max: Optional[float]
    status: ResultStatusEnum
    is_abnormal: bool
    test_name: Optional[str]
    notes: Optional[str]
    verified_at: Optional[datetime]
    verified_by: Optional[int]
    verification_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "order_id": 1,
                "test_id": 1,
                "result_value": "7.2",
                "numeric_value": 7.2,
                "unit": "g/dL",
                "reference_range_min": 6.0,
                "reference_range_max": 8.0,
                "status": "verified",
                "is_abnormal": False,
                "test_name": "Hemoglobin",
                "notes": "Normal result within reference range",
                "verified_at": "2024-01-01T12:00:00Z",
                "verified_by": 1,
                "verification_notes": "Result verified and approved",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }