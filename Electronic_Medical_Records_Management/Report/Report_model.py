from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from ..database import Base


class Report(Base):
    __tablename__ = "report"

    report_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("medical_record.record_id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(String(100), nullable=False)  # e.g., "lab", "discharge_summary", "radiology"
    report_date = Column(Date, default=date.today, nullable=False)
    findings = Column(String, nullable=False)  # Main content of the report (text)

    # Relationship back to MedicalRecord
    medical_record = relationship("MedicalRecord", back_populates="reports")


# IMPORTANT: In your MedicalRecord model (in MedicalRecord_model.py or similar),
# you should have this line:
# reports = relationship("Report", back_populates="medical_record", cascade="all, delete-orphan")