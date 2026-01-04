from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .stock_audit_schema import StockAuditCreate
from .stock_audit_service import create_stock_audit

def add_stock_audit(payload: StockAuditCreate, db: Session = Depends(get_db)):
    return create_stock_audit(db, payload)
