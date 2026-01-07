from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey, Text
from database import Base

class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    expense_date = Column(Date, nullable=False)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    amount = Column(Numeric(12, 2), nullable=False)

    # TEMP: department FK disabled until department module is migrated

    # department_id = Column(
    #     Integer,
    #     ForeignKey("departments.department_id"),
    #     nullable=False
    # )
    department_id = Column(Integer, nullable=False)


    reference_id = Column(Integer)
    description = Column(Text)
