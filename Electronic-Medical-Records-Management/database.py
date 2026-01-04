from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:CloudComputing@localhost:5432/hospitalmanagement"

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-csearch_path=hms"}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# 🚨 IMPORT *ALL* ORM MODELS HERE
from User.User_model import User
from Role.Role_models import Role
from User_Role.User_Role_models import UserRole

from Patient.Patient_model import Patient      # ✅ THIS WAS MISSING
from Doctor.Doctor_models import Doctor
from Medical_Record.Medical_Record_model import MedicalRecord
from Report.Report_model import Report
from Prescription.Prescription_model import Prescription  # ✅ also required
from Aud_log.AuditLog_model import AuditLog
from Prescription_Item.Prescription_Item_model import PrescriptionItem 


from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
