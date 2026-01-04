from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from Patient_Registration_Management.database import Base

class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id", ondelete="CASCADE"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    status = Column(String(30))
    reason_for_visit = Column(Text)
    is_admitted = Column(CHAR(1), default="N", nullable=False)

    # ONE-TO-ONE relationship
    admission_record = relationship(
        "Admission",
        back_populates="appointment_record",
        uselist=False
    )
