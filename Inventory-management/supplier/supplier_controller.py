from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .supplier_schema import SupplierCreate
from .supplier_service import (
    create_supplier,
    get_supplier,
    list_suppliers,
    delete_supplier
    , update_supplier
)

def add_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(db, payload)

def get_supplier_by_id(supplier_id: int, db: Session = Depends(get_db)):
    return get_supplier(db, supplier_id)

def get_all_suppliers(db: Session = Depends(get_db)):
    return list_suppliers(db)

def remove_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return delete_supplier(db, supplier_id)

def modify_supplier(supplier_id: int, updated_data: dict, db: Session = Depends(get_db)):
    return update_supplier(db, supplier_id, updated_data)
