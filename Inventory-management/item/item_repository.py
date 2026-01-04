from sqlalchemy.orm import Session
from .item_models import Item

def get_all(db: Session):
    return db.query(Item).all()

def get_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_by_code(db: Session, code: str):
    return db.query(Item).filter(Item.code == code).first()

def create(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete(db: Session, item: Item):
    db.delete(item)
    db.commit()
