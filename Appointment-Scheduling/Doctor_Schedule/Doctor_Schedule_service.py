from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict
from Doctor_Schedule.Doctor_Schedule_model import DoctorSchedule, DayOfWeekEnum
from Repository.Doctor_Schedule_repository import DoctorScheduleRepository

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
        effective_from = data.get("effective_from")

        # Validate required fields
        if not all([doctor_id, day_of_week, start_time, end_time, slot_duration, effective_from]):
            raise ValueError("Missing required fields: doctor_id, day_of_week, start_time, end_time, slot_duration, effective_from")

        # Convert string values if needed
        if isinstance(day_of_week, str):
            try:
                day_of_week = DayOfWeekEnum[day_of_week.upper()]
            except KeyError:
                raise ValueError(f"Invalid day_of_week: {day_of_week}. Must be one of: {[d.name for d in DayOfWeekEnum]}")
        
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        if isinstance(effective_from, str):
            effective_from = datetime.strptime(effective_from, "%Y-%m-%d").date()
        
        effective_to = data.get("effective_to")
        if effective_to and isinstance(effective_to, str):
            effective_to = datetime.strptime(effective_to, "%Y-%m-%d").date()

        # Validate time logic
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

        # Validate slot duration
        if slot_duration <= 0 or slot_duration > 480:  # Max 8 hours
            raise ValueError("Slot duration must be between 1 and 480 minutes")

        # Calculate total minutes in schedule
        start_datetime = datetime.combine(date.today(), start_time)
        end_datetime = datetime.combine(date.today(), end_time)
        total_minutes = (end_datetime - start_datetime).total_seconds() / 60
        
        if total_minutes < slot_duration:
            raise ValueError("Schedule duration is shorter than slot duration")

        # Validate effective dates
        if effective_to and effective_to < effective_from:
            raise ValueError("effective_to must be after effective_from")

        # Check for time overlaps
        has_overlap = DoctorScheduleRepository.check_time_overlap(
            db, doctor_id, day_of_week, start_time, end_time, effective_from, effective_to
        )
        
        if has_overlap:
            raise ValueError(f"Schedule overlaps with existing schedule for this doctor on {day_of_week.value}")

        # Validate max_patients_per_slot
        max_patients = data.get("max_patients_per_slot", 1)
        if max_patients <= 0 or max_patients > 50:
            raise ValueError("max_patients_per_slot must be between 1 and 50")

        # Create schedule object
        schedule = DoctorSchedule(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            max_patients_per_slot=max_patients,
            effective_from=effective_from,
            effective_to=effective_to,
            is_active=data.get("is_active", True)
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
    def get_doctor_schedules(db: Session, doctor_id: int, active_only: bool = False) -> List[DoctorSchedule]:
        """Get all schedules for a doctor"""
        if active_only:
            return DoctorScheduleRepository.get_active_by_doctor_id(db, doctor_id)
        return DoctorScheduleRepository.get_by_doctor_id(db, doctor_id)

    @staticmethod
    def get_doctor_schedule_by_day(db: Session, doctor_id: int, day_of_week: str) -> List[DoctorSchedule]:
        """Get doctor's schedule for a specific day"""
        try:
            day_enum = DayOfWeekEnum[day_of_week.upper()]
        except KeyError:
            raise ValueError(f"Invalid day_of_week: {day_of_week}")
        
        return DoctorScheduleRepository.get_by_doctor_and_day(db, doctor_id, day_enum)

    @staticmethod
    def get_schedules_by_day(db: Session, day_of_week: str) -> List[DoctorSchedule]:
        """Get all schedules for a specific day"""
        try:
            day_enum = DayOfWeekEnum[day_of_week.upper()]
        except KeyError:
            raise ValueError(f"Invalid day_of_week: {day_of_week}")
        
        return DoctorScheduleRepository.get_by_day_of_week(db, day_enum)

    @staticmethod
    def get_effective_schedule_for_date(db: Session, doctor_id: int, check_date: date) -> List[DoctorSchedule]:
        """
        Get doctor's schedule effective for a specific date
        """
        if isinstance(check_date, str):
            check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
        
        # Get day of week from date
        day_name = check_date.strftime("%A").upper()
        day_enum = DayOfWeekEnum[day_name]
        
        return DoctorScheduleRepository.get_effective_schedule(db, doctor_id, day_enum, check_date)

    @staticmethod
    def update_schedule(db: Session, schedule_id: int, data: dict) -> DoctorSchedule:
        """
        Update an existing schedule with validation
        """
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")

        # If updating critical fields, validate
        if any(key in data for key in ["day_of_week", "start_time", "end_time", "effective_from", "effective_to"]):
            new_day = data.get("day_of_week", schedule.day_of_week)
            new_start = data.get("start_time", schedule.start_time)
            new_end = data.get("end_time", schedule.end_time)
            new_from = data.get("effective_from", schedule.effective_from)
            new_to = data.get("effective_to", schedule.effective_to)

            # Convert strings if needed
            if isinstance(new_day, str):
                try:
                    new_day = DayOfWeekEnum[new_day.upper()]
                except KeyError:
                    raise ValueError(f"Invalid day_of_week: {new_day}")
            
            if isinstance(new_start, str):
                new_start = datetime.strptime(new_start, "%H:%M:%S").time()
            if isinstance(new_end, str):
                new_end = datetime.strptime(new_end, "%H:%M:%S").time()
            if isinstance(new_from, str):
                new_from = datetime.strptime(new_from, "%Y-%m-%d").date()
            if new_to and isinstance(new_to, str):
                new_to = datetime.strptime(new_to, "%Y-%m-%d").date()

            # Validate time logic
            if new_start >= new_end:
                raise ValueError("Start time must be before end time")

            # Validate effective dates
            if new_to and new_to < new_from:
                raise ValueError("effective_to must be after effective_from")

            # Check for overlaps (excluding current schedule)
            has_overlap = DoctorScheduleRepository.check_time_overlap(
                db, schedule.doctor_id, new_day, new_start, new_end, new_from, new_to,
                exclude_schedule_id=schedule_id
            )
            
            if has_overlap:
                raise ValueError(f"Updated schedule overlaps with existing schedule for this doctor on {new_day.value}")

        # Validate slot_duration if being updated
        if "slot_duration" in data:
            slot_duration = data["slot_duration"]
            if slot_duration <= 0 or slot_duration > 480:
                raise ValueError("Slot duration must be between 1 and 480 minutes")

        # Validate max_patients_per_slot if being updated
        if "max_patients_per_slot" in data:
            max_patients = data["max_patients_per_slot"]
            if max_patients <= 0 or max_patients > 50:
                raise ValueError("max_patients_per_slot must be between 1 and 50")

        # Update fields
        for key, value in data.items():
            if key == "day_of_week" and isinstance(value, str):
                value = DayOfWeekEnum[value.upper()]
            
            if hasattr(schedule, key):
                setattr(schedule, key, value)

        return DoctorScheduleRepository.update(db, schedule)

    @staticmethod
    def delete_schedule(db: Session, schedule_id: int, soft_delete: bool = True) -> None:
        """
        Delete a schedule (soft delete by default)
        """
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")

        if soft_delete:
            DoctorScheduleRepository.deactivate(db, schedule)
        else:
            DoctorScheduleRepository.delete(db, schedule)

    @staticmethod
    def activate_schedule(db: Session, schedule_id: int) -> DoctorSchedule:
        """
        Activate a deactivated schedule
        """
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")

        if schedule.is_active:
            raise ValueError("Schedule is already active")

        return DoctorScheduleRepository.activate(db, schedule)

    @staticmethod
    def deactivate_schedule(db: Session, schedule_id: int) -> DoctorSchedule:
        """
        Deactivate an active schedule
        """
        schedule = DoctorScheduleRepository.get_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")

        if not schedule.is_active:
            raise ValueError("Schedule is already inactive")

        return DoctorScheduleRepository.deactivate(db, schedule)

    @staticmethod
    def get_schedules_by_date_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[DoctorSchedule]:
        """
        Get schedules within a date range
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

        return DoctorScheduleRepository.get_schedules_by_date_range(db, doctor_id, start_date, end_date)

    @staticmethod
    def get_available_time_slots(
        db: Session,
        doctor_id: int,
        check_date: date
    ) -> List[Dict]:
        """
        Generate available time slots for a doctor on a specific date based on their schedule
        """
        if isinstance(check_date, str):
            check_date = datetime.strptime(check_date, "%Y-%m-%d").date()

        # Get effective schedules for the date
        schedules = DoctorScheduleService.get_effective_schedule_for_date(db, doctor_id, check_date)
        
        if not schedules:
            return []

        all_slots = []
        
        for schedule in schedules:
            slots = DoctorScheduleService._generate_slots_from_schedule(schedule)
            all_slots.extend(slots)

        return all_slots

    @staticmethod
    def _generate_slots_from_schedule(schedule: DoctorSchedule) -> List[Dict]:
        """
        Helper method to generate time slots from a schedule
        """
        slots = []
        
        current_time = datetime.combine(date.today(), schedule.start_time)
        end_datetime = datetime.combine(date.today(), schedule.end_time)
        slot_delta = timedelta(minutes=schedule.slot_duration)
        
        while current_time + slot_delta <= end_datetime:
            slot_end = current_time + slot_delta
            
            slots.append({
                "start_time": current_time.time().strftime("%H:%M:%S"),
                "end_time": slot_end.time().strftime("%H:%M:%S"),
                "duration_minutes": schedule.slot_duration,
                "max_patients": schedule.max_patients_per_slot,
                "schedule_id": schedule.schedule_id
            })
            
            current_time = slot_end
        
        return slots

    @staticmethod
    def get_doctor_weekly_schedule(db: Session, doctor_id: int) -> Dict[str, List[DoctorSchedule]]:
        """
        Get doctor's schedule organized by day of week
        """
        schedules = DoctorScheduleRepository.get_active_by_doctor_id(db, doctor_id)
        
        weekly_schedule = {
            "MONDAY": [],
            "TUESDAY": [],
            "WEDNESDAY": [],
            "THURSDAY": [],
            "FRIDAY": [],
            "SATURDAY": [],
            "SUNDAY": []
        }
        
        for schedule in schedules:
            day_name = schedule.day_of_week.name
            weekly_schedule[day_name].append(schedule)
        
        return weekly_schedule

    @staticmethod
    def expire_old_schedules(db: Session) -> int:
        """
        Deactivate expired schedules (where effective_to is in the past)
        Returns the count of schedules deactivated
        """
        current_date = date.today()
        expired_schedules = DoctorScheduleRepository.get_expired_schedules(db, current_date)
        
        count = 0
        for schedule in expired_schedules:
            DoctorScheduleRepository.deactivate(db, schedule)
            count += 1
        
        return count

    @staticmethod
    def get_upcoming_schedules(db: Session, doctor_id: int) -> List[DoctorSchedule]:
        """
        Get upcoming schedules for a doctor (effective_from is in the future)
        """
        current_date = date.today()
        return DoctorScheduleRepository.get_upcoming_schedules(db, doctor_id, current_date)

    @staticmethod
    def bulk_create_weekly_schedule(
        db: Session,
        doctor_id: int,
        weekly_schedule: Dict[str, Dict],
        effective_from: date,
        effective_to: Optional[date] = None
    ) -> List[DoctorSchedule]:
        """
        Create schedules for multiple days of the week at once
        weekly_schedule format: {
            "MONDAY": {"start_time": "09:00:00", "end_time": "17:00:00", "slot_duration": 30},
            "TUESDAY": {...},
            ...
        }
        """
        created_schedules = []
        
        for day_name, schedule_data in weekly_schedule.items():
            if schedule_data:  # Only create if data provided
                data = {
                    "doctor_id": doctor_id,
                    "day_of_week": day_name,
                    "start_time": schedule_data.get("start_time"),
                    "end_time": schedule_data.get("end_time"),
                    "slot_duration": schedule_data.get("slot_duration"),
                    "max_patients_per_slot": schedule_data.get("max_patients_per_slot", 1),
                    "effective_from": effective_from,
                    "effective_to": effective_to
                }
                
                schedule = DoctorScheduleService.create_schedule(db, data)
                created_schedules.append(schedule)
        
        return created_schedules
