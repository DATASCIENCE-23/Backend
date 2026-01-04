from sqlalchemy import Column, Integer, String
from Patient_Registration_Management.database import Base

class Specialization(Base):
    __tablename__ = "specializations"

    specialization_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
