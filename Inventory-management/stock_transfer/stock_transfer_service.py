from sqlalchemy.orm import Session
from fastapi import HTTPException
from .stock_transfer_models import StockTransfer
from . import stock_transfer_repository as repository
from item.item_repository import get_by_id as get_item
from store_location.store_location_repository import get_by_id as get_location
from stock.stock_repository import get_by_item_and_location, update as update_stock

def create_stock_transfer(db: Session, data):
    # item exists
    if not get_item(db, data.item_id):
        raise HTTPException(400, "Item does not exist")

    # locations exist
    if not get_location(db, data.from_location_id):
        raise HTTPException(400, "From location does not exist")

    if not get_location(db, data.to_location_id):
        raise HTTPException(400, "To location does not exist")

    if data.from_location_id == data.to_location_id:
        raise HTTPException(400, "From and To locations cannot be same")

    from_stock = get_by_item_and_location(
        db, data.item_id, data.from_location_id
    )

    if not from_stock or from_stock.quantity_available < data.quantity:
        raise HTTPException(400, "Insufficient stock in source location")

    # reduce stock from source
    from_stock.quantity_available -= data.quantity
    update_stock(db, from_stock)

    # add stock to destination
    to_stock = get_by_item_and_location(
        db, data.item_id, data.to_location_id
    )

    if to_stock:
        to_stock.quantity_available += data.quantity
        update_stock(db, to_stock)
    else:
        from stock.models import Stock
        new_stock = Stock(
            item_id=data.item_id,
            location_id=data.to_location_id,
            quantity_available=data.quantity
        )
        db.add(new_stock)
        db.commit()

    transfer = StockTransfer(
        item_id=data.item_id,
        from_location_id=data.from_location_id,
        to_location_id=data.to_location_id,
        quantity=data.quantity
    )
    return repository.create(db, transfer)
