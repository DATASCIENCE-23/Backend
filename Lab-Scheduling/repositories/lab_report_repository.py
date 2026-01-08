"""
Lab Report Repository
Data access layer for lab report operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from models.lab_report import LabReport, ReportStatus
from exceptions import LabReportNotFoundException, DatabaseConnectionException


class LabReportRepository:
    """Repository for lab report data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, report_data: dict) -> LabReport:
        """Create a new lab report"""
        try:
            report = LabReport(**report_data)
            self.db.add(report)
            self.db.commit()
            self.db.refresh(report)
            return report
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to create lab report: {str(e)}")
    
    def get_by_id(self, report_id: int) -> LabReport:
        """Get lab report by ID"""
        try:
            report = self.db.query(LabReport).filter(LabReport.id == report_id).first()
            if not report:
                raise LabReportNotFoundException(f"Lab report with ID {report_id} not found")
            return report
        except LabReportNotFoundException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab report: {str(e)}")
    
    def get_by_order_id(self, order_id: int) -> Optional[LabReport]:
        """Get lab report by order ID"""
        try:
            return self.db.query(LabReport).filter(LabReport.order_id == order_id).first()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve report by order: {str(e)}")
    
    def get_by_patient_id(self, patient_id: int) -> List[LabReport]:
        """Get all lab reports for a patient"""
        try:
            from models.lab_order import LabOrder
            return self.db.query(LabReport).join(LabOrder).filter(
                LabOrder.patient_id == patient_id
            ).order_by(desc(LabReport.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve patient reports: {str(e)}")
    
    def get_by_status(self, status: ReportStatus) -> List[LabReport]:
        """Get lab reports by status"""
        try:
            return self.db.query(LabReport).filter(LabReport.status == status).order_by(desc(LabReport.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve reports by status: {str(e)}")
    
    def get_finalized_reports(self) -> List[LabReport]:
        """Get all finalized lab reports"""
        try:
            return self.db.query(LabReport).filter(LabReport.status == ReportStatus.FINALIZED).order_by(desc(LabReport.finalized_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve finalized reports: {str(e)}")
    
    def get_pending_finalization(self) -> List[LabReport]:
        """Get reports pending finalization"""
        try:
            return self.db.query(LabReport).filter(LabReport.status == ReportStatus.PENDING_FINALIZATION).order_by(LabReport.created_at).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve pending finalization reports: {str(e)}")
    
    def finalize_report(self, report_id: int, finalized_by: int) -> LabReport:
        """Finalize a lab report"""
        try:
            report = self.get_by_id(report_id)
            report.status = ReportStatus.FINALIZED
            report.finalized_by = finalized_by
            report.finalized_at = datetime.utcnow()
            report.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(report)
            return report
        except LabReportNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to finalize report: {str(e)}")
    
    def update_status(self, report_id: int, status: ReportStatus) -> LabReport:
        """Update report status"""
        try:
            report = self.get_by_id(report_id)
            report.status = status
            report.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(report)
            return report
        except LabReportNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update report status: {str(e)}")
    
    def update(self, report_id: int, update_data: dict) -> LabReport:
        """Update lab report"""
        try:
            report = self.get_by_id(report_id)
            for key, value in update_data.items():
                if hasattr(report, key):
                    setattr(report, key, value)
            report.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(report)
            return report
        except LabReportNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update report: {str(e)}")
    
    def delete(self, report_id: int) -> bool:
        """Delete lab report"""
        try:
            report = self.get_by_id(report_id)
            self.db.delete(report)
            self.db.commit()
            return True
        except LabReportNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to delete report: {str(e)}")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[LabReport]:
        """Get all lab reports with pagination"""
        try:
            return self.db.query(LabReport).order_by(desc(LabReport.created_at)).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve reports: {str(e)}")
    
    def get_reports_by_date_range(self, start_date: datetime, end_date: datetime) -> List[LabReport]:
        """Get reports within date range"""
        try:
            return self.db.query(LabReport).filter(
                and_(
                    LabReport.created_at >= start_date,
                    LabReport.created_at <= end_date
                )
            ).order_by(desc(LabReport.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve reports by date range: {str(e)}")
    
    def search_reports(self, query: str) -> List[LabReport]:
        """Search reports by summary or findings"""
        try:
            return self.db.query(LabReport).filter(
                or_(
                    LabReport.summary.ilike(f"%{query}%"),
                    LabReport.findings.ilike(f"%{query}%")
                )
            ).order_by(desc(LabReport.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to search reports: {str(e)}")
    
    def get_emr_integrated_reports(self) -> List[LabReport]:
        """Get reports that have been integrated with EMR"""
        try:
            return self.db.query(LabReport).filter(LabReport.emr_integrated == True).order_by(desc(LabReport.emr_integration_date)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve EMR integrated reports: {str(e)}")