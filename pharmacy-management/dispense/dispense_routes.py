"""
Pharmacy Module - Dispense Routes
FastAPI endpoints for dispensing operations
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from .. import (
    DispenseCreate,
    DispenseResponse,
    DispenseItemResponse,
    DispenseBillingInfo,
)
from . import get_dispense_controller
from .import DispenseController

router = APIRouter(prefix="/pharmacy/dispense", tags=["Pharmacy - Dispense"])


# ----- Helpers -----
def _get_controller(
    db: Session = Depends(get_db),
) -> DispenseController:
    return DispenseController(db)


# ----- Main dispense endpoints -----


@router.post(
    "/",
    response_model=DispenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_dispense(
    payload: DispenseCreate,
    db: Session = Depends(get_db),
    # in real app, pharmacist_id comes from auth user
    pharmacist_id: int = 1,
):
    controller = DispenseController(db)
    dispense = controller.create_dispense(payload, pharmacist_id=pharmacist_id)
    return dispense


@router.get(
    "/{dispense_id}",
    response_model=DispenseResponse,
)
def get_dispense(
    dispense_id: int,
    controller: DispenseController = Depends(_get_controller),
):
    result = controller.get_dispense(dispense_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispense not found",
        )
    return result


@router.get(
    "/prescription/{prescription_id}",
    response_model=List[DispenseResponse],
)
def list_dispenses_for_prescription(
    prescription_id: int,
    controller: DispenseController = Depends(_get_controller),
):
    return controller.list_dispenses_for_prescription(prescription_id)


# ----- Billing / integration -----


@router.post(
    "/{dispense_id}/bill/{invoice_id}",
    response_model=DispenseResponse,
)
def mark_dispense_billed(
    dispense_id: int,
    invoice_id: int,
    controller: DispenseController = Depends(_get_controller),
):
    result = controller.mark_dispense_billed(dispense_id, invoice_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispense not found",
        )
    return result


@router.get(
    "/unbilled",
    response_model=List[DispenseResponse],
)
def get_unbilled_dispenses(
    controller: DispenseController = Depends(_get_controller),
):
    return controller.get_unbilled_dispenses()


@router.get(
    "/{dispense_id}/billing-info",
    response_model=DispenseBillingInfo,
)
def get_billing_info(
    dispense_id: int,
    controller: DispenseController = Depends(_get_controller),
):
    info = controller.get_billing_info(dispense_id)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispense not found",
        )
    return info


# ----- Dispense item endpoints (optional) -----


@router.get(
    "/{dispense_id}/items",
    response_model=List[DispenseItemResponse],
)
def list_dispense_items(
    dispense_id: int,
    controller: DispenseController = Depends(_get_controller),
):
    return controller.list_dispense_items(dispense_id)
