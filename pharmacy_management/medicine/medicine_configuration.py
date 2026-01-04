"""
Pharmacy Module - Medicine Configuration
Provides dependencies for MedicineController
"""

from typing import Generator

from sqlalchemy.orm import Session

from database import get_db  # your existing DB dependency
from . import MedicineController


def get_medicine_controller(db: Session = None) -> MedicineController:
    """
    FastAPI-friendly dependency to get a MedicineController.

    Usage in routes:
        @router.post("/medicines")
        def create_medicine(
            payload: MedicineCreate,
            controller: MedicineController = Depends(get_medicine_controller),
            current_user: User = Depends(get_current_user),
        ):
            return controller.create_medicine(payload, user_id=current_user.user_id)
    """
    if db is None:
        db_gen: Generator[Session, None, None] = get_db()
        db = next(db_gen)
    return MedicineController(db)
