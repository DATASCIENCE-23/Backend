from sqlalchemy import (
    Column,
    Integer,
    Date,
    Time,
    Text,
    DateTime,
    Enum,
    ForeignKey
)
from sqlalchemy.sql import func
from Waiting_List.Waiting_List_config import Base
import enum


# ================= ENUM =================

class WaitingListStatusEnum(enum.Enum):
    ACTIVE = "Active"
    NOTIFIED = "Notified"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"


# ================= MODEL =================

class WaitingList(Base):
    __tablename__ = "waiting_list"
    __table_args__ = {"schema": "hms"}   # IMPORTANT – must match DB schema

    waiting_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # -------- Foreign Keys --------
    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id"),
        nullable=False,
        index=True
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.doctor_id"),
        nullable=False,
        index=True
    )

    # -------- Preferred Slot --------
    preferred_date = Column(
        Date,
        nullable=False,
        index=True
    )

    preferred_time_start = Column(
        Time,
        nullable=False
    )

    preferred_time_end = Column(
        Time,
        nullable=False
    )

    # -------- Reason --------
    reason = Column(
        Text,
        nullable=True
    )

    # -------- Status --------
    status = Column(
        Enum(
            WaitingListStatusEnum,
            name="waiting_list_status_enum",
            create_type=False   # VERY IMPORTANT
        ),
        nullable=False,
        default=WaitingListStatusEnum.ACTIVE,
        index=True
    )

    # -------- Timestamps --------
    added_at = Column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    notified_at = Column(
        DateTime,
        nullable=True
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    def __repr__(self):
        return (
            f"<WaitingList("
            f"waiting_id={self.waiting_id}, "
            f"patient_id={self.patient_id}, "
            f"doctor_id={self.doctor_id}, "
            f"status={self.status}"
            f")>"
        )
