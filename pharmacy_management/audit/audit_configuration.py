# pharmacy_management/audit/audit_configuration.py

from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .audit_controller import PharmacyAuditController  # adjust name

def get_audit_controller(
    db: Session = Depends(get_db),
) -> PharmacyAuditController:
    """
    Dependency that creates a PharmacyAuditController using a DB session.
    This is where Session is used, and only as a dependency argument.
    """
    return PharmacyAuditController(db)
