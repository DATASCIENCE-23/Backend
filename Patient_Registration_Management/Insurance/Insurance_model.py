from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from database import Base

class Insurance(Base):
    __tablename__ = "insurance"

    insurance_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id", ondelete="CASCADE"), nullable=False)
    provider_name = Column(String(150))
    policy_number = Column(String(100), unique=True, nullable=False)
    coverage_type = Column(String(50))
    coverage_percent = Column(Numeric(5, 2))
    valid_from = Column(Date)
    valid_to = Column(Date)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Insurance(insurance_id={self.insurance_id}, policy_number='{self.policy_number}')>"
    