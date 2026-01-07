from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, nullable=False)
    contact_info = Column(String)
    gst_number = Column(String)
    is_active = Column(Boolean, default=True)
