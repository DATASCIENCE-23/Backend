"""
Lab Schedule Service
Business logic layer for lab schedule operations
"""

from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta

from repositories.lab_schedule_repository import LabScheduleRepository
from repositories.lab_order_repository import LabOrderRepository
from models.lab_schedule import LabSchedule, ScheduleStatus, SampleType
from models.lab_order import OrderStatus
from exceptions import (
    LabScheduleNotFoundException,
    LabOrderNotFoundException,
    ScheduleConflictException,
    InvalidScheduleTimeException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabScheduleService:
    """Service for lab schedule business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = LabScheduleRepository(db)
        self.order_repository = LabOrderRepository(db)
    
    def create_schedule(self, schedule_data: dict) -> LabSchedule:
        """Create a new lab schedule with validation"""
        try:
            # Validate required fields
            required_fields = ['order_id', 'technician_id', 'scheduled_datetime']
            for field in required_fields:
                if field not in schedule_data or not schedule_data[field]:
                    raise LabSchedulingException(f"Missing required field: {field}")
            
            # Validate order exists and is in correct status
            order = self.order_repository.get_by_id(schedule_data['order_id'])
            if order.status != OrderStatus.PENDING:
                raise LabSchedulingException(f"Cannot schedule order with status {order.status.value}")
            
            # Validate scheduling time
            scheduled_datetime = schedule_data['scheduled_datetime']
            if isinstance(scheduled_datetime, str):
                scheduled_datetime = datetime.fromisoformat(scheduled_datetime)
            
            if not self._is_valid_schedule_time(scheduled_datetime):
                raise InvalidScheduleTimeException("Invalid scheduling time")
            
            # Check for conflicts
            if self.repository.check_conflicts(
                schedule_data['technician_id'], 
                scheduled_datetime
            ):
                raise ScheduleConflictException("Technician is not available at the requested time")
            
            # Set default values
            schedule_data.setdefault('status', ScheduleStatus.SCHEDULED)
            schedule_data.setdefault('sample_type', SampleType.BLOOD)
            schedule_data.setdefault('is_home_collection', False)
            schedule_data.setdefault('created_at', datetime.utcnow())
            schedule_data.setdefault('updated_at', datetime.utcnow())
            
            # Create the schedule
            schedule = self.repository.create(schedule_data)
            
            # Update order status to scheduled
            self.order_repository.update_status(schedule_data['order_id'], OrderStatus.SCHEDULED)
            
            return schedule
            
        except (LabOrderNotFoundException, ScheduleConflictException, InvalidScheduleTimeException, LabSchedulingException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to create schedule: {str(e)}")
    
    def get_schedule(self, schedule_id: int) -> LabSchedule:
        """Get lab schedule by ID"""
        return self.repository.get_by_id(schedule_id)
    
    def get_schedule_by_order(self, order_id: int) -> Optional[LabSchedule]:
        """Get schedule for a specific order"""
        return self.repository.get_by_order_id(order_id)
    
    def get_technician_schedule(self, technician_id: int, schedule_date: date = None) -> List[LabSchedule]:
        """Get schedules for a technician"""
        return self.repository.get_by_technician_id(technician_id, schedule_date)
    
    def get_available_slots(self, schedule_date: date, technician_id: int = None) -> List[Dict]:
        """Get available time slots for scheduling"""
        return self.repository.get_available_slots(schedule_date, technician_id)
    
    def get_schedules_by_date_range(self, start_date: date, end_date: date) -> List[LabSchedule]:
        """Get schedules within date range"""
        return self.repository.get_by_date_range(start_date, end_date)
    
    def get_schedules_by_status(self, status: ScheduleStatus) -> List[LabSchedule]:
        """Get schedules by status"""
        return self.repository.get_by_status(status)
    
    def get_home_collections(self, schedule_date: date = None) -> List[LabSchedule]:
        """Get home collection schedules"""
        return self.repository.get_home_collections(schedule_date)
    
    def update_schedule_status(self, schedule_id: int, status: ScheduleStatus, notes: str = None) -> LabSchedule:
        """Update schedule status with business logic validation"""
        try:
            # Get current schedule
            schedule = self.repository.get_by_id(schedule_id)
            
            # Validate status transition
            if not self._is_valid_status_transition(schedule.status, status):
                raise LabSchedulingException(
                    f"Invalid status transition from {schedule.status.value} to {status.value}"
                )
            
            # Update schedule status
            updated_schedule = self.repository.update_status(schedule_id, status)
            
            # Update related order status if needed
            if status == ScheduleStatus.IN_PROGRESS:
                self.order_repository.update_status(schedule.order_id, OrderStatus.IN_PROGRESS)
            elif status == ScheduleStatus.COMPLETED:
                self.order_repository.update_status(schedule.order_id, OrderStatus.COMPLETED)
            elif status == ScheduleStatus.CANCELLED:
                self.order_repository.update_status(schedule.order_id, OrderStatus.PENDING)
            
            # Add notes if provided
            if notes:
                self.repository.update(schedule_id, {'notes': notes})
            
            return updated_schedule
            
        except LabScheduleNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update schedule status: {str(e)}")
    
    def reschedule_appointment(self, schedule_id: int, new_datetime: datetime, new_technician_id: int = None) -> LabSchedule:
        """Reschedule an appointment"""
        try:
            # Get current schedule
            schedule = self.repository.get_by_id(schedule_id)
            
            # Check if schedule can be rescheduled
            if schedule.status not in [ScheduleStatus.SCHEDULED]:
                raise LabSchedulingException(f"Cannot reschedule appointment with status {schedule.status.value}")
            
            # Validate new scheduling time
            if not self._is_valid_schedule_time(new_datetime):
                raise InvalidScheduleTimeException("Invalid rescheduling time")
            
            # Use existing technician if not specified
            technician_id = new_technician_id or schedule.technician_id
            
            # Check for conflicts
            if self.repository.check_conflicts(technician_id, new_datetime):
                raise ScheduleConflictException("Technician is not available at the requested time")
            
            # Update schedule
            update_data = {
                'scheduled_datetime': new_datetime,
                'technician_id': technician_id
            }
            
            return self.repository.update(schedule_id, update_data)
            
        except (LabScheduleNotFoundException, InvalidScheduleTimeException, ScheduleConflictException, LabSchedulingException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to reschedule appointment: {str(e)}")
    
    def cancel_schedule(self, schedule_id: int, reason: str) -> LabSchedule:
        """Cancel a lab schedule"""
        try:
            schedule = self.repository.get_by_id(schedule_id)
            
            # Check if schedule can be cancelled
            if schedule.status in [ScheduleStatus.COMPLETED, ScheduleStatus.CANCELLED]:
                raise LabSchedulingException(f"Cannot cancel schedule with status {schedule.status.value}")
            
            # Update status and add cancellation reason
            update_data = {
                'status': ScheduleStatus.CANCELLED,
                'notes': f"CANCELLED: {reason}. Previous notes: {schedule.notes or ''}"
            }
            
            updated_schedule = self.repository.update(schedule_id, update_data)
            
            # Update order status back to pending
            self.order_repository.update_status(schedule.order_id, OrderStatus.PENDING)
            
            return updated_schedule
            
        except LabScheduleNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to cancel schedule: {str(e)}")
    
    def update_schedule(self, schedule_id: int, update_data: dict) -> LabSchedule:
        """Update lab schedule with validation"""
        try:
            # Validate status transition if status is being updated
            if 'status' in update_data:
                current_schedule = self.repository.get_by_id(schedule_id)
                if not self._is_valid_status_transition(current_schedule.status, update_data['status']):
                    raise LabSchedulingException(
                        f"Invalid status transition from {current_schedule.status.value} to {update_data['status'].value}"
                    )
            
            # Validate scheduling time if being updated
            if 'scheduled_datetime' in update_data:
                if not self._is_valid_schedule_time(update_data['scheduled_datetime']):
                    raise InvalidScheduleTimeException("Invalid scheduling time")
            
            return self.repository.update(schedule_id, update_data)
            
        except LabScheduleNotFoundException:
            raise
        except (InvalidScheduleTimeException, LabSchedulingException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update schedule: {str(e)}")
    
    def delete_schedule(self, schedule_id: int) -> bool:
        """Delete a lab schedule (only if not started)"""
        try:
            schedule = self.repository.get_by_id(schedule_id)
            
            # Check if schedule can be deleted
            if schedule.status not in [ScheduleStatus.SCHEDULED, ScheduleStatus.CANCELLED]:
                raise LabSchedulingException(
                    f"Cannot delete schedule with status {schedule.status.value}. Only scheduled or cancelled schedules can be deleted."
                )
            
            # Update order status back to pending if schedule was active
            if schedule.status == ScheduleStatus.SCHEDULED:
                self.order_repository.update_status(schedule.order_id, OrderStatus.PENDING)
            
            return self.repository.delete(schedule_id)
            
        except LabScheduleNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to delete schedule: {str(e)}")
    
    def get_all_schedules(self, skip: int = 0, limit: int = 100) -> List[LabSchedule]:
        """Get all schedules with pagination"""
        return self.repository.get_all(skip, limit)
    
    def get_todays_schedules(self) -> List[LabSchedule]:
        """Get today's schedules"""
        today = date.today()
        return self.repository.get_by_date_range(today, today)
    
    def _is_valid_schedule_time(self, scheduled_datetime: datetime) -> bool:
        """Validate if scheduling time is valid"""
        # Check if time is in the future
        if scheduled_datetime <= datetime.now():
            return False
        
        # Check if time is within working hours (8 AM to 5 PM)
        if scheduled_datetime.hour < 8 or scheduled_datetime.hour >= 17:
            return False
        
        # Check if it's a weekday (Monday = 0, Sunday = 6)
        if scheduled_datetime.weekday() >= 5:  # Saturday or Sunday
            return False
        
        return True
    
    def _is_valid_status_transition(self, current_status: ScheduleStatus, new_status: ScheduleStatus) -> bool:
        """Validate if status transition is allowed"""
        valid_transitions = {
            ScheduleStatus.SCHEDULED: [ScheduleStatus.IN_PROGRESS, ScheduleStatus.CANCELLED],
            ScheduleStatus.IN_PROGRESS: [ScheduleStatus.COMPLETED, ScheduleStatus.CANCELLED],
            ScheduleStatus.COMPLETED: [],  # Final state
            ScheduleStatus.CANCELLED: []   # Final state
        }
        
        return new_status in valid_transitions.get(current_status, [])