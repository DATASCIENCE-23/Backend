"""
Pharmacy package root
Exports ORM models and schemas for easy import.
"""

# MODELS
from .medicine import Medicine, MedicineBatch,  MedicineRepository, MedicineBatchRepository, MedicineService, MedicineController, get_medicine_controller
from .dispense import Dispense, DispenseItem, DispenseRepository, DispenseItemRepository, DispenseService, DispenseController
from .pharmacist import Pharmacist, PharmacistRepository, PharmacistService, PharmacistController, get_pharmacist_controller
from .audit import PharmacyAuditLog, PharmacyAuditRepository, PharmacyAuditService, PharmacyAuditController



# SCHEMAS (pharmacy-schema.py)
from .schemas import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse,
    MedicineSearchResponse,
    MedicineBatchCreate,
    MedicineBatchResponse,
    DispenseCreate,
    DispenseResponse,
    DispenseItemCreate,
    DispenseItemResponse,
    DispenseBillingInfo,
    LowStockMedicine,
    StockAvailability,
    StockValidationResponse,
    MessageResponse,
    ErrorResponse,
    MedicineStatusEnum,
    PrescriptionStatusEnum,
    DispenseStatusEnum,
)

__all__ = [
    # models
    "Medicine",
    "MedicineBatch",
    "Dispense",
    "DispenseItem",
    "Pharmacist",
    "PharmacyAuditLog",
    #repositories
    "MedicineRepository",
    "MedicineBatchRepository",
    "DispenseRepository",
    "DispenseItemRepository",
    "PharmacistRepository",
    "PharmacyAuditLogRepository",
    #services
    "MedicineService",
    "DispenseService",
    "PharmacistService",
    "PharmacyAuditService",
    #controllers
    "MedicineController",
    "DispenseController",
    "PharmacistController",
    "PharmacyAuditController",
    #configurations
    "get_medicine_controller",
    "get_pharmacist_controller",
    # schemas
    "MedicineCreate",
    "MedicineUpdate",
    "MedicineResponse",
    "MedicineSearchResponse",
    "MedicineBatchCreate",
    "MedicineBatchResponse",
    "DispenseCreate",
    "DispenseResponse",
    "DispenseItemCreate",
    "DispenseItemResponse",
    "DispenseBillingInfo",
    "LowStockMedicine",
    "StockAvailability",
    "StockValidationResponse",
    "MessageResponse",
    "ErrorResponse",
    "MedicineStatusEnum",
    "PrescriptionStatusEnum",
    "DispenseStatusEnum",
    
]
