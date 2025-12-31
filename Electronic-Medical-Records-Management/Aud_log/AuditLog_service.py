from .AuditLog_model import AuditLog
from .AuditLog_repository import AuditLogRepository
from datetime import datetime


class AuditLogService:
    def __init__(self, db):
        self.repository = AuditLogRepository(db)

    def log_action(self, user_id: int, action_type: str, ip_address: str = None) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            action_time=datetime.utcnow(),
            action_type=action_type,
            ip_address=ip_address
        )
        return self.repository.create(log)

    def get_logs_for_user(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def get_recent_logs(self):
        return self.repository.get_recent()

    def get_log(self, log_id: int):
        log = self.repository.get_by_id(log_id)
        if not log:
            raise ValueError("Log not found")
        return log