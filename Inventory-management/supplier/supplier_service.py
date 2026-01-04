from sqlalchemy.orm import Session
from fastapi import HTTPException
from .supplier_models import Supplier
from . import supplier_repository as repository

def create_supplier(db: Session, data):
    supplier = Supplier(
        name=data.name,
        contact_person=data.contact_person,
        phone=data.phone,
        email=data.email,
        address=data.address
    )
    return repository.create(db, supplier)

def get_supplier(db: Session, supplier_id: int):
    supplier = repository.get_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

def list_suppliers(db: Session):
    return repository.get_all(db)

def delete_supplier(db: Session, supplier_id: int):
    supplier = repository.get_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    repository.delete(db, supplier)

def update_supplier(db: Session, supplier_id: int, updated_data):
    supplier = repository.get_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return repository.update(db, supplier, updated_data)