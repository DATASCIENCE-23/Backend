from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from BUDGET.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, index=True)

    financial_year = Column(String(20), nullable=False)
    department = Column(String(100), nullable=False)

    total_amount = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "financial_year",
            "department",
            name="uq_budget_year_department"
        ),
    )
