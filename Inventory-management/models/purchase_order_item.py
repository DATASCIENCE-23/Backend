from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


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

    po = relationship("PO", back_populates="items")
