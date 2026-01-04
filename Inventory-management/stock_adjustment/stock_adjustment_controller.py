from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .stock_adjustment_schema import StockAdjustmentCreate
from .stock_adjustment_service import create_stock_adjustment

def add_stock_adjustment(payload: StockAdjustmentCreate, db: Session = Depends(get_db)):
    return create_stock_adjustment(db, payload)
