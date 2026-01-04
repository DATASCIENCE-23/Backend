from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    full_name = Column(String(150), nullable=True)
    status = Column(String(30), default="ACTIVE")

    department_id = Column(Integer, nullable=True)


    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, nullable=True)

    audit_logs = relationship("AuditLog", back_populates="user")