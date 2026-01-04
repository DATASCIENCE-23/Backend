from .Doctor_repository import DoctorRepository
from .Doctor_models import Doctor


class DoctorService:

    def __init__(self, repository: DoctorRepository):
        self.repository = repository

    def create_doctor(self, data: dict):
        doctor = Doctor(**data)
        return self.repository.create_doctor(doctor)

    def get_doctor(self, doctor_id: int):
        return self.repository.get_doctor_by_id(doctor_id)

    def get_all_doctors(self):
        return self.repository.get_all_doctors()

    def update_doctor(self, doctor_id: int, data: dict):
        return self.repository.update_doctor(doctor_id, data)

    def delete_doctor(self, doctor_id: int):
        return self.repository.delete_doctor(doctor_id)
