from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from .AuditLog_controller import AuditLogController

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

# Only admins should access these routes in real app (add auth later)

@router.post("/log")
def log_action(
    user_id: int,
    action_type: str,
    ip_address: str = None,
    db: Session = Depends(get_db)
):
    controller = AuditLogController(db)
    return controller.create_log(user_id, action_type, ip_address)


@router.get("/user/{user_id}")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    controller = AuditLogController(db)
    return controller.get_user_logs(user_id)


@router.get("/recent")
def get_recent_logs(db: Session = Depends(get_db)):
    controller = AuditLogController(db)
    return controller.get_recent_logs()