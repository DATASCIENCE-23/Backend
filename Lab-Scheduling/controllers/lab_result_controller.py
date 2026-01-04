"""
Lab Result Controller
HTTP request handling for lab result operations
"""

from typing import List
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from services.lab_result_service import LabResultService
from schemas.lab_result import (
    LabResultCreate,
    LabResultUpdate,
    LabResultResponse,
    LabResultVerification
)
from models.lab_result import ResultStatus
from exceptions import (
    LabResultNotFoundException,
    ResultValidationException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabResultController:
    """Controller for lab result HTTP operations"""
    
    @staticmethod
    def create_result(
        result_data: LabResultCreate,
        db: Session = Depends(get_db)
    ) -> LabResultResponse:
        """Create a new lab result"""
        try:
            service = LabResultService(db)
            result = service.create_result(result_data.dict())
            return LabResultResponse.from_orm(result)
        except (ResultValidationException, LabSchedulingException) as e:
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
                detail=f"Failed to create result: {str(e)}"
            )
    
    @staticmethod
    def get_result(
        result_id: int,
        db: Session = Depends(get_db)
    ) -> LabResultResponse:
        """Get lab result by ID"""
        try:
            service = LabResultService(db)
            result = service.get_result(result_id)
            return LabResultResponse.from_orm(result)
        except LabResultNotFoundException as e:
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
                detail=f"Failed to retrieve result: {str(e)}"
            )
    
    @staticmethod
    def get_results_by_order(
        order_id: int,
        db: Session = Depends(get_db)
    ) -> List[LabResultResponse]:
        """Get all results for an order"""
        try:
            service = LabResultService(db)
            results = service.get_results_by_order(order_id)
            return [LabResultResponse.from_orm(result) for result in results]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve results by order: {str(e)}"
            )
    
    @staticmethod
    def verify_result(
        result_id: int,
        verification: LabResultVerification,
        db: Session = Depends(get_db)
    ) -> LabResultResponse:
        """Verify a lab result"""
        try:
            service = LabResultService(db)
            result = service.verify_result(
                result_id,
                verification.verified_by,
                verification.verification_notes
            )
            return LabResultResponse.from_orm(result)
        except LabResultNotFoundException as e:
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
                detail=f"Failed to verify result: {str(e)}"
            )
    
    @staticmethod
    def get_abnormal_results(
        db: Session = Depends(get_db)
    ) -> List[LabResultResponse]:
        """Get all abnormal results"""
        try:
            service = LabResultService(db)
            results = service.get_abnormal_results()
            return [LabResultResponse.from_orm(result) for result in results]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve abnormal results: {str(e)}"
            )
    
    @staticmethod
    def get_pending_verification(
        db: Session = Depends(get_db)
    ) -> List[LabResultResponse]:
        """Get results pending verification"""
        try:
            service = LabResultService(db)
            results = service.get_pending_verification()
            return [LabResultResponse.from_orm(result) for result in results]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve pending verification results: {str(e)}"
            )