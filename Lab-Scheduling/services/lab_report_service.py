"""
Lab Report Service
Business logic layer for lab report operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from repositories.lab_report_repository import LabReportRepository
from repositories.lab_result_repository import LabResultRepository
from repositories.lab_order_repository import LabOrderRepository
from models.lab_report import LabReport, ReportStatus
from models.lab_result import ResultStatus
from models.lab_order import OrderStatus
from exceptions import (
    LabReportNotFoundException,
    LabOrderNotFoundException,
    ReportFinalizedException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabReportService:
    """Service for lab report business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = LabReportRepository(db)
        self.result_repository = LabResultRepository(db)
        self.order_repository = LabOrderRepository(db)
    
    def create_report(self, report_data: dict) -> LabReport:
        """Create a new lab report with validation"""
        try:
            # Validate required fields
            required_fields = ['order_id']
            for field in required_fields:
                if field not in report_data or not report_data[field]:
                    raise LabSchedulingException(f"Missing required field: {field}")
            
            # Validate order exists and has results
            order = self.order_repository.get_by_id(report_data['order_id'])
            results = self.result_repository.get_by_order_id(report_data['order_id'])
            
            if not results:
                raise LabSchedulingException("Cannot create report for order without results")
            
            # Check if all results are verified
            unverified_results = [r for r in results if r.status != ResultStatus.VERIFIED]
            if unverified_results:
                raise LabSchedulingException("Cannot create report with unverified results")
            
            # Generate report content
            report_content = self._generate_report_content(order, results)
            
            # Set default values
            report_data.setdefault('status', ReportStatus.DRAFT)
            report_data.setdefault('summary', report_content['summary'])
            report_data.setdefault('findings', report_content['findings'])
            report_data.setdefault('recommendations', report_content['recommendations'])
            report_data.setdefault('created_at', datetime.utcnow())
            report_data.setdefault('updated_at', datetime.utcnow())
            
            # Create the report
            report = self.repository.create(report_data)
            
            return report
            
        except (LabOrderNotFoundException, LabSchedulingException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to create lab report: {str(e)}")
    
    def get_report(self, report_id: int) -> LabReport:
        """Get lab report by ID"""
        return self.repository.get_by_id(report_id)
    
    def get_report_by_order(self, order_id: int) -> Optional[LabReport]:
        """Get report for a specific order"""
        return self.repository.get_by_order_id(order_id)
    
    def get_patient_reports(self, patient_id: int) -> List[LabReport]:
        """Get all reports for a patient"""
        return self.repository.get_by_patient_id(patient_id)
    
    def get_reports_by_status(self, status: ReportStatus) -> List[LabReport]:
        """Get reports by status"""
        return self.repository.get_by_status(status)
    
    def get_finalized_reports(self) -> List[LabReport]:
        """Get all finalized reports"""
        return self.repository.get_finalized_reports()
    
    def get_pending_finalization(self) -> List[LabReport]:
        """Get reports pending finalization"""
        return self.repository.get_pending_finalization()
    
    def finalize_report(self, report_id: int, finalized_by: int) -> LabReport:
        """Finalize a lab report"""
        try:
            # Get current report
            report = self.repository.get_by_id(report_id)
            
            # Check if report can be finalized
            if report.status == ReportStatus.FINALIZED:
                raise ReportFinalizedException("Report is already finalized")
            
            # Validate that all results are still verified
            results = self.result_repository.get_by_order_id(report.order_id)
            unverified_results = [r for r in results if r.status != ResultStatus.VERIFIED]
            if unverified_results:
                raise LabSchedulingException("Cannot finalize report with unverified results")
            
            # Finalize the report
            finalized_report = self.repository.finalize_report(report_id, finalized_by)
            
            # Update order status to completed if not already
            order = self.order_repository.get_by_id(report.order_id)
            if order.status != OrderStatus.COMPLETED:
                self.order_repository.update_status(report.order_id, OrderStatus.COMPLETED)
            
            return finalized_report
            
        except (LabReportNotFoundException, ReportFinalizedException):
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to finalize report: {str(e)}")
    
    def update_report_status(self, report_id: int, status: ReportStatus) -> LabReport:
        """Update report status with validation"""
        try:
            # Get current report
            report = self.repository.get_by_id(report_id)
            
            # Check if report is finalized
            if report.status == ReportStatus.FINALIZED:
                raise ReportFinalizedException("Cannot update finalized report")
            
            # Validate status transition
            if not self._is_valid_status_transition(report.status, status):
                raise LabSchedulingException(
                    f"Invalid status transition from {report.status.value} to {status.value}"
                )
            
            return self.repository.update_status(report_id, status)
            
        except (LabReportNotFoundException, ReportFinalizedException):
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update report status: {str(e)}")
    
    def update_report(self, report_id: int, update_data: dict) -> LabReport:
        """Update lab report with validation"""
        try:
            # Get current report
            current_report = self.repository.get_by_id(report_id)
            
            # Check if report is finalized
            if current_report.status == ReportStatus.FINALIZED:
                raise ReportFinalizedException("Cannot update finalized report")
            
            # Validate status transition if status is being updated
            if 'status' in update_data:
                if not self._is_valid_status_transition(current_report.status, update_data['status']):
                    raise LabSchedulingException(
                        f"Invalid status transition from {current_report.status.value} to {update_data['status'].value}"
                    )
            
            return self.repository.update(report_id, update_data)
            
        except (LabReportNotFoundException, ReportFinalizedException):
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update report: {str(e)}")
    
    def delete_report(self, report_id: int) -> bool:
        """Delete a lab report (only if not finalized)"""
        try:
            report = self.repository.get_by_id(report_id)
            
            # Check if report can be deleted
            if report.status == ReportStatus.FINALIZED:
                raise ReportFinalizedException("Cannot delete finalized report")
            
            return self.repository.delete(report_id)
            
        except (LabReportNotFoundException, ReportFinalizedException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to delete report: {str(e)}")
    
    def get_all_reports(self, skip: int = 0, limit: int = 100) -> List[LabReport]:
        """Get all reports with pagination"""
        return self.repository.get_all(skip, limit)
    
    def get_reports_by_date_range(self, start_date: datetime, end_date: datetime) -> List[LabReport]:
        """Get reports within date range"""
        return self.repository.get_reports_by_date_range(start_date, end_date)
    
    def search_reports(self, query: str) -> List[LabReport]:
        """Search reports by summary or findings"""
        return self.repository.search_reports(query)
    
    def integrate_with_emr(self, report_id: int) -> LabReport:
        """Integrate report with EMR system"""
        try:
            report = self.repository.get_by_id(report_id)
            
            # Check if report is finalized
            if report.status != ReportStatus.FINALIZED:
                raise LabSchedulingException("Only finalized reports can be integrated with EMR")
            
            # Simulate EMR integration (in real implementation, this would call EMR API)
            update_data = {
                'emr_integrated': True,
                'emr_integration_date': datetime.utcnow()
            }
            
            return self.repository.update(report_id, update_data)
            
        except LabReportNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to integrate with EMR: {str(e)}")
    
    def get_emr_integrated_reports(self) -> List[LabReport]:
        """Get reports that have been integrated with EMR"""
        return self.repository.get_emr_integrated_reports()
    
    def regenerate_report(self, report_id: int) -> LabReport:
        """Regenerate report content based on current results"""
        try:
            report = self.repository.get_by_id(report_id)
            
            # Check if report can be regenerated
            if report.status == ReportStatus.FINALIZED:
                raise ReportFinalizedException("Cannot regenerate finalized report")
            
            # Get current results
            results = self.result_repository.get_by_order_id(report.order_id)
            order = self.order_repository.get_by_id(report.order_id)
            
            # Generate new content
            report_content = self._generate_report_content(order, results)
            
            # Update report
            update_data = {
                'summary': report_content['summary'],
                'findings': report_content['findings'],
                'recommendations': report_content['recommendations']
            }
            
            return self.repository.update(report_id, update_data)
            
        except (LabReportNotFoundException, ReportFinalizedException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to regenerate report: {str(e)}")
    
    def _generate_report_content(self, order, results) -> dict:
        """Generate report content based on order and results"""
        # Count abnormal results
        abnormal_results = [r for r in results if r.is_abnormal]
        
        # Generate summary
        summary = f"Laboratory report for {len(results)} test(s). "
        if abnormal_results:
            summary += f"{len(abnormal_results)} abnormal result(s) found."
        else:
            summary += "All results within normal ranges."
        
        # Generate findings
        findings = "Test Results:\n"
        for result in results:
            status_indicator = "⚠️ ABNORMAL" if result.is_abnormal else "✓ Normal"
            findings += f"- {result.test_name or f'Test ID {result.test_id}'}: {result.result_value} {result.unit or ''} [{status_indicator}]\n"
        
        # Generate recommendations
        recommendations = ""
        if abnormal_results:
            recommendations = "Recommendations:\n- Follow up with ordering physician for abnormal results\n- Consider repeat testing if clinically indicated"
        else:
            recommendations = "No specific recommendations. Results are within normal limits."
        
        return {
            'summary': summary,
            'findings': findings,
            'recommendations': recommendations
        }
    
    def _is_valid_status_transition(self, current_status: ReportStatus, new_status: ReportStatus) -> bool:
        """Validate if status transition is allowed"""
        valid_transitions = {
            ReportStatus.DRAFT: [ReportStatus.PENDING_FINALIZATION],
            ReportStatus.PENDING_FINALIZATION: [ReportStatus.FINALIZED, ReportStatus.DRAFT],
            ReportStatus.FINALIZED: []  # Final state
        }
        
        return new_status in valid_transitions.get(current_status, [])