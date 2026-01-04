"""
Lab Report Routes
API endpoints for lab report operations
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from controllers.lab_report_controller import LabReportController
from schemas.lab_report import (
    LabReportCreate,
    LabReportUpdate,
    LabReportResponse,
    LabReportFinalization
)
from models.lab_report import ReportStatus

router = APIRouter(prefix="/lab-reports", tags=["Lab Reports"])

@router.post(
    "/",
    response_model=LabReportResponse,
    status_code=201,
    summary="Create Lab Report",
    description="Generate a comprehensive lab report from verified test results",
    response_description="Created lab report with summary and findings"
)
def create_report(
    report_data: LabReportCreate,
    db: Session = Depends(get_db)
):
    """
    Generate a comprehensive lab report from verified test results.
    
    This endpoint creates professional lab reports with:
    - Automated content generation from verified results
    - Clinical summary and findings
    - Abnormal value highlighting
    - Recommendations based on results
    - Integration-ready format for EMR systems
    
    **Requirements:**
    - All test results must be verified
    - Order must have completed sample collection
    - Results must pass quality control checks
    
    **Report Contents:**
    - Patient and order information
    - Complete test result panel
    - Reference ranges and abnormal flags
    - Clinical interpretation and recommendations
    """
    return LabReportController.create_report(report_data, db)

@router.get(
    "/{report_id}",
    response_model=LabReportResponse,
    summary="Get Lab Report",
    description="Retrieve a specific lab report by ID",
    response_description="Complete lab report with all sections"
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific lab report.
    
    Returns complete report information including:
    - Patient demographics and order details
    - Complete test result summary
    - Clinical findings and interpretations
    - Recommendations and follow-up suggestions
    - Report status and finalization details
    - EMR integration status
    """
    return LabReportController.get_report(report_id, db)

@router.get(
    "/patient/{patient_id}",
    response_model=List[LabReportResponse],
    summary="Get Patient Reports",
    description="Get all lab reports for a specific patient",
    response_description="List of patient's lab reports ordered by date"
)
def get_patient_reports(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all lab reports for a specific patient.
    
    This endpoint provides:
    - Complete patient lab history
    - Chronological report ordering
    - Trend analysis capabilities
    - Historical result comparison
    
    Useful for:
    - Patient care continuity
    - Clinical decision making
    - Longitudinal health monitoring
    - Medical record management
    """
    return LabReportController.get_patient_reports(patient_id, db)

@router.put(
    "/{report_id}/finalize",
    response_model=LabReportResponse,
    summary="Finalize Lab Report",
    description="Finalize a lab report for official release and EMR integration",
    response_description="Finalized lab report ready for distribution"
)
def finalize_report(
    report_id: int,
    finalization: LabReportFinalization,
    db: Session = Depends(get_db)
):
    """
    Finalize a lab report for official release.
    
    **Finalization Process:**
    - Final quality review and approval
    - Digital signature and timestamp
    - Report becomes immutable
    - Triggers EMR integration workflow
    - Enables patient and provider access
    
    **Requirements:**
    - All results must remain verified
    - Report content must be complete
    - Only authorized personnel can finalize
    - Finalization cannot be reversed
    
    **Post-Finalization:**
    - Report is available for distribution
    - EMR integration is enabled
    - Patient portal access is granted
    - Billing processes are triggered
    """
    return LabReportController.finalize_report(report_id, finalization, db)

@router.get(
    "/finalized/",
    response_model=List[LabReportResponse],
    summary="Get Finalized Reports",
    description="Get all finalized lab reports",
    response_description="List of finalized reports ready for distribution"
)
def get_finalized_reports(
    db: Session = Depends(get_db)
):
    """
    Get all finalized lab reports.
    
    This endpoint provides:
    - Official report archive
    - Distribution-ready reports
    - Quality assurance tracking
    - Performance metrics data
    
    **Use Cases:**
    - Report distribution management
    - Quality control auditing
    - Performance monitoring
    - Compliance reporting
    """
    return LabReportController.get_finalized_reports(db)

@router.put(
    "/{report_id}/integrate-emr",
    response_model=LabReportResponse,
    summary="Integrate with EMR",
    description="Integrate finalized report with Electronic Medical Records system",
    response_description="Report with EMR integration status updated"
)
def integrate_with_emr(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Integrate finalized report with EMR system.
    
    **Integration Process:**
    - Validates report is finalized
    - Formats data for EMR compatibility
    - Transmits report to EMR system
    - Updates integration status and timestamp
    - Handles integration errors and retries
    
    **Requirements:**
    - Report must be finalized
    - EMR system must be available
    - Patient must exist in EMR
    - Integration credentials must be valid
    
    **Benefits:**
    - Seamless clinical workflow
    - Reduced manual data entry
    - Improved care coordination
    - Enhanced patient safety
    """
    return LabReportController.integrate_with_emr(report_id, db)