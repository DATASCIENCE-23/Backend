from sqlalchemy.orm import Session
from PATIENT.patient_model import Patient
from PATIENT.patient_repository import PatientRepository


class PatientService:
    """
    Business logic for Patient
    """

    @staticmethod
    def register_patient(db: Session, payload: dict) -> Patient:
        """
        Register a new patient
        """
        patient_name = payload.get("patient_name")
        contact_details = payload.get("contact_details")
        insurance_id = payload.get("insurance_id")

        if not patient_name:
            raise ValueError("Patient name is required")

        patient = Patient(
            patient_name=patient_name,
            contact_details=contact_details,
            insurance_id=insurance_id
        )

        return PatientRepository.create(db, patient)

    @staticmethod
    def get_patient_details(db: Session, patient_id: int) -> Patient:
        """
        Fetch patient details by ID
        """
        patient = PatientRepository.get_by_id(db, patient_id)

        if not patient:
            raise ValueError("Patient not found")

        return patient

    @staticmethod
    def list_patients(db: Session) -> list[Patient]:
        """
        List all patients
        """
        return PatientRepository.list_all(db)

    @staticmethod
    def search_patients(
        db: Session,
        name: str | None = None,
        contact: str | None = None
    ) -> list[Patient]:
        """
        Search patients by name or contact details
        """
        if not name and not contact:
            raise ValueError("At least one search parameter must be provided")

        return PatientRepository.search(db, name, contact)

    @staticmethod
    def delete_patient(db: Session, patient_id: int) -> None:
        """
        Delete a patient
        """
        patient = PatientRepository.get_by_id(db, patient_id)

        if not patient:
            raise ValueError("Patient not found")

        PatientRepository.delete(db, patient)
