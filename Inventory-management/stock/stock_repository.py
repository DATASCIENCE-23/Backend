from sqlalchemy.orm import Session
from .stock_models import Stock

def get_by_item_and_location(db: Session, item_id: int, location_id: int):
    return (
        db.query(Stock)
        .filter(
            Stock.item_id == item_id,
            Stock.location_id == location_id
        )
        .first()
    )

def get_all(db: Session):
    return db.query(Stock).all()

def create(db: Session, stock: Stock):
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock

def update(db: Session, stock: Stock):
    db.commit()
    db.refresh(stock)
    return stock
