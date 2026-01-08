"""
Lab Schedule Routes
API endpoints for lab schedule operations
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from controllers.lab_schedule_controller import LabScheduleController
from schemas.lab_schedule import (
    LabScheduleCreate,
    LabScheduleUpdate,
    LabScheduleResponse,
    LabScheduleStatusUpdate,
    AvailableSlotResponse
)
from models.lab_schedule import ScheduleStatus

router = APIRouter(prefix="/lab-schedule", tags=["Lab Scheduling"])

@router.post(
    "/",
    response_model=LabScheduleResponse,
    status_code=201,
    summary="Create Lab Schedule",
    description="Create a new lab appointment schedule for a patient with an assigned technician",
    response_description="Created lab schedule with appointment details"
)
def create_schedule(
    schedule_data: LabScheduleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new lab schedule appointment.
    
    This endpoint allows scheduling lab appointments by:
    - Linking to an existing lab order
    - Assigning a technician
    - Setting appointment date and time
    - Specifying collection type (in-lab or home collection)
    - Adding special instructions or notes
    
    **Business Rules:**
    - Order must be in PENDING status
    - Appointment time must be in the future
    - Technician must be available at the requested time
    - Working hours: 8 AM to 5 PM, Monday to Friday
    """
    return LabScheduleController.create_schedule(schedule_data, db)

@router.get(
    "/{schedule_id}",
    response_model=LabScheduleResponse,
    summary="Get Lab Schedule",
    description="Retrieve a specific lab schedule by ID",
    response_description="Lab schedule details"
)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific lab schedule.
    
    Returns complete schedule information including:
    - Appointment date and time
    - Assigned technician details
    - Patient and order information
    - Collection type and location
    - Current status and notes
    """
    return LabScheduleController.get_schedule(schedule_id, db)

@router.get(
    "/available-slots/{schedule_date}",
    response_model=List[AvailableSlotResponse],
    summary="Get Available Time Slots",
    description="Get available appointment slots for a specific date",
    response_description="List of available time slots"
)
def get_available_slots(
    schedule_date: date,
    technician_id: int = Query(None, description="Filter by specific technician"),
    db: Session = Depends(get_db)
):
    """
    Get available appointment time slots for scheduling.
    
    This endpoint helps with appointment booking by showing:
    - Available 30-minute time slots
    - Working hours: 8:00 AM to 5:00 PM
    - Excludes weekends and holidays
    - Filters out already booked appointments
    
    **Parameters:**
    - `schedule_date`: Date to check availability
    - `technician_id`: Optional filter for specific technician
    """
    return LabScheduleController.get_available_slots(schedule_date, technician_id, db)

@router.get(
    "/technician/{technician_id}",
    response_model=List[LabScheduleResponse],
    summary="Get Technician Schedule",
    description="Get all scheduled appointments for a specific technician",
    response_description="List of technician's scheduled appointments"
)
def get_technician_schedule(
    technician_id: int,
    schedule_date: date = Query(None, description="Filter by specific date"),
    db: Session = Depends(get_db)
):
    """
    Get all scheduled appointments for a technician.
    
    Useful for:
    - Technician daily schedule management
    - Workload distribution analysis
    - Appointment coordination
    
    **Parameters:**
    - `technician_id`: ID of the technician
    - `schedule_date`: Optional date filter (returns all dates if not specified)
    """
    return LabScheduleController.get_technician_schedule(technician_id, schedule_date, db)

@router.put(
    "/{schedule_id}/status",
    response_model=LabScheduleResponse,
    summary="Update Schedule Status",
    description="Update the status of a lab schedule appointment",
    response_description="Updated lab schedule"
)
def update_schedule_status(
    schedule_id: int,
    status_update: LabScheduleStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of a lab schedule appointment.
    
    **Valid Status Transitions:**
    - SCHEDULED → IN_PROGRESS (when technician starts collection)
    - SCHEDULED → CANCELLED (if appointment is cancelled)
    - IN_PROGRESS → COMPLETED (when sample collection is finished)
    - IN_PROGRESS → CANCELLED (if collection cannot be completed)
    
    **Status Effects:**
    - IN_PROGRESS: Updates related lab order status
    - COMPLETED: Marks order as ready for result entry
    - CANCELLED: Returns order to PENDING status for rescheduling
    """
    return LabScheduleController.update_schedule_status(schedule_id, status_update, db)

@router.get(
    "/home-collections/",
    response_model=List[LabScheduleResponse],
    summary="Get Home Collection Schedules",
    description="Get all home collection appointments",
    response_description="List of home collection schedules"
)
def get_home_collections(
    schedule_date: date = Query(None, description="Filter by specific date"),
    db: Session = Depends(get_db)
):
    """
    Get all home collection appointments.
    
    This endpoint is useful for:
    - Home collection route planning
    - Technician assignment for home visits
    - Patient communication and coordination
    
    **Parameters:**
    - `schedule_date`: Optional date filter for specific day's collections
    """
    return LabScheduleController.get_home_collections(schedule_date, db)