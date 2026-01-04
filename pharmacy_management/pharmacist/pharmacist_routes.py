"""
Pharmacy Module - Pharmacist Routes
FastAPI endpoints for pharmacist management and stats
"""

from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .pharmacist_model import Pharmacist  # ORM model (used only internally, not as response_model)
from ..schemas import (
    MessageResponse,
    PharmacistCreate,
    PharmacistUpdate,
    PharmacistRead,
    DispenseStatusEnum,
)
from .pharmacist_configuration import get_pharmacist_controller
from .pharmacist_controller import PharmacistController  # or from . import PharmacistController if __init__ re-exports

router = APIRouter(
    prefix="/pharmacy/pharmacists",
    tags=["Pharmacy - Pharmacists"],
)


def _get_controller(db: Session = Depends(get_db)) -> PharmacistController:
    return PharmacistController(db)


# ---------- Pharmacist CRUD ----------

@router.post(
    "/",
    response_model=PharmacistRead,
    status_code=status.HTTP_201_CREATED,
)
def create_pharmacist(
    data: PharmacistCreate,
    controller: PharmacistController = Depends(_get_controller),
):
    """
    Create a pharmacist.
    """
    try:
        return controller.create_pharmacist(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{pharmacist_id}",
    response_model=PharmacistRead,
)
def get_pharmacist(
    pharmacist_id: int,
    controller: PharmacistController = Depends(_get_controller),
):
    pharmacist = controller.get_pharmacist(pharmacist_id)
    if not pharmacist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacist not found",
        )
    return pharmacist


@router.get(
    "/",
    response_model=List[PharmacistRead],
)
def list_pharmacists(
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    controller: PharmacistController = Depends(_get_controller),
):
    return controller.list_pharmacists(
        active_only=active_only,
        skip=skip,
        limit=limit,
    )


@router.put(
    "/{pharmacist_id}",
    response_model=PharmacistRead,
)
def update_pharmacist(
    pharmacist_id: int,
    data: PharmacistUpdate,
    controller: PharmacistController = Depends(_get_controller),
):
    try:
        result = controller.update_pharmacist(pharmacist_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacist not found",
        )
    return result


@router.post(
    "/{pharmacist_id}/deactivate",
    response_model=MessageResponse,
)
def deactivate_pharmacist(
    pharmacist_id: int,
    controller: PharmacistController = Depends(_get_controller),
):
    ok = controller.deactivate_pharmacist(pharmacist_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacist not found",
        )
    return MessageResponse(message="Pharmacist deactivated", success=True)


# ---------- Dispense-related endpoints ----------

@router.get(
    "/{pharmacist_id}/dispenses",
    response_model=List[dict],  # you can define a proper schema later
)
def get_dispenses_by_pharmacist(
    pharmacist_id: int,
    status: Optional[DispenseStatusEnum] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    controller: PharmacistController = Depends(_get_controller),
):
    dispenses = controller.get_dispenses_by_pharmacist(
        pharmacist_id=pharmacist_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )
    return [
        {
            "dispense_id": d.dispense_id,
            "prescription_id": d.prescription_id,
            "dispensed_at": d.dispensed_at,
            "total_amount": d.total_amount,
            "status": d.status,
        }
        for d in dispenses
    ]


@router.get(
    "/{pharmacist_id}/dispense-stats",
    response_model=dict,
)
def get_dispense_stats(
    pharmacist_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    controller: PharmacistController = Depends(_get_controller),
):
    """
    Returns:
    {
      "total_dispenses": int,
      "total_amount": Decimal,
      "completed_dispenses": int,
      "billed_dispenses": int
    }
    """
    return controller.get_dispense_stats(
        pharmacist_id=pharmacist_id,
        start_date=start_date,
        end_date=end_date,
    )
