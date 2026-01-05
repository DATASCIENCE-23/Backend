from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from .stock_models import Stock
from . import stock_repository as repository
from item.item_repository import get_by_id as get_item
from store_location.store_location_repository import get_by_id as get_location

def add_or_update_stock(db: Session, data):
    # item must exist
    if not get_item(db, data.item_id):
        raise HTTPException(400, "Item does not exist")

    # location must exist
    if not get_location(db, data.location_id):
        raise HTTPException(400, "Store location does not exist")

    stock = repository.get_by_item_and_location(
        db, data.item_id, data.location_id
    )

    if stock:
        stock.quantity_available += data.quantity_available
        stock.last_updated = datetime.utcnow()
        return repository.update(db, stock)

    stock = Stock(
        item_id=data.item_id,
        location_id=data.location_id,
        quantity_available=data.quantity_available
    )
    return repository.create(db, stock)

def list_stock(db: Session):
    return repository.get_all(db)

def get_stock_by_id(db: Session, stock_id: int):
    stock = repository.get_by_id(db, stock_id)
    if not stock:
        raise HTTPException(404, "Stock record not found")
    return stock

def delete_stock_by_id(db: Session, stock_id: int):
    stock = repository.get_by_id(db, stock_id)
    if not stock:
        raise HTTPException(404, "Stock record not found")
    return repository.delete(db, stock)

def update_stock(db: Session, item_id: int, location_id: int, updated_data: dict):
    stock = repository.get_by_item_and_location(db, item_id, location_id)
    if not stock:
        raise HTTPException(404, "Stock record not found")
    return repository.update(db, stock, updated_data)
