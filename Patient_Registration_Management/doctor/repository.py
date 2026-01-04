from sqlalchemy.orm import Session
from .models import Doctor


class DoctorRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_doctor(self, doctor: Doctor):
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def get_doctor_by_id(self, doctor_id: int):
        return self.db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()

    def get_all_doctors(self):
        return self.db.query(Doctor).all()

    def update_doctor(self, doctor_id: int, data: dict):
        doctor = self.get_doctor_by_id(doctor_id)
        if not doctor:
            return None

        for key, value in data.items():
            setattr(doctor, key, value)

        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def delete_doctor(self, doctor_id: int):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            self.db.delete(doctor)
            self.db.commit()
        return doctor
