from sqlalchemy import Column, Integer, Text, Enum as SQLEnum
from ..database import Base
import enum

class RoleName(enum.Enum):
    admin = "admin"
    doctor = "doctor"
    nurse = "nurse"
    patient = "patient"
    pharmacist = "pharmacist"
    lab_tech = "lab_tech"

class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "hms"}

    role_id = Column(Integer, primary_key=True, autoincrement=True)

    role_name = Column(
        SQLEnum(RoleName, name="role_name_enum"),
        unique=True,
        nullable=False
    )

    description = Column(Text)
