from sqlalchemy.orm import Session
from .Prescription_repository import PrescriptionRepository

class PrescriptionService:
    def __init__(self, db: Session):
        self.db = db

    def create_prescription(self, current_user_id: int, record_id: int, patient_id: int, payload: dict):
        notes = payload.get("notes")
        status = payload.get("status", "Active")
        return PrescriptionRepository.create_prescription(
            self.db, record_id, patient_id, current_user_id, notes, status
        )

    def get_prescription(self, prescription_id: int):
        prescription = PrescriptionRepository.get_prescription_by_id(self.db, prescription_id)
        if not prescription:
            raise ValueError("Prescription not found")
        return prescription

    def get_patient_prescriptions(self, patient_id: int):
        return PrescriptionRepository.get_prescriptions_by_patient(self.db, patient_id)

    def get_prescriptions_for_record(self, record_id: int):
        return PrescriptionRepository.get_prescriptions_by_record(self.db, record_id)

    def update_prescription(self, prescription_id: int, payload: dict):
        return PrescriptionRepository.update_prescription(self.db, prescription_id, payload)

    def cancel_prescription(self, prescription_id: int):
        return PrescriptionRepository.update_prescription(
            self.db, prescription_id, {"status": "Cancelled"}
        )

    def delete_prescription(self, prescription_id: int):
        PrescriptionRepository.delete_prescription(self.db, prescription_id)