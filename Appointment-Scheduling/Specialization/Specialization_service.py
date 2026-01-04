from Specialization_repository import SpecializationRepository


class SpecializationService:

    def __init__(self, repository: SpecializationRepository):
        self.repository = repository

    def list_specializations(self):
        return self.repository.get_all()

    def get_specialization(self, specialization_id: int):
        return self.repository.get_by_id(specialization_id)