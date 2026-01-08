"""
Lab Report Controller
HTTP request handling for lab report operations
"""

from typing import List
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from services.lab_report_service import LabReportService
from schemas.lab_report import (
    LabReportCreate,
    LabReportUpdate,
    LabReportResponse,
    LabReportFinalization
)
from models.lab_report import ReportStatus
from exceptions import (
    LabReportNotFoundException,
    ReportFinalizedException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabReportController:
    """Controller for lab report HTTP operations"""
    
    @staticmethod
    def create_report(
        report_data: LabReportCreate,
        db: Session = Depends(get_db)
    ) -> LabReportResponse:
        """Create a new lab report"""
        try:
            service = LabReportService(db)
            report = service.create_report(report_data.dict())
            return LabReportResponse.from_orm(report)
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
                detail=f"Failed to create report: {str(e)}"
            )
    
    @staticmethod
    def get_report(
        report_id: int,
        db: Session = Depends(get_db)
    ) -> LabReportResponse:
        """Get lab report by ID"""
        try:
            service = LabReportService(db)
            report = service.get_report(report_id)
            return LabReportResponse.from_orm(report)
        except LabReportNotFoundException as e:
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
                detail=f"Failed to retrieve report: {str(e)}"
            )
    
    @staticmethod
    def get_patient_reports(
        patient_id: int,
        db: Session = Depends(get_db)
    ) -> List[LabReportResponse]:
        """Get all reports for a patient"""
        try:
            service = LabReportService(db)
            reports = service.get_patient_reports(patient_id)
            return [LabReportResponse.from_orm(report) for report in reports]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve patient reports: {str(e)}"
            )
    
    @staticmethod
    def finalize_report(
        report_id: int,
        finalization: LabReportFinalization,
        db: Session = Depends(get_db)
    ) -> LabReportResponse:
        """Finalize a lab report"""
        try:
            service = LabReportService(db)
            report = service.finalize_report(report_id, finalization.finalized_by)
            return LabReportResponse.from_orm(report)
        except LabReportNotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except (ReportFinalizedException, LabSchedulingException) as e:
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
                detail=f"Failed to finalize report: {str(e)}"
            )
    
    @staticmethod
    def get_finalized_reports(
        db: Session = Depends(get_db)
    ) -> List[LabReportResponse]:
        """Get all finalized reports"""
        try:
            service = LabReportService(db)
            reports = service.get_finalized_reports()
            return [LabReportResponse.from_orm(report) for report in reports]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve finalized reports: {str(e)}"
            )
    
    @staticmethod
    def integrate_with_emr(
        report_id: int,
        db: Session = Depends(get_db)
    ) -> LabReportResponse:
        """Integrate report with EMR"""
        try:
            service = LabReportService(db)
            report = service.integrate_with_emr(report_id)
            return LabReportResponse.from_orm(report)
        except LabReportNotFoundException as e:
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
                detail=f"Failed to integrate with EMR: {str(e)}"
            )