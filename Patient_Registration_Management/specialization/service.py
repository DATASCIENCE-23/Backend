from .repository import SpecializationRepository
from .models import Specialization

class SpecializationService:
    def __init__(self, repository: SpecializationRepository):
        self.repository = repository

    def create_specialization(self, data):
        # convert Pydantic model to dict if necessary
        specialization_data = data.dict() if hasattr(data, "dict") else data
        specialization = Specialization(**specialization_data)
        return self.repository.create(specialization)

    def get_specialization(self, specialization_id: int):
        return self.repository.get_by_id(specialization_id)

    def get_all_specializations(self):
        return self.repository.get_all()

    def update_specialization(self, specialization_id: int, data):
        update_data = data.dict(exclude_unset=True) if hasattr(data, "dict") else data
        return self.repository.update(specialization_id, update_data)

    def delete_specialization(self, specialization_id: int):
        return self.repository.delete(specialization_id)
