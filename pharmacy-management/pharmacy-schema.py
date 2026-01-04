"""
Pharmacy Module - Pydantic Schemas (Data Transfer Objects)
Used for API request/response validation and serialization
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


# ============ ENUMS ============

class MedicineStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class PrescriptionStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    CANCELLED = "cancelled"


class DispenseStatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    BILLED = "billed"


# ============ MEDICINE SCHEMAS ============

class MedicineCreate(BaseModel):
    medicine_name: str = Field(..., min_length=1, max_length=200)
    generic_name: str = Field(..., min_length=1, max_length=200)
    strength: str = Field(..., min_length=1, max_length=50)
    form: str = Field(..., min_length=1, max_length=50)
    shelf_location: Optional[str] = Field(None, max_length=50)
    unit_price: Decimal = Field(..., gt=0, decimal_places=2)
    min_quantity: int = Field(default=10, ge=0)
    reorder_level: int = Field(default=20, ge=0)


class MedicineUpdate(BaseModel):
    medicine_name: Optional[str] = Field(None, min_length=1, max_length=200)
    generic_name: Optional[str] = Field(None, min_length=1, max_length=200)
    strength: Optional[str] = Field(None, min_length=1, max_length=50)
    form: Optional[str] = Field(None, min_length=1, max_length=50)
    shelf_location: Optional[str] = Field(None, max_length=50)
    unit_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    is_active: Optional[bool] = None
    min_quantity: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)


class MedicineResponse(BaseModel):
    medicine_id: int
    medicine_name: str
    generic_name: str
    strength: str
    form: str
    shelf_location: Optional[str]
    unit_price: Decimal
    is_active: bool
    min_quantity: int
    reorder_level: int
    created_at: datetime
    updated_at: datetime
    total_stock: Optional[int] = None  # Calculated field
    
    class Config:
        from_attributes = True


class MedicineSearchResponse(BaseModel):
    medicine_id: int
    medicine_name: str
    generic_name: str
    strength: str
    form: str
    unit_price: Decimal
    is_active: bool
    available_quantity: int
    nearest_expiry: Optional[date]
    
    class Config:
        from_attributes = True


# ============ MEDICINE BATCH SCHEMAS ============

class MedicineBatchCreate(BaseModel):
    medicine_id: int
    batch_number: str = Field(..., min_length=1, max_length=50)
    quantity_in_stock: int = Field(..., ge=0)
    manufacture_date: date
    expiry_date: date
    purchase_price: Decimal = Field(..., gt=0, decimal_places=2)
    
    @validator('expiry_date')
    def expiry_must_be_after_manufacture(cls, v, values):
        if 'manufacture_date' in values and v <= values['manufacture_date']:
            raise ValueError('Expiry date must be after manufacture date')
        return v


class MedicineBatchResponse(BaseModel):
    batch_id: int
    medicine_id: int
    batch_number: str
    quantity_in_stock: int
    manufacture_date: date
    expiry_date: date
    purchase_price: Decimal
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ PRESCRIPTION SCHEMAS ============

class PrescriptionItemCreate(BaseModel):
    medicine_id: int
    prescribed_quantity: int = Field(..., gt=0)
    dosage: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., min_length=1, max_length=100)
    duration_days: int = Field(..., gt=0)
    instructions: Optional[str] = None


class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    record_id: Optional[int] = None
    notes: Optional[str] = None
    external_ref: Optional[str] = None
    items: List[PrescriptionItemCreate] = Field(..., min_items=1)


class PrescriptionItemResponse(BaseModel):
    prescription_item_id: int
    medicine_id: int
    medicine_name: str
    generic_name: str
    strength: str
    form: str
    prescribed_quantity: int
    dosage: str
    frequency: str
    duration_days: int
    instructions: Optional[str]
    available_quantity: int  # Calculated from stock
    unit_price: Decimal
    
    class Config:
        from_attributes = True


class PrescriptionResponse(BaseModel):
    prescription_id: int
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    created_at: datetime
    status: PrescriptionStatusEnum
    notes: Optional[str]
    items: List[PrescriptionItemResponse]
    
    class Config:
        from_attributes = True


class PrescriptionListResponse(BaseModel):
    prescription_id: int
    patient_id: int
    patient_name: str
    doctor_id: int
    doctor_name: str
    created_at: datetime
    status: PrescriptionStatusEnum
    total_items: int
    
    class Config:
        from_attributes = True


# ============ DISPENSE SCHEMAS ============

class DispenseItemCreate(BaseModel):
    prescription_item_id: int
    batch_id: int
    dispensed_quantity: int = Field(..., gt=0)


class DispenseCreate(BaseModel):
    prescription_id: int
    pharmacist_id: int
    notes: Optional[str] = None
    items: List[DispenseItemCreate] = Field(..., min_items=1)


class DispenseItemResponse(BaseModel):
    dispense_item_id: int
    prescription_item_id: int
    medicine_name: str
    batch_number: str
    dispensed_quantity: int
    unit_price: Decimal
    line_total: Decimal
    
    class Config:
        from_attributes = True


class DispenseResponse(BaseModel):
    dispense_id: int
    prescription_id: int
    pharmacist_id: int
    pharmacist_name: str
    dispensed_at: datetime
    total_amount: Decimal
    status: DispenseStatusEnum
    notes: Optional[str]
    items: List[DispenseItemResponse]
    
    class Config:
        from_attributes = True


class DispenseBillingInfo(BaseModel):
    """Schema for billing module integration"""
    dispense_id: int
    prescription_id: int
    patient_id: int
    dispensed_at: datetime
    total_amount: Decimal
    items: List[DispenseItemResponse]
    is_billed: bool
    
    class Config:
        from_attributes = True


# ============ LOW STOCK SCHEMAS ============

class LowStockMedicine(BaseModel):
    medicine_id: int
    medicine_name: str
    generic_name: str
    strength: str
    form: str
    available_quantity: int
    min_quantity: int
    reorder_level: int
    deficit: int  # How much below reorder level
    
    class Config:
        from_attributes = True


# ============ STOCK AVAILABILITY SCHEMA ============

class StockAvailability(BaseModel):
    medicine_id: int
    medicine_name: str
    total_available: int
    batches: List[dict]  # List of batch info with quantities and expiry
    
    class Config:
        from_attributes = True


# ============ VALIDATION RESPONSE ============

class StockValidationResponse(BaseModel):
    prescription_id: int
    can_dispense_fully: bool
    validation_items: List[dict]  # Each item with medicine_id, requested, available, can_fulfill
    
    class Config:
        from_attributes = True


# ============ GENERIC RESPONSE ============

class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    success: bool = False