from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Text,
    ForeignKey,
    CHAR
)
from sqlalchemy.orm import relationship
from Patient.database import Base


class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patient.patient_id", ondelete="CASCADE"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctor.doctor_id", ondelete="CASCADE"),
        nullable=False
    )

    schedule_id = Column(
        Integer,
        ForeignKey("doctor_schedule.schedule_id", ondelete="CASCADE"),
        nullable=False
    )

    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)

    status = Column(String(30))
    reason_for_visit = Column(Text)

    is_admitted = Column(
        CHAR(1),
        default="N",
        nullable=False
    )

    admission = relationship(
        "Admission",
        back_populates="appointment",
        uselist=False
    )
