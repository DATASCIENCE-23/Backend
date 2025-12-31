from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, UniqueConstraint
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    role = Column(
        Enum("Admin", "Doctor", "Nurse", "Patient", name="user_role_enum"),
        nullable=False
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("phone", name="uq_user_phone"),
    )