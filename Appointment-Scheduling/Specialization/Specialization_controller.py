from sqlalchemy.orm import Session
from .specialization_service import SpecializationService
from .specialization_repository import SpecializationRepository


class SpecializationController:

    def __init__(self, db: Session):
        self.service = SpecializationService(
            SpecializationRepository(db)
        )

    def get_all_specializations(self):
        return self.service.list_specializations()

    def get_specialization(self, specialization_id: int):
        return self.service.get_specialization(specialization_id)