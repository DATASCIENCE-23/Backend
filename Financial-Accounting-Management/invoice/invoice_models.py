from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column(Integer, primary_key=True, index=True)

        # TEMP: department FK disabled until patient module is migrated

    # patient_id = Column(
    #     Integer,
    #     ForeignKey("patients.patient_id"),
    #     nullable=False
    # )
    patient_id = Column(Integer, nullable=False)


    invoice_date = Column(Date, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    status = Column(String, nullable=False)
