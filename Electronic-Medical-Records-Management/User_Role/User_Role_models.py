from sqlalchemy import Column, Integer, Date, ForeignKey
from database import Base
from datetime import date

class UserRole(Base):
    __tablename__ = "user_roles"

    user_role_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    assigned_date = Column(Date, default=date.today)
