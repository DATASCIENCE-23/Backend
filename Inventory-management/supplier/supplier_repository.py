from sqlalchemy.orm import Session
from .supplier_models import Supplier

def get_all(db: Session):
    return db.query(Supplier).all()

def get_by_id(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def create(db: Session, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def delete(db: Session, supplier: Supplier):
    db.delete(supplier)
    db.commit()

def update(db: Session, supplier: Supplier, updated_data: dict):
    for key, value in updated_data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier
