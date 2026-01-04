from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from JOURNAL_ENTRY.database import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    journal_id = Column(Integer, primary_key=True, index=True)
    journal_date = Column(Date, nullable=False)

    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)

    description = Column(String(255))
    posted_status = Column(Boolean, default=False, nullable=False)

    # -------------------------
    # Relationships
    # -------------------------

    # 1. Journal Entry → Journal Lines (1 : many)
    journal_lines = relationship(
        "JournalLine",
        back_populates="journal_entry",
        cascade="all, delete-orphan"
    )

    # 2. Journal Entry ← Invoice (1 : 1)
    invoice = relationship(
        "Invoice",
        back_populates="journal_entry",
        uselist=False
    )

    # 3. Journal Entry ← Payment (1 : 1)
    payment = relationship(
        "Payment",
        back_populates="journal_entry",
        uselist=False
    )

    # 4. Journal Entry ← Bill (1 : 1)
    bill = relationship(
        "Bill",
        back_populates="journal_entry",
        uselist=False
    )

    # 5. Journal Entry ← Asset capitalization (1 : 1)
    asset = relationship(
        "Asset",
        back_populates="journal_entry",
        uselist=False
    )

    # 6. Journal Entry ← Depreciation posting (1 : 1)
    depreciation = relationship(
        "Depreciation",
        back_populates="journal_entry",
        uselist=False
    )
