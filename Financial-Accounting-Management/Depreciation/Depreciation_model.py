from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from Depreciation.database import Base

class Depreciation(Base):
    __tablename__ = "depreciations"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    depreciation_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
