from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
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

    po = relationship("PO", back_populates="grns")
