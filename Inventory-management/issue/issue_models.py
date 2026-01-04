from sqlalchemy import Column, Integer, Date, ForeignKey, String
from database import Base
from datetime import date

class IssueRequest(Base):
    __tablename__ = "issue_requests"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    request_date = Column(Date, default=date.today)
    status = Column(String(20), default="pending")  
    # pending / approved / rejected

class IssueDetail(Base):
    __tablename__ = "issue_details"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("issue_requests.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
