from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from ..database import Base
from sqlalchemy.orm import relationship

class MedicalRecord(Base):
    __tablename__ = "medical_record"

    record_id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.doctor_id"), nullable=False)

    visit_id = Column(Integer, nullable=True)
    record_date = Column(DateTime, default=datetime.utcnow)

    chief_complaint = Column(Text)
    history_of_present_illness = Column(Text)
    past_medical_history = Column(Text)
    physical_examination = Column(Text)
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    notes = Column(Text)

    reports = relationship("Report", back_populates="medical_record", cascade="all, delete-orphan")