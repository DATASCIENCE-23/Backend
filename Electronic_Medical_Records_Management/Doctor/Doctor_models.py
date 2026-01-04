from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database import Base



class Doctor(Base):
    __tablename__ = "doctor"

    doctor_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    specialization_id = Column(Integer, ForeignKey("specializations.specialization_id"))
    qualification = Column(String(150))
    license_number = Column(String(100), unique=True, nullable=False)

    phone_number = Column(String(15), nullable=False)
    email = Column(String(100), unique=True)

    experience_years = Column(Integer)
    consultation_fee = Column(DECIMAL(10, 2))

    date_joined = Column(Date)
    date_of_birth = Column(Date)

    is_active = Column(Boolean, default=True)
