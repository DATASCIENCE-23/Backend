from fastapi import HTTPException
from .AuditLog_service import AuditLogService


class AuditLogController:
    def __init__(self, db):
        self.service = AuditLogService(db)

    def create_log(self, user_id: int, action_type: str, ip_address: str = None):
        log = self.service.log_action(user_id, action_type, ip_address)
        return {
            "message": "Action logged",
            "log_id": log.log_id,
            "action_time": log.action_time.isoformat(),
            "action_type": log.action_type
        }

    def get_user_logs(self, user_id: int):
        logs = self.service.get_logs_for_user(user_id)
        return [
            {
                "log_id": log.log_id,
                "action_time": log.action_time.isoformat(),
                "action_type": log.action_type,
                "ip_address": log.ip_address
            } for log in logs
        ]

    def get_recent_logs(self):
        logs = self.service.get_recent_logs()
        return [
            {
                "log_id": log.log_id,
                "user_id": log.user_id,
                "action_time": log.action_time.isoformat(),
                "action_type": log.action_type,
                "ip_address": log.ip_address
            } for log in logs
        ]