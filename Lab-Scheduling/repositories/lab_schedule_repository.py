"""
Lab Schedule Repository
Data access layer for lab schedule operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, date, time

from models.lab_schedule import LabSchedule, ScheduleStatus, SampleType
from exceptions import LabScheduleNotFoundException, DatabaseConnectionException


class LabScheduleRepository:
    """Repository for lab schedule data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, schedule_data: dict) -> LabSchedule:
        """Create a new lab schedule"""
        try:
            schedule = LabSchedule(**schedule_data)
            self.db.add(schedule)
            self.db.commit()
            self.db.refresh(schedule)
            return schedule
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to create lab schedule: {str(e)}")
    
    def get_by_id(self, schedule_id: int) -> LabSchedule:
        """Get lab schedule by ID"""
        try:
            schedule = self.db.query(LabSchedule).filter(LabSchedule.id == schedule_id).first()
            if not schedule:
                raise LabScheduleNotFoundException(f"Lab schedule with ID {schedule_id} not found")
            return schedule
        except LabScheduleNotFoundException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab schedule: {str(e)}")
    
    def get_by_order_id(self, order_id: int) -> Optional[LabSchedule]:
        """Get lab schedule by order ID"""
        try:
            return self.db.query(LabSchedule).filter(LabSchedule.order_id == order_id).first()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab schedule by order: {str(e)}")
    
    def get_by_technician_id(self, technician_id: int, schedule_date: date = None) -> List[LabSchedule]:
        """Get lab schedules for a technician"""
        try:
            query = self.db.query(LabSchedule).filter(LabSchedule.technician_id == technician_id)
            if schedule_date:
                query = query.filter(func.date(LabSchedule.scheduled_datetime) == schedule_date)
            return query.order_by(LabSchedule.scheduled_datetime).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve technician schedules: {str(e)}")
    
    def get_available_slots(self, schedule_date: date, technician_id: int = None) -> List[dict]:
        """Get available time slots for scheduling"""
        try:
            # Get existing appointments for the date
            query = self.db.query(LabSchedule).filter(
                func.date(LabSchedule.scheduled_datetime) == schedule_date,
                LabSchedule.status.in_([ScheduleStatus.SCHEDULED, ScheduleStatus.IN_PROGRESS])
            )
            
            if technician_id:
                query = query.filter(LabSchedule.technician_id == technician_id)
            
            existing_appointments = query.all()
            
            # Generate available slots (simplified logic)
            # In a real implementation, this would consider technician working hours,
            # break times, and other constraints
            available_slots = []
            start_hour = 8  # 8 AM
            end_hour = 17   # 5 PM
            
            for hour in range(start_hour, end_hour):
                for minute in [0, 30]:  # 30-minute slots
                    slot_time = time(hour, minute)
                    slot_datetime = datetime.combine(schedule_date, slot_time)
                    
                    # Check if slot is available
                    is_available = not any(
                        abs((apt.scheduled_datetime - slot_datetime).total_seconds()) < 1800  # 30 minutes
                        for apt in existing_appointments
                    )
                    
                    if is_available:
                        available_slots.append({
                            "datetime": slot_datetime,
                            "time": slot_time.strftime("%H:%M"),
                            "available": True
                        })
            
            return available_slots
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to get available slots: {str(e)}")
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[LabSchedule]:
        """Get lab schedules within date range"""
        try:
            return self.db.query(LabSchedule).filter(
                and_(
                    func.date(LabSchedule.scheduled_datetime) >= start_date,
                    func.date(LabSchedule.scheduled_datetime) <= end_date
                )
            ).order_by(LabSchedule.scheduled_datetime).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve schedules by date range: {str(e)}")
    
    def get_by_status(self, status: ScheduleStatus) -> List[LabSchedule]:
        """Get lab schedules by status"""
        try:
            return self.db.query(LabSchedule).filter(LabSchedule.status == status).order_by(LabSchedule.scheduled_datetime).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve schedules by status: {str(e)}")
    
    def get_home_collections(self, schedule_date: date = None) -> List[LabSchedule]:
        """Get home collection schedules"""
        try:
            query = self.db.query(LabSchedule).filter(LabSchedule.is_home_collection == True)
            if schedule_date:
                query = query.filter(func.date(LabSchedule.scheduled_datetime) == schedule_date)
            return query.order_by(LabSchedule.scheduled_datetime).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve home collections: {str(e)}")
    
    def update_status(self, schedule_id: int, status: ScheduleStatus) -> LabSchedule:
        """Update schedule status"""
        try:
            schedule = self.get_by_id(schedule_id)
            schedule.status = status
            schedule.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(schedule)
            return schedule
        except LabScheduleNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update schedule status: {str(e)}")
    
    def update(self, schedule_id: int, update_data: dict) -> LabSchedule:
        """Update lab schedule"""
        try:
            schedule = self.get_by_id(schedule_id)
            for key, value in update_data.items():
                if hasattr(schedule, key):
                    setattr(schedule, key, value)
            schedule.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(schedule)
            return schedule
        except LabScheduleNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update schedule: {str(e)}")
    
    def delete(self, schedule_id: int) -> bool:
        """Delete lab schedule"""
        try:
            schedule = self.get_by_id(schedule_id)
            self.db.delete(schedule)
            self.db.commit()
            return True
        except LabScheduleNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to delete schedule: {str(e)}")
    
    def check_conflicts(self, technician_id: int, scheduled_datetime: datetime, duration_minutes: int = 30) -> bool:
        """Check for scheduling conflicts"""
        try:
            start_time = scheduled_datetime
            end_time = datetime.combine(
                scheduled_datetime.date(),
                (datetime.combine(date.today(), scheduled_datetime.time()) + 
                 datetime.timedelta(minutes=duration_minutes)).time()
            )
            
            conflicts = self.db.query(LabSchedule).filter(
                and_(
                    LabSchedule.technician_id == technician_id,
                    LabSchedule.scheduled_datetime >= start_time,
                    LabSchedule.scheduled_datetime < end_time,
                    LabSchedule.status.in_([ScheduleStatus.SCHEDULED, ScheduleStatus.IN_PROGRESS])
                )
            ).count()
            
            return conflicts > 0
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to check conflicts: {str(e)}")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        """Get all lab schedules with pagination"""
        try:
            return self.db.query(LabSchedule).order_by(LabSchedule.scheduled_datetime).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve schedules: {str(e)}")