from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from issue.database import Base  # assuming shared database.py

class IssueRequest(Base):
    __tablename__ = "issue_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    request_number = Column(String(50), unique=True, index=True, nullable=False)
    department_id = Column(Integer, nullable=False)  # FK to departments table
    request_datetime = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(
        Enum(
            "draft", "pending_approval", "approved", "partially_issued",
            "completed", "cancelled",
            name="issue_status_enum"
        ),
        default="draft",
        nullable=False
    )
    requested_by = Column(Integer, nullable=False)  # User ID
    approved_by = Column(Integer, nullable=True)

    details = relationship("IssueDetail", back_populates="request", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("request_number", name="uq_issue_request_number"),
    )


class IssueDetail(Base):
    __tablename__ = "issue_details"

    issue_detail_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("issue_requests.request_id", ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, nullable=False)  # FK to items table
    requested_quantity = Column(Integer, nullable=False)
    issued_quantity = Column(Integer, default=0)
    issued_datetime = Column(DateTime, nullable=True)
    issued_by = Column(Integer, nullable=True)

    request = relationship("IssueRequest", back_populates="details")