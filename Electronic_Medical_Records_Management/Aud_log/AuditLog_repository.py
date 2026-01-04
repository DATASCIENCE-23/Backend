from sqlalchemy.orm import Session
from .AuditLog_model import AuditLog
from typing import List, Optional


class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, log: AuditLog) -> AuditLog:
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def get_by_id(self, log_id: int) -> Optional[AuditLog]:
        return self.db.query(AuditLog).filter(AuditLog.log_id == log_id).first()

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return (
            self.db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.action_time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_recent(self, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).order_by(AuditLog.action_time.desc()).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return self.db.query(AuditLog).order_by(AuditLog.action_time.desc()).offset(skip).limit(limit).all()