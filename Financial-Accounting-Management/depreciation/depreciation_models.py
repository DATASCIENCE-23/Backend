from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey
from database import Base

class Depreciation(Base):
    __tablename__ = "depreciations"

    depreciation_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(
        Integer,
        ForeignKey("assets.asset_id"),
        nullable=False
    )
    depreciation_date = Column(Date, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    journal_id = Column(
        Integer,
        ForeignKey("journal_entries.journal_id"),
        nullable=True
    )
