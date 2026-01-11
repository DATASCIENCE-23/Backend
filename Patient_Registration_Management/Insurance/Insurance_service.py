from sqlalchemy.orm import Session
from .Insurance_model import Insurance
from .Insurance_repository import InsuranceRepository

class InsuranceService:
    def __init__(self, db: Session):
        self.db = db

    def create_insurance(self, data: dict):
        if InsuranceRepository.get_by_policy_number(self.db, data["policy_number"]):
            raise ValueError("Insurance with this policy number already exists")
        insurance = Insurance(**data)
        return InsuranceRepository.create(self.db, insurance)

    def get_insurance(self, insurance_id: int):
        insurance = InsuranceRepository.get_by_id(self.db, insurance_id)
        if not insurance:
            raise ValueError("Insurance not found")
        return insurance

    def list_insurances(self):
        return InsuranceRepository.get_all(self.db)

    def update_insurance(self, insurance_id: int, data: dict):
        insurance = InsuranceRepository.get_by_id(self.db, insurance_id)
        if not insurance:
            raise ValueError("Insurance not found")
        for key, value in data.items():
            setattr(insurance, key, value)
        return InsuranceRepository.update(self.db, insurance)

    def delete_insurance(self, insurance_id: int):
        insurance = InsuranceRepository.get_by_id(self.db, insurance_id)
        if not insurance:
            raise ValueError("Insurance not found")
        InsuranceRepository.delete(self.db, insurance)
