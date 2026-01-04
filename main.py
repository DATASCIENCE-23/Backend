from fastapi import FastAPI
from Patient_Registration_Management.database import Base, engine

# ===== Import models =====
from Patient_Registration_Management.user.models import User
from Patient_Registration_Management.specialization.models import Specialization
from Patient_Registration_Management.doctor.models import Doctor
from Patient_Registration_Management.patient.patient_model import Patient
from Patient_Registration_Management.Address.address_model import Address
from Patient_Registration_Management.Insurance.Insurance_model import Insurance
from Patient_Registration_Management.Appointment.appointment_model import Appointment
from Patient_Registration_Management.Admission.admission_model import Admission

# ===== Import routers =====
from Patient_Registration_Management.user.routes import router as user_router
from Patient_Registration_Management.specialization.routes import router as specialization_router
from Patient_Registration_Management.doctor.routes import router as doctor_router
from Patient_Registration_Management.patient.patient_routes import router as patient_router
from Patient_Registration_Management.Address.address_router import router as address_router
from Patient_Registration_Management.Insurance.Insurance_routes import router as insurance_router
from Patient_Registration_Management.Admission.admission_routes import router as admission_router

app = FastAPI(
    title="Hospital Management System – Patient Registration",
    version="1.0.0"
)

# ===== Create tables =====
Base.metadata.create_all(bind=engine)

# ===== Register API routers =====
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(specialization_router, prefix="/specializations", tags=["Specialization"])
app.include_router(doctor_router, prefix="/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/patients", tags=["Patients"])
app.include_router(address_router, prefix="/addresses", tags=["Address"])
app.include_router(insurance_router, prefix="/insurance", tags=["Insurance"])
app.include_router(admission_router, prefix="/admissions", tags=["Admission"])
