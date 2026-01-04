from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional, Dict

from database import get_db
from Purchase_schema import POCreate, POResp, POUpdate, POItemCreate, POItemResp
from Purchase_controller import PurchaseController

router = APIRouter(prefix="/api/po", tags=["purchase"])


@router.post("", response_model=POResp)
def create_po(data: POCreate, db: Session = Depends(get_db)):
    """Create purchase order"""
    return PurchaseController.create_po(data, db)


@router.get("/{purchase_id}", response_model=POResp)
def get_po(purchase_id: int, db: Session = Depends(get_db)):
    """Get purchase order"""
    return PurchaseController.get_po(purchase_id, db)


@router.get("", response_model=List[POResp])
def list_po(
    supplier_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """List purchase orders"""
    return PurchaseController.list_po(supplier_id, status, date_from, date_to, db)


@router.patch("/{purchase_id}", response_model=POResp)
def update_status(purchase_id: int, data: POUpdate, db: Session = Depends(get_db)):
    """Update purchase order status"""
    return PurchaseController.update_status(purchase_id, data, db)


@router.post("/{purchase_id}/items", response_model=POItemResp)
def add_item(purchase_id: int, data: POItemCreate, db: Session = Depends(get_db)):
    """Add item to purchase order"""
    return PurchaseController.add_item(purchase_id, data, db)


@router.delete("/{purchase_id}/items/{item_id}")
def remove_item(purchase_id: int, item_id: int, db: Session = Depends(get_db)):
    """Remove item from purchase order"""
    return PurchaseController.remove_item(item_id, db)


@router.post("/{purchase_id}/grn")
def create_grn(purchase_id: int, recv_by: int, notes: Optional[str] = None, db: Session = Depends(get_db)):
    """Create goods receipt note"""
    return PurchaseController.create_grn(purchase_id, recv_by, notes, db)


@router.get("/report/summary", response_model=Dict)
def get_report(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    supplier_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get purchase report by date range and supplier"""
    return PurchaseController.get_report(date_from, date_to, supplier_id, db)

