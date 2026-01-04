from fastapi import FastAPI

# Import routers from pharmacy module
from .medicine.medicine_routes import router as medicine_router
from .dispense.dispense_routes import router as dispense_router
from .pharmacist.pharmacist_routes import router as pharmacist_router
from .audit.audit_routes import router as audit_router

from Electronic_Medical_Records_Management.Prescription_Item.Prescription_Item_routes import router as prescription_item_router
from Electronic_Medical_Records_Management.Prescription.Prescription_routes import router as prescription_router

#check
from .User.User_routes import router as user_router
from .Role.Role_routes import router as role_router
from .User_Role.User_Role_routes import router as user_role_router
from .Doctor.Doctor_routes import router as doctor_router
from .Patient.Patient_routes import router as patient_router
from .Prescription.Prescription_routes import router as prescription_router
from .Prescription_Item.Prescription_Item_routes import router as prescription_item_router

from pharmacy_management.database import Base, engine  # ✅

app = FastAPI(
    title="Pharmacy Module API",
    version="0.1.0",
    description="Isolated Pharmacy module for testing",
)
Base.metadata.create_all(bind=engine)
# Include only pharmacy routers
app.include_router(medicine_router)
app.include_router(dispense_router)
app.include_router(pharmacist_router)
app.include_router(audit_router)
app.include_router(prescription_router)
app.include_router(prescription_item_router)


# Optional: simple health check
@app.get("/health")
def health_check():
    return {"status": "ok", "module": "pharmacy"}
