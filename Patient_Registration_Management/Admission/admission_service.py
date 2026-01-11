from datetime import datetime
from sqlalchemy.orm import Session
from .admission_model import Admission
from .admission_repository import AdmissionRepository
from Patient_Registration_Management.Appointment.appointment_model import Appointment

class AdmissionService:

    def __init__(self, db: Session):
        self.db = db

    def admit_patient(self, data: dict):
        appointment_id = data["appointment_id"]
        ward = data["ward"]
        bed_number = data["bed_number"]
        reason = data["admission_reason"]

        appointment = self.db.query(Appointment).filter(
            Appointment.appointment_id == appointment_id
        ).first()
        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.is_admitted != 'Y':
            raise ValueError("Appointment is not marked as admitted")

        if AdmissionRepository.get_by_appointment_id(self.db, appointment_id):
            raise ValueError("Admission already exists for this appointment")

        admission = Admission(
            appointment_id=appointment_id,
            admission_datetime=datetime.utcnow(),
            ward=ward,
            bed_number=bed_number,
            admission_reason=reason,
            status="ADMITTED"
        )

        return AdmissionRepository.create(self.db, admission)

    def discharge_patient(self, admission_id: int, summary: str):
        admission = AdmissionRepository.get_by_id(self.db, admission_id)
        if not admission:
            raise ValueError("Admission not found")

        admission.discharge_datetime = datetime.utcnow()
        admission.discharge_summary = summary
        admission.status = "DISCHARGED"

        return AdmissionRepository.update(self.db, admission)

    def get_admission(self, admission_id: int):
        admission = AdmissionRepository.get_by_id(self.db, admission_id)
        if not admission:
            raise ValueError("Admission not found")
        return admission

    def list_active_admissions(self):
        return AdmissionRepository.get_active_admissions(self.db)

    def transfer_bed(self, admission_id: int, ward: str, bed_number: str):
        admission = AdmissionRepository.get_by_id(self.db, admission_id)
        if not admission:
            raise ValueError("Admission not found")
        if admission.status != "ADMITTED":
            raise ValueError("Cannot transfer bed after discharge")

        admission.ward = ward
        admission.bed_number = bed_number
        return AdmissionRepository.update(self.db, admission)

    def update_admission(self, admission_id: int, data: dict):
        admission = AdmissionRepository.get_by_id(self.db, admission_id)
        if not admission:
            raise ValueError("Admission not found")

        for key, value in data.items():
            setattr(admission, key, value)

        return AdmissionRepository.update(self.db, admission)

    def delete_admission(self, admission_id: int):
        admission = AdmissionRepository.get_by_id(self.db, admission_id)
        if not admission:
            raise ValueError("Admission not found")
        AdmissionRepository.delete(self.db, admission)
        return {"message": "Admission deleted successfully"}
