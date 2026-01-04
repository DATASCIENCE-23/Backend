"""
Pharmacy Module - Medicine Routes
FastAPI endpoints for medicine & batch management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse,
    MedicineBatchCreate,
    MedicineBatchResponse,
    LowStockMedicine,
    MedicineSearchResponse,
)
from . import get_medicine_controller
from . import MedicineController

router = APIRouter(prefix="/pharmacy/medicines", tags=["Pharmacy - Medicines"])


# Helper to get controller (if you prefer not to use get_medicine_controller)
def _get_controller(db: Session = Depends(get_db)) -> MedicineController:
    return MedicineController(db)


# ---------- Medicine endpoints ----------


@router.post(
    "/",
    response_model=MedicineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_medicine(
    payload: MedicineCreate,
    controller: MedicineController = Depends(_get_controller),
    # in real app: user_id from auth
    user_id: int = 1,
):
    try:
        return controller.create_medicine(payload, user_id=user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{medicine_id}",
    response_model=MedicineResponse,
)
def get_medicine(
    medicine_id: int,
    controller: MedicineController = Depends(_get_controller),
):
    result = controller.get_medicine(medicine_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found",
        )
    return result


@router.get(
    "/",
    response_model=List[MedicineResponse],
)
def list_medicines(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    controller: MedicineController = Depends(_get_controller),
):
    return controller.list_medicines(skip=skip, limit=limit, active_only=active_only)


@router.get(
    "/search/",
    response_model=List[MedicineSearchResponse],
)
def search_medicines(
    q: str,
    active_only: bool = True,
    controller: MedicineController = Depends(_get_controller),
):
    return controller.search_medicines(term=q, active_only=active_only)


@router.put(
    "/{medicine_id}",
    response_model=MedicineResponse,
)
def update_medicine(
    medicine_id: int,
    payload: MedicineUpdate,
    controller: MedicineController = Depends(_get_controller),
    user_id: int = 1,
):
    try:
        result = controller.update_medicine(medicine_id, payload, user_id=user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found",
        )
    return result


@router.get(
    "/low-stock",
    response_model=List[LowStockMedicine],
)
def get_low_stock_medicines(
    controller: MedicineController = Depends(_get_controller),
):
    return controller.get_low_stock_medicines()


# ---------- Batch endpoints ----------


@router.post(
    "/{medicine_id}/batches",
    response_model=MedicineBatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_batch(
    medicine_id: int,
    payload: MedicineBatchCreate,
    controller: MedicineController = Depends(_get_controller),
):
    # Ensure path ID and body ID match
    if payload.medicine_id != medicine_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="medicine_id in path and body must match",
        )

    try:
        return controller.create_batch(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{medicine_id}/batches",
    response_model=List[MedicineBatchResponse],
)
def list_batches_for_medicine(
    medicine_id: int,
    active_only: bool = True,
    controller: MedicineController = Depends(_get_controller),
):
    return controller.list_batches_for_medicine(
        medicine_id=medicine_id, active_only=active_only
    )


@router.get(
    "/batches/{batch_id}",
    response_model=MedicineBatchResponse,
)
def get_batch(
    batch_id: int,
    controller: MedicineController = Depends(_get_controller),
):
    result = controller.get_batch(batch_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )
    return result


@router.post(
    "/batches/{batch_id}/adjust",
    response_model=MedicineBatchResponse,
)
def adjust_batch_stock(
    batch_id: int,
    quantity_change: int,
    controller: MedicineController = Depends(_get_controller),
):
    result = controller.update_batch_stock(batch_id, quantity_change)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )
    return result
