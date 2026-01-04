from sqlalchemy import Column, Integer, Date, ForeignKey
from database import Base
from datetime import date

class StockTransfer(Base):
    __tablename__ = "stock_transfers"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    from_location_id = Column(Integer, ForeignKey("store_locations.id"), nullable=False)
    to_location_id = Column(Integer, ForeignKey("store_locations.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    transfer_date = Column(Date, default=date.today)
