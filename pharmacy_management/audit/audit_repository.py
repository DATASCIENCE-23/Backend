from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, desc
from typing import List, Optional, Tuple
from datetime import datetime, date, timedelta
from .. import (
    PharmacyAuditLog
)
class PharmacyAuditRepository:
    """Repository for Audit Log operations"""

    @staticmethod
    def log_action(db: Session, user_id: int, entity_name: str, entity_id: int,
                   action_type: str, details: str, ip_address: Optional[str] = None):
        """Create an audit log entry"""
        log = PharmacyAuditLog(
            user_id=user_id,
            entity_name=entity_name,
            entity_id=entity_id,
            action_type=action_type,
            details=details,
            ip_address=ip_address
        )
        db.add(log)
        db.commit()

    @staticmethod
    def get_logs_by_entity(db: Session, entity_name: str, entity_id: int) -> List[PharmacyAuditLog]:
        """Get all audit logs for a specific entity"""
        return db.query(PharmacyAuditLog).filter(
            PharmacyAuditLog.entity_name == entity_name,
            PharmacyAuditLog.entity_id == entity_id
        ).order_by(desc(PharmacyAuditLog.action_time)).all()