from fastapi import APIRouter
from .stock_audit_controller import add_stock_audit

router = APIRouter(prefix="/stock-audits", tags=["Stock Audit"])

router.post("/")(add_stock_audit)
