from .repository import DoctorRepository
from .models import Doctor
from Patient_Registration_Management.user.models import User
from Patient_Registration_Management.specialization.models import Specialization


class DoctorService:

    def __init__(self, repository: DoctorRepository):
        self.repository = repository
        self.db = repository.db

    def create_doctor(self, data: dict):
        # ✅ Validate User
        user = self.db.query(User).filter(
            User.user_id == data["user_id"],
            User.is_active == True
        ).first()
        if not user:
            raise ValueError("Invalid user_id: User does not exist")

        # ✅ Validate Specialization
        if data.get("specialization_id"):
            specialization = self.db.query(Specialization).filter(
                Specialization.specialization_id == data["specialization_id"],
                Specialization.is_active == True
            ).first()
            if not specialization:
                raise ValueError("Invalid specialization_id: Specialization does not exist")

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
