from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from core.database import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "hms"}

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255))
    email = Column(String(100), unique=True)
    full_name = Column(String(150))
    status = Column(String(30), default="active")
    department_id = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
