

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey
)
from Patient_Registration_Management.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)

    hospital_id = Column(String(50), unique=True, nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))

    date_of_birth = Column(Date, nullable=False)

    gender = Column(
        Enum("Male", "Female", "Other", name="gender_enum"),
        nullable=False
    )

    blood_group = Column(String(10))
    phone_number = Column(String(15), nullable=False)
    email = Column(String(100))
    marital_status = Column(String(20))

    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(15))

    registration_date = Column(DateTime)

    patient_type = Column(String(50))

    medical_record_number = Column(String(100), unique=True, nullable=False)

    # TODO: enable FK when users table is ready
    # user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user_id = Column(Integer)

    is_active = Column(Boolean, default=True)
