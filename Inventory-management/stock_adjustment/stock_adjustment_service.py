from sqlalchemy.orm import Session
from fastapi import HTTPException
from .stock_adjustment_models import StockAdjustment
from . import stock_adjustment_repository as repository
from item.item_repository import get_by_id as get_item
from store_location.store_location_repository import get_by_id as get_location
from stock.stock_repository import get_by_item_and_location, update as update_stock

def create_stock_adjustment(db: Session, data):
    # item exists
    if not get_item(db, data.item_id):
        raise HTTPException(400, "Item does not exist")

    # location exists
    if not get_location(db, data.location_id):
        raise HTTPException(400, "Store location does not exist")

    stock = get_by_item_and_location(db, data.item_id, data.location_id)
    if not stock:
        raise HTTPException(400, "Stock record does not exist")

    if data.adjustment_type == "SUBTRACT":
        if stock.quantity_available < data.quantity_changed:
            raise HTTPException(400, "Insufficient stock to subtract")
        stock.quantity_available -= data.quantity_changed

    if data.adjustment_type == "ADD":
        stock.quantity_available += data.quantity_changed

    update_stock(db, stock)

    adjustment = StockAdjustment(
        item_id=data.item_id,
        location_id=data.location_id,
        adjustment_type=data.adjustment_type,
        quantity_changed=data.quantity_changed,
        reason=data.reason
    )
    return repository.create(db, adjustment)
