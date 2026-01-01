from sqlalchemy import Column, Integer, String, Text
from database import Base

class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"schema": "hms"}   # ⭐ THIS LINE IS THE FIX

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
