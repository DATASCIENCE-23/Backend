"""
Lab Order Schemas
Pydantic models for lab order request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

from .base import BaseResponse


class OrderPriorityEnum(str, Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    STAT = "stat"


class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LabOrderCreate(BaseModel):
    """Request model for creating lab orders"""
    patient_id: int = Field(..., gt=0, description="Patient identifier")
    doctor_id: int = Field(..., gt=0, description="Doctor identifier")
    medical_record_id: Optional[int] = Field(None, gt=0, description="Medical record identifier")
    test_names: str = Field(..., min_length=1, max_length=500, description="Test names")
    priority: Optional[OrderPriorityEnum] = Field(OrderPriorityEnum.NORMAL, description="Order priority")
    clinical_notes: Optional[str] = Field(None, max_length=1000, description="Clinical notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": 123,
                "doctor_id": 456,
                "medical_record_id": 789,
                "test_names": "Complete Blood Count, Lipid Panel",
                "priority": "normal",
                "clinical_notes": "Routine blood work for annual checkup"
            }
        }


class LabOrderUpdate(BaseModel):
    """Request model for updating lab orders"""
    priority: Optional[OrderPriorityEnum] = None
    clinical_notes: Optional[str] = Field(None, max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "priority": "urgent",
                "clinical_notes": "Patient experiencing symptoms, expedite processing"
            }
        }


class LabOrderStatusUpdate(BaseModel):
    """Request model for updating lab order status"""
    status: OrderStatusEnum = Field(..., description="New status")
    notes: Optional[str] = Field(None, max_length=500, description="Status change notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "scheduled",
                "notes": "Appointment scheduled for tomorrow morning"
            }
        }


class LabOrderResponse(BaseModel):
    """Response model for lab order data"""
    id: int
    patient_id: int
    doctor_id: int
    medical_record_id: Optional[int]
    test_names: str
    priority: OrderPriorityEnum
    status: OrderStatusEnum
    clinical_notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_id": 123,
                "doctor_id": 456,
                "medical_record_id": 789,
                "test_names": "Complete Blood Count, Lipid Panel",
                "priority": "normal",
                "status": "pending",
                "clinical_notes": "Routine blood work for annual checkup",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        }