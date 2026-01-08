"""
Lab Schedule Schemas
Pydantic models for lab schedule request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum

from .base import BaseResponse


class ScheduleStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SampleTypeEnum(str, Enum):
    BLOOD = "blood"
    URINE = "urine"
    STOOL = "stool"
    SALIVA = "saliva"
    OTHER = "other"


class LabScheduleCreate(BaseModel):
    """Request model for creating lab schedules"""
    order_id: int = Field(..., gt=0, description="Lab order identifier")
    technician_id: int = Field(..., gt=0, description="Technician identifier")
    scheduled_datetime: datetime = Field(..., description="Scheduled appointment datetime")
    sample_type: Optional[SampleTypeEnum] = Field(SampleTypeEnum.BLOOD, description="Sample type")
    is_home_collection: Optional[bool] = Field(False, description="Home collection flag")
    notes: Optional[str] = Field(None, max_length=500, description="Schedule notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "technician_id": 1,
                "scheduled_datetime": "2024-01-15T10:00:00",
                "sample_type": "blood",
                "is_home_collection": False,
                "notes": "Patient prefers morning appointments"
            }
        }


class LabScheduleUpdate(BaseModel):
    """Request model for updating lab schedules"""
    scheduled_datetime: Optional[datetime] = None
    technician_id: Optional[int] = Field(None, gt=0)
    sample_type: Optional[SampleTypeEnum] = None
    is_home_collection: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "scheduled_datetime": "2024-01-16T14:00:00",
                "notes": "Rescheduled due to patient request"
            }
        }


class LabScheduleStatusUpdate(BaseModel):
    """Request model for updating lab schedule status"""
    status: ScheduleStatusEnum = Field(..., description="New status")
    notes: Optional[str] = Field(None, max_length=500, description="Status change notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_progress",
                "notes": "Sample collection started"
            }
        }


class LabScheduleResponse(BaseModel):
    """Response model for lab schedule data"""
    id: int
    order_id: int
    technician_id: int
    scheduled_datetime: datetime
    sample_type: SampleTypeEnum
    status: ScheduleStatusEnum
    is_home_collection: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "order_id": 1,
                "technician_id": 1,
                "scheduled_datetime": "2024-01-15T10:00:00Z",
                "sample_type": "blood",
                "status": "scheduled",
                "is_home_collection": False,
                "notes": "Patient prefers morning appointments",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        }


class AvailableSlotResponse(BaseModel):
    """Response model for available time slots"""
    datetime: datetime
    time: str
    available: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "datetime": "2024-01-15T10:00:00Z",
                "time": "10:00",
                "available": True
            }
        }