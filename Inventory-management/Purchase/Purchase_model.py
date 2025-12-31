from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from core.database import Base


class GRN(Base):
    __tablename__ = "goods_receipt"
    __table_args__ = {"schema": "hms"}

    receiptId = Column("receipt_id", Integer, primary_key=True)
    purchaseId = Column("purchase_id", Integer, ForeignKey("hms.purchase_order.purchase_id"), nullable=False)
    grnNum = Column("grn_number", String(50), nullable=False, index=True)
    recvDate = Column("receipt_date", Date)
    recvBy = Column("received_by", Integer, ForeignKey("hms.user.user_id"))
    notes = Column(Text)

    # Relationship back to Purchase Order
    po = relationship("PO", back_populates="grns")


class POItem(Base):
    __tablename__ = "purchase_order_item"
    __table_args__ = {"schema": "hms"}

    poItemId = Column("po_item_id", Integer, primary_key=True)
    purchaseId = Column("purchase_id", Integer, ForeignKey("hms.purchase_order.purchase_id"), nullable=False)
    itemId = Column("item_id", Integer, nullable=False)
    orderedQty = Column("ordered_quantity", Integer)
    receivedQty = Column("received_quantity", Integer)
    unitPrice = Column("unit_price", Numeric(10, 2))
    lineTotal = Column("line_total", Numeric(10, 2))
    expiryDate = Column("expiry_date", Date)

    # Relationship back to Purchase Order
    po = relationship("PO", back_populates="items")


class PO(Base):
    __tablename__ = "purchase_order"
    __table_args__ = {"schema": "hms"}

    purchaseId = Column("purchase_id", Integer, primary_key=True)
    poNum = Column("po_number", String(50), nullable=False, index=True)
    orderDate = Column("order_date", Date, nullable=False, index=True)
    supplierId = Column("supplier_id", Integer, ForeignKey("hms.supplier.supplier_id"), nullable=False, index=True)
    totalAmt = Column("total_amount", Numeric(12, 2))
    status = Column(String(30))
    createdBy = Column("created_by", Integer, ForeignKey("hms.user.user_id"))
    expDeliveryDate = Column("expected_delivery_date", Date)

    # Relationships
    items = relationship("POItem", back_populates="po", cascade="all, delete-orphan")
    grns = relationship("GRN", back_populates="po")
