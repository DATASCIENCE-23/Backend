"""
Pharmacy Module - Main Application
FastAPI application setup with all route registrations
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging

from config import (
    get_settings, configure_middleware, setup_logging,
    init_db, PharmacyException, NotFoundException,
    DuplicateRecordException, InsufficientStockException,
    ValidationException, UnauthorizedException
)
from controller import (
    medicine_router, batch_router, prescription_router,
    dispense_router, health_router
)

# Setup logging
logger = setup_logging()


# ============ APPLICATION LIFESPAN ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting Pharmacy Module...")
    settings = get_settings()
    logger.info(f"Application: {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")

    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Pharmacy Module...")


# ============ CREATE APPLICATION ============

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Hospital Management System - Pharmacy Module API",
    docs_url="/api/pharmacy/docs",
    redoc_url="/api/pharmacy/redoc",
    openapi_url="/api/pharmacy/openapi.json",
    lifespan=lifespan
)

# Configure middleware
configure_middleware(app)


# ============ EXCEPTION HANDLERS ============

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """Handle not found exceptions"""
    logger.warning(f"Not found: {exc}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Resource not found",
            "details": str(exc),
            "success": False
        }
    )


@app.exception_handler(DuplicateRecordException)
async def duplicate_record_exception_handler(request: Request, exc: DuplicateRecordException):
    """Handle duplicate record exceptions"""
    logger.warning(f"Duplicate record: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Duplicate record",
            "details": str(exc),
            "success": False
        }
    )


@app.exception_handler(InsufficientStockException)
async def insufficient_stock_exception_handler(request: Request, exc: InsufficientStockException):
    """Handle insufficient stock exceptions"""
    logger.warning(f"Insufficient stock: {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Insufficient stock",
            "details": str(exc),
            "success": False
        }
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handle validation exceptions"""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation error",
            "details": str(exc),
            "success": False
        }
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    """Handle unauthorized exceptions"""
    logger.warning(f"Unauthorized: {exc}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Unauthorized",
            "details": str(exc),
            "success": False
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Request validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Invalid request data",
            "details": exc.errors(),
            "success": False
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": str(exc) if settings.DEBUG else "An error occurred",
            "success": False
        }
    )


# ============ REGISTER ROUTERS ============

# Include all API routers
app.include_router(health_router)
app.include_router(medicine_router)
app.include_router(batch_router)
app.include_router(prescription_router)
app.include_router(dispense_router)


# ============ ROOT ENDPOINTS ============

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/pharmacy/docs",
        "health": "/api/pharmacy/health"
    }


@app.get("/api/pharmacy/info", tags=["Root"])
async def api_info():
    """API information endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "REST API for Hospital Pharmacy Management",
        "endpoints": {
            "medicines": "/api/pharmacy/medicines",
            "batches": "/api/pharmacy/batches",
            "prescriptions": "/api/pharmacy/prescriptions",
            "dispense": "/api/pharmacy/dispense",
            "health": "/api/pharmacy/health"
        },
        "documentation": "/api/pharmacy/docs",
        "features": [
            "Medicine catalogue management",
            "Batch tracking with expiry dates",
            "Electronic prescription handling",
            "Stock validation before dispensing",
            "Automated inventory updates",
            "Low stock alerts",
            "Integration with billing module",
            "Audit logging"
        ]
    }


# ============ MIDDLEWARE FOR REQUEST LOGGING ============

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


# ============ RUN APPLICATION ============

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )

"""
==================== USAGE ====================

1. Install dependencies:
   pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic-settings python-jose[cryptography] passlib[bcrypt]

2. Set up environment variables (.env file):
   DATABASE_URL=postgresql://user:password@localhost:5432/hospital_pharmacy
   SECRET_KEY=your-secret-key-here
   DEBUG=True

3. Run the application:
   python main.py

   OR with uvicorn directly:
   uvicorn main:app --reload --port 8000

4. Access API documentation:
   - Swagger UI: http://localhost:8000/api/pharmacy/docs
   - ReDoc: http://localhost:8000/api/pharmacy/redoc

5. Test endpoints:
   curl http://localhost:8000/api/pharmacy/health

==================== API ENDPOINTS ====================

MEDICINE MANAGEMENT:
- POST   /api/pharmacy/medicines/              - Create medicine
- GET    /api/pharmacy/medicines/{id}          - Get medicine by ID
- PUT    /api/pharmacy/medicines/{id}          - Update medicine
- GET    /api/pharmacy/medicines/?search=term  - Search medicines
- GET    /api/pharmacy/medicines/stock/low     - Get low stock medicines

MEDICINE BATCHES:
- POST   /api/pharmacy/batches/                - Create batch
- GET    /api/pharmacy/batches/medicine/{id}   - Get batches by medicine

PRESCRIPTIONS:
- POST   /api/pharmacy/prescriptions/          - Create prescription (from doctor)
- GET    /api/pharmacy/prescriptions/pending   - Get pending prescriptions
- GET    /api/pharmacy/prescriptions/{id}      - Get prescription details
- GET    /api/pharmacy/prescriptions/{id}/validate-stock - Validate stock

DISPENSING:
- POST   /api/pharmacy/dispense/               - Dispense medicines
- GET    /api/pharmacy/dispense/{id}           - Get dispense details
- GET    /api/pharmacy/dispense/unbilled/list  - Get unbilled dispenses
- PUT    /api/pharmacy/dispense/{id}/mark-billed - Mark as billed

==================== INTEGRATION POINTS ====================

1. Doctor Module Integration (Prescription Creation):
   POST /api/pharmacy/prescriptions/
   {
     "patient_id": 1,
     "doctor_id": 1,
     "notes": "Take with food",
     "items": [
       {
         "medicine_id": 1,
         "prescribed_quantity": 30,
         "dosage": "500mg",
         "frequency": "Twice daily",
         "duration_days": 15,
         "instructions": "After meals"
       }
     ]
   }

2. Billing Module Integration (Get Unbilled Dispenses):
   GET /api/pharmacy/dispense/unbilled/list

   PUT /api/pharmacy/dispense/{id}/mark-billed?invoice_id=123

3. Inventory Module Integration (Low Stock Alert):
   GET /api/pharmacy/medicines/stock/low

==================== SECURITY ====================

All endpoints (except health check) require JWT authentication.
Include token in Authorization header:
Authorization: Bearer <your-jwt-token>

Role-based access control is implemented:
- pharmacist: Can manage medicines, view prescriptions, dispense
- admin: Full access
- doctor: Can create prescriptions
- billing: Can view unbilled dispenses, mark as billed
- inventory_manager: Can view low stock, manage batches

"""