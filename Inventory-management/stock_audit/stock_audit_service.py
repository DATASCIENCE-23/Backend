from sqlalchemy.orm import Session
from fastapi import HTTPException
from .stock_audit_models import StockAudit, StockAuditDetail
from . import stock_audit_repository as repository
from store_location.store_location_repository import get_by_id as get_location
from stock.stock_repository import get_by_item_and_location, update as update_stock

def create_stock_audit(db: Session, data):
    # location must exist
    if not get_location(db, data.location_id):
        raise HTTPException(400, "Store location does not exist")

    audit = StockAudit(
        location_id=data.location_id,
        remarks=data.remarks
    )
    audit = repository.create_audit(db, audit)

    for i in data.items:
        stock = get_by_item_and_location(db, i.item_id, data.location_id)
        system_qty = stock.quantity_available if stock else 0

        difference = i.physical_quantity - system_qty

        # update stock to physical quantity
        if stock:
            stock.quantity_available = i.physical_quantity
            update_stock(db, stock)

        detail = StockAuditDetail(
            audit_id=audit.id,
            item_id=i.item_id,
            system_quantity=system_qty,
            physical_quantity=i.physical_quantity,
            difference=difference
        )
        repository.create_audit_detail(db, detail)

    return audit
