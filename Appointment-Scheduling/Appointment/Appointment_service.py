from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict
from Appointment.Appointment_model import Appointment, AppointmentStatusEnum, AppointmentTypeEnum
from Appointment.Appointment_repository import AppointmentRepository

class AppointmentService:

    @staticmethod
    def create_appointment(db: Session, data: dict) -> Appointment:
        """
        Create a new appointment with validation
        """
        # Extract required fields
        doctor_id = data.get("doctor_id")
        patient_id = data.get("patient_id")
        appointment_date = data.get("appointment_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        # Validate required fields
        if not all([doctor_id, patient_id, appointment_date, start_time, end_time]):
            raise ValueError("Missing required fields: doctor_id, patient_id, appointment_date, start_time, end_time")

        # Convert string dates/times if needed
        if isinstance(appointment_date, str):
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        # Validate appointment date (should not be in the past)
        if appointment_date < date.today():
            raise ValueError("Appointment date cannot be in the past")

        # Validate time logic
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        # Check if the time slot is available
        is_available = AppointmentRepository.check_time_slot_availability(
            db, doctor_id, appointment_date, start_time, end_time
        )
        
        if not is_available:
            raise ValueError("Time slot is not available. Please choose a different time.")

        # Get appointment type - convert to match database enum
        appt_type_str = data.get("appointment_type", "opd").lower()
        # Map common names to database enum values
        type_mapping = {
            "consultation": "opd",
            "followup": "follow_up",
            "follow-up": "follow_up",
            "emergency": "emergency",
            "opd": "opd"
        }
        db_type = type_mapping.get(appt_type_str, "opd")
        appointment_type = AppointmentTypeEnum[db_type]

        # Create appointment object
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            start_time=start_time,
            end_time=end_time,
            appointment_type=appointment_type,
            status=AppointmentStatusEnum.scheduled,
            reason_for_visit=data.get("reason_for_visit"),
            symptoms=data.get("symptoms"),
            notes=data.get("notes"),
            consultation_fee=data.get("consultation_fee"),
            booking_date=datetime.now()
        )

        return AppointmentRepository.create(db, appointment)

    @staticmethod
    def get_appointment(db: Session, appointment_id: int) -> Appointment:
        """Get appointment by ID"""
        appointment = AppointmentRepository.get_by_id(db, appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")
        return appointment

    @staticmethod
    def list_appointments(db: Session, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """List all appointments with pagination"""
        return AppointmentRepository.get_all(db, skip, limit)

    @staticmethod
    def get_patient_appointments(db: Session, patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient"""
        return AppointmentRepository.get_by_patient_id(db, patient_id)

    @staticmethod
    def get_doctor_appointments(db: Session, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a doctor"""
        return AppointmentRepository.get_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_appointments_by_date(db: Session, appointment_date: date) -> List[Appointment]:
        """Get all appointments on a specific date"""
        return AppointmentRepository.get_by_date(db, appointment_date)

    @staticmethod
    def get_doctor_appointments_by_date(db: Session, doctor_id: int, appointment_date: date) -> List[Appointment]:
        """Get doctor's appointments on a specific date"""
        return AppointmentRepository.get_by_doctor_and_date(db, doctor_id, appointment_date)

    @staticmethod
    def update_appointment(db: Session, appointment_id: int, data: dict) -> Appointment:
        """
        Update an existing appointment with validation
        """
        appointment = AppointmentRepository.get_by_id(db, appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")

        # If updating date or time, check availability
        if any(key in data for key in ["appointment_date", "start_time", "end_time", "doctor_id"]):
            new_doctor_id = data.get("doctor_id", appointment.doctor_id)
            new_date = data.get("appointment_date", appointment.appointment_date)
            new_start_time = data.get("start_time", appointment.start_time)
            new_end_time = data.get("end_time", appointment.end_time)

            # Convert strings if needed
            if isinstance(new_date, str):
                new_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if isinstance(new_start_time, str):
                new_start_time = datetime.strptime(new_start_time, "%H:%M:%S").time()
            if isinstance(new_end_time, str):
                new_end_time = datetime.strptime(new_end_time, "%H:%M:%S").time()

            # Validate time logic
            if new_start_time >= new_end_time:
                raise ValueError("Start time must be before end time")

            # Check availability (excluding current appointment)
            is_available = AppointmentRepository.check_time_slot_availability(
                db, new_doctor_id, new_date, new_start_time, new_end_time, 
                exclude_appointment_id=appointment_id
            )
            
            if not is_available:
                raise ValueError("Time slot is not available. Please choose a different time.")

        # Update fields
        for key, value in data.items():
            if key == "appointment_type" and isinstance(value, str):
                # Map type name to database enum
                type_mapping = {
                    "consultation": "opd",
                    "followup": "follow_up",
                    "follow-up": "follow_up",
                    "emergency": "emergency",
                    "opd": "opd"
                }
                db_type = type_mapping.get(value.lower(), "opd")
                value = AppointmentTypeEnum[db_type]
            elif key == "status" and isinstance(value, str):
                # Map status to database enum
                value = AppointmentStatusEnum[value.lower()]
            
            if hasattr(appointment, key):
                setattr(appointment, key, value)

        return AppointmentRepository.update(db, appointment)

    @staticmethod
    def cancel_appointment(db: Session, appointment_id: int, cancelled_by: int, reason: str) -> Appointment:
        """
        Cancel an appointment
        """
        appointment = AppointmentRepository.get_by_id(db, appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")

        if appointment.status in [AppointmentStatusEnum.cancelled, AppointmentStatusEnum.completed]:
            raise ValueError(f"Cannot cancel appointment with status: {appointment.status.value}")

        appointment.status = AppointmentStatusEnum.cancelled
        
        # Note: cancellation_reason, cancelled_at, cancelled_by fields don't exist in DB schema
        # If you need them, add them to database first

        return AppointmentRepository.update(db, appointment)

    @staticmethod
    def complete_appointment(db: Session, appointment_id: int) -> Appointment:
        """
        Mark an appointment as completed
        """
        appointment = AppointmentRepository.get_by_id(db, appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")

        if appointment.status != AppointmentStatusEnum.scheduled:
            raise ValueError(f"Can only complete scheduled appointments. Current status: {appointment.status.value}")

        appointment.status = AppointmentStatusEnum.completed

        return AppointmentRepository.update(db, appointment)

    @staticmethod
    def mark_no_show(db: Session, appointment_id: int) -> Appointment:
        """
        Mark an appointment as no-show
        """
        appointment = AppointmentRepository.get_by_id(db, appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")

        appointment.status = AppointmentStatusEnum.no_show

        return AppointmentRepository.update(db, appointment)

    @staticmethod
    def delete_appointment(db: Session, appointment_id: int) -> None:
        """
        Delete an appointment (hard delete)
        """
        appointment = AppointmentRepository.get_by_id(db, appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID {appointment_id} not found")

        AppointmentRepository.delete(db, appointment)

    @staticmethod
    def get_upcoming_appointments_for_patient(db: Session, patient_id: int) -> List[Appointment]:
        """Get upcoming appointments for a patient"""
        return AppointmentRepository.get_upcoming_appointments(db, patient_id)

    @staticmethod
    def get_past_appointments_for_patient(db: Session, patient_id: int) -> List[Appointment]:
        """Get past appointments for a patient"""
        return AppointmentRepository.get_past_appointments(db, patient_id)

    @staticmethod
    def get_today_appointments_for_doctor(db: Session, doctor_id: int) -> List[Appointment]:
        """Get today's appointments for a doctor"""
        return AppointmentRepository.get_today_appointments_by_doctor(db, doctor_id)

    @staticmethod
    def check_availability(
        db: Session, 
        doctor_id: int, 
        appointment_date: date, 
        start_time: time, 
        end_time: time
    ) -> Dict[str, bool]:
        """
        Check if a time slot is available
        """
        is_available = AppointmentRepository.check_time_slot_availability(
            db, doctor_id, appointment_date, start_time, end_time
        )
        
        return {
            "available": is_available,
            "doctor_id": doctor_id,
            "date": str(appointment_date),
            "start_time": str(start_time),
            "end_time": str(end_time)
        }

    # Note: confirm_appointment and reschedule_appointment removed 
    # because database doesn't have 'confirmed' or 'rescheduled' enum values