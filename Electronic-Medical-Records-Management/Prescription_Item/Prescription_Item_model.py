from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class PrescriptionItem(Base):
    __tablename__ = "prescription_item"

    prescription_item_id = Column(Integer, primary_key=True, index=True)

    prescription_id = Column(
        Integer,
        ForeignKey("prescription.prescription_id", ondelete="CASCADE"),
        nullable=False
    )

    medicine_id = Column(Integer, nullable=False)

    prescribed_quantity = Column(Integer, nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    duration_days = Column(Integer, nullable=False)
    instructions = Column(Text)
