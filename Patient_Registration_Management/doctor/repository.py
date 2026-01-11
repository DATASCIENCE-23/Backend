# Patient_Registration_Management/doctor/repository.py

from sqlalchemy.orm import Session
from .models import Doctor

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class DoctorRepository:
    def __init__(self, db):
        self.db = db

    def create_doctor(self, doctor):
        try:
            self.db.add(doctor)
            self.db.commit()
            self.db.refresh(doctor)
            return doctor
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Doctor with this license number or email already exists"
            )


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
            doctor.is_active = False  # Soft delete
            self.db.commit()
            self.db.refresh(doctor)
        return doctor
