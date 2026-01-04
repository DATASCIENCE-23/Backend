from sqlalchemy import Column, Integer, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("store_locations.id"), nullable=False)

    quantity_available = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
