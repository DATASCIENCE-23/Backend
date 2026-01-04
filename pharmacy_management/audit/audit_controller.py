"""
Pharmacy Module - Audit Controller
Coordinates HTTP/API layer and Audit Service
"""

from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session

from . import PharmacyAuditLog  # model exported from pharmacy/__init__.py
from . import PharmacyAuditService


class PharmacyAuditController:
    """
    Thin controller around PharmacyAuditService.
    Use this in FastAPI routes or other module controllers.
    """

    def __init__(self, db: Session):
        self.db = db

    # ---------- Generic actions ----------

    def log_create(
        self,
        user_id: int,
        entity_name: str,
        entity_id: int,
        details: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log a create action for any pharmacy entity.
        """
        PharmacyAuditService.log_create(
            db=self.db,
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
        )

    def log_update(
        self,
        user_id: int,
        entity_name: str,
        entity_id: int,
        before: Dict[str, Any],
        after: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log an update with before/after states.
        """
        PharmacyAuditService.log_update(
            db=self.db,
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            before=before,
            after=after,
            ip_address=ip_address,
        )

    def log_delete(
        self,
        user_id: int,
        entity_name: str,
        entity_id: int,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log a delete action.
        """
        PharmacyAuditService.log_delete(
            db=self.db,
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            reason=reason,
            ip_address=ip_address,
        )

    # ---------- Domain-specific helpers ----------

    def log_dispense_action(
        self,
        user_id: int,
        prescription_id: int,
        dispense_id: int,
        summary: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log a dispense event.
        summary can contain line items, totals, etc.
        """
        PharmacyAuditService.log_dispense(
            db=self.db,
            user_id=user_id,
            prescription_id=prescription_id,
            dispense_id=dispense_id,
            summary=summary,
            ip_address=ip_address,
        )

    # ---------- Queries ----------

    def get_entity_logs(
        self,
        entity_name: str,
        entity_id: int,
    ) -> List[PharmacyAuditLog]:
        """
        Fetch full audit history for an entity.
        """
        return PharmacyAuditService.get_entity_logs(
            db=self.db,
            entity_name=entity_name,
            entity_id=entity_id,
        )
