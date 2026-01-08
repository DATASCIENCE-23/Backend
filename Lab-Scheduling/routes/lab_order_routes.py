"""
Lab Order Routes
FastAPI routes for lab order management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import get_db
from controllers.lab_order_controller import LabOrderController
from schemas.lab_order import (
    LabOrderCreate, 
    LabOrderResponse, 
    LabOrderUpdate,
    LabOrderStatusUpdate
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/lab-orders",
    tags=["Lab Orders"],
    responses={404: {"description": "Not found"}}
)

# Dependency to get controller
def get_lab_order_controller(db: Session = Depends(get_db)) -> LabOrderController:
    return LabOrderController(db)


@router.post(
    "/", 
    response_model=LabOrderResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create Lab Order",
    description="""
    Create a new laboratory test order from a doctor for a patient.
    
    This endpoint allows doctors to order specific laboratory tests for their patients.
    The order will be created with 'ordered' status and can later be scheduled for sample collection.
    
    **Required Fields:**
    - patient_id: Valid patient identifier
    - doctor_id: Valid doctor identifier
    
    **Optional Fields:**
    - record_id: Link to specific medical record
    - priority: Order priority (normal, urgent, stat)
    - clinical_notes: Additional clinical information
    
    **Business Rules:**
    - Patient and doctor must exist in the system
    - Priority defaults to 'normal' if not specified
    - Order date is automatically set to current timestamp
    """,
    responses={
        201: {
            "description": "Lab order created successfully",
            "model": LabOrderResponse
        },
        400: {
            "description": "Invalid input data or business rule violation",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Invalid patient_id",
                            "details": "Patient with ID 123 does not exist"
                        }
                    }
                }
            }
        },
        422: {
            "description": "Request validation failed",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Request validation failed",
                            "details": [
                                {
                                    "loc": ["body", "patient_id"],
                                    "msg": "ensure this value is greater than 0",
                                    "type": "value_error.number.not_gt"
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
)
async def create_lab_order(
    lab_order_data: LabOrderCreate,
    controller: LabOrderController = Depends(get_lab_order_controller)
):
    """Create a new lab order"""
    try:
        logger.info(f"Creating lab order for patient {lab_order_data.patient_id}")
        lab_order = controller.create_lab_order(lab_order_data)
        return lab_order
    except Exception as e:
        logger.error(f"Failed to create lab order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create lab order: {str(e)}"
        )


@router.get(
    "/patient/{patient_id}", 
    response_model=List[LabOrderResponse],
    summary="Get Patient Lab Orders",
    description="""
    Retrieve all laboratory orders for a specific patient.
    
    This endpoint returns a list of all lab orders associated with a patient,
    with optional filtering by order status.
    
    **Path Parameters:**
    - patient_id: Patient identifier (must be positive integer)
    
    **Query Parameters:**
    - status_filter: Optional status filter (ordered, scheduled, sample_collected, completed, cancelled)
    
    **Response:**
    - Returns paginated list of lab orders
    - Includes order details, priority, status, and timestamps
    - Empty list if no orders found for patient
    """,
    responses={
        200: {
            "description": "List of patient lab orders",
            "model": List[LabOrderResponse]
        },
        404: {
            "description": "Patient not found or no orders exist",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "PATIENT_NOT_FOUND",
                            "message": "Patient with ID 123 not found",
                            "details": "The specified patient does not exist in the system"
                        }
                    }
                }
            }
        }
    }
)
async def get_patient_lab_orders(
    patient_id: int,
    status_filter: Optional[str] = None,
    controller: LabOrderController = Depends(get_lab_order_controller)
):
    """Get all lab orders for a specific patient"""
    try:
        logger.info(f"Retrieving lab orders for patient {patient_id}")
        lab_orders = controller.get_patient_lab_orders(patient_id, status_filter)
        return lab_orders
    except Exception as e:
        logger.error(f"Failed to retrieve patient lab orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to retrieve lab orders: {str(e)}"
        )


@router.get(
    "/{order_id}", 
    response_model=LabOrderResponse,
    summary="Get Lab Order Details",
    description="""
    Retrieve detailed information for a specific laboratory order.
    
    This endpoint returns complete details for a single lab order including
    patient information, doctor details, test specifications, and current status.
    
    **Path Parameters:**
    - order_id: Lab order identifier (must be positive integer)
    
    **Response:**
    - Complete lab order information
    - Includes all order details and metadata
    - Returns 404 if order not found
    """,
    responses={
        200: {
            "description": "Lab order details",
            "model": LabOrderResponse
        },
        404: {
            "description": "Lab order not found",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "LAB_ORDER_NOT_FOUND",
                            "message": "Lab order with ID 123 not found",
                            "details": "The specified lab order does not exist or has been deleted"
                        }
                    }
                }
            }
        }
    }
)
async def get_lab_order(
    order_id: int,
    controller: LabOrderController = Depends(get_lab_order_controller)
):
    """Get a specific lab order by ID"""
    try:
        logger.info(f"Retrieving lab order {order_id}")
        lab_order = controller.get_lab_order(order_id)
        if not lab_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lab order {order_id} not found"
            )
        return lab_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve lab order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve lab order: {str(e)}"
        )


@router.put(
    "/{order_id}/status", 
    response_model=LabOrderResponse,
    summary="Update Lab Order Status",
    description="""
    Update the status of a laboratory order.
    
    This endpoint allows updating the status of a lab order as it progresses
    through the workflow (ordered → scheduled → sample_collected → completed).
    
    **Path Parameters:**
    - order_id: Lab order identifier (must be positive integer)
    
    **Request Body:**
    - status: New status value (ordered, scheduled, sample_collected, completed, cancelled)
    - notes: Optional notes explaining the status change
    
    **Business Rules:**
    - Status transitions must follow logical workflow
    - Cannot change status of cancelled orders
    - Completed orders cannot be modified
    - Status change is logged with timestamp
    """,
    responses={
        200: {
            "description": "Lab order status updated successfully",
            "model": LabOrderResponse
        },
        400: {
            "description": "Invalid status transition or business rule violation",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "INVALID_STATUS_TRANSITION",
                            "message": "Cannot change status from completed to ordered",
                            "details": "Status transitions must follow logical workflow"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Lab order not found",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "LAB_ORDER_NOT_FOUND",
                            "message": "Lab order with ID 123 not found",
                            "details": "The specified lab order does not exist"
                        }
                    }
                }
            }
        }
    }
)
async def update_lab_order_status(
    order_id: int,
    status_update: LabOrderStatusUpdate,
    controller: LabOrderController = Depends(get_lab_order_controller)
):
    """Update lab order status"""
    try:
        logger.info(f"Updating status for lab order {order_id} to {status_update.status}")
        lab_order = controller.update_lab_order_status(order_id, status_update.status)
        if not lab_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lab order {order_id} not found"
            )
        return lab_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update lab order status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update lab order status: {str(e)}"
        )


@router.get("/doctor/{doctor_id}", response_model=List[LabOrderResponse])
async def get_doctor_lab_orders(
    doctor_id: int,
    status_filter: Optional[str] = None,
    controller: LabOrderController = Depends(get_lab_order_controller)
):
    """Get all lab orders for a specific doctor"""
    try:
        logger.info(f"Retrieving lab orders for doctor {doctor_id}")
        lab_orders = controller.get_doctor_lab_orders(doctor_id, status_filter)
        return lab_orders
    except Exception as e:
        logger.error(f"Failed to retrieve doctor lab orders: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to retrieve lab orders: {str(e)}"
        )


@router.get("/priority/{priority}", response_model=List[LabOrderResponse])
async def get_orders_by_priority(
    priority: str,
    controller: LabOrderController = Depends(get_lab_order_controller)
):
    """Get lab orders by priority level"""
    try:
        logger.info(f"Retrieving lab orders with priority {priority}")
        lab_orders = controller.get_orders_by_priority(priority)
        return lab_orders
    except Exception as e:
        logger.error(f"Failed to retrieve orders by priority: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve orders by priority: {str(e)}"
        )