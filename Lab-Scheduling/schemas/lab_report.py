"""
Lab Report Schemas
Pydantic models for lab report request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

from .base import BaseResponse


class ReportStatusEnum(str, Enum):
    DRAFT = "draft"
    PENDING_FINALIZATION = "pending_finalization"
    FINALIZED = "finalized"


class LabReportCreate(BaseModel):
    """Request model for creating lab reports"""
    order_id: int = Field(..., gt=0, description="Lab order identifier")
    summary: Optional[str] = Field(None, max_length=1000, description="Report summary")
    findings: Optional[str] = Field(None, max_length=2000, description="Report findings")
    recommendations: Optional[str] = Field(None, max_length=1000, description="Report recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "summary": "Complete blood count results",
                "findings": "All values within normal limits",
                "recommendations": "Continue current health regimen"
            }
        }


class LabReportUpdate(BaseModel):
    """Request model for updating lab reports"""
    summary: Optional[str] = Field(None, max_length=1000)
    findings: Optional[str] = Field(None, max_length=2000)
    recommendations: Optional[str] = Field(None, max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Updated complete blood count results",
                "findings": "All values within normal limits with minor variations"
            }
        }


class LabReportFinalization(BaseModel):
    """Request model for finalizing lab reports"""
    finalized_by: int = Field(..., gt=0, description="Finalizer user ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "finalized_by": 1
            }
        }


class LabReportResponse(BaseModel):
    """Response model for lab report data"""
    id: int
    order_id: int
    summary: Optional[str]
    findings: Optional[str]
    recommendations: Optional[str]
    status: ReportStatusEnum
    finalized_at: Optional[datetime]
    finalized_by: Optional[int]
    emr_integrated: bool
    emr_integration_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "order_id": 1,
                "summary": "Complete blood count results",
                "findings": "All values within normal limits",
                "recommendations": "Continue current health regimen",
                "status": "finalized",
                "finalized_at": "2024-01-01T15:00:00Z",
                "finalized_by": 1,
                "emr_integrated": True,
                "emr_integration_date": "2024-01-01T16:00:00Z",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T15:00:00Z"
            }
        }