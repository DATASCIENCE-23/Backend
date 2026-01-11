from sqlalchemy import Column, Integer, String, ForeignKey
from Patient_Registration_Management.database import Base


class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, index=True)

    street = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    country = Column(String(100))

    patient_id = Column(
        Integer,
        ForeignKey("patients.patient_id", ondelete="CASCADE"),
        nullable=False
    )
