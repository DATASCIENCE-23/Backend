from sqlalchemy import Column, Integer, Float, ForeignKey, CheckConstraint
from JOURNAL_LINE.database import Base

class JournalLine(Base):
    __tablename__ = "journal_lines"

    journal_line_id = Column(Integer, primary_key=True, index=True)

    journal_id = Column(
        Integer,
        ForeignKey("journal_entries.journal_id", ondelete="CASCADE"),
        nullable=False
    )

    account_id = Column(Integer, nullable=False)

    debit_amount = Column(Float, default=0.0)
    credit_amount = Column(Float, default=0.0)

    __table_args__ = (
        CheckConstraint(
            "(debit_amount >= 0 AND credit_amount >= 0)",
            name="chk_debit_credit_non_negative"
        ),
    )
