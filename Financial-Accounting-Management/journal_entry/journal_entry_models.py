from sqlalchemy import Column, Integer, Date, String, Boolean, Text, ForeignKey
from database import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    journal_id = Column(Integer, primary_key=True, index=True)
    journal_date = Column(Date, nullable=False)
    reference_type = Column(String)
    reference_id = Column(Integer)
    description = Column(Text)
    posted_status = Column(Boolean, default=False)

    #created_by FK disabled until user module is migrated
    # created_by = Column(
    #     Integer,
    #     ForeignKey("users.user_id"),
    #     nullable=True
    # )
    created_by = Column(Integer, nullable=True)

