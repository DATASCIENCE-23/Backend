"""
Lab Schedule Controller
HTTP request handling for lab schedule operations
"""

from typing import List
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from services.lab_schedule_service import LabScheduleService
from schemas.lab_schedule import (
    LabScheduleCreate,
    LabScheduleUpdate,
    LabScheduleResponse,
    LabScheduleStatusUpdate,
    AvailableSlotResponse
)
from models.lab_schedule import ScheduleStatus
from exceptions import (
    LabScheduleNotFoundException,
    ScheduleConflictException,
    InvalidScheduleTimeException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabScheduleController:
    """Controller for lab schedule HTTP operations"""
    
    @staticmethod
    def create_schedule(
        schedule_data: LabScheduleCreate,
        db: Session = Depends(get_db)
    ) -> LabScheduleResponse:
        """Create a new lab schedule"""
        try:
            service = LabScheduleService(db)
            schedule = service.create_schedule(schedule_data.dict())
            return LabScheduleResponse.from_orm(schedule)
        except (ScheduleConflictException, InvalidScheduleTimeException, LabSchedulingException) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create schedule: {str(e)}"
            )
    
    @staticmethod
    def get_schedule(
        schedule_id: int,
        db: Session = Depends(get_db)
    ) -> LabScheduleResponse:
        """Get lab schedule by ID"""
        try:
            service = LabScheduleService(db)
            schedule = service.get_schedule(schedule_id)
            return LabScheduleResponse.from_orm(schedule)
        except LabScheduleNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve schedule: {str(e)}"
            )
    
    @staticmethod
    def get_available_slots(
        schedule_date: date,
        technician_id: int = Query(None, description="Filter by technician ID"),
        db: Session = Depends(get_db)
    ) -> List[AvailableSlotResponse]:
        """Get available time slots"""
        try:
            service = LabScheduleService(db)
            slots = service.get_available_slots(schedule_date, technician_id)
            return [AvailableSlotResponse(**slot) for slot in slots]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get available slots: {str(e)}"
            )
    
    @staticmethod
    def get_technician_schedule(
        technician_id: int,
        schedule_date: date = Query(None, description="Filter by specific date"),
        db: Session = Depends(get_db)
    ) -> List[LabScheduleResponse]:
        """Get schedules for a technician"""
        try:
            service = LabScheduleService(db)
            schedules = service.get_technician_schedule(technician_id, schedule_date)
            return [LabScheduleResponse.from_orm(schedule) for schedule in schedules]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve technician schedule: {str(e)}"
            )
    
    @staticmethod
    def update_schedule_status(
        schedule_id: int,
        status_update: LabScheduleStatusUpdate,
        db: Session = Depends(get_db)
    ) -> LabScheduleResponse:
        """Update schedule status"""
        try:
            service = LabScheduleService(db)
            schedule = service.update_schedule_status(
                schedule_id,
                status_update.status,
                status_update.notes
            )
            return LabScheduleResponse.from_orm(schedule)
        except LabScheduleNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except LabSchedulingException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update schedule status: {str(e)}"
            )
    
    @staticmethod
    def get_home_collections(
        schedule_date: date = Query(None, description="Filter by specific date"),
        db: Session = Depends(get_db)
    ) -> List[LabScheduleResponse]:
        """Get home collection schedules"""
        try:
            service = LabScheduleService(db)
            schedules = service.get_home_collections(schedule_date)
            return [LabScheduleResponse.from_orm(schedule) for schedule in schedules]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve home collections: {str(e)}"
            )