from sqlalchemy import Column, Integer, String, Date, Boolean
from JOURNAL_ENTRY.database import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    journal_id = Column(Integer, primary_key=True, index=True)

    journal_date = Column(Date, nullable=False)

    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)

    description = Column(String(255))

    posted_status = Column(Boolean, default=False, nullable=False)
