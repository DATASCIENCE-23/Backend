"""
Pharmacy Module - Pharmacist Configuration
Provides dependencies for PharmacistController
"""

from typing import Generator

from sqlalchemy.orm import Session

from ..database import get_db  # your existing DB dependency
from . import PharmacistController


def get_pharmacist_controller(db: Session = None) -> PharmacistController:
    """
    FastAPI-friendly dependency to get a PharmacistController.

    Usage in routes:
        @router.get("/pharmacists")
        def list_pharmacists(
            controller: PharmacistController = Depends(get_pharmacist_controller),
        ):
            return controller.list_pharmacists()
    """
    if db is None:
        db_gen: Generator[Session, None, None] = get_db()
        db = next(db_gen)
    return PharmacistController(db)
