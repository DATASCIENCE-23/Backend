from sqlalchemy import Column, Integer, ForeignKey, Numeric
from database import Base

class BudgetLine(Base):
    __tablename__ = "budget_lines"

    budget_line_id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(
        Integer,
        ForeignKey("budgets.budget_id", ondelete="CASCADE"),
        nullable=False
    )
    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )
    allocated_amount = Column(Numeric(12, 2), nullable=False)
