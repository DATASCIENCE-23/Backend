from fastapi import FastAPI
from Patient_Registration_Management.database import Base, engine


from Patient_Registration_Management.user.models import User
from Patient_Registration_Management.specialization.models import Specialization
from Patient_Registration_Management.doctor.models import Doctor

from Patient_Registration_Management.doctor.routes import router as doctor_router

app = FastAPI(title="Hospital Management System")

Base.metadata.create_all(bind=engine)

app.include_router(doctor_router, prefix="/doctors", tags=["Doctors"])
