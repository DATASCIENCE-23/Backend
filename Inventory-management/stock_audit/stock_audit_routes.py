from fastapi import APIRouter
from .stock_audit_controller import add_stock_audit, list_stock_audits

router = APIRouter(prefix="/stock-audits", tags=["Stock Audit"])

router.post("/")(add_stock_audit)
router.get("/")(list_stock_audits)