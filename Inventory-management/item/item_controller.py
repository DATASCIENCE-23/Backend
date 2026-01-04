from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .item_schema import ItemCreate
from .item_service import (
    create_item,
    get_item,
    list_items,
    delete_item
)

def add_item(payload: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, payload)

def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    return get_item(db, item_id)

def get_all_items(db: Session = Depends(get_db)):
    return list_items(db)

def remove_item(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db, item_id)
