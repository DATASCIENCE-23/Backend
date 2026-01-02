# Prescription/Prescription_service.py
from .Prescription_repository import PrescriptionRepository

class PrescriptionService:
    def __init__(self, db):
        self.db = db

    def create_prescription(self, doctor_id: int, record_id: int, patient_id: int, payload: dict):
        return PrescriptionRepository.create(
            self.db,
            record_id,
            patient_id,
            doctor_id,
            payload.get("notes")
        )

    def get_prescription(self, prescription_id: int):
        prescription = PrescriptionRepository.get_by_id(self.db, prescription_id)
        if not prescription:
            raise ValueError("Prescription not found")
        return prescription

    def get_patient_prescriptions(self, patient_id: int):
        return PrescriptionRepository.get_by_patient(self.db, patient_id)

    def get_record_prescriptions(self, record_id: int):
        return PrescriptionRepository.get_by_record(self.db, record_id)

    def cancel_prescription(self, prescription_id: int):
        return PrescriptionRepository.update(
            self.db,
            prescription_id,
            {"status": "Cancelled"}
        )
    def update_prescription(self, prescription_id: int, payload: dict):
        return PrescriptionRepository.update_prescription(
            self.db, prescription_id, payload
        )
    def delete_prescription(self, prescription_id: int):
        PrescriptionRepository.delete_prescription(self.db, prescription_id)
