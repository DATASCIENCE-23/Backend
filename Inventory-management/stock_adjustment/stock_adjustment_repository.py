from sqlalchemy.orm import Session
from .stock_adjustment_models import StockAdjustment

def create(db: Session, adjustment: StockAdjustment):
    db.add(adjustment)
    db.commit()
    db.refresh(adjustment)
    return adjustment

def get_all(db: Session):
    return db.query(StockAdjustment).all()
