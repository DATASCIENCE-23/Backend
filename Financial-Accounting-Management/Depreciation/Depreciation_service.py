from sqlalchemy.orm import Session
from Depreciation.Depreciation_model import Depreciation
from Depreciation.Depreciation_repository import DepreciationRepository

class DepreciationService:

    @staticmethod
    def create_depreciation(db: Session, data: dict):
        depreciation = Depreciation(**data)
        return DepreciationRepository.create(db, depreciation)

    @staticmethod
    def list_depreciations(db: Session):
        return DepreciationRepository.get_all(db)
