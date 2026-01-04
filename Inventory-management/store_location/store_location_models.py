from sqlalchemy import Column, Integer, String
from database import Base

class StoreLocation(Base):
    __tablename__ = "store_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location_type = Column(String(50))  
    # e.g. Main Store, ICU Store, OT Store
