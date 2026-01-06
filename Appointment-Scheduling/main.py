"""
Main FastAPI Application for Appointment Scheduling Module
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import database initialization
from database import startup_db, init_db

# Import routers from your modules
from Appointment.Appointment_routes import router as appointment_router
from Doctor_Schedule.Doctor_Schedule_routes import router as doctor_schedule_router
from Blocked_Slots.Blocked_Slots_routes import router as blocked_slots_router

from Waiting_List.Waiting_List_routes import router as waiting_list_router
from Appointment_History.Appointment_History_routes import router as appointment_history_router
from Appointment_Reminder.Appointment_Reminder_routes import router as appointment_reminder_router


# ============ LIFESPAN EVENT (Database Initialization) ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event - runs on app startup and shutdown
    This is where we initialize the database as per project lead requirements
    """
    # STARTUP: Initialize database
    print("\n" + "=" * 60)
    print("🚀 FASTAPI APPLICATION STARTING UP")
    print("=" * 60)
    
    # Initialize database tables (as required by project lead)
    init_db()
    
    print("✅ Application startup complete!")
    print("=" * 60 + "\n")
    
    yield  # Application runs here
    
    # SHUTDOWN: Cleanup (if needed)
    print("\n🛑 Application shutting down...")


# ============ CREATE FASTAPI APP ============

app = FastAPI(
    title="Hospital Appointment Scheduling API",
    description="API for managing hospital appointments, doctor schedules, and blocked slots",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Add lifespan event
)

# CORS middleware (optional - for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ REGISTER ROUTERS ============

app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(doctor_schedule_router, prefix="/doctor-schedules", tags=["Doctor Schedules"])
app.include_router(blocked_slots_router, prefix="/blocked-slots", tags=["Blocked Slots"])

app.include_router(waiting_list_router, prefix="/waiting-list", tags=["Waiting List"])
app.include_router(appointment_history_router, prefix="/appointment-history", tags=["Appointment History"])
app.include_router(appointment_reminder_router, prefix="/appointment-reminders", tags=["Appointment Reminders"])


# ============ ROOT ENDPOINTS ============

@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API status"""
    return {
        "status": "Appointment Scheduling API running",
        "version": "1.0.0",
        "module": "Appointment Scheduling",
        "database": "initialized via Base.metadata.create_all()",
        "endpoints": {
            "appointments": "/appointments",
            "doctor_schedules": "/doctor-schedules",
            "blocked_slots": "/blocked-slots",
            "documentation": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Appointment Scheduling Module",
        "database": "connected",
        "initialization": "Base.metadata.create_all() executed"
    }


@app.get("/info", tags=["Info"])
def api_info():
    """API information"""
    return {
        "title": "Hospital Appointment Scheduling API",
        "version": "1.0.0",
        "description": "Manage appointments, doctor schedules, and blocked time slots",
        "database_initialization": "SQLAlchemy ORM (Base.metadata.create_all)",
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


# ============ RUN APPLICATION ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (disable in production)
    )
