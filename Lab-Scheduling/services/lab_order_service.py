"""
Lab Order Service
Business logic layer for lab order operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from repositories.lab_order_repository import LabOrderRepository
from models.lab_order import LabOrder, OrderStatus, OrderPriority
from exceptions import (
    LabOrderNotFoundException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabOrderService:
    """Service for lab order business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = LabOrderRepository(db)
    
    def create_order(self, order_data: dict) -> LabOrder:
        """Create a new lab order with validation"""
        try:
            # Validate required fields
            required_fields = ['patient_id', 'doctor_id', 'medical_record_id', 'test_names']
            for field in required_fields:
                if field not in order_data or not order_data[field]:
                    raise LabSchedulingException(f"Missing required field: {field}")
            
            # Set default values
            order_data.setdefault('status', OrderStatus.PENDING)
            order_data.setdefault('priority', OrderPriority.NORMAL)
            order_data.setdefault('created_at', datetime.utcnow())
            order_data.setdefault('updated_at', datetime.utcnow())
            
            # Validate priority
            if 'priority' in order_data:
                if order_data['priority'] not in [p.value for p in OrderPriority]:
                    raise LabSchedulingException(f"Invalid priority: {order_data['priority']}")
            
            # Create the order
            return self.repository.create(order_data)
            
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to create lab order: {str(e)}")
    
    def get_order(self, order_id: int) -> LabOrder:
        """Get lab order by ID"""
        return self.repository.get_by_id(order_id)
    
    def get_patient_orders(self, patient_id: int) -> List[LabOrder]:
        """Get all orders for a patient"""
        return self.repository.get_by_patient_id(patient_id)
    
    def get_doctor_orders(self, doctor_id: int) -> List[LabOrder]:
        """Get all orders by a doctor"""
        return self.repository.get_by_doctor_id(doctor_id)
    
    def get_orders_by_status(self, status: OrderStatus) -> List[LabOrder]:
        """Get orders by status"""
        return self.repository.get_by_status(status)
    
    def get_orders_by_priority(self, priority: OrderPriority) -> List[LabOrder]:
        """Get orders by priority"""
        return self.repository.get_by_priority(priority)
    
    def get_pending_orders(self) -> List[LabOrder]:
        """Get all pending orders sorted by priority"""
        return self.repository.get_pending_orders()
    
    def update_order_status(self, order_id: int, status: OrderStatus, notes: str = None) -> LabOrder:
        """Update order status with business logic validation"""
        try:
            # Get current order
            order = self.repository.get_by_id(order_id)
            
            # Validate status transition
            if not self._is_valid_status_transition(order.status, status):
                raise LabSchedulingException(
                    f"Invalid status transition from {order.status.value} to {status.value}"
                )
            
            # Update status
            updated_order = self.repository.update_status(order_id, status)
            
            # Add notes if provided
            if notes:
                self.repository.update(order_id, {'clinical_notes': notes})
            
            return updated_order
            
        except LabOrderNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update order status: {str(e)}")
    
    def update_order(self, order_id: int, update_data: dict) -> LabOrder:
        """Update lab order with validation"""
        try:
            # Validate update data
            if 'status' in update_data:
                current_order = self.repository.get_by_id(order_id)
                if not self._is_valid_status_transition(current_order.status, update_data['status']):
                    raise LabSchedulingException(
                        f"Invalid status transition from {current_order.status.value} to {update_data['status'].value}"
                    )
            
            if 'priority' in update_data:
                if update_data['priority'] not in [p.value for p in OrderPriority]:
                    raise LabSchedulingException(f"Invalid priority: {update_data['priority']}")
            
            # Update the order
            return self.repository.update(order_id, update_data)
            
        except LabOrderNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update order: {str(e)}")
    
    def cancel_order(self, order_id: int, reason: str) -> LabOrder:
        """Cancel a lab order"""
        try:
            order = self.repository.get_by_id(order_id)
            
            # Check if order can be cancelled
            if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
                raise LabSchedulingException(f"Cannot cancel order with status {order.status.value}")
            
            # Update status and add cancellation reason
            update_data = {
                'status': OrderStatus.CANCELLED,
                'clinical_notes': f"CANCELLED: {reason}. Previous notes: {order.clinical_notes or ''}"
            }
            
            return self.repository.update(order_id, update_data)
            
        except LabOrderNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to cancel order: {str(e)}")
    
    def delete_order(self, order_id: int) -> bool:
        """Delete a lab order (only if not processed)"""
        try:
            order = self.repository.get_by_id(order_id)
            
            # Check if order can be deleted
            if order.status not in [OrderStatus.PENDING, OrderStatus.CANCELLED]:
                raise LabSchedulingException(
                    f"Cannot delete order with status {order.status.value}. Only pending or cancelled orders can be deleted."
                )
            
            return self.repository.delete(order_id)
            
        except LabOrderNotFoundException:
            raise
        except LabSchedulingException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to delete order: {str(e)}")
    
    def search_orders(self, query: str) -> List[LabOrder]:
        """Search orders by clinical notes or test names"""
        return self.repository.search(query)
    
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[LabOrder]:
        """Get all orders with pagination"""
        return self.repository.get_all(skip, limit)
    
    def get_urgent_orders(self) -> List[LabOrder]:
        """Get all urgent priority orders"""
        return self.repository.get_by_priority(OrderPriority.URGENT)
    
    def _is_valid_status_transition(self, current_status: OrderStatus, new_status: OrderStatus) -> bool:
        """Validate if status transition is allowed"""
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.SCHEDULED, OrderStatus.CANCELLED],
            OrderStatus.SCHEDULED: [OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED],
            OrderStatus.IN_PROGRESS: [OrderStatus.COMPLETED, OrderStatus.CANCELLED],
            OrderStatus.COMPLETED: [],  # Final state
            OrderStatus.CANCELLED: []   # Final state
        }
        
        return new_status in valid_transitions.get(current_status, [])