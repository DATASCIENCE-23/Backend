from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from .store_location_schema import StoreLocationCreate
from .store_location_service import (
    create_location,
    get_location,
    list_locations,
    delete_location
)

def add_location(payload: StoreLocationCreate, db: Session = Depends(get_db)):
    return create_location(db, payload)

def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    return get_location(db, location_id)

def get_all_locations(db: Session = Depends(get_db)):
    return list_locations(db)

def remove_location(location_id: int, db: Session = Depends(get_db)):
    return delete_location(db, location_id)
def modify_location(location_id: int, updated_data: dict, db: Session = Depends(get_db)):
    return update_location(db, location_id, updated_data)
