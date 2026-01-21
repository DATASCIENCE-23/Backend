from sqlalchemy.orm import Session
from .purchase_service import Purchase, PurchaseDetail

def create_purchase(db: Session, purchase: Purchase):
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase

def create_purchase_detail(db: Session, detail: PurchaseDetail):
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail

def get_all(db: Session):
    return db.query(Purchase).all()
