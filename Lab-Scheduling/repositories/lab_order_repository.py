"""
Lab Order Repository
Data access layer for lab order operations
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime

from models.lab_order import LabOrder, OrderStatus, OrderPriority
from exceptions import LabOrderNotFoundException, DatabaseConnectionException


class LabOrderRepository:
    """Repository for lab order data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, lab_order_data: dict) -> LabOrder:
        """Create a new lab order"""
        try:
            lab_order = LabOrder(**lab_order_data)
            self.db.add(lab_order)
            self.db.commit()
            self.db.refresh(lab_order)
            return lab_order
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to create lab order: {str(e)}")
    
    def get_by_id(self, order_id: int) -> LabOrder:
        """Get lab order by ID"""
        try:
            lab_order = self.db.query(LabOrder).filter(LabOrder.id == order_id).first()
            if not lab_order:
                raise LabOrderNotFoundException(f"Lab order with ID {order_id} not found")
            return lab_order
        except LabOrderNotFoundException:
            raise
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab order: {str(e)}")
    
    def get_by_patient_id(self, patient_id: int) -> List[LabOrder]:
        """Get all lab orders for a patient"""
        try:
            return self.db.query(LabOrder).filter(LabOrder.patient_id == patient_id).order_by(desc(LabOrder.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve patient lab orders: {str(e)}")
    
    def get_by_doctor_id(self, doctor_id: int) -> List[LabOrder]:
        """Get all lab orders by a doctor"""
        try:
            return self.db.query(LabOrder).filter(LabOrder.doctor_id == doctor_id).order_by(desc(LabOrder.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve doctor lab orders: {str(e)}")
    
    def get_by_status(self, status: OrderStatus) -> List[LabOrder]:
        """Get lab orders by status"""
        try:
            return self.db.query(LabOrder).filter(LabOrder.status == status).order_by(desc(LabOrder.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab orders by status: {str(e)}")
    
    def get_by_priority(self, priority: OrderPriority) -> List[LabOrder]:
        """Get lab orders by priority"""
        try:
            return self.db.query(LabOrder).filter(LabOrder.priority == priority).order_by(desc(LabOrder.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab orders by priority: {str(e)}")
    
    def get_pending_orders(self) -> List[LabOrder]:
        """Get all pending lab orders"""
        try:
            return self.db.query(LabOrder).filter(
                LabOrder.status.in_([OrderStatus.PENDING, OrderStatus.SCHEDULED])
            ).order_by(LabOrder.priority.desc(), LabOrder.created_at).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve pending lab orders: {str(e)}")
    
    def update_status(self, order_id: int, status: OrderStatus) -> LabOrder:
        """Update lab order status"""
        try:
            lab_order = self.get_by_id(order_id)
            lab_order.status = status
            lab_order.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(lab_order)
            return lab_order
        except LabOrderNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update lab order status: {str(e)}")
    
    def update(self, order_id: int, update_data: dict) -> LabOrder:
        """Update lab order"""
        try:
            lab_order = self.get_by_id(order_id)
            for key, value in update_data.items():
                if hasattr(lab_order, key):
                    setattr(lab_order, key, value)
            lab_order.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(lab_order)
            return lab_order
        except LabOrderNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to update lab order: {str(e)}")
    
    def delete(self, order_id: int) -> bool:
        """Delete lab order"""
        try:
            lab_order = self.get_by_id(order_id)
            self.db.delete(lab_order)
            self.db.commit()
            return True
        except LabOrderNotFoundException:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseConnectionException(f"Failed to delete lab order: {str(e)}")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[LabOrder]:
        """Get all lab orders with pagination"""
        try:
            return self.db.query(LabOrder).order_by(desc(LabOrder.created_at)).offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to retrieve lab orders: {str(e)}")
    
    def search(self, query: str) -> List[LabOrder]:
        """Search lab orders by clinical notes or test names"""
        try:
            return self.db.query(LabOrder).filter(
                or_(
                    LabOrder.clinical_notes.ilike(f"%{query}%"),
                    LabOrder.test_names.ilike(f"%{query}%")
                )
            ).order_by(desc(LabOrder.created_at)).all()
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to search lab orders: {str(e)}")