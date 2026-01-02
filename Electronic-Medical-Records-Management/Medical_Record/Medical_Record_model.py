from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime
from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_record"

    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    visit_id = Column(Integer, nullable=True)

    record_date = Column(DateTime, default=datetime.utcnow)

    chief_complaint = Column(Text)
    history_of_present_illness = Column(Text)
    past_medical_history = Column(Text)
    physical_examination = Column(Text)

    diagnosis = Column(Text)          # ✅ THIS WAS MISSING
    treatment_plan = Column(Text)
    notes = Column(Text)
