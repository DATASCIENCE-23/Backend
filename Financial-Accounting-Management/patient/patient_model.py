from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from common_base import Base

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    contact_details = Column(String(255))
    insurance_id = Column(Integer)

    # Relationships
    invoices = relationship("Invoice", back_populates="patient")