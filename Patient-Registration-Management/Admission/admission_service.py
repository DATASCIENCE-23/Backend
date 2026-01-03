from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .admission_model import Admission
from .admission_repository import AdmissionRepository
from appointment.appointment_model import Appointment

class AdmissionService:

    @staticmethod
    def admit_patient(db: Session, appointment_id: int, ward: str, bed_number: str, reason: str):
        appointment = db.query(Appointment).filter(
            Appointment.appointment_id == appointment_id
        ).first()

        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.is_admitted != 'Y':
            raise ValueError("Appointment is not marked as admitted")

        if AdmissionRepository.get_by_appointment_id(db, appointment_id):
            raise ValueError("Admission already exists for this appointment")

        admission = Admission(
            appointment_id=appointment_id,
            admission_datetime=datetime.utcnow(),
            ward=ward,
            bed_number=bed_number,
            admission_reason=reason,
            status="ADMITTED"
        )

        return AdmissionRepository.create(db, admission)

    @staticmethod
    def discharge_patient(db: Session, admission_id: int, summary: str):
        admission = AdmissionRepository.get_by_id(db, admission_id)

        if not admission:
            raise ValueError("Admission not found")

        admission.discharge_datetime = datetime.utcnow()
        admission.discharge_summary = summary
        admission.status = "DISCHARGED"

        return AdmissionRepository.update(db, admission)

    @staticmethod
    def get_admission(db: Session, admission_id: int):
        admission = AdmissionRepository.get_by_id(db, admission_id)
        if not admission:
            raise ValueError("Admission not found")
        return admission

    @staticmethod
    def list_active_admissions(db: Session):
        return AdmissionRepository.get_active_admissions(db)

    @staticmethod
    def transfer_bed(db: Session, admission_id: int, ward: str, bed_number: str):
        admission = AdmissionRepository.get_by_id(db, admission_id)

        if not admission:
            raise ValueError("Admission not found")

        if admission.status != "ADMITTED":
            raise ValueError("Cannot transfer bed after discharge")

        admission.ward = ward
        admission.bed_number = bed_number

        return AdmissionRepository.update(db, admission)

    @staticmethod
    def delete_admission(db: Session, admission_id: int):
        admission = AdmissionRepository.get_by_id(db, admission_id)

        if not admission:
            raise ValueError("Admission not found")

        AdmissionRepository.delete(db, admission)
        return {"message": "Admission deleted successfully"}
