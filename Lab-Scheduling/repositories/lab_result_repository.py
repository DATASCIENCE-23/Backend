"""
Lab Result Repository
Data access layer for lab result operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from models.lab_result import LabResult, ResultStatus
from exceptions import LabResultNotFoundException, DatabaseConnectionException


class LabResultRepository:
    """Repository for lab result data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, result_data: dict) -> LabResult:
        """Create a new lab result"""
        try:
            result = LabResult(**result_data)
            self.db.add(result)
            self.db.commit()
            self.db.refresh(result)
            return result
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to create lab result: {str(e)}")
    
    def get_by_id(self, result_id: int) -> LabResult:
        """Get lab result by ID"""
        try:
            result = self.db.query(LabResult).filter(LabResult.id == result_id).first()
            if not result:
                raise LabResultNotFoundException(f"Lab result with ID {result_id} not found")
            return result
        except LabResultNotFoundException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab result: {str(e)}")
    
    def get_by_order_id(self, order_id: int) -> List[LabResult]:
        """Get all lab results for an order"""
        try:
            return self.db.query(LabResult).filter(LabResult.order_id == order_id).order_by(LabResult.created_at).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve results by order: {str(e)}")
    
    def get_by_test_id(self, test_id: int) -> List[LabResult]:
        """Get all results for a specific test"""
        try:
            return self.db.query(LabResult).filter(LabResult.test_id == test_id).order_by(desc(LabResult.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve results by test: {str(e)}")
    
    def get_by_status(self, status: ResultStatus) -> List[LabResult]:
        """Get lab results by status"""
        try:
            return self.db.query(LabResult).filter(LabResult.status == status).order_by(desc(LabResult.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve results by status: {str(e)}")
    
    def get_abnormal_results(self) -> List[LabResult]:
        """Get all abnormal lab results"""
        try:
            return self.db.query(LabResult).filter(LabResult.is_abnormal == True).order_by(desc(LabResult.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve abnormal results: {str(e)}")
    
    def get_pending_verification(self) -> List[LabResult]:
        """Get results pending verification"""
        try:
            return self.db.query(LabResult).filter(LabResult.status == ResultStatus.PENDING_VERIFICATION).order_by(LabResult.created_at).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve pending verification results: {str(e)}")
    
    def update_status(self, result_id: int, status: ResultStatus) -> LabResult:
        """Update result status"""
        try:
            result = self.get_by_id(result_id)
            result.status = status
            result.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(result)
            return result
        except LabResultNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update result status: {str(e)}")
    
    def verify_result(self, result_id: int, verified_by: int, verification_notes: str = None) -> LabResult:
        """Verify a lab result"""
        try:
            result = self.get_by_id(result_id)
            result.status = ResultStatus.VERIFIED
            result.verified_by = verified_by
            result.verified_at = datetime.utcnow()
            if verification_notes:
                result.verification_notes = verification_notes
            result.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(result)
            return result
        except LabResultNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to verify result: {str(e)}")
    
    def update(self, result_id: int, update_data: dict) -> LabResult:
        """Update lab result"""
        try:
            result = self.get_by_id(result_id)
            for key, value in update_data.items():
                if hasattr(result, key):
                    setattr(result, key, value)
            result.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(result)
            return result
        except LabResultNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update result: {str(e)}")
    
    def delete(self, result_id: int) -> bool:
        """Delete lab result"""
        try:
            result = self.get_by_id(result_id)
            self.db.delete(result)
            self.db.commit()
            return True
        except LabResultNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to delete result: {str(e)}")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[LabResult]:
        """Get all lab results with pagination"""
        try:
            return self.db.query(LabResult).order_by(desc(LabResult.created_at)).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve results: {str(e)}")
    
    def search_by_value_range(self, test_id: int, min_value: float, max_value: float) -> List[LabResult]:
        """Search results by value range"""
        try:
            return self.db.query(LabResult).filter(
                and_(
                    LabResult.test_id == test_id,
                    LabResult.numeric_value >= min_value,
                    LabResult.numeric_value <= max_value
                )
            ).order_by(desc(LabResult.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to search results by value range: {str(e)}")
    
    def get_patient_results(self, patient_id: int) -> List[LabResult]:
        """Get all results for a patient through their orders"""
        try:
            from models.lab_order import LabOrder
            return self.db.query(LabResult).join(LabOrder).filter(
                LabOrder.patient_id == patient_id
            ).order_by(desc(LabResult.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve patient results: {str(e)}")