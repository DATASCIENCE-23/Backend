# visit/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False)
    visit_type = Column(String(50), nullable=False)
    visit_date = Column(Date, nullable=False)
    reason_for_visit = Column(String(255))
    status = Column(String(50), default="ACTIVE")

    
