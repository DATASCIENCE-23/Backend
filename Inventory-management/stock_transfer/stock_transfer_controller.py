from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .stock_transfer_schema import StockTransferCreate
from .stock_transfer_service import create_stock_transfer

def add_stock_transfer(payload: StockTransferCreate, db: Session = Depends(get_db)):
    return create_stock_transfer(db, payload)
