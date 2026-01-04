"""
Pharmacy Module - Audit Service
High-level functions to record and query audit logs
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session

from . import PharmacyAuditLog  # model (from pharmacy/__init__.py exports)
from . import PharmacyAuditRepository
from ..internal_utils import _ensure_str_details



class PharmacyAuditService:
    """
    Service layer for pharmacy audit logging.
    Use this from controllers/services in medicine/dispense/pharmacist modules.
    """

    @staticmethod
    def log_create(
        db: Session,
        user_id: int,
        entity_name: str,
        entity_id: int,
        details: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log a CREATE action for an entity.
        details: dict with serializable info (will be JSON-encoded by caller or controller).
        """
        PharmacyAuditRepository.log_action(
            db=db,
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            action_type="CREATE",
            details=_ensure_str_details(details),
            ip_address=ip_address,
        )

    @staticmethod
    def log_update(
        db: Session,
        user_id: int,
        entity_name: str,
        entity_id: int,
        before: Dict[str, Any],
        after: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log an UPDATE action with before/after snapshots.
        """
        payload = {
            "before": before,
            "after": after,
            "updated_at": datetime.utcnow().isoformat(),
        }
        PharmacyAuditRepository.log_action(
            db=db,
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            action_type="UPDATE",
            details=_ensure_str_details(payload),
            ip_address=ip_address,
        )

    @staticmethod
    def log_delete(
        db: Session,
        user_id: int,
        entity_name: str,
        entity_id: int,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Log a DELETE action.
        """
        payload = {
            "reason": reason,
            "deleted_at": datetime.utcnow().isoformat(),
        }
        PharmacyAuditRepository.log_action(
            db=db,
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            action_type="DELETE",
            details=_ensure_str_details(payload),
            ip_address=ip_address,
        )

    @staticmethod
    def log_dispense(
        db: Session,
        user_id: int,
        prescription_id: int,
        dispense_id: int,
        summary: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> None:
        """
        Specialized helper: log a DISPENSE action for prescriptions/dispense.
        entity_name: "Dispense" or "Prescription" depending on what you want to track.
        """
        payload = {
            "prescription_id": prescription_id,
            "dispense_id": dispense_id,
            "summary": summary,
            "dispensed_at": datetime.utcnow().isoformat(),
        }
        PharmacyAuditRepository.log_action(
            db=db,
            user_id=user_id,
            entity_name="Dispense",
            entity_id=dispense_id,
            action_type="DISPENSE",
            details=_ensure_str_details(payload),
            ip_address=ip_address,
        )

    @staticmethod
    def get_entity_logs(
        db: Session,
        entity_name: str,
        entity_id: int,
    ) -> List[PharmacyAuditLog]:
        """
        Get full audit history for an entity.
        """
        return PharmacyAuditRepository.get_logs_by_entity(
            db=db,
            entity_name=entity_name,
            entity_id=entity_id,
        )

