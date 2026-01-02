from sqlalchemy.orm import Session
from Insurance_model import Insurance
from Insurance_repository import InsuranceRepository
#from Repository.Patient_repository import PatientRepository

class InsuranceService:

    @staticmethod
    def create_insurance(db: Session, data: dict):
        # Check if patient exists
        #if not PatientRepository.get_by_id(db, data["patient_id"]):
        #    raise ValueError("Patient not found")

        if InsuranceRepository.get_by_policy_number(db, data["policy_number"]):
            raise ValueError("Insurance with this policy number already exists")

        insurance = Insurance(**data)
        return InsuranceRepository.create(db, insurance)

    @staticmethod
    def get_insurance(db: Session, insurance_id: int):
        insurance = InsuranceRepository.get_by_id(db, insurance_id)
        if not insurance:
            raise ValueError("Insurance not found")
        return insurance

    @staticmethod
    def list_insurances(db: Session):
        return InsuranceRepository.get_all(db)

    @staticmethod
    def update_insurance(db: Session, insurance_id: int, data: dict):
        insurance = InsuranceRepository.get_by_id(db, insurance_id)
        if not insurance:
            raise ValueError("Insurance not found")

        for key, value in data.items():
            setattr(insurance, key, value)

        return InsuranceRepository.update(db, insurance)

    @staticmethod
    def delete_insurance(db: Session, insurance_id: int):
        insurance = InsuranceRepository.get_by_id(db, insurance_id)
        if not insurance:
            raise ValueError("Insurance not found")

        InsuranceRepository.delete(db, insurance)
