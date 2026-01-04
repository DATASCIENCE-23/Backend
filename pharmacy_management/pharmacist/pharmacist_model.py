from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from ..database import Base

class Pharmacist(Base):
    __tablename__ = "pharmacist"

    pharmacist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    employee_code = Column(String(50), unique=True, nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    dispenses = relationship("Dispense", back_populates="pharmacist")

    def __repr__(self):
        return f"<Pharmacist {self.first_name} {self.last_name}>"

