from sqlalchemy.orm import Session
from fastapi import HTTPException
from .store_location_models import StoreLocation
from . import store_location_repository as repository

def create_location(db: Session, data):
    location = StoreLocation(
        name=data.name,
        location_type=data.location_type
    )
    return repository.create(db, location)

def get_location(db: Session, location_id: int):
    location = repository.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Store location not found")
    return location

def list_locations(db: Session):
    return repository.get_all(db)

def delete_location(db: Session, location_id: int):
    location = repository.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Store location not found")
    repository.delete(db, location)

def update_location(db: Session, location_id: int, updated_data):
    location = repository.get_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Store location not found")
    return repository.update(db, location, updated_data)