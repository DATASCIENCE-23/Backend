from sqlalchemy import Column, Integer, String, Boolean
from Patient_Registration_Management.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(150), unique=True)
    is_active = Column(Boolean, default=True)

    role = Column(String(20), default="USER", nullable=False)