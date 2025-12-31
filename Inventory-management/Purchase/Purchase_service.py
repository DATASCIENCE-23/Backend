from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime
from typing import List, Optional

# Import models
from models.purchase_order import PO
from models.purchase_order_item import POItem
from models.goods_receipt import GRN

# Import schemas
from schemas.purchase_schema import POCreate, POUpdate
from schemas.purchase_item_schema import POItemCreate


class POService:
    """Service class for managing Purchase Orders"""

    @staticmethod
    def createPO(db: Session, data: POCreate) -> PO:
        """Create purchase order"""
        po = PO(**data.dict())
        db.add(po)
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def addItem(db: Session, purchaseId: int, data: POItemCreate) -> POItem:
        """Add item to PO"""
        po = db.query(PO).filter(PO.purchaseId == purchaseId).first()
        if not po:
            raise ValueError(f"PO {purchaseId} not found")

        # Check duplicate
        existing = db.query(POItem).filter(
            and_(POItem.purchaseId == purchaseId, POItem.itemId == data.itemId)
        ).first()
        if existing:
            raise ValueError(f"Item {data.itemId} already in PO")

        lineTotal = data.orderedQty * data.unitPrice
        item = POItem(
            purchaseId=purchaseId,
            itemId=data.itemId,
            orderedQty=data.orderedQty,
            unitPrice=data.unitPrice,
            lineTotal=lineTotal,
            expiryDate=data.expiryDate
        )
        db.add(item)
        db.commit()
        POService.updateTotal(db, purchaseId)
        db.refresh(item)
        return item

    @staticmethod
    def updateTotal(db: Session, purchaseId: int) -> None:
        """Update PO total"""
        items = db.query(POItem).filter(POItem.purchaseId == purchaseId).all()
        total = sum(item.lineTotal for item in items)
        po = db.query(PO).filter(PO.purchaseId == purchaseId).first()
        if po:
            po.totalAmt = total
            db.commit()

    @staticmethod
    def getPO(db: Session, purchaseId: int) -> Optional[PO]:
        """Get PO by ID"""
        return db.query(PO).filter(PO.purchaseId == purchaseId).first()

    @staticmethod
    def listPO(
        db: Session,
        supplierId: Optional[int] = None,
        status: Optional[str] = None,
        dateFrom: Optional[date] = None,
        dateTo: Optional[date] = None
    ) -> List[PO]:
        """List POs with filters"""
        query = db.query(PO)
        if supplierId:
            query = query.filter(PO.supplierId == supplierId)
        if status:
            query = query.filter(PO.status == status)
        if dateFrom:
            query = query.filter(PO.orderDate >= dateFrom)
        if dateTo:
            query = query.filter(PO.orderDate <= dateTo)
        return query.all()

    @staticmethod
    def updateStatus(db: Session, purchaseId: int, data: POUpdate) -> PO:
        """Update PO status"""
        po = db.query(PO).filter(PO.purchaseId == purchaseId).first()
        if not po:
            raise ValueError(f"PO {purchaseId} not found")
        if data.status:
            po.status = data.status
        if data.expDeliveryDate:
            po.expDeliveryDate = data.expDeliveryDate
        if data.totalAmt:
            po.totalAmt = data.totalAmt
        db.commit()
        db.refresh(po)
        return po

    @staticmethod
    def removeItem(db: Session, itemId: int) -> None:
        """Remove item from PO"""
        item = db.query(POItem).filter(POItem.poItemId == itemId).first()
        if not item:
            raise ValueError(f"Item {itemId} not found")
        purchaseId = item.purchaseId
        db.delete(item)
        db.commit()
        POService.updateTotal(db, purchaseId)


class GRNService:
    """Service class for managing Goods Receipt Notes (GRN)"""

    @staticmethod
    def genGRN(db: Session) -> str:
        """Generate sequential GRN: GRN-YYYY-MM-XXXXX"""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        count = db.query(GRN).filter(
            GRN.grnNum.like(f"GRN-{year}-{month}-%")
        ).count()
        seq = str(count + 1).zfill(5)
        return f"GRN-{year}-{month}-{seq}"

    @staticmethod
    def createGRN(db: Session, purchaseId: int, recvBy: int, notes: str = None) -> GRN:
        """Create GRN"""
        grnNum = GRNService.genGRN(db)
        grn = GRN(
            purchaseId=purchaseId,
            grnNum=grnNum,
            recvDate=datetime.now().date(),
            recvBy=recvBy,
            notes=notes
        )
        db.add(grn)
        db.commit()
        db.refresh(grn)
        return grn
