from sqlalchemy.orm import Session
from .stock_transfer_models import StockTransfer

def create(db: Session, transfer: StockTransfer):
    db.add(transfer)
    db.commit()
    db.refresh(transfer)
    return transfer

def get_all(db: Session):
    return db.query(StockTransfer).all()