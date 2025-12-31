from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date

from models.purchase_model import PO, POItem, GRN


class PurchaseRepository:
    @staticmethod
    def create_po(db: Session, po: PO) -> PO:
        db.add(po)
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def get_po(db: Session, purchase_id: int) -> Optional[PO]:
        return db.query(PO).filter(PO.purchaseId == purchase_id).first()

    @staticmethod
    def list_po(db: Session, supplier_id=None, status=None, date_from=None, date_to=None) -> List[PO]:
        query = db.query(PO)
        if supplier_id:
            query = query.filter(PO.supplierId == supplier_id)
        if status:
            query = query.filter(PO.status == status)
        if date_from:
            query = query.filter(PO.orderDate >= date_from)
        if date_to:
            query = query.filter(PO.orderDate <= date_to)
        return query.all()

    @staticmethod
    def add_item(db: Session, item: POItem) -> POItem:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_po_item(db: Session, purchase_id: int, item_id: int) -> Optional[POItem]:
        return db.query(POItem).filter(
            and_(POItem.purchaseId == purchase_id, POItem.itemId == item_id)
        ).first()

    @staticmethod
    def get_items_by_po(db: Session, purchase_id: int) -> List[POItem]:
        return db.query(POItem).filter(POItem.purchaseId == purchase_id).all()

    @staticmethod
    def update_po(db: Session, po: PO) -> PO:
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def delete_item(db: Session, item: POItem):
        db.delete(item)
        db.commit()

    @staticmethod
    def get_item_by_id(db: Session, item_id: int) -> Optional[POItem]:
        return db.query(POItem).filter(POItem.poItemId == item_id).first()

    @staticmethod
    def count_grn_for_month(db: Session, year: str, month: str) -> int:
        return db.query(GRN).filter(GRN.grnNum.like(f"GRN-{year}-{month}-%")).count()

    @staticmethod
    def create_grn(db: Session, grn: GRN) -> GRN:
        db.add(grn)
        db.commit()
        db.refresh(grn)
        return grn
