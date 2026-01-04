from fastapi import FastAPI

# Import routers from pharmacy module
from .medicine.medicine_routes import router as medicine_router
from .dispense.dispense_routes import router as dispense_router
from .pharmacist.pharmacist_routes import router as pharmacist_router
from .audit.audit_routes import router as audit_router


app = FastAPI(
    title="Pharmacy Module API",
    version="0.1.0",
    description="Isolated Pharmacy module for testing",
)

# Include only pharmacy routers
app.include_router(medicine_router)
app.include_router(dispense_router)
app.include_router(pharmacist_router)
app.include_router(audit_router)


# Optional: simple health check
@app.get("/health")
def health_check():
    return {"status": "ok", "module": "pharmacy"}
