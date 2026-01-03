from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, time, datetime
from typing import List, Optional
from Appointment.Appointment_model import Appointment, AppointmentStatusEnum

class AppointmentRepository:

    @staticmethod
    def get_by_id(db: Session, appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID"""
        return db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get all appointments with pagination"""
        return db.query(Appointment).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int) -> List[Appointment]:
        """Get all appointments for a specific patient"""
        return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

    @staticmethod
    def get_by_doctor_id(db: Session, doctor_id: int) -> List[Appointment]:
        """Get all appointments for a specific doctor"""
        return db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    @staticmethod
    def get_by_date(db: Session, appointment_date: date) -> List[Appointment]:
        """Get all appointments on a specific date"""
        return db.query(Appointment).filter(Appointment.appointment_date == appointment_date).all()

    @staticmethod
    def get_by_doctor_and_date(db: Session, doctor_id: int, appointment_date: date) -> List[Appointment]:
        """Get all appointments for a doctor on a specific date"""
        return db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date
            )
        ).all()

    @staticmethod
    def get_by_status(db: Session, status: AppointmentStatusEnum) -> List[Appointment]:
        """Get all appointments with a specific status"""
        return db.query(Appointment).filter(Appointment.status == status).all()

    @staticmethod
    def check_time_slot_availability(
        db: Session, 
        doctor_id: int, 
        appointment_date: date, 
        start_time: time, 
        end_time: time,
        exclude_appointment_id: Optional[int] = None
    ) -> bool:
        """Check if a time slot is available for a doctor on a specific date"""
        query = db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.status.in_([
                    AppointmentStatusEnum.SCHEDULED,
                    AppointmentStatusEnum.CONFIRMED
                ]),
                or_(
                    and_(
                        Appointment.start_time <= start_time,
                        Appointment.end_time > start_time
                    ),
                    and_(
                        Appointment.start_time < end_time,
                        Appointment.end_time >= end_time
                    ),
                    and_(
                        Appointment.start_time >= start_time,
                        Appointment.end_time <= end_time
                    )
                )
            )
        )
        
        # Exclude current appointment when checking for updates
        if exclude_appointment_id:
            query = query.filter(Appointment.appointment_id != exclude_appointment_id)
        
        conflicting_appointments = query.all()
        return len(conflicting_appointments) == 0

    @staticmethod
    def get_upcoming_appointments(db: Session, patient_id: int) -> List[Appointment]:
        """Get upcoming appointments for a patient"""
        today = date.today()
        return db.query(Appointment).filter(
            and_(
                Appointment.patient_id == patient_id,
                Appointment.appointment_date >= today,
                Appointment.status.in_([
                    AppointmentStatusEnum.SCHEDULED,
                    AppointmentStatusEnum.CONFIRMED
                ])
            )
        ).order_by(Appointment.appointment_date, Appointment.start_time).all()

    @staticmethod
    def get_past_appointments(db: Session, patient_id: int) -> List[Appointment]:
        """Get past appointments for a patient"""
        today = date.today()
        return db.query(Appointment).filter(
            and_(
                Appointment.patient_id == patient_id,
                or_(
                    Appointment.appointment_date < today,
                    Appointment.status.in_([
                        AppointmentStatusEnum.COMPLETED,
                        AppointmentStatusEnum.CANCELLED,
                        AppointmentStatusEnum.NO_SHOW
                    ])
                )
            )
        ).order_by(Appointment.appointment_date.desc(), Appointment.start_time.desc()).all()

    @staticmethod
    def create(db: Session, appointment: Appointment) -> Appointment:
        """Create a new appointment"""
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def update(db: Session, appointment: Appointment) -> Appointment:
        """Update an existing appointment"""
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def delete(db: Session, appointment: Appointment) -> None:
        """Delete an appointment"""
        db.delete(appointment)
        db.commit()

    @staticmethod
    def get_today_appointments_by_doctor(db: Session, doctor_id: int) -> List[Appointment]:
        """Get today's appointments for a doctor"""
        today = date.today()
        return db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == today,
                Appointment.status.in_([
                    AppointmentStatusEnum.SCHEDULED,
                    AppointmentStatusEnum.CONFIRMED
                ])
            )
        ).order_by(Appointment.start_time).all()

    @staticmethod
    def count_by_doctor_and_date(db: Session, doctor_id: int, appointment_date: date) -> int:
        """Count appointments for a doctor on a specific date"""
        return db.query(Appointment).filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date,
                Appointment.status.in_([
                    AppointmentStatusEnum.SCHEDULED,
                    AppointmentStatusEnum.CONFIRMED
                ])
            )
        ).count()
