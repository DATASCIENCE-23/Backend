from sqlalchemy import Column, Integer, ForeignKey, Numeric
from database import Base

class JournalLine(Base):
    __tablename__ = "journal_lines"

    journal_line_id = Column(Integer, primary_key=True, index=True)

    journal_id = Column(
        Integer,
        ForeignKey("journal_entries.journal_id", ondelete="CASCADE"),
        nullable=False
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    debit_amount = Column(Numeric(12, 2), default=0)
    credit_amount = Column(Numeric(12, 2), default=0)
