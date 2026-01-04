# pharmacy_management/audit/audit_routes.py

"""
Pharmacy Module - Audit Routes
FastAPI endpoints for viewing audit logs
"""

from fastapi import APIRouter, Depends

from .audit_configuration import get_audit_controller
from .audit_controller import PharmacyAuditController  # or from . import PharmacyAuditController

router = APIRouter(
    prefix="/pharmacy/audit",
    tags=["Pharmacy Audit"],
)


@router.get("/{entity_name}/{entity_id}", response_model=list[dict])
def list_audit_logs(
    entity_name: str,
    entity_id: int,
    controller: PharmacyAuditController = Depends(get_audit_controller),
):
    """
    Return audit logs for a given entity.
    Later you can replace list[dict] with an AuditLogRead schema.
    """
    return controller.get_entity_logs(entity_name, entity_id)
