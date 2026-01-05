from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .stock_schema import StockCreate
from .stock_service import add_or_update_stock, list_stock, delete_stock_by_id, update_stock, get_stock_by_id

def add_stock(payload: StockCreate, db: Session = Depends(get_db)):
    return add_or_update_stock(db, payload)

def get_all_stock(db: Session = Depends(get_db)):
    return list_stock(db)

def remove_stock(stock_id: int, db: Session = Depends(get_db)):
    return delete_stock_by_id(db, stock_id)

def modify_stock(stock_id: int, updated_data: dict, db: Session = Depends(get_db)):
    return update_stock(db, stock_id, updated_data)

def get_stock(stock_id: int, db: Session = Depends(get_db)):
    return get_stock_by_id(db, stock_id)

