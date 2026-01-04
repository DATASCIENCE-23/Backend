from sqlalchemy import Column, Integer, Date, ForeignKey, String
from database import Base
from datetime import date

class StockAudit(Base):
    __tablename__ = "stock_audits"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("store_locations.id"), nullable=False)
    audit_date = Column(Date, default=date.today)
    remarks = Column(String(255))

class StockAuditDetail(Base):
    __tablename__ = "stock_audit_details"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("stock_audits.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    system_quantity = Column(Integer, nullable=False)
    physical_quantity = Column(Integer, nullable=False)
    difference = Column(Integer, nullable=False)
