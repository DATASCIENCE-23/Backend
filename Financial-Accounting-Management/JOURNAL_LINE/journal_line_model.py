from sqlalchemy import Column, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from JOURNAL_LINE.database import Base

class JournalLine(Base):
    __tablename__ = "journal_lines"

    journal_line_id = Column(Integer, primary_key=True, index=True)

    # FK → Journal Entry
    journal_id = Column(
        Integer,
        ForeignKey("journal_entries.journal_id", ondelete="CASCADE"),
        nullable=False
    )

    # FK → Account
    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    debit_amount = Column(Float, default=0.0)
    credit_amount = Column(Float, default=0.0)

    __table_args__ = (
        CheckConstraint(
            "(debit_amount >= 0 AND credit_amount >= 0)",
            name="chk_debit_credit_non_negative"
        ),
        CheckConstraint(
            "(debit_amount = 0 AND credit_amount > 0) OR "
            "(credit_amount = 0 AND debit_amount > 0)",
            name="chk_only_one_side_positive"
        ),
    )

    # -------------------------
    # Relationships
    # -------------------------

    # Many JournalLines → One JournalEntry
    journal_entry = relationship(
        "JournalEntry",
        back_populates="journal_lines"
    )

    # Many JournalLines → One Account
    account = relationship(
        "Account",
        back_populates="journal_lines"
    )
