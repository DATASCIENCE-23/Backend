from sqlalchemy import Column, Integer, String, Date, Numeric
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, nullable=False)
    purchase_date = Column(Date)
    purchase_cost = Column(Numeric(12, 2), nullable=False)
    useful_life_years = Column(Integer, nullable=False)
    salvage_value = Column(Numeric(12, 2), default=0)
