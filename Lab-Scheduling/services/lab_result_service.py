"""
Lab Result Service
Business logic layer for lab result operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from repositories.lab_result_repository import LabResultRepository
from repositories.lab_order_repository import LabOrderRepository
from models.lab_result import LabResult, ResultStatus
from models.lab_order import OrderStatus
from exceptions import (
    LabResultNotFoundException,
    LabOrderNotFoundException,
    ResultValidationException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabResultService:
    """Service for lab result business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = LabResultRepository(db)
        self.order_repository = LabOrderRepository(db)
    
    def create_result(self, result_data: dict) -> LabResult:
        """Create a new lab result with validation"""
        try:
            # Validate required fields
            required_fields = ['order_id', 'test_id', 'result_value']
            for field in required_fields:
                if field not in result_data or result_data[field] is None:
                    raise LabSchedulingException(f"Missing required field: {field}")
            
            # Validate order exists and is in correct status
            order = self.order_repository.get_by_id(result_data['order_id'])
            if order.status not in [OrderStatus.IN_PROGRESS, OrderStatus.COMPLETED]:
                raise LabSchedulingException(f"Cannot add results for order with status {order.status.value}")
            
            # Validate and process result value
            self._validate_result_value(result_data)
            
            # Set default values
            result_data.setdefault('status', ResultStatus.PENDING_VERIFICATION)
            result_data.setdefault('created_at', datetime.utcnow())
            result_data.setdefault('updated_at', datetime.utcnow())
            
            # Determine if result is abnormal
            result_data['is_abnormal'] = self._check_abnormal_result(result_data)
            
            # Create the result
            result = self.repository.create(result_data)
            
            return result
            
        except (LabOrderNotFoundException, LabSchedulingException):
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to create lab result: {str(e)}")
    
    def get_result(self, result_id: int) -> LabResult:
        """Get lab result by ID"""
        return self.repository.get_by_id(result_id)
    
    def get_results_by_order(self, order_id: int) -> List[LabResult]:
        """Get all results for an order"""
        return self.repository.get_by_order_id(order_id)
    
    def get_results_by_test(self, test_id: int) -> List[LabResult]:
        """Get all results for a specific test"""
        return self.repository.get_by_test_id(test_id)
    
    def get_results_by_status(self, status: ResultStatus) -> List[LabResult]:
        """Get results by status"""
        return self.repository.get_by_status(status)
    
    def get_abnormal_results(self) -> List[LabResult]:
        """Get all abnormal results"""
        return self.repository.get_abnormal_results()
    
    def get_pending_verification(self) -> List[LabResult]:
        """Get results pending verification"""
        return self.repository.get_pending_verification()
    
    def verify_result(self, result_id: int, verified_by: int, verification_notes: str = None) -> LabResult:
        """Verify a lab result"""
        try:
            # Get current result
            result = self.repository.get_by_id(result_id)
            
            # Check if result can be verified
            if result.status != ResultStatus.PENDING_VERIFICATION:
                raise LabSchedulingException(f"Cannot verify result with status {result.status.value}")
            
            # Verify the result
            verified_result = self.repository.verify_result(result_id, verified_by, verification_notes)
            
            return verified_result
            
        except LabResultNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to verify result: {str(e)}")
    
    def update_result_status(self, result_id: int, status: ResultStatus) -> LabResult:
        """Update result status with validation"""
        try:
            # Get current result
            result = self.repository.get_by_id(result_id)
            
            # Validate status transition
            if not self._is_valid_status_transition(result.status, status):
                raise LabSchedulingException(
                    f"Invalid status transition from {result.status.value} to {status.value}"
                )
            
            return self.repository.update_status(result_id, status)
            
        except LabResultNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update result status: {str(e)}")
    
    def update_result(self, result_id: int, update_data: dict) -> LabResult:
        """Update lab result with validation"""
        try:
            # Get current result
            current_result = self.repository.get_by_id(result_id)
            
            # Check if result can be updated
            if current_result.status == ResultStatus.VERIFIED:
                raise LabSchedulingException("Cannot update verified results")
            
            # Validate result value if being updated
            if 'result_value' in update_data:
                self._validate_result_value(update_data)
                # Re-check if result is abnormal
                update_data['is_abnormal'] = self._check_abnormal_result(update_data)
            
            # Validate status transition if status is being updated
            if 'status' in update_data:
                if not self._is_valid_status_transition(current_result.status, update_data['status']):
                    raise LabSchedulingException(
                        f"Invalid status transition from {current_result.status.value} to {update_data['status'].value}"
                    )
            
            return self.repository.update(result_id, update_data)
            
        except LabResultNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update result: {str(e)}")
    
    def delete_result(self, result_id: int) -> bool:
        """Delete a lab result (only if not verified)"""
        try:
            result = self.repository.get_by_id(result_id)
            
            # Check if result can be deleted
            if result.status == ResultStatus.VERIFIED:
                raise LabSchedulingException("Cannot delete verified results")
            
            return self.repository.delete(result_id)
            
        except LabResultNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to delete result: {str(e)}")
    
    def get_patient_results(self, patient_id: int) -> List[LabResult]:
        """Get all results for a patient"""
        return self.repository.get_patient_results(patient_id)
    
    def search_results_by_value_range(self, test_id: int, min_value: float, max_value: float) -> List[LabResult]:
        """Search results by value range"""
        return self.repository.search_by_value_range(test_id, min_value, max_value)
    
    def get_all_results(self, skip: int = 0, limit: int = 100) -> List[LabResult]:
        """Get all results with pagination"""
        return self.repository.get_all(skip, limit)
    
    def bulk_verify_results(self, result_ids: List[int], verified_by: int) -> List[LabResult]:
        """Verify multiple results at once"""
        verified_results = []
        for result_id in result_ids:
            try:
                verified_result = self.verify_result(result_id, verified_by)
                verified_results.append(verified_result)
            except LabSchedulingException:
                # Skip results that cannot be verified
                continue
        return verified_results
    
    def _validate_result_value(self, result_data: dict) -> None:
        """Validate result value format and content"""
        result_value = result_data['result_value']
        
        if not result_value or str(result_value).strip() == '':
            raise ResultValidationException("Result value cannot be empty")
        
        # Try to convert to numeric if possible
        try:
            numeric_value = float(result_value)
            result_data['numeric_value'] = numeric_value
        except (ValueError, TypeError):
            # Non-numeric result, store as text
            result_data['numeric_value'] = None
        
        # Validate reference ranges if provided
        if 'reference_range_min' in result_data and 'reference_range_max' in result_data:
            try:
                min_val = float(result_data['reference_range_min'])
                max_val = float(result_data['reference_range_max'])
                if min_val >= max_val:
                    raise ResultValidationException("Invalid reference range: minimum must be less than maximum")
            except (ValueError, TypeError):
                raise ResultValidationException("Reference range values must be numeric")
    
    def _check_abnormal_result(self, result_data: dict) -> bool:
        """Check if result is abnormal based on reference ranges"""
        if 'numeric_value' not in result_data or result_data['numeric_value'] is None:
            return False
        
        numeric_value = result_data['numeric_value']
        min_range = result_data.get('reference_range_min')
        max_range = result_data.get('reference_range_max')
        
        if min_range is not None and max_range is not None:
            try:
                min_val = float(min_range)
                max_val = float(max_range)
                return numeric_value < min_val or numeric_value > max_val
            except (ValueError, TypeError):
                pass
        
        return False
    
    def _is_valid_status_transition(self, current_status: ResultStatus, new_status: ResultStatus) -> bool:
        """Validate if status transition is allowed"""
        valid_transitions = {
            ResultStatus.PENDING_VERIFICATION: [ResultStatus.VERIFIED, ResultStatus.REJECTED],
            ResultStatus.VERIFIED: [],  # Final state
            ResultStatus.REJECTED: [ResultStatus.PENDING_VERIFICATION]  # Can be resubmitted
        }
        
        return new_status in valid_transitions.get(current_status, [])