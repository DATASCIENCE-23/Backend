from sqlalchemy.orm import Session
from datetime import date, time, datetime
from typing import List, Optional, Dict
from Doctor_Schedule.Doctor_Schedule_model import DoctorSchedule, DayOfWeekEnum
from Doctor_Schedule.Doctor_Schedule_repository import DoctorScheduleRepository

class DoctorScheduleService:

    @staticmethod
    def create_schedule(db: Session, data: dict) -> DoctorSchedule:
        """
        Create a new doctor schedule with validation
        """
        # Extract required fields
        doctor_id = data.get("doctor_id")
        day_of_week = data.get("day_of_week")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        slot_duration = data.get("slot_duration")
        max_patients_per_slot = data.get("max_patients_per_slot")
        effective_from = data.get("effective_from")

        # Validate required fields
        if not all([doctor_id, day_of_week, start_time, end_time, slot_duration, max_patients_per_slot, effective_from]):
            raise ValueError("Missing required fields")

        # Convert string dates/times if needed
        if isinstance(effective_from, str):
            effective_from = datetime.strptime(effective_from, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        
        # Convert day_of_week to enum (lowercase)
        if isinstance(day_of_week, str):
            day_of_week = DayOfWeekEnum[day_of_week.lower()]

        # Validate time logic
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        # Handle effective_to
        effective_to = data.get("effective_to")
        if effective_to and isinstance(effective_to, str):
            effective_to = datetime.strptime(effective_to, "%Y-%m-%d").date()

        # Check for time overlap
        has_overlap = DoctorScheduleRepository.check_time_overlap(
            db, doctor_id, day_of_week, start_time, end_time, effective_from, effective_to
        )
        
        if has_overlap:
            raise ValueError("Schedule overlaps with existing schedule for this doctor")

        # Create schedule object
        schedule = DoctorSchedule(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            max_patients_per_slot=max_patients_per_slot,
            is_active=True,
            effective_from=effective_from,
            effective_to=effective_to
        )

        return DoctorScheduleRepository.create(db, schedule)

    @staticmethod
    def get_schedule(db: Session, schedule_id: int) -> DoctorSchedule:
        """Get schedule by ID"""
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")
        return schedule

    @staticmethod
    def list_schedules(db: Session, skip: int = 0, limit: int = 100) -> List[DoctorSchedule]:
        """List all schedules with pagination"""
        return DoctorScheduleRepository.get_all(db, skip, limit)

    @staticmethod
    def get_doctor_schedules(db: Session, doctor_id: int) -> List[DoctorSchedule]:
        """Get all schedules for a doctor"""
        return DoctorScheduleRepository.get_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_active_doctor_schedules(db: Session, doctor_id: int) -> List[DoctorSchedule]:
        """Get active schedules for a doctor"""
        return DoctorScheduleRepository.get_active_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_schedules_by_day(db: Session, doctor_id: int, day_of_week: str) -> List[DoctorSchedule]:
        """Get schedules for a doctor on a specific day"""
        day_enum = DayOfWeekEnum[day_of_week.lower()]
        return DoctorScheduleRepository.get_by_doctor_and_day(db, doctor_id, day_enum)

    @staticmethod
    def update_schedule(db: Session, schedule_id: int, data: dict) -> DoctorSchedule:
        """
        Update an existing schedule with validation
        """
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")

        # If updating time or day, check for overlaps
        if any(key in data for key in ["day_of_week", "start_time", "end_time", "effective_from", "effective_to"]):
            new_day = data.get("day_of_week", schedule.day_of_week)
            new_start = data.get("start_time", schedule.start_time)
            new_end = data.get("end_time", schedule.end_time)
            new_effective_from = data.get("effective_from", schedule.effective_from)
            new_effective_to = data.get("effective_to", schedule.effective_to)

            # Convert if needed
            if isinstance(new_day, str):
                new_day = DayOfWeekEnum[new_day.lower()]
            if isinstance(new_start, str):
                new_start = datetime.strptime(new_start, "%H:%M:%S").time()
            if isinstance(new_end, str):
                new_end = datetime.strptime(new_end, "%H:%M:%S").time()
            if isinstance(new_effective_from, str):
                new_effective_from = datetime.strptime(new_effective_from, "%Y-%m-%d").date()
            if new_effective_to and isinstance(new_effective_to, str):
                new_effective_to = datetime.strptime(new_effective_to, "%Y-%m-%d").date()

            # Validate time logic
            if new_start >= new_end:
                raise ValueError("Start time must be before end time")

            # Check for overlaps
            has_overlap = DoctorScheduleRepository.check_time_overlap(
                db, schedule.doctor_id, new_day, new_start, new_end,
                new_effective_from, new_effective_to, exclude_schedule_id=schedule_id
            )
            
            if has_overlap:
                raise ValueError("Updated schedule overlaps with existing schedule")

        # Update fields
        for key, value in data.items():
            if key == "day_of_week" and isinstance(value, str):
                value = DayOfWeekEnum[value.lower()]
            if hasattr(schedule, key):
                setattr(schedule, key, value)

        return DoctorScheduleRepository.update(db, schedule)

    @staticmethod
    def deactivate_schedule(db: Session, schedule_id: int) -> DoctorSchedule:
        """Deactivate a schedule"""
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")
        
        return DoctorScheduleRepository.deactivate(db, schedule)

    @staticmethod
    def delete_schedule(db: Session, schedule_id: int) -> None:
        """Delete a schedule (hard delete)"""
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")
        
        DoctorScheduleRepository.delete(db, schedule)

    @staticmethod
    def get_doctor_schedule_summary(db: Session, doctor_id: int) -> Dict:
        """Get summary of doctor's schedules"""
        schedules = DoctorScheduleRepository.get_active_by_doctor_id(db, doctor_id)
        
        return {
            "doctor_id": doctor_id,
            "total_schedules": len(schedules),
            "schedules_by_day": {
                "mon": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.mon]),
                "tue": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.tue]),
                "wed": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.wed]),
                "thu": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.thu]),
                "fri": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.fri]),
                "sat": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.sat]),
                "sun": len([s for s in schedules if s.day_of_week == DayOfWeekEnum.sun]),
            },
            "schedules": schedules
        }