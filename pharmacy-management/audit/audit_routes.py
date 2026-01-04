# audit-route.py
from fastapi import APIRouter, Depends
from .import get_audit_controller
from . import PharmacyAuditController

router = APIRouter(prefix="/pharmacy/audit", tags=["Pharmacy Audit"])

@router.get("/{entity_name}/{entity_id}")
def list_audit_logs(
    entity_name: str,
    entity_id: int,
    controller: PharmacyAuditController = Depends(get_audit_controller),
):
    return controller.get_entity_logs(entity_name, entity_id)
