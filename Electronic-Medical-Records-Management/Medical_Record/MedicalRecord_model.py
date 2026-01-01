from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=False, index=True)
    visit_id = Column(Integer, nullable=True)  # Can link to future Appointment/Visit table

    record_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Core clinical fields from user stories
    chief_complaint = Column(Text, nullable=True)
    history_of_present_illness = Column(Text, nullable=True)
    past_medical_history = Column(Text, nullable=True)
    physical_examination = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)                  # Current diagnoses
    treatment_plan = Column(Text, nullable=True)             # Doctor's plan
    clinical_notes = Column(Text, nullable=True)             # General progress/notes (doctor/nurse)
    vital_signs = Column(Text, nullable=True)                # Nurse-entered vitals (JSON or text)
    medication_orders = Column(Text, nullable=True)          # Future: e-prescriptions
    allergies_notified = Column(Text, nullable=True)         # Alerts shown
    notes = Column(Text, nullable=True)                      # Additional free-text

    # Relationships
    patient = relationship("User", foreign_keys=[patient_id], back_populates="medical_records")
    doctor = relationship("User", foreign_keys=[doctor_id])