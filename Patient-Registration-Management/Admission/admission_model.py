from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .admission_configuration import Base

class Admission(Base):
    __tablename__ = "admission"

    admission_id = Column(Integer, primary_key=True, index=True)

    appointment_id = Column(
        Integer,
        ForeignKey("appointment.appointment_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    admission_datetime = Column(TIMESTAMP)
    discharge_datetime = Column(TIMESTAMP)
    ward = Column(String(100))
    bed_number = Column(String(20))
    admission_reason = Column(Text)
    discharge_summary = Column(Text)
    status = Column(String(30))

    appointment = relationship("Appointment", backref="admission", uselist=False)
