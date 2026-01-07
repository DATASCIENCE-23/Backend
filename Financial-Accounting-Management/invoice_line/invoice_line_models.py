from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from database import Base

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    invoice_line_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.invoice_id", ondelete="CASCADE"),
        nullable=False
    )

    service_name = Column(String, nullable=False)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    line_total = Column(Numeric(12, 2), nullable=False)
