from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional, Dict

from database import get_db
from Purchase_schema import POCreate, POResp, POUpdate, POItemCreate, POItemResp
from Purchase_service import PurchaseService, GRNService


class PurchaseController:
    """Controller for Purchase Order endpoints"""

    @staticmethod
    def create_po(data: POCreate, db: Session = Depends(get_db)) -> POResp:
        """Create purchase order"""
        try:
            return PurchaseService.createPO(db, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def get_po(purchase_id: int, db: Session = Depends(get_db)) -> POResp:
        """Get purchase order"""
        po = PurchaseService.getPO(db, purchase_id)
        if not po:
            raise HTTPException(status_code=404, detail="PO not found")
        return po

    @staticmethod
    def list_po(
        supplier_id: Optional[int] = None,
        status: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        db: Session = Depends(get_db)
    ) -> List[POResp]:
        """List purchase orders"""
        return PurchaseService.listPO(db, supplier_id, status, date_from, date_to)

    @staticmethod
    def update_status(purchase_id: int, data: POUpdate, db: Session = Depends(get_db)) -> POResp:
        """Update purchase order status"""
        try:
            return PurchaseService.updateStatus(db, purchase_id, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def add_item(purchase_id: int, data: POItemCreate, db: Session = Depends(get_db)) -> POItemResp:
        """Add item to purchase order"""
        try:
            return PurchaseService.addItem(db, purchase_id, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def remove_item(item_id: int, db: Session = Depends(get_db)):
        """Remove item from purchase order"""
        try:
            PurchaseService.removeItem(db, item_id)
            return {"msg": "Item removed"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def create_grn(purchase_id: int, recv_by: int, notes: Optional[str] = None, db: Session = Depends(get_db)):
        """Create goods receipt note"""
        try:
            return GRNService.createGRN(db, purchase_id, recv_by, notes)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def get_report(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        supplier_id: Optional[int] = None,
        db: Session = Depends(get_db)
    ) -> Dict:
        """Get purchase report"""
        try:
            return PurchaseService.get_purchase_report(db, date_from, date_to, supplier_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
