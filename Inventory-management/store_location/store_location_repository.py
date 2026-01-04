from sqlalchemy.orm import Session
from .store_location_models import StoreLocation

def get_all(db: Session):
    return db.query(StoreLocation).all()

def get_by_id(db: Session, location_id: int):
    return db.query(StoreLocation).filter(StoreLocation.id == location_id).first()

def create(db: Session, location: StoreLocation):
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

def delete(db: Session, location: StoreLocation):
    db.delete(location)
    db.commit()

def update(db: Session, location: StoreLocation, updated_data: dict):
    for key, value in updated_data.items():
        setattr(location, key, value)
    db.commit()
    