from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date

from Purchase_model import PO, POItem, GRN


class PurchaseRepository:
    """Repository for Purchase Order operations"""

    @staticmethod
    def create_po(db: Session, po: PO) -> PO:
        """Create a new purchase order"""
        db.add(po)
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def get_po(db: Session, purchase_id: int) -> Optional[PO]:
        """Get purchase order by ID"""
        return db.query(PO).filter(PO.purchaseId == purchase_id).first()

    @staticmethod
    def list_po(
        db: Session,
        supplier_id: Optional[int] = None,
        status: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[PO]:
        """List purchase orders with filters"""
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
    def update_po(db: Session, po: PO) -> PO:
        """Update purchase order"""
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def delete_po(db: Session, po: PO) -> None:
        """Delete purchase order"""
        db.delete(po)
        db.commit()

    @staticmethod
    def add_item(db: Session, item: POItem) -> POItem:
        """Add item to purchase order"""
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_item(db: Session, item_id: int) -> Optional[POItem]:
        """Get purchase order item by ID"""
        return db.query(POItem).filter(POItem.poItemId == item_id).first()

    @staticmethod
    def get_items_by_po(db: Session, purchase_id: int) -> List[POItem]:
        """Get all items for a purchase order"""
        return db.query(POItem).filter(POItem.purchaseId == purchase_id).all()

    @staticmethod
    def check_duplicate_item(db: Session, purchase_id: int, item_id: int) -> Optional[POItem]:
        """Check if item already exists in purchase order"""
        return db.query(POItem).filter(
            and_(POItem.purchaseId == purchase_id, POItem.itemId == item_id)
        ).first()

    @staticmethod
    def delete_item(db: Session, item: POItem) -> None:
        """Delete purchase order item"""
        db.delete(item)
        db.commit()

    @staticmethod
    def create_grn(db: Session, grn: GRN) -> GRN:
        """Create goods receipt note"""
        db.add(grn)
        db.commit()
        db.refresh(grn)
        return grn

    @staticmethod
    def count_grn_for_month(db: Session, year: str, month: str) -> int:
        """Count GRNs for a specific month"""
        return db.query(GRN).filter(GRN.grnNum.like(f"GRN-{year}-{month}-%")).count()
