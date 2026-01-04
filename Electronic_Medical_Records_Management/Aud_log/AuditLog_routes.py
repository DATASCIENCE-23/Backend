from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from .AuditLog_controller import AuditLogController

router = APIRouter(tags=["Audit Logs"])

class LogActionRequest(BaseModel):
    user_id: int
    action_type: str
    ip_address: str = None
    entity_name: str = None
    entity_id: int = None
    details: str = None

# Only admins should access these routes in real app (add auth later)

@router.post("/log")
def log_action(
    request: LogActionRequest,
    db: Session = Depends(get_db)
):
    controller = AuditLogController(db)
    return controller.create_log(request.user_id, request.action_type, request.ip_address, request.entity_name, request.entity_id, request.details)


@router.get("/user/{user_id}")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    controller = AuditLogController(db)
    return controller.get_user_logs(user_id)


@router.get("/recent")
def get_recent_logs(db: Session = Depends(get_db)):
    controller = AuditLogController(db)
    return controller.get_recent_logs()