from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from database import Base
import enum

class ItemStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    unit_price = Column(Float, nullable=False)

    minimum_stock_level = Column(Integer, nullable=False)
    expiry_applicable = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    status = Column(Enum(ItemStatus), default=ItemStatus.active)
