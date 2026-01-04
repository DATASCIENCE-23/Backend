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
