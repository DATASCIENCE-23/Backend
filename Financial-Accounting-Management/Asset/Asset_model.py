from sqlalchemy import Column, Integer, String, Date, Float
from Asset.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String(150), nullable=False)
    purchase_date = Column(Date, nullable=False)
    purchase_cost = Column(Float, nullable=False)
    useful_life_years = Column(Integer, nullable=False)
    salvage_value = Column(Float, default=0.0)
