from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .stock_schema import StockCreate
from .stock_service import add_or_update_stock, list_stock

def add_stock(payload: StockCreate, db: Session = Depends(get_db)):
    return add_or_update_stock(db, payload)

def get_all_stock(db: Session = Depends(get_db)):
    return list_stock(db)
