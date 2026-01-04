"""
Pharmacy Module - Audit Configuration
Provides dependency helpers for Audit Controller/Service
"""

from typing import Generator

from sqlalchemy.orm import Session

from database import get_db  # your existing session dependency
from .import PharmacyAuditController


def get_audit_controller(db: Session = None) -> PharmacyAuditController:
    """
    FastAPI-friendly dependency to get a PharmacyAuditController.

    Usage in routes:
        @router.get(...)
        def handler(controller: PharmacyAuditController = Depends(get_audit_controller)):
            ...
    """
    # If used with FastAPI Depends, db will be injected by get_db
    if db is None:
        # Fallback for manual usage (non-FastAPI contexts)
        db_gen: Generator[Session, None, None] = get_db()
        db = next(db_gen)
    return PharmacyAuditController(db)
