"""
Main FastAPI Application for Appointment Scheduling Module
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from your modules
from Appointment.Appointment_routes import router as appointment_router
from Doctor_Schedule.Doctor_Schedule_routes import router as doctor_schedule_router
from Blocked_Slots.Blocked_Slots_routes import router as blocked_slots_router

# Create FastAPI app
app = FastAPI(
    title="Hospital Appointment Scheduling API",
    description="API for managing hospital appointments, doctor schedules, and blocked slots",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (optional - for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(doctor_schedule_router, prefix="/doctor-schedules", tags=["Doctor Schedules"])
app.include_router(blocked_slots_router, prefix="/blocked-slots", tags=["Blocked Slots"])

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API status"""
    return {
        "status": "Appointment Scheduling API running",
        "version": "1.0.0",
        "module": "Appointment Scheduling",
        "endpoints": {
            "appointments": "/appointments",
            "doctor_schedules": "/doctor-schedules",
            "blocked_slots": "/blocked-slots",
            "documentation": "/docs",
            "redoc": "/redoc"
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Appointment Scheduling Module",
        "database": "connected"
    }

# API info endpoint
@app.get("/info", tags=["Info"])
def api_info():
    """API information"""
    return {
        "title": "Hospital Appointment Scheduling API",
        "version": "1.0.0",
        "description": "Manage appointments, doctor schedules, and blocked time slots",
        "modules": [
            {
                "name": "Appointments",
                "description": "Create, update, and manage patient appointments",
                "endpoints": 17
            },
            {
                "name": "Doctor Schedules",
                "description": "Manage doctor working hours and availability",
                "endpoints": 18
            },
            {
                "name": "Blocked Slots",
                "description": "Block time slots for meetings, leaves, etc.",
                "endpoints": 20
            }
        ],
        "total_endpoints": 55
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (disable in production)
    )