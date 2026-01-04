from sqlalchemy.orm import Session
from .service import DoctorService
from .repository import DoctorRepository


class DoctorController:
    def __init__(self, db: Session):
        self.service = DoctorService(DoctorRepository(db))

    def create_doctor(self, data: dict):
        return self.service.create_doctor(data)

    def get_doctor(self, doctor_id: int):
        return self.service.get_doctor(doctor_id)

    def get_all_doctors(self):
        return self.service.get_all_doctors()

    def update_doctor(self, doctor_id: int, data: dict):
        return self.service.update_doctor(doctor_id, data)

    def delete_doctor(self, doctor_id: int):
        return self.service.delete_doctor(doctor_id)
