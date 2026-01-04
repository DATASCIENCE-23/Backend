from sqlalchemy import Column, Integer, Float, ForeignKey
from BUDGET_LINE.database import Base

class BudgetLine(Base):
    __tablename__ = "budget_lines"

    budget_line_id = Column(Integer, primary_key=True, index=True)

    budget_id = Column(
        Integer,
        ForeignKey("budgets.budget_id", ondelete="CASCADE"),
        nullable=False
    )

    account_id = Column(Integer, nullable=False)

    allocated_amount = Column(Float, nullable=False)
