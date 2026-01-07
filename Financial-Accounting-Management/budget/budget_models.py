from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from database import Base

class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, index=True)
    financial_year = Column(String, nullable=False)

    # TEMP: department FK disabled until department module is migrated

    # department_id = Column(
    #     Integer,
    #     ForeignKey("departments.department_id"),
    #     nullable=False
    # )
    department_id = Column(Integer, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
