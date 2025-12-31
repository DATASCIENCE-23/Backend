# items/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from Patient.database import Base  # Adjust import if needed
import enum

class StatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))

    items = relationship("Item", back_populates="category")

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(255))

class StoreLocation(Base):
    __tablename__ = "store_locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location_type = Column(String(50))

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    unit_price = Column(Float, nullable=False)
    expiry_applicable = Column(Boolean, default=False)
    minimum_stock_level = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.active)

    category = relationship("Category", back_populates="items")