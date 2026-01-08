"""
Lab Order Controller
HTTP request handling for lab order operations
"""

from typing import List
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from services.lab_order_service import LabOrderService
from schemas.lab_order import (
    LabOrderCreate,
    LabOrderUpdate,
    LabOrderResponse,
    LabOrderStatusUpdate
)
from models.lab_order import OrderStatus, OrderPriority
from exceptions import (
    LabOrderNotFoundException,
    LabSchedulingException,
    DatabaseConnectionException
)


class LabOrderController:
    """Controller for lab order HTTP operations"""
    
    @staticmethod
    def create_order(
        order_data: LabOrderCreate,
        db: Session = Depends(get_db)
    ) -> LabOrderResponse:
        """Create a new lab order"""
        try:
            service = LabOrderService(db)
            order = service.create_order(order_data.dict())
            return LabOrderResponse.from_orm(order)
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
                detail=f"Failed to create lab order: {str(e)}"
            )
    
    @staticmethod
    def get_order(
        order_id: int,
        db: Session = Depends(get_db)
    ) -> LabOrderResponse:
        """Get lab order by ID"""
        try:
            service = LabOrderService(db)
            order = service.get_order(order_id)
            return LabOrderResponse.from_orm(order)
        except LabOrderNotFoundException as e:
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
                detail=f"Failed to retrieve lab order: {str(e)}"
            )
    
    @staticmethod
    def get_patient_orders(
        patient_id: int,
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get all orders for a patient"""
        try:
            service = LabOrderService(db)
            orders = service.get_patient_orders(patient_id)
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve patient orders: {str(e)}"
            )
    
    @staticmethod
    def get_doctor_orders(
        doctor_id: int,
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get all orders by a doctor"""
        try:
            service = LabOrderService(db)
            orders = service.get_doctor_orders(doctor_id)
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve doctor orders: {str(e)}"
            )
    
    @staticmethod
    def get_orders_by_status(
        order_status: OrderStatus,
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get orders by status"""
        try:
            service = LabOrderService(db)
            orders = service.get_orders_by_status(order_status)
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve orders by status: {str(e)}"
            )
    
    @staticmethod
    def get_orders_by_priority(
        priority: OrderPriority,
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get orders by priority"""
        try:
            service = LabOrderService(db)
            orders = service.get_orders_by_priority(priority)
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve orders by priority: {str(e)}"
            )
    
    @staticmethod
    def get_pending_orders(
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get all pending orders"""
        try:
            service = LabOrderService(db)
            orders = service.get_pending_orders()
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve pending orders: {str(e)}"
            )
    
    @staticmethod
    def get_urgent_orders(
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get all urgent orders"""
        try:
            service = LabOrderService(db)
            orders = service.get_urgent_orders()
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve urgent orders: {str(e)}"
            )
    
    @staticmethod
    def update_order_status(
        order_id: int,
        status_update: LabOrderStatusUpdate,
        db: Session = Depends(get_db)
    ) -> LabOrderResponse:
        """Update order status"""
        try:
            service = LabOrderService(db)
            order = service.update_order_status(
                order_id, 
                status_update.status, 
                status_update.notes
            )
            return LabOrderResponse.from_orm(order)
        except LabOrderNotFoundException as e:
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
                detail=f"Failed to update order status: {str(e)}"
            )
    
    @staticmethod
    def update_order(
        order_id: int,
        order_update: LabOrderUpdate,
        db: Session = Depends(get_db)
    ) -> LabOrderResponse:
        """Update lab order"""
        try:
            service = LabOrderService(db)
            order = service.update_order(order_id, order_update.dict(exclude_unset=True))
            return LabOrderResponse.from_orm(order)
        except LabOrderNotFoundException as e:
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
                detail=f"Failed to update order: {str(e)}"
            )
    
    @staticmethod
    def cancel_order(
        order_id: int,
        reason: str,
        db: Session = Depends(get_db)
    ) -> LabOrderResponse:
        """Cancel a lab order"""
        try:
            service = LabOrderService(db)
            order = service.cancel_order(order_id, reason)
            return LabOrderResponse.from_orm(order)
        except LabOrderNotFoundException as e:
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
                detail=f"Failed to cancel order: {str(e)}"
            )
    
    @staticmethod
    def delete_order(
        order_id: int,
        db: Session = Depends(get_db)
    ) -> dict:
        """Delete a lab order"""
        try:
            service = LabOrderService(db)
            success = service.delete_order(order_id)
            return {"message": "Order deleted successfully", "success": success}
        except LabOrderNotFoundException as e:
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
                detail=f"Failed to delete order: {str(e)}"
            )
    
    @staticmethod
    def search_orders(
        query: str = Query(..., description="Search query for clinical notes or test names"),
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Search orders by clinical notes or test names"""
        try:
            service = LabOrderService(db)
            orders = service.search_orders(query)
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to search orders: {str(e)}"
            )
    
    @staticmethod
    def get_all_orders(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
        db: Session = Depends(get_db)
    ) -> List[LabOrderResponse]:
        """Get all orders with pagination"""
        try:
            service = LabOrderService(db)
            orders = service.get_all_orders(skip, limit)
            return [LabOrderResponse.from_orm(order) for order in orders]
        except DatabaseConnectionException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve orders: {str(e)}"
            )