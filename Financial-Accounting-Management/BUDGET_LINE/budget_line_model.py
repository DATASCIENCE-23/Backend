from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from BUDGET_LINE.database import Base

class BudgetLine(Base):
    __tablename__ = "budget_lines"

    budget_line_id = Column(Integer, primary_key=True, index=True)

    # FK → Budget
    budget_id = Column(
        Integer,
        ForeignKey("budgets.budget_id", ondelete="CASCADE"),
        nullable=False
    )

    # FK → Account
    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    allocated_amount = Column(Float, nullable=False)

    # -------------------------
    # Relationships
    # -------------------------

    # Many BudgetLines → One Budget
    budget = relationship(
        "Budget",
        back_populates="budget_lines"
    )

    # Many BudgetLines → One Account
    account = relationship(
        "Account",
        back_populates="budget_lines"
    )
