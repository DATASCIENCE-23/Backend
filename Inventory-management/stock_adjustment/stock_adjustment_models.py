from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base
from datetime import date

class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("store_locations.id"), nullable=False)

    adjustment_type = Column(String(20), nullable=False)
    # ADD / SUBTRACT

    quantity_changed = Column(Integer, nullable=False)
    reason = Column(String(255))
    adjustment_date = Column(Date, default=date.today)
