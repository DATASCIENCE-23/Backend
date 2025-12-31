from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from core.database import get_db
from schemas.purchase_schema import POCreate, POResp, POUpdate
from schemas.purchase_item_schema import POItemCreate, POItemResp
from services.purchase_service import POService

router = APIRouter(prefix="/api/po", tags=["purchase"])


@router.post("", response_model=POResp)
def createPO(data: POCreate, db: Session = Depends(get_db)):
    """Create PO"""
    try:
        return POService.createPO(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{purchaseId}/items", response_model=POItemResp)
def addItem(purchaseId: int, data: POItemCreate, db: Session = Depends(get_db)):
    """Add item to PO"""
    try:
        return POService.addItem(db, purchaseId, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{purchaseId}", response_model=POResp)
def getPO(purchaseId: int, db: Session = Depends(get_db)):
    """Get PO"""
    po = POService.getPO(db, purchaseId)
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    return po


@router.get("", response_model=List[POResp])
def listPO(
    supplierId: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    dateFrom: Optional[date] = Query(None),
    dateTo: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """List POs"""
    return POService.listPO(db, supplierId, status, dateFrom, dateTo)


@router.patch("/{purchaseId}", response_model=POResp)
def updateStatus(purchaseId: int, data: POUpdate, db: Session = Depends(get_db)):
    """Update PO status"""
    try:
        return POService.updateStatus(db, purchaseId, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{purchaseId}/items/{itemId}")
def removeItem(purchaseId: int, itemId: int, db: Session = Depends(get_db)):
    """Remove item from PO"""
    try:
        POService.removeItem(db, itemId)
        return {"msg": "Item removed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
