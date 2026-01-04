"""
Pharmacy Module - Dispense Configuration
Provides dependencies for DispenseController
"""

from typing import Generator

from sqlalchemy.orm import Session

from database import get_db  # your existing session dependency
from . import DispenseController


def get_dispense_controller(db: Session = None) -> DispenseController:
    """
    FastAPI-friendly dependency to get a DispenseController.

    Usage in routes:
        @router.post("/dispense")
        def create_dispense(
            payload: DispenseCreate,
            controller: DispenseController = Depends(get_dispense_controller),
        ):
            return controller.create_dispense(payload, pharmacist_id=current_user.id)
    """
    # If used with FastAPI Depends, db will be injected via get_db
    if db is None:
        db_gen: Generator[Session, None, None] = get_db()
        db = next(db_gen)
    return DispenseController(db)
