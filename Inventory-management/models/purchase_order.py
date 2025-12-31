from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


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

    items = relationship("POItem", back_populates="po", cascade="all, delete-orphan")
    grns = relationship("GRN", back_populates="po")
