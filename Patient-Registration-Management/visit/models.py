# visit/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    visit_type = Column(String(50))
    visit_date = Column(Date)
    reason_for_visit = Column(String(255))
    status = Column(String(50))
