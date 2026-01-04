from sqlalchemy.orm import Session
from fastapi import HTTPException
from .purchase_models import Purchase, PurchaseDetail
from . import purchase_repository as repository
from supplier.supplier_repository import get_by_id as get_supplier
from item.item_repository import get_by_id as get_item
from stock.stock_service import add_or_update_stock

def create_purchase(db: Session, data):
    # Supplier must exist
    if not get_supplier(db, data.supplier_id):
        raise HTTPException(400, "Supplier does not exist")

    total = 0
    for i in data.items:
        total += i.quantity * i.purchase_price

    purchase = Purchase(
        supplier_id=data.supplier_id,
        invoice_number=data.invoice_number,
        total_amount=total
    )
    purchase = repository.create_purchase(db, purchase)

    for i in data.items:
        # Item must exist
        if not get_item(db, i.item_id):
            raise HTTPException(400, f"Item {i.item_id} does not exist")

        detail = PurchaseDetail(
            purchase_id=purchase.id,
            item_id=i.item_id,
            quantity=i.quantity,
            purchase_price=i.purchase_price
        )
        repository.create_purchase_detail(db, detail)

        # 🔥 STOCK INCREASE
        add_or_update_stock(
            db,
            type("StockObj", (), {
                "item_id": i.item_id,
                "location_id": 1,  # MAIN STORE
                "quantity_available": i.quantity
            })()
        )

    return purchase
