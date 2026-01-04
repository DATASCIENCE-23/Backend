from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, UniqueConstraint
from database import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))

    dob = Column(Date, nullable=False)

    gender = Column(
        Enum("Male", "Female", "Other", name="gender_enum"),
        nullable=False
    )

    blood_group = Column(
        Enum(
            "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-",
            name="blood_group_enum"
        ),
        nullable=False
    )

    phone = Column(String(20), nullable=False, unique=True)

    emergency_contact_name = Column(String(100), nullable=False)
    emergency_contact_phone = Column(String(20), nullable=False)

    patient_type = Column(
        Enum("Inpatient", "Outpatient", name="patient_type_enum"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("phone", name="uq_patient_phone"),
    )
