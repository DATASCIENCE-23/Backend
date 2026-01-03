from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, time
from typing import List, Optional
from Doctor_Schedule.Doctor_Schedule_model import DoctorSchedule, DayOfWeekEnum

class DoctorScheduleRepository:

    @staticmethod
    def get_by_id(db: Session, schedule_id: int) -> Optional[DoctorSchedule]:
        """Get doctor schedule by ID"""
        return db.query(DoctorSchedule).filter(DoctorSchedule.schedule_id == schedule_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[DoctorSchedule]:
        """Get all doctor schedules with pagination"""
        return db.query(DoctorSchedule).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_doctor_id(db: Session, doctor_id: int) -> List[DoctorSchedule]:
        """Get all schedules for a specific doctor"""
        return db.query(DoctorSchedule).filter(DoctorSchedule.doctor_id == doctor_id).all()

    @staticmethod
    def get_active_by_doctor_id(db: Session, doctor_id: int) -> List[DoctorSchedule]:
        """Get all active schedules for a specific doctor"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.is_active == True
            )
        ).all()

    @staticmethod
    def get_by_doctor_and_day(db: Session, doctor_id: int, day_of_week: DayOfWeekEnum) -> List[DoctorSchedule]:
        """Get schedules for a doctor on a specific day of week"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.day_of_week == day_of_week,
                DoctorSchedule.is_active == True
            )
        ).all()

    @staticmethod
    def get_by_day_of_week(db: Session, day_of_week: DayOfWeekEnum) -> List[DoctorSchedule]:
        """Get all schedules for a specific day of week"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.day_of_week == day_of_week,
                DoctorSchedule.is_active == True
            )
        ).all()

    @staticmethod
    def get_effective_schedule(
        db: Session, 
        doctor_id: int, 
        day_of_week: DayOfWeekEnum, 
        check_date: date
    ) -> List[DoctorSchedule]:
        """
        Get effective schedules for a doctor on a specific day considering effective dates
        """
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.day_of_week == day_of_week,
                DoctorSchedule.is_active == True,
                DoctorSchedule.effective_from <= check_date,
                or_(
                    DoctorSchedule.effective_to == None,
                    DoctorSchedule.effective_to >= check_date
                )
            )
        ).all()

    @staticmethod
    def check_time_overlap(
        db: Session,
        doctor_id: int,
        day_of_week: DayOfWeekEnum,
        start_time: time,
        end_time: time,
        effective_from: date,
        effective_to: Optional[date] = None,
        exclude_schedule_id: Optional[int] = None
    ) -> bool:
        """
        Check if there's a time overlap for a doctor's schedule on a specific day
        Returns True if there's overlap, False if no overlap
        """
        query = db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.day_of_week == day_of_week,
                DoctorSchedule.is_active == True,
                # Time overlap check
                or_(
                    and_(
                        DoctorSchedule.start_time <= start_time,
                        DoctorSchedule.end_time > start_time
                    ),
                    and_(
                        DoctorSchedule.start_time < end_time,
                        DoctorSchedule.end_time >= end_time
                    ),
                    and_(
                        DoctorSchedule.start_time >= start_time,
                        DoctorSchedule.end_time <= end_time
                    )
                ),
                # Date range overlap check
                or_(
                    and_(
                        DoctorSchedule.effective_from <= effective_from,
                        or_(
                            DoctorSchedule.effective_to == None,
                            DoctorSchedule.effective_to >= effective_from
                        )
                    ),
                    and_(
                        DoctorSchedule.effective_from <= (effective_to if effective_to else date.max),
                        DoctorSchedule.effective_from >= effective_from
                    )
                )
            )
        )
        
        # Exclude current schedule when checking for updates
        if exclude_schedule_id:
            query = query.filter(DoctorSchedule.schedule_id != exclude_schedule_id)
        
        overlapping_schedules = query.all()
        return len(overlapping_schedules) > 0

    @staticmethod
    def get_schedules_by_date_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[DoctorSchedule]:
        """Get schedules within a date range"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.is_active == True,
                DoctorSchedule.effective_from <= end_date,
                or_(
                    DoctorSchedule.effective_to == None,
                    DoctorSchedule.effective_to >= start_date
                )
            )
        ).all()

    @staticmethod
    def get_expired_schedules(db: Session, current_date: date) -> List[DoctorSchedule]:
        """Get all expired schedules"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.is_active == True,
                DoctorSchedule.effective_to != None,
                DoctorSchedule.effective_to < current_date
            )
        ).all()

    @staticmethod
    def get_upcoming_schedules(db: Session, doctor_id: int, current_date: date) -> List[DoctorSchedule]:
        """Get upcoming schedules for a doctor"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.is_active == True,
                DoctorSchedule.effective_from > current_date
            )
        ).order_by(DoctorSchedule.effective_from).all()

    @staticmethod
    def create(db: Session, schedule: DoctorSchedule) -> DoctorSchedule:
        """Create a new doctor schedule"""
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def update(db: Session, schedule: DoctorSchedule) -> DoctorSchedule:
        """Update an existing doctor schedule"""
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def delete(db: Session, schedule: DoctorSchedule) -> None:
        """Delete a doctor schedule (hard delete)"""
        db.delete(schedule)
        db.commit()

    @staticmethod
    def deactivate(db: Session, schedule: DoctorSchedule) -> DoctorSchedule:
        """Soft delete by deactivating the schedule"""
        schedule.is_active = False
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def activate(db: Session, schedule: DoctorSchedule) -> DoctorSchedule:
        """Activate a deactivated schedule"""
        schedule.is_active = True
        db.commit()
        db.refresh(schedule)
        return schedule

    @staticmethod
    def count_active_schedules_by_doctor(db: Session, doctor_id: int) -> int:
        """Count active schedules for a doctor"""
        return db.query(DoctorSchedule).filter(
            and_(
                DoctorSchedule.doctor_id == doctor_id,
                DoctorSchedule.is_active == True
            )
        ).count()

    @staticmethod
    def get_all_active_schedules(db: Session) -> List[DoctorSchedule]:
        """Get all active schedules across all doctors"""
        return db.query(DoctorSchedule).filter(
            DoctorSchedule.is_active == True
        ).all()
