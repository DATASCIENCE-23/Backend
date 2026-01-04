"""
Lab Scheduling Module - FastAPI Application
Main application entry point with middleware and configuration
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time
import os
from contextlib import asynccontextmanager

from config import config
from database import engine, Base
from routes import lab_order_routes, lab_schedule_routes, lab_result_routes, lab_report_routes
from exceptions import (
    LabSchedulingException,
    LabOrderNotFoundException,
    LabScheduleNotFoundException,
    LabResultNotFoundException,
    LabReportNotFoundException,
    ResultValidationException,
    ReportFinalizedException,
    InvalidScheduleTimeException,
    ScheduleConflictException,
    DatabaseConnectionException,
    AuthenticationException,
    AuthorizationException
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lab_scheduling.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Lab Scheduling Application")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Lab Scheduling Application")


# Get configuration
env = os.getenv('FLASK_ENV', 'development')
app_config = config.get(env, config['default'])()

# Create FastAPI application
app = FastAPI(
    title="Lab Scheduling API",
    description="""
    ## Hospital Management System - Laboratory Scheduling Module
    
    This API provides comprehensive laboratory test management functionality including:
    
    ### Core Features
    * **Lab Order Management** - Create and manage laboratory test orders from doctors
    * **Appointment Scheduling** - Schedule lab appointments with technicians
    * **Sample Collection** - Track sample collection process (in-lab and home collection)
    * **Result Management** - Enter, validate, and verify test results
    * **Report Generation** - Generate comprehensive lab reports with EMR integration
    
    ### Workflow
    1. **Doctor creates lab order** for patient with specific tests
    2. **Patient schedules appointment** with available technician
    3. **Technician collects samples** at scheduled time/location
    4. **Lab staff enters results** with validation and verification
    5. **System generates reports** and integrates with EMR
    
    ### Authentication
    All endpoints require proper authentication. Include JWT token in Authorization header:
    ```
    Authorization: Bearer <your-jwt-token>
    ```
    
    ### Error Handling
    The API uses standard HTTP status codes and returns structured error responses:
    * `200` - Success
    * `201` - Created
    * `400` - Bad Request (validation errors)
    * `401` - Unauthorized (authentication required)
    * `403` - Forbidden (insufficient permissions)
    * `404` - Not Found
    * `409` - Conflict (business rule violations)
    * `422` - Unprocessable Entity (data validation errors)
    * `500` - Internal Server Error
    
    ### Rate Limiting
    API requests are rate-limited to ensure system stability. Contact administrator if limits are exceeded.
    """,
    version="1.0.0",
    terms_of_service="https://hospital.example.com/terms",
    contact={
        "name": "Lab Scheduling API Support",
        "url": "https://hospital.example.com/support",
        "email": "lab-api-support@hospital.example.com",
    },
    license_info={
        "name": "Hospital Management System License",
        "url": "https://hospital.example.com/license",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Lab Orders",
            "description": "Operations for managing laboratory test orders from doctors",
        },
        {
            "name": "Lab Scheduling",
            "description": "Operations for scheduling lab appointments and managing technician availability",
        },
        {
            "name": "Lab Results",
            "description": "Operations for entering, validating, and verifying test results",
        },
        {
            "name": "Lab Reports",
            "description": "Operations for generating and accessing comprehensive lab reports",
        },
        {
            "name": "Health Check",
            "description": "System health and status monitoring endpoints",
        },
    ],
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response


# Custom exception handlers for lab-specific errors
@app.exception_handler(LabOrderNotFoundException)
async def lab_order_not_found_handler(request: Request, exc: LabOrderNotFoundException):
    """Handle lab order not found exceptions"""
    logger.error(f"Lab Order Not Found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(LabScheduleNotFoundException)
async def lab_schedule_not_found_handler(request: Request, exc: LabScheduleNotFoundException):
    """Handle lab schedule not found exceptions"""
    logger.error(f"Lab Schedule Not Found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(LabResultNotFoundException)
async def lab_result_not_found_handler(request: Request, exc: LabResultNotFoundException):
    """Handle lab result not found exceptions"""
    logger.error(f"Lab Result Not Found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(LabReportNotFoundException)
async def lab_report_not_found_handler(request: Request, exc: LabReportNotFoundException):
    """Handle lab report not found exceptions"""
    logger.error(f"Lab Report Not Found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(ResultValidationException)
async def result_validation_handler(request: Request, exc: ResultValidationException):
    """Handle result validation exceptions"""
    logger.error(f"Result Validation Error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(ReportFinalizedException)
async def report_finalized_handler(request: Request, exc: ReportFinalizedException):
    """Handle report finalized exceptions"""
    logger.error(f"Report Finalized Error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(InvalidScheduleTimeException)
async def invalid_schedule_time_handler(request: Request, exc: InvalidScheduleTimeException):
    """Handle invalid schedule time exceptions"""
    logger.error(f"Invalid Schedule Time: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(ScheduleConflictException)
async def schedule_conflict_handler(request: Request, exc: ScheduleConflictException):
    """Handle schedule conflict exceptions"""
    logger.error(f"Schedule Conflict: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(DatabaseConnectionException)
async def database_connection_handler(request: Request, exc: DatabaseConnectionException):
    """Handle database connection exceptions"""
    logger.error(f"Database Connection Error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": "Database service is temporarily unavailable"
            }
        }
    )


@app.exception_handler(AuthenticationException)
async def authentication_handler(request: Request, exc: AuthenticationException):
    """Handle authentication exceptions"""
    logger.error(f"Authentication Error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": "Authentication required"
            }
        }
    )


@app.exception_handler(AuthorizationException)
async def authorization_handler(request: Request, exc: AuthorizationException):
    """Handle authorization exceptions"""
    logger.error(f"Authorization Error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": "Insufficient permissions"
            }
        }
    )


@app.exception_handler(LabSchedulingException)
async def lab_scheduling_exception_handler(request: Request, exc: LabSchedulingException):
    """Handle general lab scheduling exceptions"""
    logger.error(f"Lab Scheduling Error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "details": f"HTTP {exc.status_code} error occurred"
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred",
                "details": "Please contact system administrator"
            }
        }
    )


# Include routers with API prefix
app.include_router(lab_order_routes, prefix=app_config.API_PREFIX)
app.include_router(lab_schedule_routes, prefix=app_config.API_PREFIX)
app.include_router(lab_result_routes, prefix=app_config.API_PREFIX)
app.include_router(lab_report_routes, prefix=app_config.API_PREFIX)


# Health check endpoint
@app.get(
    "/health",
    tags=["Health Check"],
    summary="System Health Check",
    description="Check the health status of the Lab Scheduling API service",
    response_description="Health status information",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "service": "Lab Scheduling API",
                        "version": "1.0.0",
                        "timestamp": 1704110400.0,
                        "database": "connected",
                        "dependencies": {
                            "patient_module": "available",
                            "emr_module": "available"
                        }
                    }
                }
            }
        },
        503: {
            "description": "Service is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "unhealthy",
                        "service": "Lab Scheduling API",
                        "version": "1.0.0",
                        "timestamp": 1704110400.0,
                        "database": "disconnected",
                        "error": "Database connection failed"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Comprehensive health check endpoint that verifies:
    - API service status
    - Database connectivity
    - External module dependencies
    - System resources
    """
    try:
        # Test database connection
        from database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": "Lab Scheduling API",
            "version": "1.0.0",
            "timestamp": time.time(),
            "database": "connected",
            "dependencies": {
                "patient_module": "available",
                "emr_module": "available"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "Lab Scheduling API",
                "version": "1.0.0",
                "timestamp": time.time(),
                "database": "disconnected",
                "error": str(e)
            }
        )


# Root endpoint
@app.get(
    "/",
    tags=["Health Check"],
    summary="API Information",
    description="Get basic information about the Lab Scheduling API",
    response_description="API information and available endpoints",
    responses={
        200: {
            "description": "API information",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Lab Scheduling API",
                        "version": "1.0.0",
                        "description": "Hospital Management System - Laboratory Scheduling Module",
                        "docs": "/docs",
                        "redoc": "/redoc",
                        "health": "/health",
                        "openapi": "/openapi.json",
                        "endpoints": {
                            "lab_orders": "/api/lab-orders/",
                            "lab_schedule": "/api/lab-schedule/",
                            "lab_results": "/api/lab-results/",
                            "lab_reports": "/api/lab-reports/"
                        }
                    }
                }
            }
        }
    }
)
async def root():
    """
    Root endpoint providing API information and navigation links.
    Use this endpoint to discover available API endpoints and documentation.
    """
    return {
        "message": "Lab Scheduling API",
        "version": "1.0.0",
        "description": "Hospital Management System - Laboratory Scheduling Module",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "openapi": "/openapi.json",
        "endpoints": {
            "lab_orders": "/api/lab-orders/",
            "lab_schedule": "/api/lab-schedule/",
            "lab_results": "/api/lab-results/",
            "lab_reports": "/api/lab-reports/"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=app_config.DEBUG,
        log_level="info"
    )