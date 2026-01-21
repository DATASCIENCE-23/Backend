from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .stock_audit_schema import StockAuditCreate
from .stock_audit_service import create_stock_audit

def add_stock_audit(payload: StockAuditCreate, db: Session = Depends(get_db)):
    return create_stock_audit(db, payload)

from .stock_audit_repository import get_all # Import the new function

def list_stock_audits(db: Session = Depends(get_db)):
    return get_all(db)