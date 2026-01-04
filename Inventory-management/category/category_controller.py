from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .category_service import (
    create_category,
    get_category,
    list_categories,
    delete_category
    , update_category
)
from .category_schema import CategoryCreate

def add_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, payload)

def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)

def get_all_categories(db: Session = Depends(get_db)):
    return list_categories(db)

def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)

def modify_category(category_id: int, updated_data: dict, db: Session = Depends(get_db)):
    return update_category(db, category_id, updated_data)