# Prescription/Prescription_model.py
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from datetime import datetime
from database import Base
class Prescription(Base):
    __tablename__ = "prescription"

    prescription_id = Column(Integer, primary_key=True, index=True)

    record_id = Column(
        Integer,
        ForeignKey("medical_record.record_id", ondelete="CASCADE"),
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("patient.id"),  # ✅ FIXED
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctor.doctor_id"),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default="Active")
    notes = Column(Text)
