from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime
from typing import List, Optional, Dict

from Purchase_model import PO, POItem, GRN
from Purchase_repository import PurchaseRepository
from Purchase_schema import POCreate, POUpdate, POItemCreate


class PurchaseService:
    """Service layer for Purchase Order operations"""

    @staticmethod
    def _validate_supplier(db: Session, supplier_id: int) -> bool:
        """Validate supplier exists"""
        result = db.execute(text("SELECT 1 FROM hms.supplier WHERE supplier_id = :id"), {"id": supplier_id})
        return result.first() is not None

    @staticmethod
    def _validate_item(db: Session, item_id: int) -> bool:
        """Validate item exists"""
        result = db.execute(text("SELECT 1 FROM hms.item WHERE item_id = :id"), {"id": item_id})
        return result.first() is not None

    @staticmethod
    def createPO(db: Session, data: POCreate) -> PO:
        """Create purchase order with validation"""
        # Validate supplier exists
        if not PurchaseService._validate_supplier(db, data.supplierId):
            raise ValueError(f"Supplier {data.supplierId} does not exist")
        
        po = PO(**data.dict())
        return PurchaseRepository.create_po(db, po)

    @staticmethod
    def getPO(db: Session, purchase_id: int) -> Optional[PO]:
        """Get purchase order by ID"""
        return PurchaseRepository.get_po(db, purchase_id)

    @staticmethod
    def listPO(
        db: Session,
        supplier_id: Optional[int] = None,
        status: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[PO]:
        """List purchase orders"""
        return PurchaseRepository.list_po(db, supplier_id, status, date_from, date_to)

    @staticmethod
    def updateStatus(db: Session, purchase_id: int, data: POUpdate) -> PO:
        """Update purchase order status"""
        po = PurchaseRepository.get_po(db, purchase_id)
        if not po:
            raise ValueError(f"PO {purchase_id} not found")
        
        # If approving, update stock
        if data.status == "approved" and po.status != "approved":
            PurchaseService._update_stock_on_approval(db, po)
        
        if data.status:
            po.status = data.status
        if data.expDeliveryDate:
            po.expDeliveryDate = data.expDeliveryDate
        if data.totalAmt:
            po.totalAmt = data.totalAmt
        
        return PurchaseRepository.update_po(db, po)

    @staticmethod
    def _update_stock_on_approval(db: Session, po: PO) -> None:
        """Update stock when PO is approved"""
        for item in po.items:
            # Add to default location (location_id = 1, adjust as needed)
            db.execute(text("""
                INSERT INTO hms.stock (item_id, location_id, quantity_available, reserved_quantity, last_updated)
                VALUES (:item_id, 1, :qty, 0, NOW())
                ON CONFLICT (item_id, location_id) DO UPDATE
                SET quantity_available = quantity_available + :qty, last_updated = NOW()
            """), {"item_id": item.itemId, "qty": item.orderedQty})
        db.commit()

    @staticmethod
    def addItem(db: Session, purchase_id: int, data: POItemCreate) -> POItem:
        """Add item to purchase order with validation"""
        po = PurchaseRepository.get_po(db, purchase_id)
        if not po:
            raise ValueError(f"PO {purchase_id} not found")

        # Validate item exists
        if not PurchaseService._validate_item(db, data.itemId):
            raise ValueError(f"Item {data.itemId} does not exist")

        # Check for duplicate
        existing = PurchaseRepository.check_duplicate_item(db, purchase_id, data.itemId)
        if existing:
            raise ValueError(f"Item {data.itemId} already in PO")

        line_total = data.orderedQty * data.unitPrice
        item = POItem(
            purchaseId=purchase_id,
            itemId=data.itemId,
            orderedQty=data.orderedQty,
            unitPrice=data.unitPrice,
            lineTotal=line_total,
            expiryDate=data.expiryDate
        )
        
        item = PurchaseRepository.add_item(db, item)
        PurchaseService.updateTotal(db, purchase_id)
        return item

    @staticmethod
    def removeItem(db: Session, item_id: int) -> None:
        """Remove item from purchase order"""
        item = PurchaseRepository.get_item(db, item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")
        
        purchase_id = item.purchaseId
        PurchaseRepository.delete_item(db, item)
        PurchaseService.updateTotal(db, purchase_id)

    @staticmethod
    def updateTotal(db: Session, purchase_id: int) -> None:
        """Update purchase order total"""
        items = PurchaseRepository.get_items_by_po(db, purchase_id)
        total = sum(item.lineTotal for item in items) if items else 0
        
        po = PurchaseRepository.get_po(db, purchase_id)
        if po:
            po.totalAmt = total
            PurchaseRepository.update_po(db, po)

    @staticmethod
    def get_purchase_report(
        db: Session,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        supplier_id: Optional[int] = None
    ) -> Dict:
        """Generate purchase report"""
        query = """
            SELECT 
                po.purchase_id,
                po.po_number,
                po.order_date,
                s.supplier_name,
                po.total_amount,
                po.status,
                COUNT(poi.po_item_id) as item_count
            FROM hms.purchase_order po
            LEFT JOIN hms.supplier s ON po.supplier_id = s.supplier_id
            LEFT JOIN hms.purchase_order_item poi ON po.purchase_id = poi.purchase_id
            WHERE 1=1
        """
        params = {}
        
        if date_from:
            query += " AND po.order_date >= :date_from"
            params["date_from"] = date_from
        if date_to:
            query += " AND po.order_date <= :date_to"
            params["date_to"] = date_to
        if supplier_id:
            query += " AND po.supplier_id = :supplier_id"
            params["supplier_id"] = supplier_id
        
        query += " GROUP BY po.purchase_id, s.supplier_name ORDER BY po.order_date DESC"
        
        result = db.execute(text(query), params)
        rows = result.fetchall()
        
        total_amount = sum(row[4] for row in rows) if rows else 0
        
        return {
            "total_pos": len(rows),
            "total_amount": float(total_amount),
            "purchases": [
                {
                    "purchase_id": row[0],
                    "po_number": row[1],
                    "order_date": row[2],
                    "supplier_name": row[3],
                    "total_amount": float(row[4]),
                    "status": row[5],
                    "item_count": row[6]
                }
                for row in rows
            ]
        }


class GRNService:
    """Service layer for Goods Receipt Note operations"""

    @staticmethod
    def genGRN(db: Session) -> str:
        """Generate sequential GRN: GRN-YYYY-MM-XXXXX"""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        count = PurchaseRepository.count_grn_for_month(db, year, month)
        seq = str(count + 1).zfill(5)
        return f"GRN-{year}-{month}-{seq}"

    @staticmethod
    def createGRN(db: Session, purchase_id: int, recv_by: int, notes: str = None) -> GRN:
        """Create goods receipt note"""
        grn_num = GRNService.genGRN(db)
        grn = GRN(
            purchaseId=purchase_id,
            grnNum=grn_num,
            recvDate=datetime.now().date(),
            recvBy=recv_by,
            notes=notes
        )
        return PurchaseRepository.create_grn(db, grn)

