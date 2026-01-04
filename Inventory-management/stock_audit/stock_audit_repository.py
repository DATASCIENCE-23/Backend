from sqlalchemy.orm import Session
from .stock_audit_models import StockAudit, StockAuditDetail

def create_audit(db: Session, audit: StockAudit):
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit

def create_audit_detail(db: Session, detail: StockAuditDetail):
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail
