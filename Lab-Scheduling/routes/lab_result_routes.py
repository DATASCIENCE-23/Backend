"""
Lab Result Routes
API endpoints for lab result operations
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from controllers.lab_result_controller import LabResultController
from schemas.lab_result import (
    LabResultCreate,
    LabResultUpdate,
    LabResultResponse,
    LabResultVerification
)
from models.lab_result import ResultStatus

router = APIRouter(prefix="/lab-results", tags=["Lab Results"])

@router.post(
    "/",
    response_model=LabResultResponse,
    status_code=201,
    summary="Create Lab Result",
    description="Enter a new lab test result with validation and abnormal value detection",
    response_description="Created lab result with validation status"
)
def create_result(
    result_data: LabResultCreate,
    db: Session = Depends(get_db)
):
    """
    Enter a new lab test result.
    
    This endpoint allows lab staff to enter test results with:
    - Automatic validation against reference ranges
    - Abnormal value detection and flagging
    - Support for both numeric and text results
    - Quality control and verification workflow
    
    **Business Rules:**
    - Order must be in IN_PROGRESS or COMPLETED status
    - Result values are validated for format and content
    - Abnormal results are automatically flagged
    - All results require verification before reporting
    """
    return LabResultController.create_result(result_data, db)

@router.get(
    "/{result_id}",
    response_model=LabResultResponse,
    summary="Get Lab Result",
    description="Retrieve a specific lab result by ID",
    response_description="Lab result details with verification status"
)
def get_result(
    result_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific lab result.
    
    Returns complete result information including:
    - Test result value and units
    - Reference ranges and abnormal flags
    - Verification status and notes
    - Quality control information
    - Timestamps for result entry and verification
    """
    return LabResultController.get_result(result_id, db)

@router.get(
    "/order/{order_id}",
    response_model=List[LabResultResponse],
    summary="Get Results by Order",
    description="Get all lab results for a specific order",
    response_description="List of all results for the order"
)
def get_results_by_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all lab results for a specific order.
    
    This endpoint provides:
    - Complete result panel for an order
    - Results grouped by test type
    - Verification status for each result
    - Abnormal value highlighting
    
    Useful for:
    - Result review and verification
    - Report generation
    - Quality assurance checks
    """
    return LabResultController.get_results_by_order(order_id, db)

@router.put(
    "/{result_id}/verify",
    response_model=LabResultResponse,
    summary="Verify Lab Result",
    description="Verify a lab result for accuracy and clinical validity",
    response_description="Verified lab result"
)
def verify_result(
    result_id: int,
    verification: LabResultVerification,
    db: Session = Depends(get_db)
):
    """
    Verify a lab result for accuracy and clinical validity.
    
    **Verification Process:**
    - Reviews result value against reference ranges
    - Confirms abnormal value flags are appropriate
    - Adds verification notes if needed
    - Updates result status to VERIFIED
    - Records verifying technician and timestamp
    
    **Requirements:**
    - Result must be in PENDING_VERIFICATION status
    - Only authorized personnel can verify results
    - Verification notes are optional but recommended for abnormal results
    """
    return LabResultController.verify_result(result_id, verification, db)

@router.get(
    "/abnormal/",
    response_model=List[LabResultResponse],
    summary="Get Abnormal Results",
    description="Get all lab results flagged as abnormal",
    response_description="List of abnormal lab results requiring attention"
)
def get_abnormal_results(
    db: Session = Depends(get_db)
):
    """
    Get all lab results flagged as abnormal.
    
    This endpoint helps with:
    - Critical value management
    - Quality assurance review
    - Clinical decision support
    - Priority result handling
    
    **Abnormal Result Criteria:**
    - Values outside reference ranges
    - Critical high or low values
    - Unexpected result patterns
    - Quality control failures
    """
    return LabResultController.get_abnormal_results(db)

@router.get(
    "/pending-verification/",
    response_model=List[LabResultResponse],
    summary="Get Pending Verification",
    description="Get all results awaiting verification",
    response_description="List of results pending verification"
)
def get_pending_verification(
    db: Session = Depends(get_db)
):
    """
    Get all results awaiting verification.
    
    This endpoint supports:
    - Verification workflow management
    - Quality control processes
    - Workload distribution
    - Performance monitoring
    
    **Verification Queue:**
    - Results ordered by entry time
    - Priority given to abnormal results
    - Batch verification capabilities
    - Verification assignment tracking
    """
    return LabResultController.get_pending_verification(db)