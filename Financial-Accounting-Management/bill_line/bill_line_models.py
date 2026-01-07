from sqlalchemy import Column, Integer, ForeignKey, Numeric, Text
from database import Base

class BillLine(Base):
    __tablename__ = "bill_lines"

    bill_line_id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(
        Integer,
        ForeignKey("bills.bill_id", ondelete="CASCADE"),
        nullable=False
    )
    expense_account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )
    description = Column(Text)
    amount = Column(Numeric(12, 2), nullable=False)
