from fastapi import FastAPI
from Patient_Registration_Management.database import Base, engine


from Patient_Registration_Management.user.models import User
from Patient_Registration_Management.specialization.models import Specialization
from Patient_Registration_Management.doctor.models import Doctor

from Patient_Registration_Management.doctor.routes import router as doctor_router

from fastapi import FastAPI

# Import routers from pharmacy module
from .pharmacy_management.medicine.medicine_route import router as medicine_router
from .pharmacy_management.dispense.dispense_route import router as dispense_router
from .pharmacy_management.pharmacist.pharmacist_route import router as pharmacist_router
from .pharmacy_management.audit.audit_route import router as audit_router

app = FastAPI(
    title="Hospital Management System",
    version="0.1.0",
    description="Isolated Hospital Management System",
)



# Optional: simple health check
@app.get("/health")
def health_check():
    return {"status": "ok", "module": "pharmacy"}


app = FastAPI(title="Hospital Management System")

Base.metadata.create_all(bind=engine)

app.include_router(doctor_router, prefix="/doctors", tags=["Doctors"])

# Include only pharmacy routers
app.include_router(medicine_router)
app.include_router(dispense_router)
app.include_router(pharmacist_router)
app.include_router(audit_router)

