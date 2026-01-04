from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from ..database import Base  # shared Base from your project

class ServiceMaster(Base):
    __tablename__ = "service_master"

    service_id = Column(Integer, primary_key=True, index=True)
    service_code = Column(String(50), unique=True, nullable=False, index=True)
    service_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    standard_price = Column(Numeric(10, 2), nullable=False)  # decimal(10,2)
    #tax_id = Column(Integer, ForeignKey("tax_master.tax_id"), nullable=True)  # adjust table name if different
    is_active = Column(Boolean, default=True, nullable=False)