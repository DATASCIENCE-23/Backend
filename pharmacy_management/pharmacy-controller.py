"""
Pharmacy Module - Controllers (FastAPI Routers)
Handles HTTP requests and responses
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from auth import get_current_user, require_role
from schemas import (
    MedicineCreate, MedicineUpdate, MedicineResponse,
    MedicineBatchCreate, MedicineBatchResponse,
    PrescriptionCreate, PrescriptionResponse, PrescriptionListResponse,
    DispenseCreate, DispenseResponse,
    LowStockMedicine, StockValidationResponse,
    MessageResponse, ErrorResponse
)
from service import (
    MedicineService, MedicineBatchService,
    PrescriptionService, DispenseService
)
from exceptions import (
    DuplicateRecordException, NotFoundException,
    InsufficientStockException, ValidationException
)


# ============ MEDICINE MANAGEMENT ENDPOINTS ============

medicine_router = APIRouter(prefix="/api/pharmacy/medicines", tags=["Medicines"])


@medicine_router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(
    medicine_data: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "admin"]))
):
    """
    Create a new medicine (US-1: Add new medicine)
    Requires pharmacist or admin role
    """
    try:
        return MedicineService.create_medicine(db, medicine_data, current_user["user_id"])
    except DuplicateRecordException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@medicine_router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get medicine by ID with current stock information"""
    try:
        return MedicineService.get_medicine(db, medicine_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@medicine_router.put("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "admin"]))
):
    """
    Update medicine details (US-2: Update medicine details)
    Requires pharmacist or admin role
    """
    try:
        return MedicineService.update_medicine(db, medicine_id, medicine_data, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateRecordException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@medicine_router.get("/", response_model=List[MedicineResponse])
def search_medicines(
    search: Optional[str] = Query(None, description="Search by name or generic name"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Search medicines (US-3: View and search medicines)
    If search parameter is provided, returns filtered results, otherwise returns all
    """
    if search:
        return MedicineService.search_medicines(db, search)
    else:
        # Return all medicines (limited to 100)
        from repository import MedicineRepository
        medicines = MedicineRepository.get_all(db, limit=100)
        return [MedicineResponse.from_orm(med) for med in medicines]


@medicine_router.get("/stock/low", response_model=List[LowStockMedicine])
def get_low_stock_medicines(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "inventory_manager", "admin"]))
):
    """
    Get medicines with low stock (US-9: Low stock alert)
    For integration with inventory module
    """
    return MedicineService.get_low_stock_medicines(db)


# ============ MEDICINE BATCH ENDPOINTS ============

batch_router = APIRouter(prefix="/api/pharmacy/batches", tags=["Medicine Batches"])


@batch_router.post("/", response_model=MedicineBatchResponse, status_code=status.HTTP_201_CREATED)
def create_medicine_batch(
    batch_data: MedicineBatchCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "inventory_manager", "admin"]))
):
    """Create a new medicine batch"""
    try:
        return MedicineBatchService.create_batch(db, batch_data, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateRecordException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@batch_router.get("/medicine/{medicine_id}", response_model=List[MedicineBatchResponse])
def get_medicine_batches(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all active batches for a medicine"""
    return MedicineBatchService.get_batches_by_medicine(db, medicine_id)


# ============ PRESCRIPTION ENDPOINTS ============

prescription_router = APIRouter(prefix="/api/pharmacy/prescriptions", tags=["Prescriptions"])


@prescription_router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Receive prescription from doctor module (US-4: Receive prescription via web service)
    This endpoint is called by the doctor module API
    """
    try:
        return PrescriptionService.create_prescription(db, prescription_data)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@prescription_router.get("/pending", response_model=List[PrescriptionResponse])
def get_pending_prescriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "admin"]))
):
    """
    Get pending prescriptions (US-5: View pending prescriptions)
    Shows prescriptions ready for dispensing
    """
    return PrescriptionService.get_pending_prescriptions(db, skip, limit)


@prescription_router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get prescription details with item information"""
    try:
        return PrescriptionService.get_prescription(db, prescription_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@prescription_router.get("/{prescription_id}/validate-stock", response_model=StockValidationResponse)
def validate_prescription_stock(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "admin"]))
):
    """
    Validate stock availability (US-6: Validate stock before dispensing)
    Check if prescription can be fully or partially dispensed
    """
    try:
        return PrescriptionService.validate_stock_availability(db, prescription_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============ DISPENSE ENDPOINTS ============

dispense_router = APIRouter(prefix="/api/pharmacy/dispense", tags=["Dispensing"])


@dispense_router.post("/", response_model=DispenseResponse, status_code=status.HTTP_201_CREATED)
def dispense_medicines(
    dispense_data: DispenseCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["pharmacist", "admin"]))
):
    """
    Dispense medicines (US-7: Dispense medicines)
    Process medicine dispensing and update stock
    """
    try:
        return DispenseService.dispense_medicines(db, dispense_data, current_user["user_id"])
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientStockException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@dispense_router.get("/{dispense_id}", response_model=DispenseResponse)
def get_dispense(
    dispense_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get dispense details"""
    try:
        return DispenseService.get_dispense(db, dispense_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@dispense_router.get("/unbilled/list", response_model=List[dict])
def get_unbilled_dispenses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["billing", "pharmacist", "admin"]))
):
    """
    Get unbilled dispenses (US-8: Generate billable dispensing information)
    For billing module integration
    """
    return DispenseService.get_unbilled_dispenses(db)


@dispense_router.put("/{dispense_id}/mark-billed", response_model=DispenseResponse)
def mark_dispense_as_billed(
    dispense_id: int,
    invoice_id: int = Query(..., description="Invoice ID from billing module"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["billing", "admin"]))
):
    """
    Mark dispense as billed (US-8: Generate billable dispensing information)
    Called by billing module after invoice creation
    """
    try:
        return DispenseService.mark_as_billed(db, dispense_id, invoice_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============ HEALTH CHECK ============

health_router = APIRouter(prefix="/api/pharmacy", tags=["Health"])


@health_router.get("/health", response_model=MessageResponse)
def health_check():
    """Health check endpoint for pharmacy module"""
    return MessageResponse(message="Pharmacy module is running", success=True)