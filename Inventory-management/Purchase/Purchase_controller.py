from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from core.database import get_db
from schemas.purchase_schema import POCreate, POResp, POUpdate
from schemas.purchase_schema import POItemCreate, POItemResp
from services.purchase_service import POService


class PurchaseController:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_po(self, data: POCreate) -> POResp:
        try:
            return POService.createPO(self.db, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def add_item(self, purchase_id: int, data: POItemCreate) -> POItemResp:
        try:
            return POService.addItem(self.db, purchase_id, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_po(self, purchase_id: int) -> POResp:
        po = POService.getPO(self.db, purchase_id)
        if not po:
            raise HTTPException(status_code=404, detail="PO not found")
        return po

    def list_po(
        self,
        supplier_id: Optional[int] = None,
        status: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[POResp]:
        return POService.listPO(self.db, supplier_id, status, date_from, date_to)

    def update_status(self, purchase_id: int, data: POUpdate) -> POResp:
        try:
            return POService.updateStatus(self.db, purchase_id, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def remove_item(self, item_id: int):
        try:
            POService.removeItem(self.db, item_id)
            return {"msg": "Item removed"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
